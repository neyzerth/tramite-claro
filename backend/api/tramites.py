# api/tramites.py â€” Router FastAPI con los endpoints del recurso "trÃ¡mites".
# Gestiona la lÃ³gica de negocio: verificar existencia en SQLite, generar
# el Markdown si es necesario, y retornar las URLs de los archivos.

from fastapi import APIRouter, Depends, HTTPException
from sqlModel import Session, select

from backend.core.markdown_utils import generar_markdown
from backend.database import get_session
from backend.models.tramite import Tramite  # noqa: E402 (importado despuÃ©s de database para que SQLModel registre la tabla)
from backend.schemas.tramite import TramiteCreate, TramiteRead

# Prefijo /tramites aplicado a todos los endpoints de este router.
router = APIRouter(prefix="/tramites", tags=["TrÃ¡mites"])


@router.post("", response_model=TramiteRead, status_code=200)
def crear_o_recuperar_tramite(
    payload: TramiteCreate,
    session: Session = Depends(get_session),
) -> TramiteRead:
    """Recibe el texto simplificado de watsonx.ai y lo persiste como Markdown.

    Flujo:
    1. Busca el trÃ¡mite por homoclave en SQLite.
    2. Si ya existe â†’ retorna la URL del documento guardado (ya_existia=True).
    3. Si no existe â†’ genera el .md, inserta el registro en SQLite, retorna URL.

    Este endpoint es idempotente: mÃºltiples llamadas con la misma homoclave
    siempre retornan la misma URL sin duplicar archivos ni registros.
    """
    # Buscar si ya existe un registro para esta homoclave.
    tramite_existente = session.exec(
        select(Tramite).where(Tramite.homoclave == payload.homoclave)
    ).first()

    if tramite_existente:
        # El trÃ¡mite ya fue procesado antes. Retornar las URLs guardadas.
        return TramiteRead(
            homoclave=tramite_existente.homoclave,
            nombre=tramite_existente.nombre,
            organismo=tramite_existente.organismo,
            url_documento=f"/{tramite_existente.ruta_md}",
            url_audio=f"/{tramite_existente.ruta_audio}" if tramite_existente.ruta_audio else None,
            ya_existia=True,
        )

    # El trÃ¡mite es nuevo. Generar el archivo Markdown en documentos/.
    ruta_md = generar_markdown(
        homoclave=payload.homoclave,
        nombre=payload.nombre,
        organismo=payload.organismo,
        texto=payload.texto_simplificado,
    )

    # Crear el registro en SQLite con la ruta del archivo generado.
    nuevo_tramite = Tramite(
        homoclave=payload.homoclave,
        nombre=payload.nombre,
        organismo=payload.organismo,
        ruta_md=ruta_md,
        # ruta_audio queda None hasta que se integre el agente TTS.
    )
    session.add(nuevo_tramite)
    session.commit()
    session.refresh(nuevo_tramite)

    return TramiteRead(
        homoclave=nuevo_tramite.homoclave,
        nombre=nuevo_tramite.nombre,
        organismo=nuevo_tramite.organismo,
        url_documento=f"/{ruta_md}",
        url_audio=None,
        ya_existia=False,
    )


@router.get("/{homoclave}/documento", response_model=dict)
def obtener_documento(
    homoclave: str,
    session: Session = Depends(get_session),
) -> dict:
    """Retorna la URL de descarga del Markdown de un trÃ¡mite ya procesado.

    Ãštil para que el frontend o el chatbot obtenga el enlace del documento
    sin necesidad de volver a enviar el texto completo.

    Retorna 404 si la homoclave no existe en la base de datos.
    """
    tramite = session.exec(
        select(Tramite).where(Tramite.homoclave == homoclave)
    ).first()

    if not tramite:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontrÃ³ el trÃ¡mite con homoclave '{homoclave}'",
        )

    return {"url_documento": f"/{tramite.ruta_md}"}


@router.get("/{homoclave}/audio", response_model=dict)
def obtener_audio(
    homoclave: str,
    session: Session = Depends(get_session),
) -> dict:
    """Retorna la URL de descarga del audio de un trÃ¡mite.

    Por ahora siempre retorna 404 porque la integraciÃ³n con watsonx Speech (TTS)
    estÃ¡ pendiente para una iteraciÃ³n futura. Cuando se implemente, este endpoint
    ya estÃ¡ preparado: solo hay que guardar ruta_audio en el modelo Tramite.
    """
    tramite = session.exec(
        select(Tramite).where(Tramite.homoclave == homoclave)
    ).first()

    if not tramite:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontrÃ³ el trÃ¡mite con homoclave '{homoclave}'",
        )

    if not tramite.ruta_audio:
        raise HTTPException(
            status_code=404,
            detail="Audio no disponible para este trÃ¡mite",
        )

    return {"url_audio": f"/{tramite.ruta_audio}"}

