# Plan: Real RETyS Data + Pre-generated Lectura Fácil for Demo

## Overview

Replace the 5 simulated trámites in the frontend with the 5 real RETyS Baja California fichas
from `docs/fichas-dificiles.json`, and pre-generate the Lectura Fácil Markdown for each so the
♿ toggle works end-to-end without calling watsonx during the demo.

**Scope:**
1. **Tarea A — Frontend data**: Replace `frontend/src/data/tramites.ts` with real JSON data,
   extend the `Tramite` type with two optional fields (`urlOficial`, `metricas`), and update
   `TramitePage` to show `urlOficial` in normal view and `metricas` inside the Lectura Fácil panel.
2. **Tarea B — Lectura Fácil Markdown**: Author the 5 `.md` files under `backend/documentos/`
   following the fixed template and the fidelity rules (≤15 words/sentence, no invention, errors
   preserved verbatim, contradictions flagged in a notes section).
3. **Backend wiring**: Add the 5 new homoclaves to `HOMOCLAVE_MAP` and `TRAMITES_DB` in
   `backend/skill_retys.py` so that `GET /admin/tramites` shows them in the admin panel, and
   seed the SQLite DB with the pre-generated file paths via a Python seed script so
   `GET /tramites/{homoclave}/accesible` returns `generado=true` without ever calling the agent.

**Non-goals:**
- No changes to the admin generation pipeline or watsonx integration.
- No audio generation (TTS is absent in demo environment; the Web Speech fallback already works).
- No auth, routing, or new API endpoints beyond what already exists.

---

## Mapping: JSON → Tramite Type

| JSON field | Tramite field | Notes |
|---|---|---|
| `id` | `id` | direct |
| `homoclave` | `homoclave` | direct |
| `nombre` | `titulo` | direct |
| `organismo` | `dependencia` | direct |
| `descripcion` | `descripcion` | direct |
| `fundamento[]` | `fundamento` | join with `"; "` |
| `tiempo_resolucion` | `tiempoResolucion` | direct |
| `vigencia` | `vigencia` | direct |
| `requisitos[]` | `requisitos` | mapped to `Requisito[]` (numero = index+1) |
| `costo` (string) | `costos` | single `Costo` entry; `concepto="Costo"`, `monto=<verbatim costo string>`, `fundamento=""`, `formaPago=""`. `TramitePage` renders a plain `<p>` instead of a table when only one raw-string entry is present (Sub-Task 3). |
| `url` | `urlOficial` | new optional field |
| `metricas` (object) | `metricas` | new optional field (subset) |
| **no JSON source** | `area` | set to `organismo` value (same); flagged as pending |
| **no JSON source** | `documentos` | set to `[]`; flagged as pending |
| **no JSON source** | `contacto.direccion` | `""` for most; BC-CEJUM-001 has address from `texto_original`; others flagged as pending |
| **no JSON source** | `contacto.telefono` | `""` — pending |
| **no JSON source** | `contacto.email` | `""` — pending |
| **no JSON source** | `contacto.horario` | `""` — pending |
| **no JSON source** | `tramitesRelacionados` | `[]` — pending |

---

## File Naming Convention for Markdown

`backend/core/markdown_utils.slug()` is used by the admin pipeline. Pre-generated files must
follow the same naming so the static mount `GET /documentos/<file>.md` resolves correctly.

| homoclave | slug(homoclave) | slug(nombre, 60) | filename |
|---|---|---|---|
| BC-CESPT-041 | `bc-cespt-041` | `registro-o-revalidacion-de-exencion-de-permiso-de-descarga` | `bc-cespt-041_registro-o-revalidacion-de-exencion-de-permiso-de-descarga.md` |
| BC-SH-012 | `bc-sh-012` | `expedicion-de-licencia-de-conducir` | `bc-sh-012_expedicion-de-licencia-de-conducir.md` |
| BC-CEJUM-001 | `bc-cejum-001` | `atencion-integral-a-mujeres-victimas-de-violencia` | `bc-cejum-001_atencion-integral-a-mujeres-victimas-de-violencia.md` |
| BC-SHFP-002 | `bc-shfp-002` | `constancia-de-no-inhabilitacion` | `bc-shfp-002_constancia-de-no-inhabilitacion.md` |
| BC-SSCBC-022 | `bc-sscbc-022` | `expedicion-de-constancia-de-antecedentes-penales` | `bc-sscbc-022_expedicion-de-constancia-de-antecedentes-penales.md` |

> Note: the `slug()` function caps at 60 chars. "registro-o-revalidacion-de-exencion-de-permiso-de-descarga" is 59 chars — within limit.

---

