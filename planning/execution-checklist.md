# Execution Checklist — Direction B MVP (Solo, 1-Week Sprint)

> **Master execution tracker.** Walk through this **one scope at a time**; update as the build
> progresses. Carries every task from the 5 area files with the resolved decisions + cut line from
> `plan.md`. Deferred items are kept and marked `[deferred]` — not deleted.
>
> **Legend:** `- [ ]` todo · `- [x]` done. Each task has checkable **sub-steps** + a `✅ Done when:`
> acceptance line. `[deferred]` = post-MVP · `[content]` = curation not code.
> **Flow** = the 8-step end-to-end flow in `../brainstorming result/direction B summary.md` §2.

---

## Status Matrix

| Area | Status | Core tasks | Deferred | Primary days |
|---|---|---|---|---|
| 4. Cost / Tooling (dev env) | 🟡 In progress — env vars set + Day-1 API checks passed; Docker/clients not yet built | 7 | 1 | Day 1 |
| 3. Database + datasets | ⚪ Not started | 9 | 0 | Day 2–3 |
| 2. Backend & AI | 🟡 Decisions locked, 4 gaps resolved | 16 | 0 | Day 4–7 |
| 1. Frontend UI/UX | 🟡 Decisions locked, UX gaps resolved | 13 | 2 | Day 8–11 |
| 5. QA | 🟡 Rewritten, 11 gaps closed | 8 | 5 | Day 4-12 (shifted left, spans build; final pass Day 12 — see banner) |

Status values: ⚪ Not started · 🟡 In progress · 🟢 Done/locked.

**⏱️ Timeline re-baselined 2026-07-12** (see § Effort & Difficulty Estimates below for the full
audit): the original 1-week/7-day day-map undercounted actual scope by ~45 hours once every
gap-closing session's additions were tallied. **Extended to ~13 working days + buffer**, which still
fits comfortably inside the real Tahap 3 deadline (2026-07-26, ~14 days from 2026-07-12) — the 7-day
figure was always an internal ambition, not the actual submission constraint.

**Day map (re-baselined):** D1 Foundation (Area 4) · D2-3 Database + datasets (Area 3) ·
D4-7 Backend & AI (Area 2) · D8-11 Frontend (Area 1, D10 dedicated to the audio recorder) ·
D12 QA final pass + demo rehearsal (Area 5 T10/T12; shifted-left tests T3/T3b/T4/T5/T6/T8 run
throughout D4-11 as their dependencies land, per the existing failure-gate rule) · D13 buffer/record.

**⚠️ Scope update (2026-07-12, Area-4 session): AUDIO IS BACK IN CORE.** The interview is
**audio voice recording** (not text-only). STT = **Groq `whisper-large-v3` API** (SumoPod has no
STT). This un-defers audio capture (Area 1), STT (Area 2), audio storage + retention (Area 3).
Also added: a **recruiter question edit/approve** step. LLM = **SumoPod**
(`https://ai.sumopod.com/v1`, OpenAI-compatible; `deepseek-v4-pro`, `deepseek-v4-flash`).
Env: `../.env.example`.

### Global conventions (confirmed 2026-07-12)
- **Language:** **Bahasa Indonesia everywhere** — UI, LLM-generated questions, transcripts (STT `id`),
  summaries, reports. Prompts instruct the model to output Indonesian. Datasets curated in Indonesian.
- **Interview length:** **2-3 questions** per candidate.
- **Auth model:** **ONLY the recruiter/HR logs in.** The **candidate has NO account** — they reach the
  consent + interview via an **unguessable token link**; their session is scoped by that token.
- **Result delivery:** **Telegram Bot API only** (email and WhatsApp both dropped). HR triggers
  delivery; the system auto-sends the report FILE (`sendDocument`) + a summary message
  (`sendMessage`). Candidate links Telegram once via a `t.me/<bot>?start=<token>` deep-link on the
  token page (captures `chat_id`); after that, delivery needs no manual click from HR.
  ~~Email/SMTP~~ and ~~WhatsApp `wa.me`~~ **dropped** — Telegram alone is free, fully automatable,
  reliable (no spam-filter risk), and supports real file attachments; email added setup (App
  Password + MIME attachment code) and spam-deliverability risk for no benefit on a solo 1-week
  build. No candidate login required either way.
- **Run mode:** **dev = `uvicorn --reload` on host**; **finalization = full Docker Compose** (backend containerized).

### Confirmed interview & delivery flow (target)
```
HR logs in → posts JD → AI generates interview questions (Flash, 2-3)
   → RECRUITER edits/adjusts + approves questions          [human-in-the-loop]
   → Candidate opens TOKEN LINK (no login) → consent (PDP)
   → Candidate records AUDIO answer (voice)                [audio core]
   → Candidate submits audio
   → STT transcribes audio → text (Groq whisper-large-v3, id)
   → AI summarizes answer + produces development report (skill-gap + training style, Pro)
   → Recruiter sees: raw AUDIO + transcript + AI summary + rubric score
   → Recruiter scores pass / continue-or-not (human decides, no auto-reject)
   → System delivers report to candidate (pass OR fail) via TELEGRAM (file + summary)
```

---

## Area 4 — Cost / Tooling (Dev Environment)  ·  Status: 🟡 In progress (env + API verification done; Docker + client code not started)

> Set up FIRST — Areas 2/3 build on this. Cost story: keep it local + cache SumoPod calls.
> **Locked:** LLM=SumoPod (OpenAI-compat), STT=Groq whisper-large-v3 API, embeddings=local
> multilingual, DB=Postgres(Docker), frontend on host, email off by default. Env: `../.env.example`.
>
> **Machine (confirmed):** Windows 11, Ryzen 7, 24 GB RAM, RTX 3050, Docker working, Python 3.11.
> **Tahap 2 code:** `../brainstorming result/tahap 2 code reference/` (backend/, frontend/, docker-compose.yml).
> **New MVP repo:** `git init` at `implementation/` root; app code in `backend/` + `frontend/` there, `planning/` alongside.
> **Audio format (resolved 2026-07-12): WebM (Opus codec), universally.** Browser `MediaRecorder`'s
> native output; Groq accepts it directly with no transcoding/ffmpeg. Used for BOTH the live
> candidate's real recording and the 2-3 synthetic seed candidates' pre-made clips (Area 3 T10) —
> one format everywhere, no conversion step anywhere in the pipeline.
> **Manual seed source folders (created 2026-07-12):** `../seed/raw/cv/` — place the 30 curated
> Kaggle PDFs here by hand. `../seed/raw/audio/` — place the 2-3 manually pre-recorded `.webm`
> sample answers here (record them once yourself, e.g. via the same interview-recording UI once
> built, or any recorder that outputs webm/opus) — real distinct audio, not a duplicated file, no
> new TTS dependency.

### Task summary

| Task | Status | Summary |
|---|---|---|
| T1. Stack + versions | **Final result** | `backend/`+`frontend/` scaffolded, deps installed clean (frontend via Vite, backend via venv), `uvicorn`/`npm run dev` both verified booting. |
| T2. Docker Compose + run modes | **Final result** | Postgres 16 + Qdrant containers healthy; found and fixed a real port-5432 collision with a pre-existing native Postgres (remapped to 5433). Finalization mode intentionally deferred. |
| T3. Unified LLM client + caching | **Final result** | `llm_client.py` built and verified: cache miss/hit/bypass all behave correctly, token usage logged. |
| T3b. STT client (Groq) | **Final result** | `stt_client.py` verified against two real Indonesian audio clips — both transcribed accurately. |
| T3c. Telegram bot client | **Final result** | `telegram_client.py` verified fully live — deep-link chat_id capture, message send, and document send all confirmed received. |
| T3d. Vision-LLM client | **Final result** | `vision_client.py` verified — SumoPod vision confirmed non-functional, Groq's Llama 4 Scout confirmed working for both transcribe and describe modes. |
| T8. Cost estimate | **Final result** | Projected ≈$0.07/demo run, ≈$0.20 with dev re-runs, from real observed token counts + published rates. Flagged to re-verify against real logs once seed data exists. |
| T4. Local-LLM substitution | **To do** *(deferred)* | Cut from scope — negligible savings for real solo build hours. |

- [x] **T1. Lock the local-first stack + versions. — DONE 2026-07-13.** — *Depends: none · Flow: infra*
  - [x] **Folders scaffolded 2026-07-13**: `backend/` (routers/services/models/db/tests, each a Python package) + `frontend/` (real Vite React-TS app via `npm create vite@5`)
  - [x] Pin frontend deps: React 18.3 + Vite 5.4 + TypeScript 5.6, generated in `frontend/package.json` by the scaffolder
  - [x] **Node upgraded 2026-07-13**: was 18.16 (2023), now **22.23.1** via freshly reinstalled `nvm-windows` (first install attempt silently removed the old Node without completing its own setup — required a clean admin-mode reinstall). `frontend/` deps reinstalled clean under Node 22 — **0 engine warnings** (previously 2). Confirmed `npm run dev` boots Vite on port 5173, matching `.env`'s `FRONTEND_PORT`
  - [x] **Backend deps installed 2026-07-13**: created `backend/.venv`, ran `pip install -r requirements.txt` — all top-level pins resolved with **zero conflicts**, no forced version changes. Full transitive tree frozen to `backend/requirements.lock.txt` (`pip freeze`, 42 packages)
  - [x] Pin PDF deps: `pypdf` + `Pillow` installed as part of the above — **no OCR binary needed** (replicated from NalarX: vision-LLM captioning instead of Tesseract; see Area 3 T5 note)
  - [x] Commit exact versions — `requirements.txt` (top-level pins) + `requirements.lock.txt` (full resolved tree) + `frontend/package-lock.json`, no floating `latest` anywhere
  - ✅ Done when: a fresh clone documents exact versions across `requirements.txt` + `package.json` — **verified**: `uvicorn main:app` booted clean, `GET /health` returned `200 {"status":"ok"}`

- [x] **T2. Docker Compose (DBs) + run modes — dev mode DONE 2026-07-13; finalization mode deferred.** — *Depends: T1 · Flow: infra*
  - [x] Compose services: `postgres:16` + `qdrant:latest` with named volumes (`postgres_data`, `qdrant_data`) + healthchecks (`pg_isready`, TCP check) — `docker-compose.yml` at repo root
  - [x] **Port conflict found + fixed**: a native PostgreSQL 17 Windows service was already listening on host port 5432 (unrelated pre-existing install), silently intercepting connections meant for the container (auth failures traced to `psycopg` connecting to the wrong server). **Remapped Docker Postgres to host port 5433** — `POSTGRES_PORT`/`DATABASE_URL` updated in `.env` + `.env.example`
  - [x] Wire `.env` into the backend — verified via `psycopg` direct connect AND SQLAlchemy engine (`SELECT 1` succeeds) against `localhost:5433`; Qdrant verified via `GET /collections` on `localhost:6333`
  - [x] **Dev mode verified**: `docker compose up -d` (both containers healthy) + `uvicorn main:app --reload` on host (`/health` → 200) — confirmed working together
  - [ ] `[deferred]` **Finalization mode**: adding backend (+ optionally frontend) to Compose for a one-command run — postponed until closer to the demo per `README.md`, dev mode is the working mode for now
  - [x] Document both run modes — `README.md` created at repo root (prereqs, dev-mode steps, the port-5433 note, stop/reset commands)
  - ✅ Done when: dev = `docker compose up` (DBs) + `uvicorn` + `npm run dev` works — **verified**; finalization = full `docker compose up` works — **deferred, not yet attempted**

- [x] **T3. Unified LLM client (SumoPod) + response caching. — DONE 2026-07-13.** — *Depends: T2 · Flow: 2,3,5*
  - [x] **API key + model access verified 2026-07-13**: new `LLM_API_KEY` confirmed working against `gpt-4o-mini`, `deepseek-v4-flash`, `deepseek-v4-pro`, and embeddings (`gemini/gemini-embedding-001`, 1536-dim truncation confirmed)
  - [x] `openai`-SDK client with `base_url=LLM_BASE_URL`, `api_key=LLM_API_KEY` — `backend/services/llm_client.py`, plus `backend/config.py` (central env loader) and `backend/services/llm_cache.py` (disk cache helper)
  - [x] Helpers for `deepseek-v4-flash` and `deepseek-v4-pro` — `chat_flash()` / `chat_pro()`
  - [x] Enforce `temperature=0` for scoring calls — `chat_pro()` always uses `LLM_TEMPERATURE_SCORING` from `.env`, not caller-supplied
  - [x] Disk cache keyed on (prompt hash, model, temp) — JSON files under `storage/llm_cache/`, key = `sha256(model, messages, temperature)`
  - [x] **Cache-bypass parameter**: `bypass_cache=True` kwarg on `chat()`/`chat_flash()`/`chat_pro()`, verified to force a live API call even with identical input already cached
  - [x] Log token usage per call — `prompt_tokens`/`completion_tokens`/`total_tokens` logged on cache miss; cache hits log `tokens=0`
  - [x] **Bug found + fixed during verification**: `STORAGE_DIR=./storage` in `.env` is a relative path meant to resolve at the **repo root** (`implementation/storage/`), but the first test run (invoked from `backend/`) created a stray `backend/storage/` instead. Fixed in `config.py` by resolving `STORAGE_DIR` against `REPO_ROOT` explicitly, regardless of the process's cwd. Re-verified: cache now correctly lands at `implementation/storage/llm_cache/`
  - ✅ Done when: a test call to each model returns — **verified**: call 1 (flash) real API 1.4s, tokens logged 14/54/68; call 2 same input → cache hit, 0.00s, `tokens=0`; call 3 `bypass_cache=True` → forced real API call again, 1.09s; call 4 (`chat_pro`) → real call, `temperature=0` enforced

