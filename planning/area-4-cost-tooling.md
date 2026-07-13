# Area 4 — Lowest-Cost / Free Execution (Local Tooling)

> **Resolved 2026-07-12 (solo/1-week) — DECISIONS LOCKED:** set up dev env FIRST (Day 1). **All LLM via SumoPod + caching** (`https://ai.sumopod.com/v1`, OpenAI-compat; `deepseek-v4-flash`/`deepseek-v4-pro`) — local-LLM substitution **cut** (T4). **STT = Groq `whisper-large-v3` API** (`id`; free tier) — API-based, not local (T5). Embeddings = local **multilingual** sentence-transformers. Frontend on host; DBs in Compose. **Report delivery = Telegram Bot API only — no email/SMTP** (T3c/T7, dropped 2026-07-12: less setup, more reliable than cold-sent Gmail). **Env: `../.env.example` (created, no EMAIL/SMTP vars).** Machine confirmed: Win11, Ryzen 7, 24GB, RTX 3050, Docker OK, Py3.11.
>
> **Resolved 2026-07-12 (Area-3 session, revised):** ~~Tesseract OCR + poppler~~ **dropped per user
> instruction** — replicating the `NalarX-ai-engine` pattern instead: `pypdf` text extraction +
> embedded-image extraction + **vision-LLM captioning** for scanned/image pages (no OCR system
> binary, no new install). New Area 4 task T3d (vision-LLM client). **Vision endpoint = SumoPod
> primary** (verify live with the API key on Day 1 — vision support unconfirmed via docs), **Groq
> vision model as documented fallback** (reuses the STT client already being built).
>
> **Resolved 2026-07-12 (gap-closing pass):** **Interview audio format = WebM (Opus), universal** —
> native `MediaRecorder` output, no transcoding, Groq accepts it directly. **Kaggle CV sourcing is
> manual for now** — no `kaggle` API/credential this week; drop files into `../seed/raw/cv/` and
> `../seed/raw/audio/` (both created) by hand. `.env.example` gained `VISION_PROVIDER`/`VISION_MODEL`.
> Live task status + steps: `execution-checklist.md` → Area 4.

**Goal:** build and run the entire MVP for as close to $0 as possible. Nearly everything is free/local — the only cost lines are SumoPod tokens (pennies with caching) and Groq STT (likely $0 on free tier).
**Principle:** local-first, open-source-first. Pay only where quality genuinely requires it.

## Free/Local Stack Confirmation

| Need | Tool | Cost |
|---|---|---|
| Frontend | React + Vite (on host) | $0 |
| Backend | FastAPI + uvicorn | $0 |
| Structured DB | PostgreSQL (Docker) | $0 |
| Vector DB | Qdrant OSS (Docker) | $0 |
| File storage | Local filesystem (CV + audio) | $0 |
| Embeddings | sentence-transformers, multilingual (local) | $0 |
| Speech-to-text | **Groq `whisper-large-v3` API** (`id`) | ~$0 (free tier) |
| Report delivery | **Telegram Bot API** (`sendDocument`/`sendMessage`) — only channel, no email | $0 |
| Orchestration | Docker Compose | $0 |
| **LLM** | **Deepseek Flash/Pro via SumoPod API** | **the one real cost (small + cached)** |

## Task List (first draft)

- [ ] T1. Confirm the local-first stack above; lock versions.
- [ ] T2. Set up Docker Compose to run everything (Postgres + Qdrant + backend + frontend) with one command — reproducible dev env for the whole team.
- [ ] T3. LLM cost strategy: estimate token usage for a full demo run; add response caching so re-runs don't re-bill; batch where possible. **Include a `bypass_cache` param** the client honors (resolved 2026-07-12) — Area 5's determinism tests (T3/T4) need genuinely independent calls, not cached replays.
- [ ] T4. **[cut]** Local-model substitution for LLM steps — negligible saving vs solo hours; all steps stay on SumoPod + caching.
- [ ] T5. **STT = Groq `whisper-large-v3` API** (`language=id`), OpenAI-compatible via `openai` SDK + base_url. Local faster-whisper is the drop-in fallback (RTX 3050).
- [ ] T3d. **Vision-LLM for scanned-CV pages** — `pypdf` extraction + embedded-image captioning (transcribe/describe modes), replicated from `NalarX-ai-engine`. No Tesseract/OCR binary. **SumoPod primary (verify Day 1), Groq vision model fallback.**
- [ ] T6. Use local **multilingual** sentence-transformers for embeddings (free) instead of a paid embedding API.
- [ ] T7. Report delivery: **Telegram Bot API only** — `sendDocument` (file) + `sendMessage` (summary); no email/SMTP (dropped for setup effort + spam-deliverability risk).
- [ ] T8. Produce the true minimal cost estimate for the MVP (expect: ~$0 fixed + a small Deepseek API bill, minimizable with caching). Flag anything that unavoidably costs money.

## Decisions — RESOLVED
- LLM endpoint → **SumoPod** (OpenAI-compat), `deepseek-v4-flash` / `deepseek-v4-pro`, + caching. Key: user has it.
- STT → **Groq `whisper-large-v3` API** (`id`), free tier. Needs a free Groq key.
- ~~Compose vs bare-metal~~ → **Docker Compose for DBs**, **frontend on host** (Vite hot-reload).
- Report delivery → **Telegram Bot API only**; email/SMTP dropped entirely (2026-07-12) — less setup than Gmail App Password + MIME attachments, more reliable than cold-sent email (no spam-filter risk).
- Env file → **`../.env.example` created**; copy to `.env` with real keys.

## Note
This area is cross-cutting: set up the dev env (T2) first, since Areas 2/3 build on top of it. The "cost" framing largely collapses to "keep it local" now that cloud is out of scope for this phase — cloud costing (the `infra comparison A vs B.md` numbers) becomes relevant again only at the post-MVP deployment stage.
