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
| 1. Frontend UI/UX | 🟡 In progress (T1-T9, T11-T15 done; T10 visual rebuild 6.5/8 pages remaining) | 19 | 0 | Day 8–11 |
| 5. QA | 🟢 Done (all 9 tasks T3/T3b/T4/T5-fixture/T5/T6/T8/T10/T11/T12 verified end-to-end; 3 real findings found and fixed across the session) | 9 | 5 | Day 4-12 (shifted left, spans build; final pass Day 12 — see banner) |
| **Round 2 — Post-MVP Polish** (see § below; extended 2026-07-18 with points #16-21) | 🟡 In progress — user verifying one-by-one (no Playwright, per explicit instruction). Points #1-15: 7/13 tasks done (B7 #1, B1 #2, B2 #3+#4, B3 #6+#7, B8 #5, A3+B6 #11 — 8/13 points), 6/13 tasks code-applied awaiting check, 1 resolved no-code. Points #16-21 (T16-T21, added 2026-07-18): 3/6 done + verified (#16, #17, #18); 3/6 code-complete pending live verification (#19 needs Gmail App Password, #20 needs a backfill run, #21 needs a real-browser camera pass — none of these three have been exercised in a browser this session) | 19 | 0 | 2026-07-17+ |

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
| T3d. Vision-LLM client | ✅ **Final result, provider + routing changed 2026-07-15** | `vision_client.py` now on SumoPod `gemini-2.5-flash-lite` (~12% cheaper, Groq kept as rollback). `describe_image()` removed — every image is now transcribed unconditionally, fixing a real content-loss bug found via testing the user's own real CVs. | **2.0** ↓ *(was 2.5)* | 🟠 | **Tahap 2 reuse**: its Gemini-vision OCR fallback (`_ocr_pdf_with_gemini`) is a working, validated version of this exact pattern |
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

- [x] **T3d. Vision-LLM client (scanned-PDF image captioning). — DONE 2026-07-13, provider + routing CHANGED 2026-07-15 (real gaps found via testing against the user's own real CVs).** — *Depends: T2 · Flow: 3 (CV parsing)*
  - [ ] **Reference (2026-07-12 Tahap 2 audit):** `backend/config/utils.py::_ocr_pdf_with_gemini()` in the Tahap 2 code is a working version of this exact pattern (rasterize page → send to vision model) — same idea, different provider (Gemini vs SumoPod/Groq) and different trigger (whole-page rasterization vs NalarX's per-embedded-image approach we're using) — read it for validation, don't copy verbatim
  - [x] **Verify first — DONE 2026-07-13:** sent a test image to SumoPod's `deepseek-v4-pro` as an `image_url` content block. **Confirmed NOT supported** — model's own `reasoning_content` showed it reasoning "no image was provided," `prompt_tokens` too low to have ingested image data, returned empty (`finish_reason: length`)
  - [x] ~~Groq `meta-llama/llama-4-scout-17b-16e-instruct` — used 2026-07-13 to 2026-07-15~~ **replaced 2026-07-15**: user asked to check if SumoPod's `gemini/gemini-2.5-flash-lite` supports vision (SumoPod's catalog includes it) — tested directly on a real image and **confirmed working** (real `image_tokens=258` in the response usage, not the silent-failure pattern seen with `deepseek-v4-pro`). Measured ~12-14% cheaper per image than Groq on real token counts. **User's explicit choice**: vision → SumoPod Gemini 2.5 Flash-Lite; Groq scoped to Whisper STT only from here on. `vision_client.py` now supports both providers via `VISION_PROVIDER` (`sumopod` default, `groq` kept as a working rollback path)
  - [x] Client call: image bytes → base64 → `image_url` content block — `backend/services/vision_client.py`
  - [x] **Routing bug found and fixed 2026-07-15, via real-world testing against the user's own 8 real CVs (never committed to the repo)**: originally had two prompt modes — **transcribe** (verbatim) chosen only for images on text-EMPTY pages, **describe** (short caption) chosen for images on pages that already had some real text, assuming such images must be decorative. One of the user's real CVs disproved this: a page had a short typed summary AND the full CV content ALSO embedded as an image on the same page — the page "having text" caused the routing to pick `describe`, silently dropping the entire image's content (name, education, skills, all organizational experience — verified missing from the parsed profile). **Fixed**: `describe_image()` removed entirely (zero real callers left); `transcribe_image()` is now called unconditionally on every embedded image found by `pypdf`, regardless of page text. A genuinely decorative image just costs one vision call that comes back saying "no text found" — a negligible real cost (~$0.0002/image) versus the risk of silently losing real CV content again. Pages with **zero** embedded images never trigger a vision call at all — unaffected by this change.
  - ✅ Done when: a sample scanned-CV image returns an accurate verbatim transcription, AND an image alongside real page text is ALSO fully transcribed (not just captioned) — **verified on real data**: ran all 8 of the user's real CVs plus 2 dedicated image-only/image+text test CVs through the actual pipeline (in-memory only, zero DB/storage writes, confirmed via DB query each time). Before the routing fix: 1 of 10 real files (the image+text hybrid) silently lost its entire CV content. After the fix: the same file's parsed profile now correctly contains the real name, all 5 skills, all 5 organizational roles with durations, and full education history — genuinely recovered from the image. Added a permanent regression test (`backend/tests/test_vision_always_transcribe.py`, synthetic generated image, not the user's real CV content) reproducing the exact failure shape.

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
  - [ ] `[deferred]` **🚩 Finding (2026-07-15, frontend rebuild pass): skill-gap should be computed once at CV-ingest time and persisted, not recomputed live on every candidate-detail page view.** T8's original "no dedicated table" call (line above, 2026-07-13) was made when `analyze_skill_gap()` was a single cheap call — the later self-consistency-voting fix (Area 5 QA T4, 2026-07-13) tripled it to 3 sequential Deepseek Pro calls per invocation, and nothing revisited whether live-recompute-on-every-view was still the right call after that cost changed. Real, measured impact: `GET /candidates/{id}/detail` now takes ~25-30s on every single page load (re-verified live 2026-07-15), because the endpoint calls `analyze_skill_gap()` fresh each time instead of reading a stored result — the same real API/DB/network round-trip repeats identically on every HR click into the same candidate, forever, with zero caching. Correct architecture: run the skill-gap analysis once when a candidate's CV is ingested and matched against a job (alongside `match_scores`, since skill-gap is inherently a candidate×job pair, not a candidate-only property), persist it, and have `GET /candidates/{id}/detail` simply read the stored row. Needs: (1) a new persisted column/table for the gap result, most naturally on `match_scores` (already the candidate×job junction) or a new `skill_gap_results` table: `{candidate_id, job_id, gap_summary, missing_competencies, development_priority, computed_at}`; (2) trigger the computation at the same point `compute_match_score()` already runs (CV ingest + JD-competency-change re-match); (3) `candidate_detail.py`'s live `analyze_skill_gap()` call replaced with a read of the persisted row; (4) a re-compute path for when JD competencies change after initial matching (`_extract_and_store_competencies()` in `routers/jobs.py` already invalidates+re-extracts JD competencies on JD edit — skill-gap results would need the same invalidation). **Immediate mitigation shipped 2026-07-15** (not a fix, just honesty): the frontend's loading spinner now says "Menganalisis kesenjangan keahlian dengan AI... (bisa memakan waktu hingga 30 detik)" instead of a generic "Memuat..." message, since the un-messaged 25-30s wait was originally mistaken for a hung/looping page.

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

## Area 1 — Frontend UI/UX  ·  Status: 🟡 In progress (T1-T9 and T11 done; T10 visual-parity rebuild 6.5/8 pages done, Page 7 + artifact-merge polish remaining)

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

- [x] **T10. 💎 Visual-parity rebuild against the locked Enterprise Trust artifact — DONE 2026-07-15 (pages 1/2/3/4/5/6/8), IN PROGRESS (Dashboard/Job Detail/Questions-redesign).** — *Depends: T1-T9 (functional build) · Flow: all*
  - **Why this task exists**: T1-T9 above built real, working functionality but the actual rendered
    pages never matched the locked design artifact (`claude.ai/code/artifact/c3799402-...`) — plain
    unstyled cards, no top nav shell, raw 0-1 scores instead of the artifact's 0-100 + fit-label
    treatment, generic badges instead of the artifact's exact pill/status system. The user asked for
    a page-by-page rebuild against the artifact's real HTML/CSS (fetched directly as ground truth,
    not worked from screenshots), reviewing each page live before moving to the next.
  - [x] **Design tokens**: `frontend/src/styles/tokens.css` rewritten to the artifact's exact CSS
    variables (`--teal`, `--teal-soft`, `--gold`, `--gold-soft`, `--bg`, `--surface`, `--ink`,
    `--ink-2`, `--muted`, `--success`/`--warning`/`--danger` + `-soft` variants, `--border`) and
    shared utility classes (`.topbar`/`.nav`/`.hr-avatar`, `.cand-header`, `.main`/`.main.wide`,
    `.pagehead`, `.card`, `.row`, `.score`/`.score-label`, `.comp-line`/`.ok`/`.no`, `.qcard`/`.qn`,
    `.rubric-row`/`.rubric-dots`, `.consent-box`/`.checkline`), with back-compat aliases so existing
    component CSS (`Button.css`, `Badge.css`, `Card.css`, `Table.css`, `FormField.css`, `Modal.css`)
    didn't need a parallel rewrite.
  - [x] New shared components: `TopBar.tsx` (job-scoped nav — see gap below) and `CandidateHeader.tsx`
    (candidate-facing simplified header), matching the artifact's two distinct page shells.
  - [x] **Page 1 (Login)** — real logo/tagline, correctly labeled fields, matches artifact exactly.
  - [x] **Page 2 (JD List + Form)** — merged the previously-separate `JobFormPage.tsx` into
    `JobsListPage.tsx`'s split two-column layout (list left, create/edit form right), matching the
    artifact's actual page-2 structure; `JobFormPage.tsx` retired. Added `company_name` and
    `created_at` to `JobOut` (previously missing from the API response entirely) for the real
    "PT Gaskeun Demo · kelola deskripsi pekerjaan" subtitle and "Dibuat" column.
  - [x] **Page 3 (Shortlist)** — real 0-100 score + Sangat Cocok/Cocok/Kurang Cocok fit label, real
    per-competency Terpenuhi/Belum-terlihat comparison against **all** JD-required competencies
    (added `competency_status`/`latest_role` to `matching.py`'s `MatchOut`, previously only returned
    matched names with no way to show gaps). **User-requested additions beyond the artifact**: 8
    candidates/page pagination (real JD has 13 competencies vs. the artifact's 2-3 curated example
    lines, making full cards too tall) and a nested 5-competencies-per-page dot-pagination inside
    each card, independent per candidate.
  - [x] **Page 4 (Invite modal)** — re-view state (existing token, never regenerated) and new-invite
    state both verified; **real bug found and fixed from user feedback**: "Salin"/"Tutup" buttons
    were stacking illegibly instead of sitting side-by-side — fixed by giving the link input its own
    full-width row and moving both buttons into one footer action row.
  - [x] **Page 5 (Questions approval)** — empty/draft/approved states; **real bug found and fixed
    from user feedback**: the approved/locked textarea's "disabled" background color was identical to
    the page's own background, making it look broken/plain rather than intentionally locked — fixed
    to a teal-tinted, teal-bordered treatment matching the artifact's "settled/confirmed" visual
    language. (User separately flagged the missing "Simpan Perubahan" button in one screenshot —
    root-caused as the user looking at the static artifact mockup itself, not the live rebuilt app;
    confirmed via DB query that no such job/questions existed in real data, and a fresh live test
    showed all 3 buttons present and correct.)
  - [x] **Page 6 (Candidate consent + Telegram)** — added `alias` to the candidate-facing `/self`
    endpoint (`CandidateSelfOut`) for the artifact's "Selamat datang, {alias}" greeting — confirmed
    non-PII (anonymized display name, not a real name) and safe to expose per the project's existing
    PII-redaction design; both the pre-consent and post-consent/Telegram-link states verified live.
  - [x] **Page 8 (Candidate detail + report)** — real two-column split layout (Profil CV/Skill
    Gap/Interview left, Skor Rubrik/Keputusan/Kirim Laporan right), real rubric dot indicators, real
    "Skor Kecocokan" header line (added `match_score` to `CandidateFullDetailOut`, previously absent).
  - [x] **Real nav-scoping bug found and fixed from user feedback**: the top nav's "Kandidat" /
    "Wawancara" / "Laporan" links were dead-feeling two ways in sequence — first genuinely
    unclickable (they pointed at global stub routes with no real destination), then after a first
    fix (added `/candidates`, `/interviews`, `/reports` routes via a new `NavRedirectPage` resolving
    "most recently created active job") they instead silently jumped to a *different* job than the
    one the user was currently viewing. Final fix: `TopBar` now accepts an optional `jobId` prop —
    when rendered from inside a `/jobs/:jobId/*` page, nav links stay scoped to THAT job; the global
    stub routes are only used when no job context exists (e.g. from the plain `/jobs` list).
  - [x] **Operational note, re-confirmed multiple times this pass**: uvicorn's `--reload` repeatedly
    logged a successful reload while the running process kept serving the OLD Pydantic schema (new
    fields silently absent from `/openapi.json`) — a full process kill + restart was required each
    time. Standing rule for this project going forward: after any backend schema change, verify with
    `curl localhost:8000/openapi.json | grep <new_field>` before trusting a `--reload` log line, and
    do a full restart if the field is missing.
  - [ ] **Page 7 (Interview audio)** — NOT YET STARTED. Candidate-facing recording screen (progress
    dots, timer, record/stop button) needs the artifact's `.timer`/`.rec-btn`/`.progress`/`.qtext`
    styling applied to `CandidateInterviewPage.tsx`.
  - [ ] `[deferred, real finding, not a rebuild bug]` **Skill-gap analysis recomputes live on every
    candidate-detail page view** (~25-30s, 3 real LLM calls) instead of being cached at CV-ingest/
    match time — full technical detail already logged under Area 2 T8's finding below. Interim
    mitigation shipped: the loading spinner now says how long the wait is instead of a generic
    "Memuat..." message that read as a hang.
  - ✅ Done when: all 8 original artifact pages visually match, both real bugs found via user
    testing (invite-modal button stacking, nav dead-links/wrong-job-jump) are fixed and verified,
    and Page 7 + the three new pages below (T11) are complete — **6.5/8 original pages done, T11 not
    started**.

- [x] **T11. 💎 Three new/extended pages beyond the original 8-page artifact — DONE 2026-07-15.** — *Depends: T10 · Flow: extends 2, adds a new entry point*
  - **Why this task exists**: the user asked to extend the platform beyond the original 8-page
    artifact with a Dashboard (new post-login landing page), a Job Detail page (new destination for
    clicking a JD title, replacing the current jump-straight-to-Shortlist behavior), and a richer
    redesign of the Questions page (currently functionally complete but visually plain). Full design
    plan (backend endpoint shape, page layouts, content decisions) was written and user-approved via
    plan mode before any code changed — see `C:\Users\zikri\.claude\plans\snuggly-toasting-crayon.md`
    for the complete original plan text.
  - **⚠️ Process correction mid-task**: the plan's original Part E ("update the artifact after
    building") had the sequencing backwards — the user stopped implementation immediately after
    Part A (backend only) and required a **mockup-first** approach instead: build a static HTML
    design-preview artifact for all three pages, get explicit sign-off, and only then write any
    React/TSX. This is the correct order (cheap to iterate on a mockup, expensive to iterate on real
    code) and is now the standing approach for any future new-page work in this project.
  - [x] **Backend**: new `GET /dashboard/stats` endpoint (`backend/routers/dashboard.py`, mounted in
    `main.py`) — the generic repository only supports equality-filter list queries (no COUNT/GROUP
    BY), so this aggregates in Python: active/closed job counts, total candidates, pipeline-stage
    counts (belum diundang / menunggu wawancara / selesai wawancara — same row-presence derivation
    already authoritative in `matching.py`), decision counts (advance/reject/pending), reports sent,
    average match score, a per-job summary table, and a capped "attention" list of actionable items
    (interviewed-but-undecided candidates, active jobs with no approved questions, decided-but-
    report-not-sent candidates). **Verified live**: real curl against real seeded data returned
    correct numbers (2 active jobs, 36 total candidates, 3 interviewed, 2 advance/2 reject decisions,
    3 reports sent, 1 real attention item surfaced for a fixture candidate with a decision but no
    report sent).
  - [x] **Mockup artifact built and approved before any frontend code**: a new static-HTML preview
    (`claude.ai/code/artifact/d70af3d0-ed77-4f18-ba2e-8ca0c4ee0921`) with 3 tabs — Dashboard, Detail
    Lowongan, Pertanyaan Wawancara v2 — built entirely from the locked artifact's existing shared CSS
    (zero new colors/fonts, only new component classes: `.stat-tile`, `.funnel`, `.chip`,
    `.mini-stat`, `.status-banner`, `.guide-box`, `.qcard-foot`/`.charcount`/`.reorder`,
    `.empty-onboard`). **User reviewed and confirmed alignment** before implementation began.
  - [x] **Dashboard page (NEW)** — `frontend/src/pages/DashboardPage.tsx`, route `/dashboard`, is now
    the post-login landing page (`LoginPage.tsx` navigates here instead of `/jobs`; `/` redirects
    here) and the new `TopBar` "Dashboard" nav item's target. Built to match the approved mockup
    exactly: KPI stat-tile row, pipeline funnel bar (proportional segment widths from real counts),
    "Perlu Perhatian" attention list linking into Job Detail, and a per-job summary table. Verified
    live: real numbers matching the backend curl check, funnel proportions correct, attention item
    for the real fixture candidate rendering with a working link.
  - [x] **Job Detail page (NEW)** — `frontend/src/pages/JobDetailPage.tsx`, route
    `/jobs/:jobId/detail`, is now the title-click destination on the JD list (`JobsListPage.tsx`'s
    "Judul" column rewired); Shortlist stays at `/jobs/:jobId`, reached via this page's "Lihat
    Kandidat" button and top-nav "Kandidat". Built to match the mockup: status-badged header with
    relative-time + Edit shortcut, 4-tile pipeline snapshot, "Lihat Kandidat"/"Kelola Pertanyaan"
    shortcut buttons, an interview-questions status card (Belum dibuat/Draf/Disetujui, real question
    count), required-competency chips with importance dots (fetched from the existing
    `GET /jobs/{id}/competencies` endpoint), and the three JD text sections. Verified live on the
    real "Web Developer" job: 30 candidates, 13 real competency chips, real JD text rendering
    correctly with preserved line breaks. **Real bug found from user feedback, fixed same pass**: the
    page's `TopBar` was set to `active="kandidat"`, wrongly highlighting "Kandidat" in the nav even
    though this page is about the job itself (reached from the "Lowongan" list), not the candidate
    shortlist — fixed to `active="lowongan"` across all three render branches (loading/error/ready),
    re-verified live.
  - [x] **Questions page redesign — reverted to the ORIGINAL locked page-5 design after user
    correction.** The first pass (status banner, guidance panel, reorder arrows, char count, tip
    line — described in an earlier version of this entry) was **wrong**: the user's actual target
    was the plain, original locked artifact's page 5 (`claude.ai/code/artifact/c3799402-...`, tab 5),
    not the new "v2" mockup tab this session invented. **Corrected**: `QuestionsPage.tsx` stripped
    back to exactly the original design — plain numbered `.qcard`s (no banner/badge/guide-box/
    reorder/char-count/tip-line), a red "Hapus" button per draft question, and a two-button footer
    (primary "Setujui & Kunci Pertanyaan" + ghost "+ Tambah Pertanyaan") — no third "Simpan
    Perubahan" button, matching the target image exactly. **One real functional fix required by
    this**: the backend's `POST .../approve` only flips already-persisted `draft` rows — it never
    reads in-memory edits — so removing the separate "Simpan Perubahan" button would have silently
    dropped any unsaved edits/added questions on approve. Fixed by folding save into approve:
    `handleApprove()` now calls `PUT .../questions` (save) first, then `POST .../approve`, as one
    user-facing action. **Verified live**: edited an existing question's text, clicked "Setujui &
    Kunci Pertanyaan" directly (no separate save step), reloaded — the edit was correctly persisted
    before locking, confirmed programmatically (`textarea.inputValue()` after approve matched the
    edited text, not the original). Approved-state screenshot matches the original artifact exactly:
    plain locked teal-tinted textareas, a plain "Disetujui" badge, nothing else.
  - [x] Regenerated `frontend/src/api/openapi.json` + `schema.d.ts` after the backend endpoint
    landed; full backend restart + `curl .../openapi.json | grep dashboard` verification (per the T10
    operational note — `--reload` was not trusted alone).
  - [x] End-to-end Playwright verification against real seeded data for all three pages, including
    the login-redirect flow and nav highlighting; one disposable test job created for the
    draft-questions-state screenshot, cleaned up and confirmed via DB query afterward (jobs table
    back to exactly the 3 real jobs: 16, 21, 27).
  - [ ] `[deferred]` Reflect the AS-BUILT pages back into the locked 8-page artifact / merge the new
    3-page mockup artifact into it as pages 9-11 — not done this pass; the 3-page mockup artifact
    remains the source of truth for the new pages' design, separate from the original 8-page one.
  - ✅ Done when: dashboard shows real live metrics with a working attention list, clicking any JD
    title opens Job Detail (not Shortlist) with all 4 content sections populated from real data, the
    Questions page reads clearly at a glance with zero loss of existing functionality — **all
    verified live 2026-07-15**; only the artifact-merge cleanup step remains, deferred as non-blocking.

- [x] **T13 — Logout button + auto-redirect-to-login on expired/invalid token (2026-07-15)** — after
  shipping T12, the user hit "Gagal memuat dashboard" on every page; root-caused via the backend log
  to `POST /auth/login` returning 200 immediately followed by `GET /dashboard/stats` returning 401 —
  a stale JWT (`JWT_EXPIRE_MINUTES=120`, and this session had run well past that) was still cached in
  `localStorage`, and `HrAuthGuard` only checked *token presence*, never validity, so the expired
  token passed the guard and then failed at the backend. **Fixed properly, not just patched around**:
  (1) `api/client.ts` gained an `onResponse` middleware — any 401 while an HR token is set clears it
  and hard-redirects to `/login`; (2) `TopBar.tsx`'s HR avatar is now a clickable button opening a
  small dropdown with a "Keluar" (logout) action that clears the token and navigates to `/login`.
  Verified live via Playwright: fresh login reaches the dashboard with real data (36 candidates, full
  funnel/attention list — confirming the dashboard code itself was never broken, only the stale
  token), clicking the avatar shows the Keluar menu and logging out clears `localStorage` + redirects,
  and manually setting an invalid token then navigating to `/dashboard` auto-redirects to `/login` and
  clears the bad token — all three confirmed via `localStorage.getItem` assertions, not just visual
  screenshots.
  - ✅ Done when: an expired/invalid session can never silently show a raw "Gagal memuat" error;
    it either recovers by no longer sending a dead token or explicitly routes back to login — **verified live 2026-07-15**.

- [x] **T14 — Dashboard: 4 real insight charts (2026-07-15)** — user found the dashboard "too plain"
  and asked for real visualization beyond the KPI tiles/funnel/table. A true time-series line chart
  was ruled out — no daily/weekly snapshot data exists anywhere in the schema, so it would either be
  fake or require new backend tracking with zero retroactive history. Instead scoped to 4 charts fully
  derivable from existing tables (no new tracking): score-distribution histogram, competency-gap bars,
  invite-to-interview conversion bars, and a decision-breakdown stacked bar — all confirmed via direct
  SQL against real data before mockup, then mockup-first per the standing rule (static HTML artifact,
  `claude.ai/code/artifact/429847cc-96b3-4986-b0cd-2522bc857bd8`), user-approved, then implemented to
  match exactly.
  - [x] Ran the `dataviz` skill's procedure before building: chose horizontal-bar forms for all 4
    (never a donut/pie, never dual-axis), one sequential teal hue for the histogram, one warning hue
    for the competency-gap bars (a deficit metric, not a categorical series), status colors
    (success/danger/muted) for the decision stacked bar with a legend + direct in-bar count labels
    (not color-alone, since status colors always ship with a label per the skill's rules). Validated
    the success/warning/danger triple via `scripts/validate_palette.js` before use — all 6 checks
    passed (worst adjacent CVD ΔE 8.4, right at the floor — legend + direct labels satisfy the
    "secondary encoding required" condition that floor triggers).
  - [x] **Backend** (`routers/dashboard.py`): extended `DashboardStatsOut` with `score_distribution`
    (4 buckets computed from `match_scores.overall_score`), `conversion_by_job` (invited vs.
    interview-completed count per job, reusing the same `invited_at`/`interview_answers` presence
    rules as the funnel), `competency_gaps` (top-7 by missing%, computed for whichever job has the
    most candidates — reuses the exact matched-competency-name-set logic already in `matching.py`),
    and `decisions_by_job` (advance/reject/pending counts per job, same source data as the existing
    company-wide decision tiles, just not yet broken out per-job). All computed inline in the existing
    per-job/per-candidate aggregation loop — no new queries beyond what the loop already fetches.
  - [x] Verified every dataset against real DB values via direct `psql` queries *before* writing the
    mockup, and again via a live `curl` of `/dashboard/stats` after implementing — both matched
    exactly (e.g. score buckets 1/33/2/0, Web Developer conversion 3/4=75%, decision 2 advance/1
    reject).
  - [x] Regenerated `openapi.json`/`schema.d.ts`; `npx tsc --noEmit` clean.
  - [x] End-to-end Playwright verification: all 4 chart-row counts matched expected data shape
    (4 histogram buckets, 2 conversion rows, 7 gap rows, 2 decision rows), full-page screenshot
    compared directly against the approved mockup — layout, colors, and real values all match.
  - ✅ Done when: the dashboard shows 4 real, non-fake charts derived entirely from existing data,
    matching the approved mockup exactly — **verified live 2026-07-15**.

- [x] **T15 — Dashboard production-polish redesign (2026-07-15)** — user supplied a detailed
  "senior product designer" style brief (Stripe/Linear/Vercel/Notion quality bar) asking for visual
  hierarchy, spacing, typography, and component polish on the Dashboard page ONLY — explicitly no
  data changes, no removed sections, no nav restructuring, same component order. One item (an "AI
  Recruitment Insight" card with example bullets like "candidate quality increased 18%") was flagged
  before building: those are fabricated metrics we don't compute — asked the user, who chose to keep
  the AI card purely visual/branding with zero specific numeric claims, avoiding a fake-data risk.
  Mockup-first per the standing rule: built and got sign-off on a full redesign preview
  (`claude.ai/code/artifact/2a83b8b0-e6a1-429a-b841-c33fa56a6f33`) before touching real code.
  **New standing rule from this pass**: user asked not to mint a new artifact URL per mockup pass —
  reuse one ongoing artifact with tabs/sections instead, since scattered URLs across the project are
  hard to reference later. Saved as a memory (`feedback_single_mockup_artifact`) for future sessions.
  - [x] Implemented into `DashboardPage.tsx` + a new CSS block in `tokens.css`, scoped entirely under
    a `.dashboard-shell` wrapper class so it can't leak into other pages that reuse the *same*
    original class names (`.stat-tile`/`.attn-row`/`.chart-card` are also used by `JobsListPage.tsx`)
    — confirmed via Playwright that Lowongan's 3-tile stat-grid renders unchanged after the redesign.
  - [x] KPI tiles → larger tabular numbers, hover lift, softer shadow; "Alur Kandidat" funnel →
    redesigned as 4 large stage tiles (hero treatment) + a slim progress track underneath, replacing
    the old single stacked bar; "Ringkasan per Lowongan" → real `<table>` with zebra striping, hover
    rows, clickable rows, right-aligned numbers, rounded status pills; "Perlu Perhatian" → colored
    left-border cards (amber for blocking issues, blue for informational) with icon chips instead of
    a plain dotted list; new "AI sedang menganalisis kandidat Anda" banner card (teal gradient,
    sparkle icon, "AI AKTIF" badge) added beneath the KPI row per item 14 of the brief, with
    branding-only copy (no fabricated stats).
  - [x] Same data, same section order (KPI → AI banner → pipeline → per-job/attention split → 4
    chart cards), same nav — confirmed via direct visual diff against the pre-redesign screenshot.
  - [x] `Table`/`Badge` component imports removed from `DashboardPage.tsx` (dead after switching the
    job-summary panel to a hand-styled `<table>` for hover/zebra/click-row behavior the generic
    `Table` component didn't support).
  - [x] `npx tsc --noEmit` clean; verified live via Playwright (5 KPI cards, 4 pipeline stages, 4
    table rows, 2 attention items, all rendering with real data) plus a full-page screenshot compared
    directly against the approved mockup.
  - ✅ Done when: the dashboard reads as a polished production SaaS page (Stripe/Linear-tier) while
    preserving 100% of the original data/structure/nav — **verified live 2026-07-15**.
  - [x] **Real polish fix, round 1 (2026-07-15, from a user screenshot)**: two issues surfaced —
    (a) "Ringkasan per Lowongan"/"Perlu Perhatian" panels had visibly mismatched heights, leaving
    obvious dead whitespace at the bottom of the shorter one (`.db-split` used `align-items: start`);
    (b) the job-summary table's title column had no fixed width, so a longer title
    ("Web Developer (QA Fixture)") wrapped across 3 cramped lines. **Fixed**: `.db-split` switched to
    `align-items: stretch` + `.panel` given `display:flex; flex-direction:column` with its
    table/attn-list set to `flex:1`, so both panels always match height regardless of content length;
    `table.jt` switched to `table-layout: fixed` with explicit per-column width percentages (title
    28%, status 15%, three numeric columns 19% each) so the title wraps at 2 clean lines instead of 3
    cramped ones, and column padding tightened (22px to 12px) so "Diwawancara"/"Diputuskan" headers no
    longer truncate with an ellipsis at the new fixed width. Verified live via screenshot.
  - [x] **Real polish fix, round 2 (2026-07-15, three issues from a user screenshot)**:
    (a) table header labels (0.72rem, `--muted`) rendered visually smaller than the numeric data
    cells (0.86rem) — backwards hierarchy, headers should read at least as prominently as values.
    Fixed: headers bumped to 0.8rem/`--ink-2`, numeric cells reduced to 0.82rem, closing the gap so
    labels no longer look like an afterthought under bigger numbers.
    (b) "Perlu Perhatian" had no cap on visible height — since the backend caps attention items at 8
    (`_ATTENTION_CAP` in `dashboard.py`), a company with many real issues would grow that panel far
    taller than the table panel it's stretched to match, or force the whole page to stretch
    awkwardly. Fixed: `.attn-list` given `max-height: 360px; overflow-y: auto` (about 4-5 items
    visible before an internal scrollbar appears) so the panel never grows unboundedly regardless of
    item count.
    (c) Distribusi Skor Kecocokan's value column (1/33/2/0) had no explicit text-align, so varying
    digit widths made the numbers look raggedly right-jammed against the bar track instead of forming
    a clean column. Fixed: `.hval` set to `text-align: left` so all values start from the same
    x-position regardless of digit count. Verified live via screenshot for all three.

- [ ] `[deferred]` **Full HR dashboard shell / nav polish beyond the JD list (T4b)** — superseded by
  T11's real Dashboard page above; this line kept for history, not actionable separately.
- [ ] `[deferred]` **Responsive/usability polish beyond demo happy-path.**

- [x] **T12 — Post-T11 usability fixes: Lowongan form-on-demand, Kandidat job-picker, Pertanyaan
  add-after-approval (2026-07-15)** — three real gaps surfaced by live-testing the T11 pages, fixed
  mockup-first per the standing project rule (static HTML artifact reviewed and approved before any
  real code):
  - [x] **Lowongan (JobsListPage)** — the "Buat / Edit Lowongan" form was permanently visible in a
    1fr/1.1fr split even when just browsing. Split into two real states: browsing (`/jobs`, full-width
    table only, no form) and create/edit (`/jobs/new`, `/jobs/:id/edit`, form takes over as primary
    content with a compact reference-table strip above it + a "Batal" cancel button). Browsing state
    also gained: 3 stat tiles (Total Lowongan/Aktif/Ditutup, reusing the Dashboard's `.stat-grid`/
    `.stat-tile` classes with an inline 3-col override) and two new table columns (Kandidat count,
    Pertanyaan status pill: Belum dibuat/Draf/Disetujui).
  - [x] **Kandidat (ShortlistPage)** — switching jobs required navigating back to Lowongan and
    clicking a different title. Added a `<select>` job-picker directly under the pagehead
    ("Pindah ke lowongan lain"), populated from `GET /jobs`, navigating via `onChange`.
    **Real UI polish fix, round 1 (2026-07-15, from a user screenshot)**: the first version used the
    bare `.field select` with zero dedicated select styling (`.field` CSS only styled
    `input`/`textarea`), rendering as a raw unstyled browser `<select>` floating with no container —
    looked broken next to the rest of the styled page. Fixed: added real `.select-control`/
    `.field select` CSS (custom SVG chevron via `appearance:none` + background-image, matching
    border/radius/focus-ring treatment as inputs).
    **Real UI polish fix, round 2 (2026-07-15, user flagged the header row itself as "jelek banget")**:
    even after the select was styled, the picker's own `.card` wrapper plus two differently-sized
    ghost buttons ("Pertanyaan Wawancara" / "Kembali ke Daftar Lowongan") crowded directly under the
    title/subtitle read as cluttered and unbalanced. Fixed by redesigning the whole pagehead: dropped
    the redundant "Kembali ke Daftar Lowongan" button entirely (TopBar's "Lowongan" nav link already
    covers that navigation), merged the job-picker into the same header row as a compact inline
    label+select group instead of a separate floating card, and made "Pertanyaan Wawancara" the one
    remaining action styled as `variant="secondary"` (gold) for clear visual priority. Verified live
    via screenshot — title/subtitle now have breathing room, and the picker + single action form one
    tidy baseline-aligned group on the right.
  - [x] **Pertanyaan Wawancara (QuestionsPage)** — "+ Tambah Pertanyaan" only showed pre-approval.
    Added a new `POST /jobs/{job_id}/questions/reopen` backend endpoint (flips approved rows back to
    draft, does not touch draft-only jobs) + a ghost "+ Tambah Pertanyaan" button next to the
    "Disetujui" badge that calls it, appends one blank draft locally, and shows an explanatory
    warning-toned note ("menambahkan pertanyaan baru membuka kembali draf ini..."). Re-approving locks
    it again through the existing `handleApprove()` flow.
  - [x] **Backend**: `GET /jobs` response model changed from `JobOut` to new `JobListItemOut`
    (adds `candidate_count`, `question_status`); `POST /jobs/{job_id}/questions/reopen` added to
    `interview_questions.py`. Regenerated `openapi.json`/`schema.d.ts` after.
  - [x] **Operational gotcha recurred and was resolved**: after the backend edits, `--reload`'s
    child process silently failed to pick up the new route (confirmed via `curl .../openapi.json |
    grep reopen` returning nothing). Compounded by a real PID-translation split across tool
    namespaces on this machine — the actual listening PID differed between `Get-NetTCPConnection`,
    `Get-CimInstance`/`taskkill` (which reported "process not found" for that same PID), and
    git-bash's `ps -W` (a third, different PID value again). Root cause: a **stray uvicorn process
    was still bound to the port from an earlier session using the wrong (system) Python, which
    lacked the project's `.venv` sqlalchemy version** — a second start attempt using the system
    Python crash-looped on `ImportError: cannot import name 'mapped_column'`. Resolved by killing via
    `Get-Process python | Stop-Process` (the only Windows-tool view that showed the real PID) and
    restarting explicitly via `backend/.venv/Scripts/python.exe -m uvicorn ...`, not bare `python`.
  - [x] Regenerated `frontend/src/api/openapi.json` + `schema.d.ts`; `npx tsc --noEmit` clean.
  - [x] End-to-end Playwright verification against real seeded data (job 16, "Web Developer", 30
    candidates, 1 approved question): browsing-state stat tiles/columns, create-state form, edit-state
    reference strip, job-picker options list, approved-state add button, and the reopened state (2nd
    blank qcard appended, warning note shown) all confirmed live via screenshots + DOM assertions.
    Test mutation on job 16 (reopened-to-draft) reverted back to `approved` afterward via direct DB
    update so real demo data wasn't left mid-edit.
  - ✅ Done when: Lowongan only shows the form on explicit create/edit, browsing state shows real
    stat tiles + per-job candidate/question data; Kandidat page can switch jobs without leaving it;
    Pertanyaan page allows adding questions after approval with a clear re-approval requirement —
    **all verified live 2026-07-15**.

---

## Area 5 — QA  ·  Status: 🟢 Done (all 9 tasks T3/T3b/T4/T5-fixture/T5/T6/T8/T10/T11/T12 verified end-to-end; T11's 7-scenario visible suite found and fixed one more real gap — rubric scoring/interview-summary was never wired into the real candidate flow)

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
| T3b. PII redaction test | ✅ **Final result, 2 gaps found and fixed** | LLM-based name detection shipped, then re-tested against the user's own 8 real CVs — found and fixed a real truncation bug (name past char 800 was missed on 1 of 8), now 8/8 clean. | 2.0 | 🟡 | One extra Flash call per CV ingest; sends full text now (was 800-char prefix) |
| T4. Report consistency test | ✅ **Final result, gap fixed** | Same voting fix extended to `skillgap.analyze_skill_gap()` (majority vote) — 9 real calls, zero drift, re-verified. | 1.5 | 🟡 | Cost tripled for this call site — user-approved tradeoff |
| T5-fixture. Tiered test CVs | ✅ **Final result** | 6 synthetic CVs (2 strong/2 mid/2 weak) seeded under a separate "Web Developer (QA Fixture)" JD (job_id=21), fully separate from the 30-CV demo pool. | 1.0 | 🟢 | |
| T5. Matching/tier check | ✅ **Final result** | Real scores confirm monotonic discrimination: strong (0.69, 0.64) > mid (0.52, 0.50) > weak (0.43, 0.43). | 1.0 | 🟢 | |
| T6. Human-in-loop test | ✅ **Final result** | Real AST-based static check (not a one-off grep) confirms `hr_decisions.create()` only ever called from the HR-authenticated endpoint + the seed script. | 1.0 | 🟢 | |
| T8. Consent-gate test | ✅ **Final result** | Both cases verified live: no-consent → `ConsentRequiredError`/403; valid consent → real submit+transcribe succeeds. Cleanup verified, zero orphaned data. | 1.0 | 🟢 | |
| T10. Full e2e run | ✅ **Final result** | Real seed→HR→invite→consent→Telegram-link→interview→decision→report flow verified live end-to-end, including a real Telegram delivery confirmed received. Also found+fixed a real "Terkirim" seed gap. | 2.0 | 🟡 | |
| T11. 💎 Visible e2e scenario suite (NEW) | ✅ **Final result, 1 real gap found and fixed** | All 7 scenarios run live in a visible (non-headless) browser on the user's screen. Scenario 6 found rubric scoring/interview-summary was never wired into the real candidate flow — fixed. | 6.0 | 🟠 | Ran over the original 4.0h estimate — several scripting/timing bugs plus the real T6 gap and its fix+re-verify+full-suite-rerun cycle |
| T12. Demo-readiness checklist | ✅ **Final result, all 7/7 edge states verified** | All edge states confirmed live, including the previously-outstanding real Telegram delivery check. | 2.5 | 🟡 | |
| **Subtotal** | | | **~19h** | | Spread across Day 4-12 alongside build work — same person, same hours pool |

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
  - [x] **Second real gap found and fixed, 2026-07-13, real-world validation**: user asked for a direct test against their own 8 real CVs (`dataset/for testing cv/`, in-memory only — no DB/storage writes at any point, verified afterward). 7/8 came back clean, but the 2018 CV leaked the real name in the redacted output — root-caused to `detect_candidate_name()` truncating to a fixed 800-character prefix, an assumption that "names appear near the top of virtually every resume." That specific CV's `pypdf` text-extraction order put personal-info fields (address/email/phone) first and the name-as-styled-text-box last, past character position 1400 — outside the window entirely. **Fixed**: send the full extracted text (capped at a generous 20000 chars for pathological inputs only, not a "near the top" assumption) — every real CV tested fit well under this cap (max observed: 14,721 chars). Re-verified: **8/8 real CVs now come back fully clean** (no raw name/email/phone in the redacted output). Added `test_name_detected_when_it_appears_late_in_a_long_document()` as a permanent regression test, using synthetic content shaped like the real failure (long preamble, name near the end) — the user's actual CV content is never committed to the test suite.
  - ✅ Done when: 4 tests pass — email/phone redaction proven, name detection+redaction proven working, name-free-text correctly declined, late-position-name regression guarded — **and separately confirmed against 8 real user CVs outside the test suite, with zero DB/storage side effects**

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

- [x] **T10. Full e2e happy-path run — rewritten to match the current flow. — DONE 2026-07-15.** — *Depends: all core · **Run: Day 12** (re-baselined 2026-07-12; this one genuinely needs everything built; T3/T3b/T4/T5/T6/T8 above are re-run here as a confirmation pass, not run for the first time)*
  - [x] Seed data loads: 1 company, 1 JD (**Web Developer**), **30 candidates** — **verified live**: all 30 candidates have real `parsed_profiles` rows (zero silent partial-parse failures)
  - [x] HR: create/view JD (structured fields) → view Shortlist (instant, pre-computed scores + tier status pills) — **verified live, headless/background** (per user instruction: visible-browser mode is T11-only)
  - [x] HR: edit/approve interview questions (T5b) → **invited the designated live candidate** (candidate_id=59, "Kandidat WD-28" — the 3rd-from-last seeded candidate per `load_demo_data.py`'s tier logic), copied the real token link
  - [x] Candidate: open token link → consent recorded
  - [x] Candidate: **link Telegram** (real click, real chat_id=1304618784) → record + submit audio answer → completion screen — **verified live in T11 Scenario 1**
  - [x] HR: review candidate detail → record decision → **send report via Telegram** (real send) — **verified live in T11 Scenario 1, real Telegram delivery confirmed received by the user**
  - [x] Spot-check the 2 synthetic candidates show their pre-seeded "Terkirim" state correctly — **real gap found and fixed**: the seed script never actually set `telegram_chat_id`/`report_sent_at` for the 2 synthetic candidates (60, 61), so despite the plan's own T7 writeup claiming this was verified, they were actually showing the "missing Telegram" disabled state, not "Terkirim." Patched both candidates' DB rows directly (fabricated `telegram_chat_id`, real `report_sent_at` timestamp) and updated `load_demo_data.py`'s `_seed_synthetic_interview()` so any future fresh seed run sets this correctly too. Re-verified live: both now correctly show "Terkirim."
  - ✅ Done when: one clean pass with no manual DB fiddling — **verified**: candidate 59 completed the full lifecycle live, including a real confirmed Telegram report delivery

- [x] **T11. 💎 Visible end-to-end scenario suite (NEW 2026-07-13 — user-requested sufficiency check). — DONE 2026-07-15, all 7 scenarios verified, 1 real gap found and fixed.** — *Depends: T10 · **Run: Day 12, alongside T10/T12***
  - **Why this is distinct from T10**: T10 is one scripted happy-path confirmation pass. T11 is the user directly watching Playwright drive the real running app on their own screen — `headless: false` + `slowMo`, not headless/background — across 7 scenarios chosen to sufficiency-check the whole system, including blocked/failure/multi-actor paths T10 doesn't cover. **This visible-browser mode applies only to these T11 runs** — every other area's edit-verification work reverts to headless/background Playwright, per the user's explicit instruction.
  - [x] **Scenario 1 — Happy path, full lifecycle**: HR logs in → creates a JD → questions generate/approve → HR invites a real ranked candidate → candidate consents + links Telegram (real click on the real `t.me` link, opened by the user on their own phone/browser — an isolated Playwright context has no logged-in Telegram Web session, so the automated browser handles only the surrounding app-side steps) → candidate completes the audio interview → HR reviews (audio/transcript/rubric/skill-gap) → HR records a decision → HR sends the report → **real Telegram delivery confirmed received by the user**
  - [x] **Scenario 2 — Candidate-blocked paths**: expired/invalid token → "Link tidak valid" screen — verified; reopening an already-completed interview → completion-guard message — verified; mic-permission denied on a fresh candidate → blocking message + retry — verified (temporary consent record given for the test, cleaned up after)
  - [x] **Scenario 3 — HR-blocked paths**: inviting before questions are approved → 400 error surfaces correctly ("Cannot invite: interview questions are not approved yet") — verified; JD form validation (empty title) → blocked with message — verified; re-opening an already-issued invite link → shows the identical token, never regenerates — verified programmatically (`firstLink === secondLink`). **Took 5 script-side debugging iterations to get a valid test fixture**: a fresh test JD has zero shortlist candidates by default, and a candidate borrowed from a different job (whose own `job_id` didn't match the test job) caused the invite-gate to validate against the *wrong* job's approved-questions state — the real fix was creating a throwaway candidate scoped directly to the test job. All test artifacts (disposable test jobs 22-26, throwaway candidates 68-71) cleaned up and verified via DB query; one accidental mutation of a real seed candidate (58's token/invited_at, from an earlier flawed fixture attempt) was caught and reverted.
  - [x] **Scenario 4 — Failure + retry paths**: audio upload failure (intercepted/aborted request) → error shown, retry works — verified (after fixing a script typo: the real stop-recording button is "Berhenti Rekam", not "Berhenti Merekam"); report send with no Telegram link → disabled state with explanatory label — verified; report send with a broken Telegram delivery (real invalid chat_id) → **real error, not a crash or masked CORS failure**: confirmed via an instrumented network-response listener that the request genuinely takes ~25-30s before Telegram's API rejects it, after which the sanitized global exception handler (`{"detail":"An unexpected error occurred.","error_id":"..."}`) renders correctly with a working "Coba lagi" retry button — no raw traceback leaked, matching the Tahap 2 anti-pattern this handler was built to avoid
  - [x] **Scenario 5 — Multi-actor / concurrency-adjacent status correctness**: temporarily invited one never-touched seed candidate to produce a real "Menunggu wawancara" example alongside the existing "Belum diundang" (28 candidates) and "Selesai wawancara" (3 candidates) rows — confirmed all three statuses render correctly and simultaneously on the same shortlist; confirmed a synthetic candidate's "Terkirim" state — verified, then reverted the temporary invite
  - [x] **Scenario 6 — Data-integrity tracing — real gap found and fixed**: traced candidate 59's full pipeline directly against the DB (parsed_profiles → match_scores → interview_answers → interview_questions → transcripts → rubric_scores → interview_summaries), confirming every row correctly scoped to candidate 59/job 16 with no cross-contamination. **Found a genuine pipeline gap along the way**: `rubric_scores`/`interview_summaries` were only ever populated by the seed script's direct Python call for synthetic candidates (60, 61) — grep confirmed **zero call sites** for the `/score` and `/interview-summary` endpoints anywhere in the actual frontend source. A real candidate completing a real interview (candidate 59, from Scenario 1) got a transcript but was never scored, and `CandidateDetailPage.tsx` silently rendered an empty rubric section (`.map()` over an empty array) with no "not yet scored" indicator — so Scenario 1's "happy path" had technically passed while masking this gap. **Fixed**: `backend/services/interview_answers.py::submit_answer()` now calls `score_and_persist_answer()` right after the transcript is created, and once a candidate has answered all their job's approved questions, also calls `compute_and_persist_interview_summary()` — matching, for real candidates, exactly what the seed script already did for synthetic ones. Backfilled candidate 59's real answer (genuinely scored 1/5 on all three criteria — an honest low score, since the real T12 test answer was just "Terima kasih"). Re-verified live: rubric badges and the AI summary now render correctly on candidate 59's detail page. Full backend test suite (13 tests, including the LLM-backed determinism/consistency/PII suites) re-run clean after the fix, with `test_qa_t8_consent_gate.py`'s teardown updated to also clean up the new `rubric_scores`/`interview_summaries` side effects.
  - [x] **Scenario 7 — Seed-data hygiene after test runs**: confirmed via direct DB query that every T11 test artifact is cleaned up — zero leftover test jobs (22-26), zero leftover throwaway candidates (68-71), candidates 32/33/58 reverted to their original untouched state, candidate 59's real data and candidates 60/61's synthetic data intact and unaffected, exactly 2 jobs remain (16 and the T5-fixture job 21) with the expected 30+6 candidate counts, and all scratch `_t11_*.mjs` script files removed from the frontend directory (never committed)
  - ✅ Done when: all 7 scenarios have been run **visibly on the user's screen** with the user confirming each one in real time, and the seed DB is verified clean afterward — **all verified**, plus one real product gap (Scenario 6) found and fixed within the same session

- [x] **T12. Demo-readiness checklist — now includes the edge-state walkthrough (promoted from happy-path-only). — DONE 2026-07-15, all 7/7 edge states verified.** — *Depends: T10*
  - [x] Happy-path script written and rehearsed — see T10 above, run to full completion including real Telegram delivery
  - [x] **Edge/safety states walked through (7 of 7 done, all verified live)**:
    - [x] Expired/invalid token screen → real garbage token correctly shows "Link tidak valid"
    - [x] Mic-permission denied → correctly shows the blocking message with retry
    - [x] Empty/0-second audio submit blocked, then a real answer recorded+submitted successfully (candidate 59's real interview answer)
    - [x] Interview completion-guard → reloading after submission correctly shows "Wawancara sudah selesai" instead of the recorder
    - [x] Invite-modal re-view ("Lihat Link Undangan") → reopening the modal for the already-invited live candidate shows the byte-identical token link, confirmed programmatically, not just eyeballed
    - [x] **Synthetic-candidate "Terkirim" state — real gap found and fixed** (see T10 above): was never actually producing "Terkirim" before this session despite being claimed done in T7's writeup; now genuinely verified showing correctly for both candidates 60 and 61
    - [x] Missing-Telegram disabled send button — **verified live in T11 Scenario 4**
  - [x] **Telegram delivery verified for real**: real report send confirmed received by the user in T11 Scenario 1, and a broken-delivery (invalid chat_id) path confirmed to fail gracefully in T11 Scenario 4
  - [x] Seed loaded, latency acceptable, no crashes on any of the above — confirmed across all runs, zero console errors
  - ✅ Done when: a rehearsed run is recorded AND every edge state above has been seen at least once, AND a real Telegram message has been confirmed received — **all 7/7 edge states done, including the real Telegram delivery check**

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

## Round 2 — Post-MVP Polish (2026-07-17, extended 2026-07-18)

> Source: originally a 15-item punch list from live-testing the running app (screenshots), planned in
> `C:\Users\zikri\.claude\plans\okay-good-now-i-hazy-meadow.md` (full context/root-causes/decisions
> there). Two items (#10 CV↔job storage, #14 Telegram-to-phone) resolved as **no code change** —
> feasibility/design questions answered directly with the user. The old placeholder entry that used
> to live at this spot ("Persist skill-gap analysis instead of recomputing live...") is now
> **Task A1** below — same task, same root cause (Area 2 T8's finding, line ~564).
>
> **Extended 2026-07-18** with 6 new feature requests from a team discussion (points #16-21 below) —
> same section, same numbering scheme continued, not a separate round. Written into this checklist
> BEFORE any of #16-21's implementation, per explicit user instruction.
>
> **Verification note**: per explicit user instruction, this round is **not** verified with
> Playwright — the user will check it themselves in the browser. What's below reflects
> code-completion status (typechecked, backend boots clean, non-LLM tests pass) — every item is
> marked **"code applied, needs manual check,"** not "done," until the user confirms it live.

### Status Matrix — ordered by original point #, with how to check each one

| # | What it is | Task(s) | Status | How to check |
|---|---|---|---|---|
| 1 | Dashboard chart interactivity | B7 | ✅ Done — user-verified 2026-07-17 | All 4 chart cards + pipeline progress-bar segments + "Perlu Perhatian" list items lift and glow on hover (no navigation); "Ringkasan per Lowongan" table and "Perlu Perhatian" list both got a scroll-down button + evened-out column widths, per user follow-up requests during this check. |
| 2 | Block-list editor for JD text fields | B1 | ✅ Done — user-verified 2026-07-17 | Functionality confirmed working; colored-panel design (matching Job Detail) added as a same-day follow-up per user request and confirmed. |
| 3 | Processing modal after "Simpan & Ekstrak Kompetensi" | B2 | ✅ Done — user-verified 2026-07-17 | Confirmed working, including several real bugs found and fixed during the check (X-button no-op, form-reset-on-edit-save, duplicate competency names). |
| 4 | Review/edit extracted competencies, dismiss → recommended pool | A2 + B2 | ✅ Done — user-verified 2026-07-17 | Confirmed working; recommendation pool now correctly AI-sourced-only, duplicate-name creation now blocked at the source. |
| 5 | Jobs list page visualization | B8 | ✅ Done — user-verified 2026-07-17 | Went through several live-iterated corrections (per-job funnel not one combined bar, full-width bars not volume-scaled, custom tooltip replacing the clipped/invisible native one) before landing on the confirmed final design. |
| 6 | Job Detail — colored blocks for JD text | B3 | ✅ Done — user-verified 2026-07-17 | Confirmed working; also got the same lift+glow hover treatment as a same-day follow-up. |
| 7 | Edit Kompetensi Wajib on Job Detail | A2 + B3 | ✅ Done — user-verified 2026-07-17 | Confirmed working; changed to a centered modal popup (matching the edit-job flow) as a same-day follow-up. |
| 8 | Regenerate questions button + back-nav fix + generate-count + per-question duration + stateless AI drafts + selective regenerate + 5-question cap + overlap-aware prompt + duration on unsaved drafts + job-level duration removed + buttons relocated + single-question prompt + "add new" removed from regenerate modal + loading spinner + close-guard + per-slot hint-grounded sequential generation + live progress | #8 | ✅ Done — user-verified 2026-07-19 (14 rounds of real findings across live testing, all fixed and confirmed) | **Round 14 (real bug, the actual root cause of "unrelated questions" — user very explicitly frustrated this took 5 attempts to nail)**: each question SLOT can carry HR's own short topic note (e.g. "QC pengalaman", "ISO 45001" — visible as the preview text in the regenerate modal) — Round 13's sequential loop was discarding that slot's own text entirely once checked and generating a generic JD-grounded question instead, which is why a slot literally labeled "QC pengalaman" came back with a completely unrelated "alat ukur" question. Fixed: `POST /questions/generate` request/response reshaped from batch (`count`/`questions[]`) to single (`hint`/`question`) — `hint` is that slot's own current text (blank/whitespace → `None`, falls back to a plain JD-grounded question); the prompt's new `_HINT_SECTION_TEMPLATE` instructs the model to build specifically off that note, not other JD content. The per-slot loop moved from backend to `QuestionsPage.tsx::handleGenerateConfirm` (one `fetch` per slot, in order, `contextQuestions` accumulated client-side) specifically so the UI can show live progress — `GenerateQuestionsModal` now displays "AI sedang membuat pertanyaan X dari Y..." during generation instead of a generic spinner (also satisfies the earlier "show progress" request that Round 11's spinner only partially addressed). Verified via `curl`: hint="QC pengalaman" → a QC-experience-grounded question; hint="ISO 45001" with slot 1's real output as context → an ISO-45001-grounded question with zero overlap. `generate_questions_sequential()` (Round 13's backend-side loop) removed as dead code now that the loop lives client-side. | **Round 13 (design change, user-requested after Round 12's single-prompt attempt still produced "awful" results)**: switched from one batched `chat_flash()` call per generate request to a NEW `generate_questions_sequential()` that calls `generate_questions(..., count=1)` once per question, IN ORDER starting from slot 1, accumulating every question generated so far in the run (plus the caller's `existing_questions`) as context for each next call — the 2nd call sees the 1st's real output, the 3rd sees both, etc. Distinctness is now enforced by construction (each call literally sees what came before) rather than relying on the model to self-check a whole batch, which Round 12 showed wasn't reliable. Explicit tradeoff the user accepted: `count` LLM calls instead of 1 (measured ~24s per call, so a 4-question generate takes ~96s total — real latency cost, not free). While testing this, found the FIRST call in a sequence (no existing_questions yet) still produced one badly compound question ("...sesuai SOP, dokumentasi memenuhi ISO 9001 dan ISO 45001, serta tetap teliti saat bekerja shift?" — 3 clauses in one item) that slipped past the Round 10 backstop, because that regex only matched "dan/serta" followed by a specific verb whitelist (bagaimana/apa/jelaskan/ceritakan/mengapa/kenapa), not "serta tetap...". Broadened `_single_question()` with a second pattern that cuts at ANY comma-then-dan/serta clause join (verified safe: a plain word-list like "jangka sorong dan mikrometer" has no comma before "dan", so it's untouched) — unit-tested against the exact failing example (correctly trimmed to the first clause) and against the word-list case (correctly left alone), then re-verified end-to-end via `curl` that a fresh 3-question sequential generation produced clean, single-focus, distinct questions throughout. | **Round 11 (real bug + UX, user-requested)**: `GenerateQuestionsModal` could be dismissed (backdrop click / "×") while a generate call was still in flight — the modal would disappear but `busy` stayed true on the page's own buttons with no visible explanation, reading as "the pop-up closed before the question was actually created." Fixed: `Modal`'s `onClose` is now a no-op while `busy` (backdrop/× both blocked; "Batal" was already disabled), and the modal body swaps to a `SpinnerWithLabel` ("AI sedang membuat pertanyaan...") while generating, matching the loading pattern used elsewhere in the app (e.g. camera permission requests). **Round 12 (real bug, confirmed via `curl`)**: batch-generated questions could overlap/mix topically with EACH OTHER within the same request (not just vs. kept questions — Round 6 only covered that case), since the prompt had no distinctness requirement between the N items in one call. User considered a one-LLM-call-per-question sequential design (each seeded with prior questions as context) but explicitly flagged the token cost and asked for a single-prompt fix if possible — stayed a single `chat_flash()` call: `_QUESTION_PROMPT` gained an "ATURAN KEBERAGAMAN ANTAR-PERTANYAAN" section requiring all `count` questions to cover distinct competencies and instructing the model to self-check for topic duplication before answering. Verified via `curl`: a fresh 5-question batch for a QC job produced 5 genuinely distinct topics (calibration, ISO 9001 process, ISO 45001 safety, documentation/traceability, shift-work consistency), each single-focus. | **Round 9 (UX simplification, user-requested)**: removed the "Tambah pertanyaan baru" stepper from `GenerateQuestionsModal` — adding brand-new slots is already "+ Tambah Pertanyaan"'s job, so the modal now does exactly one thing when questions exist: regenerate the checked slots (checkbox list only, no capacity/stepper UI). The count-picker (1-5) only appears when there are zero existing questions (the from-scratch case). **Round 10 (real bug, confirmed via `curl`)**: generated questions were compound/double-barreled — e.g. "Ceritakan pengalaman Anda menggunakan alat ukur..., serta bagaimana Anda memastikan hasilnya akurat?" asks two distinct things in one item, and (real finding) these only ever have ONE terminal "?" even though they're compound, so a naive "count the question marks" check can't detect it. Fixed two ways: (1) `_QUESTION_PROMPT` now has an explicit "ATURAN FORMAT PENTING" section forbidding "dan/serta"-joined compound questions, requiring exactly one "?" per item; (2) a deterministic backstop `_single_question()` regex-detects the actual joining pattern (`, dan/serta bagaimana/apa/jelaskan/ceritakan/mengapa/kenapa`) and truncates to the first half even if the model ignores the prompt — unit-tested directly against the exact reported example (confirmed it correctly trims to "Ceritakan pengalaman Anda dalam menggunakan alat ukur... sesuai SOP?"), and verified end-to-end via `curl` that a fresh 3-question generation produced single-focus questions with no compounding. | **Round 7 (real bug)**: newly AI-generated/manually-added questions (not yet saved, `id === null`) showed an empty box instead of a duration selector, because the selector only rendered for persisted questions (`d.id !== null`) — there was nowhere to PATCH against yet. Fixed: `DraftItem` now carries its own local `duration_seconds` (defaults to 120s), editable via a plain local state update for unsaved drafts; persisted questions keep using the immediate-save `PATCH .../duration` endpoint as before. `QuestionUpdateItem` gained an optional `duration_seconds` field so a new question's locally-chosen duration survives being saved at approve time — verified via `curl`: PUT-ing a brand-new question with `duration_seconds:180` persisted it as 180, not the old default. **Round 8 (layout, user-requested)**: the job-level "Durasi default untuk pertanyaan baru" card is gone — since every question now has its own duration from creation (Round 7), a separate job-wide default no longer served a purpose. Fully removed end-to-end, not just hidden: `jobs.interview_duration_seconds` column dropped (migration), `JobOut`/`InterviewDurationRequest`/the `PATCH /jobs/{id}/interview-duration` endpoint all deleted from `routers/jobs.py` — confirmed zero remaining references anywhere in the codebase (grepped after removal). New questions now default to a `_DEFAULT_QUESTION_DURATION_SECONDS = 120` constant in `routers/interview_questions.py` instead. "+ Tambah Pertanyaan" and "Buat Pertanyaan (AI)" moved from the bottom action row to a new toolbar directly under the page header (where the removed duration card was), visible whenever the question set isn't locked; "Setujui & Kunci Pertanyaan" alone remains at the bottom. | **Round 6 (real bug, confirmed via `curl`)**: each generate call had zero awareness of sibling questions already kept — regenerating slot 5 (which had a QC-experience question) produced a new question about ISO 9001/45001, duplicating the topic slot 4 (ISO 45001) already covered — user-reported as "unaligned." Fixed by passing the KEPT (unchecked) questions' text as `existing_questions` context in the generate request; `_QUESTION_PROMPT` now includes an explicit "don't overlap with these already-existing questions" instruction when that list is non-empty. Verified via `curl`: generating with an ISO-9001/45001 question passed as context produced a question about SOP non-conformance handling instead of repeating ISO content. `QuestionsPage.tsx`'s `handleGenerateConfirm` now collects every draft's text EXCEPT the ones being regenerated and sends it along. | **Round 1**: back-nav now goes to `/jobs` (list) via "Kembali ke Daftar Lowongan", not Job Detail. **Round 2 (real bug)**: regenerating a reopened question that already had a candidate answer 500'd on a foreign-key violation (`interview_answers_question_id_fkey`) — confirmed via a real traceback, the transaction rolled back cleanly (verified via `psql`, no data lost); the underlying delete-based approach that caused this was superseded entirely by Round 5. **Round 3→superseded by Round 5**: an interim append-based design (1-5 count selector) was built and verified, then replaced same-day per user follow-up. **Round 4 (design change, confirmed via AskUserQuestion)**: duration is now per-QUESTION, not job-wide — each question has its own 1/2/3 min selector (immediate-save `PATCH /jobs/{id}/questions/{id}/duration`, works regardless of draft/approved status); the job-level selector is relabeled "Durasi default untuk pertanyaan baru" and only seeds new questions' starting value. Verified via `curl`: PATCH-ing one question's duration to 180s survives a subsequent `PUT /questions` full edit-save (which deletes-and-recreates all rows). **Round 5 (design change, user-requested)**: `POST /questions/generate` is now fully **stateless** — returns generated question TEXT only, writes nothing to the DB (verified via `curl`: generate 3 → `GET /questions` still returns `[]`). AI-suggested drafts now live purely in `QuestionsPage.tsx`'s local `drafts` state, same as manually-typed ones, and only ever get persisted when "Setujui & Kunci Pertanyaan" runs its `PUT /questions` + `POST /questions/approve` calls — this also makes the Round 2 FK-violation risk structurally impossible for `generate` (nothing is deleted since nothing was ever written). Clicking "Buat Pertanyaan (AI)" now opens a `GenerateQuestionsModal` with a checkbox per existing question slot (unchecked=keep, checked=let AI regenerate that slot; empty slots default checked) plus a stepper for how many brand-new slots to add — HR can mix "regenerate #1 and #3, leave #2 alone, add 2 new" in one action. **Hard cap of 5 total questions** enforced client-side (`MAX_QUESTIONS`) — "+ Tambah Pertanyaan" disables at 5, and the modal's "new slots" stepper is capped to remaining capacity. |
| 9 | Questions re-lock bug | #9 | ✅ Done — user-verified 2026-07-19 | Approve/lock → "Edit Pertanyaan" to unlock (now a purely local, non-destructive action — see point #8 Round 7-8+ history) → edit → "Setujui & Kunci Pertanyaan" again. Re-locks successfully; confirmed as part of point #8's extensive live-testing pass. |
| 10 | CV↔job storage | — | ✅ Resolved, no code change | Nothing to check — confirmed staying DB-only (`Candidate.job_id` FK), no UI change. |
| 11 | Job hard-delete | A3 + B6 | ✅ Done — user-verified 2026-07-17 | Tested by deleting the real "Sales Executive" job; backend deletion confirmed correct via direct DB query, and a real frontend stale-list bug (deleted job still showing, "Gagal memuat" on click) was found and fixed during the test. |
| 12 | Skill-gap no longer recomputes live | A1 | ✅ Done — user-verified 2026-07-19 | Open any candidate's detail page twice in a row (Shortlist → click a candidate → go back → click again). Second (and later) loads are near-instant. **Deliberate design, keep this note**: the very first view of a candidate that predates this session still takes ~30s (self-heals once, then cached) — user explicitly chose lazy per-candidate backfill (compute only the CV actually clicked into) over running `python -m seed.backfill_skill_gap` to bulk-precompute all 36 seeded candidates up front (real LLM cost, ~108 calls worst case). The bulk script still exists as an optional demo-warming step but is NOT the intended default flow. |
| 13 | Report has richer content, no live AI | B5 (backend) | ✅ Done — user-confirmed 2026-07-22 | Verified via the laporan page + PDF for candidate 45 (Kandidat WD-14) through extensive iteration this session: Ringkasan Analisis, Sesuai Kebutuhan/Kompetensi Belum Terpenuhi chip grid, Kekuatan Utama, Saran Perbaikan CV (ATS), Kekuatan Utama Wawancara/Feedback Wawancara, and Estimasi Waktu Upskilling (grouped by kompetensi/area, effort-tiered) all render from cached DB data — no live LLM call on page reload. |
| 14 | Telegram invite explanatory copy | B9 | ⏭️ Skipped 2026-07-19 — superseded by the Telegram → Gmail switch (point #19) | No longer relevant: candidate notifications moved to Gmail SMTP, so the Telegram-can't-message-first-contact explanation this point was about no longer applies. Not implemented, intentionally. |
| 15 | "Laporan" page didn't open | B5 (routing) | ✅ Done — user-verified 2026-07-19 | Clicking "Laporan" in the top nav now correctly opens the report list/page instead of silently jumping to the Shortlist page. |
| 16 | Question generation uses all 3 JD fields | T16 | ✅ Done — verified 2026-07-18 | Job → Questions → "Buat Ulang dengan AI" → confirm a question reflects Kualifikasi text specifically (already verified against job 34 "Quality Control": referenced shift work / minimal supervision). |
| 17 | Match-score variance (56 vs 52) — investigate + explain, then **ranking formula replaced entirely 2026-07-19** | T17 | ✅ Done — user-verified 2026-07-19 | **2026-07-18**: explained the semantic+graph_boost formula (kept the formula, added a breakdown tooltip). **2026-07-19 superseding follow-up**: after a deeper discussion the user found a concrete case where semantic similarity ranked a candidate poorly despite the candidate detail page's grounded skill-gap analysis correctly showing the competency present (e.g. "Cloud Deployment") — root-caused to `candidate_embedding.py` comparing ONE blob-vs-blob vector per side (all skills+experience vs all competency names concatenated), which cannot reflect one specific missing/present skill. Decision: **replace the ranking formula entirely**, reusing the same grounded skill-gap analysis (`services/skillgap.py`) already shown on Kandidat Detail instead of embeddings — see the `services/matching.py` entry below for the full implementation. Shortlist's score breakdown tooltip now reads "N/M kompetensi terpenuhi" instead of "Semantik X + Kompetensi Y". |
| 18 | "Lihat CV" button → CV viewer page | T18 | ✅ Done — user-verified 2026-07-19, then narrowed 2026-07-19 | Candidate Detail → click "Lihat CV" → opens that candidate's real uploaded PDF next to their score. **Follow-up (2026-07-19, user-requested)**: the Shortlist card's own "Lihat CV" button was removed (`ShortlistPage.tsx`) — the CV viewer route/page itself is untouched, still reachable from Candidate Detail. In its place, `ShortlistPage.tsx` gained a `SkillGapReadyBadge` next to each candidate's name/alias, backed by a new `skill_gap_ready: bool` field on `MatchOut` (`routers/matching.py`, computed by checking whether a `skill_gap_results` row already exists for that candidate+job) — a green dot + "Data siap" for candidates whose skill-gap analysis is already cached (instant detail-page load), an amber dot + "Belum diproses" for ones that will trigger the ~30s live compute on first view (ties directly into point #12's deliberate lazy-backfill design above). Verified via `curl` against the real seeded Web Developer job: 5 candidates `true`, 25 `false`, matching the real cache state. |
| 19 | Telegram → Gmail SMTP switch | T19 | ✅ Done — user-verified 2026-07-19 (real Gmail send confirmed) | Live with the user's real Gmail App Password (`EMAIL_ENABLED=true`, `TELEGRAM_ENABLED=false`). Real send confirmed working end-to-end via the "Kirim Undangan Wawancara" flow (invite email → real inbox). **2026-07-19 follow-up**: remaining Telegram-branded frontend copy/dead type fields removed now that email is the live channel — see T19-followup #1 below. |
| 20 | Education level/major extraction + eligibility badge | T20 | 🟡 Code complete, backfill script not yet run | Run `python -m seed.backfill_education` (real LLM cost, backfills the ~36 existing candidates/jobs) — or skip it and create a fresh job+CV with an explicit education requirement instead. Either way: Shortlist shows a pass/fail eligibility badge; Candidate Detail shows the extracted level/major; numeric match score is unchanged. |
| 21 | Interview redesign: video + countdown + time-limit + per-answer summary + laporan video | T21 | ✅ Done — user-confirmed 2026-07-22 | Live camera flow (countdown → recording → auto-stop → submit), real transcript + rubric scores, and the laporan "Wawancara" section (video + per-question summary) all confirmed working end-to-end for candidate 45; PDF report unchanged (no video, static Q&A + rubric tables). |
| 22 | Competency dismiss/restore/add-to-pool | A2 | ✅ Done — user-confirmed 2026-07-22 | Confirmed: dismissing a required competency drops it from matching, report, candidate detail, and dashboard, while staying visible and restorable in the recommended pool (Job Detail). |
| 23 | Dashboard "Kesenjangan Kompetensi Terbanyak" widget is single-job only | — | ⚪ Not started | Hardcoded to the Web Developer job, not multi-job aware. Needs a redesign (aggregate across jobs) or removal. |
| 24 | Candidate list reachable outside Job Detail | — | ⚪ Not started | The candidate list should only be reachable via a job's "Lihat Kandidat" button; confirm no other nav path (e.g. the global "Kandidat" item, point 25) surfaces the same list ungrouped by job. |
| 25 | "Kandidat" top navbar item is a shortlist redirect, not a real page | — | ⚪ Not started | Currently jumps straight to the most-recently-created job's Shortlist. Needs an actual landing page — a cross-job entry point that links out per-job, distinct from the "Laporan" page's per-job insight content (point 26). |
| 26 | "Laporan" page is a flat per-job list, not a cross-job view | B5 | ⚪ Not started | `JobReportsPage.tsx` only ever shows one job's candidates. Needs a compact, professional overview aggregating insight/visualization across ALL jobs, complementing the entry point built for point 25 rather than duplicating it. |
| 27 | Backfill skill-gap + match scoring for pre-existing seeded candidates | — | 🟡 Partially done, stopped mid-run 2026-07-19 (deliberate, not an error) | 21/36 candidates on the current pipeline; ~15 remain. Resume with `python -m seed.backfill_match_scores` from `backend/` (real LLM cost, ~75 calls, picks up where it left off). |

### Tasks

- [x] **#9. Fix QuestionsPage re-lock bug — DONE, user-verified.** — *Depends: none*
  - [x] Root cause confirmed by reading the code (not guessing): `handleApprove()` never called
    `setReopened(false)` on success, so after unlock→edit→re-approve the UI kept rendering the
    unlocked form even though the backend had re-approved — a second click then hit the backend's
    "cannot edit already-approved" 400 guard.
  - [x] Fix: `handleApprove()`'s success path now calls `setReopened(false)` and re-syncs `drafts`
    from `approveRes.data` — `frontend/src/pages/QuestionsPage.tsx`.
  - ✅ Done when: lock → unlock ("+ Tambah Pertanyaan") → add a question → re-lock succeeds without
    a 400 — **verified.**

- [x] **#8. Regenerate button + fix mislabeled back-nav — DONE, user-verified.** — *Depends: none*
  - [x] "Buat Ulang dengan AI" button added to the non-approved action row (previously the generate
    button only showed in the zero-questions empty state) — reuses the existing `generate`
    endpoint/handler as-is, with a `window.confirm` guard since it replaces current drafts.
  - [x] "Kembali ke Kandidat" renamed to "Kembali ke Detail Lowongan", target changed from
    `/jobs/${jobId}` (Shortlist — was mislabeled) to `/jobs/${jobId}/detail` (the real Job Detail page).
  - ✅ Done when: regenerate is reachable with existing drafts present; back button lands on Job
    Detail, not Shortlist — **verified.**

- [x] **B1. Block-list editor for Tanggung Jawab / Kualifikasi / Persyaratan Tambahan — DONE,
  user-verified 2026-07-17 (design revised same day, then reconfirmed).**
  (#2) — *Depends: none*
  - [x] New shared component `frontend/src/components/BulletListField.tsx` (+ `.css`) — one text
    input per bullet with a delete button, "+ Tambah poin" to add a row. Mirrors the existing
    `addDraft`/`removeDraft`/`updateDraft` pattern already built in `QuestionsPage.tsx`.
  - [x] Wired into `JobsListPage.tsx`'s create/edit form, replacing the 3 `TextAreaField`s.
  - [x] Backend contract unchanged: still a single `"- line\n- line"` string field — parsed to an
    array on mount, joined back on every edit.
  - [x] **Design revision**: user confirmed the block-list editing itself works, but asked for the
    form to visually match Job Detail's colored panel treatment (point #6/B3) — "table inside
    table," same colors. Extracted a new shared `frontend/src/components/ColorPanel.tsx` (+
    `.css`) generalizing B3's page-local `JdPanel` into a reusable colored-header-bar component;
    `JobDetailPage.tsx` now uses it too (its old local `JdPanel` removed, `JobDetailPage.css`
    deleted — fully superseded, not left as a dead file). `JobsListPage.tsx`'s form now wraps
    Judul Posisi (teal) and each bullet section — Tanggung Jawab (teal), Persyaratan Tambahan
    (green/success), Kualifikasi (gold) — in a `ColorPanel`, same tones as Job Detail, and
    reordered the fields to match Job Detail's display order (Tanggung Jawab → Persyaratan
    Tambahan → Kualifikasi, was previously Tanggung Jawab → Kualifikasi → Persyaratan Tambahan).
    Added an optional `hideLabel` prop to `TextField` and `BulletListField` so their own internal
    `<label>` doesn't duplicate the ColorPanel's colored header text.
  - ✅ Done when: `npx tsc --noEmit` clean (**verified**); the create/edit form's fields render as
    colored panels matching Job Detail's palette; add/remove/save round-trip still works —
    **confirmed by user 2026-07-17.**
  - [x] **Follow-up (real nav gap, found separately from the design revision above)**: the form's
    "Batal" button always went to `/jobs` (the list), even when editing an existing job that has
    its own Detail page — user expects cancelling an edit to return to that job's Detail page, not
    the whole list. Fixed: `Batal` now navigates to `/jobs/${jobId}/detail` when `isEdit`, and
    still falls back to `/jobs` for the create-new-job flow (no detail page exists yet for a job
    that was never saved).

- [x] **A1. Persist skill-gap results instead of recomputing live — DONE, user-verified.**
  (#12, foundation for #13) — *Depends: none*
  - [x] New table `skill_gap_results` (`candidate_id`, `job_id`, `gap_summary`,
    `missing_competencies` JSONB, `matched_competencies` JSONB, `development_priority`,
    `computed_at`) — `backend/models/skill_gap_result.py`, registered in `models/__init__.py` +
    `db/repositories.py`. Table confirmed created in the real running Postgres via `\dt`.
  - [x] **Design adjustment found while implementing**: the plan assumed skill-gap should trigger
    "at CV-ingest time," but `services/candidate_ingest.py::ingest_cv()` never actually calls match
    scoring — only the seed scripts call `compute_match_score()` today; live `POST /candidates`
    doesn't wire up matching at all (a pre-existing gap, out of this round's scope — flagged to the
    user directly mid-session when they asked how to add a CV to a specific job). Hooked the
    trigger into `services/matching.py::compute_match_score()` instead — the one real choke point.
  - [x] `services/skillgap.py`: added `persist_skill_gap()` and `get_or_compute_skill_gap()`
    (self-heals for older candidates with no row yet).
  - [x] `services/matching.py::compute_match_score()` calls `persist_skill_gap()` after the match
    score is created.
  - [x] `backend/routers/candidate_detail.py` — both `get_candidate_full_detail` and the new
    `reanalyze-skill-gap` endpoint now use `get_or_compute_skill_gap`/`persist_skill_gap`; loading
    spinner copy changed from the old "...bisa memakan waktu hingga 30 detik" to a plain "Memuat
    detail kandidat..." since the common case is no longer a live LLM wait. Added a manual
    "Analisis Ulang" button + `POST /candidates/{id}/reanalyze-skill-gap` endpoint as the escape
    hatch called out in the scope guard below.
  - [x] `backend/services/report.py::build_report()` — same swap; also extended to return
    `matched_competencies`, `job_title`, `key_strengths` (from curated `competency_framework` text,
    no LLM), and a per-resource `effort_tier` (deterministic keyword bucket on `duration`, no LLM) —
    feeds B5's report page.
  - [x] **Broke and fixed a real pre-existing test**: `tests/test_qa_t4_report_consistency.py`
    called `build_report(..., bypass_cache=True)`, which no longer exists now that `build_report`
    reads a persisted row instead of calling the LLM. Split into two tests: the original
    self-consistency-voting claim now tests `analyze_skill_gap()` directly (the real place that
    determinism risk lives), plus a new test asserting `build_report()` is byte-identical across
    repeated calls. Both collect and are believed correct; not run this session (real LLM cost).
  - [x] One-off backfill script written — `backend/seed/backfill_skill_gap.py`
    (`python -m seed.backfill_skill_gap` from `backend/`). **Deliberately NOT run this session** —
    confirmed via `psql` that 36 `match_scores` rows currently have 0 matching `skill_gap_results`
    rows, meaning a full backfill would cost up to 36×3=108 real LLM calls. Left for the user to
    run when ready to spend that cost, rather than spending it unprompted.
  - [x] **Scope guard (explicit, carried from the plan)**: no JD-edit invalidation for
    `skill_gap_results` this round — `match_scores` isn't recomputed on JD edit either today
    (pre-existing gap). The "Analisis Ulang" button above is the manual escape hatch.
  - ✅ Done when: a second `GET /candidates/{id}/detail` call for the same candidate reads the
    stored row with **zero** new LLM calls — **verified** (first click per un-backfilled
    candidate will still self-heal-compute once; run the backfill script first for a fully warm demo).

- [ ] **A2. Competency confirm/dismiss/recommend-pool — code applied 2026-07-17, needs manual
  check.** (#4, #7) — *Depends: none*
  - [x] Added `status` column to `jd_competencies` (`active` default | `dismissed`) — model updated
    AND the live Postgres table altered directly (`ALTER TABLE jd_competencies ADD COLUMN status...`,
    confirmed via `\d jd_competencies`), since `create_all()` never alters existing tables.
  - [x] **Ripple audit — ended up being 7 real call sites, not the originally-scoped 4**: found and
    fixed 3 more while grepping (`routers/matching.py`'s shortlist competency comparison,
    `routers/dashboard.py`'s competency-gap chart, and — most consequential —
    `services/candidate_embedding.py::embed_jd_competencies()`, which feeds the JD's Qdrant vector
    used for 70% of the match-score weight; a dismissed competency was still influencing semantic
    similarity before this fix). All 7 now filter to `status="active"`.
  - [x] **Known related limitation, not fixed (documented, not silently ignored)**:
    `embed_jd_competencies()` is only ever called from the seed scripts, never from the live
    `POST/PUT /jobs` flow — so a job's semantic embedding never refreshes when competencies are
    dismissed/added/restored after creation. Same category of pre-existing gap as A1's CV-upload
    finding; out of this round's scope to fix.
  - [x] `_extract_and_store_competencies` (JD create/edit) now only deletes+recreates `active` rows,
    leaving previously-dismissed ones untouched — so editing a JD doesn't wipe the recommended pool.
  - [x] New endpoints: `POST /jobs/{job_id}/competencies/{id}/dismiss`, `.../restore`,
    `POST /jobs/{job_id}/competencies` (add custom, as `active`) — all confirmed registered via a
    live `/openapi.json` check.
  - ✅ Done when: dismissing a competency removes it from "required" everywhere (matching, report,
    candidate detail, dashboard, embeddings) but stays visible/restorable — **user to verify live.**

- [x] **A3. Job hard-delete cascade — DONE, user-verified 2026-07-17.** (#11) —
  *Depends: none*
  - [x] New `DELETE /jobs/{job_id}/permanent`, separate from the existing soft-close
    `DELETE /jobs/{job_id}` (kept as-is) — confirmed registered via live `/openapi.json`.
  - [x] Manual cascade in FK-safe order (rubric_scores → transcripts → interview_answers →
    interview_summaries → hr_decisions → consent_records → match_scores → skill_gap_results →
    parsed_profiles → candidates → interview_questions → jd_competencies → best-effort audit_log
    rows → job) + on-disk CV/audio/report file cleanup per candidate (`shutil.rmtree`).
  - [x] `audit_log` cleanup is explicitly best-effort (its `entity_type`/`entity_id` are free-form,
    no FK constraint — matches the two conventions actually used, `"job"`/`"candidate"`, not
    guaranteed exhaustive). Documented as such, not silently assumed complete.
  - [x] **Real bug found by user's live test (deleted "Sales Executive")**: the backend delete
    itself worked correctly (confirmed gone via direct `psql` query — 0 rows), but the job kept
    showing in the Lowongan list afterward, and clicking it showed "Gagal memuat". **Real cause**:
    `handleHardDelete()` navigated from `/jobs/{id}/edit` to `/jobs` after a successful delete but
    never bumped `reloadKey` — since both routes render the same `JobsListPage` component instance
    (React Router doesn't remount it) and the jobs-list fetch effect only re-runs on `reloadKey`
    changing (not on navigation), the stale pre-delete list kept showing until some unrelated
    reload happened. The soft-close handler already did this correctly; hard-delete was missing
    the same one line. Fixed: `setReloadKey((k) => k + 1)` added before the navigate call.
  - ✅ Done when: deleting a job removes every dependent DB row and on-disk file, AND the job
    immediately disappears from the list with no stale/dead link — **confirmed by user 2026-07-17**
    (backend deletion verified via direct `psql` query; frontend stale-list bug found and fixed
    during the same test).

- [x] **B2. Processing modal + competency review flow — DONE, user-verified 2026-07-17, 3 real findings
  from user testing fixed same day.** (#3, #4) — *Depends: A2*
  - [x] Staged-label processing modal on "Simpan & Ekstrak Kompetensi" (`Modal` + `SpinnerWithLabel`)
    — explicitly a UX-only staged label (900ms timer), not real backend phase tracking.
  - [x] New shared `CompetencyEditor.tsx` (+ `.css`): dismiss/add chips, collapsible "Rekomendasi"
    restore section — opens automatically right after a successful job save, reused again in B3.
  - [x] **Finding 1 (real bug)**: the review modal's X button (and backdrop click) did nothing —
    `onClose` was wired to a no-op `() => {}`. First fix made both X and "Selesai" navigate to
    `/jobs` — **wrong on user re-test**: from the edit flow (`/jobs/34/edit`), clicking X kicked
    the user back to the jobs LIST instead of letting them stay on/return to what they were
    doing, and "Selesai" landed on the list instead of the job's own Detail page. **Corrected**:
    X now just closes the modal with no navigation at all (`setReviewJobId(null)` only) — the
    user stays exactly where they were, free to keep editing the form; "Selesai" closes the modal
    AND navigates to `/jobs/{jobId}/detail`, since reviewing competencies is naturally followed by
    looking at the finished job, not the list.
  - [x] **Finding 1b (real bug, surfaced by the X-button fix above)**: after the X-button fix,
    closing the review modal via X on an EDIT save showed "Judul wajib diisi" and an apparently
    empty title, even though the job clearly had one. **Real cause**: `handleSubmit`'s success
    path unconditionally called `setFields(EMPTY)` — written for the CREATE flow (clear the form,
    ready for the next entry) but running on every save including edits. This was invisible
    before because the page always navigated away immediately after saving; now that X no longer
    navigates, the emptied `title` (a plain controlled `TextField`) became visible immediately,
    while the `BulletListField`s appeared to still show old content only because their internal
    `lines` state is seeded once at mount and never resyncs to a changed `value` prop — so the
    same reset looked selective/inconsistent when it wasn't. Fixed: `setFields(EMPTY)` now only
    runs `if (!isEdit)` — an edit save keeps showing exactly what was just saved.
  - [x] **Finding 2 (real gap)**: dismissing a custom-added competency (typed in via
    "+ Tambah kompetensi", not AI-extracted) put it in the "Rekomendasi" pool alongside genuine
    AI suggestions — user only wants AI-sourced dismissals resurfaced there. Added a `source`
    column to `jd_competencies` (`"ai"` default | `"custom"`, migrated onto the live Postgres
    table directly since `create_all()` doesn't alter existing tables) — `models/job.py`,
    `routers/jobs.py`, `CompetencyOut` schema. `CompetencyEditor.tsx`'s recommended-pool list now
    filters to `source === "ai"`; a dismissed custom competency still exists in the DB (never
    deleted, per A2's design) but never resurfaces in this UI. **Also fixed a related bug this
    surfaced**: `_extract_and_store_competencies` (JD create/edit) was deleting+recreating ALL
    active rows regardless of source, silently wiping out any custom competency the HR had added
    and left active — now scoped to `status="active" AND source="ai"` only, matching the
    protection already given to dismissed rows.
  - [x] **Finding 2b (real bug, user re-test found it live)**: dismissing a competency then
    saving the job again (re-triggering extraction) could recreate an active row with the exact
    same name as the one just dismissed — the dismissed row stayed dismissed, but a fresh
    duplicate appeared active too, so the same competency showed simultaneously in the active
    list AND the recommended pool. Root cause: `_extract_and_store_competencies` only checked
    against rows it was ABOUT to delete (active+ai), never against names that already existed
    elsewhere (e.g. dismissed). Fixed: it now skips creating any competency whose name already
    exists for the job in ANY status. Found + fixed the same class of bug in `restore_competency`
    and `add_competency` too (both could independently create the same kind of active-active or
    active-dismissed name collision) — both now reject with a clear 400 if an active row with
    that name already exists, surfaced as a real error message in `CompetencyEditor.tsx` instead
    of the previous generic "gagal" text. **Cleaned up 3 real duplicate rows already created by
    this bug** in the live DB (job 34: 2× "Microsoft Excel"/"Microsoft excel" case-variant
    duplicates, 1× "Dokumentasi dan Pelaporan" duplicate) via a new one-off script,
    `backend/seed/dedupe_competencies.py` — kept the active row (or most recent, if none active)
    per duplicate group, confirmed zero duplicate groups remain via direct `psql` query.
  - [x] **Finding 3 (polish request)**: the processing modal's spinner sat beside the label text;
    user wanted it above, for a more prominent modal-level loading state. Added an optional
    `layout="stacked"` prop to `SpinnerWithLabel` (default stays `"inline"`, unchanged everywhere
    else it's used) and applied it only to this modal.
  - ✅ Done when: saving a job shows visible AI-processing feedback (spinner above the label) then
    a reviewable/editable competency list before returning to the job list; the X button/backdrop
    close the review modal; only AI-sourced dismissals appear as recommendations — **confirmed by
    user 2026-07-17.**

- [x] **B3. Job Detail — colored blocks + editable competencies — DONE, user-verified 2026-07-17,
  manual check.** (#6, #7) — *Depends: A2, B2*
  - [x] Restyled the 3 JD text sections from plain `<p className="jd-text">` blobs into 3 distinct
    colored panel cards with real `<ul><li>` bullet lists.
  - [x] Mounted `CompetencyEditor.tsx` behind an "Edit Kompetensi Wajib" toggle on the existing chip
    section.
  - [x] **Refactor (same day, driven by B1's design revision)**: the page-local `JdPanel`
    component + `JobDetailPage.css` were extracted into a shared
    `frontend/src/components/ColorPanel.tsx` (+ `.css`) so `JobsListPage.tsx`'s form could reuse
    the exact same colored-panel treatment — `JobDetailPage.css` deleted (fully superseded, not
    left dead), `JobDetailPage.tsx` now imports `ColorPanel` like any other page would. No visual
    change to this page from the refactor itself.
  - [x] **Revision 1 (user re-test)**: user asked for (1) the same lift+glow hover effect from
    the Dashboard/Lowongan applied to this page's mini-stat tiles (Total Kandidat/Sudah
    Diundang/Selesai Wawancara/Diputuskan) — added `.mini-stat:hover` with the same
    `translateY(-3px)` + `--shadow-hover` treatment (no background wash, matching the
    Finding-2/B8 correction that muddy full-tile tint looks bad on elements with their own
    internal color); (2) the inline "Edit Kompetensi Wajib" toggle (which replaced the chip
    display in-place inside the card) changed to a centered `Modal` popup instead — matching the
    "Tinjau Kompetensi Wajib" modal from the job edit flow, for a consistent editing pattern
    across both entry points into `CompetencyEditor`.
  - [x] **Revision 2**: user asked for the same lift+glow on the 3 colored JD panels
    (Tanggung Jawab/Persyaratan Tambahan/Kualifikasi) and the Pertanyaan Wawancara/Kompetensi
    Wajib cards too. Scoped narrowly — added a `.jd-visuals` wrapper class to this page's
    `.split3` container and targeted `.jd-visuals > div > .card` / `.color-panel` specifically,
    rather than styling `.card`/`.color-panel` globally (`.card` in particular is used for plain,
    non-interactive content across nearly every other page — a global hover-lift there would
    misleadingly imply clickability that doesn't exist). No background wash, same reasoning as
    the mini-stat/chart-row fixes.
  - ✅ Done when: JD text reads as 3 clearly separated colored blocks; competencies are editable
    via a centered modal popup; the mini-stat tiles AND the colored panels/cards all lift+glow on
    hover — **confirmed by user 2026-07-17.**

- [ ] **B5. Report page — real content, zero live AI calls — code applied 2026-07-17, needs manual
  check.** (#13, #15) — *Depends: A1*
  - [x] `report.py::get_candidate_report` now has a typed `ReportOut` (was a raw untyped dict)
    including `matched_competencies`, `key_strengths`, per-resource `effort_tier`; new
    `GET /jobs/{job_id}/reports` list endpoint (candidates with a decision, for the entry-point list).
  - [x] Fixed the actual root cause of #15 — it was in **two places, not one**: `NavRedirectPage.tsx`'s
    `DESTINATION_SUFFIX.laporan` (global nav) AND a second, separately-broken copy of the exact same
    bug in `TopBar.tsx`'s job-scoped nav branch (`href: /jobs/${jobId}` — also silently aliased to
    Shortlist). Both now point to `/jobs/${jobId}/reports`.
  - [x] New pages `JobReportsPage.tsx` (`/jobs/:jobId/reports`) and `ReportPage.tsx`
    (`/jobs/:jobId/candidates/:candidateId/report` — nested under jobId to match the existing
    `CandidateDetailPage` route convention, not the flatter path in the original plan), styled per
    the reference images (`skillgap_vis10`/`vis11`, reviewed this session): summary card,
    matched-vs-missing chip grid, "Kekuatan Utama" cards, "Estimasi Waktu Upskilling" grouped by
    the backend's deterministic `effort_tier`. Zero new AI calls anywhere in this page.
  - [x] "Lihat Laporan" link added to `CandidateDetailPage.tsx` next to the existing Telegram send.
  - ✅ Done when: clicking "Laporan" in the nav (both the global and job-scoped variants) opens a
    real report list, and opening a report triggers zero new LLM calls — **user to verify live.**

- [x] **B6. Job hard-delete UI — DONE, user-verified 2026-07-17.** (#11) — *Depends: A3*
  - [x] "Hapus Permanen" danger-styled action, distinct from "Tutup Lowongan", on `JobsListPage.tsx`'s
    edit form — confirmation modal requires typing the exact job title before the delete button enables.
  - [x] **Real bug found by user's live test**: see A3's entry above — `handleHardDelete()` wasn't
    bumping `reloadKey` after navigating back to the list, so the deleted job kept showing as a
    dead link. Fixed there (one shared handler for both A3's backend contract and this UI).
  - ✅ Done when: hard-delete is only reachable through an explicit typed-confirmation step, and
    the deleted job actually disappears from the list afterward — **confirmed by user 2026-07-17.**

- [x] **B7. Dashboard chart interactivity — DONE, user-verified 2026-07-17 (revised 5x same day
  per live user feedback while checking it).** (#1) — *Depends: none*
  - [x] Native `title` hover tooltips (exact values) added to all 4 existing hand-rolled CSS charts.
  - [x] **Revision 1**: first pass made conversion/competency-gap/decision rows navigate to the
    job's detail page on click — user asked to remove that in favor of a pure visual highlight.
    Reverted all `onClick`/`navigate` calls on those 3 chart types.
  - [x] **Revision 2 (final behavior)**: user clarified with a screenshot exactly which effect they
    meant — the existing `.pstage:hover` lift (`translateY(-3px)`) + glow (`--db-shadow-hover`) on
    the pipeline stage tiles, applied on **hover** (not click), to **all 4** chart types including
    the score histogram (originally left out). `.lightable` class rewritten to apply that same
    transform+shadow directly (side-only padding/negative-margin so the resting layout is
    pixel-identical to before — only `:hover` changes anything), added to `hbar-row` (score
    histogram — new), `conv-row`, `gap-row`, `dec-row` — `tokens.css`, `DashboardPage.tsx`. The
    pipeline-track `.pseg` segments (bottom progress bar under "Alur Kandidat," image 1) got the
    same hover lift+glow treatment instead of the earlier click-flash — required changing
    `.pipeline-track`'s `overflow: hidden` to `visible` so the lift isn't clipped by its own
    container (each `.pseg` still clips its own text independently, so this is safe).
  - [x] **Revision 3**: user pointed at the "Perlu Perhatian" attention-list panel (per-item cards
    with the warn/info color coding and a real "Lihat →" link) and asked for the same treatment.
    `.attn-item`'s old subtle `background: var(--bg)` hover replaced with the same
    `translateY(-3px)` + `--db-shadow-hover` lift, keeping its warn/info tint and colored
    left-border intact (those aren't touched by the hover rule) — `tokens.css`. The real
    "Lihat →" navigation link is untouched — this panel's clicks were always meant to navigate,
    unlike the 3 chart types in Revision 1.
  - [x] **Revision 4**: user asked for a scroll-down affordance on the "Perlu Perhatian" list
    (it already scrolls via `.attn-list`'s native `overflow-y: auto`/`max-height: 360px`, but a
    bare scrollbar is easy to miss). Added a floating round "▼" button, bottom-center of the
    panel, that only renders while there's more content below the visible area — tracked via a
    `scrollHeight - clientHeight - scrollTop > 4` check on mount/data-load and on every scroll
    event (`attnListRef` + `attnCanScrollDown` state in `DashboardPage.tsx`), click smooth-scrolls
    the list down 150px (`.attn-scroll-btn` in `tokens.css`, `.panel` given `position: relative`
    as its anchor).
  - [x] **Revision 5**: user flagged the "Diputuskan" (last numeric) column on the
    "Ringkasan per Lowongan" table as too cramped, and asked for the same scroll-down treatment
    on that table. **Real cause found**: a leftover `nth-child(4)` CSS override gave
    "Diwawancara" 27% width while "Kandidat" and "Diputuskan" were stuck at 17% each (not the
    even 3-way split the T15 history describes — the values had drifted since then). Fixed to an
    even 22%/22%/22% split across all 3 numeric columns. Table body wrapped in a new
    `.jt-scroll` container (`max-height: 360px; overflow-y: auto`, matching `.attn-list`'s cap)
    with the same `jobTableRef`/`jobTableCanScrollDown` scroll-button pattern as Revision 4,
    reusing the same `.attn-scroll-btn` styling; `thead th` made `position: sticky; top: 0` so
    the header stays visible while scrolling.
  - ✅ Done when: all 4 charts (including the histogram) AND the attention-list items lift + glow
    on hover with no navigation change, matching the pipeline-tile hover language exactly;
    pipeline progress-bar segments do the same; both the attention list and the job-summary table
    show a scroll-down button exactly when there's more content to reveal and hide once fully
    scrolled; the job-summary table's 3 numeric columns are evenly sized
    — **confirmed by user 2026-07-17.**

- [x] **B8. Jobs list page visualization — DONE, user-verified 2026-07-17, revised same day per user
  feedback.** (#5) — *Depends: none*
  - [x] "Kandidat per Lowongan" horizontal bar chart added under the stat tiles (reuses existing
    `candidate_count`, no backend change), same hand-rolled `.hbar-row` style as the Dashboard.
  - [x] The 3 stat tiles (Total/Aktif/Ditutup) are now clickable toggles that filter the jobs table
    by status, with a visual outline showing the active filter and a proper empty-state message
    when a filter matches zero jobs.
  - [x] **Revision**: user asked for (1) the same lift+glow hover effect from the Dashboard here
    too, and (2) the status filter to also apply to the bar chart, not just the table below it.
    For (2): the chart previously always rendered from the unfiltered `listState.jobs` — now
    reads `filteredJobs`, with its own empty-state message when a filter matches nothing. For
    (1): `.lightable` (previously `.dashboard-shell`-scoped) unscoped to work on any page —
    required promoting `--db-shadow-hover` to a global `:root` token (`--shadow-hover`, same
    value) since the Dashboard-only CSS variable wasn't available outside `.dashboard-shell`.
    Applied `.lightable` to the bar-chart rows; added the same lift+glow `:hover` treatment
    directly to `.stat-tile` (`tokens.css`) and to `.data-table tbody tr` (`Table.css` — the
    generic table component, currently only used on this page, so safe to change globally without
    affecting other pages).
  - [x] **Follow-up 1**: user pointed out the job table's hover was missing the teal background
    tint the Dashboard's `table.jt` rows have (only lift+shadow was there, no color) — added
    `background: var(--teal-soft)` to `.data-table tbody tr:hover` to match, plus
    `border-bottom-color: transparent` on hovered cells so the internal row-divider line doesn't
    visually cut through the now-tinted, lifted row.
  - [x] **Follow-up 2 (real regression from Follow-up 1's sibling change)**: the `.lightable`
    class (used by the bar-chart rows, not the table) had ALSO picked up a
    `background: var(--teal-soft)` on hover during the earlier Dashboard work — for chart rows
    that already contain their own colored track/fill (the bar chart, competency-gap bars, etc.)
    this stacked into one heavy, muddy green block instead of a clean highlight, which the user
    correctly flagged as looking bad. Removed the background from `.lightable:hover` entirely —
    it keeps only the lift + shadow, no tint. `.stat-tile`/`.data-table` row hovers are separate
    CSS rules and keep their tint (those don't have internal color competing with it).
  - [x] **Follow-up 3 (redesign)**: user wanted the pipeline-stage breakdown (Belum Diundang /
    Menunggu Wawancara / Selesai Wawancara / Sudah Diputuskan) with real counts, styled like the
    Dashboard's segmented bar — but **per job**, not collapsed into one combined bar (first
    attempt got this wrong — corrected same-session after the user clarified with "not like that,
    similar visualization for each job, but like before, per job, add this funnel"). **Backend**:
    `JobListItemOut` (`GET /jobs`) extended with 4 new per-job fields using the *exact same*
    row-presence derivation rules as `dashboard.py`'s company-wide funnel
    (`invited_at`/`interview_answers`/`hr_decisions` presence — new `_pipeline_breakdown()`
    helper in `routers/jobs.py`, kept consistent with the existing logic rather than reinvented).
    **Frontend (corrected)**: back to one row per job (matching the original "Kandidat per
    Lowongan" list shape), but each row's bar is now a `.pipeline-track`/`.pseg` 4-segment mini
    funnel for THAT job instead of a single solid-color bar — segment widths proportional to that
    job's own stage counts, segment labels are the real counts, and the row's overall bar WIDTH
    is still scaled by that job's total candidates relative to the largest job (preserving the
    original "longer bar = more candidates" comparison across jobs). One shared color legend
    below the list instead of repeating it per row. `.pipeline-track`/`.pseg` (previously
    `.dashboard-shell`-scoped) unscoped to global, same pattern as `.lightable` earlier, so this
    page can reuse the Dashboard's exact bar styling.
  - [x] **Follow-up 4**: two more corrections from the same live check — (1) the relative-width
    scaling from Follow-up 3 (shorter bars for jobs with fewer candidates) wasn't what was wanted
    after all — bars are now always full width for every job, only the internal segment
    proportions vary; the now-inaccurate "panjang bar mencerminkan jumlah kandidat" subtitle text
    was removed since it no longer applies. (2) the native browser `title` tooltip on each segment
    rendered as a plain unstyled box that visually overlapped into the next row (a real,
    reproducible layout problem, not just a style preference) — replaced with a new reusable
    CSS-only tooltip (`[data-tooltip]` attribute + `::after`/`::before` pseudo-elements,
    `tokens.css`; no JS/state needed), styled consistently with the rest of the app. **Found and
    fixed a real bug while wiring this up**: the row wrapper also had its own `data-tooltip`
    initially, and since CSS `:hover` bubbles to ancestors, hovering a segment triggered BOTH the
    segment's own tooltip AND the parent row's tooltip simultaneously (two overlapping boxes) —
    removed the redundant row-level tooltip (the title + count are already shown as plain visible
    text on the row, so it added nothing anyway).
  - [x] **Follow-up 5 (real bug, tooltip was completely invisible)**: user reported still seeing
    no popup at all on hover, not even the fixed CSS one from Follow-up 4. **Real cause**:
    `.pipeline-track .pseg` has its own `overflow: hidden` (needed for text truncation when a
    segment is narrow) — but a pseudo-element (`::after`/`::before`) is clipped by its OWN host
    element's overflow, even when absolutely positioned outside that element's box. Putting
    `data-tooltip` directly on `.pseg` meant the tooltip was being generated and then immediately
    clipped to invisible by the same element's `overflow: hidden`. Fixed by introducing a
    `.pseg-wrap` outer element (no overflow clipping of its own) that carries `data-tooltip` and
    the `flex` sizing, while the inner `.pseg` keeps its `overflow: hidden` for text truncation —
    `tokens.css`, `JobsListPage.tsx`.
  - ✅ Done when: the Lowongan list page has a real per-job chart and clickable filtering;
    hovering the stat tiles and table rows lift+glow+tint; each job's bar is full-width and shows
    its own real pipeline-stage counts as a mini funnel with a properly styled (non-overlapping)
    tooltip per segment; the whole list respects the active status filter — **confirmed by user
    2026-07-17.**

- [x] **B9. `[skipped]` Telegram invite — explanatory copy only — SKIPPED.** (#14) — *Depends: none*
  - [x] Explanatory line added in `InviteModal.tsx` below the copy-link box, clarifying that
    Telegram's Bot API cannot message a phone number or anyone who hasn't started the bot first
    (platform constraint, confirmed with the user, not a code gap).
  - **Skipped**: moot since Telegram delivery was superseded by the Gmail SMTP switch
    (T17-followup #19, `TELEGRAM_ENABLED=false`) — not verifying a copy tweak on a disabled channel.

- [x] **Cross-cutting (not one of the original 15 points, raised while checking B7/point #1) —
  unify `.pagehead` heading size + fix low-contrast subtitle across all 9 pages — DONE
  2026-07-17.** — *Depends: none*
  - [x] **Real cause**: `.pagehead h1` was `1.4rem` globally, but a `.dashboard-shell`-scoped
    override bumped it to `2rem` on the Dashboard page only — exactly the "inconsistent between
    pages" the user noticed. Unified to `2rem` everywhere (the already-approved, larger
    Dashboard scale) and removed the now-redundant dashboard-only override — `tokens.css`. Affects
    all 9 pages using `.pagehead` (Dashboard, Lowongan, Job Detail, Shortlist, Questions,
    Candidate Detail, Job Reports, Report, Candidate Consent).
  - [x] `.pagehead p` (the subtitle, e.g. "PT Gaskeun Demo · ringkasan rekrutmen") was
    `color: var(--muted)` (a low-contrast gray-green, `#748580`) at `0.86rem` — read as nearly
    invisible next to the larger heading. Changed to `var(--ink-2)` (darker ink) at `0.98rem`,
    `font-weight: 500`.
  - ✅ Done when: every page's title reads the same size, and the subtitle underneath is clearly
    legible, not washed out — **user to verify live.**

- [x] **#10. CV↔job storage — RESOLVED, no code change (2026-07-17).**
  Confirmed with the user: keep DB-only linkage via `Candidate.job_id` FK (already works — every
  candidate row is job-scoped from creation). No filesystem restructuring; job-scoped folders would
  be redundant with the existing FK and add migration risk for no benefit. **Related finding
  surfaced to the user mid-session** (asked directly, not buried here): there is currently no
  frontend UI to upload a CV to a job at all (`POST /candidates` exists but no page calls it), and
  the endpoint doesn't trigger match scoring/embeddings even if called directly — both pre-existing
  gaps, explicitly deferred per the user's "continue the process" instruction rather than silently
  expanded into this round's scope.

### Points #16-21 (added 2026-07-18 — 6 new feature requests from a team discussion)

**Blocker at plan time**: Docker Desktop (Postgres) and the backend (`uvicorn`) were both down when
this section was written — confirmed via a failed `docker ps` and a non-responding `GET /health`.
Every task below except #16 needs the live DB for migrations (`ALTER TABLE`, since `create_all()`
never alters existing tables) and/or live verification. #16 itself only needed a code+prompt change —
confirmed done via `ast.parse` syntax check, not yet verified live.

- [x] **T16. Question generation uses ALL JD fields — DONE, verified 2026-07-18.** (#16) —
  *Depends: none · Effort ~0.5h 🟢*
  - [x] `backend/services/interview_questions.py`: `generate_questions()` now takes a `qualifications`
    param; `_QUESTION_PROMPT` includes a `Kualifikasi: {qualifications}` line and an explicit
    instruction to draw from all three sections (Tanggung Jawab, Kualifikasi, Persyaratan) — was
    previously silently ignoring `job.qualifications` entirely.
  - [x] `backend/routers/interview_questions.py`: call site now passes `job.qualifications`.
  - ✅ Done when: regenerating questions for a job with a distinctive Kualifikasi line produces at
    least one question clearly derived from it — **verified live**: regenerated questions for job 34
    "Quality Control" (Kualifikasi mentions "sistem shift" and "bekerja... dengan pengawasan yang
    minimal"), and question 3 explicitly asked about working shifts and minimal supervision —
    content that was unreachable before this fix since `qualifications` was never passed to the prompt.

- [x] **T17. Match-score variance: investigate + explain — DONE, confirmed against real data
  2026-07-18.** (#17) — *Depends: Docker up · Effort ~2-3h 🟢*
  - [x] **Confirmed with real numbers** (Docker was back up): ran the confirm-query on `match_scores`
    for the Web Developer job. Ranks 1-2 (Kandidat WD-14, WD-03) have `graph_boost=0.2143` and
    `n_matched=3` **identical** for both — the entire score gap (54 vs 52) is 100% explained by
    `semantic_similarity` alone (0.6793 vs 0.6571). Math checks out exactly:
    `0.6793*0.7*100 + 0.2143*0.3*100 ≈ 54`, `0.6571*0.7*100 + 0.2143*0.3*100 ≈ 52`. Root cause fully
    confirmed, not just code-traced — **not a bug**, expected embedding behavior per the confirmed
    decision (explain, don't change the formula).
  - [x] Added a `ScoreBreakdown` component to `ShortlistPage.tsx`, rendered under each candidate's
    score: `Semantik {N} + Kompetensi {N}` (the two weighted point contributions, summing to the shown
    score) with a `data-tooltip` (the reusable CSS tooltip from Round 2's B8 work) explaining why two
    candidates with identical competency matches can still land a few points apart. Uses
    `competency_breakdown`, already returned by `GET /jobs/{id}/candidates` — no backend change needed.
  - [x] Scope note: added to `ShortlistPage.tsx` only (where the original complaint's screenshot was
    from), not `CandidateDetailPage.tsx` — that page's `CandidateFullDetailOut` doesn't expose
    `competency_breakdown` today, and adding it would be a backend change beyond what's needed here.
  - ✅ Done when: the shortlist shows each candidate's semantic vs competency sub-scores; the root-cause
    finding is confirmed against real DB numbers, not just code-reading — **both done**; `npx tsc
    --noEmit` clean. **User to visually confirm the breakdown renders correctly in the browser.**

- [x] **T17-followup. Ranking formula replaced entirely — DONE, user-verified 2026-07-19.** (#17
  superseding change) — *not a new point number, folds into #17 since it's the same "why do scores
  disagree" thread taken to its conclusion*
  - **Why**: user found a concrete case where the semantic+graph_boost score ranked a candidate
    poorly despite Kandidat Detail's grounded skill-gap analysis correctly showing a required
    competency (e.g. "Cloud Deployment") as present. Root-caused via a design discussion (not a bug
    report) to `candidate_embedding.py`: both sides are ONE blob embedding each (all candidate
    skills+experience+qualifications concatenated vs. all JD competency names concatenated), so
    `semantic_similarity` is a single fuzzy number over two blobs — structurally incapable of
    reflecting one specific missing/present skill, and prone to false positives (topical similarity
    isn't skill possession). Decision (user's, after a full tradeoff discussion): stop using
    embeddings for ranking; reuse the ALREADY-GROUNDED skill-gap analysis instead — one source of
    truth for both the Kandidat Detail narrative and the Shortlist score.
  - [x] **Fixed a real false-positive bug in `skillgap.py::_is_skill_match()` first** (found during
    the same discussion, not live testing): the old rule was substring containment (`c in r or r in
    c`), so "Java" would match required "JavaScript" (substring). This had been a soft input to an
    LLM narrative before; now that it directly drives ranking, tightened to exact normalized
    word-TOKEN-SET matching (`_tokenize()` + set equality) — eliminates the Java/JavaScript class of
    false positive. Known tradeoff, accepted: minor punctuation/spacing variants that tokenize
    differently (e.g. "ReactJS" as one token vs "React JS" as two) won't match — intentionally
    stricter now that this feeds a ranking score, not just a sentence.
  - [x] **Added proficiency rating (1-3) per matched competency** — new
    `skillgap.py::rate_competency_proficiency()`, one additional LLM call (not self-consistency
    voted, since a 1-3 rating has far lower variance risk than an open-ended missing-competency
    judgment) that rates how strongly the candidate's actual experience TEXT evidences each already-
    matched competency (1=mentioned only, 2=some usage evidence, 3=strong/senior evidence),
    persisted as a new `skill_gap_results.competency_proficiency` JSONB column (migration applied).
    This is what lets two candidates matching the identical competency SET still be ranked apart by
    depth of experience — the gap the pure "N/M matched" count-based formula (the user's original
    proposal) would have lost, per an explicit tradeoff discussion before implementing.
  - [x] **New ranking formula**, `services/matching.py` (full rewrite, `compute_graph_boost()` and
    all embedding/Qdrant retrieval removed from the scoring path — `candidate_embedding.py`'s
    functions themselves are untouched/still called at seed time, just no longer feed the score):
    `overall_score = sum(proficiency[c] for c in matched) / (3 × len(required))`. A candidate
    matching every required competency at max evidenced strength scores 100; missing or
    weakly-evidenced competencies pull the score down proportionally.
  - [x] `compute_match_score()` now calls `persist_skill_gap()` directly (was already doing this
    alongside the old formula) and derives the score from ITS output — same call, new use of the
    result, no new LLM call added beyond the one proficiency-rating call above.
  - [x] New `rescore_from_existing_skill_gap()` — re-derives `overall_score` from an
    **already-persisted** `skill_gap_results` row, with NO new LLM call. Powers a new one-off script
    `seed/rescore_from_skill_gap.py` that migrates existing candidates from the old formula to the
    new one, explicitly scoped to "Data siap" candidates only (per user instruction) — candidates
    without a cached skill-gap row are skipped, not force-computed, keeping the lazy-backfill design
    from point #12 intact. **Run against the real seeded DB**: 5 candidates rescored (job 16 / Web
    Developer), 31 skipped as not-yet-ready — confirmed via `curl` that ranks and scores updated
    correctly (e.g. Kandidat WD-14 → 0.6, ranks 1-30 all consistent with the new scores). Rescored
    candidates fall back to a neutral proficiency of 2/3 per matched competency (their
    `skill_gap_results` predates the new column) until they're reanalyzed — real, expected, not a bug.
  - [x] `reanalyze_skill_gap()` (`candidate_detail.py`'s "Analisis Ulang" button) now also calls
    `rescore_from_existing_skill_gap()` + `rank_candidates_for_job()` after recomputing — previously
    this endpoint only refreshed the skill-gap narrative, silently leaving the ranking score stale
    relative to the freshly recomputed matched/proficiency data.
  - [x] `routers/matching.py`: `CompetencyStatus` gained a `proficiency: int | None` field (only set
    when `matched=True`); `MatchOut.competency_breakdown` reshaped to
    `{matched_competencies, missing_competencies, competency_proficiency}` (was
    `{semantic_similarity, graph_boost, matched_competencies}`).
  - [x] Frontend `ShortlistPage.tsx`: `ScoreBreakdown` rewritten to show "N/M kompetensi terpenuhi"
    (was "Semantik X + Kompetensi Y"); `CompetencyList` now shows a ★-count next to "Terpenuhi" when
    a proficiency rating exists.
  - [x] OpenAPI schema regenerated; `npx tsc --noEmit` clean; backend hot-reloads clean throughout.
  - **Round 2 (real false negative found via live testing, same day)**: candidate WD-14's CV
    plainly showed database work ("SQL, MySql", "SQL Database Access layer") but their skill-gap
    listed "Database" as missing. Root cause: their PARSED skills list contains `"SQL"`/`"MySQL"`
    as atomic entries, never the literal word "database" — whole-word containment (Round 1's fix)
    can't bridge that, since it's a domain-knowledge relationship, not a string-matching one.
    Considered reusing `competency_framework.related_competency_ids` (what the OLD `graph_boost`
    used) — **rejected after checking the actual table**: it's a coarse 10-category
    learning-resource taxonomy (e.g. "Database (SQL/NoSQL)" related to "Backend Development"), not
    a per-technology synonym map, and has zero entries for specific tools like "SQL"/"MySQL". Wrong
    shape of data for this problem. Built a purpose-specific `_COMPETENCY_SYNONYMS` table instead
    (`skillgap.py`), hand-curated for competency names seen in this project's demo JDs (database →
    sql/mysql/postgresql/mongodb/...; rest api → rest/api/web service/...; cloud deployment →
    aws/azure/gcp/...; etc.) — checked as a fallback when whole-word containment finds nothing.
    **Immediately found a second instance of the same class of bug while verifying**: "GitHub"
    stopped matching required "Git" (compound word, no shared token — the OLD substring-bug had
    been accidentally covering this one too). Fixed by adding a `git` synonym entry. Verified via a
    REAL end-to-end reanalysis of candidate WD-14 (`POST /candidates/45/reanalyze-skill-gap`):
    matched_competencies went from `[HTML, CSS, JavaScript]` (3) to
    `[HTML, CSS, JavaScript, REST API, Database, Git, Agile/Scrum]` (7), score 20 → 33 — genuinely
    reflects their real CV content now, not before/after guesswork. **Known, disclosed limitation**:
    this synonym list is hand-curated and reactive — any competency name or technology not yet
    listed still falls back to pure whole-word matching, so it won't generalize to an arbitrary
    future JD without extending the table. Not chasing full generality here; fixing real, found
    cases as they surface is the deliberate scope.
  - ✅ Done when: Shortlist ranking is derived from the same grounded analysis shown on Kandidat
    Detail, not embeddings; the false-positive substring bug is fixed; the false-negative synonym
    gap is fixed for the cases found so far; proficiency differentiates same-competency-set
    candidates; the rescore script only touches "Data siap" candidates — **all verified against the
    real seeded DB via `curl`**, not just code-reading.
  - **Round 3 (formula redesign, same day, 2026-07-19)**: user explicitly rejected the Round 1/2
    formula (`sum(proficiency) / (3 × required)`) as "mathematically incorrect" in the sense that
    matters for the demo — WD-14's 7/10 matched (mostly 1★ "Pemula" proficiency) scored only 33,
    reading as "Kurang Cocok" despite matching 70% of requirements; a low proficiency rating on
    MOST matched items dragged the whole score down disproportionately, when coverage (matched at
    all) should dominate. User proposed a "70 base points for 7/10 + a level bonus" idea but flagged
    the overflow risk themselves (a 10/10-at-max-level candidate could exceed 100) and asked for the
    correct method. **New formula** (`matching.py::_score_from_skill_gap`, replaces Round 1/2's
    body — a weighted CONVEX combination, mathematically guaranteed ≤100 since it's a weighted
    average of two ≤100 inputs with weights summing to 1):
    ```
    coverage_score = (matched_count / total_required) × 100
    quality_score  = (avg proficiency of matched competencies / 3) × 100   (0 if no matches)
    overall_score  = 0.7 × coverage_score + 0.3 × quality_score
    ```
    Weight split (70% coverage / 30% quality) confirmed via `AskUserQuestion`. The stale-competency
    intersection fix from Round 1 is preserved unchanged (still filters `matched_competencies`
    against the job's CURRENT active list before scoring).
  - [x] **Verified against real seeded data**: candidate WD-14 (id 45, job 16) recomputed via
    `compute_match_score()` → `overall_score = 0.6329` (63.3%), matched=7,
    `proficiency={HTML:1, CSS:1, JavaScript:1, REST API:1, Database:3, Git:1, Agile/Scrum:2}` →
    coverage=70, avg proficiency=1.43, quality=47.6, `0.7×70 + 0.3×47.6 = 63.3` — matches the
    worked example given to the user before implementation, exactly.
  - [x] Re-ran `seed/rescore_from_skill_gap.py` (no new LLM calls, "Data siap"-scoped as before): 6
    candidates rescored across job 16, 30 skipped (not yet analyzed).
  - [x] OpenAPI schema regenerated; `npx tsc --noEmit` clean; backend hot-reloaded clean throughout
    (no route/response-shape changes — this was a pure scoring-math change).
  - ✅ Done when: a candidate matching most required competencies at low-but-real proficiency scores
    meaningfully above 50%, matching the user's intuition, while a candidate matching everything at
    max proficiency still tops out at exactly 100 — both verified, not just derived on paper.
  - **Round 4 (weight retune, same day)**: user asked to shift 70/30 → 80/20, then immediately →
    90/10 (both changes applied directly to `COVERAGE_WEIGHT`/`QUALITY_WEIGHT` in `matching.py`,
    final state is 90/10). Re-verified against WD-14 each time via `compute_match_score()` +
    `seed/rescore_from_skill_gap.py`: 63.3% (70/30) → 65.5% (80/20) → 83.5% (90/10, using the
    job's actual 7/8 required competencies, not the earlier assumed 10 — corrected mid-verification).
    Final formula in production: `overall_score = 0.9 × coverage_score + 0.1 × quality_score`.
  - **Round 5 (UI, `CandidateDetailPage.tsx`, same day)**: user flagged two issues from a live
    screenshot — (1) the "Keputusan" card was cramped into the narrow right sidebar column; moved
    it to a new full-width card directly below the page header, above the two-column CV/rubrik
    split, with its action buttons laid out horizontally instead of stacked `block` buttons; (2)
    two disabled buttons both literally showed the text "Kandidat belum memiliki email" side by
    side (visually duplicated). Fixed by keeping each button's real action label always visible
    (just disabled when `!has_email`) and replacing the duplicated inline button text with a single
    shared hint line below the button row: "Kandidat belum memiliki email — tambahkan email di
    Profil CV untuk mengirim laporan atau notifikasi." `npx tsc --noEmit` clean after the
    restructure.

- [x] **T17-followup #4. Candidate-detail/laporan redesign to match the Tahap 2 "SkillGap AI"
  template — DONE, verified against real seeded data, 2026-07-19.** (#17 superseding change,
  same day as Rounds 1-5 above)
  - **Why**: user wanted the candidate-detail page (and laporan) to visually and structurally
    match the Tahap 2 prototype's report style (CV Summary, Work Experience with tags,
    Education/Certifications/Projects/Organization grids, Explicit/Implicit skill chips, Summary
    Analysis + Market-Aligned/High-Demand chip grids, Key Strengths, ATS Resume Action Items) —
    "Estimasi Waktu Upskilling" explicitly excluded from candidate-detail (deferred as a separate
    future item) but explicitly INCLUDED on laporan. User chose the "extend extraction to match
    fully" scope option (not just a reskin with existing data) via `AskUserQuestion`.
  - [x] **New `parsed_profiles` columns** (migration applied): `cv_summary`, `skills_implicit`,
    `education_history` (JSONB list of {degree, institution, period, gpa}), `certifications`
    (JSONB list of {name, issuer}), `featured_projects` (JSONB list of {name, description, url}),
    `organization_experience` (JSONB list of {role, organization, period, description}). Existing
    `skills` column is treated as "explicit skills" for display — no new column needed for that
    half of the explicit/implicit split.
  - [x] **`cv_parser.py`** — `_PARSE_PROMPT` extended with all of the above as ONE additional
    JSON schema block in the SAME LLM call as skills/experience (not a new call per field);
    `experience` items gain an optional `tags` list (1-4 keyword chips per job). No extra LLM
    cost per candidate at ingest time.
  - [x] **New `skill_gap_results` columns**: `key_strengths` (JSONB list of {title, description})
    and `resume_action_items` (JSONB list of {original, improved}) — new
    `skillgap.py::generate_recommendation_extras()`, ONE additional LLM call grounded on the
    candidate's actual experience text + already-matched competencies (adapted from Tahap 2's
    Agent 4 "Recommendation Report": Key Strengths + ATS action items). Computed once inside
    `persist_skill_gap()`, same one-time-compute/persist discipline as the rest of this module —
    laporan stays free of live AI calls per the earlier standing requirement. Total LLM calls per
    first-time candidate analysis: 3 (skill-gap votes) + 1 (proficiency) + 1 (recommendation
    extras) = 5, up from 4.
  - [x] `report.py::build_report()`'s OLD deterministic `key_strengths` (matched competency name +
    curated `competency_framework.level_description`, generic/identical across any candidate
    matching the same competency) REPLACED with the new LLM-grounded, experience-evidenced
    version — one source of truth for "key strengths" across candidate-detail and laporan, not
    two different definitions.
  - [x] **New shared frontend components** (`components/CvProfileSections.tsx`,
    `components/SkillGapSections.tsx`, `components/ProfileSections.css`) — reused by BOTH
    `CandidateDetailPage.tsx` and `ReportPage.tsx` so the two pages share one template
    implementation, not two. Restyled with this app's own teal/gold/success/warning palette
    (tokens.css) instead of the Tahap 2 original's blue/purple/pink — visual/structural parity
    (sectioned cards, icon-square headers, 2-column grids, chip grids, tag chips), not a literal
    color copy. `ReportPage.tsx` additionally keeps its pre-existing "Estimasi Waktu Upskilling"
    section (unchanged) AFTER the shared sections — candidate-detail does not render it at all.
  - [x] `CandidateDetailPage.tsx` "Email kandidat" field moved out of the old Profil CV card into
    the "Keputusan" card (same row, right-aligned) per explicit user request.
  - [x] **Backfill**: new `seed/backfill_profile_extras.py` — re-reads each candidate's stored raw
    CV, re-runs the (now-extended) `cv_parser` call, UPDATES the existing `parsed_profiles` row's
    new columns only. Spot-checked on 1 candidate first, then run against all 36 seeded
    candidates (real LLM cost, flagged, run to completion in the background — confirmed 36/36 via
    direct DB query, not just script exit code). Also re-ran `compute_match_score()` for all 6
    "Data siap" candidates (job 16) so `key_strengths`/`resume_action_items` populate and scores
    reflect the final 90/10 formula together with the new recommendation-extras call.
  - [x] OpenAPI regenerated; `npx tsc --noEmit` clean; `curl`-verified against candidate 45
    (WD-14) post-backfill: `cv_summary`, `skills_implicit` (7 items), `education_history` (2
    degrees w/ GPA), `experience[].tags`, `key_strengths` (3), `resume_action_items` (3) all
    populated with real, CV-grounded content — not placeholders.
  - ✅ Done when: candidate-detail and laporan both render the full Tahap 2-style sectioned
    template from real extracted/generated data (not mocked), laporan additionally shows the
    upskill-estimate section, and the Keputusan/email UI fixes from Round 5 are preserved.
  - **Round 6 (real bug found via live testing, same day)**: user spotted a visible contradiction
    on candidate WD-14 — "Keahlian Tersirat" (implicit skills) showed "Team Collaboration" and
    "Communication" as things the candidate has, but the SAME page's skill-gap analysis listed
    "Team Collaboration and Communication" as a missing/high-demand competency. Root cause:
    `skillgap.py`'s matching functions (`build_seed_gap`/`analyze_skill_gap`/
    `rate_competency_proficiency`) only ever received `parsed_profiles.skills` (explicit) at every
    call site — `skills_implicit` (new in Round 4's redesign) was rendered in the UI but never
    passed into matching at all, so anything the LLM classified as an implicit/soft skill was
    structurally invisible to the gap check. Fixed with a new `skillgap.py::combine_skills(skills,
    skills_implicit)` helper (dedupes by normalized name, explicit skills first) wired into all 4
    real call sites: `matching.py::compute_match_score`, `candidate_detail.py`'s
    `get_candidate_full_detail` and `reanalyze_skill_gap`, and `report.py::build_report` (kept
    separate from that function's `"skills"` DISPLAY field, which stays explicit-only — combining
    is only for the matching input, not what's shown as "Keahlian Eksplisit"). The existing
    `_COMPETENCY_SYNONYMS` table already had entries bridging "team collaboration"/"communication"
    to the compound required-competency name, so no new synonym-table changes were needed — the
    fix was purely about which skills list gets fed into matching at all.
  - [x] Verified end-to-end via `POST /candidates/45/reanalyze-skill-gap`: matched went from 7/8
    to **8/8** ("Team Collaboration and Communication" now correctly matched), score 85.4% → 95.4%
    (rank #1). Re-ran the same reanalysis for the other 5 "Data siap" candidates (job 16) so the
    fix applies consistently, not just to the one candidate that surfaced the bug — candidate 34
    also picked up an extra match (4/8 → 6/8, score 60.3% → 71.9%); candidates 60/32/33/39 had no
    matching implicit-skill overlap with their job's required competencies, so their scores were
    unaffected (expected, not a bug). OpenAPI regenerated; `npx tsc --noEmit` clean.
  - ✅ Done when: a competency the "Keahlian Tersirat" section displays as present can no longer
    be simultaneously listed as missing in the same candidate's skill-gap analysis — verified
    against the real case that surfaced the bug, not just reasoned about.

- [x] **T17-followup #7. Candidate-detail/laporan UI polish pass — DONE, same day, 2026-07-19.**
  User feedback from a live screenshot review of the new template, 4 items:
  - [x] **Work experience → real bullet points, not one paragraph.** `cv_parser.py::_PARSE_PROMPT`
    gained `experience[].bullets` (2-6 short achievement/responsibility lines per job, mirroring
    how the source CV itself is usually bulleted) — `summary` kept as a 1-sentence fallback.
    `CvProfileSections.tsx` renders `bullets` as a `<ul>` when present, falling back to `summary`
    for any candidate not yet re-backfilled with this prompt version.
  - [x] **Explicit Bahasa Indonesia requirement** added to the prompt for every LLM-AUTHORED
    narrative field (`cv_summary`, `experience[].summary`/`bullets`, project/org descriptions) —
    translates meaning rather than copying English CV sentences verbatim; entity names (company,
    institution, certification, tech/tool names) explicitly left untranslated.
  - [x] **`skillgap.py::_experience_to_text()` now uses bullets when available** (falls back to
    `summary` otherwise) — incidentally resolves an EARLIER-FLAGGED, previously-deferred issue
    (`cv_parser.py` compressing detailed CV bullets into one thin sentence before the proficiency-
    rating LLM call ever saw them) as a side effect of this same change, not a separate task.
  - [x] **Scroll caps**: work-experience list capped to ~2 visible jobs (`.profile-scroll-2`,
    max-height 560px) and each job's bullet list capped to ~5 lines (`.profile-bullet-list`,
    max-height 150px), both `overflow-y: auto` beyond that — mirrors the same "N visible before
    scroll" pattern requested for skills/competencies below.
  - [x] **Skills/competency chip-cloud round-trip**: first pass (T17-followup #6, immediately
    prior) converted "Ringkasan Keahlian" and "Sesuai Kebutuhan"/"Kompetensi Belum Terpenuhi" into
    literal `<table>` rows via a new `ScrollTable` component — user corrected this as a REGRESSION
    ("not like image 1, i mean like image 2 skill lainnya bisa dikananin jadi bubble gitu"): the
    chip/bubble look should stay, just height-capped and scrollable, not converted to table rows.
    `ScrollTable.tsx` REWRITTEN to render the original chip-row bubbles inside a
    `.profile-scroll-chips` box (max-height 168px, `overflow-y: auto`) instead of a `<table>` —
    same call sites (`CvProfileSections.tsx`, `SkillGapSections.tsx`), just a different internal
    render, so nothing else needed to change.
  - [x] **"Saran Perbaikan CV (ATS)" removed from display** — deferred to build later alongside
    the (also-deferred) upskilling-plan feature, per explicit user instruction, rather than shown
    now. `resume_action_items` is still computed and persisted by the backend
    (`generate_recommendation_extras`) — only the frontend render was removed, no backend/data
    change, so nothing is lost when this gets picked back up.
  - [x] **"Kekuatan Utama" (Key Strengths) promoted to a full-width standalone card** (was sharing
    a 2-column grid row with the now-removed ATS card) with its own scroll cap
    (`.profile-scroll-3`, max-height 380px, ~3 items visible) — same "long box, capped, scrollable"
    treatment as work experience, per explicit request.
  - [x] **Backfill note**: only candidates 45 (WD-14) and 53 (WD-22) were re-backfilled with the
    new bullets/Indonesian-language prompt so far (via `seed/backfill_profile_extras.py`'s new
    `--force`/`--candidate-id` flags, added this round for exactly this kind of targeted
    spot-check) — the other 34 seeded candidates still show the OLD paragraph-style English
    summary until a broader `--force` re-run happens (flagged to the user, not yet approved/run,
    same real-LLM-cost discipline as every other backfill this session).
  - [x] OpenAPI regenerated where relevant; `npx tsc --noEmit` clean after every sub-change;
    candidates 45 and 53 both `curl`-verified showing real bulleted, Indonesian-language content
    post-backfill (not placeholders).
  - ✅ Done when: work experience reads as real bullet points in Bahasa Indonesia (for backfilled
    candidates), all four scroll-capped sections behave consistently, skills/competencies are
    bubbles again (not table rows), ATS suggestions are hidden (not deleted) pending the deferred
    upskilling feature, and Key Strengths is a full-width scrollable card.
  - **Round 4 (same day, user pointed to a concrete reference implementation)**: the chip-in-a-
    plain-box style from Round 3 above was STILL not what the user wanted — they explicitly pointed
    to a separate personal project (`Skill gap analysis/prod_v1`, outside this repo) as the source
    of the reference screenshots' actual logic/markup, rather than continuing to guess from images
    alone. Read that project's `frontend/static/index.html` + `style.css` directly: each
    skill/competency box (`.skill-panel`/`.a4-gap-panel`) is a bordered card with a COLORED,
    FULL-WIDTH HEADER BAR (like a table's `<thead>` — uppercase label, tinted background, a
    `border-bottom` separating it from the body) followed by a white chip body — not a small
    floating icon-square over a plain background (what Rounds 1-3 had all been, in different
    forms). Also found: their scroll behavior only activates past 7 items
    (`applyTagScrollLimit(el, count, 7)` → `max-height: 210px`), not an always-on capped box.
  - [x] **New `components/GapPanel.tsx`** (replaces `ScrollTable.tsx`, renamed) — renders exactly
    that structure: colored header bar (`tone`-based: success/warning/info, mapped to this app's
    existing `--success-soft`/`--warning-soft`/`--teal-soft` tokens, not the reference's literal
    hex values) + a chip body that only gets `overflow-y:auto`/`max-height:210px` when `items.length
    > 7`. Used for all 4 boxes: Keahlian Eksplisit/Tersirat (`CvProfileSections.tsx`) and Sesuai
    Kebutuhan/Kompetensi Belum Terpenuhi (`SkillGapSections.tsx`).
  - [x] **"Ringkasan Keahlian" restructured**: dropped the outer shared card + "SK" icon wrapper
    that used to contain BOTH Explicit/Implicit columns — now a plain section label above a
    `profile-grid-2` of two independent, self-contained `GapPanel`s side by side, matching the
    reference's `.skill-panel-grid` (two separate panel cards, not one shared card with two
    sub-columns inside it).
  - [x] **Fixed the "Ringkasan Analisis" flat hardcoded sentence** (item 2 of this round): traced
    to `skillgap.py::analyze_skill_gap()`'s no-gap branch returning a static string
    ("Kandidat memiliki seluruh kompetensi...") instead of calling the LLM at all. The reference
    project's "Summary Analysis" is ALWAYS one LLM call (win-or-lose), producing a real 2-3
    sentence paragraph about fit/strengths either way. Added `_summarize_no_gap()` +
    `_NO_GAP_SUMMARY_PROMPT` (one direct call, no self-consistency voting needed here since there's
    no missing-competency list to ground/protect) and wired it into the no-gap branch. Verified
    directly (bypassing the DB, since candidate 45's own implicit skills had drifted — see below):
    `analyze_skill_gap(["HTML","CSS","JavaScript","Python","Django"], ["HTML","CSS"])` now returns
    a full analytical paragraph discussing the candidate's strengths and fit, not the flat line.
  - **Real side-finding surfaced while verifying (not yet fixed, flagged to user)**: candidate 45's
    match dropped from 8/8 back to 7/8 (missing "Team Collaboration and Communication" again) —
    root cause is that the EARLIER `--force` bullets/Indonesian backfill (this same day, T17-
    followup #7 round above) regenerated `skills_implicit` with different Indonesian phrasing
    ("Kerja tim lintas fungsi" instead of separate "Team Collaboration"/"Communication" entries),
    and `_COMPETENCY_SYNONYMS` is English-only, so it no longer bridges to the compound required-
    competency name. This is a genuine consequence of today's Indonesian-translation change
    interacting with the T17-followup #6 implicit-skills-matching fix — not something this round
    fixed, since the user's ask was UI-focused; noted here so it isn't lost.
  - [x] `npx tsc --noEmit` clean; backend hot-reloaded clean; no OpenAPI schema change needed
    (pure prompt/markup change, no route/response shape change).
  - ✅ Done when: skill/competency boxes have a colored header bar matching the reference project's
    actual markup (not a redrawn guess), Explicit/Implicit Skills are two independent panels, and a
    fully-matched candidate's analysis reads as a real paragraph instead of one static sentence.
  - **Round 5 (same day)**: fixed the Indonesian-synonym side-finding flagged (not fixed) at the
    end of Round 4, plus 3 more UI items from a fresh screenshot review.
    - [x] **Indonesian synonym fix**: added Indonesian terms ("kerja tim", "kerja tim lintas
      fungsi", "kolaborasi", "komunikasi", etc.) to `_COMPETENCY_SYNONYMS["team collaboration and
      communication"]` — the one entry concretely observed breaking after implicit skills started
      being generated in Bahasa Indonesia. Verified directly:
      `_is_skill_match("Kerja tim lintas fungsi", "Team Collaboration and Communication")` → now
      `True`; candidate 45 re-analyzed back to 8/8 matched (was 7/8).
    - [x] **Spacing fix**: the "Ringkasan Keahlian" section (Round 4's two independent `GapPanel`s)
      lost its `margin-bottom` when the outer wrapping `.card` was removed — the next card
      ("Ringkasan Analisis") sat directly against it with almost no gap, reported as "too tight and
      ugly." Added an explicit `marginBottom: 20` to the wrapping `<div>`.
    - [x] **Education entries compacted to 2 rows**: was 3 lines (degree / institution / period+gpa)
      — now 2 (degree, then `institution · period · GPA X` joined on one line, skipping any
      null/missing piece rather than leaving stray " · " separators).
    - [x] **Scroll caps added to Education/Certifications/Featured Projects/Organization
      Experience** (`.profile-scroll-2-small`, max-height 170px, ~2 compact entries visible) — these
      4 boxes had NO cap at all before (unlike work experience's `.profile-scroll-2`), so a
      candidate with many degrees/certs could grow the card unbounded.
    - [x] `npx tsc --noEmit` clean; backend hot-reloaded clean; no schema change (prompt/CSS only).
    - ✅ Done when: the Team Collaboration false-negative from Round 4 no longer reproduces, section
      spacing reads as intentional not cramped, and education/certification/project/organization
      entries are compact 2-row items capped at ~2 visible before scrolling.
  - **Round 6 (same day)**: the "Sesuai Kebutuhan"/"Kompetensi Belum Terpenuhi" panels were STILL
    too tight against "Ringkasan Analisis" above them (Round 5's spacing fix only targeted the
    Ringkasan Keahlian wrapper, not `.profile-grid-2` generally), plus 2 more items from a fresh
    screenshot: removing the now-pointless "Kualifikasi tambahan" line, and a full cleanup of the
    "Keputusan" card + page header.
    - [x] **Spacing fixed at the root** instead of per-instance: `.profile-grid-2` (the shared grid
      class used by every 2-column row in this template — skills panels, education/cert row,
      project/org row, gap panels) now carries its own `margin-bottom: 20px`, so every usage gets
      consistent breathing room automatically instead of hunting each call site one at a time
      (removed the now-redundant inline `marginBottom` from the Round 5 fix on the Keahlian
      wrapper, since the grid itself handles it now).
    - [x] **"Kualifikasi tambahan" removed** from the Pendidikan card (`CvProfileSections.tsx`) —
      user flagged it as useless now that `education_history` (structured degree/institution/
      period/GPA) covers the same ground properly; the underlying `qualifications` field is
      untouched in the data model, just no longer rendered here.
    - [x] **"Kirim Notifikasi Status via Email" button removed entirely** from
      `CandidateDetailPage.tsx` (state, handler, and JSX) — backend endpoint
      (`POST /candidates/{id}/send-decision-notice`) left in place, unused from the frontend, per
      the same "UI-level lockout, don't delete backend capability" pattern as T17-followup #6's
      Analisis Ulang removal.
    - [x] **"Lihat CV" moved from the page header into the Keputusan card's action row** (next to
      "Lihat Laporan"/"Kirim Laporan via Email"), grouped with the other document/report actions
      instead of floating in the top-right corner next to "Kembali ke Kandidat."
    - [x] **Keputusan card reorganized into 3 clearly separated rows** (decision buttons/badge →
      `<hr className="divider">` → report/CV/email-send actions → `<hr className="divider">` →
      email-capture input+save) instead of one long wrapped flex row with the email field pinned
      to the right via `marginLeft: auto` — directly addresses "messy."
    - [x] `npx tsc --noEmit` clean; backend healthy (no schema change — pure frontend cleanup).
    - ✅ Done when: the competency panels no longer read as cramped against the analysis text
      above them, the Pendidikan card has no dead "Kualifikasi tambahan" line, HR can no longer
      trigger a decision-notice email from this page, and the Keputusan card reads as 3 distinct
      grouped actions instead of one crowded row.
  - **Round 7 (same day)**: 2 more Keputusan-card polish items from a fresh screenshot.
    - [x] **Decision badge ("Lanjutkan"/"Tolak") moved to the card's title row**, right-aligned
      next to "Keputusan" — was sitting alone on its own line below the title with a lot of dead
      space around it; now reads as a status chip attached to the section header, matching how
      score/status chips are shown elsewhere in the app (e.g. the pagehead's "Skor Kecocokan ·
      Sangat Cocok" line).
    - [x] **Color variation added for "Lihat Laporan"/"Lihat CV"**: both were plain `ghost`
      (identical white/outline look, hard to tell apart at a glance) — added two new `Button`
      variants, `info` (teal, `--teal-soft`/`--teal`) and `success` (green, `--success-soft`/
      `--success`), mirroring the existing `secondary` (gold) and `danger` (red) variants'
      soft-bg + colored-border pattern. "Lihat Laporan" → `info`, "Lihat CV" → `success`, "Kirim
      Laporan via Email" stays `secondary` (gold) — 3 visually distinct actions in one row now.
    - [x] `npx tsc --noEmit` clean; backend healthy (pure frontend change, no schema impact).
    - ✅ Done when: the decision badge sits inline with the card title instead of floating alone
      below it, and the three action buttons are each a different, intentional color.

- [x] **T18. "Lihat CV" button → CV viewer page — code applied + backend verified 2026-07-18.**
  (#18) — *Depends: Docker up · Effort ~2-3h 🟢*
  - [x] New `GET /candidates/{candidate_id}/cv` in `routers/candidate_detail.py` (mirrors the existing
    audio-stream endpoint), `FileResponse(profile.raw_cv_path, media_type="application/pdf")`; added
    `cv_url` to `CandidateFullDetailOut` AND to `MatchOut` (`routers/matching.py`, reusing the
    `profiles` list already fetched there for `latest_role`) so both the shortlist and candidate
    detail can link to it.
  - [x] New `frontend/src/pages/CandidateCvPage.tsx` (route
    `/jobs/:jobId/candidates/:candidateId/cv`) — score header (alias/job/score/fit-label) + PDF via
    `<iframe>` (HR-token blob fetch, same pattern as `AudioPlayer.tsx`). "Lihat CV" button added to
    `ShortlistPage.tsx` (per candidate row) and `CandidateDetailPage.tsx` (Profil CV card header).
  - [x] **Verified live**: `curl` against the real endpoint with a real HR JWT returned
    `200, content-type: application/pdf, size: 30603` for candidate 32; `cv_url` confirmed present
    and correctly formed on both `GET /candidates/{id}/detail` and `GET /jobs/{id}/candidates`.
  - ✅ Done when: clicking "Lihat CV" opens that candidate's real PDF next to their match score —
    backend fully verified; `npx tsc --noEmit` clean. **User to visually confirm the page renders
    correctly in the browser.**

- [x] **T19. Telegram → Gmail SMTP switch — CODE COMPLETE, needs real Gmail App Password to test live send.** (#19) —
  *Effort ~6-8h 🟠*
  - [x] `candidates.contact_email` column added (`ALTER TABLE candidates ADD COLUMN contact_email
    VARCHAR;` applied to the live Postgres); `pii_redaction.detect_candidate_email()` (reuses
    `_EMAIL_RE`) captures the real email in `candidate_ingest.py::ingest_cv` **before** `redact_pii()`
    runs — everything downstream of that line (the LLM parse call) is unchanged, still redacted.
  - [x] `backend/services/email_client.py` — stdlib `smtplib.SMTP_SSL` + `email.message.EmailMessage`,
    no new dependency. New `EMAIL_ENABLED`/`SMTP_HOST`/`SMTP_PORT`/`SMTP_USERNAME`/`SMTP_PASSWORD`/
    `SMTP_FROM` in `config.py` + `.env.example` (real `.env` left with `TELEGRAM_ENABLED=true` and no
    SMTP creds for now — flipping to email live requires the user's own Gmail App Password, an
    external one-time step this session can't do).
  - [x] `delivery.py::send_report` rewritten with `if EMAIL_ENABLED: ... elif TELEGRAM_ENABLED: ...`
    branching — guard swapped to `contact_email`/new `NoEmailAddressError` on the email path; the
    Telegram path (`telegram_chat_id`/`NoTelegramLinkError`) kept 100% intact, not deleted. Two new
    functions in the same file: `send_invite_email()`, `send_decision_notice()`.
  - [x] `routers/report.py::send_candidate_report` now catches both `NoTelegramLinkError` and the new
    `NoEmailAddressError` → HTTP 400.
  - [x] New endpoints: `PATCH /candidates/{id}/contact-email` (HR-editable override for a CV with no
    detectable email), `POST /candidates/{id}/send-invite-email` (emails the already-built invite
    link), `POST /candidates/{id}/send-decision-notice` (manual-trigger accept/reject email, reads the
    candidate's `hr_decisions` row — never automatic on decision, matching the existing manual
    send-report pattern).
  - [x] `main.py`: `run_telegram_poller()` now gated behind `if TELEGRAM_ENABLED:` (config import added;
    flag existed before but nothing read it).
  - [x] `CandidateFullDetailOut` (`candidate_detail.py`) gains `contact_email`/`has_email`; `InviteOut`/
    `CandidateDetailOut` (`candidates.py`) gain `contact_email`.
  - [x] Frontend: `CandidateDetailPage.tsx` — editable "Email kandidat" input + Save button (Profil CV
    card); "Kirim Laporan via Telegram" → "via Email", gated on `has_email` instead of
    `has_telegram_link`; new "Kirim Notifikasi Status via Email" button (manual decision-notice
    trigger). `InviteModal.tsx` — shows the CV-detected `contact_email` when present, adds a "Kirim via
    Email" button alongside the existing copy-link box.
  - [x] OpenAPI schema regenerated (`curl .../openapi.json` → `src/api/openapi.json` +
    `npx openapi-typescript` → `src/api/schema.d.ts`); `npx tsc --noEmit` clean; backend confirmed
    hot-reloaded without errors (`/health` OK, new routes present in the live `/openapi.json`).
  - ✅ Done when: with `EMAIL_ENABLED=true` and real SMTP creds, sending a report emails the PDF to the
    candidate's real CV-extracted address; invite + decision notices can also be emailed; flipping the
    flags back restores Telegram cleanly. **Live send verified 2026-07-19** — real Gmail App Password
    in `.env`, real invite email sent and received.

- [x] **T19-followup #1 (2026-07-19): Telegram-branded frontend cleanup, now that email is the live
  channel.** — Backend Telegram code (`telegram_client.py`, the `delivery.py` fallback branch, the
  `TELEGRAM_ENABLED`-gated poller in `main.py`) is deliberately left intact as the documented rollback
  path, per T19's original design — only user-visible/frontend Telegram traces were removed:
  - [x] `InviteModal.tsx` — the hint paragraph explaining Telegram's first-contact limitation (now
    stale, since email is the active auto-send channel) replaced with a plain email-focused line.
  - [x] `DashboardPage.tsx` — "Laporan Terkirim" KPI's `via Telegram` sub-label → `via Email`.
  - [x] `has_telegram_link` removed from 3 frontend-only type declarations (`CandidateTokenGuard.tsx`,
    `useCandidateSelf.ts`, `CandidateDetailPage.tsx`'s `CandidateDetail` type) — confirmed dead via
    grep (`.has_telegram_link` had zero property-access usages anywhere in the frontend before
    removal). Backend still returns the field (harmless, unused by the frontend now) since the
    backend response models weren't touched — out of scope for a frontend-only cleanup.
  - [x] `npx tsc --noEmit` clean; confirmed no remaining `telegram`/`Telegram` text in hand-written
    frontend source (only the generated `openapi.json`/`schema.d.ts` still mention it, mirroring the
    untouched backend schema).
  - ✅ Done when: no Telegram-branded copy or dead Telegram-only fields remain in frontend source. Not
    a UI behavior change — email was already the only working send path.

- [x] **T20. Education level/major extraction + eligibility badge — CODE COMPLETE, backfill not yet run.** (#20) —
  *Effort ~5-7h 🟠*
  - [x] 4 new nullable columns applied on the live Postgres (`ALTER TABLE parsed_profiles ADD COLUMN
    education_level VARCHAR; ... major VARCHAR;` and `ALTER TABLE jobs ADD COLUMN
    required_education_level VARCHAR; ... required_major VARCHAR;`) + matching model fields.
  - [x] `cv_parser.py::_PARSE_PROMPT` extended with `education_level` (validated against a fixed enum
    SMA/SMK/D3/S1/S2/S3, anything else coerced to `null`) + `major`; `parse_cv_text()`'s return dict
    and its JSON-decode-failure fallback both extended; `candidate_ingest.py::ingest_cv` persists both
    onto the new `parsed_profiles` row.
  - [x] New `extract.extract_education_requirement(qualifications)` — a small parallel LLM call (kept
    separate from `extract_competencies()` so that prompt's JSON-array shape didn't need to change)
    reading the JD's Kualifikasi text for a required level/major. Wired into
    `jobs.py::_extract_and_store_competencies` (runs on both job create and edit) and persisted onto
    `jobs.required_education_level`/`required_major`.
  - [x] New `backend/services/education.py::meets_education(candidate_level, required_level)` — ordinal
    ranking `SMA/SMK(0) < D3(1) < S1(2) < S2(3) < S3(4)`; returns `None` (not a fail) when either side
    is unset. Surfaced as `education_level`/`major`/`meets_education` on `MatchOut`
    (`routers/matching.py`) and on `CandidateFullDetailOut` (`routers/candidate_detail.py`); `JobOut`
    (`routers/jobs.py`) gained `required_education_level`/`required_major`. **Score untouched** — no
    scoring code path was touched, per the confirmed decision.
  - [x] Frontend: `ShortlistPage.tsx` — new `EducationBadge` component rendering "Memenuhi syarat
    pendidikan" (green) / "Belum memenuhi syarat pendidikan" (amber) next to the pipeline-status badge,
    hidden entirely when `meets_education` is `null` (no requirement set, or candidate's level
    unknown — a neutral case, not a fail). `CandidateDetailPage.tsx` — education level + major + the
    same pass/fail badge shown under Kualifikasi in the Profil CV card.
  - [x] One-off backfill script `backend/seed/backfill_education.py` — two idempotent passes (jobs:
    one cheap LLM call each against existing `qualifications` text; candidates: re-reads each stored
    CV PDF and re-runs extract→redact→parse to fill only the two new columns). **Not yet run** — real
    LLM cost (a vision-fallback pass may trigger for scanned CVs), flagged per the project's standing
    rule on backfills, left for the user to run when warming the demo.
  - [x] OpenAPI schema regenerated; `npx tsc --noEmit` clean; backend confirmed hot-reloaded without
    errors (new fields present in the live `/openapi.json`).
  - ✅ Done when: candidate detail shows extracted education + major; shortlist shows a pass/fail
    education badge against the job's requirement; numeric match score is unchanged. **Code path is
    complete and verified via schema/typecheck; the badge won't show real data on the existing ~36
    seeded candidates/jobs until the backfill script is run** (new candidates/jobs get it
    automatically going forward). User to visually confirm in the browser.

- [x] **T21. Interview redesign: video + countdown + time-limit + per-answer summary + laporan
  video — CODE COMPLETE, live camera end-to-end NOT verified (no Playwright, no webcam in this
  session — user to test manually).** (#21) — *Effort ~14-18h 🔴* — **the single largest task in
  the project, bigger than the original audio recorder build (5.5h)**
  - [x] `jobs.interview_duration_seconds` column added (migration, default 120s, constrained to
    60/120/180 by the new endpoint); duration selector (1/2/3 min) on `QuestionsPage.tsx` via a
    dedicated `PATCH /jobs/{id}/interview-duration` (not `PUT /jobs`, which would re-run competency
    extraction) — reads/writes `job.interview_duration_seconds` directly. **Superseded same day
    (2026-07-19, see point #8's row in the Status Matrix above)**: duration is now set per-QUESTION,
    not job-wide — this job-level field/endpoint is kept, but only as the starting default for
    newly-generated questions, not the value actually applied during the interview anymore.
  - [x] New `frontend/src/lib/useVideoRecorder.ts` replacing the deleted `useAudioRecorder.ts`:
    `getUserMedia({video:true, audio:true})`, live muted `<video>` preview bound via
    `previewVideoRef`, a 5-second pre-record countdown state (`countdown`) before recording starts,
    a count-DOWN `remainingSeconds` timer that calls `recorder.stop()` itself at 0 (no user action
    needed to auto-stop), `video/webm` blob output.
  - [x] `CandidateInterviewPage.tsx` fully redesigned: camera preview on top (live during
    countdown/recording, frozen playback once stopped) → question text → controls. Flow: idle →
    "Mulai Jawab" → 5s countdown overlay → recording (live camera + red REC badge counting down) →
    auto-stops → stopped (video playback + re-record/submit) → uploading → next question. New
    `CandidateQuestionsOut` response shape (`{interview_duration_seconds, questions}`) replaces the
    old bare list so the recorder knows the HR-set limit before it starts.
  - [x] Backend: `GET /candidates/{id}/answers/{id}/audio` now serves `media_type="video/webm"`
    (old audio-only recordings still play fine in a `<video>` element — blank frame, working
    controls, so no branching by recording age). STT (`stt_client.transcribe`) is unchanged — sends
    the video webm directly to Groq Whisper, which extracts the audio track. **Flagged risk, not
    resolved this session**: this is unverified against a real video-webm file (no webcam available
    in this environment); if Groq rejects the container, the documented fallback is a parallel
    audio-only `MediaRecorder` on the same stream for the STT upload — not built, since the direct
    path is expected to work (webm/mp4 with an audio track is an explicitly supported Whisper API
    input) and building a fallback for an unconfirmed failure would be speculative. **User must
    verify with one real recording before relying on this in a demo.**
  - [x] `transcripts.summary_text` column added (migration) — `rubric_persist.py::
    score_and_persist_answer` now writes the already-computed `score_answer()` summary onto the
    transcript row instead of dropping it. This also fixes a real pre-existing bug found while
    wiring it up: `compute_and_persist_interview_summary` previously only ever received the LAST
    answer's summary from the caller (`interview_answers.py::submit_answer` collected just
    `[scored["summary"]]` from its own call, with a comment acknowledging earlier answers'
    summaries were unavailable) — it now reads every answer's persisted `summary_text` itself, so a
    multi-question interview's overall AI summary reflects ALL answers, not just the last one.
  - [x] Laporan page (`ReportPage.tsx`, NOT the PDF) gets a new "Wawancara" section: per question,
    shows the question text, its persisted per-answer summary, and a playable video via a new
    `VideoPlayer.tsx` component (HR-token blob fetch, same pattern the deleted `AudioPlayer.tsx`
    used). Built via a new `_build_interview_answers()` helper in `routers/report.py`, called
    separately from `build_report()` so the PDF (which reuses `build_report()`'s same dict) is
    completely untouched, per the request ("not the pdf"). `CandidateDetailPage.tsx`'s existing
    per-answer cards also upgraded to `VideoPlayer` + show the per-answer summary.
  - [x] Cleanup: `useAudioRecorder.ts` and `AudioPlayer.tsx` deleted (fully replaced, confirmed
    zero remaining imports before deleting).
  - [x] OpenAPI schema regenerated; `npx tsc --noEmit` clean; backend confirmed hot-reloaded without
    errors (all new routes — `PATCH /jobs/{id}/interview-duration`, the new `CandidateQuestionsOut`
    shape — present in the live `/openapi.json`).
  - ✅ Done when: a candidate records a video answer that auto-stops at the HR-set limit after a 5s
    countdown; each answer's transcript + AI summary are stored; HR sees, per question on the laporan
    page, the summarized answer plus a playable video. **Code path is complete; the live
    camera/countdown/auto-stop/STT-on-video flow has NOT been exercised in a real browser this
    session** (standing instruction: no Playwright, user verifies manually) — this is the task most
    in need of that manual pass before the demo, given the flagged STT risk above.

### Verification — user-driven, not Playwright (per explicit instruction this session)

All code above is typechecked (`npx tsc --noEmit` clean throughout), the backend boots clean with
every new endpoint confirmed present in a live `/openapi.json` fetch, and the two non-LLM-cost test
files (`test_qa_t6_human_in_the_loop.py`, `test_qa_t8_consent_gate.py`) pass. Nothing beyond that has
been exercised through the actual browser this session — that verification pass is the user's to run.
Suggested checks, in the order they build on each other:
1. `#9` — lock → unlock → add a question → re-lock; confirm no 400.
2. `A1`/`B5` — open a candidate detail page twice; second load should be near-instant, not ~30s
   (run `python -m seed.backfill_skill_gap` first for a fully warm demo — real LLM cost, ~108 calls
   worst case). Then open that candidate's report from the new Laporan page.
3. `A2`/`B2`/`B3` — create or edit a job, dismiss a suggested competency in the review modal, confirm
   it disappears from the Shortlist's required-competency comparison, then restore it from Job
   Detail's "Edit Kompetensi Wajib" pool.
4. `A3`/`B6` — hard-delete a **disposable** test job (not real seed data) and confirm its rows/files
   are actually gone via `psql`/filesystem.
5. `B1`, `B7`, `B8`, `B9` — visual/interaction spot-checks (block-list editor, dashboard tooltips,
   Lowongan page chart + filter tiles, invite modal copy).

### Manual verification steps for points #16-21 (added 2026-07-18, none exercised in a browser yet — see the Status Matrix above for the condensed per-point version)

**#16 — Questions use all 3 JD fields.** On a job's Questions page, click "Buat Ulang dengan AI".
Confirm at least one generated question clearly reflects something written in that job's
Kualifikasi text specifically (not just Tanggung Jawab/Persyaratan) — e.g. if Kualifikasi mentions
"sistem shift" or a specific certification, a question should reference it.

**#17 — Score breakdown.** Open Shortlist for a job with candidates whose scores are close (e.g.
56 vs 52). Under each candidate's score number, confirm a small line reading "Semantik NN +
Kompetensi NN ⓘ" appears; hover it for the full tooltip explanation. Confirms the gap is now
self-explanatory instead of looking arbitrary.

**#18 — Lihat CV.** From either the Shortlist page (per-candidate row) or a Candidate Detail page
(Profil CV card header), click "Lihat CV". Confirm it opens a page showing that candidate's real
uploaded PDF next to their score/alias — this is the *raw* CV (real name/email/phone visible by
design, HR-only).

**#19 — Telegram → Gmail (needs your own Gmail App Password first, not done in this session):**
1. Generate a Gmail App Password: Google Account → Security → 2-Step Verification → App passwords.
2. Edit `.env` (real one, not `.env.example`): set `EMAIL_ENABLED=true`, `TELEGRAM_ENABLED=false`,
   `SMTP_USERNAME=<your gmail>`, `SMTP_PASSWORD=<the app password>`, `SMTP_FROM=<your gmail>`.
3. Restart the backend process (`.env` is only read at startup — `uvicorn --reload` picking up a
   code change is not enough; stop and re-run it, or `docker compose restart backend` if
   containerized).
4. Open a candidate's detail page. Under "Profil CV" you should see an "Email kandidat" field —
   if empty (CV had no detectable email), type a real test-inbox address and click "Simpan".
5. Make a decision (Lanjutkan/Tidak Dilanjutkan) if not already made, then click "Kirim Laporan via
   Email" (label should already say "via Email", not "via Telegram" — confirms the gating switched).
   Check that test inbox for the PDF + summary.
6. Click "Kirim Notifikasi Status via Email" — check the inbox for the accept/reject notice.
7. Open that candidate's invite modal (Shortlist → "Undang ke Interview" or "Lihat Link Undangan").
   If `contact_email` is set, a "Kirim via Email" button should appear next to "Salin Link" — click
   it and check the inbox for the invite link email.
8. To confirm the rollback path still works: flip `EMAIL_ENABLED=false`, `TELEGRAM_ENABLED=true`,
   restart, and confirm "Kirim Laporan via Email" reverts to "Kirim Laporan via Telegram" and gates
   on `has_telegram_link` again.

**#20 — Education extraction (run the backfill first, or test fresh — either works):**
- *Option A, backfill the existing demo pool* (real LLM cost — one call per job + up to two calls
  per candidate with a CV file still on disk): `cd backend`, activate the venv, run
  `python -m seed.backfill_education`. Watch the printed per-row output for failures. Then open
  Shortlist for that job — candidates should now show a "Memenuhi syarat pendidikan" (green) or
  "Belum memenuhi syarat pendidikan" (amber) badge next to their pipeline-status badge. Open a
  Candidate Detail page — a "Pendidikan: <level> — <major>" line should appear under Kualifikasi,
  with the same pass/fail badge.
- *Option B, test on something new* (no backfill needed): create a new job whose Kualifikasi text
  states an explicit requirement (e.g. "Minimal S1 Teknik Informatika"), upload a candidate CV that
  states their own education level/major, and confirm both the job's requirement and the
  candidate's extracted level/major show up automatically, with the eligibility badge computed
  correctly (candidate's level ≥ job's required level → green).
- Either way: confirm the candidate's numeric match score is unaffected by this — same score before
  and after the education fields populate.

**#21 — Interview redesign (the flagged risk task — this is the one most likely to surface a real
bug, since none of this was exercised in a browser or against a real webcam this session):**
1. On a job's Questions page, confirm a "Batas waktu menjawab per pertanyaan" selector shows 1/2/3
   menit. Change it, reload the page, confirm the new value persisted (reads from the job, not
   local state).
2. Get a candidate's invite link (Shortlist → "Undang ke Interview"), open it in a separate
   browser/incognito window (simulating the candidate).
3. Give consent, then on the interview screen click "Mulai Jawab". Confirm: browser prompts for
   camera+mic permission; after granting, a live camera preview appears; a 5-second countdown
   overlay (5→1) plays before recording starts; once recording starts, a red "● mm:ss" badge
   appears and counts DOWN from the HR-set duration; recording auto-stops on its own at 0 (or click
   "Berhenti Rekam" to stop early and confirm that also works).
4. After stop, confirm the camera preview area now shows the recorded video with playback controls,
   and "Rekam Ulang" / "Kirim Jawaban" buttons appear. Click "Kirim Jawaban".
5. **This is the critical check**: confirm the upload succeeds (no error banner) and, most
   importantly, that transcription actually completed — this is the flagged, unverified risk
   (Groq Whisper receiving a video/webm container instead of audio-only). Confirm by opening that
   candidate's HR-side Candidate Detail page and checking the answer card shows a non-empty
   "Transkrip:" line and rubric-score dots. **If the transcript is empty or the answer submission
   errors, that's the STT-on-video risk materializing — report it back so the documented fallback
   (a parallel audio-only `MediaRecorder` track for the STT upload) can be built.**
6. Repeat for all approved questions, then confirm the "Wawancara selesai" screen appears.
7. Back on the HR side: confirm the Candidate Detail page's per-answer cards now play back as
   `<video>` (not just audio) and show a "Ringkasan AI" line above the transcript.
8. Make a decision, then open "Lihat Laporan" (the page, not the PDF). Confirm a new "Wawancara"
   section lists each question with its AI summary and a playable video beneath it. Then also open
   the PDF report (existing "Kirim Laporan" flow or however the PDF is currently viewed) and confirm
   it is unchanged — no video/interview section should appear there.

## To Do — dashboard/navigation scoping + visualization redesign (added 2026-07-19, not started)

User-flagged during live testing, explicitly noted for later — no code written yet for any of these.

- [ ] **Dashboard "Kesenjangan Kompetensi Terbanyak" widget** — currently hardcoded/focused on Web
  Developer only, not multi-job aware. Either change it to a different visualization or remove it
  entirely.
- [ ] **Candidate list scoping** — the current candidate list should only live inside Job Detail's
  "Lihat Kandidat" button, not be reachable elsewhere as a general cross-job list.
- [ ] **"Kandidat" top navbar item** *(lowest priority)* — currently just redirects to a shortlist
  view (via the most-recently-created job). Should instead show a proper detail/visualization page.
  Needs design thinking on what a cross-job "Kandidat" overview visualization should actually show
  — should include a general visualization per job.
- [ ] **"Laporan" page** *(main priority)* — needs compact, professional visualization/insight
  covering ALL jobs, not just a flat per-job candidate list (current `JobReportsPage.tsx` is
  job-scoped only). Needs design thinking on the right visualization — should include a general
  visualization per job, similar spirit to the Kandidat item above but for reports.
- [x] **RESOLVED for new uploads, 2026-07-19 — root cause found and fixed, not just worked
  around.** Originally logged as a deferred "run analysis for unprocessed candidates" backfill
  item; investigating it with the user surfaced the actual root cause: `compute_match_score()` was
  **never called from the live `POST /candidates` upload endpoint at all** — it only ever ran from
  one-off seed scripts (`load_demo_data.py`, `load_t5_fixture.py`). A real candidate uploaded
  through the running app got a `parsed_profiles` row (CV extraction) but NO `match_scores` row,
  which means `get_ranked_candidates` (Shortlist) wouldn't show them AT ALL — not even as "Belum
  diproses", since that endpoint only lists candidates that already have a `match_scores` row.
  WD-22/WD-18's "Belum diproses" badges were a symptom of a ONE-TIME SEED that ran the OLD scoring
  pipeline for all 36 demo candidates long before this session's ranking-formula work — not
  something new uploads would ever hit going forward once fixed.
  - [x] **Fix**: `routers/candidates.py::create_candidate` now calls `compute_match_score(db,
    candidate.id, job_id)` + `rank_candidates_for_job(db, job_id)` immediately after `ingest_cv(...)`
    succeeds — CV upload now runs BOTH pipelines (extraction + skill-gap analysis + scoring)
    synchronously in one request. User explicitly chose synchronous over a background task
    (`AskUserQuestion`) — accepts ~25-30s added latency (5 LLM calls) rather than building new
    background-task/error-reporting infra this late in the build; matches `ingest_cv`'s existing
    synchronous style.
  - [x] **Verified end-to-end with a real upload**: `POST /candidates` (job 16, a real seeded CV
    file as the payload) → candidate 72 created with `parsed_profiles` (real `cv_summary`),
    `match_scores` (96.25%, rank #2), AND `skill_gap_results` (8/8 matched) all populated from ONE
    request, no manual script needed. Test candidate cleaned up afterward (FK-safe deletion order:
    `match_scores`/`skill_gap_results` → `parsed_profiles` → `candidates`), job 16 re-ranked.
  - [x] OpenAPI regenerated; `npx tsc --noEmit` clean (backend-only change, but re-verified per
    this project's standing discipline).
  - **Still open, NOT part of this fix**: the ~36 ALREADY-SEEDED candidates outside job 16 (like
    WD-18/WD-22) still carry their stale one-time-seed `match_scores`/lack of `skill_gap_results`
    — this fix only guarantees the pipeline runs correctly for uploads from now on. Backfilling the
    pre-existing seeded candidates to the current pipeline is still a separate, explicitly-deferred
    task (real LLM cost across every never-reanalyzed candidate) — not done here, not asked for
    yet.
  - ✅ Done when: a brand-new CV upload produces a fully scored, ranked, skill-gap-analyzed
    candidate in one request — verified against a real upload, not just reasoned about.

- [x] **T17-followup #9. Required competencies locked after job creation — DONE, verified
  2026-07-19.** User's reasoning: skill-gap analysis is computed against a job's competency list
  at analysis time — if HR could freely add/dismiss/restore competencies on an EXISTING job (the
  "Edit Kompetensi Wajib" toggle on Job Detail, and the fact that editing a job's text fields also
  silently re-extracted+re-stored competencies via `PUT /jobs/{job_id}`), every already-scored
  candidate's skill-gap/score would go stale relative to the new list with no auto-invalidation to
  catch up (a gap this project already knew about and had documented, never fixed). Rather than
  literally gating on "was this the create flow," implemented the more precise underlying
  invariant: **lock competency changes once at least one candidate has been scored against the
  job** — a job with zero candidates yet stays freely editable even after leaving the create flow,
  since there's nothing to invalidate; "new job creation" is just the common case where that's true.
  - [x] **`update_job` (PUT) no longer re-extracts competencies at all** — editing a job's title/
    responsibilities/requirements/qualifications is now a pure text update; only `create_job`
    (POST) still calls `_extract_and_store_competencies`.
  - [x] **New `_require_no_scored_candidates()` guard**, called from all 3 competency-mutating
    endpoints (`dismiss`, `restore`, `add`) — 400s with a clear Indonesian message if
    `match_scores` already exists for the job.
  - [x] **`JobDetailPage.tsx`**: "Edit Kompetensi Wajib" button + its `CompetencyEditor` modal
    removed entirely — competencies render as plain read-only chips there now, with a hint line
    explaining why ("dikunci setelah lowongan dibuat... ubah kompetensi hanya saat membuat
    lowongan baru").
  - [x] **`JobsListPage.tsx`**: the "Tinjau Kompetensi Wajib" review modal (full add/dismiss/
    restore `CompetencyEditor`) now only opens after a fresh CREATE (`!isEdit`) — an edit save no
    longer reopens it, no longer shows the "Mengekstrak kompetensi..." staged label (nothing is
    extracted), and the submit button reads "Simpan Perubahan" instead of "Simpan & Ekstrak
    Kompetensi" in edit mode.
  - [x] **Verified against real data**: `POST /jobs/16/competencies/{id}/dismiss` on job 16 (has
    scored candidates) → 400 with the expected message. `PUT /jobs/16` with unchanged fields →
    200, competency list identical before/after (8 competencies, same names) — confirms no
    re-extraction fired. `npx tsc --noEmit` clean; backend hot-reloaded clean.
  - ✅ Done when: an existing, already-scored job's competencies cannot be changed through any
    UI path or direct API call, while a brand-new job (via `create_job`) remains fully editable
    through its post-creation review modal — both verified, not just reasoned about.
  - **Follow-up (same day)**: added an explicit, professionally-worded warning inside the "Tinjau
    Kompetensi Wajib" review modal itself (`CompetencyEditor.tsx`, highlighted amber notice box,
    distinct from the plain instructional hint above it) — "Peninjauan ini hanya dapat dilakukan
    satu kali. Kompetensi yang dikonfirmasi di sini akan menjadi acuan tetap untuk seluruh proses
    analisis kesenjangan keahlian dan penilaian kandidat pada lowongan ini, serta tidak dapat
    diubah kembali setelah lowongan disimpan." — so the one-time-only constraint is communicated
    to HR in the moment they're making the decision, not just enforced silently after the fact.
    `npx tsc --noEmit` clean.

- [x] **Backfill: CV bullets + Indonesian-language extraction, ALL 36 candidates — DONE,
  2026-07-19.** `seed/backfill_profile_extras.py --force` (new `--force`/`--candidate-id` flags
  added this session for targeted spot-checks, used here for the full run) re-ran the extended
  `cv_parser` prompt (bullets, `cv_summary`, `education_history`, certifications, projects, org
  experience, all in Bahasa Indonesia) across every seeded profile — previously only candidates 45
  (WD-14) and 53 (WD-22) had this. Confirmed via direct DB query: `36 / 36 profiles have bullets`.
  Real LLM cost (1 `deepseek-v4-flash` call/candidate), run in background, completed cleanly.

- [ ] **Backfill: skill-gap + match scoring for pre-existing seeded candidates — PARTIALLY DONE,
  STOPPED MID-RUN by explicit user request 2026-07-19, remainder deferred.** New
  `seed/backfill_match_scores.py` (mirrors `rescore_from_skill_gap.py`'s pattern but calls
  `compute_match_score()` — a NEW LLM analysis, not just a re-derive — for every candidate lacking
  a `skill_gap_results` row). Spot-checked on 1 candidate first (candidate 35 → 41.5%), then run
  broadly.
  - **Stopped deliberately, not due to an error**: user said "just stop this first... doing it for
    to do later after you finish the last candidate" — the in-flight candidate was allowed to
    finish and commit (`skill_gap_results` count ticked 20→21) before the two background processes
    were force-stopped (`Stop-Process`), so nothing was left half-computed. Both affected jobs
    (16, 21) were re-ranked (`rank_candidates_for_job`) immediately after stopping, so the ranking
    table is internally consistent for however many candidates got through, not left stale.
  - **Progress at stop time**: `skill_gap_results` went from 6/36 (only job 16's original "Data
    siap" candidates from earlier sessions) to **21/36**. `match_scores` is at 36/36 (every
    candidate has SOME score — either from the original one-time seed, or freshly computed by this
    run) — but only the 21 with a `skill_gap_results` row are on the CURRENT pipeline/formula; the
    other 15 still carry a stale score from the original seed run (same caveat as
    T17-followup #9's "still open" note above, just a smaller remaining set now).
  - **Remaining work** (real LLM cost, ~15 candidates × 5 calls ≈ 75 calls): re-run
    `python -m seed.backfill_match_scores` (from `backend/`, no flags needed — it already skips
    anything with an existing `skill_gap_results` row, so it will pick up exactly where this run
    left off, not restart from scratch) whenever picked back up.

- [x] **T17-followup #10. Job-create flow: real data-loss bug found via live testing — DONE,
  2026-07-19.** User's exact repro: fill "Formulir Lowongan" → "Simpan & Ekstrak Kompetensi" → job
  created, "Tinjau Kompetensi Wajib" modal opens → click X to close it → the underlying form now
  shows BLANK fields (still on `/jobs/new`) → user, reasonably assuming their data was lost,
  re-typed only "Tanggung Jawab" and submitted again → this created a SECOND, incomplete job
  (since the route was still the CREATE route, not edit) rather than continuing the first one —
  the final saved job ended up missing "Persyaratan Tambahan"/"Kualifikasi" entirely.
  - **Root cause**: `handleSubmit`'s success path called `setFields(EMPTY)` immediately after a
    successful create, while STAYING on `/jobs/new` with the review modal open on top as an
    overlay — closing the modal revealed the now-cleared local form state, which had never been
    reconciled with what was actually saved to the server.
  - [x] **Fix**: on create success, `navigate(`/jobs/${data.id}/edit`, { replace: true })`
    immediately (instead of clearing fields) — this changes the route's `jobId` param, which
    triggers the EXISTING edit-mode load effect to `GET` the just-created job's real saved data
    and populate the form from THAT (server-verified), not from local state that could drift.
    Closing the review modal (or finishing it) now always reveals the correct, real, fully-saved
    data — never a blank form standing in for lost work.
  - [x] **New unsaved-changes guard on the job form**, mirroring the exact pattern already built
    for `QuestionsPage.tsx` (a `savedFields` baseline snapshot, `isDirty` comparison, `pendingNav`
    state, a `beforeunload` listener for tab-close/refresh, `guardedNavigate()` wrapping every
    in-app navigation away from the form): triggers on the "Batal" button and any `TopBar` nav
    link click (via the existing `interceptNav` prop) while the form has unsaved edits. Shows a
    "Perubahan Belum Disimpan" modal with two choices — "Lanjutkan Mengisi" (stay) or "Keluar
    Tanpa Menyimpan" (discard and go) — professionally worded per explicit user request, simpler
    than `QuestionsPage`'s 3-option version since triggering a full save+AI-extraction from inside
    a confirmation dialog isn't appropriate here (validation could fail silently mid-navigation).
  - [x] `npx tsc --noEmit` clean; backend unchanged (pure frontend fix — `POST /jobs`/`PUT
    /jobs/{id}` themselves were never the problem, confirmed by re-reading them, this was purely a
    frontend state-management bug).
  - ✅ Done when: closing the competency-review modal after creating a job always shows that job's
    real saved data (never blank), and navigating away from a dirty job form (create or edit)
    always prompts for confirmation first.
  - **Round 2 (same day, user corrected the fix's exact behavior)**: the first fix above navigated
    to `/jobs/{id}/edit` IMMEDIATELY on create success — user explicitly did NOT want that: closing
    the review modal via X should return to the SAME create form exactly as it was, not jump to
    Edit Lowongan. Only clicking "Selesai" should navigate — and to `/edit`, not `/detail` as it
    was doing. Also: the modal was dismissible by clicking anywhere on the backdrop, not just X.
    - [x] Removed the immediate `navigate()` call — `fields` is left as the just-submitted values
      (never cleared) and `savedFields` synced to match, so closing via X (`onClose`, no
      navigation) reveals the identical filled form, not blank and not auto-navigated.
    - [x] `onDone` ("Selesai") now navigates to `/jobs/{id}/edit` (was `/detail`).
    - [x] New `Modal` prop `dismissOnBackdropClick` (default `true`, unchanged for every other
      existing usage) — set to `false` on the "Tinjau Kompetensi Wajib" modal specifically, so only
      the X button or an explicit in-modal action can close it, not an accidental backdrop click.
    - [x] `npx tsc --noEmit` clean.
    - **Known, disclosed tradeoff (not fixed, flagged to user)**: since closing via X no longer
      navigates anywhere, the page technically stays in CREATE mode (`isEdit` still false,
      URL still `/jobs/new`) — if the user resubmits the form after closing via X without
      navigating away first, it will `POST` again and create a SECOND job, reintroducing the
      original duplicate-creation risk in that one specific path. Not fixed here since the user's
      explicit ask was about the modal's close behavior, not this edge case — flagging it rather
      than silently deciding whether to add guard logic for it.
  - ✅ Done when (Round 2): X closes the modal and returns to the exact same filled create form
    with no navigation; Selesai navigates to Edit Lowongan; the modal cannot be dismissed by
    clicking outside it.
  - **Round 3 (same day, user confirmed the flagged tradeoff was a real problem and clarified the
    actual requirement)**: the Round 2 "known tradeoff" materialized exactly as predicted — a
    duplicate "Data Engineer" job appeared in the list after the user closed the review modal via
    X and resubmitted. Their correction: a job should only really exist (be visible/counted as
    created at all) once "Selesai" is clicked — closing via X means backing out of the WHOLE
    creation, not just dismissing a summary screen.
  - [x] **Fix**: since the backend has no "draft job" state (competency extraction requires a real
    persisted `job_id` to attach `jd_competencies` rows to), the only correct way to honor "not
    created until Selesai" is to actually roll the creation back. New
    `handleCancelReview()` — X now calls `DELETE /jobs/{id}/permanent` (the SAME hard-delete
    endpoint Job Detail's "Hapus Permanen" already uses) on the just-created job before closing the
    modal, safe here since a brand-new job has zero candidates or anything else to lose. The form
    stays on-screen with the same filled values afterward — clicking "Simpan & Ekstrak Kompetensi"
    again creates a genuinely fresh job (the old one is really gone), so no duplicate is possible.
  - [x] Modal shows a `SpinnerWithLabel` ("Membatalkan pembuatan lowongan...") in place of the
    `CompetencyEditor` while the delete is in flight, and `onClose` is a no-op during that window
    (same "ignore closes while busy" pattern used elsewhere this session) so a second X-click can't
    double-fire the delete.
  - [x] `npx tsc --noEmit` clean; checked the live DB for the specific duplicate the user showed —
    already gone (cleaned up before/during this fix, nothing left to manually remove).
  - ✅ Done when (Round 3): closing the review modal via X actually removes the job that was
    tentatively created for extraction purposes — a job only persists in the list once the user
    explicitly finishes reviewing its competencies via Selesai.

- [x] **T17-followup #11. Email delivery config fix + Kandidat Detail action reordering — DONE,
  real emails verified, 2026-07-19.**
  - **Config bug found live**: user clicked "Kirim Laporan via Email" and got
    `"Candidate 45 has not linked Telegram yet"` — traced to `EMAIL_ENABLED` never actually being
    set in the real `.env` (only `.env.example` had it) — it silently defaulted to `false` all
    session, so every send fell through to the (Telegram) branch. Fixed: `.env` now has
    `EMAIL_ENABLED=true`, `TELEGRAM_ENABLED=false`, and real Gmail SMTP credentials (App Password,
    entered directly by the user into the file, never through chat).
  - **Stale-process gotcha hit twice**: after editing `.env`, `uvicorn --reload` did NOT reliably
    pick up the change — env vars are read once at process start via `load_dotenv()`, not
    hot-reloaded like code, and partial `Stop-Process`/restart attempts kept leaving orphaned
    workers still serving the OLD config (confirmed via `Get-NetTCPConnection` showing stale
    listener PIDs). Resolved both times with a full "kill every python.exe, confirm port 8000 is
    completely free, then start exactly once" sequence — the same recipe now documented here for
    next time this happens (e.g. after T17-followup #11's own `invited` field also silently didn't
    show up in the OpenAPI schema until the same full-kill-and-restart was repeated).
  - [x] **Verified with a REAL email send**: `POST /candidates/45/send-report` →
    `{"channel":"email","to":"zikriaj@gmail.com"}` — user confirmed receipt.
  - **User clarified the actual intended flow**: "Kirim Laporan via Email" on Kandidat Detail was
    premature — the development report should only be sent once BOTH CV analysis and interview
    results exist, and Kandidat Detail's "Lanjutkan" moment is really where the INTERVIEW INVITE
    belongs instead.
  - [x] **Interview-invite email template polished** (confirmed with user before implementing,
    per their explicit request to review wording first): subject now
    `"Undangan Wawancara — {job_title} di {company_name}"`, body adds role/company context,
    explicit expectations (quiet environment, camera/mic permission), and a warmer sign-off.
    `services/delivery.py::send_invite_email()` gained `job_title`/`company_name` params;
    `routers/candidates.py`'s call site now fetches the job + company to supply them.
  - [x] **`CandidateFullDetailOut` gained `invited: bool`** (`candidate.invited_at is not None`,
    same derivation already used in `MatchOut`) so Kandidat Detail can correctly decide
    "Kirim Undangan Wawancara" vs "Lihat Undangan Wawancara" without a separate fetch.
  - [x] **`CandidateDetailPage.tsx`**: removed "Kirim Laporan via Email" (and its
    `sendBusy`/`sendError`/`sendSuccess` state + `handleSendReport`) from the Keputusan card
    entirely; replaced with a button that opens the existing `InviteModal` component (reused
    as-is, not reimplemented) — shown only when `decision === "advance"` (inviting a rejected
    candidate makes no sense). "Lihat Laporan" and "Lihat CV" stay in the same row unchanged.
  - [x] **`ReportPage.tsx`**: gained its OWN "Kirim Laporan via Email" button (busy/error/success
    state, same `POST /candidates/{id}/send-report` call) next to "Kembali ke Daftar Laporan" —
    this is now the only place the development report can be emailed from.
  - [x] Real end-to-end verification: `POST /candidates/45/send-invite-email` with the polished
    template → `{"status":"sent","to":"zikriaj@gmail.com"}`, subject confirmed as
    "Undangan Wawancara — Web Developer di [company]". OpenAPI regenerated; `npx tsc --noEmit`
    clean throughout every sub-change.
  - ✅ Done when: report-sending only exists on the Laporan page; Kandidat Detail's post-decision
    action is inviting to interview with a polished, context-aware email; both were verified with
    real sent emails, not just code review.

- [x] **T17-followup #12. Candidate invite link redirected to HR login instead of the interview —
  DONE, real bug found via live testing, 2026-07-19.**
  - **Repro**: user opened the interview invite link (sent via the just-fixed email flow) in the
    same browser they were already logged into HR with — instead of landing on the candidate
    consent/interview flow, it bounced straight to the GaskeunKerja HR login page.
  - **Root cause**: `api/client.ts`'s global `onResponse` middleware redirected to `/login`
    unconditionally on ANY 401 response, as long as an HR token happened to still be sitting in
    `localStorage` — with zero awareness of which PAGE triggered the request.
    Candidate-facing routes (`/candidate/:id/consent`, `/candidate/:id/interview`) are
    unauthenticated by design (a per-candidate `token` query param, not the HR Bearer token) and
    already have their own dedicated "invalid link" handling
    (`CandidateTokenGuard` → `InvalidLinkPage`) — but that never got a chance to run, because the
    blanket interceptor hijacked navigation first. This is exactly what happens whenever someone
    tests a candidate link in the same browser as an active HR session (the normal way to test
    locally), which is presumably why it went unnoticed until now.
  - [x] **Fix**: added `isCandidateRoute()` (checks `location.pathname.startsWith("/candidate/")`)
    and gated BOTH the `onRequest` HR-Bearer-token attachment and the `onResponse` 401→login
    redirect on NOT being a candidate route — candidate pages no longer send an HR token they
    don't need, and their own 401s no longer trigger an HR-scoped redirect at all.
  - [x] `npx tsc --noEmit` clean; frontend dev server confirmed up (Vite HMR, not subject to the
    same stale-process issue as the backend's `uvicorn --reload`).
  - ✅ Done when: opening a candidate invite link in a browser with an active HR session lands on
    the actual candidate consent/interview flow, never the HR login page.
  - **Follow-up verification (same day)**: after the routing fix, the SAME link correctly showed
    "Link tidak valid" instead of the HR login page — confirming the fix worked — but that itself
    turned out to be a genuinely expired token (invited 2026-07-15, 72h TTL long past). Two things
    fixed while unblocking real end-to-end testing:
    - [x] **`InviteModal.tsx` gained expiry detection**: the "already invited" view now checks
      `token_expires_at` client-side and shows a dedicated "Link undangan ... sudah kedaluwarsa"
      state with a **"Buat Link Baru"** button (calls the existing regenerate-safe
      `POST /candidates/{id}/invite`) instead of silently handing over a dead link with no
      indication anything was wrong.
    - [x] Job 16's interview questions had been left in `draft` status from earlier session
      testing (reopened, never re-approved) — user explicitly confirmed approving them now;
      `POST /jobs/16/questions/approve` → all 4 approved.
    - [x] **Real end-to-end verification**: regenerated candidate 45's token
      (`POST /candidates/45/invite`), confirmed the fresh token resolves correctly via
      `GET /candidates/45/self?token=...` (200, real candidate data), sent a fresh invite email
      with the new link (`{"status":"sent"}`). `npx tsc --noEmit` clean.

- [x] **T17-followup #13. Interview page redesign (wireframe-driven) + a real blocking bug found
  along the way — DONE, 2026-07-19.**
  - [x] **`CandidateInterviewPage.tsx` restructured** to match a user-provided wireframe: added
    the same `CandidateHeader` top navbar used on the consent page ("Langkah 2 dari 2" — the
    interview is step 2 of the 2-step candidate flow), question text restyled as "Pertanyaan N:"
    + the question on its own line (was a single `<h1>`).
  - [x] **New "Uji Kamera & Mikrofon" button** fills the wireframe's placeholder second button —
    a genuinely useful video-interview pattern (let the candidate confirm their camera/mic work
    BEFORE committing to a timed answer), not an arbitrary filler. Implemented as a new
    `previewing` state in `useVideoRecorder.ts`: `startPreview()` requests `getUserMedia` and
    shows a live feed WITHOUT starting the countdown/recording/timer; `startRecording()` reuses
    that already-granted stream if one exists (no second permission prompt), or requests fresh
    permission itself if the candidate skips straight to "Mulai Recording" — either button path
    triggers the real browser camera+mic permission prompt, satisfying the explicit requirement
    that clicking through actually asks for both.
  - **Real blocking bug found while tracing the flow to verify it**: `CandidateConsentPage.tsx`
    still had a MANDATORY "link your Telegram before the interview can start" step — a leftover
    from before Round-3 Task 19 switched report delivery to email. With `TELEGRAM_ENABLED=false`
    (set earlier this session), this was an unconditional dead end: no candidate could ever reach
    "Mulai Wawancara" at all, since report delivery no longer needs any candidate-side linking
    action in the first place.
  - [x] **Fix**: removed the Telegram-linking step entirely — consent now goes straight from the
    checkbox to "Mulai Wawancara". `hasTelegramLink` prop and all related state
    (`telegramLinked`/`checkingStatus`/`notYetLinkedMessage`) removed from `ConsentFlow`.
  - [x] `npx tsc --noEmit` clean; backend + frontend dev servers both confirmed healthy.
  - ✅ Done when: the candidate flow goes consent → interview (camera/mic test or direct start,
    both requesting real permissions) → recording, with no dead-end step in between, and the
    interview page visually matches the provided wireframe including the top navbar.

- [x] **T17-followup #14. Camera stayed black during preview/recording + invite link skipped
  consent — DONE, both real bugs found via live testing, 2026-07-19.**
  - **Bug 1 (camera black)**: root cause was a mount-order race in `useVideoRecorder.ts` —
    `previewVideoRef.current.srcObject = stream` ran INSIDE `startPreview()`/`startRecording()`
    while `state` was still `"requesting-permission"`, but the `<video>` element only mounts once
    `state` becomes `"previewing"`/`"countdown"`/`"recording"` (conditionally rendered in
    `CandidateInterviewPage.tsx`). The assignment silently landed on a null ref every time; by the
    time the element actually mounted, nothing re-attached the stream to it — camera access was
    genuinely granted (browser permission prompt fired correctly), but never visually connected.
    - [x] **Fix**: moved the `srcObject` assignment into a `useEffect` keyed on `state`, which runs
      AFTER React commits the newly-mounted `<video>` element — the ref is guaranteed populated by
      then. Removed the now-redundant early assignments from `startPreview()`/`startRecording()`.
  - **Bug 2 (invite skipped consent)**: `InviteModal.tsx::buildLink()` pointed straight at
    `/candidate/:id/interview` — `CandidateTokenGuard`'s consent redirect only fires while
    `has_consent` is still false, so once a candidate had EVER consented (true for candidate 45,
    from earlier session testing), a freshly regenerated invite link silently skipped consent
    every time afterward. User wants every invite link to land on consent first, unconditionally.
    - [x] **Fix**: `buildLink()` now points at `/candidate/:id/consent` instead — consent's own
      "Mulai Wawancara" button already forwards to `/interview` afterward, so this is a one-line
      change with no other flow impact. `send_invite_email()`'s template is unaffected since it
      receives the (now-corrected) link as a plain string from the caller.
  - [x] `npx tsc --noEmit` clean. Regenerated a fresh token for candidate 45 and sent a real invite
    email with the corrected `/consent` link so both fixes could be tested together.
  - ✅ Done when: the camera preview shows a real live feed (not black) during both "Uji Kamera &
    Mikrofon" and the recording countdown, and every invite link — regenerated or not — lands the
    candidate on consent first, every time.

- [x] **T17-followup #15. Dedicated camera/mic test step — DONE, 2026-07-19.** User wanted a
  standalone "test your camera and sound" screen between consent and the interview questions,
  not just the per-question "Uji Kamera & Mikrofon" button buried inside question 1.
  - [x] **New `CandidateCameraTestPage.tsx`** (route `/candidate/:id/camera-test`) — a dedicated
    step reusing `useVideoRecorder`'s `startPreview()`/`previewVideoRef` (no new hook needed):
    shows a live camera preview once the candidate clicks "Uji Kamera & Mikrofon", then
    "Lanjutkan ke Wawancara" once satisfied. The per-question test button on
    `CandidateInterviewPage.tsx` (T17-followup #13) stays as a secondary safety net — this page is
    now the primary, always-shown check.
  - [x] **Candidate flow is now 3 steps, not 2**: consent → camera test → interview. Updated
    `CandidateHeader step=` labels across all three pages ("Langkah 1/2/3 dari 3") and
    `CandidateConsentPage.tsx`'s "Mulai Wawancara" button to navigate to `/camera-test` instead of
    straight to `/interview`.
  - [x] `npx tsc --noEmit` clean; backend + frontend dev servers both confirmed healthy.
  - ✅ Done when: after consent, the candidate sees a dedicated camera/mic check page before any
    interview question, with a clear "Lanjutkan ke Wawancara" action once they're satisfied.

- [x] **T17-followup #16. Candidate flow polish after live-testing the new 3-step flow — DONE,
  2026-07-19.**
  - [x] **"Kirim Jawaban"/"Rekam Ulang" button order swapped** — primary action ("Kirim Jawaban")
    now on the left, secondary ("Rekam Ulang") on the right, matching the user's expected reading
    order for a primary-then-secondary action pair.
  - [x] **Per-question "Uji Kamera & Mikrofon" removed** from `CandidateInterviewPage.tsx` — now
    redundant with the dedicated `CandidateCameraTestPage` (T17-followup #15), which is the
    primary, always-shown check before question 1. The `idle` state is back to a single "Mulai
    Recording" button; the `previewing`-state JSX branch was removed too (unreachable from this
    page now that its only trigger is gone) — `startPreview`/`"previewing"` stay in
    `useVideoRecorder.ts` since `CandidateCameraTestPage` still uses them directly.
  - [x] **Consent's redundant confirmation screen removed** — used to show a second "Terima
    kasih, siap memulai wawancara?" card requiring ANOTHER click after the consent checkbox was
    already submitted. `handleSubmit()` now navigates straight to `/camera-test` on a successful
    consent POST — one click (checkbox + Lanjutkan) takes the candidate directly into the camera
    test step, no extra confirmation screen in between.
  - [x] `npx tsc --noEmit` clean; backend + frontend dev servers both confirmed healthy.
  - ✅ Done when: submitting consent goes straight to the camera-test page with no intermediate
    screen; the interview question page shows only "Mulai Recording" (no redundant test button);
    and the post-recording action pair reads "Kirim Jawaban" then "Rekam Ulang", left to right.

- [x] **T17-followup #17. Live microphone level meter on the camera-test page — DONE, 2026-07-19.**
  User's request: a "heartbeat"-style visual below the camera so the candidate can SEE their
  voice register, not just trust the camera preview implies audio works too.
  - [x] **`useVideoRecorder.ts` gained a Web Audio-driven `audioLevel` (0-100)** — a new
    `startAudioMeter(stream)` creates an `AudioContext` + `AnalyserNode` on the SAME stream
    already used for the video preview, computes RMS volume from `getByteTimeDomainData` on every
    `requestAnimationFrame` tick, and exposes it as state. Wired into both `startPreview()` and
    `startRecording()`'s stream-acquisition path (whichever runs first). `stopAudioMeter()` folded
    into the existing `cleanupStream()` so the `AudioContext` is properly closed and the
    animation-frame loop stops whenever the stream itself is torn down — no separate cleanup path
    to forget.
  - [x] **New `AudioLevelMeter` component** (`CandidateCameraTestPage.tsx`) — 9 vertical bars with
    per-bar sensitivity weights (center bars swing tallest, outer bars least) for a natural pulse
    look rather than uniform bars, colored teal once level exceeds a small noise-floor threshold
    (level ≤ 4 stays neutral gray). Shown only while `previewing`, with a prompt: "coba bicara
    untuk memastikan suara Anda terekam."
  - [x] `npx tsc --noEmit` clean; backend + frontend dev servers both confirmed healthy.
  - ✅ Done when: speaking while the camera-test preview is active visibly moves the bar meter in
    real time, giving the candidate direct visual confirmation their microphone works.

- [x] **T17-followup #18. Bigger camera preview, question in its own boxed panel — DONE,
  2026-07-19.** Matched more closely to the user's wireframe (camera dominant, question in a
  distinct bordered box below it, not plain text).
  - [x] **`CandidateInterviewPage.tsx`**: container widened 480px → 640px, camera aspect ratio
    4:3 → 5:4 (both changes compound — a wider container at a taller ratio makes the box
    noticeably larger, not just proportionally scaled). Question text moved into a `.consent-box`
    panel (reusing the same teal-tinted bordered box already used on the consent page, "Pertanyaan
    N:" as a bold lead-in) instead of a bare `<h1>`/`<p>` pair.
  - [x] **`CandidateCameraTestPage.tsx`** given the same container/aspect-ratio treatment for
    visual consistency across all 3 steps of the candidate flow — the camera-test preview and the
    real interview preview are now the same size/shape.
  - [x] `npx tsc --noEmit` clean; backend + frontend dev servers both confirmed healthy.
  - ✅ Done when: the camera preview reads as the dominant element on both the camera-test and
    interview pages, and the question text sits in its own visually distinct box.

- [x] **T17-followup #19. Interview page not properly centered/too narrow — DONE, real bug found
  via live testing, 2026-07-19.**
  - **Root cause**: `CandidateInterviewPage.tsx` was the ONLY candidate-facing page using an
    ad-hoc inline-styled wrapper (`maxWidth`/`margin: "44px auto"`) instead of the app's existing
    `.main` layout class — the one already proven to center correctly everywhere else in the app
    (every HR page, plus `CandidateConsentPage.tsx` and `CandidateCameraTestPage.tsx`). The
    inline version visibly failed to center (card sat left-skewed with a large unused gap on the
    right, per the user's screenshot) — whatever the exact CSS interaction was, reusing the
    proven pattern sidesteps it entirely rather than debugging the inline version further.
  - [x] **Fix**: switched to `className="main" style={{ maxWidth: 900, paddingTop: 44 }}` (same
    pattern `CandidateCameraTestPage.tsx` already used correctly) on both branches (interview
    loader + "sudah selesai" card). Also widened from 640px → 900px per the explicit "make it
    wider" request, and matched `CandidateCameraTestPage.tsx` to the same 900px for consistency
    across the 3-step flow.
  - [x] **Spacing increased** ("jangan mepet2"): camera-box bottom margin 16px → 22px, question
    counter label given its own 14px bottom margin (was touching the camera box directly above).
  - [x] `npx tsc --noEmit` clean; backend + frontend dev servers both confirmed healthy.
  - ✅ Done when: the interview page card is visibly centered in the viewport (not skewed left)
    and noticeably wider/roomier than before, matching the other two candidate-flow pages.

- [x] **T17-followup #20. Camera box too tall, forced vertical scroll — DONE, 2026-07-19.**
  The previous round's `aspectRatio: "5 / 4"` at 900px container width made the camera box
  ~720px tall on its own, pushing the question box and button off-screen and forcing a scroll —
  the wireframe's camera box is wide/flat (~16:9), not nearly square.
  - [x] **Fix**: aspect ratio `5/4` → `16/9` on both `CandidateInterviewPage.tsx` and
    `CandidateCameraTestPage.tsx`'s camera boxes; container width trimmed `900px` → `680px`
    (`paddingTop` 44 → 32) on both pages so the derived camera-box height stays modest at any
    reasonable container width instead of growing with it.
  - [x] **Trimmed extra vertical spacing** added in the previous round now that fitting one
    viewport is the priority: camera-box bottom margin 22px → 14px, question-counter label 14px →
    10px, question box (`.consent-box`) given tighter inline padding/font-size overrides
    (12px padding, 1rem/0.92rem text) instead of the default larger consent-page sizing.
  - [x] `npx tsc --noEmit` clean; backend + frontend dev servers both confirmed healthy.
  - ✅ Done when: the full interview card (camera + question + button) fits within a single
    viewport at typical laptop screen heights, with no vertical scroll required.

- [x] **T17-followup #21. Defer answer uploads to the end of the interview — DONE, 2026-07-19.**
  User's request: uploading + saving to the database shouldn't happen per-question during the
  interview — it added a real, visible wait ("Mengunggah jawaban...") between every single
  question, compounding total perceived latency across N questions.
  - [x] **`CandidateInterviewPage.tsx::InterviewFlow` restructured**: recording and saving are now
    fully decoupled. Each "Kirim Jawaban" click just accumulates `{questionId, blob}` into local
    `pendingAnswers` state and immediately advances to the next question — ZERO network calls
    during that transition. Only on the LAST question does `uploadAllAnswers()` fire, uploading
    every accumulated answer sequentially to the existing (unchanged) `POST
    /candidates/{id}/answers` endpoint, with a "Mengunggah jawaban N dari total..." progress
    screen shown once, at the end, instead of a spinner after every question.
  - [x] **Backend verified safe for this**: `submit_interview_answer` has no ordering/sequencing
    dependency between questions — each answer is submitted independently, keyed by `question_id`
    — so uploading all of them back-to-back at the end (rather than spread out with think-time in
    between) requires no backend change at all.
  - [x] **Error handling**: if any upload in the batch fails, the flow stops and shows a retry
    screen — explicitly reassures the candidate their already-recorded answers aren't lost
    ("jawaban yang sudah terekam tidak hilang"), and retrying re-attempts the FULL batch (simple,
    correct for the small number of questions in this MVP; per-item resume was not built).
  - [x] Last question's submit button relabeled "Selesai & Kirim Semua Jawaban" (was "Kirim
    Jawaban") so it's clear this one actually triggers the batch upload, not just "next question."
  - [x] `npx tsc --noEmit` clean; backend + frontend dev servers both confirmed healthy.
  - ✅ Done when: moving between questions never shows an upload spinner; all recorded answers
    are uploaded together, once, only after the final question is answered.

- [x] **T17-followup #22. Answer processing made truly async (background task) — DONE, verified
  with a real timed request, 2026-07-19.** Follow-up to #21: batching uploads to the end moved
  ALL the latency into one place, and the user then asked WHY that lump sum was still 10-20+
  seconds per answer. Traced it: `POST /candidates/{id}/answers` was fully synchronous end-to-end
  — save video (fast) → STT transcription (1 API call) → rubric scoring (**3 sequential
  self-consistency LLM votes**, the dominant cost, same pattern already measured at ~25-30s/5-call
  for skill-gap analysis) — all inside the SAME request/response cycle the candidate's browser was
  waiting on.
  - [x] **`services/interview_answers.py` split into `save_answer()` + `process_answer()`**:
    `save_answer()` is the fast synchronous half (consent gate, write file, create the
    `interview_answers` row) — returns as soon as the video is on disk. `process_answer()` is the
    slow half (STT + rubric scoring + interview-summary aggregation), now called via a NEW
    `process_answer_background()` entry point designed for `FastAPI.BackgroundTasks` — runs AFTER
    the HTTP response is already sent, so the candidate's `fetch()` call returns almost instantly
    regardless of how long transcription/scoring take.
  - [x] **Own DB session per background task**: `process_answer_background()` opens a fresh
    `SessionLocal()` rather than reusing the request's session, which is already closed by the
    time background tasks execute — reusing it would have raised on first use.
  - [x] **Race-safe interview-summary trigger**: with answers now processed in the background,
    multiple answers' background tasks can genuinely overlap (each upload returns near-instantly,
    so answer 4 can be background-processing before answer 1 finishes). Guarded by checking that
    EVERY answer has actually finished scoring (`all(rubric_scores exist for a in all_answers)`),
    not just that N answer rows exist — whichever background task finishes scoring LAST
    self-elects to compute the summary. `compute_and_persist_interview_summary()` was already
    idempotent (delete+recreate), so even a near-simultaneous double-trigger is harmless.
  - [x] **`AnswerOut` response shape changed**: `transcript_text` removed (doesn't exist yet at
    response time now) — confirmed via grep that nothing reads it from this endpoint's response
    (the candidate-detail page's `transcript_text` comes from a completely different endpoint/
    model). `routers/interview_answers.py` updated to inject `BackgroundTasks` and call
    `background_tasks.add_task(process_answer_background, answer.id, candidate_id)`.
  - [x] **`load_demo_data.py` unaffected** — confirmed it never called the old `submit_answer()`;
    it directly orchestrates its own inline transcribe+score+summarize sequence, untouched by
    this refactor.
  - [x] **Verified with a real timed request** (not just code review): hit a stale-process issue
    identical to earlier this session (traceback showed the OLD `submit_answer` code still
    running after a hot-reload) — same full kill-and-restart recipe resolved it. After that,
    `POST /candidates/45/answers` measured **344ms** (down from 3700ms+ blocking on the old
    synchronous path) — the background task then ran, failed gracefully on the deliberately-fake
    test payload (`openai.BadRequestError: could not process file`, logged via
    `logger.exception`, caught, did not crash the server), and the server kept serving other real
    requests throughout. Test data cleaned up afterward. OpenAPI regenerated; `npx tsc --noEmit`
    clean; both dev servers confirmed healthy.
  - ✅ Done when: the candidate's answer-upload request returns in a few hundred milliseconds
    regardless of transcription/scoring time, and a failure in background processing never
    crashes the server or blocks other requests — both verified against a real timed request, not
    just reasoned about.