## Sub-Task 1 — Extend the Tramite type

**Status:** [ ] pending

**Intent:** Add `urlOficial?: string` and `metricas?: { inflesz: number; nivel: string; palabras: number; terminosJuridicos: number }` to the `Tramite` interface in `frontend/src/data/tramites.ts`. These are strictly optional so the existing type contract is not broken.

**Relevant files:**
- [`frontend/src/data/tramites.ts`](../frontend/src/data/tramites.ts)

**Expected outcomes:**
- TypeScript compiles without errors (`tsc -b`).
- Both new fields are optional (`?:`), so existing tramites that don't set them still typecheck.

**Todo list:**
1. In `frontend/src/data/tramites.ts`, add after `vigencia: string`:
   ```
   urlOficial?: string
   metricas?: { inflesz: number; nivel: string; palabras: number; terminosJuridicos: number }
   ```
2. Run `npm run build` in `frontend/` to confirm no type errors before proceeding.

---

## Sub-Task 2 — Replace tramites array with real RETyS data

**Status:** [ ] pending

**Intent:** Replace the 5 simulated tramites with the 5 real fichas from `docs/fichas-dificiles.json`.
Map each field as described in the Mapping table above. Use only data present in the JSON; mark absent
fields explicitly (empty string or empty array) and add a `// PENDIENTE` comment inline.

**Fidelity rules (non-negotiable):**
- Preserve `costo` strings verbatim, including `$1,7999.46` (apparent typo in original).
- Set `area` to the same value as `dependencia` — flag as pending.
- `contacto.direccion` for BC-CEJUM-001 can be filled from `texto_original`: `"Avenida Moctezuma #1, Residencial de Cortez, Tijuana, 22190"`. All others: `""`.
- `tramitesRelacionados`: `[]` for all 5 — no cross-references exist in the JSON.
- `documentos`: `[]` for all 5 — no downloadable formats referenced in JSON.

**Relevant files:**
- [`frontend/src/data/tramites.ts`](../frontend/src/data/tramites.ts)
- [`docs/fichas-dificiles.json`](fichas-dificiles.json)

**Expected outcomes:**
- `tramites` array contains exactly 5 entries with real IDs: 1634, 661, 1238, 1131, 1618.
- `npm run lint` passes (oxlint, no unused vars).
- `npm run build` passes.
- Each trámite card on the home page shows the real title and dependencia.
- `/Portal/TyS/1634` (CESPT) loads the real description without 404.

**Todo list:**
1. Replace the entire `const tramites: Tramite[] = [...]` block with the 5 real fichas.
2. For `costos`: each tramite gets a single-entry array with `concepto: "Costo"`, `monto: <verbatim costo string from JSON>`, `fundamento: ""`, `formaPago: ""`.
3. For `requisitos`: map `requisitos[]` → `{ numero: i+1, descripcion: req }` for each entry.
4. For BC-CESPT-041 specifically, the `requisitos` field in the JSON has 4 items but `texto_original` shows many more (multiple secciones). Map the JSON 4 items as-is; add `// PENDIENTE: texto_original contiene requisitos extendidos (Secciones 1–4)` comment inline. The Lectura Fácil .md (Sub-Task 5) will include the full requirements from texto_original.
5. Add `urlOficial` and `metricas` fields to each entry.
6. Add a `// PENDIENTES` comment block at the bottom of the file listing: contacto completo (4 fichas), tramitesRelacionados, documentos (formatos descargables), area (usa dependencia como placeholder).

---

## Sub-Task 3 — Update TramitePage to surface urlOficial and metricas

**Status:** [ ] pending

