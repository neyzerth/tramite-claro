# Project Architecture Rules (Non-Obvious Only)

## Data Layer Split

- **Frontend and backend use completely separate procedure datasets.** `frontend/src/data/tramites.ts` is a static TypeScript array (5 procedures) used to render the UI. `backend/skill_retys.py`:`TRAMITES_DB` is an in-memory Python dict (8 procedures) used by the ReAct agent. They overlap but are not in sync and share no code path.
- **SQLite (`tramites.db`) only stores processing results**, not the source procedure catalog. It records which procedures have been converted to Markdown + their file paths. Adding a new procedure to `TRAMITES_DB` does NOT automatically create a DB entry — that only happens when `POST /tramites` is called.

## Pipeline Architecture

The AI pipeline has two sequential watsonx.ai calls per citizen query:
1. `AgenteRETyS._loop_react()` — ReAct agent queries `TRAMITES_DB` via tool calling, generates a full technical response
2. `lectura_facil.transformar_a_lectura_facil()` — second LLM call rewrites the response into Lectura Fácil

Both calls use the same `WATSONX_MODEL_ID`. The agent uses `temperature=0.3`; the Lectura Fácil transformer uses `temperature=0.1`.

## Storage Architecture

- Generated Markdown files live in `documentos/` (created at project root at runtime)
- Audio files would live in `audios/` — both directories are mounted as FastAPI `StaticFiles` with `check_dir=False` so startup doesn't fail if empty
- File naming: `slug(homoclave)_slug(nombre).md` — slugs strip accents and replace non-alphanumerics with `-`

## Coupling Constraints

- `backend/core/markdown_utils.py` deliberately knows nothing about FastAPI or SQLite — it only writes files. Keep it that way.
- The `TramiteCreate` → `TramiteRead` flow is intentionally asymmetric: input has `texto_simplificado`, output has `url_documento`. The text is discarded after file generation.
- Frontend has no API integration yet — it renders static data only. Backend and frontend are currently decoupled.
