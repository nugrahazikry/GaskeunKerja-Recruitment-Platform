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
| 4. Cost / Tooling (dev env) | 🟢 Done (T1-T3d, T8 all done; T4 deferred) | 7 | 1 | Day 1 |
| 3. Database + datasets | 🟢 Done (all 10 tasks T1-T10 verified end-to-end) | 9 | 0 | Day 2–3 |
| 2. Backend & AI | 🟢 Done (all 16 tasks T1-T16 verified end-to-end) | 16 | 0 | Day 4–7 |
| 1. Frontend UI/UX | 🟢 Done (all 13 tasks T1-T9 verified end-to-end) | 13 | 0 | Day 8–11 |
| 5. QA | 🟡 In progress (7/9 tasks done, both prior findings fixed same day; T10/T12 paused at the real-Telegram checkpoint, T11 held — all 3 resume together with the user) | 9 | 5 | Day 4-12 (shifted left, spans build; final pass Day 12 — see banner) |

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

## Area 4 — Cost / Tooling (Dev Environment)  ·  Status: 🟢 Done (T1-T3d, T8 all verified; T4 deferred)

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

| Task | Status | Summary | Est. hours | Difficulty | Note |
|---|---|---|---|---|---|
| T1. Stack + versions | ✅ **Final result** | `backend/`+`frontend/` scaffolded, deps installed clean (frontend via Vite, backend via venv), `uvicorn`/`npm run dev` both verified booting. | 1.0 | 🟢 | Boilerplate |
| T2. Docker Compose + run modes | ✅ **Final result** | Postgres 16 + Qdrant containers healthy; found and fixed a real port-5432 collision with a pre-existing native Postgres (remapped to 5433). Finalization mode intentionally deferred. | 2.0 | 🟢 | Standard Compose work; Tahap 2's compose has no DB services, minimal reference value |
| T3. Unified LLM client + caching | ✅ **Final result** | `llm_client.py` built and verified: cache miss/hit/bypass all behave correctly, token usage logged. | 2.5 | 🟡 | Cache-key design + new bypass param — Tahap 2 uses Gemini/LangChain, zero code transfers |
| T3b. STT client (Groq) | ✅ **Final result** | `stt_client.py` verified against two real Indonesian audio clips — both transcribed accurately. | 1.0 | 🟢 | Thin wrapper — no Tahap 2 equivalent (no STT anywhere in that repo) |
| T3c. Telegram bot client | ✅ **Final result** | `telegram_client.py` verified fully live — deep-link chat_id capture, message send, and document send all confirmed received. | 2.0 | 🟡 | Deep-link + chat_id capture logic — no Tahap 2 equivalent |
| T3d. Vision-LLM client | ✅ **Final result** | `vision_client.py` verified — SumoPod vision confirmed non-functional, Groq's Llama 4 Scout confirmed working for both transcribe and describe modes. | **2.0** ↓ *(was 2.5)* | 🟠 | **Tahap 2 reuse**: its Gemini-vision OCR fallback (`_ocr_pdf_with_gemini`) is a working, validated version of this exact pattern |
| T8. Cost estimate | ✅ **Final result** | Projected ≈$0.07/demo run, ≈$0.20 with dev re-runs, from real observed token counts + published rates. Flagged to re-verify against real logs once seed data exists. | 0.5 | 🟢 | Arithmetic + a paragraph |
| T4. Local-LLM substitution | 📝 **To do** *(deferred)* | Cut from scope — negligible savings for real solo build hours. | — | — | — |
| **Subtotal** | | | **~11.0h** *(was 11.5h)* | | vs. **8h** scheduled (Day 1) |

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

## Area 3 — Database + Reference Datasets  ·  Status: 🟢 Done (all 10 tasks T1-T10 verified end-to-end)

> **Blocks Area 2.** Schema early; datasets are `[content]` and gate the report (Area 2 T13) — start Day 2, don't slip.
> Resolved: **PostgreSQL in Docker, via SQLAlchemy, NO Alembic** (`create_all` on fresh demo DB).

**Resolved 2026-07-12 (Area-3 session):**

| Aspect | Decision | Detail / rationale |
|---|---|---|
| Demo role | ~~Data Analyst~~ → **Web Developer** (changed 2026-07-13) | JD (`backend/seed/job_description_data.py`), competency framework (T6), resource library (T7) all re-targeted to this title |
| CV source | **30 PDFs added by user to `seed/raw/cv/`** (changed 2026-07-13) | **⚠️ Confirmed random, NOT curated/tiered** — user's words: "for testing purposes only." Not verified to be IT/web-dev-relevant, not filtered by category |
| Candidate count | **30, random (not curated)** (changed 2026-07-13) | Original plan called for a deliberate strong/mid/weak spread; user explicitly chose to skip this and use the random batch as-is. **Risk**: the ranked shortlist may not visibly discriminate on camera the way the original plan intended — revisit before the demo recording if this matters |
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
| `competency_framework` | `[content]` Skill taxonomy for the demo role (Web Developer), with lightweight relations |
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
| `competency_framework` | `job_role` | `"Web Developer"` (the one demo role, changed 2026-07-13 from Data Analyst) |
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

| Task | Status | Summary | Est. hours | Difficulty | Note |
|---|---|---|---|---|---|
| T1. DB connection | ✅ **Final result** | SQLAlchemy engine + `create_all()` wired and verified against the Docker Postgres — idempotent restart confirmed. | 0.5 | 🟢 | Tahap 2 has **zero** DB/ORM code — fully from scratch |
| T2. Schema (17 tables) | ✅ **Final result** | All 17 models built and verified — `create_all` produces every table, FKs and JSONB/array columns confirmed correct. | 2.0 | 🟡 | Many tables, mechanically straightforward; no models to reference |
| T3. Qdrant collections | ✅ **Final result** | `candidate_vectors` + `jd_vectors` collections created and verified with a real upsert/query round-trip. | 1.0 | 🟢 | No vector DB in Tahap 2 |
| T4. File storage layout | ✅ **Final result** | Isolated per-candidate folders for CV + audio verified — layout, isolation, and round-trip all confirmed. | 1.0 | 🟢 | Tahap 2 only has a temp-file + in-memory dict, no structured layout to borrow |
| T5. Repository layer | ✅ **Final result** | Generic Repository class + one instance per entity, verified with real get/list/create calls. | 1.5 | 🟡 | |
| T6. Competency framework `[content]` | ✅ **Final result** | 10 competencies curated for **Web Developer** (re-curated 2026-07-13 after the role switch) with level descriptions + verified relations, loaded via an idempotent seed script. | 2.0 | 🟡 | Domain judgment, not code |
| T7. Resource library `[content]` | ✅ **Final result** | 30 resources (3/competency) curated and verified — every competency has full coverage. | 1.5 | 🟡 | Domain judgment |
| T8. Consent + audit write paths | ✅ **Final result** | Audit-log helper + consent gate verified — blocks without consent, allows once recorded. | 1.5 | 🟡 | No Tahap 2 equivalent |
| T9. Retention policy | ✅ **Final result** | 30-day retention rule + manual cleanup helper verified — deletes expired audio, correctly leaves recent audio untouched. | 0.5 | 🟢 | |
| T10. Seed data | ✅ **Final result** | All 30 CVs ran through the real pipeline + 2 synthetic interviews seeded, verified via direct DB queries. Found and fixed 2 real bugs (arg mismatch, hardcoded HR id) along the way. | **4.5** | 🟠 | Tiering explicitly skipped per user decision — QA Area 5 T5 still has no ground truth to test against |
| **Subtotal** | | | **~16h** | | vs. **16h** scheduled (Day 2-3) — tight but plausible IF T10 doesn't overrun |

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

- [x] **T5. Data access layer (repository pattern). — DONE 2026-07-13.** — *Depends: T2 · Flow: all*
  - [x] Thin repositories/CRUD over SQLAlchemy (no Alembic) — `backend/db/repository.py` (generic `Repository[ModelType]`: `get`/`list`/`create`), `backend/db/repositories.py` (one instance per entity, all 17)
  - ✅ Done when: each entity has get/create used by services — **verified**: created a `Company` + a linked `HRUser` through the repositories, fetched the company back by id, listed `hr_users` filtered by `company_id` (correct single result), confirmed `get()` on a nonexistent id returns `None` rather than raising; test rows cleaned up afterward (children deleted before parents, respecting FKs)

- [x] **T6. `[content]` Competency framework — ONE demo role: ~~Data Analyst~~ → Web Developer. — DONE 2026-07-13, RE-CURATED 2026-07-13 after the role switch.** — *Depends: T2 · Flow: 4, 8*
  - [x] List ~8-12 competencies with levels — **10 competencies curated for Web Developer**: HTML & CSS, JavaScript, Framework Frontend (React/Vue/Angular), Backend Development, Database (SQL/NoSQL), API Design & Integration, Version Control (Git), Responsive & Mobile-First Design, Deployment & DevOps Dasar, State Management — each with a 1/3/5-anchored Indonesian level description (`backend/seed/competency_framework_data.py`). The original Data Analyst set (SQL, Excel, Statistics, etc.) was deleted from the DB and fully replaced, not appended
  - [x] Encode lightweight relations (parent/related) feeding the matching graph (Area 2 T7) — each competency has 1-2 related competencies, internally consistent (e.g. HTML&CSS↔JavaScript↔Responsive Design cross-reference correctly)
  - [x] Store as seed rows in the reference table — `backend/seed/load_competency_framework.py`, idempotent (two-pass: create rows, then fill `related_competency_ids` once all ids exist); unchanged code, just re-run against the new content
  - ✅ Done when: one role fully covered; relations queryable; used by matching + report — **verified twice**: first for Data Analyst (10 competencies + 30 resources), then re-verified identically after the Web Developer re-curation — re-ran the loader (10 + 30 created), queried `related_competency_ids` directly, all populated and cross-referencing correctly

- [x] **T7. `[content]` Curated resource library — same role. — DONE 2026-07-13, RE-CURATED 2026-07-13 after the role switch.** — *Depends: T6 · Flow: 8*
  - [x] ~3 resources per competency (title, duration, milestone), keyed to competency ids — exactly 3 per Web Developer competency, 30 total, Indonesian titles/milestones (`backend/seed/competency_framework_data.py::RESOURCES`)
  - [x] Enough to assemble a deterministic report — same loader as T6, `backend/seed/load_competency_framework.py`
  - ✅ Done when: every competency has ≥1 mapped resource; report can select/order from it — **verified**: `LEFT JOIN` query confirms all 10 Web Developer competencies have exactly 3 resources each, none with zero

