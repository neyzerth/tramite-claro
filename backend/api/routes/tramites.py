"""
api/routes/tramites.py — Endpoints para consulta de trámites por texto.

GET  /tramites              → lista todos los trámites disponibles
POST /tramites/consultar    → consulta el agente con texto y devuelve Lectura Fácil
"""
import sys
import os

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select

# Añadir el directorio raíz del backend al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skill_retys import TRAMITES_DB
from database import get_session
from models.tramite import Tramite
from api.models import AccesibleResponse, ConsultaRequest, ConsultaResponse, TramiteResumen

router = APIRouter()


@router.get(
    "",
    response_model=list[TramiteResumen],
    summary="Listar trámites disponibles",
    description="Devuelve el catálogo completo de trámites registrados en la base de datos RETyS BC.",
)
async def listar_tramites() -> list[TramiteResumen]:
    """Devuelve la lista de trámites disponibles en la DB local."""
    return [
        TramiteResumen(
            nombre=ficha["nombre"],
            dependencia=ficha["dependencia"],
            costo=ficha["costo"],
            modalidad=ficha["modalidad"],
        )
        for ficha in TRAMITES_DB.values()
    ]


@router.post(
    "/consultar",
    response_model=ConsultaResponse,
    summary="Consultar un trámite",
    description=(
        "Recibe la pregunta del ciudadano, la procesa con el agente IA + skill RETyS BC "
        "y devuelve la respuesta simplificada en Lectura Fácil (UNE 153101:2018 EX)."
    ),
)
async def consultar_tramite(body: ConsultaRequest, request: Request) -> ConsultaResponse:
    """Consulta el agente RETyS y devuelve la respuesta en Lectura Fácil."""
    agente = request.app.state.agente

    try:
        respuesta = agente.consultar(body.pregunta, modo=body.modo)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error del agente: {exc}") from exc

    # Heurística: si la respuesta menciona "no encontré" es que el trámite no existe en la DB
    tramite_encontrado = "no encontré" not in respuesta.lower() and "no disponible" not in respuesta.lower()

    # Intentar extraer el nombre del trámite de la respuesta (simplificado)
    nombre_tramite = ""
    for ficha in TRAMITES_DB.values():
        if ficha["nombre"].lower() in respuesta.lower():
            nombre_tramite = ficha["nombre"]
            break

    return ConsultaResponse(
        respuesta=respuesta,
        tramite_encontrado=tramite_encontrado,
        nombre_tramite=nombre_tramite,
    )


# ─────────────────────────────────────────────────────────────────────────────
# GET /{homoclave}/accesible
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "/{homoclave}/accesible",
    response_model=AccesibleResponse,
    summary="Consultar estado accesible de un trámite",
    description=(
        "Devuelve si el documento en Lectura Fácil ya ha sido generado para el trámite "
        "identificado por su homoclave. Si no existe, devuelve generado=false sin error."
    ),
)
async def consultar_accesible(
    homoclave: str,
    session: Session = Depends(get_session),
) -> AccesibleResponse:
    """Devuelve el estado de generación del documento accesible para una homoclave."""
    tramite = session.exec(
        select(Tramite).where(Tramite.homoclave == homoclave)
    ).first()

    if tramite is None:
        return AccesibleResponse(homoclave=homoclave, generado=False)

    return AccesibleResponse(
        homoclave=homoclave,
        generado=True,
        url_documento=tramite.ruta_md,
        url_audio=tramite.ruta_audio,
    )
