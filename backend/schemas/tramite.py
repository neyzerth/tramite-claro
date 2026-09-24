# schemas/tramite.py — Contratos Pydantic para los endpoints de la API.
# Separa los modelos de entrada (lo que recibe la API) de los de salida
# (lo que la API responde), sin acoplarlos al modelo de base de datos.

from typing import Optional

from pydantic import BaseModel, Field


class TramiteCreate(BaseModel):
    """Body esperado en POST /tramites.

    Lo envía watsonx.ai después de simplificar el texto de un trámite del RETyS.
    El campo texto_simplificado se usa para generar el Markdown y luego se descarta;
    nunca se persiste en la base de datos.
    """

    # Identificador oficial del trámite en el catálogo RETyS.
    # Ejemplo: "BC-TYS-001"
    homoclave: str = Field(..., examples=["BC-TYS-001"])

    # Nombre del trámite en lenguaje ciudadano.
    nombre: str = Field(..., examples=["Expedición de licencia de conducir"])

    # Dependencia responsable del trámite. Opcional porque no todos los
    # registros del RETyS incluyen este dato.
    organismo: Optional[str] = Field(default=None, examples=["Secretaría de Movilidad"])

    # Texto ya simplificado en Lectura Fácil producido por watsonx.ai.
    # Se convierte a Markdown y se guarda en documentos/. No va a SQLite.
    texto_simplificado: str = Field(
        ..., examples=["Para sacar tu licencia necesitas..."]
    )


class TramiteRead(BaseModel):
    """Respuesta estándar de todos los endpoints de trámites.

    Incluye las URLs de descarga de los archivos generados. Las URLs son
    relativas a la raíz de la API (ej. /documentos/bc-tys-001_licencia.md)
    y pueden usarse directamente para descargar el archivo.
    """

    # Homoclave del trámite, igual a la recibida en TramiteCreate.
    homoclave: str

    # Nombre del trámite.
    nombre: str

    # Organismo responsable.
    organismo: Optional[str] = None

    # URL relativa del documento Markdown generado.
    # Será None solo si el trámite aún no tiene documento (no debería ocurrir
    # en respuestas del POST, pero puede ocurrir en GETs si hay inconsistencia).
    url_documento: Optional[str] = None

    # URL relativa del archivo de audio. Siempre None hasta que se integre TTS.
    url_audio: Optional[str] = None

    # Indica si el trámite ya existía en la base de datos antes de este request.
    # True = se devolvió el documento existente sin regenerarlo.
    # False = se generó el documento por primera vez.
    ya_existia: bool
