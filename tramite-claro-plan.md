# Plan: Trámite Claro — Backend Python con watsonx.ai + Watson Speech

## Visión general

Construir el backend completo de **Trámite Claro**, una herramienta de asistencia ciudadana
accesible que usa IBM watsonx.ai para simplificar documentos de trámites del Registro Estatal
de Trámites y Servicios de Baja California (RETyS BC) aplicando la norma de Lectura Fácil
UNE 153101:2018 EX.

El sistema:
- Expone una API REST (FastAPI) para consultas de trámites
- Usa un agente IA con tool calling para buscar información de RETyS BC
- Simplifica las respuestas con la norma Lectura Fácil antes de entregarlas al ciudadano
- Soporta entrada y salida por voz (Watson STT + TTS)
- Tiene un módulo experimental de Lenguaje de Señas Mexicana (LSM) para Watson ML

---

## Variables de entorno requeridas

Todas las claves van en un archivo `.env` en la raíz del proyecto.

```
# watsonx.ai
WATSONX_API_KEY=       # valor de API_PROJECT
WATSONX_URL=           # valor de URL_PROJECT
WATSONX_PROJECT_ID=    # valor de PROJECT_ID
WATSONX_MODEL_ID=ibm/granite-4-h-small  # valor de NAME_MODEL para MVP

# Watson Speech (instancias separadas de watsonx.ai)
STT_API_KEY=
STT_URL=
TTS_API_KEY=
TTS_URL=

# Watson Machine Learning (para el módulo LSM)
WML_LSM_DEPLOYMENT_ID=
```

---

## Selección de modelo para MVP

| Modelo | Params | Costo input/1K tokens | Tool Calling | Recomendación |
|---|---|---|---|---|
| **granite-4-h-small** | 30B | **$0.0000636** | Sí | **MVP — usar este** |
| mistral-small-3-1-24b | 24B | ~$0.0002 | Sí | Alternativa MVP |
| llama-4-maverick-17b-128e-fp8 | 17B MoE | Medio | Sí + imagen | Backup visión/LSM |
| granite-guardian-3-8b | 8B | $0.0002 | No | Solo guardrails — Deprecado |
| llama-3-3-70b-instruct | 70B | Alto | Sí | Producción futura |
| mistral-large-2512 | Grande | Muy alto | Sí | Producción premium |
| gpt-oss-120b | 120B | Muy alto | Sí | No IBM — evitar en MVP |

**Motivo de elección granite-4-h-small:**
- Precio más bajo de la lista
- Contexto de 131K tokens (cabe toda la DB de trámites en el prompt)
- Tool calling nativo compatible con el formato OpenAI
- Modelo proporcionado por IBM dentro de watsonx.ai

---

## Estructura de archivos del proyecto

```
tramite-claro/
├── .env                          # Credenciales (no commitear)
├── .env.example                  # Plantilla de variables
├── requirements.txt              # Dependencias Python
├── README.md
│
├── skill_retys.py                # Tool/Skill: definición + lógica RETyS BC
├── lectura_facil.py              # Transformador de texto a norma UNE 153101
├── agent_service.py              # Agente principal: loop ReAct + tool calling
│
├── stt_service.py                # Watson STT: grabar y transcribir audio
├── tts_service.py                # Watson TTS: sintetizar y reproducir voz
├── main_voz.py                   # CLI: modo texto o modo voz
│
├── api/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app + rutas principales
│   ├── models.py                 # Pydantic schemas de request/response
│   └── routes/
│       ├── tramites.py           # GET /tramites, POST /consultar
│       └── accesibilidad.py     # POST /voz/consultar, POST /lsm/consultar
│
└── lsm/
    ├── lsm_capture.py            # Captura de dataset: MediaPipe + CSV keypoints
    ├── train_lsm.py              # Notebook Watson Studio: TF/Keras + deploy WML
    ├── lsm_predictor.py          # Inferencia en tiempo real: WML scoring endpoint
    └── dataset/
        └── keypoints.csv         # Generado por lsm_capture.py
```

---

## Sub-tareas

---

### ST-01 — Estructura base del proyecto

**Intent:**
Crear la estructura de directorios, el archivo de dependencias y la configuración de entorno
para que todos los módulos puedan importar correctamente las credenciales y librerías.

**Expected Outcomes:**
- Directorio `tramite-claro/` creado con subdirectorio `api/` y `lsm/`
- `requirements.txt` con todas las dependencias necesarias
- `.env.example` con todas las variables documentadas
- `README.md` con instrucciones de instalación y ejecución

