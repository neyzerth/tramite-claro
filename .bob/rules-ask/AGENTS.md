# Project Documentation Rules (Non-Obvious Only)

- **`backend/api/main.py`** and **`backend/main.py`** are two separate, unconnected FastAPI entry points. The primary one is `backend/main.py`. `backend/api/main.py` appears to be an older/alternate version. Don't confuse them.
- **`backend/skill_retys.py`** is the canonical knowledge base for RETyS BC procedures (in-memory Python dict `TRAMITES_DB`). It is NOT connected to the frontend's `frontend/src/data/tramites.ts` — these are two independent data sources with partially overlapping procedure data.
- **Lectura Fácil** (UNE 153101:2018 EX) is the core transformation that all output passes through. There are two modes: `"texto"` (Markdown + emojis for screen) and `"voz"` (plain text for TTS). This is a legal accessibility standard, not just a style choice.
- **TTS/audio is not yet implemented** — `ruta_audio` in the DB model is always `None`, the `/audios` static mount is empty, and `/tramites/{id}/audio` always returns 404. Don't assume audio functionality is working.
- The **LSM module** (`backend/lsm/`) is experimental Mexican Sign Language support requiring a deployed Watson Machine Learning model. It is NOT part of the core system.
- `backend/descargar_fichas.py` downloads real RETyS BC procedure fiches from the official government website — it requires an internet connection and is not a test fixture generator.
