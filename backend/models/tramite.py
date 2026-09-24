# models/tramite.py — Modelo SQLModel que define la tabla "tramite" en SQLite.
# Solo guarda RUTAS a los archivos generados (documentos y audios),
# nunca el contenido de los archivos directamente en la base de datos.

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Tramite(SQLModel, table=True):
    """Tabla principal de trámites procesados.

    Cada registro representa un trámite del catálogo RETyS que ya fue
    simplificado por watsonx.ai y tiene su documento Markdown generado.
    """

    # Clave primaria autoincremental (interna, no expuesta en la API).
    id: Optional[int] = Field(default=None, primary_key=True)

    # Homoclave del RETyS (ej. "BC-TYS-001"). Identificador único y oficial
    # del trámite. Se usa como parámetro en los endpoints de la API.
    homoclave: str = Field(unique=True, index=True)

    # Nombre ciudadano del trámite (ej. "Expedición de licencia de conducir").
    nombre: str

    # Organismo o dependencia responsable del trámite. Puede ser nulo si
    # watsonx no lo envía en el payload.
    organismo: Optional[str] = Field(default=None)

    # Ruta relativa del archivo Markdown generado dentro de BackEnd/.
    # Ejemplo: "documentos/bc-tys-001_expedicion-de-licencia.md"
    ruta_md: str

    # Ruta relativa del archivo de audio (MP3/WAV). Nulo hasta que se
    # integre el agente TTS de watsonx Speech en una iteración futura.
    ruta_audio: Optional[str] = Field(default=None)

    # Fecha y hora UTC en que se procesó y guardó el trámite por primera vez.
    created_at: datetime = Field(default_factory=datetime.utcnow)