**Todo List:**
1. Crear el directorio `tramite-claro/` y todos sus subdirectorios
2. Crear `requirements.txt` con: `ibm-watsonx-ai`, `ibm-watson`, `fastapi`,
   `uvicorn`, `python-dotenv`, `pyaudio`, `mediapipe`, `tensorflow`,
   `opencv-python`, `pydantic`, `httpx`
3. Crear `.env.example` documentando cada variable
4. Crear `README.md` con secciones: Descripción, Requisitos, Instalación, Ejecución

**Relevant Context:**
- SDK principal: `ibm-watsonx-ai` (reemplaza `ibm-watson-machine-learning`)
- Watson STT/TTS usan `ibm-watson` SDK por separado
- Python 3.10+

**Status:** [ ] pending

---

### ST-02 — Skill RETyS BC (`skill_retys.py`)

**Intent:**
Implementar la skill (tool) que el agente usa para consultar el catálogo de trámites del
Registro Estatal de Trámites y Servicios de Baja California. Esta skill es el único punto
de acceso a la información de trámites y debe exponer una interfaz compatible con el
formato de tool calling de watsonx.ai.

**Expected Outcomes:**
- `TOOL_DEFINITION` en formato JSON Schema compatible con OpenAI/watsonx.ai tool calling
- `TRAMITES_DB`: diccionario con al menos 5 trámites reales de RETyS BC con sus campos completos
- Función `ejecutar_skill(nombre_tramite: str) -> dict` que devuelve la ficha del trámite
- Manejo de caso "trámite no encontrado" con lista de trámites disponibles

**Todo List:**
1. Definir `TOOL_DEFINITION` con:
   - `name`: `consultar_tramite_retys`
   - `description`: descripción clara de qué hace la skill
   - `parameters`: schema con `nombre_tramite` (string, required) y
     `tipo_busqueda` (enum: exacta, parcial)
2. Crear `TRAMITES_DB` como diccionario Python con trámites de RETyS BC.
   Cada trámite debe tener: `nombre`, `descripcion`, `dependencia`,
   `requisitos` (lista), `costo`, `tiempo_respuesta`, `url_oficial`,
   `fundamento_legal`, `horario`, `modalidad` (presencial/en línea/mixto)
3. Implementar `buscar_tramite(nombre: str, tipo: str) -> list` con búsqueda
   exacta e insensible a mayúsculas
4. Implementar `ejecutar_skill(argumentos: dict) -> str` que llama a
   `buscar_tramite` y devuelve un JSON string con el resultado
5. Agregar al menos estos trámites: licencia de conducir, acta de nacimiento,
   credencial de elector, pasaporte, registro civil

**Relevant Context:**
- El agente llama a `ejecutar_skill` cuando el modelo decide invocar la tool
- El resultado de la skill se devuelve como mensaje `"tool"` en el historial
- Formato de tool calling de watsonx.ai es compatible con OpenAI function calling

**Status:** [ ] pending

---

### ST-03 — Transformador Lectura Fácil (`lectura_facil.py`)

**Intent:**
Implementar el módulo que toma la respuesta cruda del agente (texto técnico-administrativo)
y la transforma aplicando estrictamente la norma UNE 153101:2018 EX de Lectura Fácil.
Este módulo hace una segunda llamada al modelo con un system prompt especializado.

**Expected Outcomes:**
- Función `transformar_a_lectura_facil(texto: str, modo: str) -> str`
  - `modo="texto"`: respuesta con emojis y Markdown para pantalla
  - `modo="voz"`: respuesta sin emojis, oraciones ≤20 palabras para TTS
- System prompt que embebe los 6 apartados de la norma UNE:
  - 6.1 Ortotipografía, 6.2 Vocabulario, 6.3 Frases, 6.4 Texto y estilo
  - 7.1 Presentación, 7.2 Imágenes, 7.3 Elementos del documento
- Configuración de generación: `max_new_tokens=600` (texto), `max_new_tokens=512` (voz)
- Temperatura baja (0.1) para respuestas consistentes

**Todo List:**
1. Crear instancia de `ModelInference` con `ibm/granite-4-h-small`
2. Definir `SYSTEM_PROMPT_LECTURA_FACIL` con las reglas de la norma UNE 153101:2018 EX
   organizadas en 6 pasos de revisión
