# database.py — Configuración de la base de datos SQLite para Trámite Claro.
# Usa SQLModel (que combina SQLAlchemy + Pydantic) para definir el engine,
# la sesión de base de datos y la función de inicialización de tablas.

from sqlmodel import SQLModel, Session, create_engine

# Ruta del archivo SQLite. Se crea automáticamente en BackEnd/tramites.db
# al arrancar la aplicación si no existe.
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = f"sqlite:///{BASE_DIR / 'tramites.db'}"

# check_same_thread=False es necesario para SQLite cuando FastAPI usa
# múltiples hilos (lo hace por defecto con async).
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    """Crea todas las tablas definidas en los modelos SQLModel.
    Se llama una sola vez al arrancar la aplicación en main.py.
    Si las tablas ya existen, no hace nada.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """Generador de sesiones para inyección de dependencias en FastAPI.
    Uso: session: Session = Depends(get_session)
    Garantiza que la sesión se cierra siempre al terminar el request,
    incluso si ocurre una excepción.
    """
    with Session(engine) as session:
        yield session