**Intent:** In the normal view, add a small "🔗 Ficha oficial RETyS" link using `urlOficial`.
Replace the `costos` table with a plain `<p>` when the only cost entry has empty `fundamento` and
`formaPago` (i.e., it's a raw string from JSON). In the Lectura Fácil panel, after the markdown
content, show a collapsible `<details>` block with the `metricas` data so reviewers can see the
original difficulty score without cluttering the citizen view.

**Relevant files:**
- [`frontend/src/pages/TramitePage.tsx`](../frontend/src/pages/TramitePage.tsx)

**Expected outcomes:**
- Normal view: "🔗 Ficha oficial RETyS" link appears when `tramite.urlOficial` is defined.
- LF view: a `<details><summary>Datos de origen</summary>…</details>` block appears below the markdown content when `tramite.metricas` is defined.
- Both sections are absent (no render, no empty space) when the fields are `undefined`.
- `npm run build` and `npm run lint` pass.

**Todo list:**
1. In the normal-view section (after Fundamento Legal `<p>`), add:
   ```tsx
   {tramite.urlOficial && (
     <p style={{ fontSize: '0.85rem' }}>
       🔗 <a href={tramite.urlOficial} target="_blank" rel="noreferrer">
         Ficha oficial en el RETyS BC
       </a>
     </p>
   )}
   ```
2. In the costos section of the normal view, add a conditional: if there is exactly one cost entry
   and `fundamento` and `formaPago` are both empty strings, render `<p>{costo.monto}</p>` instead
   of the full table. Otherwise render the existing table as-is.
3. In the LF view, after the `dangerouslySetInnerHTML` div (inside the `mdContent` branch), add a `<details>` block:
   ```tsx
   {tramite.metricas && (
     <details className="mt-3" style={{ fontSize: '0.8rem', color: '#555' }}>
       <summary style={{ cursor: 'pointer', fontWeight: 600 }}>
         Datos de origen (legibilidad)
       </summary>
       <ul className="mt-2">
         <li>INFLESZ: {tramite.metricas.inflesz} — {tramite.metricas.nivel}</li>
         <li>Palabras: {tramite.metricas.palabras}</li>
         <li>Términos jurídicos: {tramite.metricas.terminosJuridicos}</li>
       </ul>
     </details>
   )}
   ```

---

## Sub-Task 4 — Update HOMOCLAVE_MAP and TRAMITES_DB in backend/skill_retys.py

**Status:** [ ] pending

**Intent:** The admin panel (`GET /admin/tramites`) iterates `HOMOCLAVE_MAP`. The 5 new real
homoclaves must be present there. Each must also have a corresponding entry in `TRAMITES_DB`
with the minimum fields needed by the admin route (`nombre`, `dependencia`).

**Relevant files:**
- [`backend/skill_retys.py`](../backend/skill_retys.py)
- [`backend/api/routes/admin.py`](../backend/api/routes/admin.py)

**Expected outcomes:**
- `GET /admin/tramites` returns 5 rows with the correct nombres and new homoclaves.
- No KeyError when the admin route looks up `TRAMITES_DB[clave_db]`.
- Existing entries (old BC-TYS-* homoclaves) can optionally be removed or left; they do not conflict.

**Todo list:**
1. In `TRAMITES_DB`, add 5 new entries keyed by a stable snake_case key (e.g. `"cespt_041"`,
   `"sh_licencia_conducir"`, `"cejum_001"`, `"shfp_002"`, `"sscbc_022"`). Each entry needs at
   minimum: `nombre`, `dependencia`, `descripcion`, `costo`, `modalidad`, `tiempo_respuesta`.
2. In `HOMOCLAVE_MAP`, add the 5 new mappings:
   ```python
   "BC-CESPT-041": "cespt_041",
   "BC-SH-012":    "sh_licencia_conducir",
   "BC-CEJUM-001": "cejum_001",
   "BC-SHFP-002":  "shfp_002",
   "BC-SSCBC-022": "sscbc_022",
   ```
3. Keep the old 5 BC-TYS-* entries in both dicts — removing them would break any existing DB rows.

---

## Sub-Task 5 — Pre-generate the 5 Lectura Fácil Markdown files

**Status:** [ ] pending

**Intent:** Author the 5 `.md` files that the citizen-facing toggle will serve. These files must
follow the fixed template exactly and the fidelity rules (no invention, errors preserved, ≤15 words
per sentence, active voice, Mexican tuteo).

**Fixed template per file:**
```
# {nombre del trámite}
Fuente: RETyS BC · Homoclave {homoclave} · {url}

## ¿Qué es?
…
## ¿Cuándo lo haces?
…
## ¿Quién puede hacerlo?
…
## ¿Qué necesitas?
1. …
## ¿Cuánto cuesta?
…
## ¿Cuánto tarda?
…
## ¿Cómo lo haces?
1. …
## ¿Dónde?
…
```
> Add `> **Notas para revisión:** …` section at bottom only if there are errors, contradictions, or ilegible data.

**Fidelity notes per ficha:**
- **BC-CESPT-041**: Amount `$1,7999.46` is a clear typo in `texto_original`. Preserve verbatim AND flag in Notas.
- **BC-SH-012**: Include the full cost table (all license types) as a list. Note: the `texto_original` says `"interesadoa"` (typo) — no need to flag this since it only affects the source, not our output.
- **BC-CEJUM-001**: Very sparse original. `texto_original` has address (Tijuana, Av. Moctezuma #1). The fundamento lists many article numbers — copy verbatim.
- **BC-SHFP-002**: Carta poder section in `texto_original` has additional requirements not captured in JSON `requisitos[]` — include those from `texto_original`. Cost note says "actualizándose mensualmente" — include verbatim.
- **BC-SSCBC-022**: Online steps from `texto_original` include a full URL. Preserve it. Note that `pasos` in JSON omits the online modality detail — use `texto_original` for online steps.

**Target files:**
- `backend/documentos/bc-cespt-041_registro-o-revalidacion-de-exencion-de-permiso-de-descarga.md`
- `backend/documentos/bc-sh-012_expedicion-de-licencia-de-conducir.md`
- `backend/documentos/bc-cejum-001_atencion-integral-a-mujeres-victimas-de-violencia.md`
- `backend/documentos/bc-shfp-002_constancia-de-no-inhabilitacion.md`
- `backend/documentos/bc-sscbc-022_expedicion-de-constancia-de-antecedentes-penales.md`

**Expected outcomes:**
- All 5 files exist in `backend/documentos/`.
- Each file starts with `# {nombre}` and has all 8 sections.
- No invented data (cross-check against `texto_original`).
- Sentences are ≤15 words.

**Todo list:**
1. Write `bc-cespt-041_...md` using the CESPT ficha data. Flag `$1,7999.46` in Notas.
2. Write `bc-sh-012_...md` using the SH ficha. Include all cost variants from texto_original.
3. Write `bc-cejum-001_...md` using the CEJUM ficha. Include address from texto_original.
4. Write `bc-shfp-002_...md` using the SHFP ficha. Include carta poder requirements from texto_original.
5. Write `bc-sscbc-022_...md` using the SSCBC ficha. Include both presencial and online steps from texto_original.

---

## Sub-Task 6 — Seed SQLite so the accesible endpoint returns generado=true

**Status:** [ ] pending

**Intent:** `GET /tramites/{homoclave}/accesible` queries SQLite. Without a DB row, it returns
`generado=false`. We need to insert 5 rows (one per ficha) pointing to the pre-generated `.md`
files. This must run once before the demo.

The cleanest approach is a **standalone Python seed script** (`backend/seed_demo.py`) that uses
the same `database.py` + `models/tramite.py` that the API uses, so it's guaranteed to be
consistent. The script does an upsert: insert or update if already exists.

**Relevant files:**
- [`backend/database.py`](../backend/database.py)
- [`backend/models/tramite.py`](../backend/models/tramite.py)
- [`backend/core/markdown_utils.py`](../backend/core/markdown_utils.py) — for the slug() function and DOCUMENTOS_DIR

**Expected outcomes:**
- After running `python backend/seed_demo.py` from project root, `tramites.db` has 5 rows.
- `GET /tramites/BC-CESPT-041/accesible` returns `{"generado": true, "url_documento": "documentos/bc-cespt-041_registro-o-revalidacion-de-exencion-de-permiso-de-descarga.md", ...}`.
- The script is idempotent: running it twice does not create duplicates.

**Todo list:**
1. Create `backend/seed_demo.py`.
2. Import `engine`, `Session`, `Tramite`, `slug` (from `core.markdown_utils`).
3. Define a list of the 5 fichas with `homoclave`, `nombre`, `organismo`, and the expected `ruta_md` path.
4. For each: do `SELECT` by homoclave, then `UPDATE` if found or `INSERT` if not. `ruta_audio=None`.
5. Print a summary line per row: `"✓ BC-CESPT-041 → documentos/bc-cespt-041_..."`.
6. Guard with `if __name__ == "__main__": seed()`.
7. Add instructions to run the seed in the AGENTS.md "Commands" section or in a `# Demo setup` comment block at the top of the seed script.

---

## Pending Items (to document as PR notes)

The following data was absent from the JSON and must be sourced manually before production:

| Campo | Fichas afectadas |
|---|---|
| `contacto.direccion` | BC-CESPT-041, BC-SH-012, BC-SHFP-002, BC-SSCBC-022 |
| `contacto.telefono` | All 5 |
| `contacto.email` | All 5 |
| `contacto.horario` | All 5 |
| `tramitesRelacionados` | All 5 |
| `documentos` (formatos descargables) | All 5 |
| `area` (uses dependencia as placeholder) | All 5 |
| BC-CESPT-041 requisitos Sección 2-4 | Extended requirements in texto_original not fully captured in JSON |

---

## Implementation Order

```
Sub-Task 1 → Sub-Task 2 → Sub-Task 3   (frontend — run npm run build after each)
Sub-Task 4                               (backend skill_retys)
Sub-Task 5                               (markdown files)
Sub-Task 6                               (seed script)
```

Sub-tasks 1–3 are pure frontend. Sub-tasks 4–6 are pure backend. They can be done in either
order relative to each other, but Sub-Task 1 must precede Sub-Task 2 (type must exist before data).
