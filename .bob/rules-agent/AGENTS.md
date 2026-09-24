# Project Coding Rules (Non-Obvious Only)

## Backend Python

- **`uvicorn` entry point** — use `uvicorn api.main:app --reload` from the `backend/` directory (or `uvicorn backend.api.main:app --reload` from project root). `backend/main.py` is a legacy entry point **not** used by the integration — do not confuse them.
- **`backend/api/main.py`** is the canonical FastAPI app. It initialises `AgenteRETyS` as a singleton on `app.state.agente` inside the lifespan, calls `create_db_and_tables()` on startup, and mounts `/documentos` and `/audios` as `StaticFiles` (both directories are created at startup with `mkdir(exist_ok=True)` so the server never fails if they are empty).
- **`backend/api/routes/admin.py`** accesses the agent via `request.app.state.agente`. Always use this pattern — never import `AgenteRETyS` directly inside a route handler.
- **`backend/core/markdown_utils.py`:`generar_markdown()`** is idempotent — it will NOT overwrite an existing `.md` file. The admin endpoint deletes `DOCUMENTOS_DIR/<slug>.md` before calling it to force regeneration.
- **`texto_simplificado`** in `TramiteCreate` is intentionally NOT persisted to SQLite — only the generated file path (`ruta_md`) is stored. Don't add raw text to the `Tramite` model.
- **`backend/skill_retys.py`:`TRAMITES_DB`** is an in-memory dict (not SQLite). It now contains **12 procedures** (8 original + 4 added to match the frontend catalog). `HOMOCLAVE_MAP` is a companion dict that maps `"BC-TYS-XXXX" → TRAMITES_DB key` for the 5 frontend procedures — used by admin routes to look up procedures by homoclave.
- **Watson TTS `texto_a_audio()`** is imported inside the admin route handler (`from tts_service import texto_a_audio`) to avoid crashing at startup when TTS credentials are absent. If it raises any exception, the route silently sets `url_audio = None` and continues.
- **Double-encoded JSON from watsonx.ai** — `ibm/granite-4` returns `tool_calls[].function.arguments` as a JSON string that is itself JSON-encoded (i.e. `'"{\\"nombre_tramite\\": \\"x\\"}"'`). `agent_service.py` applies `json.loads()` twice when the first parse returns a `str` instead of `dict`.
- Section header style: `# ─────────────────────────────────────────────────────────────────────────────` (unicode U+2500, not ASCII `-`).
- `ModelInference` is used for both the ReAct agent and the Lectura Fácil transformer — pass `params` directly to `.chat()`, not to the constructor (the SDK ignores `max_new_tokens` in the constructor when using `.chat()`).

## Frontend TypeScript

- `verbatimModuleSyntax: true` is enforced — always `import type` for type-only imports, or the build fails.
- Linter is **oxlint**, not ESLint. Run `npm run lint` from `frontend/` directory.
- No test runner exists — there is no `vitest`/`jest`.
- **`VITE_API_URL`** environment variable controls the backend base URL (default `http://localhost:8000`). It is exported as `BASE_URL` from `frontend/src/api/tramiteApi.ts` and used directly by `TramitePage` to fetch Markdown files from the backend static file server.
- **`frontend/src/data/tramites.ts`** now includes a `homoclave: string` field on the `Tramite` interface (e.g. `"BC-TYS-1582"`). This is the join key between frontend data, the backend `HOMOCLAVE_MAP`, and SQLite.
- Tramite IDs used in routes (`/Portal/TyS/:id`) are numeric integers — the `homoclave` field is separate and used only for API calls, not for routing.
- **`markdownToHtml()`** in `TramitePage.tsx` is a zero-dependency Markdown-to-HTML converter (handles `#`, `##`, `**bold**`, `- list`, blank lines). Do not install `react-markdown` — use this helper.
- React `key` on fragments inside `.map()` must use `<Fragment key={...}>` (imported from `'react'`), not `<>`. Using `<>` with a `key` prop causes a React warning.
