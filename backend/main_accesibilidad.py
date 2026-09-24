"""
main_accesibilidad.py — Pipeline multimodal LSM + Agente + TTS.

La persona hace una seña con la mano → se clasifica con WML →
el agente RETyS responde → el ciudadano escucha la respuesta.

Uso:
  python main_accesibilidad.py

Controles (ventana de cámara):
  ESPACIO  — empezar/detener captura de señas
  Q        — salir
"""
import os
import sys
import time

import cv2
import mediapipe as mp

# Añadir el directorio padre al path para importar módulos del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_service import AgenteRETyS
from tts_service import hablar

# lsm_predictor puede no estar disponible si WML no está configurado
try:
    from lsm.lsm_predictor import reconocer_con_ventana
    LSM_DISPONIBLE = True
except Exception:  # noqa: BLE001
    LSM_DISPONIBLE = False

# ─────────────────────────────────────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────────────────────────────────────

TIMEOUT_GRABACION_SEG = 15   # Tiempo máximo de captura de señas por turno
VENTANA_FRAMES = 10          # Frames que se promedian para reducir ruido
UMBRAL_CONFIANZA = 0.7       # Confianza mínima para aceptar una seña

# Estados del pipeline
ESTADO_ESPERANDO = "ESPERANDO"
ESTADO_GRABANDO = "GRABANDO"
ESTADO_PROCESANDO = "PROCESANDO"

# ─────────────────────────────────────────────────────────────────────────────
# Utilidades de cámara y MediaPipe
# ─────────────────────────────────────────────────────────────────────────────

def _extraer_keypoints(hand_landmarks) -> list[float]:
    """Extrae 63 floats de un objeto hand_landmarks de MediaPipe."""
    puntos = []
    for lm in hand_landmarks.landmark:
        puntos.extend([lm.x, lm.y, lm.z])
    return puntos


def _dibujar_overlay(frame, estado: str, senas_acumuladas: list[str]) -> None:
    """Dibuja el estado y las señas acumuladas sobre el frame de cámara."""
    colores = {
        ESTADO_ESPERANDO:  (100, 100, 255),
        ESTADO_GRABANDO:   (0, 200, 0),
        ESTADO_PROCESANDO: (0, 200, 255),
    }
    color = colores.get(estado, (200, 200, 200))

    h = frame.shape[0]
    cv2.putText(frame, f"Estado: {estado}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
    cv2.putText(frame, f"Senas: {' '.join(senas_acumuladas) or '—'}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "ESPACIO = grabar/detener | Q = salir", (10, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)


# ─────────────────────────────────────────────────────────────────────────────
# Reconocimiento de señas en tiempo real
# ─────────────────────────────────────────────────────────────────────────────

def reconocer_en_tiempo_real(
    cap: cv2.VideoCapture,
    mp_hands,
    mp_draw,
    hands,
    timeout_seg: int = TIMEOUT_GRABACION_SEG,
) -> str:
    """
    Captura frames de cámara durante timeout_seg segundos y acumula señas
    reconocidas para formar una frase.

    Args:
        cap:         Objeto VideoCapture ya abierto.
        mp_hands:    Módulo mediapipe.solutions.hands.
        mp_draw:     Módulo mediapipe.solutions.drawing_utils.
        hands:       Instancia de mp_hands.Hands.
        timeout_seg: Duración máxima de captura.

    Returns:
        Frase de señas reconocidas separadas por espacio, o cadena vacía.
    """
    senas_acumuladas: list[str] = []
    buffer_frames: list[list[float]] = []
    ultima_sena: str | None = None
    inicio = time.time()

    while (time.time() - inicio) < timeout_seg:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = hands.process(frame_rgb)

        if resultado.multi_hand_landmarks:
            for hl in resultado.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hl, mp_hands.HAND_CONNECTIONS)
            kp = _extraer_keypoints(resultado.multi_hand_landmarks[0])
            buffer_frames.append(kp)

            # Procesar ventana cada VENTANA_FRAMES frames
            if len(buffer_frames) >= VENTANA_FRAMES:
                sena = reconocer_con_ventana(buffer_frames, umbral=UMBRAL_CONFIANZA)
                buffer_frames = []
                if sena and sena != ultima_sena:
                    senas_acumuladas.append(sena)
                    ultima_sena = sena
                    print(f"✋ Seña detectada: {sena}")

        # Overlay de tiempo restante
        restante = int(timeout_seg - (time.time() - inicio))
        cv2.putText(frame, f"Tiempo: {restante}s", (frame.shape[1] - 120, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        _dibujar_overlay(frame, ESTADO_GRABANDO, senas_acumuladas)
        cv2.imshow("Trámite Claro — LSM", frame)

        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord("q"):
            break
        elif tecla == ord(" "):
            break   # Detener grabación manualmente

    return " ".join(senas_acumuladas)


# ─────────────────────────────────────────────────────────────────────────────
# Procesamiento de la frase de señas
# ─────────────────────────────────────────────────────────────────────────────

def procesar_sena(frase_senas: str, agente: AgenteRETyS) -> None:
    """
    Envía la frase de señas al agente y reproduce la respuesta por voz.

    Args:
        frase_senas: Frase formada por las señas reconocidas.
        agente:      Instancia de AgenteRETyS.
    """
    print(f"\n🤲 Entendí: \"{frase_senas}\"")

    respuesta = agente.consultar(frase_senas, modo="voz")
    print(f"🔊 Respuesta: {respuesta}\n")

    try:
        hablar(respuesta)
    except Exception as exc:  # noqa: BLE001
        print(f"⚠️  No se pudo reproducir el audio: {exc}")


# ─────────────────────────────────────────────────────────────────────────────
# Loop principal
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    if not LSM_DISPONIBLE:
        print(
            "❌ El módulo LSM no está disponible.\n"
            "   Verifica que WML_LSM_DEPLOYMENT_ID esté configurado en .env\n"
            "   y que el modelo haya sido entrenado con lsm/train_lsm.py."
        )
        sys.exit(1)

    print("🖐️  Trámite Claro — Modo LSM (Lenguaje de Señas Mexicana)")
    print("   Presiona ESPACIO para empezar a grabar señas. Q para salir.\n")

    agente = AgenteRETyS()

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara.")
        sys.exit(1)

    estado = ESTADO_ESPERANDO

    try:
        hablar("Hola. Estoy listo para leer tus señas. Presiona la tecla de espacio para empezar.")
    except Exception:  # noqa: BLE001
        pass

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _dibujar_overlay(frame, estado, [])
        cv2.imshow("Trámite Claro — LSM", frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("q"):
            print("👋 Saliendo...")
            break

        elif tecla == ord(" ") and estado == ESTADO_ESPERANDO:
            estado = ESTADO_GRABANDO
            print(f"🎬 Grabando señas por {TIMEOUT_GRABACION_SEG} segundos...")

            frase = reconocer_en_tiempo_real(
                cap, mp_hands, mp_draw, hands, timeout_seg=TIMEOUT_GRABACION_SEG
            )

            if frase.strip():
                estado = ESTADO_PROCESANDO
                procesar_sena(frase, agente)
            else:
                print("⚠️  No se reconoció ninguna seña. Intenta de nuevo.")
                try:
                    hablar("No reconocí ninguna seña. Por favor intenta de nuevo.")
                except Exception:  # noqa: BLE001
                    pass

            estado = ESTADO_ESPERANDO

    cap.release()
    cv2.destroyAllWindows()
    hands.close()


if __name__ == "__main__":
    main()
