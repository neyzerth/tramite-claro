# Project Architecture Rules (Non-Obvious Only)

## Data Layer

- **Frontend and backend now share a synchronised procedure catalog.** `frontend/src/data/tramites.ts` has 5 procedures with a `homoclave` field. `backend/skill_retys.py`:`TRAMITES_DB` has 12 procedures (a superset). `HOMOCLAVE_MAP` bridges them: `{ "BC-TYS-XXXX": "clave_tramites_db" }`. SQLite only stores generation results (Markdown path + audio path).
- **`homoclave` is the system-wide join key** — used in: frontend API calls, `HOMOCLAVE_MAP`, SQLite `Tramite.homoclave` (UNIQUE indexed), generated file names (`slug(homoclave)_slug(nombre).md`), and the audio file path (`audios/{homoclave}.mp3`).
- **SQLite (`tramites.db`) only stores processing results**, not the source procedure catalog. Adding a new procedure to `TRAMITES_DB` does NOT create a DB entry — that only happens when `POST /admin/tramites/{homoclave}/generar` is called.

## Pre-generation Pipeline Architecture

The system uses a **two-phase architecture** separating content generation from content delivery:

**Phase 1 — Admin generation** (one-time, triggered by admin):
1. `POST /admin/tramites/{homoclave}/generar` receives request
2. `HOMOCLAVE_MAP[homoclave]` → looks up `TRAMITES_DB` key → gets procedure data
3. `AgenteRETyS.consultar(pregunta, modo="texto")` — two watsonx.ai calls:
   - `_loop_react()`: ReAct agent queries `TRAMITES_DB` via tool call, produces technical response
   - `transformar_a_lectura_facil()`: second LLM call rewrites to Lectura Fácil (UNE 153101:2018 EX)
4. `generar_markdown()` writes `.md` to `backend/documentos/` (delete first if regenerating)
5. `texto_a_audio()` synthesises MP3 to `backend/audios/{homoclave}.mp3` (skipped if TTS creds absent)
6. SQLite upsert: stores `ruta_md` and `ruta_audio`

**Phase 2 — Citizen delivery** (every citizen visit, zero LLM calls):
1. Citizen toggles "Versión Lectura Fácil" in `TramitePage`
2. `GET /tramites/{homoclave}/accesible` → SQLite lookup → returns `{ generado, url_documento, url_audio }`
3. Frontend fetches Markdown text via `GET /documentos/<slug>.md` (FastAPI `StaticFiles`)
4. Audio plays via `GET /audios/{homoclave}.mp3` (FastAPI `StaticFiles`) or `window.speechSynthesis` fallback

## Storage Architecture

- Generated Markdown in `backend/documentos/` — path anchored to `Path(__file__).parent.parent` in `markdown_utils.py`
- Generated MP3 audio in `backend/audios/` — `{homoclave}.mp3`
- Both directories created at startup (`mkdir(exist_ok=True)`) and mounted as FastAPI `StaticFiles`
- `tramites.db` at `backend/tramites.db` — anchored to `__file__` in `database.py`
- File naming: `slug(homoclave)_slug(nombre).md` — slugs strip accents and replace non-alphanumerics with `-`

## Frontend Architecture

- **`/Portal/TyS/:id`** — citizen procedure detail page (`TramitePage`). Shows static data by default; toggling "Versión Lectura Fácil" calls `GET /tramites/{homoclave}/accesible` and renders pre-generated Markdown.
- **`/admin`** — admin panel (`AdminPage`). No auth. Shows a table of 5 procedures with generation status; per-row "Generar"/"Actualizar" buttons and a global "Generar todos" button.
- **`frontend/src/api/tramiteApi.ts`** — citizen API client (`consultarAccesible`, `BASE_URL` exported)
- **`frontend/src/api/adminApi.ts`** — admin API client (`listarEstado`, `generarTramite`)
- `AdminPage` uses `<Fragment key={homoclave}>` (not `<>`) when mapping rows that may conditionally render an error `<tr>`.

## Coupling Constraints

- `backend/core/markdown_utils.py` deliberately knows nothing about FastAPI or SQLite — it only writes files. Keep it that way.
- `tts_service` is imported lazily inside the admin route handler (not at module level) to prevent startup crash when TTS credentials are absent.
- The agent (`AgenteRETyS`) is accessed via `request.app.state.agente` in route handlers — never imported directly into routes.
- `backend/main.py` (legacy) is NOT the active entry point. All new development targets `backend/api/main.py`.
