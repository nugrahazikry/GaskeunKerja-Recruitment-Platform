# DIGDAYA 2026 — Tahap 3 Implementation Planning Agent

## Context

- **Competition**: DIGDAYA 2026, Tahap 3 (final round). Team **P0804 — Keprof Reborn**.
- **Deadline**: ~2026-07-26 (2 weeks from 2026-07-12). Verify exact date.
- **Chosen solution**: **Direction B — GaskeunKerja for Business** (company-focused AI recruitment platform). The direction decision, rationale, and full spec are DONE — see the source-of-truth docs below. This session is **not** about re-deciding direction; it's about **planning and executing the MVP build**.

## The Hard Constraint For This Phase: LOCAL MVP, NO CLOUD

The user is building the MVP **locally, without any cloud deployment/hosting infrastructure** at this stage. Every cloud service in the Direction B architecture is replaced by a local/free equivalent:

| Direction B (cloud) design | MVP local substitute |
|---|---|
| Cloud Run / GKE (hosting) | Local `uvicorn` (FastAPI), optional Docker Compose |
| BigQuery (tabular DB) | **Local PostgreSQL (Docker) or SQLite** |
| GCS (object storage: CV, audio) | **Local filesystem** |
| Qdrant (managed) | **Local Qdrant (Docker, OSS — free)** |
| Google Speech-to-Text | **Local Whisper (open-source — free)** |
| Cloud Load Balancing / Armor / CDN | Not needed for MVP |
| Managed email | Free SMTP tier / mock for demo |

