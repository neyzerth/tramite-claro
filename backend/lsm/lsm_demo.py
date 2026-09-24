#!/usr/bin/env python
"""
lsm_demo.py — Demostración en tiempo real de reconocimiento LSM.

Abre la cámara, detecta la mano con MediaPipe Tasks y clasifica la seña
usando el modelo entrenado (local o WML según el entorno).

Uso:
  source backend/lsm/venv312/bin/activate
  python backend/lsm/lsm_demo.py

Controles:
  Q  — salir
"""
import sys

if sys.version_info >= (3, 13):
    print(
        "❌ Requiere Python ≤3.12. Activa el venv:\n"
        "   source backend/lsm/venv312/bin/activate",
        file=sys.stderr,
    )
    sys.exit(1)

import os
import urllib.request
from collections import deque

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision

from lsm_predictor import predecir_sena, reconocer_con_ventana, _usar_wml

# ─────────────────────────────────────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────────────────────────────────────

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "hand_landmarker.task")
MODEL_URL  = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)

VENTANA_FRAMES = 15      # frames acumulados antes de emitir una predicción
UMBRAL_VOTO    = 0.55    # proporción mínima de votos en la ventana
UMBRAL_CONF    = 0.70    # confianza mínima por frame individual

# Grafo fijo de conexiones de los 21 landmarks de la mano
HAND_CONNECTIONS: list[tuple[int, int]] = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (0, 9), (9, 10), (10, 11), (11, 12),
    (0, 13), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17),
]

# Colores para cada seña (BGR)
COLORES_SENA: dict[str, tuple[int, int, int]] = {
    "hola":    (0, 220, 0),
    "gracias": (0, 180, 255),
    "ayuda":   (0, 60, 255),
    "si":      (180, 255, 0),
    "no":      (0, 0, 230),
}
COLOR_DEFAULT = (200, 200, 200)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers de dibujo
# ─────────────────────────────────────────────────────────────────────────────

def _dibujar_landmarks(frame: np.ndarray, landmarks, color=(0, 200, 200)) -> None:
    h, w = frame.shape[:2]
    for i, f in HAND_CONNECTIONS:
        x1, y1 = int(landmarks[i].x * w), int(landmarks[i].y * h)
        x2, y2 = int(landmarks[f].x * w), int(landmarks[f].y * h)
        cv2.line(frame, (x1, y1), (x2, y2), color, 2)
    for lm in landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        cv2.circle(frame, (cx, cy), 4, (255, 255, 255), -1)


def _extraer_keypoints(landmarks) -> list[float]:
    puntos: list[float] = []
    for lm in landmarks:
        puntos.extend([lm.x, lm.y, lm.z])
    return puntos


def _overlay(
    frame: np.ndarray,
    sena_actual: str | None,
    sena_ventana: str | None,
    mano_detectada: bool,
    n_frames_ventana: int,
) -> None:
    """Dibuja el panel de información sobre el frame."""
    h, w = frame.shape[:2]

    # Barra superior semitransparente
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 60), (30, 30, 30), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Seña confirmada (ventana de votos)
    if sena_ventana:
        color = COLORES_SENA.get(sena_ventana, COLOR_DEFAULT)
        cv2.putText(frame, f"✓ {sena_ventana.upper()}", (12, 44),
                    cv2.FONT_HERSHEY_DUPLEX, 1.4, color, 2)
    else:
        cv2.putText(frame, "—", (12, 44),
                    cv2.FONT_HERSHEY_DUPLEX, 1.0, (120, 120, 120), 1)

    # Predicción frame a frame (esquina superior derecha)
    if sena_actual:
        cv2.putText(frame, sena_actual, (w - 160, 36),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (180, 255, 180), 1)

    # Barra de progreso de la ventana
    barra_w = int((n_frames_ventana / VENTANA_FRAMES) * (w - 20))
    cv2.rectangle(frame, (10, h - 12), (10 + barra_w, h - 4), (0, 200, 100), -1)
    cv2.rectangle(frame, (10, h - 12), (w - 10, h - 4), (80, 80, 80), 1)

    # Indicador de mano
    estado_color = (0, 220, 0) if mano_detectada else (60, 60, 200)
    estado_txt   = "Mano detectada" if mano_detectada else "Sin mano"
    cv2.putText(frame, estado_txt, (12, h - 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, estado_color, 1)

    # Backend activo
    backend_txt = "WML" if _usar_wml() else "local"
    cv2.putText(frame, f"[{backend_txt}]", (w - 70, h - 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)

    # Tecla salir
    cv2.putText(frame, "Q: salir", (w - 80, h - 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (120, 120, 120), 1)


# ─────────────────────────────────────────────────────────────────────────────
# Descarga del modelo MediaPipe si falta
# ─────────────────────────────────────────────────────────────────────────────

def _descargar_modelo() -> None:
    if os.path.exists(MODEL_PATH):
        return
    os.makedirs(MODELS_DIR, exist_ok=True)
    print("⬇️  Descargando modelo MediaPipe Tasks (~8 MB)...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"✅ Modelo guardado en: {MODEL_PATH}")


# ─────────────────────────────────────────────────────────────────────────────
# Loop principal
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    _descargar_modelo()

    backend = "WML" if _usar_wml() else "local (Keras)"
    print(f"🔍 Backend de inferencia: {backend}")
    print("📷 Iniciando cámara... (Q para salir)\n")

    base_options = mp_tasks.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.6,
        min_tracking_confidence=0.6,
    )
    detector = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara.")
        detector.close()
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_idx = 0

    ventana: deque[list[float]] = deque(maxlen=VENTANA_FRAMES)
    sena_confirmada: str | None = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        timestamp_ms = int(frame_idx * (1000.0 / fps))

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image  = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        resultado = detector.detect_for_video(mp_image, timestamp_ms)

        mano_detectada = bool(resultado.hand_landmarks)
        sena_frame: str | None = None

        if mano_detectada:
            landmarks = resultado.hand_landmarks[0]
            color_landmarks = COLORES_SENA.get(sena_confirmada or "", COLOR_DEFAULT)
            _dibujar_landmarks(frame, landmarks, color=color_landmarks)

            kp = _extraer_keypoints(landmarks)
            ventana.append(kp)

            # Predicción por frame (sin ventana) para feedback visual inmediato
            sena_frame = predecir_sena(kp, umbral=UMBRAL_CONF)
        else:
            # Sin mano: vaciar ventana para evitar mezclar señas
            ventana.clear()

        # Predicción por votación en ventana completa
        if len(ventana) == VENTANA_FRAMES:
            nueva = reconocer_con_ventana(list(ventana), umbral=UMBRAL_VOTO)
            if nueva:
                if nueva != sena_confirmada:
                    print(f"🤚 Seña reconocida: {nueva.upper()}")
                sena_confirmada = nueva
                ventana.clear()  # reiniciar ventana tras confirmación

        _overlay(frame, sena_frame, sena_confirmada, mano_detectada, len(ventana))
        cv2.imshow("LSM — Reconocimiento en tiempo real", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    detector.close()
    print("\n👋 Demo finalizado.")


if __name__ == "__main__":
    main()