3. Definir `SYSTEM_PROMPT_LECTURA_FACIL_VOZ` con las mismas reglas adaptadas para
   síntesis de voz: eliminar emojis, frases ≤20 palabras, sin Markdown
4. Implementar `transformar_a_lectura_facil(texto, modo="texto") -> str`
5. Agregar función `aplicar_6_pasos_revision(texto: str) -> dict` que devuelve
   un dict con el texto transformado y notas de cada paso de revisión
6. Escribir 3 pruebas de transformación con textos de ejemplo de RETyS BC

**Relevant Context:**
- Norma UNE 153101:2018 EX apartados clave:
  - 6.1: frases cortas, una idea por frase, sin punto y coma
  - 6.2: vocabulario sencillo, explica siglas, sin abreviaturas
  - 6.3: presente de indicativo, sin pasiva, sin gerundio
  - 6.4: títulos informativos, listas para más de 3 elementos
- El modo voz reemplaza "Debes presentar" por "Tienes que llevar"
- Máximo 2 tokens de temperatura para no inventar información

**Status:** [ ] pending

---

### ST-04 — Agente principal (`agent_service.py`)

**Intent:**
Implementar el agente orquestador que recibe la consulta del ciudadano, decide si invocar
la skill RETyS BC, obtiene la información, y genera una respuesta que luego pasa al
transformador de Lectura Fácil. Usa el loop ReAct (Razonar → Actuar → Observar).

**Expected Outcomes:**
- Clase `AgenteRETyS` con método `consultar(pregunta: str, modo: str) -> str`
- Loop agentic con máximo 5 iteraciones para evitar bucles infinitos
- Integración con `skill_retys.py` (tool calling) y `lectura_facil.py`
- System prompt que define el rol del agente como asistente ciudadano
- Historial de conversación para contexto multi-turno

**Todo List:**
1. Crear `ModelInference` con `ibm/granite-4-h-small` y configuración:
   - `temperature=0.3`, `max_new_tokens=800`
   - `tools=[TOOL_DEFINITION]`, `tool_choice="auto"`
2. Definir `SYSTEM_PROMPT_AGENTE` que:
   - Define el rol: asistente de trámites gubernamentales de Baja California
   - Indica que siempre debe consultar la skill antes de responder
   - Pide respuestas en primera persona y tono amable
   - Indica que la respuesta final será procesada para Lectura Fácil
3. Implementar `loop_react(historial, max_iter=5) -> str`:
   - Llamar al modelo con el historial actual
   - Si la respuesta incluye `tool_calls`: ejecutar la skill y agregar el resultado
   - Si la respuesta es texto final: salir del loop
4. Implementar `AgenteRETyS.consultar(pregunta, modo) -> str`:
   - Armar historial con system prompt + pregunta del usuario
   - Llamar `loop_react`
   - Pasar respuesta a `transformar_a_lectura_facil(respuesta, modo)`
   - Devolver la respuesta transformada
5. Probar con 3 consultas de ejemplo

**Relevant Context:**
- `ModelInference` de `ibm_watsonx_ai.foundation_models`
- El resultado de la tool se agrega al historial como `{"role": "tool", "content": resultado, "tool_call_id": id}`
- El agente y el transformador Lectura Fácil hacen cada uno 1 llamada al modelo
- Total: máximo 2 llamadas al modelo por consulta (agente + lectura fácil)

**Status:** [ ] pending

---

### ST-05 — Watson STT (`stt_service.py`)

**Intent:**
Implementar el módulo de reconocimiento de voz que graba audio del micrófono y lo
transcribe usando Watson Speech to Text con el modelo en español latinoamericano.

**Expected Outcomes:**
- Función `grabar_audio(duracion_seg=8) -> bytes` que graba desde el micrófono
- Función `transcribir_audio(audio_bytes: bytes) -> str` que llama a Watson STT
- Función `escuchar_consulta() -> str` que combina grabación y transcripción
- Manejo de errores de conexión y de audio silencioso

**Todo List:**
1. Crear instancia de `SpeechToTextV1` con `IAMAuthenticator`
2. Configurar modelo: `es-LA_BroadbandModel` para español latinoamericano
3. Implementar `grabar_audio(duracion_seg=8) -> bytes`:
   - Usar `pyaudio` con configuración: rate=16000, channels=1, format=paInt16
   - Mostrar mensaje "Escuchando..." al usuario durante la grabación
