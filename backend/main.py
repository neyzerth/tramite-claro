# main.py - Punto de entrada de la API Tramite Claro.
# Crea la aplicacion FastAPI, inicializa la base de datos, monta el router
# de tramites y sirve los archivos estaticos generados (documentos y audios).

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.api.tramites import router as tramites_router
from backend.database import create_db_and_tables
import backend.rag_service as rag_service

BASE_DIR = Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicacion.

    Se ejecuta una vez al arrancar (antes de aceptar requests) y una vez
    al apagar. Aqui se crea la base de datos SQLite y sus tablas si no existen,
    y se construye el indice RAG si no existe todavia.
    """
    # Al arrancar: crear tramites.db y la tabla "tramite" si no existen.
    create_db_and_tables()

    # Construir el indice RAG si no existe (solo en el primer arranque).
    print("[RAG] Verificando índice vectorial...")
    if not rag_service.indice_existe():
        rag_service.construir_indice()
    else:
        print("[RAG] Índice ya existe, omitiendo construcción.")

    yield
    # Al apagar: no se requiere limpieza adicional con SQLite.


# Instancia principal de FastAPI con metadatos para la documentacion automatica.
app = FastAPI(
    title="Tramite Claro API",
    description=(
        "API para simplificar tramites del RETyS de Baja California. "
        "Recibe texto en Lectura Facil de watsonx.ai, lo convierte a Markdown "
        "y lo sirve como archivo descargable."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# Montar los archivos .md generados como estaticos en /documentos.
# Permite descargar cualquier archivo con: GET /documentos/{nombre_archivo}.md
# check_dir=False evita que falle si la carpeta esta vacia al importar el modulo.

app.mount(
    "/documentos",
    StaticFiles(directory=BASE_DIR / "documentos", check_dir=False),
    name="documentos",
)

app.mount(
    "/audios",
    StaticFiles(directory=BASE_DIR / "audios", check_dir=False),
    name="audios",
)
# Montar los audios generados como estaticos en /audios.
# Por ahora la carpeta existe pero estara vacia hasta que se integre TTS.

# Registrar el router de tramites. Todos sus endpoints quedan bajo /tramites.
app.include_router(tramites_router)