"""
seed_demo.py — Siembra las 5 fichas reales del RETyS BC en SQLite
para que GET /tramites/{homoclave}/accesible devuelva generado=true
sin necesidad de llamar al agente watsonx.

Uso (desde el directorio raíz del proyecto):
    python backend/seed_demo.py

Es idempotente: ejecutarlo más de una vez no crea duplicados.
"""
import sys
import os

# Asegurar que backend/ esté en sys.path para importar database y models
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from sqlmodel import Session, select

from database import engine, create_db_and_tables
from models.tramite import Tramite
from core.markdown_utils import slug

# ─────────────────────────────────────────────────────────────────────────────
# Fichas reales — datos mínimos para la demo
# ruta_md se construye con la misma lógica que generar_markdown() para
# garantizar que el path devuelto por el endpoint coincida con el archivo
# físico en backend/documentos/.
# ─────────────────────────────────────────────────────────────────────────────

FICHAS_DEMO: list[dict] = [
    {
        "homoclave": "BC-CESPT-041",
        "nombre": "Registro o Revalidación de Exención de Permiso de Descarga de Aguas Residuales para Comercios y Empresas de Servicios",
        "organismo": "Comisión Estatal de Servicios Públicos de Tijuana",
    },
    {
        "homoclave": "BC-SH-012",
        "nombre": "Expedición de Licencia de Conducir",
        "organismo": "Secretaría de Hacienda de Baja California",
    },
    {
        "homoclave": "BC-CEJUM-001",
        "nombre": "Atención Integral a Mujeres Víctimas de Violencia",
        "organismo": "Centro de Justicia para las Mujeres del Estado de Baja California",
    },
    {
        "homoclave": "BC-SHFP-002",
        "nombre": "Constancia de no inhabilitación.",
        "organismo": "Secretaría Anticorrupción y Buen Gobierno",
    },
    {
        "homoclave": "BC-SSCBC-022",
        "nombre": "Expedición de Constancia de Antecedentes Penales",
        "organismo": "Secretaría de Seguridad Ciudadana del Estado de Baja California",
    },
]


def _ruta_md(homoclave: str, nombre: str) -> str:
    """Reproduce la lógica de generar_markdown() para calcular la ruta relativa."""
    nombre_archivo = f"{slug(homoclave)}_{slug(nombre)}.md"
    return f"documentos/{nombre_archivo}"


def seed() -> None:
    """Inserta o actualiza las fichas demo en SQLite."""
    create_db_and_tables()

    with Session(engine) as session:
        for ficha in FICHAS_DEMO:
            homoclave = ficha["homoclave"]
            nombre = ficha["nombre"]
            organismo = ficha["organismo"]
            ruta_md = _ruta_md(homoclave, nombre)

            tramite = session.exec(
                select(Tramite).where(Tramite.homoclave == homoclave)
            ).first()

            if tramite:
                tramite.nombre = nombre
                tramite.organismo = organismo
                tramite.ruta_md = ruta_md
                tramite.ruta_audio = None
                accion = "actualizado"
            else:
                tramite = Tramite(
                    homoclave=homoclave,
                    nombre=nombre,
                    organismo=organismo,
                    ruta_md=ruta_md,
                    ruta_audio=None,
                )
                session.add(tramite)
                accion = "insertado"

            session.commit()
            print(f"  ✓ {homoclave} [{accion}] → {ruta_md}")

    print(f"\nSeed completado: {len(FICHAS_DEMO)} fichas procesadas.")
    print("El endpoint GET /tramites/{homoclave}/accesible ahora devuelve generado=true para estas fichas.")


if __name__ == "__main__":
    print("Sembrando fichas demo en backend/tramites.db …\n")
    seed()
