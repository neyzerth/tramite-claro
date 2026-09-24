"""
lsm_predictor.py — Inferencia de Lenguaje de Señas Mexicana.

Estrategia dual automática:
  1. Si WML_LSM_DEPLOYMENT_ID está en el entorno → usa Watson Machine Learning.
  2. Si no → carga el modelo Keras local (modelo_lsm/model.keras).

No requiere cambios en el código que llama a predecir_sena() o reconocer_con_ventana().
"""
import json
import os

import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# Paths del modelo local
# ─────────────────────────────────────────────────────────────────────────────

_DIR        = os.path.dirname(__file__)
MODEL_PATH  = os.path.join(_DIR, "modelo_lsm", "model.keras")
CLASES_PATH = os.path.join(_DIR, "modelo_lsm", "clases.json")

# ─────────────────────────────────────────────────────────────────────────────
# Estado interno (carga lazy)
# ─────────────────────────────────────────────────────────────────────────────

_modelo_local = None
_clases: list[str] = []


def _usar_wml() -> bool:
    """Devuelve True si las credenciales WML están disponibles."""
    return bool(os.getenv("WML_LSM_DEPLOYMENT_ID", "").strip())


# ─────────────────────────────────────────────────────────────────────────────
# Backend local (Keras)
# ─────────────────────────────────────────────────────────────────────────────

def _cargar_modelo_local() -> None:
    """Carga el modelo .keras y las clases en memoria (idempotente)."""
    global _modelo_local, _clases
    if _modelo_local is not None:
        return

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Modelo local no encontrado: {MODEL_PATH}\n"
            "Entrénalo primero:\n"
            "  source backend/venv/bin/activate\n"
            "  python backend/lsm/train_lsm.py --solo-entrenar"
        )

    import tensorflow as tf  # importación tardía — no penaliza módulos que no usan TF

    _modelo_local = tf.keras.models.load_model(MODEL_PATH)

    with open(CLASES_PATH, encoding="utf-8") as f:
        _clases = json.load(f)


def _predecir_local(keypoints: list[float], umbral: float) -> str | None:
    _cargar_modelo_local()

    X = np.array([keypoints], dtype=np.float32)
    X_min, X_max = X.min(), X.max()
    rango = X_max - X_min if X_max - X_min != 0 else 1.0
    X = (X - X_min) / rango

    probs = _modelo_local.predict(X, verbose=0)[0]
    max_prob = float(probs.max())

    if max_prob < umbral:
        return None
    return _clases[int(probs.argmax())]


# ─────────────────────────────────────────────────────────────────────────────
# Backend remoto (Watson Machine Learning)
# ─────────────────────────────────────────────────────────────────────────────

def _predecir_wml(keypoints: list[float], umbral: float) -> str | None:
    from dotenv import load_dotenv
    load_dotenv()

    from ibm_watsonx_ai import APIClient, Credentials

    credentials = Credentials(
        url=os.getenv("WATSONX_URL", ""),
        api_key=os.getenv("WATSONX_API_KEY", ""),
    )
    client = APIClient(
        credentials=credentials,
        project_id=os.getenv("WATSONX_PROJECT_ID", ""),
    )

    deployment_id = os.getenv("WML_LSM_DEPLOYMENT_ID", "")
    payload = {"input_data": [{"values": [keypoints]}]}
    respuesta = client.deployments.score(deployment_id, payload)

    try:
        probs = respuesta["predictions"][0]["values"][0]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(
            f"Formato de respuesta WML inesperado: {respuesta}"
        ) from exc

    # WML devuelve lista de floats; convertir a numpy para consistencia
    probs_arr = np.array(probs, dtype=np.float32)
    max_prob = float(probs_arr.max())

    if max_prob < umbral:
        return None

    # Necesitamos las clases — cargar desde archivo local si aún no están en memoria
    global _clases
    if not _clases and os.path.exists(CLASES_PATH):
        with open(CLASES_PATH, encoding="utf-8") as f:
            _clases = json.load(f)

    if not _clases:
        raise RuntimeError(
            f"No se encontró {CLASES_PATH}. "
            "Asegúrate de haber entrenado el modelo con train_lsm.py."
        )

    return _clases[int(probs_arr.argmax())]


# ─────────────────────────────────────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────────────────────────────────────

def predecir_sena(keypoints: list[float], umbral: float = 0.7) -> str | None:
    """
    Clasifica un vector de 63 keypoints y devuelve el nombre de la seña.

    Selecciona automáticamente el backend:
      • WML  si WML_LSM_DEPLOYMENT_ID está en el entorno.
      • Local si no (usa modelo_lsm/model.keras).

    Args:
        keypoints: Lista de 63 floats [x0,y0,z0, ..., x20,y20,z20] en [0,1].
        umbral:    Confianza mínima (0–1) para aceptar la predicción.

    Returns:
        Nombre de la seña si la confianza supera el umbral, o None.
    """
    if len(keypoints) != 63:
        raise ValueError(f"Se esperaban 63 keypoints, se recibieron {len(keypoints)}.")

    if _usar_wml():
        return _predecir_wml(keypoints, umbral)
    return _predecir_local(keypoints, umbral)


def reconocer_con_ventana(frames: list[list[float]], umbral: float = 0.6) -> str | None:
    """
    Clasifica una seña votando sobre una ventana de frames consecutivos.

    Reduce el ruido de frames individuales. Devuelve la seña más frecuente
    en la ventana si su proporción de votos supera el umbral.

    Args:
        frames: Lista de vectores de 63 keypoints (uno por frame).
        umbral: Proporción mínima de votos para aceptar la seña ganadora.

    Returns:
        Nombre de la seña más votada, o None si no supera el umbral.
    """
    if not frames:
        return None

    conteo: dict[str, int] = {}
    for kp in frames:
        sena = predecir_sena(kp, umbral=0.0)
        if sena is not None:
            conteo[sena] = conteo.get(sena, 0) + 1

    if not conteo:
        return None

    ganadora = max(conteo, key=lambda s: conteo[s])
    if conteo[ganadora] / len(frames) >= umbral:
        return ganadora
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Prueba rápida: python backend/lsm/lsm_predictor.py
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    backend = "WML" if _usar_wml() else "local (Keras)"
    print(f"Backend seleccionado: {backend}")

    print("Cargando modelo...")
    if not _usar_wml():
        _cargar_modelo_local()
        print(f"✅ Modelo cargado. Clases: {_clases}")

    rng = np.random.default_rng(42)
    kp_random = rng.random(63).tolist()
    resultado = predecir_sena(kp_random, umbral=0.0)
    print(f"Predicción con keypoints random (umbral=0): '{resultado}'")