- [x] **T8. Consent + audit write paths. — DONE 2026-07-13.** — *Depends: T2 · Flow: 5, 6*
  - [x] Helper writes an `audit_log` row at every AI decision point + candidate-data access — `backend/services/audit.py::log()`
  - [x] Consent row gates interview processing — `backend/services/consent.py`: `has_consent()`, `require_consent()` (raises `ConsentRequiredError`, the 403 trigger for Area 2 T10's endpoint), `record_consent()`
  - [x] Consent is only ever written for candidates who actually go through the interview-gate step (the 1 live demo candidate) — **seed-only candidates get no `consent_records` row** (resolved 2026-07-12: they never reach the gate, so a record would be fabricated, not real) — enforced by design: nothing calls `record_consent()` except the real consent-gate flow
  - ✅ Done when: each AI stage leaves an audit row; no interview processing without consent — **verified**: created a real company→job→candidate chain, wrote an audit row and confirmed it's readable with correct action/metadata; confirmed `require_consent()` raises for a candidate with no consent record; confirmed it passes once `record_consent()` has run; all test rows cleaned up

- [x] **T9. Audio + CV retention/cleanup policy (light). — DONE 2026-07-13.** — *Depends: T4, T8 · Flow: 5 (PDP)*
  - [x] Define a simple retention rule tied to the consent record (audio) — `backend/services/retention.py`: `RETENTION_DAYS = 30`, `is_audio_expired(consented_at)`
  - [x] **Scope note:** the policy applies to real, consented recordings — i.e. only the 1 live demo candidate's audio. The 2-3 synthetic candidates' pre-made `.webm` clips are seed fixtures, not personal data collected under consent, so they're exempt (no consent record exists for them to tie a retention rule to — see T8) — enforced structurally: `cleanup_expired_audio()` only ever iterates candidates with a real `consent_records` row, nothing else is reachable
  - [x] Provide a callable manual cleanup helper — `cleanup_expired_audio(db, storage_root)`, returns the list of cleaned-up candidate ids
  - ✅ Done when: policy documented + cleanup callable exists (supports UU PDP) — **verified**: created two candidates with real audio files — one with a 35-day-old consent record (past the 30-day retention window), one with a 5-day-old record. Ran cleanup: the expired candidate's audio file was deleted, the recent candidate's audio was correctly left untouched; all test data cleaned up afterward

- [x] **T10. Seed data for demo — DONE 2026-07-13 (role/CV plan changed, tiering skipped per user decision).** — *Depends: T2, T6, T7, Area2 T5 · Flow: all*
  - ⚠️ **Final scope (2026-07-13, confirmed against original plan)**: (1) demo role is **Web Developer**, not Data Analyst; (2) the 30 CVs are **confirmed random, not curated/tiered** — user's own words: "for testing purposes only," so no strong/mid/weak spread exists (QA Area 5 T5 has no ground truth to assert against until revisited); (3) only **2** synthetic interview candidates (not 2-3), reusing the 2 existing test recordings
  - [x] 1 company + 1 seeded HR account + 1 Web Developer JD — created via the **real JD-creation path** (`services.extract.extract_competencies`, Area 2 T4), not a raw insert. `backend/seed/load_demo_data.py::_seed_company_hr_job()`
  - [x] ~~Manual Kaggle download, filter INFORMATION-TECHNOLOGY, curate 30~~ — superseded: user's 30 CVs used as-is, confirmed random/uncurated
  - [x] ~~Manually curate 30 candidate PDFs for a strong/mid/weak spread~~ — explicitly skipped per user decision
  - [x] ~~Record the intended match-quality tier per candidate~~ — not applicable, no tiering was done (QA Area 5 T5 gap still open, unresolved)
  - [x] Run each through the anonymization + parse pipeline (Area 2 T5) before seeding — **all 30 real CVs ran through the actual live pipeline** (`ingest_cv()` → PII redaction → Deepseek parse → embed → match score), not a shortcut
  - [x] **Candidate interview-data tiers**: of the 30 — **28 profile-only** (parsed_profiles + match_scores only), **2 pre-seeded synthetic interviews** (Kandidat WD-29, WD-30 — real distinct audio, transcripts, rubric_scores, interview_summaries, hr_decisions all seeded), **1 designated live candidate** (no interview data pre-seeded, for the real demo recording later)
  - [x] Competency + resource rows (from T6/T7) — already seeded, unaffected
  - ✅ Done when: one command loads a demo-ready DB with no manual DB fiddling — **verified end-to-end via direct DB queries**: 30 candidates, 30 parsed_profiles, 30 match_scores, 2 interview_answers/transcripts, 6 rubric_scores (3 criteria × 2), 2 interview_summaries, 2 hr_decisions, 0 consent_records (correctly zero — no seed/synthetic candidate gets a fabricated consent row, per the Area 3 T8 design). Ranked shortlist spot-checked (top 5 by score, plausible for random resumes vs. a Web Developer JD). Synthetic interview summaries correctly reflect the actual thin test-audio content, not fabricated text
  - ⚠️ **Real bugs found + fixed during this run**: (1) `extract_competencies()` called with 3 args instead of the required 4 (missing `qualifications`) — a genuine signature mismatch, fixed immediately; (2) `_seed_synthetic_interview()` hardcoded `decided_by=1`, assuming HR user id 1 — broke because this run's real HR user had id 17; fixed by threading the actual `hr.id` through. The interrupted first attempt (killed mid-way through the synthetic-interview step after finishing all 30 CVs) left one duplicate `interview_answers`/`rubric_scores` row for candidate WD-29, caught by inspecting row counts and cleaned up manually before the final verification above. **Note on the run itself**: real per-CV latency was uneven (roughly 1-50s per candidate depending on load), the whole 30-CV run took a bit over 2 hours wall-clock including the investigation into whether it was hung (it wasn't — genuinely progressing throughout, confirmed by polling `match_scores` count directly rather than trusting the (buffered-then-caught-up) log output)

---

## Area 2 — Backend & AI Integration  ·  Status: 🟢 Done (all 18 tasks T1-T16 verified end-to-end)

> Largest area, core of the MVP. Reuse Tahap 2 FastAPI + CV-parse. All LLM via SumoPod + caching (Area4 T3).
> Resolved: **T7 semantic+graph**, **T10 audio→Groq STT**, **T11 rubric temp=0**, **+T9b recruiter edit/approve**.

**Resolved 2026-07-12 (Area-2 session):**

| Aspect | Decision | Detail / rationale |
|---|---|---|
| Invite step (gap found) | **HR clicks "Invite" → backend generates token → UI shows copyable link** | New task T9c. No auto-distribution — for the demo, you (playing HR + candidate) copy/open it yourself. Simplest, matches a controlled recording |
| Rubric (T11) | **3 criteria, 1-5 scale**: clarity, relevance, technical depth | Each level anchored with a short description (1=vague/off-topic … 5=clear/precise/correct); curated as `[content]`, same category as the competency framework |
| Report format (T13/T14) | ~~Real PDF via `weasyprint`~~ → **ReportLab** (superseded 2026-07-12, see decision log) | ReportLab is pure Python, no Windows Pango/Cairo dependency risk; adapted styling technique from Tahap 2's `app.py::_build_report_pdf()`. Done 2026-07-13, see T14 |
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
| 12 | `report.py` + `report_pdf.py` | Assembles report content (skill-gap + framework + resource library) and renders it as **PDF via ReportLab** — gated on an `hr_decisions` row existing | `GET /candidates/{id}/report` | T13 | T12, T8, DB T6/T7 |
| 13 | `delivery.py` | Sends the PDF + summary via Telegram | `POST /candidates/{id}/send-report` | T14 | T13, Area 4 T3c (Telegram) |
| 14 | Async/caching/retry layer | Cross-cutting: async orchestration, retries on LLM/STT calls, response caching | n/a (wraps 1-13) | T15 | Area 4 T3 (cache) |
| 15 | OpenAPI contract | Auto-generated typed contract for the frontend | `/openapi.json` | T16 | T15 |

Module #14 is cross-cutting (no dedicated router/service file — wraps the others via decorators/middleware); #15 isn't hand-written, it's FastAPI's auto-generated output from the typed endpoints above.

### Task summary

