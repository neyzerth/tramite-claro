# core/markdown_utils.py — Utilidades para generar archivos Markdown a partir
# del texto simplificado en Lectura Fácil producido por watsonx.ai.
# Esta capa no conoce FastAPI ni SQLite; solo trabaja con archivos en disco.

import os
import re
import unicodedata
from pathlib import Path

# Carpeta donde se guardan los documentos Markdown generados.
# La ruta es relativa al directorio desde donde se ejecuta uvicorn (BackEnd/).
BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTOS_DIR = BASE_DIR / "documentos"


def slug(texto: str, limite: int = 60) -> str:
    """Convierte un texto a un slug seguro para nombres de archivo.

    Normaliza caracteres unicode, elimina acentos, reemplaza espacios y
    caracteres especiales por guiones, y limita la longitud.

    Ejemplo: "Expedición de licencia" → "expedicion-de-licencia"
    """
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t[:limite]


def generar_markdown(
    homoclave: str,
    nombre: str,
    organismo: str | None,
    texto: str,
) -> str:
    """Genera un archivo Markdown con el texto simplificado y lo guarda en disco.

    Si el archivo ya existe (mismo homoclave), no lo sobreescribe y retorna
    la ruta existente. Esto hace la función idempotente: llamarla dos veces
    con los mismos datos produce el mismo resultado sin duplicar archivos.

    Args:
        homoclave: Identificador oficial del trámite en el RETyS (ej. "BC-TYS-001").
        nombre:    Nombre ciudadano del trámite.
        organismo: Dependencia responsable. Puede ser None.
        texto:     Texto simplificado en Lectura Fácil producido por watsonx.ai.

    Returns:
        Ruta relativa del archivo Markdown creado o ya existente.
        Ejemplo: "documentos/bc-tys-001_expedicion-de-licencia.md"
    """
    # Construir nombre de archivo: slug(homoclave)_slug(nombre).md
    nombre_archivo = f"{slug(homoclave)}_{slug(nombre)}.md"
    ruta = DOCUMENTOS_DIR / nombre_archivo

    # Si el archivo ya fue generado previamente, no se regenera.
    # Esto cubre el caso en que la DB ya tiene el registro pero el archivo
    # también existe (consistencia garantizada).
    if ruta.exists():
        return f"documentos/{nombre_archivo}"

    # Asegurar que el directorio documentos/ exista antes de escribir.
    DOCUMENTOS_DIR.mkdir(parents=True, exist_ok=True)

    # Construir el contenido Markdown con estructura básica:
    # título, organismo responsable, separador y cuerpo del texto.
    organismo_linea = f"**Organismo:** {organismo}" if organismo else ""
    contenido = f"# {nombre}\n\n{organismo_linea}\n\n---\n\n{texto}\n"

    # Escribir el archivo en UTF-8 para soportar caracteres del español.
    ruta.write_text(contenido, encoding="utf-8")

    return f"documentos/{nombre_archivo}"