4. Implementar `transcribir_audio(audio_bytes: bytes) -> str`:
   - Llamar `recognize()` con content_type `audio/l16;rate=16000`
   - Extraer el transcript del primer resultado
   - Devolver string vacío si no hay transcripción
5. Implementar `escuchar_consulta() -> str` combinando los dos pasos anteriores
6. Agregar manejo de `ServiceUnavailableError` y `AudioDeviceError`

**Relevant Context:**
- SDK: `ibm_watson.SpeechToTextV1`
- Variables: `STT_API_KEY`, `STT_URL` (distintas a las de watsonx.ai)
- El audio se graba en PCM 16-bit, mono, 16kHz para mejor precisión

**Status:** [ ] pending

---

### ST-06 — Watson TTS (`tts_service.py`)

**Intent:**
Implementar el módulo de síntesis de voz que convierte el texto simplificado (modo voz)
en audio MP3 usando Watson Text to Speech con voz neural en español latinoamericano.

**Expected Outcomes:**
- Función `texto_a_audio(texto: str) -> bytes` que devuelve audio MP3
- Función `reproducir_audio(audio_bytes: bytes)` que reproduce el audio
- Función `hablar(texto: str)` que combina síntesis y reproducción
- Manejo de texto demasiado largo (>5000 caracteres) con segmentación

**Todo List:**
1. Crear instancia de `TextToSpeechV1` con `IAMAuthenticator`
2. Configurar voz: `es-LA_SofiaV3Voice` (voz neural, español latinoamericano)
3. Implementar `texto_a_audio(texto: str) -> bytes`:
   - Llamar `synthesize()` con `accept="audio/mp3"`
   - Devolver los bytes del audio
4. Implementar `reproducir_audio(audio_bytes: bytes)`:
   - Guardar temporalmente como `/tmp/tramite_audio.mp3`
   - Reproducir con `subprocess.run(["ffplay", "-nodisp", "-autoexit", archivo])`
   - Limpiar el archivo temporal después de reproducir
5. Implementar `segmentar_texto(texto: str, max_chars=4800) -> list` para textos largos
6. Implementar `hablar(texto: str)` que segmenta si es necesario y reproduce todo

**Relevant Context:**
- SDK: `ibm_watson.TextToSpeechV1`
- Variables: `TTS_API_KEY`, `TTS_URL`
- `ffplay` debe estar instalado en el sistema (paquete ffmpeg)
- La voz Sofia es neural, no concatenativa, suena más natural

**Status:** [ ] pending

---

### ST-07 — Pipeline de voz CLI (`main_voz.py`)

**Intent:**
Implementar el punto de entrada CLI que integra STT + Agente + TTS en un loop
conversacional completo. Debe soportar dos modos: texto (para terminal) y voz
(micrófono + altavoz).

**Expected Outcomes:**
- Script ejecutable: `python main_voz.py` (modo texto) y `python main_voz.py --voz`
- Loop conversacional que no termina hasta que el usuario diga "salir" o "adiós"
- Modo texto: entrada por teclado, salida formateada en terminal con Markdown básico
- Modo voz: grabación automática, respuesta hablada, indicadores visuales de estado

**Todo List:**
1. Importar `AgenteRETyS` de `agent_service`, `escuchar_consulta` de `stt_service`,
   `hablar` de `tts_service`
2. Implementar `modo_texto()`:
   - Loop con `input("¿En qué puedo ayudarte? > ")`
   - Llamar `agente.consultar(pregunta, modo="texto")`
   - Imprimir respuesta con separadores visuales
   - Salir con palabras clave: "salir", "adios", "exit"
3. Implementar `modo_accesibilidad()`:
   - Indicar "Escuchando..." al inicio de cada turno
   - Llamar `escuchar_consulta()` para obtener la pregunta
   - Llamar `agente.consultar(pregunta, modo="voz")`
   - Llamar `hablar(respuesta)` para reproducir
   - Detectar "salir" o "adiós" en la transcripción para terminar
4. Implementar bloque `if __name__ == "__main__"` con `argparse`:
   - Flag `--voz` para activar el modo de accesibilidad
5. Mostrar bienvenida con el nombre del servicio y los modos disponibles

**Relevant Context:**
- `AgenteRETyS` se instancia una sola vez y se reutiliza en el loop
- El modo voz usa `modo="voz"` en `consultar()` para Lectura Fácil optimizada para TTS
- Si STT devuelve string vacío, pedir al usuario que repita

**Status:** [ ] pending

---

### ST-08 — Módulo LSM: captura y entrenamiento (`lsm/`)

