"""
api/routes/admin.py — Endpoints de administración de trámites.

GET  /admin/tramites                        → estado de generación de cada trámite del frontend
POST /admin/tramites/{homoclave}/generar    → genera (o regenera) el MD y audio de un trámite
"""
import os
import sys

from fastapi import APIRouter, HTTPException, Request
from sqlmodel import Session, select

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skill_retys import HOMOCLAVE_MAP, TRAMITES_DB
from core.markdown_utils import generar_markdown, slug, DOCUMENTOS_DIR
from database import engine
from models.tramite import Tramite
from api.models import TramiteAdminStatus, GenerarResponse

router = APIRouter()

# Directorio donde se guardan los MP3 generados.
_AUDIOS_DIR = DOCUMENTOS_DIR.parent / "audios"


# ─────────────────────────────────────────────────────────────────────────────
# GET /admin/tramites
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "/tramites",
    response_model=list[TramiteAdminStatus],
    summary="Estado de generación de trámites",
    description=(
        "Devuelve el estado de cada trámite del catálogo del frontend: "
        "si ya tiene documento Markdown generado y/o audio MP3."
    ),
)
async def listar_tramites_admin() -> list[TramiteAdminStatus]:
    """Cruza HOMOCLAVE_MAP con SQLite para reportar el estado de cada trámite."""
    with Session(engine) as session:
        resultado = []
        for homoclave, clave_db in HOMOCLAVE_MAP.items():
            ficha = TRAMITES_DB.get(clave_db, {})
            nombre = ficha.get("nombre", homoclave)

            tramite = session.exec(
                select(Tramite).where(Tramite.homoclave == homoclave)
            ).first()

            url_documento = tramite.ruta_md if tramite else None
            url_audio = tramite.ruta_audio if tramite else None

            resultado.append(
                TramiteAdminStatus(
                    homoclave=homoclave,
                    nombre=nombre,
                    tiene_md=url_documento is not None,
                    tiene_audio=url_audio is not None,
                    url_documento=url_documento,
                    url_audio=url_audio,
                )
            )
        return resultado


# ─────────────────────────────────────────────────────────────────────────────
# POST /admin/tramites/{homoclave}/generar
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "/tramites/{homoclave}/generar",
    response_model=GenerarResponse,
    summary="Generar documento y audio de un trámite",
    description=(
        "Llama al agente IA para producir el texto en Lectura Fácil del trámite, "
        "guarda el Markdown en disco y opcionalmente sintetiza audio MP3 con Watson TTS. "
        "Si el trámite ya fue generado, lo regenera desde cero."
    ),
)
async def generar_tramite(homoclave: str, request: Request) -> GenerarResponse:
    """Genera o regenera el MD y audio de un trámite identificado por su homoclave."""
    clave_db = HOMOCLAVE_MAP.get(homoclave)
    if clave_db is None:
        raise HTTPException(status_code=404, detail=f"Homoclave '{homoclave}' no encontrada.")

    ficha = TRAMITES_DB[clave_db]
    nombre = ficha["nombre"]
    organismo = ficha.get("dependencia")

    # 1. Consultar al agente para obtener el texto simplificado en Lectura Fácil.
    agente = request.app.state.agente
    pregunta = f"¿Cómo tramito: {nombre}?"
    try:
        texto = agente.consultar(pregunta, modo="texto")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error del agente: {exc}") from exc

    # 2. Generar Markdown — borrar primero si ya existe para forzar regeneración.
    nombre_archivo = f"{slug(homoclave)}_{slug(nombre)}.md"
    ruta_md_abs = DOCUMENTOS_DIR / nombre_archivo
    if ruta_md_abs.exists():
        ruta_md_abs.unlink()

    url_documento = generar_markdown(homoclave, nombre, organismo, texto)

    # 3. Intentar síntesis de audio con Watson TTS.
    url_audio: str | None = None
    try:
        from tts_service import texto_a_audio  # importación diferida para no fallar si no hay TTS
        audio_bytes = texto_a_audio(texto)
        _AUDIOS_DIR.mkdir(parents=True, exist_ok=True)
        ruta_audio_abs = _AUDIOS_DIR / f"{homoclave}.mp3"
        ruta_audio_abs.write_bytes(audio_bytes)
        url_audio = f"audios/{homoclave}.mp3"
    except Exception:
        # TTS no disponible (clave no configurada, servicio caído, etc.) — continuar sin audio.
        url_audio = None

    # 4. Upsert en SQLite: actualizar si ya existe, crear si no.
    with Session(engine) as session:
        tramite = session.exec(
            select(Tramite).where(Tramite.homoclave == homoclave)
        ).first()
        if tramite:
            tramite.nombre = nombre
            tramite.organismo = organismo
            tramite.ruta_md = url_documento
            tramite.ruta_audio = url_audio
        else:
            tramite = Tramite(
                homoclave=homoclave,
                nombre=nombre,
                organismo=organismo,
                ruta_md=url_documento,
                ruta_audio=url_audio,
            )
            session.add(tramite)
        session.commit()

    return GenerarResponse(
        homoclave=homoclave,
        nombre=nombre,
        url_documento=url_documento,
        url_audio=url_audio,
    )
