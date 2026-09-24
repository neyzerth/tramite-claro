# Project Coding Rules (Non-Obvious Only)

## Backend Python

- **`uvicorn` must be run from project root** as `uvicorn backend.main:app --reload` (module imports require the `backend.` prefix). The DB and file paths are now anchored to `__file__` so they resolve correctly from any CWD.
- **`backend/core/markdown_utils.py`:`generar_markdown()`** is idempotent — it will NOT overwrite an existing `.md` file. Delete `backend/documentos/<slug>.md` manually before regenerating.
- **`texto_simplificado`** in `TramiteCreate` schema is intentionally NOT persisted to SQLite — only the generated file path is stored. Don't add it to the `Tramite` model.
- **`backend/skill_retys.py`:`TRAMITES_DB`** is an in-memory dict (not SQLite). The SQLite DB only stores processed results. Adding new RETyS procedures means editing `TRAMITES_DB` directly.
- Section header style: `# ─────────────────────────────────────────────────────────────────────────────` (unicode U+2500, not ASCII `-`).
- `ModelInference` is used for both the ReAct agent and the Lectura Fácil transformer — pass `params` directly to `.chat()`, not to the constructor (the SDK ignores `max_new_tokens` in constructor when using `.chat()`).

## Frontend TypeScript

- `verbatimModuleSyntax: true` is enforced — always `import type` for type-only imports, or the build fails.
- Linter is **oxlint**, not ESLint. Run `npm run lint` from `frontend/` directory.
- No test runner exists — there is no `vitest`/`jest`. Module-level `if __name__ == "__main__"` patterns (Python equivalent) are handled via running backend scripts directly.
- Tramite IDs used in routes (`/Portal/TyS/:id`) are numeric integers matching the `id` field in `frontend/src/data/tramites.ts`. The path pattern intentionally mirrors the official RETyS BC government URL structure.