**Intent:**
Implementar el módulo experimental de Lenguaje de Señas Mexicana que:
1. Captura keypoints de manos con MediaPipe para construir el dataset
2. Entrena un clasificador de señas en Watson Studio (TensorFlow/Keras)
3. Despliega el modelo en Watson Machine Learning para inferencia en tiempo real

Este módulo es experimental y no bloquea el MVP. Se puede probar en paralelo.

**Expected Outcomes:**
- `lsm_capture.py`: captura keypoints de manos y guarda en CSV, con UI de cámara
- `train_lsm.py`: notebook/script para Watson Studio que entrena y despliega el modelo
- `lsm_predictor.py`: cliente del endpoint WML que clasifica señas en tiempo real
- Dataset de al menos 5 señas básicas: hola, gracias, ayuda, sí, no

**Todo List:**
1. Crear `lsm_capture.py`:
   - Abrir cámara con OpenCV
   - Procesar cada frame con `mediapipe.solutions.hands`
   - Extraer 63 valores (21 puntos x 3 coordenadas xyz) por mano
   - Guardar `(sena_label, *keypoints)` en `dataset/keypoints.csv`
   - Mostrar en pantalla el nombre de la seña que se está grabando
   - Salir con tecla 'q'
2. Crear `train_lsm.py` (para ejecutar en Watson Studio):
   - Cargar `keypoints.csv` desde Watson Studio Storage
   - Normalizar keypoints entre 0 y 1
   - Construir modelo: Dense(128, relu) → Dropout(0.3) → Dense(64, relu) → Dense(n_senas, softmax)
   - Entrenar con 80/20 train/test split, 50 épocas
   - Guardar modelo en formato SavedModel de TensorFlow
   - Desplegar en Watson Machine Learning con `ibm_watsonx_ai`
3. Crear `lsm_predictor.py`:
   - Inicializar `ModelInference` de WML con `WML_LSM_DEPLOYMENT_ID`
   - Implementar `predecir_sena(keypoints: list) -> str`
   - Implementar `reconocer_con_ventana(frames: list, umbral=0.7) -> str`
     que promedia 10 frames para reducir ruido
   - Devolver la seña con mayor confianza si supera el umbral, o None

**Relevant Context:**
- IBM no tiene servicio nativo para LSM; se usa Watson ML como plataforma de deploy
- Watson Visual Recognition fue discontinuado en 2021 — no usar
- MediaPipe es local ($0 adicional), solo WML tiene costo al hacer inferencia
- El modelo WML recibe `[[k1, k2, ..., k63]]` y devuelve `{"predictions": [{"values": [probs]}]}`

**Status:** [ ] pending

---

### ST-09 — Pipeline multimodal LSM + Agente (`main_accesibilidad.py`)

**Intent:**
Integrar el reconocimiento de señas LSM con el agente y TTS para crear el pipeline
multimodal completo: la persona hace una seña → se convierte en texto → el agente
responde → el ciudadano escucha la respuesta.

**Expected Outcomes:**
- Función `reconocer_en_tiempo_real() -> str` que graba señas hasta obtener una frase
- Función `procesar_sena(sena: str) -> str` que envía la seña al agente y habla la respuesta
- Pipeline completo ejecutable: `python main_accesibilidad.py`

**Todo List:**
1. Importar `lsm_predictor.py`, `agent_service.py`, `tts_service.py`
2. Implementar `reconocer_en_tiempo_real(timeout_seg=15) -> str`:
   - Capturar frames de cámara durante el timeout
   - Extraer keypoints con MediaPipe por cada frame
   - Pasar ventana de 10 frames a `reconocer_con_ventana()`
   - Acumular señas reconocidas para formar una frase
   - Devolver la frase al terminar el timeout
3. Implementar `procesar_sena(frase_senas: str)`:
   - Mostrar "Entendí: <frase>" en pantalla
   - Llamar `agente.consultar(frase_senas, modo="voz")`
   - Llamar `hablar(respuesta)`
4. Implementar el loop principal con estados: ESPERANDO → GRABANDO → PROCESANDO
5. Mostrar overlay en la ventana de cámara indicando el estado actual

**Relevant Context:**
- Este módulo requiere que `WML_LSM_DEPLOYMENT_ID` esté configurado
- Si no hay modelo LSM desplegado, el módulo debe mostrar error claro y sugerir
  ejecutar `lsm/train_lsm.py` primero
