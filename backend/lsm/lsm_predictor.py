"""
lsm_predictor.py — Inferencia en tiempo real de Lenguaje de Señas Mexicana.

Llama al endpoint de Watson Machine Learning para clasificar señas
a partir de keypoints extraídos con MediaPipe.
"""
import os
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Señas que el modelo puede reconocer (mismo orden que en el entrenamiento)
# ─────────────────────────────────────────────────────────────────────────────

CLASES = ["ayuda", "gracias", "hola", "no", "si"]   # Orden alfabético (igual que train_lsm.py)

# ─────────────────────────────────────────────────────────────────────────────
# Cliente WML
# ─────────────────────────────────────────────────────────────────────────────

def _get_wml_client() -> APIClient:
    """Crea y devuelve una instancia autenticada del cliente WML."""
    credentials = Credentials(
        url=os.getenv("WATSONX_URL", ""),
        api_key=os.getenv("WATSONX_API_KEY", ""),
    )
    project_id = os.getenv("WATSONX_PROJECT_ID", "")
    return APIClient(credentials=credentials, project_id=project_id)


# ─────────────────────────────────────────────────────────────────────────────
# Predicción
# ─────────────────────────────────────────────────────────────────────────────

def predecir_sena(keypoints: list[float], umbral: float = 0.7) -> str | None:
    """
    Envía un vector de 63 keypoints al endpoint WML y devuelve la seña predicha.

    Args:
        keypoints: Lista de 63 floats [x0,y0,z0, ..., x20,y20,z20] en [0,1].
        umbral:    Confianza mínima para aceptar la predicción.

    Returns:
        Nombre de la seña predicha, o None si la confianza es menor al umbral
        o no hay deployment configurado.
    """
    deployment_id = os.getenv("WML_LSM_DEPLOYMENT_ID", "")
    if not deployment_id:
        raise RuntimeError(
            "WML_LSM_DEPLOYMENT_ID no está configurado. "
            "Ejecuta lsm/train_lsm.py para entrenar y desplegar el modelo primero."
        )

    if len(keypoints) != 63:
        raise ValueError(f"Se esperaban 63 keypoints, se recibieron {len(keypoints)}.")

    client = _get_wml_client()
    payload = {"input_data": [{"values": [keypoints]}]}
    respuesta = client.deployments.score(deployment_id, payload)

    # Extraer probabilidades del formato de respuesta WML
    # {"predictions": [{"values": [[p0, p1, p2, p3, p4]]}]}
    try:
        probs = respuesta["predictions"][0]["values"][0]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(
            f"Formato de respuesta WML inesperado: {respuesta}"
        ) from exc

    max_prob = max(probs)
    if max_prob < umbral:
        return None

    idx = probs.index(max_prob)
    return CLASES[idx] if idx < len(CLASES) else None


def reconocer_con_ventana(frames: list[list[float]], umbral: float = 0.7) -> str | None:
    """
    Clasifica una seña promediando las predicciones de una ventana de frames.

    Esto reduce el ruido de frames individuales mal capturados.

    Args:
        frames: Lista de hasta 10 vectores de keypoints (63 floats cada uno).
        umbral: Confianza mínima para aceptar la predicción del conjunto.

    Returns:
        Nombre de la seña más frecuente si su confianza promedio supera el umbral,
        o None en caso contrario.
    """
    if not frames:
        return None

    conteo: dict[str, int] = {}
    for kp in frames:
        try:
            sena = predecir_sena(kp, umbral=0.0)   # umbral=0 para no filtrar por frame
        except Exception:  # noqa: BLE001
            continue
        if sena is not None:
            conteo[sena] = conteo.get(sena, 0) + 1

    if not conteo:
        return None

    sena_ganadora = max(conteo, key=lambda s: conteo[s])
    confianza = conteo[sena_ganadora] / len(frames)

    return sena_ganadora if confianza >= umbral else None


# ─────────────────────────────────────────────────────────────────────────────
# Prueba rápida (ejecutar directamente: python lsm/lsm_predictor.py)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Simular keypoints de prueba (todos en 0.5 — solo para verificar la conexión WML)
    kp_prueba = [0.5] * 63
    print("Enviando keypoints de prueba al endpoint WML...")
    try:
        resultado = predecir_sena(kp_prueba, umbral=0.0)
        print(f"Seña predicha: {resultado}")
    except RuntimeError as e:
        print(f"❌ {e}")
