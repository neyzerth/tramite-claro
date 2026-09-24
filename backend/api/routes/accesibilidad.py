"""
api/routes/accesibilidad.py — Endpoints de accesibilidad: voz y LSM.

POST /voz/consultar    → recibe audio base64, transcribe, consulta agente, sintetiza voz
POST /lsm/consultar    → recibe keypoints JSON, clasifica seña, consulta agente, sintetiza voz
"""
import base64
import os
import sys

from fastapi import APIRouter, HTTPException, Request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from stt_service import transcribir_audio
from tts_service import texto_a_audio
from api.models import AudioRequest, AudioResponse, LSMRequest, LSMResponse, TTSRequest, TTSResponse

router = APIRouter()


@router.post(
    "/voz/consultar",
    response_model=AudioResponse,
    summary="Consulta por voz",
    description=(
        "Recibe audio PCM 16-bit mono 16kHz en Base64, transcribe con Watson STT, "
        "consulta el agente y sintetiza la respuesta con Watson TTS. "
        "Devuelve texto y audio en Base64."
    ),
)
async def consultar_por_voz(body: AudioRequest, request: Request) -> AudioResponse:
    """Pipeline completo: audio de entrada → transcripción → agente → audio de salida."""
    agente = request.app.state.agente

    # 1. Decodificar el audio
    try:
        audio_bytes = base64.b64decode(body.audio_base64)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Error al decodificar audio: {exc}") from exc

    # 2. Transcribir con Watson STT
    try:
        transcripcion = transcribir_audio(audio_bytes)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    if not transcripcion:
        raise HTTPException(
            status_code=422,
            detail="No se detectó habla en el audio. Verifica que el audio tenga voz clara.",
        )

    # 3. Consultar al agente (modo voz para Lectura Fácil sin Markdown)
    try:
        respuesta_texto = agente.consultar(transcripcion, modo="voz")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error del agente: {exc}") from exc

    # 4. Sintetizar respuesta con Watson TTS
    try:
        audio_respuesta = texto_a_audio(respuesta_texto)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return AudioResponse(
        respuesta_texto=respuesta_texto,
        audio_base64=base64.b64encode(audio_respuesta).decode("utf-8"),
        transcripcion=transcripcion,
    )


@router.post(
    "/tts/sintetizar",
    response_model=TTSResponse,
    summary="Sintetizar texto a voz",
    description=(
        "Convierte texto plano a audio MP3 usando Watson TTS con voz neural "
        "en español latinoamericano (es-LA_SofiaV3Voice). "
        "Devuelve el MP3 codificado en Base64 listo para reproducir en el navegador."
    ),
)
async def sintetizar_tts(body: TTSRequest) -> TTSResponse:
    """Convierte texto a audio MP3 directamente, sin pasar por el agente."""
    try:
        audio_bytes = texto_a_audio(body.texto)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return TTSResponse(
        audio_base64=base64.b64encode(audio_bytes).decode("utf-8"),
        longitud_bytes=len(audio_bytes),
    )


@router.post(
    "/lsm/consultar",
    response_model=LSMResponse,
    summary="Consulta por Lenguaje de Señas Mexicana",
    description=(
        "Recibe un vector de 63 keypoints de mano (MediaPipe Hands), clasifica la seña "
        "con el modelo WML, consulta el agente con la seña reconocida y sintetiza la respuesta."
    ),
)
async def consultar_por_lsm(body: LSMRequest, request: Request) -> LSMResponse:
    """Pipeline LSM: keypoints → seña → agente → audio de salida."""
    agente = request.app.state.agente

    # 1. Clasificar la seña con el modelo WML
    deployment_id = os.getenv("WML_LSM_DEPLOYMENT_ID", "")
    if not deployment_id:
        raise HTTPException(
            status_code=503,
            detail=(
                "El módulo LSM no está configurado. "
                "Configura WML_LSM_DEPLOYMENT_ID en .env y entrena el modelo con lsm/train_lsm.py."
            ),
        )

    try:
        from lsm.lsm_predictor import predecir_sena
        sena = predecir_sena(body.keypoints, umbral=0.7) or ""
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    if not sena:
        raise HTTPException(
            status_code=422,
            detail="No se reconoció ninguna seña con suficiente confianza. Intenta de nuevo.",
        )

    # 2. Consultar al agente con la seña reconocida
    try:
        respuesta_texto = agente.consultar(sena, modo="voz")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error del agente: {exc}") from exc

    # 3. Sintetizar la respuesta
    try:
        audio_respuesta = texto_a_audio(respuesta_texto)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return LSMResponse(
        sena_reconocida=sena,
        respuesta_texto=respuesta_texto,
        audio_base64=base64.b64encode(audio_respuesta).decode("utf-8"),
    )