- El pipeline completo tiene latencia mayor (cámara + WML + agente + TTS)

**Status:** [ ] pending

---

### ST-10 — API REST con FastAPI (`api/`)

**Intent:**
Exponer la funcionalidad del agente como una API REST para que el portal web del MUAC,
WhatsApp, correo y otros canales puedan consumir el servicio de forma programática.

**Expected Outcomes:**
- `api/main.py`: aplicación FastAPI con CORS configurado y documentación Swagger automática
- `api/models.py`: schemas Pydantic para request y response de todos los endpoints
- `api/routes/tramites.py`: endpoints para consulta de trámites por texto
- `api/routes/accesibilidad.py`: endpoints para audio y LSM (recibe bytes, devuelve texto + audio)
- Health check en `GET /`

**Todo List:**
1. Crear `api/models.py` con:
   - `ConsultaRequest(BaseModel)`: `pregunta: str`, `modo: Literal["texto", "voz"]`
   - `ConsultaResponse(BaseModel)`: `respuesta: str`, `tramite_encontrado: bool`, `nombre_tramite: str`
   - `AudioRequest(BaseModel)`: `audio_base64: str` (PCM 16-bit, base64 encoded)
   - `AudioResponse(BaseModel)`: `respuesta_texto: str`, `audio_base64: str`
2. Crear `api/routes/tramites.py`:
   - `GET /tramites` — lista todos los trámites disponibles en la DB
   - `POST /tramites/consultar` — recibe `ConsultaRequest`, devuelve `ConsultaResponse`
3. Crear `api/routes/accesibilidad.py`:
   - `POST /voz/consultar` — recibe `AudioRequest`, transcribe, consulta, sintetiza voz
   - `POST /lsm/consultar` — recibe keypoints JSON, clasifica seña, consulta agente
4. Crear `api/main.py`:
   - Instanciar FastAPI con título "Trámite Claro API" y versión "0.1.0"
   - Configurar CORS con `allow_origins=["*"]` para MVP (restringir en producción)
   - Incluir los dos routers con prefijos `/tramites` y `/accesibilidad`
   - Endpoint `GET /` que devuelve `{"status": "ok", "servicio": "Trámite Claro"}`
5. Documentar en `README.md` cómo ejecutar: `uvicorn api.main:app --reload`

**Relevant Context:**
- La instancia de `AgenteRETyS` debe ser un singleton a nivel de app (lifespan)
- El audio base64 debe decodificarse antes de pasarlo a `transcribir_audio()`
- Swagger UI disponible en `/docs` automáticamente con FastAPI

**Status:** [ ] pending

---

## Orden de implementación recomendado

```
ST-01 (base) → ST-02 (skill) → ST-03 (lectura fácil) → ST-04 (agente)
     → ST-05 (STT) → ST-06 (TTS) → ST-07 (CLI voz)
     → ST-08 (LSM captura+entreno) → ST-09 (pipeline multimodal)
     → ST-10 (API FastAPI)
```

El MVP mínimo para demostrar la funcionalidad central es: **ST-01 + ST-02 + ST-03 + ST-04 + ST-07**.
Los módulos de voz (ST-05, ST-06) y LSM (ST-08, ST-09) se pueden agregar en iteraciones posteriores.

---

## Notas técnicas importantes

### Costos estimados por consulta (MVP)

- Consulta típica ≈ 800 tokens input + 600 tokens output
- Con `granite-4-h-small` a $0.0000636/1K input + $0.000254/1K output:
  - Input: 800 × $0.0000636/1000 ≈ $0.0000509
  - Output: 600 × $0.000254/1000 ≈ $0.0001524
  - Total ≈ **$0.0002 por consulta completa** (agente + lectura fácil)
- Para pruebas de MVP: 1000 consultas ≈ $0.20 USD

### Tool calling en watsonx.ai

- El formato de tools es compatible con OpenAI function calling
- `tool_choice="auto"` deja que el modelo decida si usar la tool o responder directamente
- El historial de mensajes incluye roles: `system`, `user`, `assistant`, `tool`

### Lectura Fácil — reglas más críticas para trámites

- Nunca usar pasiva refleja: "se deben presentar" → "tienes que presentar"
- Costos siempre en palabras: "$150 pesos" → "150 pesos"
- Tiempos de respuesta en días naturales, no hábiles: aclarar si aplica
- Siglas la primera vez: "INE (Instituto Nacional Electoral)"
- Requisitos siempre en lista, nunca en párrafo corrido
