"""
api/main.py — Aplicación FastAPI de Trámite Claro.

Corre con:
  uvicorn api.main:app --reload
"""
import os
import sys
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Añadir el directorio raíz del backend al path para que los routers
# puedan importar los módulos del proyecto sin instalación de paquete
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_service import AgenteRETyS
from api.routes.tramites import router as router_tramites
from api.routes.accesibilidad import router as router_accesibilidad

# ─────────────────────────────────────────────────────────────────────────────
# Lifespan: inicializar el agente una sola vez (singleton)
# ─────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea el agente al arrancar y lo destruye al cerrar."""
    app.state.agente = AgenteRETyS()
    yield
    # Cleanup (no hay recursos que liberar explícitamente por ahora)


# ─────────────────────────────────────────────────────────────────────────────
# Aplicación FastAPI
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Trámite Claro API",
    version="0.1.0",
    description=(
        "API REST del asistente ciudadano Trámite Claro. "
        "Usa IBM watsonx.ai para simplificar información de trámites del RETyS BC "
        "aplicando la norma de Lectura Fácil UNE 153101:2018 EX. "
        "Soporta consultas por texto, voz (Watson STT/TTS) y Lenguaje de Señas Mexicana (WML)."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — permitir todos los orígenes en MVP (restringir en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────────────
# Routers
# ─────────────────────────────────────────────────────────────────────────────

app.include_router(router_tramites, prefix="/tramites", tags=["Trámites"])
app.include_router(router_accesibilidad, prefix="/accesibilidad", tags=["Accesibilidad"])

# ─────────────────────────────────────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Estado"])
async def health_check() -> dict:
    """Verifica que la API esté en línea."""
    return {"status": "ok", "servicio": "Trámite Claro", "version": "0.1.0"}
