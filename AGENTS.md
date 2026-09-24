# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Overview

Trámite Claro is an accessibility-focused civic assistant for RETyS BC (Baja California government procedures catalog). It uses IBM watsonx.ai with `ibm/granite-4-h-small` to simplify bureaucratic texts into *Lectura Fácil* (UNE 153101:2018 EX standard). The project has two independent sub-projects: `backend/` (Python/FastAPI) and `frontend/` (React/TypeScript/Vite).

## Commands

### Backend (run from `backend/` or project root)
```bash
# Start API server (must run from project root, NOT from backend/)
uvicorn backend.main:app --reload

# CLI conversational mode
python backend/main_voz.py
python backend/main_voz.py --voz   # microphone + speaker

# Download RETyS BC corpus
python backend/descargar_fichas.py          # ~16 curated procedures
python backend/descargar_fichas.py --todas  # full 730 procedures

# Quick module tests (run directly)
python backend/skill_retys.py
python backend/lectura_facil.py
python backend/agent_service.py
```

### Frontend (run from `frontend/`)
```bash
npm run dev       # Vite dev server
npm run build     # tsc -b && vite build
npm run lint      # oxlint (NOT eslint)
```

## Backend Architecture

The backend has two entry points that don't share routing:
- **`backend/main.py`** — FastAPI app with REST API (`/tramites`, `/documentos`, `/audios`)
- **`backend/api/main.py`** — separate API entrypoint (legacy/alternate)

The ReAct agent pipeline: `AgenteRETyS` → `skill_retys.ejecutar_skill()` → `lectura_facil.transformar_a_lectura_facil()`

Key non-obvious constraints:
- `generar_markdown()` in `backend/core/markdown_utils.py` is **idempotent**: won't overwrite existing files. If you regenerate a procedure, delete `documentos/<file>.md` first.
- SQLite DB (`tramites.db`) is created at runtime relative to where `uvicorn` is invoked (project root). Running from `backend/` creates it there instead.
- `texto_simplificado` in `TramiteCreate` is **never stored in SQLite** — only the file path is persisted.
- `backend/api/tramites.py` has a bug: `from sqlModel import Session` (capital M) — should be `sqlmodel`.

## Frontend Architecture

- Route pattern mirrors RETyS BC URLs: `/Portal/TyS/:id` (matches official government site paths)
- All tramite data is **static** in `frontend/src/data/tramites.ts` (no API calls to backend yet)
- Linter is **oxlint** (not ESLint) — config in `frontend/.oxlintrc.json`

## Backend Code Style (Python)

- `verbatimModuleSyntax` is NOT enforced in Python; but TypeScript enforces it on the frontend
- Module-level docstrings use triple double-quotes `"""`; inline comments use `#`
- Section dividers use `# ─────...` (unicode box-drawing character, not dashes)
- All public functions have docstrings with `Args:` and `Returns:` sections
- Imports: stdlib → third-party → local (separated by blank lines), no `isort` enforced
- All text files written to disk use `encoding="utf-8"` explicitly

## Frontend Code Style (TypeScript)

- `verbatimModuleSyntax: true` — use `import type` for type-only imports
- `noUnusedLocals` and `noUnusedParameters` are errors — no unused vars allowed
- `erasableSyntaxOnly: true` — no `const enum` or `namespace`
- No test framework configured (no vitest/jest in package.json)
- Bootstrap 5 + react-bootstrap for UI components

## Environment Setup

Copy `backend/.env.example` to `backend/.env`. Required vars: `WATSONX_API_KEY`, `WATSONX_URL`, `WATSONX_PROJECT_ID`. Default model is `ibm/granite-4-h-small`.
