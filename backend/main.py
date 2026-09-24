# main.py - Punto de entrada de la API Tramite Claro.
# Crea la aplicacion FastAPI, inicializa la base de datos, monta el router
# de tramites y sirve los archivos estaticos generados (documentos y audios).

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.api.tramites import router as tramites_router
from backend.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicacion.

    Se ejecuta una vez al arrancar (antes de aceptar requests) y una vez
    al apagar. Aqui se crea la base de datos SQLite y sus tablas si no existen.
    """
    # Al arrancar: crear tramites.db y la tabla "tramite" si no existen.
    create_db_and_tables()
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
app.mount("/documentos", StaticFiles(directory="documentos", check_dir=False), name="documentos")

# Montar los audios generados como estaticos en /audios.
# Por ahora la carpeta existe pero estara vacia hasta que se integre TTS.
app.mount("/audios", StaticFiles(directory="audios", check_dir=False), name="audios")

# Registrar el router de tramites. Todos sus endpoints quedan bajo /tramites.
app.include_router(tramites_router)