| Task | Status | Summary | Est. hours | Difficulty | Note |
|---|---|---|---|---|---|
| T1. Audit Tahap 2 backend | ✅ **Final result** | Full 10-point code audit done — keep/rebuild/drop verdict written into `CLAUDE.md`. | **0.25** ↓ *(was 1.0)* | 🟢 | Deep audit already produced the keep/rebuild/drop verdict this task asks for |
| T2. Project structure | ✅ **Final result** | Layout already existed from Area 4 scaffolding — confirmed uvicorn boots and `/health` passes. | 1.0 | 🟢 | Tahap 2's structure is a LangGraph agent pipeline — not directly reusable |
| T3. Auth | ✅ **Final result** | JWT login + token-link isolation verified end-to-end via real HTTP requests. | 2.0 | 🟡 | Tahap 2 has zero auth code — fully from scratch |
| T4. JD full CRUD + extraction | ✅ **Final result** | Full CRUD verified end-to-end with real SumoPod extraction calls; company isolation confirmed via 404, not leakage. | 3.0 | 🟡 | No JD/employer concept exists in Tahap 2 (jobseeker-focused app) |
| T5. CV parse + PII redaction | ✅ **Final result** | Full pipeline verified end-to-end with a real CV upload; caught and fixed a real regex false-positive bug in PII redaction along the way. | **3.75** ↓ *(was 5.0)* | 🔴 | **Tahap 2 reuse**: `pdfplumber` text-extraction pattern adopted directly; PII redaction/SumoPod integration are new work |
| T6. Embeddings → Qdrant | ✅ **Final result** | Verified with real semantic matching — a JD correctly found its matching candidate at 0.805 similarity. | 1.5 | 🟡 | No embeddings code in Tahap 2 |
| T7. Matching engine | ✅ **Final result** | Verified with a real strong/mid/weak scenario — scores and ranks correctly discriminated. | 3.0 | 🟠 | Tahap 2's "matching" is a token-overlap heuristic — doesn't transfer |
| T8. Skill-gap analysis | ✅ **Final result** | Verified: real gap identified correctly, LLM output grounded to a deterministic seed, no-gap case short-circuits with zero LLM calls. | **1.0** ↓ *(was 1.5)* | 🟡 | **Tahap 2 reuse**: deterministic-seed-grounds-LLM-output pattern adapted from `_build_seed_gap()` |
| T9. Interview question gen | ✅ **Final result** | 3 real, relevant Indonesian questions verified for a live Web Developer JD. | 1.0 | 🟡 | No interview module in Tahap 2 |
| T9b. Recruiter edit/approve | ✅ **Final result** | Approval gate verified — edit blocked post-approval, invite blocked pre-approval. | 1.0 | 🟢 | |
| T9c. Invite candidate | ✅ **Final result** | Invite verified end-to-end; caught and resolved a real design conflict with T5's placeholder token. | 1.0 | 🟢 | |
| T10. Answer intake + STT | ✅ **Final result** | Consent gate + real audio transcription verified via live HTTP; token-impersonation attempt correctly rejected. | 2.0 | 🟡 | No STT in Tahap 2 |
| T11. Rubric scoring + summary | ✅ **Final result** | Verified against a real transcript; caught and fixed a design gap around interview-summary text sourcing. | 2.5 | 🟡 | No rubric/interview scoring in Tahap 2 |
| T12. HR decision endpoints | ✅ **Final result** | Verified end-to-end; grep-confirmed no auto-finalize path exists anywhere in the codebase. | 1.0 | 🟢 | No employer-decision flow in Tahap 2 |
| T13. Report generation | ✅ **Final result** | Verified end-to-end: gating, real curated resource citations, and determinism all confirmed. | 2.5 | 🟡 | Different approach from Tahap 2's LLM-free-generated content, no code reuse |
| T14. Report delivery | ✅ **Final result** | Verified with a real live Telegram send — user confirmed both PDF and summary arrived. Corrected a stale file citation along the way. | **2.0** ↓ *(was 3.0, weasyprint)* | 🟡 *(was 🟠)* | **Tahap 2 reuse**: real `_build_report_pdf()` found in `app.py` (not the file the plan cited) — adapted its panel-styling technique, pure-Python ReportLab retires the weasyprint Windows dependency risk |
| T15. Async wiring + error handling | ✅ **Final result** | Verified: retry logic behaves correctly, exception handler leaks nothing (unlike Tahap 2's). | **1.75** ↓ *(was 2.0)* | 🟡 | Tahap 2's async-job pattern is a minor reference; do not copy its traceback-leaking exception handler |
| T16. OpenAPI contract | ✅ **Final result** | Verified: 17 typed paths + 21 schemas exported correctly, genuinely usable for frontend codegen. | 0.5 | 🟢 | FastAPI-generated regardless |
| **Subtotal** | | | **~29.75h** *(was 33.5h)* | | vs. **32h** scheduled (Day 4-7, 4 days × 8h) |

### Foundation
- [x] **T1. Audit Tahap 2 backend repo — DONE 2026-07-12.** — *Depends: none · Flow: reuse for 3*
  - [x] Read `../brainstorming result/tahap 2 code reference/backend/` — full 10-point code audit completed this session
  - [x] Identify reusable FastAPI structure + working CV-parse — verdict: structure is a LangGraph agent pipeline (not reusable as-is); CV **text extraction** (pdfplumber + Gemini-vision fallback) is genuinely working and pattern-reused in T5; **PDF report generation** (ReportLab, ~700 lines) is fully working and reused in T14; skill-gap grounding pattern (`_build_seed_gap`) reused in T8
  - [x] **Strip all scraping code** — confirmed not applicable: no scraping pipeline exists in this codebase at all
  - [x] Note what's real vs merely designed (esp. security) — **confirmed absent, not just unverified**: zero auth code (no JWT, no login endpoint, all endpoints unauthenticated), zero DB/ORM (in-memory dict only, lost on restart), zero vector DB/embeddings/KGE. Full corrected inventory in `CLAUDE.md` § Existing Code To Reuse
  - ✅ Done when: a written keep/rebuild/drop verdict per component exists — **see `CLAUDE.md` correction + this file's § Effort & Difficulty Estimates for the per-task breakdown**

- [x] **T2. Project structure. — DONE (already existed from Area 4 scaffolding, confirmed 2026-07-13).** — *Depends: T1, Area4 T2 · Flow: all*
  - [x] `routers/ services/ models/ db/ services/llm.py config` — all present as Python packages since Area 4's initial scaffolding; `routers/` is an empty package pending actual endpoint files (T3+)
  - [x] Env loading for keys — centralized in `config.py`, already used by every service module built so far
  - ✅ Done when: uvicorn boots; `/health` returns ok — **re-verified**: booted clean, `GET /health` → `200 {"status":"ok"}`

- [x] **T3. Auth — HR-only login + tokenized candidate links. — DONE 2026-07-13.** — *Depends: T2 · Flow: all (isolation)*
  - [x] JWT issue/verify for **recruiter/HR only** (seeded account; no candidate signup) — `backend/services/auth.py` (`hash_password`/`verify_password` via bcrypt, `create_hr_jwt`/`verify_hr_jwt`), `backend/routers/auth.py` (`POST /auth/login`), `JWT_SECRET`/`JWT_EXPIRE_MINUTES` added to `config.py`
  - [x] Unguessable **token link** for candidate access (consent + interview), scoped to one session — `auth.generate_candidate_token()` (`secrets.token_urlsafe(32)` + TTL from `CANDIDATE_TOKEN_TTL_HOURS`), `auth.is_candidate_token_valid()`
  - [x] Guard: HR routes require JWT; candidate routes require a valid session token (own session only) — `routers/auth.py::get_current_hr()` FastAPI dependency (rejects missing/malformed/tampered tokens with 401)
  - ✅ Done when: only HR can log in; a candidate token opens only its own interview session; no candidate account exists — **verified end-to-end via real HTTP**: seeded a real HR user, `POST /auth/login` with correct credentials returned a working JWT; wrong password and unknown email both correctly 401. Verified the `get_current_hr` guard directly: valid token passes, missing "Bearer " prefix rejected, tampered/malformed token rejected. Verified candidate token isolation: two candidates' tokens are distinct and each resolves to exactly its own row; an unknown/guessed token resolves to nothing. All test rows cleaned up

### Ingestion & extraction
- [x] **T4. JD full CRUD + competency extraction (Flash). — DONE 2026-07-13.** — *Depends: DB T2, Area4 T3 · Flow: 1→2*
  - [x] `POST /jobs` — accepts **structured fields** (title, responsibilities, requirements, qualifications; see Area 1 T4b), scoped to `company_id` — `backend/routers/jobs.py`
  - [x] `GET /jobs` — list JDs for the logged-in HR's company
  - [x] `GET /jobs/{id}` — view one — scoped via `_get_scoped_job()`, returns 404 (not a leaking 403) for another company's job
  - [x] `PUT /jobs/{id}` — edit (re-triggers competency extraction)
  - [x] `DELETE /jobs/{id}` — **soft-delete (resolved 2026-07-12)**: sets `status='closed'`, no SQL `DELETE`; JD drops from the active list but all linked candidates/interviews/decisions/audit rows stay intact
  - [x] On create/update: Deepseek Flash → structured required competencies → persist to `jd_competencies` — `backend/services/extract.py::extract_competencies()`; update path deletes old competency rows first, then re-extracts fresh
  - ✅ Done when: HR can create/list/edit/close JDs; posting/editing the demo JD yields structured competencies in DB; "delete" never throws an FK error or drops audit history — **verified end-to-end via real HTTP + real SumoPod calls**: created a Web Developer JD → Flash correctly extracted 4 competencies (HTML/CSS/JavaScript/Frontend Framework); edited the JD's requirements to backend-focused content → re-extraction correctly replaced them with Node.js/PostgreSQL; list/get both correctly scoped to the JD's own company; soft-deleted → `status='closed'` in DB, row and its competency rows both still present (no FK error, no data loss); **cross-company isolation verified**: a second company's HR got `404` on the job (not data leakage) and an empty list. All test data cleaned up

- [x] **T5. CV upload + parse — text + vision-LLM caption fallback + PII redaction. — DONE 2026-07-13.** — *Depends: DB T4, Area4 T3, Area4 T3d · Flow: 3*
  - [x] **Tahap 2 reuse (2026-07-12 audit):** `backend/config/utils.py::read_file_node()` reference noted; extraction implemented fresh in `backend/services/pdf_extraction.py` following the "extract → detect empty → fall back" pattern
  - [x] `POST /candidates` accepts PDF (multipart form) — **HR/admin-side (or seed script) only for MVP**, not a public candidate-facing endpoint — `backend/routers/candidates.py`; required adding `python-multipart` to `requirements.txt` (FastAPI's `Form`/`File` deps need it, not listed as a direct dependency anywhere obvious)
  - [x] `pypdf.PdfReader` → extract text per page; mark pages with blank/whitespace text as `empty_text_pages` — `backend/services/pdf_extraction.py::extract_pdf()`
  - [x] Extract embedded images per page (`page.images`), tagged by page number — same function, `ExtractedImage` list; per-image try/except so one bad image doesn't lose the rest
  - [x] Per image: send to vision-capable LLM — **transcribe** mode if on an `empty_text_pages` page, **describe** mode otherwise — `backend/services/pdf_captioning.py::merge_pdf_text_and_captions()`, using the Area 4 T3d `vision_client`
  - [x] Merge page text + image transcriptions/captions into one document blob — same function
  - [x] **PII redaction on the merged text BEFORE the LLM parse call** — `backend/services/pii_redaction.py::redact_pii()` (regex email/phone + name substring replace); **bug found and fixed during verification**: the initial phone regex (`\d[\d\-\s()]{7,}\d`) was too loose and matched date ranges like `01/2000 to 10/2002` as false-positive phone numbers — tightened to require phone-like grouped-digit formatting (`\d{2,4}[\-\s]\d{3,4}[\-\s]\d{3,4}`), re-verified: real phone numbers (with `+62`, parens, dashes) still redact correctly, date ranges (both `/`- and `-`-separated) are now correctly left alone
  - [x] Parse redacted text → structured profile (skills/experience/qualifications), tagged with the alias only — `backend/services/cv_parser.py::parse_cv_text()` (Deepseek Flash)
  - [x] Store original file as-is (DB T4, HR-facing) + parsed/anonymized rows — `backend/services/candidate_ingest.py::ingest_cv()` ties the whole pipeline together: extract → merge captions → redact → parse → `storage.save_cv()` → `parsed_profiles` row
  - ✅ Done when: all 30 seed CVs (real PDFs, Kaggle) parse correctly regardless of text/scanned/mixed format; no real name/email/phone reaches the LLM or the structured DB row — **verified against real data**: extracted text from 5 real seed CVs correctly (all text-based, 0 scanned pages in this particular sample, so the vision-fallback path wasn't exercised by real seed data — it was separately verified in Area 4 T3d with a synthetic scanned-page image); uploaded one real CV through the full live pipeline via HTTP — correctly produced structured skills/experience/qualifications in `parsed_profiles`; **note**: the Kaggle `resume-dataset` CVs turned out to already be template/anonymized documents with no real names/emails/phones in them, so they couldn't validate redaction meaningfully — redaction was instead directly verified with an injected synthetic PII string (name+email+phone), confirmed none of it survives into the redacted text that would be sent to the LLM

- [x] **T6. Embeddings → Qdrant. — DONE 2026-07-13.** — *Depends: T4, T5, DB T3 · Flow: 4*
  - ⚠️ **Stale spec note**: this task's title still says "local multilingual sentence-transformers" from the original Area 4 draft — superseded 2026-07-13 by the actual resolved decision: **SumoPod `gemini/gemini-embedding-001`** (see `.env`, `plan.md` decision log). Built against the real current decision, not the stale title
  - [x] Embed candidate profile + JD competencies — `backend/services/embeddings.py::embed_text()` (SumoPod, 1536-dim truncated), `backend/services/candidate_embedding.py` (`embed_candidate_profile()`, `embed_jd_competencies()` — both convert structured DB rows into Indonesian-language text before embedding)
  - [x] Upsert to Qdrant collections with competency payload — candidate payload includes `skills`; JD payload includes `competencies` list
  - ✅ Done when: vectors present for JD + all candidates; query returns neighbors — **verified against real data**: seeded a JD (JavaScript/React/Node.js competencies) and a matching candidate (JavaScript/React/HTML/CSS skills), embedded both via real SumoPod calls, confirmed both vectors exist in Qdrant with 1536 dimensions and correct payloads; queried `candidate_vectors` using the JD's own vector — correctly returned the matching candidate as the top (and only) neighbor with a strong 0.805 similarity score, confirming genuine semantic matching rather than keyword overlap. Test data cleaned up

### Matching & analysis
- [x] **T7. Matching engine — semantic + lightweight competency-graph. — DONE 2026-07-13.** — *Depends: T6, DB T6 · Flow: 4*
  - [x] Qdrant similarity as base score — `backend/services/matching.py::compute_match_score()`; computed as direct cosine similarity between the candidate's and JD's own retrieved vectors (numpy), not a Qdrant filtered search — simpler and avoids depending on Qdrant's query-filter dict/model syntax
  - [x] Boost using competency-graph relations from the framework (related-competency credit) — `compute_graph_boost()`: for each JD competency, credit either an exact skill match or a candidate skill that's a `related_competency_ids` neighbor in `competency_framework`
  - [x] **Combine via weighted sum (resolved 2026-07-12)**: `overall_score = 0.7 × semantic_similarity + 0.3 × graph_boost` — `SEMANTIC_WEIGHT`/`GRAPH_WEIGHT` constants
  - [x] **Retain per-competency match detail** for explainability (Q17) — `competency_breakdown` JSONB stores `semantic_similarity`, `graph_boost`, and `matched_competencies` (the actual competency names that drove the score)
  - [x] `backend/routers/matching.py::GET /jobs/{id}/candidates` — ranked shortlist endpoint, company-scoped
  - ✅ Done when: ranked shortlist; each score expands to which competencies drove it; formula is the documented weighted sum — **verified against a realistic 3-candidate scenario** (strong/mid/weak fit vs. a JavaScript/React/Node.js/Database JD): scores correctly discriminated (Strong 0.79 > Mid 0.58 > Weak 0.44), ranks assigned 1/2/3 correctly, `matched_competencies` correctly showed `["JavaScript","React","Node.js"]` for the strong candidate vs. `[]` for the mismatched one. Verified via real HTTP call to `GET /jobs/7/candidates` — full ranked JSON returned with per-candidate breakdown. All test data cleaned up

- [x] **T8. Skill-gap per candidate (Deepseek Pro). — DONE 2026-07-13.** — *Depends: T7 · Flow: 4→8*
  - [x] **Tahap 2 reuse (2026-07-12 audit):** `agent_4_recommendation_report.py::_build_seed_gap()`/`_is_skill_match()` pattern adapted in `backend/services/skillgap.py` — `build_seed_gap()`/`_is_skill_match()` compute a deterministic token-overlap gap first; the LLM call is then grounded against it (any LLM-claimed "missing competency" not in the deterministic seed is discarded, falling back to the seed itself)
  - [x] Candidate profile vs JD competencies → structured gap output — `analyze_skill_gap()`: `{gap_summary, missing_competencies, development_priority}`, real Deepseek Pro call
  - [x] Persist — **no dedicated table exists in the 17-table schema** (confirmed against the module inventory: skill-gap is explicitly "(internal, feeds T13)" — the report-generation step is its actual consumer, not a standalone persisted record). Implemented as a callable service function T13 will invoke directly, not backed by its own DB row
  - ✅ Done when: each shortlisted candidate has a structured gap record — **verified**: real gap (missing React/Node.js/PostgreSQL for a JS/HTML/CSS candidate) correctly identified, sensible Indonesian summary generated, LLM output correctly grounded to the deterministic seed (no hallucinated extra gaps); the no-gap edge case (candidate already has everything) correctly short-circuits with zero LLM calls

### AI Interview Module (the new component)
- [x] **T9. Interview question generation (Flash). — DONE 2026-07-13.** — *Depends: T4 · Flow: 5*
  - [x] From JD → **2-3 questions** in Bahasa Indonesia — `backend/services/interview_questions.py::generate_questions()`, `POST /jobs/{id}/questions/generate`
  - [x] Persist to `interview_questions` as status=`draft`
  - ✅ Done when: demo JD generates 2-3 sensible, relevant Indonesian questions in `draft` — **verified**: real call against a Web Developer JD produced 3 genuinely relevant technical questions (state management, auth, performance optimization), all in `draft`

- [x] **T9b. Recruiter edit/approve questions (human-in-the-loop). — DONE 2026-07-13.** — *Depends: T9 · Flow: 5*
  - [x] `GET/PUT /jobs/{id}/questions` — HR edits/adds/removes — `backend/routers/interview_questions.py`; edit is blocked with `400` once any question is `approved` (a real guard, not just a comment)
  - [x] `POST .../approve` flips status → `approved` + unlocks candidate invite
  - [x] Candidate only ever sees approved questions — enforced structurally: the invite endpoint (T9c) checks for `approved` questions before issuing a token, so no candidate flow can begin without them
  - ✅ Done when: candidate can't start until HR approves; edited text is what the candidate sees — **verified**: `PUT` on already-approved questions correctly 400s; `POST .../approve` correctly flips all draft questions to `approved`

- [x] **T9c. Invite candidate to interview (NEW — closes the gap between shortlist and interview). — DONE 2026-07-13.** — *Depends: T7, T9b · Flow: 4→5*
  - [x] `POST /candidates/{id}/invite` — generates the unguessable `token` (+ `token_expires_at`) for that candidate, only callable once questions are `approved` (T9b) — `backend/routers/candidates.py::invite_candidate()`
  - ⚠️ **Design conflict found + resolved**: T5's candidate creation already writes a placeholder `token`/`token_expires_at` at CV-upload time (required by the NOT NULL schema columns), but T9c wants the *real* invite token issued only after question approval. **Resolved (user's call)**: the invite endpoint regenerates a fresh token + expiry at invite time, overwriting the meaningless placeholder — no schema change needed
  - [x] Response/UI surfaces the copyable token link — **no auto-distribution** (resolved 2026-07-12: HR copies/shares it manually; for the demo, you play both HR and candidate)
  - ✅ Done when: HR can invite a shortlisted candidate; the resulting link opens that candidate's own consent+interview session and no other's — **verified**: invite attempted before approval correctly 400s ("interview questions are not approved yet"); after approval, invite succeeds and the DB confirms the candidate's token was genuinely regenerated (differs from the T5 placeholder)

- [x] **T10. Answer intake (AUDIO) + STT transcription. — DONE 2026-07-13.** — *Depends: T9c, Area4 T3b, DB T4, DB T8 · Flow: 5*
  - [x] **Consent check (resolved 2026-07-12, explicit):** reject with 403 if no `consent_records` row exists for the candidate — `backend/routers/interview_answers.py` maps `ConsentRequiredError` → `403`
  - [x] `POST` accepts the candidate's audio file → store (DB T4) — `backend/routers/interview_answers.py::submit_interview_answer()`, candidate-token-authenticated (new `get_candidate_by_token()` dependency added to `routers/auth.py`), not HR-JWT
  - [x] Transcribe via Groq `whisper-large-v3`, `language=id` (Area4 T3b) — `backend/services/interview_answers.py::submit_answer()` calls the existing `stt_client`
  - [x] Persist transcript; recruiter can fetch raw audio + transcript — `interview_answers` + `transcripts` rows, correctly linked via `answer_id`
  - ✅ Done when: an Indonesian audio answer yields a stored file + correct transcript; a submission with no consent record is rejected — **verified end-to-end via real HTTP**: submission without a consent record correctly 403s; after writing a real consent record, submission succeeds — a real `.m4a` recording (from Area 4 T3b's earlier test clips) was correctly saved to disk and transcribed accurately by Groq; DB confirms `interview_answers`↔`transcripts` linked correctly; **also verified**: a token belonging to one candidate cannot be used against a different `candidate_id` in the URL (401), and a wrong/mismatched token check catches impersonation attempts

- [x] **T11. Rubric scoring + answer summary (Pro, temp=0, FIXED schema). — DONE 2026-07-13.** — *Depends: T10 · Flow: 5→6*
  - [x] **Rubric locked (resolved 2026-07-12) `[content]`**: 3 criteria — **clarity**, **relevance**, **technical depth** — each on a **1-5 scale** with an anchored description per level — `backend/services/rubric_data.py`, full Indonesian 1-5 level descriptions per criterion, authored this session
  - [x] Score the **transcript** per criterion at **temperature=0** — `backend/services/rubric.py::score_answer()`, uses `chat_pro()` (Area 4 T3) which always enforces `LLM_TEMPERATURE_SCORING`
  - [x] Produce an **AI summary of the answer's main points** for the recruiter — same call returns a `summary` field
  - [x] Persist to `rubric_scores` (one row per criterion, per `interview_answers` schema) — `backend/services/rubric_persist.py::score_and_persist_answer()`
  - ⚠️ **Design gap found + fixed during build**: `interview_summaries.ai_summary_text` needs a real "main points" summary, but no per-answer summary column exists on `interview_answers` to source it from later. Fixed by threading each answer's `score_answer()`-produced `summary` field through the caller (`routers/rubric.py::build_interview_summary()` collects `per_answer_summaries` from each scored answer) rather than adding a new column or a wasted extra LLM call
  - [x] `backend/routers/rubric.py` — `POST /candidates/{id}/answers/{answer_id}/score`, `POST /candidates/{id}/interview-summary`
  - ✅ Done when: same transcript → identical score across runs (QA T3); recruiter gets a readable summary — **verified**: real scoring against a real transcript produced sensible, differentiated scores (clarity=4, relevance=3, technical_depth=2) with genuine per-criterion rationale reflecting the transcript's actual thin content; repeated calls returned identical results; `rubric_scores` confirmed persisted correctly (one row per criterion); `interview-summary` endpoint correctly aggregated `overall_score=3.0` (average) with a real, non-placeholder summary text — confirming the design-gap fix above actually works, not just compiles

- [x] **T12. Human-in-the-loop endpoints — no auto-reject. — DONE 2026-07-13.** — *Depends: T11, DB T8 · Flow: 6→7*
  - [x] HR reads AI score/summary — already exposed via T11's `GET`-able rubric/summary data
  - [x] `POST /decisions` records the final outcome — `backend/routers/decisions.py`, validates `decision ∈ {advance, reject}`, company-scoped, overwrites any prior decision for the same candidate (one current decision per candidate, not a stacked history)
  - [x] **No code path finalizes a candidate without HR action** — enforce in code, not just UI — verified by direct code search: `grep -rn "hr_decisions.create"` across the entire backend returns exactly one hit, this endpoint
  - ✅ Done when: inspection shows no auto-finalize path; QA T6 passes — **verified**: invalid decision value correctly 400s; valid `advance` succeeds; re-posting `reject` for the same candidate correctly overwrites (DB confirms exactly one row, the latest); decision for a nonexistent/wrong-company candidate correctly 404s; grep-based inspection confirms no other write path exists

### Report & delivery
- [x] **T13. Deterministic development report. — DONE 2026-07-13.** — *Depends: T12, T8, DB T6, DB T7 · Flow: 8*
  - [x] **Gated on a decision existing (resolved 2026-07-12):** only generatable once `hr_decisions` has a row for the candidate — `backend/routers/report.py` checks this explicitly, 400s otherwise
  - [x] From skill-gap (T8) + competency framework + resource library — `backend/services/report.py::build_report()`
  - [x] Assemble by **selecting/ordering** curated items (no free generation) — for each missing competency (from T8's grounded gap analysis), looks up the matching `competency_framework` row by name and its `resource_library` rows — a deterministic dict lookup, never invented content; unmatched competency names are skipped, not fabricated
  - [x] Produce for **every decided** candidate (pass or fail — a decision either way triggers a report) — gate only checks a decision *exists*, not its value
  - ✅ Done when: same skill-gap input → identical report (QA T4); report cites real curated resources; no report exists for a candidate with no `hr_decisions` row — **verified end-to-end**: report request before any decision correctly 400s; after recording a decision, the report correctly identified the missing competencies (Framework Frontend, Backend Development) and cited their exact real curated resources from the Web Developer framework/resource library seeded in Area 3 T6/T7 (e.g. "React untuk Pemula sampai Mahir", "Membangun REST API dengan Node.js/Express") — not invented text; repeated calls returned byte-identical JSON, confirming determinism

- [x] **T14. Report delivery — automated via Telegram (only channel). — DONE 2026-07-13.** — *Depends: T13, DB T8, Area4 T3c · Flow: 8*
  - [x] **PDF library: ReportLab (resolved 2026-07-12, Tahap 2 audit)**: ~~weasyprint~~ — **⚠️ file-reference correction (2026-07-13)**: the plan's cited file (`agent_function/agent_4_recommendation_report.py::_build_report_pdf()`) does **not** contain this function at all — that file is only the seed-gap token-matching logic (already correctly reused in T8). The actual `_build_report_pdf()` (~370 lines, `SimpleDocTemplate`/`Paragraph`/`Table`/panel styling) lives in **`backend/app.py`**, confirmed by direct grep across the whole Tahap 2 reference tree. Read the real function and adapted its **styling technique** (bordered panel tables with colored headers) — not its literal structure, since Tahap 2's report shape (career-gap: certifications/market-aligned-skills/upskilling-effort-tiers) is structurally different from ours (competency_framework + resource_library development plan). New file `backend/services/report_pdf.py`, styled with Area 1's locked Enterprise Trust teal
  - [x] **Telegram:** using the candidate's linked `chat_id` (Area4 T3c), auto-send via `sendDocument` (the PDF) + `sendMessage` (summary) — `backend/services/delivery.py::send_report()`
  - [x] HR triggers delivery with one click; no email, no manual copy/paste — `POST /candidates/{id}/send-report`
  - ✅ Done when: HR clicks "send report" and the candidate (pass or fail) receives the file + summary via Telegram automatically — **verified end-to-end with a real live Telegram send** (user confirmed): PDF generation checked visually first (correct Indonesian layout, teal panel headers, all report sections present and readable — not just "produces bytes"); `send-report` before a decision correctly 400s; after recording a decision, a real PDF was generated, saved to `storage/reports/`, and delivered via real `sendDocument` + `sendMessage` calls to the user's actual Telegram chat — user confirmed both the file and summary message arrived correctly

### Orchestration & contract
- [x] **T15. Async wiring + error handling + caching. — DONE 2026-07-13.** — *Depends: T4–T14 · Flow: all*
  - [x] FastAPI async orchestration across stages — already in place: `interview_answers`/`candidates` routers use `async def` where file I/O benefits from it; each stage (T4-T14) already calls the next synchronously within a request, no separate job queue needed at this scale
  - [x] Retries on LLM/STT calls — `backend/services/retry.py::with_retry()` decorator (3 attempts, linear backoff), applied to `llm_client.py::_create_completion()` and `stt_client.py::_create_transcription()` — wraps only the actual network call, not the surrounding cache logic
  - [x] Caching via Area4 T3 — already built (T3), unaffected by the retry wrapper (verified a real LLM call still succeeds after wrapping)
  - [x] **⚠️ Do NOT replicate Tahap 2's exception handler (2026-07-12 audit finding):** its global `@app.exception_handler(Exception)` returns raw Python tracebacks as JSON in 500 responses — a real security anti-pattern. Ours must return a generic error message, log the traceback server-side only — `backend/main.py`: two handlers — `http_exception_handler` (passes through our own intentional `HTTPException`s with their real, safe detail) and `unhandled_exception_handler` (catches everything else, logs the full traceback server-side via `logger.exception()`, returns only a generic message + a correlation `error_id`)
  - ✅ Done when: full pipeline runs end-to-end without manual step-poking; a forced 500 never leaks a stack trace to the client — **verified**: retry decorator tested directly — succeeds after 2 transient failures on the 3rd attempt, and correctly exhausts + raises after all attempts fail; exception handlers tested directly — a forced `RuntimeError` containing deliberately sensitive-looking text returned only `{"detail": "An unexpected error occurred.", "error_id": "..."}`, no traceback or internal detail in the response body; a real `HTTPException(404, "Job not found")` correctly passed through with its actual detail intact

- [x] **T16. Publish OpenAPI contract for frontend. — DONE 2026-07-13.** — *Depends: T15 · Flow: integration*
  - [x] Ensure endpoints are typed — every router uses Pydantic request/response models (`response_model=...`), not raw dicts
  - [x] Export `/openapi.json` for Area 1 wiring — FastAPI auto-generates this, no hand-written work needed
  - ✅ Done when: frontend can generate/consume the contract — **verified**: fetched `/openapi.json` from the live server, confirmed OpenAPI 3.1.0, **17 endpoint paths** (all of T3-T14's routers) and **21 typed component schemas** registered; spot-checked `JobOut`'s schema — correct field names, types, and a `required` list, genuinely usable for typed client generation (e.g. `openapi-typescript`) once Area 1 wires the frontend

---

## Area 1 — Frontend UI/UX  ·  Status: 🟢 Done (all 13 tasks T1-T9 including sub-tasks verified end-to-end)

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

No changes from the Tahap 2 backend audit (Area 1 was already corrected in its own session — no
React code exists to reuse, only visual language, already captured in T1/T2 below).

| Task | Status | Summary | Est. hours | Difficulty | Note |
|---|---|---|---|---|---|
| T1. Audit Tahap 2 frontend | ✅ **Final result** | Confirmed no React code exists to reuse — only the visual language, already captured in the design artifacts. | 0.5 | 🟢 | |
| T2. Design system | ✅ **Final result** | 9 shared components built and verified via a real Playwright screenshot — correct teal/gold/Georgia-serif styling, zero console errors. | 3.0 | 🟡 | Design locked/previewed 2026-07-12 |
| T3. Vite structure + route guards | ✅ **Final result** | React Router + typed OpenAPI client wired; both guard screens verified via real Playwright runs against the live backend. | 1.5 | 🟡 | Required 2 backend gap-fills: CORS middleware (missing entirely) + 3 new candidate-facing endpoints |
| T4. HR login | ✅ **Final result** | Login + error state + persisted session verified live against the real seeded HR account. | 1.0 | 🟢 | |
| T4b. JD CRUD UI | ✅ **Final result** | List/create/edit/close verified end-to-end live, including validation error + competency re-extraction on save. | 2.5 | 🟡 | |
| T5. Shortlist | ✅ **Final result** | Ranked list + expandable explainability + tier status verified live on the real 30-candidate seed data. | 3.0 | 🟡 | Required 1 backend gap-fill: `invited_at` column (placeholder tokens made "invited" unrecoverable from `token` alone) |
| T5b. Question edit/approve UI | ✅ **Final result** | Generate/edit/add/remove/approve verified live end-to-end; post-approval read-only lock confirmed. | 1.5 | 🟡 | |
| T5c. Invite modal | ✅ **Final result** | Invite + copy + re-view (same link, no silent regeneration) verified live end-to-end. | 1.0 | 🟡 | Required 1 backend gap-fill: read-only `GET /candidates/{id}` so re-viewing never calls the regenerating POST /invite |
| T6. Candidate audio interview | ✅ **Final result** | Full recorder machine verified live: real getUserMedia+MediaRecorder via Playwright's fake-device flag, real upload/STT round-trip, mic-denied path, completion guard. | **5.5** | 🔴 | Live human-mic sanity check still pending (user to confirm) |
| T7. HR decision + detail + delivery | ✅ **Final result** | Full detail screen verified live: CV/skill-gap, audio+transcript+rubric, decision, all 3 report-send states including a real error+retry. | **4.0** | 🟠 | Required 3 backend gap-fills: full detail endpoint + audio-streaming endpoint, a real `report_sent_at` field (had been wrongly inferred), and a real cross-cutting CORS-on-error bug fix |
| T8. Candidate consent + Telegram linking | ✅ **Final result** | Consent + required Telegram gate verified live with 3 real repeated deep-link sends — poller correctly captured the real chat_id every time. | 1.5 | 🟡 | Required 2 backend gap-fills: the Telegram poller itself, plus a real app-wide logging visibility bug (`logging.basicConfig` was never called, silently dropping every `INFO` log in the whole app) found while double-checking the poller |
| T9. Cross-cutting UX | ✅ **Final result** | Full audit of every screen against the 6 checkpoints; found and fixed 4 real gaps (2 missing retry paths, 1 button-group race, verified the rest already correct). | 2.5 | 🟡 | Mostly an audit pass — every prior task already used the shared components |
| **Subtotal** | | | **~28h** | | vs. **32h** scheduled (Day 8-11, 4 days × 8h) |

- [ ] **T1. Audit Tahap 2 frontend — corrected scope.** — *Depends: none*
  - [ ] Confirmed: `../brainstorming result/tahap 2 code reference/frontend/` is static HTML/CSS/JS, **not React** — nothing to port as code
  - [ ] Extract the reusable **visual language only**: colors (`#102b4f` navy, `#4f46e5` indigo, teal/success/warning/danger tokens), Inter font, card/badge conventions — see the published design-comparison artifact for the faithful recreation
  - ✅ Done when: written verdict — zero code reuse, visual-language reuse only

- [x] **T2. Minimal design system (React + Vite, built fresh) — Enterprise Trust LOCKED. — DONE 2026-07-13.** — *Depends: T1*
  - [x] Direction confirmed 2026-07-12: **Enterprise Trust** — teal `#0f6b5c`, gold `#c98a2c`, Georgia serif headings, teal-tinted paper `#f4f7f6` — `frontend/src/styles/tokens.css` (CSS custom properties: colors, typography, spacing scale, radii/shadow). Top-nav dossier layout deferred to **T3** (page-shell/routing structure, not a component-library concern)
  - [x] Shared components: tables, cards, score badges, forms, status pills (T5 tier), **skeleton loader, inline error+retry, empty-state, spinner-with-label** (all used by T9) — `frontend/src/components/`: `Card`, `Button` (primary/secondary/danger), `Badge` (neutral/success/warning/danger/info tones, used for T5 tier pills), `Table`, `TextField`/`TextAreaField`, `SkeletonLoader`, `ErrorState` (with retry), `EmptyState`, `SpinnerWithLabel` — all 9 components built
  - [x] Removed default Vite boilerplate (`App.css`, `index.css`, react/vite logo assets) — replaced with the real token file
  - ✅ Done when: shared components exist (not a full system), built in React matching the locked direction — **verified visually via a real Playwright screenshot** (installed `playwright` + Chromium, since no browser-automation tool was otherwise available on this machine): booted the real Vite dev server, rendered a preview page exercising every component, screenshot confirms correct teal/gold/Georgia-serif Enterprise Trust styling, zero console errors. Screenshot showed one demo-data sloppiness (both table rows showed the same badge tone) — a throwaway preview-page bug, not a component bug, harmless since this file gets replaced by real routing in T3+

- [x] **T3. Vite structure + route guards. — DONE 2026-07-13.** — *Depends: none*
  - [x] Routing + minimal state — `react-router-dom`, routes: `/login`, `/jobs` (HR-guarded), `/candidate/:id/consent`, `/candidate/:id/interview`, catch-all → invalid-link
  - [x] API client generated/typed from OpenAPI (Area 2 T16) — `openapi-typescript` generates `frontend/src/api/schema.d.ts` from the live `/openapi.json`; `openapi-fetch`-based client in `frontend/src/api/client.ts` auto-attaches the HR bearer token
  - [x] **Route guards**: `HrAuthGuard` (frontend/src/lib/HrAuthGuard.tsx) redirects to `/login` with no HR token; `CandidateTokenGuard` (frontend/src/lib/CandidateTokenGuard.tsx) resolves the token via the new `GET /candidates/{id}/self`, redirects to consent if `has_consent=false`, renders the shared `InvalidLinkPage` on any 401 (expired/malformed/unknown token)
  - [x] **Backend gap found + fixed while building this**: no CORS middleware existed at all (confirmed via a real Playwright run — every frontend fetch to the backend failed with a CORS error, silently manifesting as "invalid token" in the UI, not an obvious CORS message). Added `CORSMiddleware` in `main.py` allowing `http://localhost:5173`. Also added 3 candidate-facing endpoints that didn't exist yet but were required for the guard to have anything to call: `GET /candidates/{id}/self` (token-gated self-info: job title, consent/telegram/interview-completion flags), `POST /candidates/{id}/consent`, `GET /candidates/{id}/questions` (approved-only, token-gated, for T6)
  - ✅ Done when: app boots on host (Vite dev server); an expired/invalid token and a consent-skip both land on the right guard screen — **verified with a real Playwright run against the live backend + a real seeded candidate token** (id 32): (1) `/` → `/login` render confirmed, (2) `/jobs` with no HR token → redirected to `/login`, (3) garbage token on the interview route → real "Link tidak valid" screen (screenshot confirms Enterprise Trust styling), (4) real valid-but-no-consent token → correctly redirected to `/candidate/32/consent`, screen fetched and displayed the real job title ("Web Developer") from the live backend

- [x] **T4. HR login screen (recruiter only). — DONE 2026-07-13.** — *Depends: Area2 T3*
  - [x] Login for HR/recruiter → HR home — `frontend/src/pages/LoginPage.tsx`, calls `POST /auth/login`, stores the JWT in localStorage via `frontend/src/api/client.ts`
  - [x] Candidate pages are **not** behind login — reached via token link (see T6/T8) — separate `CandidateTokenGuard` path, no shared auth state
  - ✅ Done when: HR logs in; no candidate login exists — **verified with a real Playwright run against the live backend and the real seeded HR account** (`hr@gaskeundemo.test`): wrong password shows the correct inline error (screenshot confirms Enterprise Trust styling), correct credentials redirect to `/jobs` with the JWT persisted in localStorage, a full page reload stays logged in (HR guard sees the token, no bounce to `/login`)

- [x] **T4b. 💎 Job description CRUD (list + structured create/edit/delete). — DONE 2026-07-13.** — *Depends: Area2 T4 · Flow: 1*
  - [x] JD list view, scoped to the logged-in HR's company — `frontend/src/pages/JobsListPage.tsx`, calls `GET /jobs` (backend already scopes by `hr["company_id"]`)
  - [x] Create/edit form: **structured fields** — title, responsibilities, requirements, qualifications (separate inputs, not one free-text box) — `frontend/src/pages/JobFormPage.tsx`, shared between `/jobs/new` and `/jobs/:jobId/edit`
  - [x] Delete action (MVP: simple, no cascade-guard) — backend `DELETE /jobs/{id}` is a soft-delete (`status='closed'`), matches the existing anti-FK-error design; UI shows a "Tutup Lowongan" button, not a destructive delete
  - ✅ Done when: HR can list, create, edit, and delete JDs from the UI using the structured form — **verified with a real Playwright run against the live backend**: empty-title validation blocks submit with the correct inline error, a real JD (`POST /jobs`, which also triggers real competency extraction) appears in the list immediately, editing pre-fills the structured fields correctly and persists changes, closing flips the status badge to "Ditutup." Zero console errors throughout. Test JDs and their `jd_competencies` rows cleaned up from the DB afterward so the seed data stays clean.

- [x] **T5. 💎 HR shortlist w/ explainability + tier status. — DONE 2026-07-13.** — *Depends: Area2 T7 · Flow: 4*
  - [x] Ranked list + match score — `frontend/src/pages/ShortlistPage.tsx`, `GET /jobs/{job_id}/candidates`, sorted by `rank`
  - [x] Expand a score → which competencies matched (Q17) — click-to-expand row shows semantic-similarity %, graph-boost %, and matched-competency badges from `competency_breakdown`
  - [x] **Status pill per candidate (resolved 2026-07-12, corrected 2026-07-13)**: *Belum diundang* / *Menunggu wawancara* / *Selesai wawancara*, derived from row presence — **found and fixed a real design gap while building this**: the original plan said "no `candidates.token` yet" for *Belum diundang*, but every candidate already gets a placeholder token at CV-upload time (T5's earlier design resolution), so `token IS NOT NULL` could never distinguish invited from not-invited. Added a nullable `candidates.invited_at` column, set once at `POST /candidates/{id}/invite` time (idempotent — re-inviting doesn't reset it, protecting T5c's re-viewable-link requirement). `GET /jobs/{job_id}/candidates` now returns `invited`/`interview_completed`/`decided` booleans derived from `invited_at`/`interview_answers`/`hr_decisions` row presence.
  - [x] "Undang ke Interview" button per row (opens T5c modal) — button present and correctly relabels to "Lihat Link Undangan" once invited; real modal wiring is T5c's job (currently a placeholder `alert()`)
  - [x] **Instant read (resolved 2026-07-12)**: reads pre-computed `match_scores` — no live matching call, no "run ranking" button
  - ✅ Done when: a viewer can see *why* a candidate ranks AND which stage each of the 30 is at; the ranked list appears instantly with no wait — **verified live against the real 30-candidate Web Developer seed data**: all 30 rows render sorted by score, the 2 synthetic interview candidates (WD-29/WD-30) correctly show "Selesai wawancara" while the other 28 show "Belum diundang" (confirmed against direct DB state, not just the UI), expanding a row shows real semantic-similarity/graph-boost percentages and matched-competency badges (e.g. HTML/CSS/JavaScript). Zero console errors.

- [x] **T5b. 💎 Recruiter question edit/approve. — DONE 2026-07-13.** — *Depends: Area2 T9b · Flow: 5*
  - [x] View AI-generated questions; edit/add/remove — `frontend/src/pages/QuestionsPage.tsx`, linked from the Shortlist page
  - [x] Approve → unlocks candidate invite — fields lock read-only and edit/remove/save controls disappear once approved (backend already rejects edits to approved questions; the invite endpoint already requires approved questions to exist)
  - ✅ Done when: HR approves before any candidate can start — **verified live on a real disposable test job**: empty state → "Buat Pertanyaan (AI)" generates real Deepseek-Flash questions, edited text persists through save, add/remove both work and persist correctly, approve flips to a read-only "Disetujui" view with zero edit affordances left. Zero console errors. Test job and its questions deleted afterward.

- [x] **T5c. 💎 Invite candidate modal (NEW — closes the Area 2 T9c UI gap). — DONE 2026-07-13.** — *Depends: Area2 T9c, T5 · Flow: 4→5*
  - [x] Modal opened from the Shortlist row action: calls `POST /candidates/{id}/invite`, only enabled once questions are approved (T5b) — `frontend/src/components/InviteModal.tsx` + `Modal.tsx` (new shared primitive)
  - [x] Shows the generated token link as copyable text — no auto-send, HR copies it manually — "Salin Link" button, clipboard-verified
  - [x] **Re-viewable (resolved 2026-07-12) — real backend gap found and fixed while building this**: re-viewing an already-invited candidate's link must NOT call `POST /invite` again, since that endpoint always regenerates the token — doing so on "re-view" would silently invalidate a link already shared with the candidate, exactly the bug this task exists to prevent. There was no read-only way to fetch the existing token, so added `GET /candidates/{id}` (HR-scoped, returns `token`/`token_expires_at` only if already invited, never regenerates). `InviteModal` now branches: not-yet-invited → `POST /invite`; already-invited → `GET /candidates/{id}`.
  - ✅ Done when: HR can invite a candidate and copy their link without leaving the Shortlist screen; reopening the modal later still shows the same link — **verified live on a real seeded candidate** (WD-14, job 16): invite generates a real link, copy-to-clipboard confirmed byte-for-byte, status pill flips to "Menunggu wawancara" and the button relabels to "Lihat Link Undangan" without a page reload, reopening shows the **identical** link (asserted programmatically, not just eyeballed) rather than a freshly regenerated one. Zero console errors. Candidate's `invited_at`/`token` reset back to its pre-test state afterward to keep the seed data clean.

- [x] **T6. 💎 Candidate AUDIO interview (token link, no login) — highest-risk component. — DONE 2026-07-13 (fake-mic verified; live-mic sanity check pending user).** — *Depends: Area2 T9b/T10 · Flow: 5*
  - [x] **Tested the recorder in Chrome (Playwright/Chromium) FIRST** — `frontend/src/lib/useAudioRecorder.ts` (MediaRecorder state machine) + `frontend/src/pages/CandidateInterviewPage.tsx`
  - [x] **Mic permission flow**: request → granted → recording; **denied/blocked → explicit blocking message** ("Izinkan akses mikrofon untuk melanjutkan") with a retry button, never silent dead-air
  - [x] Open via token link → show approved question + **count-up timer** (no auto-stop)
  - [x] Record (MediaRecorder → webm), stop, **playback, re-record**
  - [x] **Block empty submission** with a message (checked on submit: no blob or 0 elapsed seconds)
  - [x] **Per-question upload (resolved 2026-07-12)**: submit each answer → uploads + transcribes via a real `fetch` multipart POST (spinner-with-label during upload) → advance to next question on success; a failed upload shows an inline error + retry, doesn't lose the recording
  - [x] Loops for however many approved questions exist, then a completion screen
  - [x] **Completion guard**: already wired via `CandidateTokenGuard`'s `interview_completed` flag (built in T3) — reload after finishing shows "Wawancara sudah selesai, terima kasih" instead of the recorder
  - ✅ Done when: candidate opens the link, records + submits each voice answer end-to-end with no account; denied mic, empty submit, and post-completion reload each show their correct state — **verified live against the real backend using Playwright's `--use-fake-device-for-media-stream` flag** (grants mic permission and feeds a synthetic audio stream through the *real* `getUserMedia`/`MediaRecorder` code path, not a mock): real recording start/stop/playback/re-record, a real multipart upload that produced a real stored `.webm` file and a real Groq Whisper transcript in the DB, completion screen after the last question, and a reload correctly showing the completion-guard message. **Separately verified the mic-denied path** (no fake-device flag, permissions explicitly withheld) shows the exact required blocking message with a working retry button. Zero console errors across both runs. Test consent/answer/transcript rows and the test audio file were cleaned up afterward. **Still pending**: a live sanity check with the user's actual microphone in a real browser window, since Playwright's fake device — while exercising the identical code path — cannot fully stand in for real hardware/OS permission-prompt behavior.

- [x] **T7. 💎 HR decision + candidate detail + report delivery. — DONE 2026-07-13.** — *Depends: Area2 T8/T10/T11/T12/T13/T14 · Flow: 6-7,8*
  - [x] Parsed CV + skill-gap — `frontend/src/pages/CandidateDetailPage.tsx`, real-time skill-gap analysis (calls `analyze_skill_gap` live, not cached/precomputed)
  - [x] Raw **audio player** + transcript + AI summary + rubric score — `frontend/src/components/AudioPlayer.tsx` fetches the authed audio blob and plays it via object URL (the backend endpoint requires the HR bearer token, so a plain `<audio src>` wouldn't have worked)
  - [x] Advance/reject action; UI makes clear AI only *recommends* — explicit note under the AI summary: "AI hanya memberi rekomendasi, keputusan akhir ada di tangan HR"
  - [x] **Report delivery**: "Kirim Laporan" button appears once a decision exists, calls the real `send-report` endpoint
  - [x] **Missing-Telegram / already-sent states**: both verified — disabled "Kandidat belum menautkan Telegram" when no chat_id, disabled "Terkirim" when already sent
  - [x] **Send loading + error state**: spinner during send, inline error + retry on failure
  - **3 real backend gap-fills found while building this**:
    1. **No detail endpoint existed** — added `GET /candidates/{id}/detail` (new `backend/routers/candidate_detail.py`) combining parsed profile, live skill-gap, per-answer audio/transcript/rubric, interview summary, decision, and report/Telegram state in one call. Caught a real bug immediately: assumed `experience`/`qualifications` were dicts (matching the SQLAlchemy `JSONB` type annotation), but the real seeded data is a list for both — fixed the Pydantic schema to match reality, not the type-annotation assumption.
    2. **No audio-streaming endpoint existed** — `interview_answers.audio_path` was a bare filesystem path, meaningless to a browser. Added `GET /candidates/{id}/answers/{answer_id}/audio` (HR-scoped, `FileResponse`).
    3. **`report_sent` was wrongly inferred** from `decision exists AND telegram_chat_id exists` — caught by testing the ready-to-send state: a candidate who legitimately had both should show the active button, but was showing "Terkirim" despite `send_report` never having been called. No field tracked "was actually sent." Added a real `hr_decisions.report_sent_at` nullable timestamp, set only inside `services/delivery.py::send_report()` on a real successful send.
  - **1 real cross-cutting bug found and fixed**: testing the send-error path (fake `telegram_chat_id` → real Telegram API 400) surfaced that FastAPI's custom `@app.exception_handler` responses were missing CORS headers entirely — confirmed directly with curl (200/404 responses had `access-control-allow-origin`, the 500 didn't). The browser reported this as a CORS failure, completely masking the real 500 + error_id from the frontend. Fixed by explicitly attaching CORS headers in both exception handlers in `main.py` — this was a latent bug affecting every unhandled exception in the whole app, not just this endpoint.
  - ✅ Done when: HR can replay audio, read transcript+summary, record a decision, then send the report — all from this one screen; no click ever produces a failed/broken Telegram send on camera — **verified live against the real backend**: full detail view on a real synthetic candidate (skills/experience/qualifications, real skill-gap analysis, real 13-second audio playback, real transcript, real rubric scores, real AI summary, existing decision badge, disabled missing-Telegram state), a fresh decision recorded live on a different real candidate (button → badge transition), and the send-report error+retry path exercised with a real (intentionally invalid) Telegram chat_id — confirmed the UI shows the actual error message and retry button rather than crashing or masking it as a network failure. All test data (decision, telegram_chat_id) reset back to each candidate's pre-test state afterward. A genuine happy-path send (valid chat_id) was not re-tested here since it requires the user's real Telegram identity — the identical code path was already verified live during Area 2 T14.

- [x] **T9. Cross-cutting UX: loading, errors, empty states, refresh. — DONE 2026-07-13.** — *Depends: T2 · Flow: all*
  - [x] Shared inline **error component** with retry, used on every AI/STT/upload/Telegram call site — **audit found 3 real gaps, all fixed**: (1) `AudioPlayer` had no retry on a failed audio-blob fetch, only a full reload — added a `reloadKey`-driven retry, verified live with a real simulated failure+retry via Playwright route interception; (2) `CandidateInterviewPage`'s question-load error had no retry — added the same pattern; (3) `QuestionsPage`'s shared `actionError` (covering generate/save/approve) had no retry at all — added `lastFailedAction` tracking so retry re-calls whichever of the 3 actions actually failed. Login/JobForm/InviteModal's validation-style errors deliberately have no separate retry button (resubmitting via the existing submit button already covers it — a redundant button would be noise, not a gap).
  - [x] **Loading** treatments: skeleton loaders confirmed on JD list + shortlist; spinner-with-label confirmed on all long AI/upload waits; **found and fixed 1 real race**: `QuestionsPage`'s "Simpan Perubahan"/"Setujui Pertanyaan"/"+ Tambah Pertanyaan"/"Hapus" only disabled themselves individually during their own call, not each other — a user could click Approve while Save was still in flight. Fixed to disable the whole button group whenever `busy !== null`; verified live that the group correctly locks during a real save.
  - [x] **Empty states**: confirmed present and correctly conditioned on JD list (first login) and pre-match shortlist (already verified live in T4b/T5)
  - [x] **JD form validation**: confirmed present and matches the spec exactly — title required, ≥1 of responsibilities/requirements required (verified live in T4b)
  - [x] **Data freshness**: confirmed no polling/realtime exists anywhere in the frontend (`grep`'d for `setInterval`/`setTimeout` — the only two hits are the audio recorder's own countup timer and a one-shot "Tersalin!" UI reset, neither refetches data); documented the manual-refresh model in `plan.md`'s decision log since no dedicated demo-script file exists yet
  - [x] **Non-goals honored**: confirmed zero `@media`/`matchMedia`/mobile-specific code anywhere — single theme, desktop-only, no responsive/mobile recorder path, exactly as scoped
  - ✅ Done when: no screen shows a raw error, infinite spinner, or blank-with-no-explanation during the demo happy path — **systematic audit of all 9 pages against all 6 checkpoints**, not just a visual skim; 4 real gaps found and fixed (3 missing-retry, 1 disabled-state race), 2 live-verified with real simulated failures via Playwright route interception (not just code review), the rest confirmed already correct from prior tasks' live verification

- [x] **T8. 💎 Candidate consent (token link) — Telegram linking only. — DONE 2026-07-13.** — *Depends: Area2 T5, DB T8 · Flow: 5*
  - [x] Candidate token page: consent checkbox (gates interview, PDP) — `frontend/src/pages/CandidateConsentPage.tsx`, calls the existing `POST /candidates/{id}/consent`
  - [x] Candidate token page: "Tautkan Telegram" button → deep-links to `t.me/<bot>?start=<token>` — **required** step, enforced by genuinely blocking "Mulai Wawancara" until `has_telegram_link=true` (not just a UI suggestion)
  - **Real backend gap found and fixed**: "required" couldn't actually work as a hard gate — `services/telegram_client.py::get_updates`/`extract_start_token` (built in Area 4 T3c) were never invoked by anything; nothing polled Telegram or wrote the resulting `chat_id` anywhere. Consulted the user on 3 options (build a real poller / add a manual-only re-check button / soften "required" to skippable); **user chose to build a real poller**. Added `backend/services/telegram_poller.py` — a simple `asyncio` background loop (3s interval) started on FastAPI startup, calling `get_updates`/`extract_start_token` and writing `chat_id` onto the matching candidate. Runs inside the same process (no separate cron needed for a local MVP using `getUpdates`, not a webhook).
  - [x] Frontend "Sudah tautkan? Cek status" button re-fetches candidate self-info on demand, since the frontend has no other way to know a background Telegram interaction happened
  - ✅ Done when: consent recorded; candidate links Telegram before starting the interview. **Report sending now lives on T7, not here** (resolved 2026-07-12) — **verified with a real, live end-to-end test, not a mock**: recorded real consent for a real seeded candidate, generated the real `t.me/GaskeunkerjaBot?start=<token>` deep-link, **the user clicked the real link and pressed Start in their actual Telegram app**, the poller picked it up and wrote a real `chat_id` (`1304618784`) to the candidate row within the poll interval, and reloading the consent page correctly showed "Telegram berhasil ditautkan" with the interview now unblocked. Test consent record and chat_id reset afterward to keep the seed data clean.

- [ ] `[deferred]` **Full HR dashboard shell / nav polish beyond the JD list (T4b)** — minimal nav only.
- [ ] `[deferred]` **Responsive/usability polish beyond demo happy-path.**

---

## Area 5 — QA  ·  Status: 🟡 In progress (T3/T3b/T4/T5-fixture/T5/T6/T8 all done, both 2026-07-13 findings root-caused and fixed same day; T10 paused + T12 6/7 done at the real-Telegram checkpoint; T11 held — all 3 resume together with the user present)

> **⚠️ Updated 2026-07-13 (pre-Area-5-execution planning session).** Two things resolved with the
> user before build starts:
> 1. **T5's tiering blocker is resolved**: a small dedicated tiered fixture (2 strong/2 mid/2 weak,
>    curated fresh for the Web Developer JD) will be added, decoupled from the main 30-CV demo pool
>    — the demo pool stays as-is (random/untiered, per the 2026-07-13 Area 3 decision). New task
>    **T5-fixture** below.
> 2. **New task T11 added: visible end-to-end scenario suite.** The user asked to watch Playwright
>    drive the real app on their own screen (not headless/background) for a set of realistic
>    end-to-end scenarios, to independently confirm sufficiency of the whole system beyond the
>    per-task verifications already done throughout Areas 1-4. **This applies only to Area 5 test
>    runs** — headless/background Playwright remains the default for verifying edits in any other
>    area. 7 scenarios agreed (5 requested + 2 more the user asked for, for a fuller sufficiency
>    check): happy-path full lifecycle, candidate-blocked paths, HR-blocked paths, failure+retry
>    paths, multi-actor/concurrency-adjacent status correctness, data-integrity tracing, and
>    seed-data hygiene after test runs. Full breakdown in T11 below.

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

**Failure gate (resolved 2026-07-12, extended 2026-07-13):** if any 💎 claim test (T3, T3b, T4, T5, T5-fixture, T6, T8, T11) fails on the day it's run, fix it before starting the next day's build tasks. This is the entire point of shifting them left — a noted-but-deferred failure defeats the purpose. T11's scenarios apply this per-scenario: a failing scenario is fixed before moving to the next one, not batched to the end.

> ## ✅ Two significant 2026-07-13 findings — both RESOLVED same day, user-directed fixes
>
> Both tests initially **failed** against the real system. Rather than force a pass, both gaps were
> traced to root cause, presented to the user with real tradeoffs, and fixed per their explicit choice.
>
> 1. **T3b found: candidate names were NOT actually redacted before reaching the LLM.** Root cause traced
>    precisely: `ingest_cv()` never had a real name to pass to `redact_pii()` in the first place — the API
>    contract only ever accepts `job_id`/`alias`/`file`, HR never types a name, and `Candidate` has no
>    real-name DB field (by design). The name only exists inside the raw CV text. A "first line = name"
>    heuristic was tested and found unreliable on real seed data. **User chose: LLM-based name extraction**
>    (one cheap Flash call, `pii_redaction.detect_candidate_name()`) over a NER library or leaving it
>    undocumented. **Fixed and verified**: detects a real fake name correctly on fixture text, correctly
>    returns `None` (no hallucination) on genuinely name-free real seed CV text — tested against 5 real
>    samples. `backend/tests/test_qa_t3b_pii_redaction.py` now has 3 passing tests (was 2, one documenting
>    the gap) proving the fix, not just documenting the absence.
> 2. **T3 and T4 found: rubric scoring and skill-gap analysis were NOT fully deterministic at temperature=0.**
>    Root cause confirmed as provider-level (SumoPod/Deepseek's batched/distributed inference serving,
>    not our prompts/code — same category of issue OpenAI's own docs acknowledge for their API). We don't
>    control SumoPod's serving infrastructure, so it can't be fixed at the request level. **User chose:
>    self-consistency voting** (call the LLM 3x, take the per-criterion median for rubric scores / majority
>    vote for skill-gap competencies) over softening the submission wording alone. **Fixed and verified**:
>    `rubric.score_answer()` (9 real calls across 3 outer runs, zero drift) and `skillgap.analyze_skill_gap()`
>    (9 real calls, zero drift) both now vote internally. This roughly **triples the real LLM cost** of
>    rubric scoring (used once per interview answer) and skill-gap analysis (used in candidate detail view +
>    report generation) — a deliberate, informed tradeoff for the highest-stakes accuracy/consistency claims.
>    **Also found and fixed a related reliability gap while re-testing**: `llm_client.py`'s OpenAI client had
>    no configured timeout at all (SDK default is 10 minutes), which could make a single slow/stalled
>    provider response block far longer than reasonable — added an explicit 60s client-level timeout.

**Cost guardrail (resolved 2026-07-12):** T3 and T4 each make 5 genuinely independent, cache-bypassed Deepseek calls per run. Cheap individually, but run them **once when the feature is believed complete** — not repeatedly inside an edit-test-edit debugging loop. This is exactly the repeated-spend pattern Area 4's whole caching strategy exists to avoid.

### Task summary

No changes from the Tahap 2 backend audit (Tahap 2 has no test suite to reference).

| Task | Status | Summary | Est. hours | Difficulty | Note |
|---|---|---|---|---|---|
| T3. Determinism test | ✅ **Final result, gap fixed** | Self-consistency voting (3 calls, median) shipped in `rubric.score_answer()` — 9 real calls, zero drift, re-verified. | 1.5 | 🟡 | Cost tripled for this call site — user-approved tradeoff |
| T3b. PII redaction test | ✅ **Final result, gap fixed** | LLM-based name detection shipped (`pii_redaction.detect_candidate_name()`) — verified on fixture text (finds fake name) and real seed CVs (correctly returns None, no hallucination). | 2.0 | 🟡 | One extra Flash call per CV ingest |
| T4. Report consistency test | ✅ **Final result, gap fixed** | Same voting fix extended to `skillgap.analyze_skill_gap()` (majority vote) — 9 real calls, zero drift, re-verified. | 1.5 | 🟡 | Cost tripled for this call site — user-approved tradeoff |
| T5-fixture. Tiered test CVs | ✅ **Final result** | 6 synthetic CVs (2 strong/2 mid/2 weak) seeded under a separate "Web Developer (QA Fixture)" JD (job_id=21), fully separate from the 30-CV demo pool. | 1.0 | 🟢 | |
| T5. Matching/tier check | ✅ **Final result** | Real scores confirm monotonic discrimination: strong (0.69, 0.64) > mid (0.52, 0.50) > weak (0.43, 0.43). | 1.0 | 🟢 | |
| T6. Human-in-loop test | ✅ **Final result** | Real AST-based static check (not a one-off grep) confirms `hr_decisions.create()` only ever called from the HR-authenticated endpoint + the seed script. | 1.0 | 🟢 | |
| T8. Consent-gate test | ✅ **Final result** | Both cases verified live: no-consent → `ConsentRequiredError`/403; valid consent → real submit+transcribe succeeds. Cleanup verified, zero orphaned data. | 1.0 | 🟢 | |
| T10. Full e2e run | 🔄 **Paused at Telegram checkpoint** | Real seed→HR→invite→consent flow verified live; live candidate (id=59) now genuinely mid-flow, ready to resume. Also found+fixed a real "Terkirim" seed gap. | 2.0 | 🟡 | Remaining steps held for the T11 session |
| T11. 💎 Visible e2e scenario suite (NEW) | ⏸️ **Held** | 7 realistic scenarios, run live in a visible (non-headless) browser on the user's screen. | 4.0 | 🟠 | **User explicitly held this for a later session** (2026-07-13) — do not start without the user present |
| T12. Demo-readiness checklist | 🔄 **6/7 edge states verified** | All non-Telegram edge states (expired token, mic-denied, empty-submit+real-submit, completion-guard, invite re-view, Terkirim fix) confirmed live. | 2.5 | 🟡 | Real Telegram delivery check remains, folded into T11 |
| **Subtotal** | | | **~17.5h** | | Spread across Day 4-12 alongside build work — same person, same hours pool |

- [x] **T3. 💎 Determinism test. — DONE 2026-07-13, real gap FOUND AND FIXED same day.** — *Depends: Area2 T11*
  - [x] Same **transcript** → same rubric score across repeated **cache-bypassed** runs — `backend/tests/test_qa_t3_determinism.py`, added `bypass_cache` passthrough to `services.rubric.score_answer()`
  - [x] **Real finding, root-caused**: the ORIGINAL single-call version showed genuine ±1-point variance across runs, consistent with provider-level temperature=0 non-determinism (confirmed not a code bug via direct root-cause tracing — SumoPod/Deepseek's batched/distributed serving, which we don't control). Directly contradicted an explicit submission claim (`tahap 3 jawaban.md` Q9).
  - [x] **Fixed**: `services/rubric.py::score_answer()` now does self-consistency voting — calls the LLM 3x internally, takes the per-criterion **median** — user's explicit choice over softening the submission wording alone
  - ✅ Done when: re-verified against the FIXED function — 9 real calls across 3 outer runs, **zero drift observed**, matching the tightened tolerance

- [x] **T3b. 💎 PII redaction test (NEW — closes a real gap). — DONE 2026-07-13, real gap FOUND AND FIXED same day.** — *Depends: Area2 T5*
  - [x] Fed CV text with a known fake name/email/phone through the real pipeline — `backend/tests/test_qa_t3b_pii_redaction.py`, dedicated standalone fixture text, not a curated seed CV
  - [x] **Mocked the outgoing LLM request** (patched `services.cv_parser.llm_client.chat_flash`) for the parse-payload assertion — zero cost, no live call
  - [x] Asserted the captured payload never contains the raw email/phone — **passes**, both are genuinely redacted
  - [x] **Real finding, root-caused precisely**: `ingest_cv()` never had a real name to redact — the API contract only ever accepts `job_id`/`alias`/`file`, and `Candidate` has no real-name field (by design). The name only exists inside raw CV text. A "first line = name" heuristic was tested and found unreliable on real seed data.
  - [x] **Fixed**: `services/pii_redaction.py::detect_candidate_name()` — one real, cheap Flash call to find the name before redaction runs (user's explicit choice over a NER library or leaving it undocumented). Verified correctly detecting a fake name on fixture text AND correctly returning `None` (no hallucination) on 5 real, genuinely name-free seed CVs (Kaggle's public Resume Dataset is itself already PII-stripped)
  - ✅ Done when: 3 tests pass — email/phone redaction proven, name detection+redaction proven working, name-free-text correctly declined

- [x] **T4. 💎 Report consistency test. — DONE 2026-07-13, real gap FOUND AND FIXED same day.** — *Depends: Area2 T13*
  - [x] Same skill-gap input → report data compared across repeated **cache-bypassed** runs — `backend/tests/test_qa_t4_report_consistency.py`, added `bypass_cache` passthrough to `services.skillgap.analyze_skill_gap()` and threaded through `services.report.build_report()`
  - [x] **Compared the underlying report data, not rendered PDF bytes** — diffs `build_report()`'s dict directly, before `report_pdf.py` renders anything
  - [x] **Real finding, same root cause as T3**: `development_priority` AND the `development_plan`'s actual competency **set** both varied across independent runs on the same input (one run dropped a competency entirely)
  - [x] **Fixed**: `services/skillgap.py::analyze_skill_gap()` now does self-consistency voting — 3 internal calls, **majority vote** per competency (survives only if ≥half the votes included it) + most-common `development_priority`
  - **Bonus fix found while re-testing**: `llm_client.py`'s OpenAI client had no configured timeout (SDK default 10 min) — added an explicit 60s client-level timeout so a single stalled provider response can't block disproportionately
  - ✅ Done when: re-verified against the FIXED function — 9 real calls across 3 outer runs, **zero drift observed**

- [x] **T5-fixture. 💎 Curate a small dedicated tiered CV fixture (NEW — resolves the 2026-07-13 blocker below). — DONE 2026-07-13.** — *Depends: none*
  - [x] Curated **6 small CVs** for the Web Developer JD, deliberately fit-differentiated — `backend/seed/fixture_cv_content.py` (2 strong, 2 mid, 2 weak; synthetic/fabricated, no real people)
  - [x] Ingested through the real pipeline under a **separate JD** ("Web Developer (QA Fixture)", job_id=21) — `backend/seed/load_t5_fixture.py`, generates real PDFs via ReportLab, calls the real `ingest_cv`/`embed_candidate_profile`/`compute_match_score` chain, fully decoupled from the 30-CV demo pool
  - ✅ Done when: 6 fixture candidates exist with real `match_scores` — **verified**: candidate_ids 62-67, scores confirmed monotonic by tier (see T5 below)

- [x] **T5. Matching formula / curated-tier check (promoted from manual-only, unblocked 2026-07-13). — DONE 2026-07-13.** — *Depends: Area2 T7, DB T10, T5-fixture*
  - [x] Read the **intended tier per fixture candidate** — `backend/tests/test_qa_t5_matching_tiers.py`, tier read directly from `seed/fixture_cv_content.py`'s tagging, no separate manifest needed
  - [x] **Aggregate comparison**: strong-tier average vs weak-tier average, required gap ≥0.05
  - ✅ Done when: the average-score gap confirms real discrimination — **verified with real scores**: strong avg 0.667 (0.690, 0.644), weak avg 0.429 (0.430, 0.428), mid avg 0.509 (0.516, 0.502) — gap 0.238, well above the 0.05 threshold, and the full 6-candidate ordering is genuinely monotonic by tier

- [x] **T6. 💎 Human-in-the-loop test. — DONE 2026-07-13.** — *Depends: Area2 T12*
  - [x] Confirmed no code path finalizes a candidate without HR action — `backend/tests/test_qa_t6_human_in_the_loop.py`, a real **AST-based static check** over the actual source tree (not a one-off manual grep, so it stays valid as the codebase changes): asserts `repo.hr_decisions.create()` is only ever called from `routers/decisions.py` (HR-authenticated) or `seed/load_demo_data.py` (seed-only), and that `record_decision`'s signature genuinely depends on `get_current_hr`
  - ✅ Done when: no auto-finalize path exists — **verified**, both checks pass

- [x] **T8. 💎 Consent-gate enforcement test (promoted from deferred/smoke). — DONE 2026-07-13.** — *Depends: Area2 T10*
  - [x] Submit an interview answer for a candidate with no `consent_records` row → asserted `ConsentRequiredError` is raised (the real 403 the router maps it to) — `backend/tests/test_qa_t8_consent_gate.py`
  - [x] Submit after a valid consent record exists → asserted real success, including a real Groq Whisper transcription (reused an existing seed audio clip rather than fabricating new audio)
  - ✅ Done when: both cases behave correctly — **verified live**, both tests pass, test data (answer/transcript) cleaned up afterward with zero orphaned rows confirmed

- [ ] **T10. Full e2e happy-path run — rewritten to match the current flow. — PARTIALLY DONE 2026-07-13, paused at the real-Telegram checkpoint.** — *Depends: all core · **Run: Day 12** (re-baselined 2026-07-12; this one genuinely needs everything built; T3/T3b/T4/T5/T6/T8 above are re-run here as a confirmation pass, not run for the first time)*
  - [x] Seed data loads: 1 company, 1 JD (**Web Developer**), **30 candidates** — **verified live**: all 30 candidates have real `parsed_profiles` rows (zero silent partial-parse failures)
  - [x] HR: create/view JD (structured fields) → view Shortlist (instant, pre-computed scores + tier status pills) — **verified live, headless/background** (per user instruction: visible-browser mode is T11-only)
  - [x] HR: edit/approve interview questions (T5b) → **invited the designated live candidate** (candidate_id=59, "Kandidat WD-28" — the 3rd-from-last seeded candidate per `load_demo_data.py`'s tier logic), copied the real token link
  - [x] Candidate: open token link → consent recorded — **paused here**: the next step (link Telegram) is exactly the checkpoint held for the T11 session
  - [ ] Candidate: **link Telegram** → record + submit each audio answer → completion screen — *(record+submit was actually exercised separately during T12's edge-state pass, using candidate 59 — see T12 below; only the Telegram-link step itself remains, tied to T11)*
  - [ ] HR: review candidate detail → record decision → **send report via Telegram** (real send) — blocked on the same checkpoint
  - [x] Spot-check the 2 synthetic candidates show their pre-seeded "Terkirim" state correctly — **real gap found and fixed**: the seed script never actually set `telegram_chat_id`/`report_sent_at` for the 2 synthetic candidates (60, 61), so despite the plan's own T7 writeup claiming this was verified, they were actually showing the "missing Telegram" disabled state, not "Terkirim." Patched both candidates' DB rows directly (fabricated `telegram_chat_id`, real `report_sent_at` timestamp) and updated `load_demo_data.py`'s `_seed_synthetic_interview()` so any future fresh seed run sets this correctly too. Re-verified live: both now correctly show "Terkirim."
  - ✅ Done when: one clean pass with no manual DB fiddling — **candidate 59 (the live candidate) is now genuinely mid-flow** (invited, consented, has a real recorded interview answer from T12's edge-state pass) — ready to resume from exactly the Telegram-link step whenever the T11 session happens

- [ ] **T11. 💎 Visible end-to-end scenario suite (NEW 2026-07-13 — user-requested sufficiency check).** — *Depends: T10 · **Run: Day 12, alongside T10/T12***
  - **Why this is distinct from T10**: T10 is one scripted happy-path confirmation pass. T11 is the user directly watching Playwright drive the real running app on their own screen — `headless: false` + `slowMo`, not headless/background — across 7 scenarios chosen to sufficiency-check the whole system, including blocked/failure/multi-actor paths T10 doesn't cover. **This visible-browser mode applies only to these T11 runs** — every other area's edit-verification work reverts to headless/background Playwright, per the user's explicit instruction.
  - [ ] **Scenario 1 — Happy path, full lifecycle**: HR logs in → creates a JD → questions generate/approve → HR invites a real ranked candidate → candidate consents + links Telegram (real click, per the T8 pattern) → candidate completes the audio interview (fake-media-stream, real MediaRecorder code path) → HR reviews (audio/transcript/rubric/skill-gap) → HR records a decision → HR sends the report → Telegram delivery confirmed
  - [ ] **Scenario 2 — Candidate-blocked paths**: expired/invalid token → "link tidak valid" screen; no consent yet → forced to consent screen; mic permission denied → blocking message + retry; interview already completed → reload shows "sudah selesai" instead of the recorder
  - [ ] **Scenario 3 — HR-blocked paths**: inviting before questions are approved → 400 error surfaces correctly; JD form validation (empty title, empty responsibilities+requirements) → blocked with message; re-opening an already-issued invite link → shows the identical token, never regenerates
  - [ ] **Scenario 4 — Failure + retry paths**: audio upload failure mid-interview → error shown, retry doesn't lose the recording; report send with no Telegram link → disabled state; report send with a broken Telegram delivery (real invalid chat_id, per the T7 pattern) → real error + retry, not a crash or a masked CORS failure
  - [ ] **Scenario 5 — Multi-actor / concurrency-adjacent status correctness**: on one JD's shortlist, simultaneously show one "Belum diundang," one "Menunggu wawancara," one "Selesai wawancara" candidate — confirm each status pill is independently correct; confirm a synthetic seeded candidate (pre-loaded decision, no real interview) displays its "Terkirim"/finished state correctly
  - [ ] **Scenario 6 — Data-integrity tracing**: for one candidate pushed through the full pipeline, verify CV → parsed profile → embedding → match score → skill-gap → interview → rubric → summary → decision → report all trace back correctly to that *same* candidate with no cross-contamination — checked against the DB directly, not just the UI
  - [ ] **Scenario 7 — Seed-data hygiene after test runs**: confirm the test runner cleans up every piece of test data it created (consent records, decisions, telegram_chat_id, invited_at, interview_answers/transcripts, test JDs) so the real demo seed data is never left polluted — codifies the manual cleanup discipline already used throughout Areas 1-4 into an actual checked step
  - ✅ Done when: all 7 scenarios have been run **visibly on the user's screen** with the user confirming each one in real time, and the seed DB is verified clean afterward (Scenario 7)

- [ ] **T12. Demo-readiness checklist — now includes the edge-state walkthrough (promoted from happy-path-only). — 6 OF 7 EDGE STATES VERIFIED 2026-07-13.** — *Depends: T10*
  - [x] Happy-path script written and rehearsed — see T10 above (paused at the same Telegram checkpoint)
  - [x] **Edge/safety states walked through, headless/background (6 of 7 done, all verified live)**:
    - [x] Expired/invalid token screen → real garbage token correctly shows "Link tidak valid"
    - [x] Mic-permission denied → correctly shows the blocking message with retry
    - [x] Empty/0-second audio submit blocked, then a real answer recorded+submitted successfully (candidate 59's real interview answer — this is the same answer T10 will reuse when resumed)
    - [x] Interview completion-guard → reloading after submission correctly shows "Wawancara sudah selesai" instead of the recorder
    - [x] Invite-modal re-view ("Lihat Link Undangan") → reopening the modal for the already-invited live candidate shows the byte-identical token link, confirmed programmatically, not just eyeballed
    - [x] **Synthetic-candidate "Terkirim" state — real gap found and fixed** (see T10 above): was never actually producing "Terkirim" before this session despite being claimed done in T7's writeup; now genuinely verified showing correctly for both candidates 60 and 61
    - [ ] Missing-Telegram disabled send button — **not separately re-verified this pass** (already verified live during T7's original build; not re-run here since nothing changed in that code path)
  - [ ] **Telegram delivery verified for real**: still needs the user's real Telegram check — tied to the same held checkpoint as T10/T11
  - [x] Seed loaded, latency acceptable, no crashes on any of the above — confirmed across all headless runs, zero console errors
  - ✅ Done when: a rehearsed run is recorded AND every edge state above has been seen at least once, AND a real Telegram message has been confirmed received — **6/7 edge states done; the real Telegram delivery check remains, folded into the held T11 session**

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
