#!/usr/bin/env python
"""
lsm_capture.py — Captura de dataset de Lenguaje de Señas Mexicana (LSM).

Abre la cámara, extrae keypoints de manos con MediaPipe Tasks (API 1.x) y guarda
las muestras en dataset/keypoints.csv para entrenar el clasificador.

Uso:
  # Activar el venv de Python 3.12 ANTES de ejecutar:
  source lsm/venv312/bin/activate
  python lsm/lsm_capture.py              # graba todas las señas de SENAS
  python lsm/lsm_capture.py --sena hola  # graba solo una seña específica

Controles:
  ESPACIO  — empezar/pausar grabación de la seña actual
  N        — pasar a la siguiente seña
  Q        — salir

Nota: La primera ejecución descarga el modelo hand_landmarker.task (~8 MB)
      en lsm/models/ automáticamente.
"""
import argparse
import csv
import os
import sys
import urllib.request

# ─────────────────────────────────────────────────────────────────────────────
# Guardia de versión — mediapipe requiere Python <=3.12
# ─────────────────────────────────────────────────────────────────────────────

if sys.version_info >= (3, 13):
    print(
        "❌ ERROR: este script requiere Python ≤3.12.\n"
        "   mediapipe no tiene soporte para Python 3.13+.\n\n"
        "   Activa el venv correcto antes de ejecutar:\n"
        "     source backend/lsm/venv312/bin/activate\n"
        "     python backend/lsm/lsm_capture.py",
        file=sys.stderr,
    )
    sys.exit(1)

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision

# ─────────────────────────────────────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────────────────────────────────────

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
DATASET_CSV = os.path.join(DATASET_DIR, "keypoints.csv")

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "hand_landmarker.task")
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)

# Señas básicas a capturar
SENAS = ["hola", "gracias", "ayuda", "si", "no"]

# MediaPipe entrega 21 puntos × 3 coordenadas = 63 valores por mano
N_KEYPOINTS = 63
MUESTRAS_POR_SENA = 200   # frames por seña para el dataset

# Grafo de conexiones fijo de los 21 landmarks de la mano (no cambia nunca).
# Fuente: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
HAND_CONNECTIONS: list[tuple[int, int]] = [
    (0, 1), (1, 2), (2, 3), (3, 4),          # pulgar
    (0, 5), (5, 6), (6, 7), (7, 8),           # índice
    (0, 9), (9, 10), (10, 11), (11, 12),      # medio
    (0, 13), (13, 14), (14, 15), (15, 16),    # anular
    (0, 17), (17, 18), (18, 19), (19, 20),    # meñique
    (5, 9), (9, 13), (13, 17),                # nudillos
]


# ─────────────────────────────────────────────────────────────────────────────
# Descarga automática del modelo
# ─────────────────────────────────────────────────────────────────────────────

def _descargar_modelo() -> None:
    """Descarga hand_landmarker.task si no existe en models/."""
    if os.path.exists(MODEL_PATH):
        return
    os.makedirs(MODELS_DIR, exist_ok=True)
    print("⬇️  Descargando modelo MediaPipe Tasks (~8 MB)...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"✅ Modelo guardado en: {MODEL_PATH}")


# ─────────────────────────────────────────────────────────────────────────────
# Extracción de keypoints
# ─────────────────────────────────────────────────────────────────────────────

def extraer_keypoints(hand_landmarks) -> list[float]:
    """
    Convierte una lista de NormalizedLandmark de MediaPipe Tasks en 63 floats.

    Args:
        hand_landmarks: lista de 21 NormalizedLandmark del HandLandmarkerResult,
                        o None si no se detectó mano.

    Returns:
        Lista de 63 valores [x0,y0,z0, x1,y1,z1, ..., x20,y20,z20] en [0,1].
        Si no se detecta mano, devuelve 63 ceros.
    """
    if hand_landmarks is None:
        return [0.0] * N_KEYPOINTS

    puntos: list[float] = []
    for lm in hand_landmarks:
        puntos.extend([lm.x, lm.y, lm.z])
    return puntos


# ─────────────────────────────────────────────────────────────────────────────
# Dibujo de landmarks
# ─────────────────────────────────────────────────────────────────────────────

def _dibujar_landmarks(frame: np.ndarray, landmarks) -> None:
    """Dibuja los 21 landmarks y sus conexiones sobre el frame BGR."""
    h, w = frame.shape[:2]
    for inicio, fin in HAND_CONNECTIONS:
        x1 = int(landmarks[inicio].x * w)
        y1 = int(landmarks[inicio].y * h)
        x2 = int(landmarks[fin].x * w)
        y2 = int(landmarks[fin].y * h)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 200, 200), 2)
    for lm in landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        cv2.circle(frame, (cx, cy), 4, (255, 255, 255), -1)


# ─────────────────────────────────────────────────────────────────────────────
# Captura principal
# ─────────────────────────────────────────────────────────────────────────────

def capturar_dataset(senas: list[str]) -> None:
    """
    Abre la cámara y guarda muestras de keypoints en el CSV para cada seña.

    Args:
        senas: Lista de nombres de señas a capturar.
    """
    _descargar_modelo()
    os.makedirs(DATASET_DIR, exist_ok=True)

    # Crear CSV con cabecera si no existe
    if not os.path.exists(DATASET_CSV):
        with open(DATASET_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            kp_cols = [f"kp_{i}" for i in range(N_KEYPOINTS)]
            writer.writerow(["sena"] + kp_cols)

    # Construir el detector de landmarks con la Tasks API (mediapipe 1.x)
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
        print("❌ No se pudo abrir la cámara. Verifica que esté conectada.")
        detector.close()
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_idx = 0

    for sena in senas:
        grabando = False
        muestras = 0
        print(f"\n📷 Seña: '{sena.upper()}' — Presiona ESPACIO para empezar")

        while muestras < MUESTRAS_POR_SENA:
            ret, frame = cap.read()
            if not ret:
                break

            frame_idx += 1
            timestamp_ms = int(frame_idx * (1000.0 / fps))

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
            resultado = detector.detect_for_video(mp_image, timestamp_ms)

            if resultado.hand_landmarks:
                _dibujar_landmarks(frame, resultado.hand_landmarks[0])

            estado_txt = (
                f"GRABANDO ({muestras}/{MUESTRAS_POR_SENA})"
                if grabando
                else "EN PAUSA — ESPACIO para grabar"
            )
            color = (0, 200, 0) if grabando else (0, 100, 255)
            cv2.putText(frame, f"SENA: {sena.upper()}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            cv2.putText(frame, estado_txt, (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(frame, "N = siguiente | Q = salir",
                        (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            cv2.imshow("LSM — Captura de dataset", frame)

            if grabando and resultado.hand_landmarks:
                kp = extraer_keypoints(resultado.hand_landmarks[0])
                with open(DATASET_CSV, "a", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerow([sena] + kp)
                muestras += 1

            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord("q"):
                print("🛑 Captura cancelada por el usuario.")
                cap.release()
                cv2.destroyAllWindows()
                detector.close()
                return
            elif tecla == ord("n"):
                print(f"⏭  Saltando seña '{sena}'")
                break
            elif tecla == ord(" "):
                grabando = not grabando

        print(f"✅ Seña '{sena}': {muestras} muestras guardadas.")

    cap.release()
    cv2.destroyAllWindows()
    detector.close()
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