**Do not plan cloud deployment, autoscaling, GKE, Cloud Run, BigQuery, or GCS work in this phase.** If a cloud step seems necessary, flag it as "post-MVP" instead. The one likely-unavoidable external dependency is the **Deepseek LLM API** (can't be self-hosted) — treat minimizing/caching its usage as a cost task, and note where a free local model could substitute.

## Focus Areas For This Session (the 5 planning areas)

Task lists live in the per-area files. Bring them into the brainstorming session and refine:

1. **Frontend UI/UX** → `planning/area-1-frontend.md`
2. **Backend & AI integration** → `planning/area-2-backend-ai.md`
3. **Database management** → `planning/area-3-database.md`
4. **Lowest-cost / free execution (local tooling)** → `planning/area-4-cost-tooling.md`
5. **QA process** → `planning/area-5-qa.md`

`planning/plan.md` is the master: overview, the agreed local stack, cross-area sequencing/milestones, and the live decision log. Keep it as the single source of truth — write conclusions there, not only in chat.

## Source-of-Truth Docs (from the brainstorming phase, in `../brainstorming idea/`)

| File | What it gives you |
|---|---|
| `../brainstorming idea/proposal sekarang/direction B summary.md` | **Master reference** — end-to-end flow, architecture table, full data inventory, Tahap 2 reuse inventory, open risks, mapped to these 5 areas. Read this first. |
| `../brainstorming idea/plan.md` | Full decision log for why Direction B (Stage 1-4 analysis). |
| `../brainstorming idea/new idea/arsitektur direction B.md` | Architecture component list. |
| `../brainstorming idea/new idea/infra comparison A vs B.md` | Cloud cost comparison (reference only — not used in MVP local phase). |
| `../brainstorming idea/proposal sekarang/tahap 3 jawaban.md` | The 27 submission answers (what we're claiming we'll build — the build must match these claims). |
| `../brainstorming idea/proposal sebelumnya/tahap 2 proposal.md` | Tahap 2 spec. |

## Existing Code To Reuse (Tahap 2)

GitHub: `https://github.com/nugrahazikry/AI-Powered-Skill-Gap-Analysis`. Per Tahap 2 "Half Prototype" status:

**⚠️ Corrections (verified 2026-07-12 by reading the actual code — supersedes the bullets below, which were the pre-verification assumption):**
- **Frontend is NOT React** — it's a static site (`index.html`/`style.css`/`script.js`, nginx, no build tooling), branded "SkillGap AI." No React code to reuse, only its visual language. MVP frontend built fresh in React + Vite.
- **LLM is NOT Deepseek — it's Google Gemini** (`gemini-2.5-flash-lite` via `langchain_google_genai` + `google.genai`). Zero Deepseek code anywhere in the repo. The MVP's SumoPod/Deepseek client is built from scratch, no code transfers.
- **Auth is NOT designed-but-unverified — it is confirmed ABSENT.** Zero code: no JWT, no login endpoint, no auth dependency/middleware. All `/api/*` endpoints are fully unauthenticated. Built from scratch for the MVP.
- **Database is NOT designed-but-unverified — it is confirmed ABSENT.** No ORM (no SQLAlchemy), no Postgres/DB container, no migrations. Persistence is an in-memory dict (`_JOBS`), lost on restart. `docker-compose.yml` has only `backend`+`frontend` services, no DB. Built from scratch.
- **⚠️ Security note:** `backend/environment.env` has a live-looking Gemini API key committed in plaintext — rotate if still active; don't repeat this pattern in the MVP's `.env` handling. Also, the global exception handler returns raw Python tracebacks as JSON 500 responses — a pattern to explicitly avoid in the MVP's error handling (Area 2 T15).

**What's actually reusable (verified working, informs MVP estimates in `execution-checklist.md` § Effort & Difficulty Estimates):**
- **CV text extraction** (`pdfplumber` + PyMuPDF-rasterized Gemini-vision OCR fallback for scanned pages) — genuinely solid, validates the "extract text → detect empty → vision fallback" pattern the MVP's Area 2 T5 also uses (via NalarX's per-image approach instead of Tahap 2's whole-page rasterization, and SumoPod/Groq vision instead of Gemini, so it's pattern-reuse not copy-paste, but real time saved).
- **Skill-gap grounding pattern** (`agent_4_recommendation_report.py`: `_build_seed_gap()` / `_is_skill_match()` — deterministic token-overlap seed used to ground/filter LLM output) — a legitimate technique worth adapting for Area 2 T8, even though the underlying match technique (token overlap vs. our semantic+graph approach in T7) doesn't itself transfer.
- **PDF report generation** (`_build_report_pdf()`, ReportLab, ~700 lines, custom flowables for skill chips) — **fully working**. Per 2026-07-12 decision, Area 2 T14 **switches from weasyprint to adapting this ReportLab code** — eliminates the weasyprint Windows Pango/Cairo dependency risk entirely (ReportLab is pure Python) and retires real build time on the hardest part of that task.
- **Docker/async patterns** — functional Dockerfile scaffold and an in-memory async-job/polling pattern (`threading.Lock` + background thread) exist as minor reference points, not direct reuse (no DB to orchestrate; MVP's async needs differ).

**Confirmed NOT reusable (early prototype / wrong technique for the MVP's approach):**
- KGE matching — not present at all (no embeddings/vector-DB/graph code found; grep for "embedding"/"knowledge graph"/"qdrant" returned zero hits). The Tahap 2 "matching" is a token-overlap heuristic, a different technique from the MVP's semantic+graph approach (Area 2 T7) — doesn't transfer.
- Learning roadmap / skill-gap LLM output — functional but fragile (regex + `json.loads` with silent empty-fallback, no schema validation) — a pattern to avoid, not copy, for the MVP's structured-output needs.
- Scraping pipeline — removed in Direction B, and confirmed absent from the codebase anyway.
- Kubernetes infra — replaced by local for MVP.

## How To Work This Session

- **Balanced sparring partner** (same as before): propose task breakdowns AND pressure-test feasibility against the 2-week window and the "local/free" constraint. Flag when a task is bigger than it looks or when a Direction B claim (from `tahap 3 jawaban.md`) risks not being buildable in time.
- **Sequence matters**: identify what blocks what (e.g. database schema + reference datasets block backend AI; backend API contract blocks frontend wiring). Surface the critical path.
- **Every task should trace to the end-to-end flow** in `direction B summary.md` §2. If a task doesn't serve that flow or a submission claim, question it.
- **Keep the MVP honest**: the goal is a working local end-to-end demo for the hackathon (video + pilot-ready), not a production system. Prefer the simplest thing that demonstrates the flow.
- Language: Bahasa Indonesia for anything destined for the submission; English fine for internal planning.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

**⚠️ MANDATORY, not optional — this was skipped once already (2026-07-13, Area 3 T10 seed-data cleanup) and caused a real, avoidable cost: cleaning up FK-linked rows across `candidates`/`match_scores`/`parsed_profiles`/`interview_questions`/`jd_competencies`/`jobs`/`hr_users`/`companies` took 5+ failed `DELETE` attempts, discovering the foreign-key dependency order one constraint-violation error at a time, instead of querying the graph once up front. Do not repeat this.**

Rules:
- **Before any multi-table DB operation** (cleanup/delete/migration touching more than one model) **or any troubleshooting/debugging session** (an error, an unexpected state, "why is X slow/stuck/failing"): run `graphify query`/`graphify path`/`graphify explain` FIRST, before trial-and-error edits or sequential command attempts. This applies even under time pressure or mid-debugging-loop — especially then, since that's exactly when it's easiest to skip.
- For codebase questions generally, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships (e.g. FK/dependency chains before a cascading delete) and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
