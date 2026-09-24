"""
lsm_capture.py — Captura de dataset de Lenguaje de Señas Mexicana (LSM).

Abre la cámara, extrae keypoints de manos con MediaPipe y guarda
las muestras en dataset/keypoints.csv para entrenar el clasificador.

Uso:
  python lsm_capture.py              # graba todas las señas definidas en SENAS
  python lsm_capture.py --sena hola  # graba solo una seña específica

Controles:
  ESPACIO  — empezar/pausar grabación de la seña actual
  N        — pasar a la siguiente seña
  Q        — salir
"""
import argparse
import csv
import os
import time

import cv2
import mediapipe as mp
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────────────────────────────────────

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
DATASET_CSV = os.path.join(DATASET_DIR, "keypoints.csv")

# Señas básicas a capturar
SENAS = ["hola", "gracias", "ayuda", "si", "no"]

# MediaPipe entrega 21 puntos × 3 coordenadas = 63 valores por mano
N_KEYPOINTS = 63
MUESTRAS_POR_SENA = 200   # frames por seña para el dataset


# ─────────────────────────────────────────────────────────────────────────────
# Extracción de keypoints
# ─────────────────────────────────────────────────────────────────────────────

def extraer_keypoints(hand_landmarks) -> list[float]:
    """
    Convierte un resultado de MediaPipe Hands en una lista plana de 63 floats.

    Args:
        hand_landmarks: resultado de mp.solutions.hands procesado en un frame.

    Returns:
        Lista de 63 valores [x0,y0,z0, x1,y1,z1, ..., x20,y20,z20] en [0,1].
        Si no se detecta mano, devuelve 63 ceros.
    """
    if hand_landmarks is None:
        return [0.0] * N_KEYPOINTS

    puntos = []
    for lm in hand_landmarks.landmark:
        puntos.extend([lm.x, lm.y, lm.z])
    return puntos


# ─────────────────────────────────────────────────────────────────────────────
# Captura principal
# ─────────────────────────────────────────────────────────────────────────────

def capturar_dataset(senas: list[str]) -> None:
    """
    Abre la cámara y guarda muestras de keypoints en el CSV para cada seña.

    Args:
        senas: Lista de nombres de señas a capturar.
    """
    os.makedirs(DATASET_DIR, exist_ok=True)

    # Crear CSV con cabecera si no existe
    if not os.path.exists(DATASET_CSV):
        with open(DATASET_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            kp_cols = [f"kp_{i}" for i in range(N_KEYPOINTS)]
            writer.writerow(["sena"] + kp_cols)

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
        print("❌ No se pudo abrir la cámara. Verifica que esté conectada.")
        return

    for sena in senas:
        grabando = False
        muestras = 0
        print(f"\n📷 Seña: '{sena.upper()}' — Presiona ESPACIO para empezar")

        while muestras < MUESTRAS_POR_SENA:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resultado = hands.process(frame_rgb)

            # Dibujar landmarks si se detecta mano
            if resultado.multi_hand_landmarks:
                for hl in resultado.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hl, mp_hands.HAND_CONNECTIONS)

            # Overlay de estado
            estado_txt = f"GRABANDO ({muestras}/{MUESTRAS_POR_SENA})" if grabando else "EN PAUSA — ESPACIO para grabar"
            color = (0, 200, 0) if grabando else (0, 100, 255)
            cv2.putText(frame, f"SENA: {sena.upper()}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            cv2.putText(frame, estado_txt, (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(frame, "N = siguiente | Q = salir", (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            cv2.imshow("LSM — Captura de dataset", frame)

            # Guardar muestra si está grabando y hay mano detectada
            if grabando and resultado.multi_hand_landmarks:
                kp = extraer_keypoints(resultado.multi_hand_landmarks[0])
                with open(DATASET_CSV, "a", newline="") as f:
                    csv.writer(f).writerow([sena] + kp)
                muestras += 1

            # Teclas de control
            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord("q"):
                print("🛑 Captura cancelada por el usuario.")
                cap.release()
                cv2.destroyAllWindows()
                return
            elif tecla == ord("n"):
                print(f"⏭  Saltando seña '{sena}'")
                break
            elif tecla == ord(" "):
                grabando = not grabando

        print(f"✅ Seña '{sena}': {muestras} muestras guardadas.")

    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    print(f"\n🎉 Dataset guardado en: {DATASET_CSV}")


# ─────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Captura de dataset LSM")
    parser.add_argument(
        "--sena",
        type=str,
        default=None,
        help="Capturar solo una seña específica (ej: --sena hola)",
    )
    args = parser.parse_args()

    lista = [args.sena] if args.sena else SENAS
    capturar_dataset(lista)
