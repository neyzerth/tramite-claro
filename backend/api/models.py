"""
api/models.py — Schemas Pydantic para request y response de la API.
"""
import base64
from typing import Literal

from pydantic import BaseModel, Field, field_validator


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints de trámites
# ─────────────────────────────────────────────────────────────────────────────

class ConsultaRequest(BaseModel):
    pregunta: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Pregunta del ciudadano sobre un trámite.",
        examples=["¿Qué necesito para sacar mi licencia de conducir?"],
    )
    modo: Literal["texto", "voz"] = Field(
        default="texto",
        description=(
            "'texto' para respuesta con formato Markdown y emojis (pantalla). "
            "'voz' para respuesta en texto plano optimizado para TTS."
        ),
    )


class ConsultaResponse(BaseModel):
    respuesta: str = Field(..., description="Respuesta simplificada en Lectura Fácil.")
    tramite_encontrado: bool = Field(
        ..., description="True si se encontró un trámite relevante en la DB."
    )
    nombre_tramite: str = Field(
        default="",
        description="Nombre del trámite encontrado, o cadena vacía si no se encontró.",
    )


class TramiteResumen(BaseModel):
    nombre: str
    dependencia: str
    costo: str
    modalidad: str


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints de accesibilidad (voz)
# ─────────────────────────────────────────────────────────────────────────────

class AudioRequest(BaseModel):
    audio_base64: str = Field(
        ...,
        description=(
            "Audio del ciudadano codificado en Base64. "
            "Formato: PCM 16-bit, mono, 16kHz (audio/l16;rate=16000)."
        ),
    )

    @field_validator("audio_base64")
    @classmethod
    def validar_base64(cls, v: str) -> str:
        try:
            base64.b64decode(v, validate=True)
        except Exception as exc:
            raise ValueError("audio_base64 no es Base64 válido.") from exc
        return v


class AudioResponse(BaseModel):
    respuesta_texto: str = Field(
        ..., description="Respuesta del agente en texto plano (Lectura Fácil, modo voz)."
    )
    audio_base64: str = Field(
        ..., description="Audio de la respuesta sintetizado por Watson TTS, en Base64 (MP3)."
    )
    transcripcion: str = Field(
        default="",
        description="Texto transcrito del audio recibido (útil para depuración).",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints LSM
# ─────────────────────────────────────────────────────────────────────────────

class LSMRequest(BaseModel):
    keypoints: list[float] = Field(
        ...,
        description=(
            "Vector de 63 floats [x0,y0,z0, ..., x20,y20,z20] con los keypoints "
            "de la mano detectados por MediaPipe Hands, normalizados en [0, 1]."
        ),
        min_length=63,
        max_length=63,
    )


class LSMResponse(BaseModel):
    sena_reconocida: str = Field(
        default="",
        description="Nombre de la seña reconocida, o cadena vacía si la confianza es baja.",
    )
    respuesta_texto: str = Field(
        ..., description="Respuesta del agente en texto plano (Lectura Fácil, modo voz)."
    )
    audio_base64: str = Field(
        ..., description="Audio de la respuesta en Base64 (MP3)."
    )
