# Trámite Claro

Asistente ciudadano accesible para trámites del **Registro Estatal de Trámites y Servicios de Baja California (RETyS BC)**. Usa IBM watsonx.ai para simplificar información aplicando la norma de **Lectura Fácil UNE 153101:2018 EX** y soporta entrada/salida por voz con Watson Speech.

---

## Descripción

| Módulo | Descripción |
|---|---|
| `skill_retys.py` | Skill (tool) de consulta al catálogo RETyS BC |
| `lectura_facil.py` | Transformador de texto a norma Lectura Fácil |
| `agent_service.py` | Agente orquestador con loop ReAct + tool calling |
| `stt_service.py` | Watson STT: transcripción de voz (modelo `es-MX_BroadbandModel`) |
| `tts_service.py` | Watson TTS: síntesis de voz (voz `es-LA_SofiaV3Voice`) |
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

---

## Endpoints de la API

### Estado

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Health check — verifica que la API está en línea |

### Trámites (`/tramites`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/tramites` | Lista todos los trámites del catálogo RETyS BC |
| `POST` | `/tramites/consultar` | Consulta el agente IA con texto y recibe respuesta en Lectura Fácil |
| `GET` | `/tramites/{homoclave}/accesible` | Estado del documento accesible generado para una homoclave |

**`POST /tramites/consultar`** — request/response:

```json
// Request
{ "pregunta": "¿Qué necesito para sacar mi licencia?", "modo": "texto" }

// Response
{
  "respuesta": "Para sacar tu licencia necesitas...",
  "tramite_encontrado": true,
  "nombre_tramite": "Licencia de conducir"
}
```

> `modo`: `"texto"` devuelve Markdown con emojis (para pantalla); `"voz"` devuelve texto plano optimizado para TTS.

---

### Accesibilidad (`/accesibilidad`)

#### `POST /accesibilidad/voz/consultar` — Pipeline voz completo

Recibe audio del ciudadano, transcribe con Watson STT, consulta el agente y devuelve la respuesta sintetizada con Watson TTS.

```json
// Request
{ "audio_base64": "<PCM 16-bit mono 16kHz codificado en Base64>" }

// Response
{
  "respuesta_texto": "Para tramitar tu licencia...",
  "audio_base64": "<MP3 en Base64>",
  "transcripcion": "cómo saco mi licencia"
}
```

> **Formato de audio esperado:** PCM 16-bit, mono, 16 kHz (`audio/l16;rate=16000`).

---

#### `POST /accesibilidad/tts/sintetizar` — Sintetizar texto a voz

Convierte cualquier texto a audio MP3 usando Watson TTS. Útil para que el frontend reproduzca respuestas de texto en voz alta.

```json
// Request
{ "texto": "Necesitas tu INE y comprobante de domicilio." }

// Response
{
  "audio_base64": "<MP3 en Base64>",
  "longitud_bytes": 42343
}
```

**Reproducir en el navegador (JavaScript):**

```js
const res = await fetch('/accesibilidad/tts/sintetizar', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ texto: 'Texto a escuchar' })
});
const { audio_base64 } = await res.json();
const audio = new Audio(`data:audio/mp3;base64,${audio_base64}`);
audio.play();
```

---

#### `POST /accesibilidad/lsm/consultar` — Lenguaje de Señas Mexicana *(experimental)*

Recibe keypoints de mano detectados por MediaPipe Hands, clasifica la seña con un modelo WML y devuelve la respuesta sintetizada.

```json
// Request
{ "keypoints": [0.12, 0.45, 0.03, /* ... 63 floats */] }

// Response
{
  "sena_reconocida": "hola",
  "respuesta_texto": "¡Hola! Soy Claro...",
  "audio_base64": "<MP3 en Base64>"
}
```

> Requiere `WML_LSM_DEPLOYMENT_ID` configurado en `.env` y modelo entrenado con `lsm/train_lsm.py`.

---

### Administración (`/admin`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/admin/tramites` | Estado de generación de documentos/audio por trámite |
| `POST` | `/admin/tramites/{homoclave}/generar` | Genera (o regenera) el Markdown y MP3 de un trámite |

---

### Archivos estáticos

| Ruta | Descripción |
|---|---|
| `/documentos/{archivo}.md` | Documento Markdown generado para un trámite |
| `/audios/{homoclave}.mp3` | Audio MP3 pre-generado para un trámite |

### Descargar corpus RETyS BC

```bash
# Selección curada (~16 trámites, recomendado para hackathon)
python descargar_fichas.py

# Catálogo completo (730 fichas, tarda varios minutos)
python descargar_fichas.py --todas
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