- [x] **T3b. STT client (Groq `whisper-large-v3`, Bahasa Indonesia). — DONE 2026-07-13.** — *Depends: T2 · Flow: 5*
  - [x] Second `openai`-SDK client with `base_url=STT_BASE_URL` (Groq), `api_key=STT_API_KEY` — `backend/services/stt_client.py`; STT config added to `backend/config.py`
  - [x] `audio.transcriptions.create(model=STT_MODEL, language="id", file=...)` — **tested with `.m4a` and `.mp3`** (no `.webm` sample was available yet, since Area 3's seed audio doesn't exist; Groq accepts both formats directly with no conversion needed, confirming the transcription pipeline + `language=id` setting work — the real app will feed `.webm` from `MediaRecorder`, still to be tested once that pipeline exists)
  - [x] Provider switch honoring `STT_PROVIDER` (groq|openai|local) — `local` raises `NotImplementedError` with a clear message (documented fallback per plan, not built unless Groq becomes unavailable)
  - ✅ Done when: a sample Indonesian audio clip transcribes to correct text via Groq — **verified twice**: `.m4a` → "Halo nama saya Alexander Graham Bell, saya adalah kandidat nomor 7 dan saya memiliki pengalaman hingga 50 tahun data science dengan pengalaman di Python dan juga SQL, terima kasih"; `.mp3` → equivalent correct transcript, both fully accurate Indonesian text

- [x] **T3c. Telegram bot client (ONLY report delivery channel — no email). — DONE 2026-07-13.** — *Depends: T2 · Flow: 8*
  - [x] Create bot via @BotFather → get `TELEGRAM_BOT_TOKEN` (free) — done earlier, bot is `@GaskeunkerjaBot` ("GaskeunKerja Recruitment"), token verified live via `getMe`
  - [x] Client wrapper: `sendDocument` (report file) + `sendMessage` (summary text) — `backend/services/telegram_client.py`; Telegram config added to `backend/config.py`
  - [x] Deep-link handler: `t.me/<bot>?start=<token>` → bot receives `/start <token>` → capture `chat_id`, link it to the candidate session — `extract_start_token()` parses a `getUpdates` entry into `(chat_id, token)`
  - ✅ Done when: opening the deep-link from the token page links a `chat_id`; a test send delivers a file + message to that chat — **verified live end-to-end**: user opened `https://t.me/GaskeunkerjaBot?start=test123`, `getUpdates` correctly captured `chat_id=1304618784` + `token='test123'`; `sendMessage` and `sendDocument` (a test `.txt` "report") both confirmed received in the user's actual Telegram app

- [x] **T3d. Vision-LLM client (scanned-PDF image captioning). — DONE 2026-07-13.** — *Depends: T2 · Flow: 3 (CV parsing)*
  - [ ] **Reference (2026-07-12 Tahap 2 audit):** `backend/config/utils.py::_ocr_pdf_with_gemini()` in the Tahap 2 code is a working version of this exact pattern (rasterize page → send to vision model) — same idea, different provider (Gemini vs SumoPod/Groq) and different trigger (whole-page rasterization vs NalarX's per-embedded-image approach we're using) — read it for validation, don't copy verbatim
  - [x] **Verify first — DONE 2026-07-13:** sent a test image to SumoPod's `deepseek-v4-pro` as an `image_url` content block. **Confirmed NOT supported** — model's own `reasoning_content` showed it reasoning "no image was provided," `prompt_tokens` too low to have ingested image data, returned empty (`finish_reason: length`)
  - [x] ~~If SumoPod supports vision~~ — ruled out by the verification above
  - [x] **Groq vision model selected + verified 2026-07-13:** `meta-llama/llama-4-scout-17b-16e-instruct` — sent the same test image, correctly read back the embedded text (`prompt_tokens: 174`, correct output). Pinned in `.env`/`.env.example` as `VISION_MODEL`, `VISION_PROVIDER=groq` (now primary, not fallback). Reuses the Groq STT client/key from T3b
  - [x] Client call: image bytes → base64 → `image_url` content block — `backend/services/vision_client.py`, reuses the STT client's Groq `base_url`/`api_key` from `config.py`
  - [x] Two prompt modes: **transcribe** (verbatim read-out) and **describe** (caption) — `transcribe_image()` / `describe_image()`, both wrapping a shared `_caption()` helper with mode-specific Indonesian-language prompts
  - ✅ Done when: a sample scanned-CV image returns an accurate verbatim transcription — **verified**: a synthetic "scanned CV page" image (name/role/experience/education/skills as rendered text, simulating a scanned page) transcribed with 100% accuracy via `transcribe_image()`; `describe_image()` on the same image correctly produced a short summary instead, confirming the two modes genuinely behave differently

