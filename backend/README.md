# Trámite Claro

Asistente ciudadano accesible para trámites del **Registro Estatal de Trámites y Servicios de Baja California (RETyS BC)**. Usa IBM watsonx.ai para simplificar información aplicando la norma de **Lectura Fácil UNE 153101:2018 EX** y soporta entrada/salida por voz con Watson Speech.

---

## Descripción

| Módulo | Descripción |
|---|---|
| `skill_retys.py` | Skill (tool) de consulta al catálogo RETyS BC — RAG-first, fallback a TRAMITES_DB |
| `rag_service.py` | Pipeline RAG: indexación y búsqueda semántica sobre fichas RETyS |
| `lectura_facil.py` | Transformador de texto a norma Lectura Fácil |
| `agent_service.py` | Agente orquestador con loop ReAct + tool calling |
| `stt_service.py` | Watson STT: grabación y transcripción de voz |
| `tts_service.py` | Watson TTS: síntesis y reproducción de voz |
| `main_voz.py` | CLI conversacional (texto o voz) |
| `api/` | API REST con FastAPI |
| `lsm/` | Módulo experimental de Lenguaje de Señas Mexicana |

---

## Requisitos

- Python 3.10+
- `ffmpeg` instalado en el sistema (para reproducción de audio TTS)
- Cuenta IBM Cloud con acceso a:
  - watsonx.ai (proyecto activo)
  - Watson Speech to Text
  - Watson Text to Speech
  - Watson Machine Learning *(opcional, solo módulo LSM)*

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-org/tramite-claro.git
cd tramite-claro/backend

# 2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de IBM Cloud
```

---

## Ejecución

### Modo texto (terminal)

```bash
python main_voz.py
```

### Modo voz (micrófono + altavoz)

```bash
python main_voz.py --voz
```

### API REST

```bash
uvicorn api.main:app --reload
```

La documentación Swagger estará disponible en [http://localhost:8000/docs](http://localhost:8000/docs).

### Descargar corpus RETyS BC

```bash
# Selección curada (~16 trámites, recomendado para hackathon)
python descargar_fichas.py

# Catálogo completo (730 fichas, tarda varios minutos)
python descargar_fichas.py --todas
```

> **Primer arranque con RAG:** Las fichas se deben descargar **antes** de levantar el servidor.
> El servidor construye el índice vectorial automáticamente en el primer arranque.
> En arranques posteriores el índice ya existe y se omite la construcción.

### Primer arranque completo (paso a paso)

```bash
# 1. Descargar fichas del RETyS (genera fichas/*.txt)
python descargar_fichas.py

# 2. Levantar el servidor (construye el índice RAG automáticamente)
uvicorn api.main:app --reload
```

Al arrancar verás en la terminal:
```
[RAG] Verificando índice vectorial...
[RAG] Construyendo índice de fichas RETyS (10 fichas)...
[RAG] Indexando: Expedición de Licencia de Conducir
...
[RAG] Índice construido con 10 fichas. Listo.
```

---

## Variables de entorno

Ver [`.env.example`](.env.example) para la lista completa y documentada.

| Variable | Descripción |
|---|---|
| `WATSONX_API_KEY` | API key del proyecto watsonx.ai |
| `WATSONX_URL` | URL del servicio watsonx.ai |
| `WATSONX_PROJECT_ID` | ID del proyecto watsonx.ai |
| `WATSONX_MODEL_ID` | Modelo a usar (default: `ibm/granite-4-h-small`) |
| `STT_API_KEY` | API key Watson Speech to Text |
| `STT_URL` | URL Watson Speech to Text |
| `TTS_API_KEY` | API key Watson Text to Speech |
| `TTS_URL` | URL Watson Text to Speech |
| `WML_LSM_DEPLOYMENT_ID` | Deployment ID del modelo LSM en WML *(opcional)* |

---

## Costos estimados (MVP)

Con `ibm/granite-4-h-small`:

- Consulta típica ≈ 800 tokens input + 600 tokens output
- Costo por consulta ≈ **$0.0002 USD**
- 1 000 consultas ≈ **$0.20 USD**

---

## Módulo LSM (experimental)

El módulo de Lenguaje de Señas Mexicana requiere:

1. Capturar un dataset con `python lsm/lsm_capture.py`
2. Entrenar el modelo en Watson Studio con `lsm/train_lsm.py`
3. Configurar `WML_LSM_DEPLOYMENT_ID` en `.env`
4. Ejecutar el pipeline multimodal: `python main_accesibilidad.py`