- [x] **T8. True minimal cost estimate. — DONE 2026-07-13 (projected, pre-seed-data).** — *Depends: T3, T3b · Flow: reporting*
  - [x] **Projected** (not yet a real logged run — Area 3 seed data doesn't exist yet) a full demo run: 30 candidates (27 profile-only, 2-3 synthetic interviews, 1 live), using real per-call token counts observed during T3/T3d testing today plus published DeepSeek/Groq rates as the pricing basis (SumoPod's own rate card wasn't publicly findable — DeepSeek direct pricing used as a defensible proxy)
  - [x] Write the one-line honest figure into `plan.md` — see decision log 2026-07-13
  - ✅ Done when: a defensible cost number exists for the pitch — **≈ $0.07 per full demo run, ≈ $0.20 with dev-cycle re-runs** — **re-verify with real usage logs once Area 3 seed data + a live end-to-end run exist** (this task's original intent was a post-hoc tally from logs; that's not yet possible, so this is a pre-build projection instead, worth confirming later)

- [ ] `[deferred]` **T4. Local-LLM substitution** — cut: negligible saving, real solo hours. (STT is API too, per decision.)

---

## Area 3 — Database + Reference Datasets  ·  Status: 🟡 In progress (T1 done)

> **Blocks Area 2.** Schema early; datasets are `[content]` and gate the report (Area 2 T13) — start Day 2, don't slip.
> Resolved: **PostgreSQL in Docker, via SQLAlchemy, NO Alembic** (`create_all` on fresh demo DB).

**Resolved 2026-07-12 (Area-3 session):**

| Aspect | Decision | Detail / rationale |
|---|---|---|
| Demo role | **Data Analyst** (IT category) | JD, competency framework (T6), resource library (T7) all target this one title |
| CV source | **Kaggle `snehaanbhawal/resume-dataset`**, category `INFORMATION-TECHNOLOGY` | Adjacent categories as fallback if analyst-specific resumes are thin. Real PDF files included in the dataset |
| Candidate count | **30, manually curated** | Deliberate strong / mid / weak-or-mismatched spread — not a random pull — so the ranked shortlist visibly discriminates on camera |
| PII → LLM | **Redacted before the LLM ever sees the CV** | Extracted text has name/email/phone replaced with a placeholder alias prior to the Deepseek parse call (Area 2 T5); only skill-relevant content reaches the LLM |
| PII → stored file | **Raw original PDF stays HR-facing as-is** | Redaction applies to the LLM input + structured DB fields only, not the stored file itself — accepted tradeoff for build speed |
| CV parsing | **Text extraction + vision-LLM caption fallback** (replaces Tesseract/OCR — see below) | Must handle text PDFs, image/scanned PDFs, and mixed pages (Area 2 T5) |
| JD authoring | **Full CRUD, structured fields** | Title, responsibilities, requirements, qualifications (not free text); scoped to the logged-in HR's company; not a one-shot seed insert (Area 2 T4, Area 1 T4b) |

### CV parsing method — replicated from `NalarX-ai-engine` (no Tesseract/OCR binary)

Per user instruction: **no Tesseract/poppler OCR fallback.** Instead, replicate the pattern from
`D:\Data Scientist\Company\NalarX\Projects\NalarX-ai-engine\main` (`backend/app/services/parsers/`):
**native text extraction + per-page empty-text detection + embedded-image extraction sent to a
vision-capable LLM for captioning/transcription** — no page-rendering, no OCR binary, no new system
dependency.

| Step | What happens | NalarX reference |
|---|---|---|
| 1. Extract text | `pypdf.PdfReader`, `page.extract_text()` per page | `file_extraction.py: read_pdf_file()` |
| 2. Detect scanned pages | If a page's extracted text is blank/whitespace → mark page number in `empty_text_pages` (likely scanned) | `file_extraction.py` |
| 3. Extract embedded images | Pull raster images embedded in the PDF per page (`page.images`), tagged with page number | `file_extraction.py: pdf_image_page_number()` |
| 4. Vision-LLM call per image | Image → base64 → sent to a vision-capable chat model as an `image_url` content block | `image_captioning.py: caption_image()` |
| 5. Mode selection | Images on **empty-text pages** → **transcribe** prompt (verbatim OCR-style read-out); images on pages that already have text → **describe** prompt (caption only) | `pdf_captioning.py: merge_pdf_text_and_captions()` |
| 6. Merge | Page text + image transcriptions/captions concatenated into one document blob → this is what gets parsed for skills/experience | `ingest.py: _extract_pdf_text_with_captions()` |

**Adaptation for this project:** the PII-redaction step (Area 2 T5) runs on the merged text blob
*after* step 6, before the Deepseek structured-parse call — so text pulled out of a scanned page via
the vision model is redacted exactly the same way as native text. **Vision-LLM endpoint (resolved
2026-07-12): SumoPod primary** (keeps everything on one provider) **— must be verified Day 1** (its
vision support is unconfirmed pending a live API-key test); **Groq's vision model is the documented
fallback** (reuses the STT client/key already being built, Area 4 T3b). See Area 4 T3d.

### Database Schema Reference

Full column-level detail lives in `area-3-database.md` § Database Schema Reference — this is the
scannable index of what exists, used by T1-T3.

**Datastores**

| Datastore | Type | Purpose |
|---|---|---|
| `gaskeun` (PostgreSQL, Docker) | Relational DB | All structured data — companies, jobs, candidates, scores, decisions, compliance records, reference content |
| Qdrant (Docker) | Vector DB | Candidate + JD embeddings for semantic matching |
| Local filesystem (`storage/`) | File storage | Raw CV PDFs + interview audio recordings (DB stores only the path pointer) |

**PostgreSQL tables (17)**

| Table | Description |
|---|---|
| `companies` | One row per client company using the platform |
| `hr_users` | HR/recruiter login accounts, scoped to a company (the ONLY accounts with a login) |
| `jobs` | Job descriptions (JDs), full CRUD by HR, structured fields |
| `jd_competencies` | Competencies extracted from a JD by the LLM (Flash) |
| `candidates` | One row per candidate; reached via an unguessable token link, not login |
| `parsed_profiles` | Structured CV data (skills/experience/qualifications), tagged to an anonymized alias |
| `match_scores` | Candidate ↔ JD ranking score, with per-competency breakdown for explainability |
| `interview_questions` | AI-generated interview questions per job, editable/approvable by HR |
| `interview_answers` | One row per candidate's audio answer to a question |
| `transcripts` | STT output (Groq) for each interview answer |
| `rubric_scores` | Per-criterion rubric score + rationale for each interview answer (temperature=0) |
| `interview_summaries` | AI-generated summary of a candidate's full interview, shown to HR |
| `hr_decisions` | HR's final human decision per candidate — separate from any AI score |
| `consent_records` | Candidate's PDP consent record, gates interview processing |
| `audit_log` | Every AI decision point + candidate-data access, for auditability |
| `competency_framework` | `[content]` Skill taxonomy for the demo role (Data Analyst), with lightweight relations |
| `resource_library` | `[content]` Curated learning resources keyed to competencies, powers the deterministic report |

**Qdrant collections (2)**

| Collection | Payload | Purpose |
|---|---|---|
| `jd_vectors` | `job_id`, competency metadata | JD embedding for semantic matching |
| `candidate_vectors` | `candidate_id`, competency metadata | Candidate profile embedding for semantic matching |

**PostgreSQL columns (all 17 tables)**

| Table | Column Name | Column Description |
|---|---|---|
| `companies` | `id` | Primary key |
| `companies` | `name` | Company display name |
| `companies` | `created_at` | Row creation timestamp |
| `hr_users` | `id` | Primary key |
| `hr_users` | `company_id` | FK → `companies` |
| `hr_users` | `email` | Login identifier, unique |
| `hr_users` | `password_hash` | Hashed login credential |
| `hr_users` | `created_at` | Row creation timestamp |
| `jobs` | `id` | Primary key |
| `jobs` | `company_id` | FK → `companies`, scopes the JD to one company |
| `jobs` | `title` | Structured field |
| `jobs` | `responsibilities` | Structured field |
| `jobs` | `requirements` | Structured field |
| `jobs` | `qualifications` | Structured field |
| `jobs` | `status` | `draft` / `active` / `closed` |
| `jobs` | `created_at` | Row creation timestamp |
| `jobs` | `updated_at` | Last-edit timestamp |
| `jd_competencies` | `id` | Primary key |
| `jd_competencies` | `job_id` | FK → `jobs` |
| `jd_competencies` | `competency_name` | Name of the required competency |
| `jd_competencies` | `importance_level` | Weight used in matching (Area 2 T7) |
| `candidates` | `id` | Primary key |
| `candidates` | `job_id` | FK → `jobs` |
| `candidates` | `alias` | Anonymized display name (e.g. `Kandidat IT-07`) — never the real name |
| `candidates` | `token` | Unguessable link identifier for the candidate's own session |
| `candidates` | `token_expires_at` | Expiry, from `CANDIDATE_TOKEN_TTL_HOURS` |
| `candidates` | `telegram_chat_id` | Captured after the candidate links via the deep-link; nullable |
| `candidates` | `created_at` | Row creation timestamp |
| `parsed_profiles` | `id` | Primary key |
| `parsed_profiles` | `candidate_id` | FK → `candidates` |
| `parsed_profiles` | `skills` | Structured LLM output |
| `parsed_profiles` | `experience` | Structured LLM output |
| `parsed_profiles` | `qualifications` | Structured LLM output |
| `parsed_profiles` | `raw_cv_path` | Pointer to the original, un-redacted PDF file (still HR-facing) |
| `parsed_profiles` | `parsed_at` | Parse timestamp |
| `match_scores` | `id` | Primary key |
| `match_scores` | `candidate_id` | FK → `candidates` |
| `match_scores` | `job_id` | FK → `jobs` |
| `match_scores` | `overall_score` | Aggregate match score |
| `match_scores` | `competency_breakdown` | Per-competency detail — the explainability data for Q17 |
| `match_scores` | `rank` | Candidate's rank for this job |
| `match_scores` | `computed_at` | Computation timestamp |
| `interview_questions` | `id` | Primary key |
| `interview_questions` | `job_id` | FK → `jobs` |
| `interview_questions` | `question_text` | Editable by HR |
| `interview_questions` | `order_index` | Display/ask order |
| `interview_questions` | `status` | `draft` / `approved` — candidate only sees `approved` |
| `interview_questions` | `created_at` | Row creation timestamp |
| `interview_answers` | `id` | Primary key |
| `interview_answers` | `candidate_id` | FK → `candidates` |
| `interview_answers` | `question_id` | FK → `interview_questions` |
| `interview_answers` | `audio_path` | Pointer to the stored `.webm` recording |
| `interview_answers` | `submitted_at` | Submission timestamp |
| `transcripts` | `id` | Primary key |
| `transcripts` | `answer_id` | FK → `interview_answers` |
| `transcripts` | `transcript_text` | Groq `whisper-large-v3` output, `language=id` |
| `transcripts` | `created_at` | Row creation timestamp |
| `rubric_scores` | `id` | Primary key |
| `rubric_scores` | `answer_id` | FK → `interview_answers` |
| `rubric_scores` | `criterion_name` | e.g. clarity, relevance, technical depth |
| `rubric_scores` | `score` | Scored at temperature=0 for determinism |
| `rubric_scores` | `rationale` | LLM's justification for the score |
| `interview_summaries` | `id` | Primary key |
| `interview_summaries` | `candidate_id` | FK → `candidates` |
| `interview_summaries` | `ai_summary_text` | Main-points summary shown to HR alongside audio + transcript |
| `interview_summaries` | `overall_score` | Aggregate across `rubric_scores` |
| `interview_summaries` | `created_at` | Row creation timestamp |
| `hr_decisions` | `id` | Primary key |
| `hr_decisions` | `candidate_id` | FK → `candidates` |
| `hr_decisions` | `decision` | `advance` / `reject` / `pending` — human-entered only, no auto-set |
| `hr_decisions` | `decided_by` | FK → `hr_users` |
| `hr_decisions` | `decided_at` | Decision timestamp |
| `hr_decisions` | `notes` | Optional HR notes |
| `consent_records` | `id` | Primary key |
| `consent_records` | `candidate_id` | FK → `candidates` |
| `consent_records` | `consent_given` | Boolean PDP consent flag |
| `consent_records` | `consent_text_version` | Which consent wording was shown |
| `consent_records` | `consented_at` | Consent timestamp |
| `audit_log` | `id` | Primary key |
| `audit_log` | `actor` | `hr_user_id`, `"system"`, or `"candidate"` |
| `audit_log` | `action` | e.g. `cv_parsed`, `match_computed`, `interview_scored`, `decision_recorded` |
| `audit_log` | `entity_type` | Type of the entity the action touched |
| `audit_log` | `entity_id` | ID of the entity the action touched |
| `audit_log` | `metadata` | Extra context, jsonb |
| `audit_log` | `created_at` | Row creation timestamp |
| `competency_framework` | `id` | Primary key |
| `competency_framework` | `job_role` | `"Data Analyst"` (the one demo role) |
| `competency_framework` | `competency_name` | Name of the competency |
| `competency_framework` | `level_description` | Description of proficiency levels |
| `competency_framework` | `related_competency_ids` | Lightweight graph relations feeding Area 2 T7's matching boost |
| `resource_library` | `id` | Primary key |
| `resource_library` | `competency_id` | FK → `competency_framework` |
| `resource_library` | `title` | Resource title |
| `resource_library` | `duration` | Estimated time to complete |
| `resource_library` | `milestone_description` | What completing it demonstrates |
| `resource_library` | `url` | Optional link |

### Task summary

| Task | Status | Summary |
|---|---|---|
| T1. DB connection | **Final result** | SQLAlchemy engine + `create_all()` wired and verified against the Docker Postgres — idempotent restart confirmed. |
| T2. Schema (17 tables) | **Final result** | All 17 models built and verified — `create_all` produces every table, FKs and JSONB/array columns confirmed correct. |
| T3. Qdrant collections | **Final result** | `candidate_vectors` + `jd_vectors` collections created and verified with a real upsert/query round-trip. |
| T4. File storage layout | **Final result** | Isolated per-candidate folders for CV + audio verified — layout, isolation, and round-trip all confirmed. |
| T5. Repository layer | **To do** | Thin CRUD repositories over SQLAlchemy. |
| T6. Competency framework `[content]` | **To do** | ~8-12 competencies for the Data Analyst demo role, with lightweight relations. |
| T7. Resource library `[content]` | **To do** | ~3 curated resources per competency. |
| T8. Consent + audit write paths | **To do** | Audit-log helper + consent gate enforcement. |
| T9. Retention policy | **To do** | Light retention rule scoped to the 1 live candidate's real consented audio. |
| T10. Seed data | **To do** | Kaggle-sourced, curated, anonymized, tiered 30-candidate seed set — the single biggest time sink in the plan. |

- [x] **T1. DB connection locked: PostgreSQL (Docker). — DONE 2026-07-13.** — *Depends: Area4 T2 · Flow: all persistence*
  - [x] SQLAlchemy engine + session factory from `DATABASE_URL` — `backend/db/session.py` (`engine`, `SessionLocal`, `Base`, `get_db()`); `DATABASE_URL` added to `backend/config.py`
  - [x] `create_all()` on startup (no migrations) — wired into `main.py`'s `@app.on_event("startup")`; one placeholder model (`backend/models/company.py::Company`, the `companies` table) added just to give `create_all()` something real to prove against — the full 17-table schema is T2's job, not T1's
  - ✅ Done when: backend creates all tables on boot against Compose Postgres — **verified**: cleared the DB (`\dt` → no relations), booted `uvicorn`, confirmed `companies` table created with correct schema (`\d companies`); restarted `uvicorn` again against the now-existing table — booted clean with no error, confirming `create_all()` is safely idempotent

- [x] **T2. Schema for the ~17 happy-path entities. — DONE 2026-07-13.** — *Depends: T1 · Flow: all*
  - [x] Core: `companies`, `hr_users`, `jobs`, `jd_competencies`, `candidates`, `parsed_profiles` — `backend/models/company.py`, `hr_user.py`, `job.py`, `candidate.py`, `parsed_profile.py`
  - [x] Matching: `match_scores` (+ per-competency detail) — `backend/models/match_score.py`, `competency_breakdown` as JSONB
  - [x] Interview: `interview_questions`, `interview_answers`, `transcripts`, `rubric_scores`, `interview_summaries` — all in `backend/models/interview.py`
  - [x] Decision/compliance: `hr_decisions`, `consent_records`, `audit_log` — `backend/models/hr_decision.py`, `consent.py`, `audit_log.py` (`metadata` column mapped to Python attribute `audit_metadata` — `metadata` is a reserved name on SQLAlchemy's `DeclarativeBase`)
  - [x] Reference tables (T6/T7): `competency_framework`, `resource_library` — `backend/models/reference.py`; `related_competency_ids` as a Postgres integer array
  - [x] Full column-level detail: see `area-3-database.md` § Database Schema Reference — all 17 models' columns cross-checked against this table, exact match
  - [x] `backend/models/__init__.py` now imports and registers all 17 models on `Base.metadata`; `main.py` imports the package so `create_all()` picks up the full schema
  - ✅ Done when: `create_all` builds every table; explicit `consent_records` + `audit_log` present — **verified**: cleared to just the T1 placeholder (`companies` only), booted `uvicorn`, confirmed all 17 tables now exist (`\dt`); spot-checked `audit_log` (confirms `metadata` column mapping works) and `interview_answers` (confirms FKs + the `rubric_scores`/`transcripts` reverse-reference chain all wired correctly)

- [x] **T3. Local Qdrant collections + payload schema. — DONE 2026-07-13.** — *Depends: Area4 T2 · Flow: 4*
  - [x] Create `candidate_vectors` + `jd_vectors` collections — `backend/db/vector_store.py`, `create_collections()`; `EMBEDDING_DIMENSIONS`-sized (1536), cosine distance; wired into `main.py` startup alongside `create_all()`; `QDRANT_HOST`/`PORT`/`URL` added to `config.py`
  - [x] Payload = ids + competency metadata needed for explainable matching — verified with a real upsert (`candidate_id` + `competencies` list payload)
  - ✅ Done when: a test upsert + query round-trips — **verified**: both collections confirmed created (`GET /collections`), upserted a 1536-dim test vector with realistic payload, queried it back — got the exact point, correct payload, ~1.0 similarity score for the identical vector; test point cleaned up afterward

- [x] **T4. Local file storage for CV + interview audio. — DONE 2026-07-13.** — *Depends: none · Flow: 3, 5*
  - [x] Layout: `storage/cv/<candidate_id>/original.pdf` and `storage/audio/<candidate_id>/<session>/answer_<n>.webm` — `backend/services/storage.py` (`cv_path()`, `audio_path()`, `save_cv()`, `save_audio()`)
  - [x] Naming convention + per-candidate folder isolation — verified: candidate 1 and candidate 2's CVs land in distinct folders (`cv/1/` vs `cv/2/`)
  - [x] DB stores only the **file path pointer**; the file itself never enters Postgres — `save_cv()`/`save_audio()` return the path string, which is what `parsed_profiles.raw_cv_path` / `interview_answers.audio_path` store
  - [x] `parsed_profiles` (structured, anonymized skill data) is the separate DB row the app reads/displays for matching/reports; the **raw original PDF is still shown to HR as-is** on request (resolved: redaction scope is LLM-input + structured data only, not the stored file) — schema already supports this (T2)
  - ✅ Done when: CV + audio land in the right isolated folders, path retrievable by the recruiter — **verified**: saved a CV + an audio file for candidate 1, confirmed both exist on disk at the exact expected paths; saved a second candidate's CV and confirmed the paths don't collide; read the saved CV back and confirmed byte-for-byte content match

- [ ] **T5. Data access layer (repository pattern).** — *Depends: T2 · Flow: all*
  - [ ] Thin repositories/CRUD over SQLAlchemy (no Alembic)
  - ✅ Done when: each entity has get/create used by services

- [ ] **T6. `[content]` Competency framework — ONE demo role: Data Analyst (IT).** — *Depends: T2 · Flow: 4, 8*
  - [ ] List ~8-12 competencies with levels (e.g. SQL, Excel/spreadsheet, data visualization, statistics, Python/R, data cleaning, dashboarding, business communication)
  - [ ] Encode lightweight relations (parent/related) feeding the matching graph (Area 2 T7)
  - [ ] Store as seed rows in the reference table
  - ✅ Done when: one role fully covered; relations queryable; used by matching + report

- [ ] **T7. `[content]` Curated resource library — same role.** — *Depends: T6 · Flow: 8*
  - [ ] ~3 resources per competency (title, duration, milestone), keyed to competency ids
  - [ ] Enough to assemble a deterministic report
  - ✅ Done when: every competency has ≥1 mapped resource; report can select/order from it

- [ ] **T8. Consent + audit write paths.** — *Depends: T2 · Flow: 5, 6*
  - [ ] Helper writes an `audit_log` row at every AI decision point + candidate-data access
  - [ ] Consent row gates interview processing
  - [ ] Consent is only ever written for candidates who actually go through the interview-gate step (the 1 live demo candidate) — **seed-only candidates get no `consent_records` row** (resolved 2026-07-12: they never reach the gate, so a record would be fabricated, not real)
  - ✅ Done when: each AI stage leaves an audit row; no interview processing without consent

- [ ] **T9. Audio + CV retention/cleanup policy (light).** — *Depends: T4, T8 · Flow: 5 (PDP)*
  - [ ] Define a simple retention rule tied to the consent record (audio)
  - [ ] **Scope note:** the policy applies to real, consented recordings — i.e. only the 1 live demo candidate's audio. The 2-3 synthetic candidates' pre-made `.webm` clips are seed fixtures, not personal data collected under consent, so they're exempt (no consent record exists for them to tie a retention rule to — see T8)
  - [ ] Provide a callable manual cleanup helper
  - ✅ Done when: policy documented + cleanup callable exists (supports UU PDP)

- [ ] **T10. Seed data for demo — Kaggle-sourced, curated, anonymized, tiered.** — *Depends: T2, T6, T7 · Flow: all*
  - [ ] 1 company + 1 seeded HR account (JD itself created via the in-app CRUD flow, Area 2 T4/Area 1 T4b — not a raw DB insert). **Single company for MVP** (resolved 2026-07-12: no second company/isolation demo — isolation logic still exists in code, Area 2 T3, just not shown on camera)
  - [ ] **Manual for now (resolved 2026-07-12):** download `snehaanbhawal/resume-dataset` from Kaggle by hand (no Kaggle API/credential this week), filter category `INFORMATION-TECHNOLOGY` (+ adjacent categories if Data Analyst resumes are thin), and place the **30 curated candidate PDFs** into `../seed/raw/cv/` — the seed script reads from that folder
  - [ ] **Manually curate 30 candidate PDFs** for a spread: clear strong-fit tier, mid tier, weak/mismatched tier — so the ranking visibly discriminates
  - [ ] **Record the intended match-quality tier per candidate in the seed manifest itself (resolved 2026-07-12)** — a simple dict/CSV column (`candidate_id → strong|mid|weak`) alongside the seed script, not just a curation-time judgment call that's lost afterward. This is what QA Area 5 T5 asserts against — without it, the matching test has no ground truth to check
  - [ ] Run each through the anonymization + parse pipeline (Area 2 T5) before seeding — structured DB/LLM input never holds raw Kaggle PII (raw PDF file itself is kept as-is, HR-facing)
  - [ ] **Candidate interview-data tiers** (resolved 2026-07-12): of the 30 —
    - **27 profile-only**: `parsed_profiles` + `match_scores` only, no interview data at all (demonstrates matching/ranking)
    - **2-3 pre-seeded synthetic interviews**: get real distinct `.webm` audio clips (manually pre-recorded once, placed in `../seed/raw/audio/` — see Area 4 banner) + `transcripts` + `rubric_scores` + `interview_summaries`, written directly to DB (not run through the live pipeline) — populates the HR-review screen (Area 1 T7) across multiple candidates with genuinely playable, non-duplicated audio. **Also seed an `hr_decisions` row for each (resolved 2026-07-12)** — advance/reject already recorded — so their candidate-detail page shows a completed "decided, report sent" state instead of a live, clickable-but-broken send-report button (they have no `telegram_chat_id`)
    - **1 live candidate**: NO interview data pre-seeded — this candidate is walked through the real flow during demo recording (consent → Telegram link → record real audio → real STT/rubric/summary → HR review → decision → Telegram delivery)
  - [ ] Competency + resource rows (from T6/T7)
  - ✅ Done when: one command loads a demo-ready DB (30 curated, anonymized-for-LLM candidates, correctly tiered) with no manual DB fiddling

---

## Area 2 — Backend & AI Integration  ·  Status: ⚪ Not started

> Largest area, core of the MVP. Reuse Tahap 2 FastAPI + CV-parse. All LLM via SumoPod + caching (Area4 T3).
> Resolved: **T7 semantic+graph**, **T10 audio→Groq STT**, **T11 rubric temp=0**, **+T9b recruiter edit/approve**.

**Resolved 2026-07-12 (Area-2 session):**

| Aspect | Decision | Detail / rationale |
|---|---|---|
| Invite step (gap found) | **HR clicks "Invite" → backend generates token → UI shows copyable link** | New task T9c. No auto-distribution — for the demo, you (playing HR + candidate) copy/open it yourself. Simplest, matches a controlled recording |
| Rubric (T11) | **3 criteria, 1-5 scale**: clarity, relevance, technical depth | Each level anchored with a short description (1=vague/off-topic … 5=clear/precise/correct); curated as `[content]`, same category as the competency framework |
| Report format (T13/T14) | **Real PDF via `weasyprint`** (HTML/CSS template → PDF) | Matches CV-file expectations and what Telegram's `sendDocument` should deliver; pip-installable, verify Windows OS-lib requirements Day 1 |
| Matching formula (T7) | **Weighted sum, similarity-dominant**: `overall_score = 0.7 × semantic_similarity + 0.3 × graph_boost` | Explainable in one sentence to a judge; semantic similarity (the reliable part) stays primary, graph relations add a visible secondary nudge |

**Resolved 2026-07-12 (Area-2 gap-closing pass):**

| Aspect | Decision | Detail / rationale |
|---|---|---|
| Report gating (T13/T14) | **Requires an HR decision (T12) to exist first** | Matches the actual flow (interview → decision → report); only candidates who reached a decision have meaningful interview data and (for the live one) a Telegram `chat_id` to deliver to |
| JD delete (T4) | **Soft-delete only** — flips `jobs.status` → `closed`, no SQL `DELETE` | Avoids FK errors against `candidates`/`interview_questions`/`audit_log`; protects the audit-log-integrity principle. "Delete" in the UI means "archive" |
| CV parsing dependency (T5) | **Fixed a doc bug**: T5 no longer depends on T4 (JD) | A CV parses into skills/experience independent of any job description — only matching (T7) needs both; the old dependency was a copy-paste error |
| Consent enforcement (T10) | **Made explicit**: T10 now states the hard check | `POST` answer-intake must reject (403) if no `consent_records` row exists for the candidate — this is exactly what Area 5 QA T8 tests, so it shouldn't be left implicit |

### Service / Module Inventory

| # | Service / Module | What it does | Endpoint(s) | Built in | Depends on |
|---|---|---|---|---|---|
| 1 | `auth.py` | JWT issue/verify for HR login; unguessable token generation + validation for candidate sessions | `POST /auth/login` | T3 | Area 4 T2 |
| 2 | `jobs.py` (router) + `extract.py` (service) | Full JD CRUD; on create/edit, calls LLM to extract structured competencies | `POST/GET/PUT/DELETE /jobs`, `GET /jobs/{id}` | T4 | SumoPod (Flash), DB |
| 3 | `candidates.py` (router) + `cv_parser.py` (service) | Ingests a CV: `pypdf` text extraction → vision-LLM caption fallback for scanned pages → merge → PII redaction → Deepseek parse → structured profile | `POST /candidates` (HR/seed-side only) | T5 | Area 4 T3d (vision), SumoPod (Flash), DB T4 |
| 4 | `embeddings.py` | Embeds candidate profiles + JD competencies, upserts to Qdrant | (internal, triggered by T4/T5) | T6 | sentence-transformers, DB T3 (Qdrant) |
| 5 | `matching.py` | Ranks candidates for a JD: `0.7 × semantic_similarity + 0.3 × graph_boost`, keeps per-competency detail | `GET /jobs/{id}/candidates` (ranked) | T7 | T6, DB T6 (framework) |
| 6 | `skillgap.py` | Per-candidate skill-gap analysis vs JD competencies | (internal, feeds T13) | T8 | T7, SumoPod (Pro) |
| 7 | `interview_questions.py` | Generates 2-3 Indonesian interview questions from the JD; HR edit/approve workflow | `POST /jobs/{id}/questions`, `GET/PUT /jobs/{id}/questions`, `POST .../approve` | T9, T9b | T4, SumoPod (Flash) |
| 8 | `invite.py` | HR invites a shortlisted candidate — generates the unguessable token/link (no auto-distribution) | `POST /candidates/{id}/invite` | T9c | T7, T9b |
| 9 | `interview_answers.py` | Accepts candidate's audio answer, stores it, sends to STT | `POST /candidates/{id}/answers` | T10 | T9c, Area 4 T3b (Groq STT), DB T4 |
| 10 | `rubric.py` | Fixed-rubric scoring (3 criteria: clarity, relevance, technical depth — 1-5 scale) of the transcript at temp=0 + AI summary | (internal, triggered after T10) | T11 | T10, SumoPod (Pro) |
| 11 | `decisions.py` (router) | Records HR's final pass/reject decision; no auto-finalize path | `POST /decisions` | T12 | T11, DB T8 (audit) |
| 12 | `report.py` | Assembles report content (skill-gap + framework + resource library) and renders it as **PDF via `weasyprint`** — gated on an `hr_decisions` row existing | (internal, triggered by HR action) | T13 | T12, T8, DB T6/T7 |
| 13 | `delivery.py` | Sends the PDF + summary via Telegram | `POST /candidates/{id}/send-report` | T14 | T13, Area 4 T3c (Telegram) |
| 14 | Async/caching/retry layer | Cross-cutting: async orchestration, retries on LLM/STT calls, response caching | n/a (wraps 1-13) | T15 | Area 4 T3 (cache) |
| 15 | OpenAPI contract | Auto-generated typed contract for the frontend | `/openapi.json` | T16 | T15 |

Module #14 is cross-cutting (no dedicated router/service file — wraps the others via decorators/middleware); #15 isn't hand-written, it's FastAPI's auto-generated output from the typed endpoints above.

### Task summary

| Task | Status | Summary |
|---|---|---|
| T1. Audit Tahap 2 backend | **Final result** | Full 10-point code audit done — keep/rebuild/drop verdict written into `CLAUDE.md`. |
| T2. Project structure | **To do** | `routers/services/models/db` FastAPI layout + env loading. |
| T3. Auth | **To do** | JWT for HR login, unguessable token links for candidates. |
| T4. JD full CRUD + extraction | **To do** | Structured-field CRUD + Flash-model competency extraction, soft-delete only. |
| T5. CV parse + PII redaction | **To do** | Text/vision-fallback extraction merged, then mandatory PII redaction before any LLM call — highest-difficulty task in the plan. |
| T6. Embeddings → Qdrant | **To do** | Embed candidate profiles + JD competencies, upsert to Qdrant. |
| T7. Matching engine | **To do** | Weighted semantic + competency-graph score, explainable per-competency detail. |
| T8. Skill-gap analysis | **To do** | Deepseek Pro candidate-vs-JD gap output, grounded via a deterministic seed. |
| T9. Interview question gen | **To do** | 2-3 Indonesian questions generated from the JD. |
| T9b. Recruiter edit/approve | **To do** | Human-in-the-loop approval gate before candidates see questions. |
| T9c. Invite candidate | **To do** | Generates the unguessable token link, HR copies it manually. |
| T10. Answer intake + STT | **To do** | Consent-gated audio upload + Groq transcription. |
| T11. Rubric scoring + summary | **To do** | Fixed 3-criteria rubric at temperature=0 + AI answer summary. |
| T12. HR decision endpoints | **To do** | Records the human pass/reject decision, no auto-finalize path. |
| T13. Report generation | **To do** | Deterministic report assembly, gated on a decision existing. |
| T14. Report delivery | **To do** | PDF via adapted ReportLab code, sent through Telegram. |
| T15. Async wiring + error handling | **To do** | Cross-cutting orchestration/retry/caching layer. |
| T16. OpenAPI contract | **To do** | FastAPI auto-generated, no dedicated work beyond typed endpoints. |

### Foundation
- [x] **T1. Audit Tahap 2 backend repo — DONE 2026-07-12.** — *Depends: none · Flow: reuse for 3*
  - [x] Read `../brainstorming result/tahap 2 code reference/backend/` — full 10-point code audit completed this session
  - [x] Identify reusable FastAPI structure + working CV-parse — verdict: structure is a LangGraph agent pipeline (not reusable as-is); CV **text extraction** (pdfplumber + Gemini-vision fallback) is genuinely working and pattern-reused in T5; **PDF report generation** (ReportLab, ~700 lines) is fully working and reused in T14; skill-gap grounding pattern (`_build_seed_gap`) reused in T8
  - [x] **Strip all scraping code** — confirmed not applicable: no scraping pipeline exists in this codebase at all
  - [x] Note what's real vs merely designed (esp. security) — **confirmed absent, not just unverified**: zero auth code (no JWT, no login endpoint, all endpoints unauthenticated), zero DB/ORM (in-memory dict only, lost on restart), zero vector DB/embeddings/KGE. Full corrected inventory in `CLAUDE.md` § Existing Code To Reuse
  - ✅ Done when: a written keep/rebuild/drop verdict per component exists — **see `CLAUDE.md` correction + this file's § Effort & Difficulty Estimates for the per-task breakdown**

- [ ] **T2. Project structure.** — *Depends: T1, Area4 T2 · Flow: all*
  - [ ] `routers/ services/ models/ db/ services/llm.py config`
  - [ ] Env loading for keys
  - ✅ Done when: uvicorn boots; `/health` returns ok

- [ ] **T3. Auth — HR-only login + tokenized candidate links.** — *Depends: T2 · Flow: all (isolation)*
  - [ ] JWT issue/verify for **recruiter/HR only** (seeded account; no candidate signup)
  - [ ] Unguessable **token link** for candidate access (consent + interview), scoped to one session
  - [ ] Guard: HR routes require JWT; candidate routes require a valid session token (own session only)
  - ✅ Done when: only HR can log in; a candidate token opens only its own interview session; no candidate account exists

### Ingestion & extraction
- [ ] **T4. JD full CRUD + competency extraction (Flash).** — *Depends: DB T2, Area4 T3 · Flow: 1→2*
  - [ ] `POST /jobs` — accepts **structured fields** (title, responsibilities, requirements, qualifications; see Area 1 T4b), scoped to `company_id`
  - [ ] `GET /jobs` — list JDs for the logged-in HR's company
  - [ ] `GET /jobs/{id}` — view one
  - [ ] `PUT /jobs/{id}` — edit (re-triggers competency extraction)
  - [ ] `DELETE /jobs/{id}` — **soft-delete (resolved 2026-07-12)**: sets `status='closed'`, no SQL `DELETE`; JD drops from the active list but all linked candidates/interviews/decisions/audit rows stay intact
  - [ ] On create/update: Deepseek Flash → structured required competencies → persist to `jd_competencies`
  - ✅ Done when: HR can create/list/edit/close JDs; posting/editing the demo JD yields structured competencies in DB; "delete" never throws an FK error or drops audit history

- [ ] **T5. CV upload + parse — text + vision-LLM caption fallback + PII redaction.** — *Depends: DB T4, Area4 T3, Area4 T3d · Flow: 3*
  - [ ] **Tahap 2 reuse (2026-07-12 audit):** `backend/config/utils.py::read_file_node()` has a working `pdfplumber`-based text-extraction + empty-page-detection implementation — read it and adapt the extraction technique directly; it validates the "extract → detect empty → fall back" approach this task also uses. PII redaction, SumoPod integration, and structured-output validation below are still new work (Tahap 2's own JSON parsing is regex+`json.loads` with silent fallback — explicitly a pattern to avoid, not copy)
  - [ ] `POST /candidates` accepts PDF — **HR/admin-side (or seed script) only for MVP**, not a public candidate-facing endpoint (resolved 2026-07-12: no self-apply upload this week, see Area 1 T8 note); the same endpoint/pipeline is what the seed script calls for all 30 demo candidates
  - [ ] `pypdf.PdfReader` → extract text per page; mark pages with blank/whitespace text as `empty_text_pages` (replicated from NalarX `file_extraction.py`)
  - [ ] Extract embedded images per page (`page.images`), tagged by page number
  - [ ] Per image: send to vision-capable LLM — **transcribe** mode if on an `empty_text_pages` page, **describe** mode otherwise (replicated from NalarX `pdf_captioning.py`/`image_captioning.py`)
  - [ ] Merge page text + image transcriptions/captions into one document blob (handles text-only, scanned, and mixed PDFs uniformly)
  - [ ] **PII redaction on the merged text BEFORE the LLM parse call**: strip/replace name, email, phone, address with a placeholder alias (e.g. `Kandidat IT-07`) — only skill-relevant content is sent to Deepseek
  - [ ] Parse redacted text → structured profile (skills/experience/qualifications), tagged with the alias only
  - [ ] Store original file as-is (DB T4, HR-facing) + parsed/anonymized rows
  - ✅ Done when: all 30 seed CVs (real PDFs, Kaggle) parse correctly regardless of text/scanned/mixed format; no real name/email/phone reaches the LLM or the structured DB row

- [ ] **T6. Embeddings → Qdrant (local multilingual sentence-transformers).** — *Depends: T4, T5, DB T3 · Flow: 4*
  - [ ] Embed candidate profile + JD competencies
  - [ ] Upsert to Qdrant collections with competency payload
  - ✅ Done when: vectors present for JD + all candidates; query returns neighbors

### Matching & analysis
- [ ] **T7. Matching engine — semantic + lightweight competency-graph.** — *Depends: T6, DB T6 · Flow: 4*
  - [ ] Qdrant similarity as base score
  - [ ] Boost using competency-graph relations from the framework (related-competency credit)
  - [ ] **Combine via weighted sum (resolved 2026-07-12)**: `overall_score = 0.7 × semantic_similarity + 0.3 × graph_boost`
  - [ ] **Retain per-competency match detail** for explainability (Q17)
  - ✅ Done when: ranked shortlist; each score expands to which competencies drove it; formula is the documented weighted sum

- [ ] **T8. Skill-gap per candidate (Deepseek Pro).** — *Depends: T7 · Flow: 4→8*
  - [ ] **Tahap 2 reuse (2026-07-12 audit):** `agent_4_recommendation_report.py::_build_seed_gap()`/`_is_skill_match()` implement a deterministic token-overlap "seed" that grounds/filters the LLM's gap output — adapt this technique (compute a cheap deterministic gap first, use it to constrain/validate the LLM's structured output) even though the underlying comparison there is candidate-vs-market, here it's candidate-vs-JD
  - [ ] Candidate profile vs JD competencies → structured gap output
  - [ ] Persist
  - ✅ Done when: each shortlisted candidate has a structured gap record

### AI Interview Module (the new component)
- [ ] **T9. Interview question generation (Flash).** — *Depends: T4 · Flow: 5*
  - [ ] From JD → **2-3 questions** in Bahasa Indonesia (e.g. "Jelaskan proses A dalam 1 menit")
  - [ ] Persist to `interview_questions` as status=`draft`
  - ✅ Done when: demo JD generates 2-3 sensible, relevant Indonesian questions in `draft`

- [ ] **T9b. Recruiter edit/approve questions (human-in-the-loop).** — *Depends: T9 · Flow: 5*
  - [ ] `GET/PUT /jobs/{id}/questions` — HR edits/adds/removes
  - [ ] `POST .../approve` flips status → `approved` + unlocks candidate invite
  - [ ] Candidate only ever sees approved questions
  - ✅ Done when: candidate can't start until HR approves; edited text is what the candidate sees

- [ ] **T9c. Invite candidate to interview (NEW — closes the gap between shortlist and interview).** — *Depends: T7, T9b · Flow: 4→5*
  - [ ] `POST /candidates/{id}/invite` — generates the unguessable `token` (+ `token_expires_at`) for that candidate, only callable once questions are `approved` (T9b)
  - [ ] Response/UI surfaces the copyable token link — **no auto-distribution** (resolved 2026-07-12: HR copies/shares it manually; for the demo, you play both HR and candidate)
  - ✅ Done when: HR can invite a shortlisted candidate; the resulting link opens that candidate's own consent+interview session and no other's

- [ ] **T10. Answer intake (AUDIO) + STT transcription.** — *Depends: T9c, Area4 T3b, DB T4, DB T8 · Flow: 5*
  - [ ] **Consent check (resolved 2026-07-12, explicit):** reject with 403 if no `consent_records` row exists for the candidate — the hard gate Area 5 QA T8 tests
  - [ ] `POST` accepts the candidate's audio file → store (DB T4)
  - [ ] Transcribe via Groq `whisper-large-v3`, `language=id` (Area4 T3b)
  - [ ] Persist transcript; recruiter can fetch raw audio + transcript
  - ✅ Done when: an Indonesian audio answer yields a stored file + correct transcript; a submission with no consent record is rejected

- [ ] **T11. Rubric scoring + answer summary (Pro, temp=0, FIXED schema).** — *Depends: T10 · Flow: 5→6*
  - [ ] **Rubric locked (resolved 2026-07-12) `[content]`**: 3 criteria — **clarity**, **relevance**, **technical depth** — each on a **1-5 scale** with an anchored description per level (e.g. 1=vague/off-topic … 5=clear/precise/correct); curate the exact wording per level (same curation category as the Area 3 competency framework)
  - [ ] Score the **transcript** per criterion at **temperature=0**
  - [ ] Produce an **AI summary of the answer's main points** for the recruiter
  - [ ] Persist to `rubric_scores` (one row per criterion, per `interview_answers` schema)
  - ✅ Done when: same transcript → identical score across runs (QA T3); recruiter gets a readable summary

- [ ] **T12. Human-in-the-loop endpoints — no auto-reject.** — *Depends: T11, DB T8 · Flow: 6→7*
  - [ ] HR reads AI score/summary
  - [ ] `POST /decisions` records the final outcome
  - [ ] **No code path finalizes a candidate without HR action** — enforce in code, not just UI
  - ✅ Done when: inspection shows no auto-finalize path; QA T6 passes

### Report & delivery
- [ ] **T13. Deterministic development report.** — *Depends: T12, T8, DB T6, DB T7 · Flow: 8*
  - [ ] **Gated on a decision existing (resolved 2026-07-12):** only generatable once `hr_decisions` has a row for the candidate — not just because skill-gap (T8) exists. Matches the actual flow (interview → decision → report) and reflects reality: only the 1 live (+2-3 synthetic) candidates have interview data to build a meaningful report from
  - [ ] From skill-gap (T8) + competency framework + resource library
  - [ ] Assemble by **selecting/ordering** curated items (no free generation)
  - [ ] Produce for **every decided** candidate (pass or fail — a decision either way triggers a report)
  - ✅ Done when: same skill-gap input → identical report (QA T4); report cites real curated resources; no report exists for a candidate with no `hr_decisions` row

- [ ] **T14. Report delivery — automated via Telegram (only channel).** — *Depends: T13, DB T8, Area4 T3c · Flow: 8*
  - [ ] **PDF library swapped to ReportLab (resolved 2026-07-12, Tahap 2 audit)**: ~~weasyprint~~ — Tahap 2's `agent_function/agent_4_recommendation_report.py::_build_report_pdf()` is a fully-working ~700-line ReportLab generator with custom flowables (including skill chips). Adapt it to our report schema (skill-gap + curated resource selections from Area 3 T6/T7) instead of building weasyprint from scratch — eliminates the Windows Pango/Cairo dependency risk entirely (ReportLab is pure Python) and reuses real, working rendering code + store for download in HR view
  - [ ] **Telegram:** using the candidate's linked `chat_id` (Area4 T3c), auto-send via `sendDocument` (the PDF) + `sendMessage` (summary)
  - [ ] HR triggers delivery with one click; no email, no manual copy/paste
  - ✅ Done when: HR clicks "send report" and the candidate (pass or fail) receives the file + summary via Telegram automatically

### Orchestration & contract
- [ ] **T15. Async wiring + error handling + caching.** — *Depends: T4–T14 · Flow: all*
  - [ ] FastAPI async orchestration across stages
  - [ ] Retries on LLM/STT calls
  - [ ] Caching via Area4 T3
  - [ ] **⚠️ Do NOT replicate Tahap 2's exception handler (2026-07-12 audit finding):** its global `@app.exception_handler(Exception)` returns raw Python tracebacks as JSON in 500 responses — a real security anti-pattern. Ours must return a generic error message, log the traceback server-side only
  - ✅ Done when: full pipeline runs end-to-end without manual step-poking; a forced 500 never leaks a stack trace to the client

- [ ] **T16. Publish OpenAPI contract for frontend.** — *Depends: T15 · Flow: integration*
  - [ ] Ensure endpoints are typed
  - [ ] Export `/openapi.json` for Area 1 wiring
  - ✅ Done when: frontend can generate/consume the contract

---

## Area 1 — Frontend UI/UX  ·  Status: ⚪ Not started

> **Money-shot screens only** (💎); drive the rest via seed data. Minimal design system.
> Resolved: **audio interview is CORE** + recruiter question edit/approve screen.

**Resolved 2026-07-12 (Area-1 session):**

| Aspect | Decision | Detail / rationale |
|---|---|---|
| ⚠️ Tahap 2 correction | **Tahap 2 has NO React frontend** — verified by reading the actual code | It's a static site (`index.html`/`style.css`/`script.js`, nginx, no build tooling), branded "SkillGap AI." Every prior doc saying "reuse Tahap 2 React" was wrong — there's no React code to reuse, only a visual language (colors, layout ideas) worth carrying over |
| Frontend stack | **Build fresh in React + Vite** | Needed anyway for the audio recorder, live shortlist re-rendering, and multi-step interview flow — awkward in vanilla JS. Matches what Area 2's OpenAPI contract (T16) already assumes |
| Invite UI (gap found) | **Modal on the Shortlist screen**, not a separate page | "Undang ke Interview" button per candidate row → modal shows the generated token link to copy (Area 2 T9c). New task **T5c** |
| Tier visibility (gap found) | **Shortlist visually distinguishes candidate status** | Status per candidate — *Belum diundang* / *Menunggu wawancara* / *Selesai wawancara* — derived from whether `interview_answers`/`hr_decisions` rows exist. Makes the demo narrative clear (why only 3 of 30 have full detail) instead of looking like a bug |
| Report delivery UI (gap found) | **Moved to T7** (HR candidate-detail page), removed from T8 | HR reviews everything and sends from one screen; T8 becomes purely the candidate-facing consent + Telegram-linking page |
| Visual direction | **"Enterprise Trust" — LOCKED (2026-07-12)** | Teal `#0f6b5c` + gold `#c98a2c`, Georgia serif headings, teal-tinted paper `#f4f7f6`, top-nav dossier layout. Chosen over the old Tahap 2 recreation, "Data Console," and "Human-first" directions |

**🎨 Design artifacts (two, kept separate):**
- [claude.ai/code/artifact/c3799402-5780-4573-a7e7-801149ffb90a](https://claude.ai/code/artifact/c3799402-5780-4573-a7e7-801149ffb90a) — full **8-page Enterprise Trust preview** (all pages from the Page List below, static/non-functional)
- [claude.ai/code/artifact/c0a5be48-4a7e-46fd-a68e-8ea757b48b0e](https://claude.ai/code/artifact/c0a5be48-4a7e-46fd-a68e-8ea757b48b0e) — the original **4-way comparison** (old Tahap 2 recreation vs. 3 new directions) that the decision came from, preserved as its own record

### Page List

| # | Page | Persona | What it shows | Backend endpoint(s) | DB tables touched |
|---|---|---|---|---|---|
| 1 | Login | HR | Email/password → HR home | `POST /auth/login` | `hr_users` |
| 2 | JD list + create/edit (T4b) | HR | CRUD on job descriptions, structured fields | `GET/POST/PUT/DELETE /jobs` | `jobs`, `jd_competencies` |
| 3 | HR Shortlist w/ explainability + tier status (T5) | HR | Ranked candidates, per-competency match detail, status pill | `GET /jobs/{id}/candidates` | `match_scores`, `jd_competencies`, `candidates`, `interview_answers`, `hr_decisions` |
| 4 | Invite modal (T5c) | HR | Generate + copy the candidate's token link | `POST /candidates/{id}/invite` | `candidates` |
| 5 | Question edit/approve (T5b) | HR | Edit AI-generated questions, approve | `GET/PUT /jobs/{id}/questions`, `POST .../approve` | `interview_questions` |
| 6 | Candidate consent + Telegram link (T8) | Candidate (token link) | PDP consent checkbox, "link Telegram" deep-link | consent write, `t.me/<bot>?start=<token>` | `consent_records`, `candidates.telegram_chat_id` |
| 7 | Candidate audio interview (T6) | Candidate (token link) | Question, record, playback, submit — loops 2-3x | `POST /candidates/{id}/answers` | `interview_answers`, `transcripts` |
| 8 | HR decision + candidate detail + report delivery (T7) | HR | CV, skill-gap, audio player, transcript, AI summary, rubric, decide, send report | `GET /candidates/{id}`, `POST /decisions`, `POST /candidates/{id}/send-report` | `parsed_profiles`, `rubric_scores`, `interview_summaries`, `hr_decisions` |

**Resolved 2026-07-12 (frontend UX gap-closing pass — detailed):**

| Concern | Decision |
|---|---|
| **Audio timer** | **Count-up, soft limit** — shows suggested duration as guidance, never auto-stops (no risk of cutting off on camera) |
| **Audio upload** | **Per-question** — record+submit each answer, uploads+transcribes in background before the next question; one failure retries just that answer |
| **Matching trigger** | **Pre-computed at seed + on candidate add**; Shortlist reads existing `match_scores` instantly — no loading, no "run" button |
| **Demo browser** | **Chrome/Edge** (full MediaRecorder + webm/opus); the audio component MUST be tested in the actual demo browser on Day 8 (frontend build start, re-baselined 2026-07-12) |
| **Loading states** | Skeleton loaders on lists; blocking spinner-with-label on the audio-submit step (longest wait, per question); buttons disable during their own call |
| **Error rendering** | One shared inline error component with a retry action across all AI/STT/upload/Telegram failures — never a raw error or silent no-op |
| **Token edge states** | One shared "link tidak valid / sudah kadaluarsa" screen (covers expired 72h token + malformed token); a route guard forces consent-before-interview |
| **Data freshness** | **Manual refresh** (no websockets/polling) — fine for a solo demo playing both roles sequentially; the demo script must account for it |
| **Empty states** | Simple messages for empty JD list (first login) and pre-match shortlist |
| **JD form validation** | Title + at least one of responsibilities/requirements required before extraction |
| **Non-goals (stated to prevent creep)** | Single theme (no in-app dark toggle) · desktop-only (mobile MediaRecorder out of scope) · Indonesian UI over English-sourced CV content (accepted cosmetic mismatch) |

**Audio recorder state machine (T6):** idle → requesting-permission → (granted / **denied** → blocking message) → recording (count-up timer) → stopped → playback → re-record | submit → uploading → transcribed → next question | completed. A denied mic and an empty/0-second submission each get an explicit blocking state + message.

### Task summary

| Task | Status | Summary |
|---|---|---|
| T1. Audit Tahap 2 frontend | **Final result** | Confirmed no React code exists to reuse — only the visual language, already captured in the design artifacts. |
| T2. Design system | **To do** | Port the locked "Enterprise Trust" visual direction into real React components. |
| T3. Vite structure + route guards | **To do** | Routing, typed API client, consent/token-expiry route guards. |
| T4. HR login | **To do** | Recruiter-only login; no candidate account exists. |
| T4b. JD CRUD UI | **To do** | Structured-field create/edit/delete/list for job descriptions. |
| T5. Shortlist | **To do** | Ranked candidates with per-competency explainability + tier status pills. |
| T5b. Question edit/approve UI | **To do** | HR edits/approves AI-generated interview questions. |
| T5c. Invite modal | **To do** | Copyable token-link modal, re-viewable after first generation. |
| T6. Candidate audio interview | **To do** | Full 8-state recorder machine — flagged as the single highest-risk component in the plan. |
| T7. HR decision + detail + delivery | **To do** | Audio player, transcript, rubric, decision action, report send. |
| T8. Candidate consent + Telegram linking | **To do** | PDP consent checkbox + Telegram deep-link capture. |
| T9. Cross-cutting UX | **To do** | Shared loading/error/empty states across all screens. |

- [ ] **T1. Audit Tahap 2 frontend — corrected scope.** — *Depends: none*
  - [ ] Confirmed: `../brainstorming result/tahap 2 code reference/frontend/` is static HTML/CSS/JS, **not React** — nothing to port as code
  - [ ] Extract the reusable **visual language only**: colors (`#102b4f` navy, `#4f46e5` indigo, teal/success/warning/danger tokens), Inter font, card/badge conventions — see the published design-comparison artifact for the faithful recreation
  - ✅ Done when: written verdict — zero code reuse, visual-language reuse only

- [ ] **T2. Minimal design system (React + Vite, built fresh) — Enterprise Trust LOCKED.** — *Depends: T1*
  - [ ] Direction confirmed 2026-07-12: **Enterprise Trust** — teal `#0f6b5c`, gold `#c98a2c`, Georgia serif headings, teal-tinted paper `#f4f7f6`, top-nav dossier layout. Reference: the 8-page artifact above (tokens/components already prototyped there — port the CSS approach into React)
  - [ ] Shared components: tables, cards, score badges, forms, status pills (T5 tier), **skeleton loader, inline error+retry, empty-state, spinner-with-label** (all used by T9)
  - ✅ Done when: shared components exist (not a full system), built in React matching the locked direction

- [ ] **T3. Vite structure + route guards.** — *Depends: none*
  - [ ] Routing + minimal state
  - [ ] API client generated/typed from OpenAPI (Area 2 T16)
  - [ ] **Route guards**: candidate interview route redirects to consent if no consent record; a shared "link tidak valid / sudah kadaluarsa" screen for expired (72h) or malformed tokens
  - ✅ Done when: app boots on host (Vite dev server); an expired/invalid token and a consent-skip both land on the right guard screen

- [ ] **T4. HR login screen (recruiter only).** — *Depends: Area2 T3*
  - [ ] Login for HR/recruiter → HR home
  - [ ] Candidate pages are **not** behind login — reached via token link (see T6/T8)
  - ✅ Done when: HR logs in; no candidate login exists

- [ ] **T4b. 💎 Job description CRUD (list + structured create/edit/delete).** — *Depends: Area2 T4 · Flow: 1*
  - [ ] JD list view, scoped to the logged-in HR's company
  - [ ] Create/edit form: **structured fields** — title, responsibilities, requirements, qualifications (separate inputs, not one free-text box) — easier for reliable competency extraction (Area 2 T4) and clearer guidance for HR
  - [ ] Delete action (MVP: simple, no cascade-guard)
  - ✅ Done when: HR can list, create, edit, and delete JDs from the UI using the structured form

- [ ] **T5. 💎 HR shortlist w/ explainability + tier status.** — *Depends: Area2 T7 · Flow: 4*
  - [ ] Ranked list + match score
  - [ ] Expand a score → which competencies matched (Q17)
  - [ ] **Status pill per candidate (resolved 2026-07-12)**: *Belum diundang* (no `candidates.token` yet) / *Menunggu wawancara* (invited, no `interview_answers` yet) / *Selesai wawancara* (has `rubric_scores`/`hr_decisions`) — derived from row presence, not a stored field
  - [ ] "Undang ke Interview" button per row (opens T5c modal)
  - [ ] **Instant read (resolved 2026-07-12)**: reads pre-computed `match_scores` (seeded + computed on candidate-add) — no live matching call, no loading spinner, no "run ranking" button. Empty state if a JD has no matched candidates yet
  - ✅ Done when: a viewer can see *why* a candidate ranks AND which stage each of the 30 is at; the ranked list appears instantly with no wait

- [ ] **T5b. 💎 Recruiter question edit/approve.** — *Depends: Area2 T9b · Flow: 5*
  - [ ] View AI-generated questions; edit/add/remove
  - [ ] Approve → unlocks candidate invite
  - ✅ Done when: HR approves before any candidate can start

- [ ] **T5c. 💎 Invite candidate modal (NEW — closes the Area 2 T9c UI gap).** — *Depends: Area2 T9c, T5 · Flow: 4→5*
  - [ ] Modal opened from the Shortlist row action: calls `POST /candidates/{id}/invite`, only enabled once questions are approved (T5b)
  - [ ] Shows the generated token link as copyable text — no auto-send, HR copies it manually (matches Area 2 T9c's "no auto-distribution" decision)
  - [ ] **Re-viewable (resolved 2026-07-12)**: once a candidate has a `token`, the Shortlist row button changes from "Undang ke Interview" to "Lihat Link Undangan" — reopening the modal shows the existing link rather than erroring or silently regenerating it. Protects the live demo from losing the link mid-recording
  - ✅ Done when: HR can invite a candidate and copy their link without leaving the Shortlist screen; reopening the modal later still shows the same link

- [ ] **T6. 💎 Candidate AUDIO interview (token link, no login) — highest-risk component.** — *Depends: Area2 T9b/T10 · Flow: 5*
  - [ ] **Test the recorder in Chrome/Edge FIRST** (Day 8, frontend build start, re-baselined 2026-07-12) — MediaRecorder + webm/opus compatibility is a demo-killer if left late; T6 itself is dedicated **Day 10** given its ~5.5h estimate
  - [ ] **Mic permission flow**: request → granted → recording; **denied/blocked → explicit blocking message** ("Izinkan akses mikrofon untuk melanjutkan"), never silent dead-air
  - [ ] Open via token link → show approved question + **count-up timer** with the suggested duration shown as guidance (no auto-stop)
  - [ ] Record (MediaRecorder → webm/opus), stop, **playback, re-record**
  - [ ] **Block empty/0-second submission** with a message
  - [ ] **Per-question upload (resolved 2026-07-12)**: submit each answer → uploads + transcribes in background (spinner-with-label) → advance to next question; a failed upload retries only that answer
  - [ ] Loops for the 2-3 questions, then a completion screen
  - [ ] **Completion guard**: on load, if `interview_answers` already exist for this candidate, show "Wawancara sudah selesai, terima kasih" instead of the recorder — blocks accidental re-record/overwrite on reload
  - ✅ Done when: candidate opens the link, records + submits each voice answer end-to-end in Chrome/Edge with no account; denied mic, empty submit, and post-completion reload each show their correct state, not a crash or the raw recorder

- [ ] **T7. 💎 HR decision + candidate detail + report delivery.** — *Depends: Area2 T8/T10/T11/T12/T13/T14 · Flow: 6-7,8*
  - [ ] Parsed CV + skill-gap
  - [ ] Raw **audio player** + transcript + AI summary + rubric score
  - [ ] Advance/reject action; UI makes clear AI only *recommends*
  - [ ] **Report delivery (moved here 2026-07-12, was in T8)**: once a decision exists (Area 2 T13 gate), "Kirim Laporan" button → view/download PDF + one-click send via Telegram (Area 2 T14)
  - [ ] **Missing-Telegram state (resolved 2026-07-12)**: if `candidates.telegram_chat_id` is null, the send button shows disabled with "Kandidat belum menautkan Telegram" rather than an active button that would fail on click. For the 2-3 synthetic candidates (seeded with a decision already, see Area 3 T10) the button instead shows a disabled **"Terkirim"** (already-sent) state — they demo as fully-processed examples, not re-triggerable
  - [ ] **Send loading + error state**: "Kirim Laporan" shows a generating/sending spinner (PDF + Telegram can take a few seconds) and a retry on failure
  - ✅ Done when: HR can replay audio, read transcript+summary, record a decision, then send the report — all from this one screen; no click ever produces a failed/broken Telegram send on camera

- [ ] **T9. Cross-cutting UX: loading, errors, empty states, refresh.** — *Depends: T2 · Flow: all*
  - [ ] Shared inline **error component** with retry, used on every AI/STT/upload/Telegram call site
  - [ ] **Loading** treatments: skeleton loaders on lists (JD list, shortlist), spinner-with-label on long AI waits (JD extraction, audio submit, report send), disable buttons during their call
  - [ ] **Empty states**: empty JD list (first login), pre-match shortlist
  - [ ] **JD form validation**: title + ≥1 of responsibilities/requirements required
  - [ ] **Data freshness**: manual refresh model documented in the demo script (no realtime); state it, don't build polling
  - [ ] **Non-goals honored**: single theme, desktop-only, no mobile recorder path
  - ✅ Done when: no screen shows a raw error, infinite spinner, or blank-with-no-explanation during the demo happy path

- [ ] **T8. 💎 Candidate consent (token link) — Telegram linking only.** — *Depends: Area2 T5, DB T8 · Flow: 5*
  - [ ] Candidate token page: consent checkbox (gates interview, PDP) — **no self-service CV upload for MVP** (resolved 2026-07-12: the 30 demo candidates are HR/seed-imported since their CVs come from Kaggle already; a public self-apply upload flow is out of scope this week, see Area 2 T5 note)
  - [ ] Candidate token page: "Get your result on Telegram" button → deep-links to `t.me/<bot>?start=<token>` (Area4 T3c) — **required** step, this is the only delivery channel
  - ✅ Done when: consent recorded; candidate links Telegram before starting the interview. **Report sending now lives on T7, not here** (resolved 2026-07-12)

- [ ] `[deferred]` **Full HR dashboard shell / nav polish beyond the JD list (T4b)** — minimal nav only.
- [ ] `[deferred]` **Responsive/usability polish beyond demo happy-path.**

---

## Area 5 — QA  ·  Status: ⚪ Not started

> Collapsed to the highest-stakes claim tests (💎) + one e2e. Broad coverage + security matrix deferred.
> ⚠️ **Rewritten 2026-07-12** — the previous version predated most of the Area 1-4 gap-closing passes
> (invite step, PII redaction, consent-gate, Telegram delivery, tiered candidates, frontend edge
> states) and referenced a flow that no longer exists (e.g. "report email"). This version matches
> the actual current product.

**Resolved 2026-07-12 (Area-5 session):**

| Gap found | Decision |
|---|---|
| PII redaction untested | **Promoted to required claim test — new T3b** |
| Area 2 T10 cites a consent test that didn't really exist as written | **T8 promoted from deferred/smoke to a required automated test** |
| Demo-safety UX states never verified before recording | **T12 now explicitly walks through all of them, not just the happy path** |
| Matching formula / curated tiers only "light manual check" | **Promoted to an asserted check — T5 upgraded** |
| All claim tests scheduled for Day 6 despite depending on Day 2-4 work | **Shifted left — each runs as soon as its dependency lands; Day 6 becomes a re-run/confirmation pass** |
| T5's test had no data to assert against (seed script didn't record intended tiers) | **Seed script (Area 3 T10) now tags each candidate's intended tier** |
| Telegram delivery only checked for "didn't error," not "actually arrived" | **T12 rehearsal now includes checking the real Telegram chat** |
| "5 repeated runs" would trivially pass via Area 4's response cache — calls 2-5 never re-query the LLM, so the test would prove nothing | **Determinism tests (T3/T4) now bypass the cache** for their own runs |
| T3b's fixture (reusing a curated seed CV) created a same-day dependency on Area 3's full 30-CV curation finishing | **T3b now uses its own dedicated minimal test fixture**, decoupled from curation |
| T5's strict per-candidate ordering risked false failures on real, messy CV data | **Changed to an aggregate/average tier comparison** |
| Shifting tests left only helps if a failure actually blocks progress | **New rule: a failing 💎 test must be fixed the same day, before starting the next day's tasks** |
| T3b's PII assertion didn't say whether it hits the real SumoPod API or mocks it | **Mock the outgoing request** — patch the LLM client, no live call, zero cost |
| T4's "identical report" comparison could false-fail on PDF metadata (creation timestamp etc.) if it diffed rendered bytes | **Compare the underlying report data, before PDF rendering — not the PDF bytes** |
| T3/T4's cache-bypassed tests have a real recurring API cost with no guardrail against careless repeat runs | **Explicit note: run once per feature, not in a tight edit-test loop** |

**Failure gate (resolved 2026-07-12):** if any 💎 claim test (T3, T3b, T4, T5, T6, T8) fails on the day it's run, fix it before starting the next day's build tasks. This is the entire point of shifting them left — a noted-but-deferred failure defeats the purpose.

**Cost guardrail (resolved 2026-07-12):** T3 and T4 each make 5 genuinely independent, cache-bypassed Deepseek calls per run. Cheap individually, but run them **once when the feature is believed complete** — not repeatedly inside an edit-test-edit debugging loop. This is exactly the repeated-spend pattern Area 4's whole caching strategy exists to avoid.

### Task summary

| Task | Status | Summary |
|---|---|---|
| T3. Determinism test | **To do** | 5 cache-bypassed rubric-scoring runs must agree exactly. |
| T3b. PII redaction test | **To do** | Mocked-request assertion that no raw PII reaches the LLM payload or the DB. |
| T4. Report consistency test | **To do** | 5 cache-bypassed runs must produce identical report data (not PDF bytes). |
| T5. Matching/tier check | **To do** | Strong-tier average score must meaningfully beat weak-tier average. |
| T6. Human-in-loop test | **To do** | Confirms no code path can finalize a candidate without HR action. |
| T8. Consent-gate test | **To do** | 403 without consent, success with a valid consent record. |
| T10. Full e2e run | **To do** | Scripted happy-path walkthrough of the entire flow, seed to Telegram delivery. |
| T12. Demo-readiness checklist | **To do** | Rehearsal covering every frontend edge state + a real Telegram delivery check. |

- [ ] **T3. 💎 Determinism test.** — *Depends: Area2 T11 · **Run: Day 6** (re-baselined 2026-07-12), as soon as rubric scoring exists*
  - [ ] Same **transcript** → same rubric score across **5 repeated runs, cache BYPASSED** for these calls (a determinism test that hits the Area 4 T3 cache after run 1 would just replay the same response and prove nothing about the LLM). Run once per feature, not in a tight debug loop (see cost guardrail above)
  - ✅ Done when: all 5 genuinely independent calls give identical scores (if not, the transparency claim is false — fix before moving on)

- [ ] **T3b. 💎 PII redaction test (NEW — closes a real gap).** — *Depends: Area2 T5 · **Run: Day 4-5** (re-baselined 2026-07-12), right after CV parsing is built*
  - [ ] Feed a CV containing a real name/email/phone through the parse pipeline — **use one dedicated, standalone test fixture PDF** (a small throwaway document with a known fake name/email/phone), NOT one of the 30 curated seed CVs — decouples this test from Area 3 T10's curation finishing, so it can run the moment CV parsing exists
  - [ ] **Mock the outgoing SumoPod request (resolved 2026-07-12)** — patch the LLM client to capture the payload it would send, no live API call; zero cost, no network dependency, still proves redaction happens before the payload is constructed
  - [ ] Assert the captured/mocked payload never contains the raw name/email/phone — only the alias
  - [ ] Assert `parsed_profiles` (structured DB row) contains only the alias, never the raw PII
  - ✅ Done when: both assertions pass — proves the UU PDP claim ("only skill-relevant info reaches the LLM") rather than just asserting it

- [ ] **T4. 💎 Report consistency test.** — *Depends: Area2 T13 · **Run: Day 7** (re-baselined 2026-07-12), as soon as report generation exists*
  - [ ] Same skill-gap input → same development report across **5 repeated runs, cache BYPASSED** for these calls (same reasoning as T3). Run once per feature, not in a tight debug loop
  - [ ] **Compare the underlying report data, not rendered PDF bytes (resolved 2026-07-12)** — diff the structured content fed into the `weasyprint` template across the 5 runs; comparing raw PDF bytes risks a false failure from non-deterministic metadata (creation timestamp, producer string) that weasyprint embeds even when visible content is identical
  - ✅ Done when: all 5 genuinely independent runs produce identical report **data** (PDF rendering itself is not the thing being asserted)

- [ ] **T5. Matching formula / curated-tier check (promoted from manual-only).** — *Depends: Area2 T7, DB T10 · **Run: Day 5** (re-baselined 2026-07-12), right after matching is built*
  - [ ] Read the **intended tier per candidate from the seed manifest** (Area 3 T10 now tags strong/mid/weak per candidate at curation time — not re-derived here)
  - [ ] **Aggregate comparison (resolved 2026-07-12)**: assert the strong-tier **average** score is meaningfully higher than the weak-tier **average** — not a strict per-candidate ordering, which would be brittle against natural noise in real, manually-curated CV data
  - ✅ Done when: the average-score gap confirms the ranking visibly discriminates — catches a formula bug or bad curation before it's on camera, without false alarms from one ambiguous real-world CV

- [ ] **T6. 💎 Human-in-the-loop test.** — *Depends: Area2 T12 · **Run: Day 6** (re-baselined 2026-07-12), as soon as decision endpoints exist*
  - [ ] Confirm no code path finalizes a candidate without HR action
  - ✅ Done when: no auto-finalize path exists (validates "assist, never decide")

- [ ] **T8. 💎 Consent-gate enforcement test (promoted from deferred/smoke).** — *Depends: Area2 T10 · **Run: Day 6** (re-baselined 2026-07-12), as soon as answer intake exists*
  - [ ] Submit an interview answer for a candidate with no `consent_records` row → assert 403
  - [ ] Submit after a valid consent record exists → assert success
  - ✅ Done when: both cases behave correctly — this is the exact test Area 2 T10 already assumes exists

- [ ] **T10. Full e2e happy-path run — rewritten to match the current flow.** — *Depends: all core · **Run: Day 12** (re-baselined 2026-07-12; this one genuinely needs everything built; T3/T3b/T4/T5/T6/T8 above are re-run here as a confirmation pass, not run for the first time)*
  - [ ] Seed data loads: 1 company, 1 JD (Data Analyst), **30 candidates correctly tiered** (27 profile-only, 2-3 synthetic-interview, 1 live) — verify all 30 have `parsed_profiles` (catches a silent partial-parse failure)
  - [ ] HR: create/view JD (structured fields) → view Shortlist (instant, pre-computed scores + tier status pills)
  - [ ] HR: edit/approve interview questions (T5b) → **invite the live candidate (T5c/T9c)**, copy the token link
  - [ ] Candidate: open token link → consent + **link Telegram** → record + submit **each** audio answer (per-question upload) → completion screen
  - [ ] HR: review candidate detail (audio player + transcript + AI summary + rubric) → record decision → **send report via Telegram** (real send, not email)
  - [ ] Spot-check the 2-3 synthetic candidates show their pre-seeded "Terkirim" state correctly, and a profile-only candidate shows "Belum Diundang"
  - ✅ Done when: one clean pass with no manual DB fiddling, matching the actual current flow end to end

- [ ] **T12. Demo-readiness checklist — now includes the edge-state walkthrough (promoted from happy-path-only).** — *Depends: T10*
  - [ ] Happy-path script written and rehearsed
  - [ ] **Edge/safety states walked through at least once before the real recording**: mic-permission denied, empty/0-second audio submit blocked, interview completion-guard (reopen link after submitting), expired/invalid token screen, invite-modal re-view ("Lihat Link Undangan"), missing-Telegram disabled send button, synthetic-candidate disabled "Terkirim" state
  - [ ] **Telegram delivery verified for real (NEW)**: after clicking "Kirim Laporan" for the live candidate, actually check the Telegram chat and confirm the PDF + summary arrived — not just that the API call returned success
  - [ ] Seed loaded, latency acceptable, no crashes on the demo flow
  - ✅ Done when: a rehearsed run is recorded AND every edge state above has been seen at least once, AND a real Telegram message has been confirmed received

- [ ] `[deferred]` **Broad unit + integration coverage** — only claim-critical stages tested.
- [ ] `[deferred]` **Access-control matrix** — thin auth smoke check only (Area2 T3); consent-gate (T8 above) is now the one promoted exception.
- [ ] `[deferred]` **Audit-log completeness full test** — spot check only.
- [ ] `[deferred]` **Vision-LLM fallback dedicated test** — covered once via Area 4 T3d's Day-1 verification, not re-tested here.
- [ ] `[deferred]` **JD soft-delete integrity test** — trust the `status='closed'` design (Area 2 T4); no dedicated test this week.

---

## Effort & Difficulty Estimates (2026-07-12 full-plan review; revised same day after the Tahap 2 backend code audit)

Per-task estimate at the same granularity as the checklist (T1, T2, ...), not sub-steps. Difficulty:
🟢 Low · 🟡 Medium · 🟠 High · 🔴 Very High (risk of blowing the schedule if it goes wrong).

**⚠️ Revision note (2026-07-12, Tahap 2 backend audit):** the original pass assumed "reuse Tahap 2
backend" without actually reading the code. A full audit found most of what was assumed reusable is
**absent** (no auth, no DB/ORM, no vector DB, no Deepseek — it's Google Gemini) — see the corrected
`CLAUDE.md` § Existing Code To Reuse. But it also found **real, working code in three places** that
genuinely reduces estimates below, plus one strategic swap (weasyprint → ReportLab for Area 2 T14,
resolved this session). Adjusted lines are marked **↓ (Tahap 2 reuse)**.

### Area 4 — Cost / Tooling (Day 1)

| Task | Status | Est. hours | Difficulty | Note |
|---|---|---|---|---|
| T1 Lock stack + versions | 🟢 Done 2026-07-13 | 1.0 | 🟢 | Boilerplate |
| T2 Docker Compose + run modes | 🟢 Dev mode done 2026-07-13 (finalization mode deferred) | 2.0 | 🟢 | Standard Compose work; Tahap 2's compose has no DB services, minimal reference value. Hit + fixed a real port-5432 collision with a pre-existing native Postgres service |
| T3 LLM client + caching + bypass | 🟢 Done 2026-07-13 | 2.5 | 🟡 | Cache-key design + new bypass param — Tahap 2 uses Gemini/LangChain, zero code transfers |
| T3b STT client (Groq) | 🟢 Done 2026-07-13 | 1.0 | 🟢 | Thin wrapper — no Tahap 2 equivalent (no STT anywhere in that repo) |
| T3c Telegram bot client | 🟢 Done 2026-07-13 | 2.0 | 🟡 | Deep-link + chat_id capture logic — no Tahap 2 equivalent |
| T3d Vision-LLM client + fallback | 🟢 Done 2026-07-13 | **2.0** ↓ *(was 2.5)* | 🟠 | **Tahap 2 reuse**: its Gemini-vision OCR fallback (`_ocr_pdf_with_gemini`, PyMuPDF rasterize→vision call) is a working, validated version of this exact pattern — reduces implementation risk even though the provider (SumoPod/Groq vs Gemini) and technique (per-image vs whole-page) differ |
| T8 Cost estimate | 🟢 Done 2026-07-13 (projected; re-verify against real logs post-seed) | 0.5 | 🟢 | Arithmetic + a paragraph |
| **Subtotal** | | **~11.0h** *(was 11.5h)* | | vs. **8h** scheduled (Day 1) |

### Area 3 — Database + Datasets (Day 2-3)

| Task | Status | Est. hours | Difficulty | Note |
|---|---|---|---|---|
| T1 DB connection | ⚪ Not started | 0.5 | 🟢 | Tahap 2 has **zero** DB/ORM code — fully from scratch |
| T2 Schema (17 tables) | ⚪ Not started | 2.0 | 🟡 | Many tables, mechanically straightforward; no models to reference |
| T3 Qdrant collections | ⚪ Not started | 1.0 | 🟢 | No vector DB in Tahap 2 |
| T4 File storage layout | ⚪ Not started | 1.0 | 🟢 | Tahap 2 only has a temp-file + in-memory dict, no structured layout to borrow |
| T5 Repository layer | ⚪ Not started | 1.5 | 🟡 | |
| T6 Competency framework `[content]` | ⚪ Not started | 2.0 | 🟡 | Domain judgment, not code |
| T7 Resource library `[content]` | ⚪ Not started | 1.5 | 🟡 | Domain judgment |
| T8 Consent + audit write paths | ⚪ Not started | 1.5 | 🟡 | No Tahap 2 equivalent |
| T9 Retention policy | ⚪ Not started | 0.5 | 🟢 | |
| T10 Seed data (Kaggle curate 30 + tier tag + anonymize + 2-3 synthetic audio + decisions) | ⚪ Not started | **4.5** | 🟠 | **The real time sink** — manual curation labor across 30 real CVs, not code complexity |
| **Subtotal** | | **~16h** | | vs. **16h** scheduled (Day 2-3) — tight but plausible IF T10 doesn't overrun |

### Area 2 — Backend & AI (Day 4-7)

| Task | Status | Est. hours | Difficulty | Note |
|---|---|---|---|---|
| T1 Audit Tahap 2 backend | 🟢 Done 2026-07-12 | **0.25** ↓ *(was 1.0)* | 🟢 | **Effectively done** — this session's deep audit (10-point code inventory) already produced the "keep/rebuild/drop" verdict this task asks for; remaining work is just formalizing it |
| T2 Project structure | ⚪ Not started | 1.0 | 🟢 | Tahap 2's structure is a LangGraph agent pipeline, not our routers/services pattern — not directly reusable |
| T3 Auth (JWT + token link) | ⚪ Not started | 2.0 | 🟡 | **Confirmed** (not just "verify"): Tahap 2 has zero auth code — fully from scratch |
| T4 JD full CRUD + extraction + soft-delete | ⚪ Not started | 3.0 | 🟡 | No JD/employer concept exists in Tahap 2 (jobseeker-focused app) |
| T5 CV parse (text + vision fallback + PII redaction) | ⚪ Not started | **3.75** ↓ *(was 5.0)* | 🔴 | **Tahap 2 reuse**: the `pdfplumber` text-extraction + empty-page-detection pattern is validated working code — adopt it directly for the text-extraction step. Still 🔴: PII redaction, SumoPod integration, and proper (non-regex) structured-output validation are all new work Tahap 2 doesn't have (its own JSON parsing is explicitly fragile — a pattern to avoid, not copy) |
| T6 Embeddings → Qdrant | ⚪ Not started (embeddings API access verified 2026-07-13) | 1.5 | 🟡 | No embeddings code in Tahap 2 |
| T7 Matching engine (semantic + graph + formula) | ⚪ Not started | 3.0 | 🟠 | Tahap 2's "matching" is a token-overlap heuristic — a different technique entirely, doesn't transfer to our semantic+graph approach |
| T8 Skill-gap analysis | ⚪ Not started | **1.0** ↓ *(was 1.5)* | 🟡 | **Tahap 2 reuse**: `_build_seed_gap()`/`_is_skill_match()`'s deterministic-seed-grounds-LLM-output pattern is a legitimate technique to adapt here, even though it's candidate-vs-market there and candidate-vs-JD here |
| T9 Interview question gen | ⚪ Not started | 1.0 | 🟡 | No interview module in Tahap 2 (the whole "new component" premise from the original pivot) |
| T9b Recruiter edit/approve | ⚪ Not started | 1.0 | 🟢 | |
| T9c Invite candidate | ⚪ Not started | 1.0 | 🟢 | |
| T10 Answer intake + STT + consent check | ⚪ Not started | 2.0 | 🟡 | No STT in Tahap 2 |
| T11 Rubric scoring + summary (+ rubric content) | ⚪ Not started | 2.5 | 🟡 | No rubric/interview scoring in Tahap 2 |
| T12 HR decision endpoints | ⚪ Not started | 1.0 | 🟢 | No employer-decision flow in Tahap 2 |
| T13 Report generation (gated, deterministic) | ⚪ Not started | 2.5 | 🟡 | Tahap 2's report content is LLM-free-generated (by design, ours is deterministic-selection) — different approach, no code reuse, only content-shape learning |
| T14 Report delivery — **PDF library swapped to ReportLab** (resolved 2026-07-12) | ⚪ Not started | **2.0** ↓ *(was 3.0, weasyprint)* | 🟡 *(was 🟠)* | **Tahap 2 reuse, biggest single win**: `_build_report_pdf()` is a fully-working ~700-line ReportLab generator with custom flowables for skill chips. Adapting it to our schema retires both the hardest part of this task AND the weasyprint Windows Pango/Cairo dependency risk (ReportLab is pure Python, no system libs) |
| T15 Async wiring + error handling + caching | ⚪ Not started | **1.75** ↓ *(was 2.0)* | 🟡 | Tahap 2's in-memory async-job/polling pattern (`threading.Lock` + background thread) is a minor reference; **do not copy its exception handler** — it leaks raw Python tracebacks in 500 responses |
| T16 OpenAPI contract | ⚪ Not started | 0.5 | 🟢 | FastAPI-generated regardless |
| **Subtotal** | | **~29.75h** *(was 33.5h)* | | vs. **32h** scheduled (Day 4-7, 4 days × 8h) — now roughly fits |

### Area 1 — Frontend UI/UX (Day 8-11)

No changes from the Tahap 2 backend audit (Area 1 was already corrected in its own session — no
React code exists to reuse, only visual language, already captured in T1/T2 below).

| Task | Status | Est. hours | Difficulty | Note |
|---|---|---|---|---|
| T1 Audit (corrected scope) | 🟢 Done 2026-07-12 | 0.5 | 🟢 | |
| T2 Design system (port Enterprise Trust to React) | ⚪ Not started (design locked/previewed 2026-07-12, not yet built in code) | 3.0 | 🟡 | |
| T3 Vite structure + route guards | 🟡 In progress — Vite scaffold done 2026-07-13, route guards not started | 1.5 | 🟡 | |
| T4 HR login | ⚪ Not started | 1.0 | 🟢 | |
| T4b JD CRUD UI | ⚪ Not started | 2.5 | 🟡 | |
| T5 Shortlist (explainability + tier status + instant read) | ⚪ Not started | 3.0 | 🟡 | |
| T5b Question edit/approve UI | ⚪ Not started | 1.5 | 🟡 | |
| T5c Invite modal (re-viewable) | ⚪ Not started | 1.0 | 🟡 | |
| T6 Candidate AUDIO interview | ⚪ Not started | **5.5** | 🔴 | **Flagged highest-risk in the plan itself** — 8-state machine, browser permission handling, per-question upload |
| T7 HR decision + detail + report delivery | ⚪ Not started | **4.0** | 🟠 | Audio player, transcript, rubric display, 2 disabled-state variants, send-error handling |
| T8 Candidate consent + Telegram linking | ⚪ Not started | 1.5 | 🟡 | |
| T9 Cross-cutting UX (loading/error/empty/refresh) | ⚪ Not started | 2.5 | 🟡 | Touches every screen |
| **Subtotal** | | **~28h** | | vs. **32h** scheduled (Day 8-11, 4 days × 8h) — now fits with room to spare |

### Area 5 — QA (Day 4-12, shifted left)

No changes from the Tahap 2 backend audit (Tahap 2 has no test suite to reference).

| Task | Status | Est. hours | Difficulty | Note |
|---|---|---|---|---|
| T3 Determinism test | ⚪ Not started | 1.5 | 🟡 | |
| T3b PII redaction test (mocked) | ⚪ Not started | 2.0 | 🟡 | Mock setup adds time |
| T4 Report consistency test | ⚪ Not started | 1.5 | 🟡 | |
| T5 Matching/tier check | ⚪ Not started | 1.0 | 🟢 | |
| T6 Human-in-loop test | ⚪ Not started | 1.0 | 🟢 | |
| T8 Consent-gate test | ⚪ Not started | 1.0 | 🟢 | |
| T10 Full e2e run | ⚪ Not started | 2.0 | 🟡 | Manual scripted walkthrough |
| T12 Demo-readiness checklist | ⚪ Not started | 2.5 | 🟡 | Rehearsal + edge states + Telegram check |
| **Subtotal** | | **~12.5h** | | Spread across Day 4-12 alongside build work — same person, same hours pool |

### Revised headline: totals after the Tahap 2 reuse audit

| | Estimated (revised) | Estimated (original 2026-07-12) | Scheduled (13-day map) |
|---|---|---|---|
| Area 4 | 11.0h | 11.5h | 8h (Day 1) |
| Area 3 | 16.0h | 16.0h | 16h (Day 2-3) |
| Area 2 | **29.75h** | 33.5h | 32h (Day 4-7) — now fits |
| Area 1 | 28.0h | 28.0h | 32h (Day 8-11) — fits with room |
| Area 5 | 12.5h | 12.5h | *(overlaps build days)* |
| **Total build** | **~97.25h** | 101.5h | **~104h** (Day 1-13 @ 8h/day incl. buffer, or ~96h across Day 1-12 excl. buffer) |

The Tahap 2 reuse audit saved **~4.25 hours** (mostly Area 2: CV-parse text extraction, skill-gap
grounding pattern, and the ReportLab swap). Not enough to shrink the 13-day re-baseline, but it
meaningfully **de-risks** Area 2 (now fits its scheduled 4 days instead of running ~40% over) and
**removes the weasyprint Windows dependency risk entirely**. The 13-day / D1-D13 schedule from the
prior re-baseline stands as the working plan.

This isn't a small rounding error — it's the cumulative effect of every gap-closing session in this
plan adding real scope (T9c, T3b, T3d, T5c, T9, tier tracking, synthetic-candidate decisions, the full
audio state machine, etc.), none of which existed in the original day-map's task counts. The **audio
recorder (Area 1 T6) alone is bigger than the entire day currently budgeted for all of Area 1.**

## Next Step

Walk this file **one area at a time** in critical-path order (Area 4 → 3 → 2 → 1 → 5). Confirm each
area's flow matches the target before code. Flip the `Status:` line and tick sub-boxes as the build proceeds.
