# Area 2 — Backend & AI Integration

> **Resolved 2026-07-12 (solo/1-week):** matching = **semantic similarity + lightweight competency-graph** (no KGE porting). Interview = **AUDIO** → **Groq `whisper-large-v3` STT** (`id`) → rubric scoring. **All LLM via SumoPod + caching** (`deepseek-v4-flash`/`deepseek-v4-pro`; no local-LLM). Auth = **thin JWT + single role gate**. **+Recruiter question edit/approve step** (checklist T9b).
>
> **Resolved 2026-07-12 (Area-3 session):** JD intake (T4) is now **full CRUD** (list/create/edit/delete, scoped to company), not a one-shot POST. CV parsing (T5) gains **vision-LLM caption fallback** (no Tesseract) for scanned/image PDFs + **mandatory PII redaction before the LLM call** (source: 30 Kaggle IT-category resumes).
>
> **Resolved 2026-07-12 (Area-3 second pass):** `POST /candidates` (T5) is **HR/admin-side only** — no public self-apply endpoint for MVP; the seed script calls the same pipeline for all 30 demo candidates. **Interview data is tiered**: 27 candidates get profile+match only, 2-3 get synthetic pre-seeded interview data (written directly to DB, bypassing the live STT/rubric pipeline), and 1 live candidate runs the real pipeline end-to-end during demo recording.
>
> **Resolved 2026-07-12 (Area-2 session):** Found a real gap — no step generated/handed over the candidate's interview token — **added T9c** (HR clicks "Invite" → backend generates token → UI shows copyable link, no auto-distribution). **Rubric locked**: 3 criteria (clarity, relevance, technical depth), 1-5 scale, anchored levels. **Report format locked**: real PDF via `weasyprint`. **Matching formula locked**: `overall_score = 0.7 × semantic_similarity + 0.3 × graph_boost`.
>
> **Resolved 2026-07-12 (Area-2 gap-closing pass):** Fixed a dependency-graph bug — **T5 no longer depends on T4** (CV parsing is JD-independent). **Consent enforcement made explicit** in T10 (403 if no consent record). **Report gating**: T13/T14 now require an `hr_decisions` row first, not just skill-gap. **JD delete (T4)**: soft-delete only (`status='closed'`), never a real SQL `DELETE`.
>
> **Resolved 2026-07-12 (Tahap 2 backend code audit):** deep-read the actual Tahap 2 backend (not just the frontend). Corrected wrong assumptions: **no Deepseek anywhere** (it's Google Gemini), **no auth code at all**, **no DB/ORM/vector-DB** (in-memory only) — see `CLAUDE.md` for the full corrected inventory. Real reusable code found in 3 places: (1) `pdfplumber` text-extraction pattern for T5, (2) `_build_seed_gap` skill-gap-grounding pattern for T8, (3) a fully-working ~700-line **ReportLab** PDF generator — **T14 swaps from weasyprint to adapting this code**, eliminating the Windows Pango/Cairo risk entirely. Also: don't replicate Tahap 2's exception handler (T15) — it leaks raw tracebacks. Estimates revised in `execution-checklist.md` § Effort & Difficulty Estimates. Live task status + steps: `execution-checklist.md` → Area 2.

**Goal:** local FastAPI backend orchestrating the Direction B AI pipeline, stage by stage.
**Stack:** FastAPI + uvicorn (reuse Tahap 2 backend). Deepseek Flash/Pro **via SumoPod** (OpenAI-compat). Local multilingual sentence-transformers for embeddings. **Groq `whisper-large-v3` API for STT**.
**Depends on:** DB schema + reference datasets (Area 3). This is the largest area and the core of the MVP.

## Pipeline Stages (map to end-to-end flow in `direction B summary.md` §2)

## Task List (first draft)

### Foundation
- [ ] T1. Audit Tahap 2 backend repo — reuse FastAPI structure, CV-parse pipeline; strip out scraping code entirely.
- [ ] T2. Project structure: routers, services, models, LLM client wrapper, config/env for API keys.
- [ ] T3. Auth service: JWT for **HR/recruiter login ONLY** (seeded account, no candidate signup); candidate reaches consent+interview via an **unguessable token link** scoped to one session; guard HR routes by JWT, candidate routes by session token.

### Ingestion & extraction
- [ ] T4. JD **full CRUD** (list/create/edit/**soft-delete**, scoped to company) + JD → required-competency extraction (Deepseek V4 Flash) on create/edit. "Delete" flips `status='closed'` — never a real SQL `DELETE` (avoids FK errors against candidates/interviews/audit_log). Prompt for structured output.
- [ ] T5. CV upload endpoint + parsing (JD-independent — no dependency on T4): **`pypdf` text extraction + vision-LLM caption fallback for scanned/image/mixed PDFs** (replicated from `NalarX-ai-engine` — no Tesseract/OCR binary: per-page empty-text detection → embedded images sent to a vision LLM in transcribe/describe mode → merged into one text blob) → **PII redaction (name/email/phone → alias) BEFORE the LLM call** → Deepseek V4 Flash → structured profile (skills, experience, qualifications), tagged to the alias only. Reuse Tahap 2 pipeline where possible.
- [ ] T6. Embedding generation for candidate profile + JD (local sentence-transformers), stored to Qdrant.

### Matching & analysis
- [ ] T7. Matching engine: rank **candidates for a JD** via Qdrant vector similarity **+ lightweight competency-graph boost** (related-competency credit from the Area 3 framework), combined via **weighted sum**: `overall_score = 0.7 × semantic_similarity + 0.3 × graph_boost`. Retain per-competency match detail for explainability (Q17). *(Full KGE porting deferred.)*
- [ ] T8. Skill-gap analysis per candidate vs JD (Deepseek V4 Pro), structured output.

### AI Interview Module (the new component)
- [ ] T9. Interview question generation from JD (Deepseek V4 Flash) — e.g. "explain process A in 1 minute".
- [ ] T9b. **Recruiter edit/approve questions** — HR edits/approves generated questions before the candidate sees them (unlocks invite). Human-in-the-loop.
- [ ] T9c. **Invite candidate to interview** — HR clicks "Invite" on a shortlisted candidate → backend generates the unguessable token/link → UI shows a copyable link. No auto-distribution for MVP.
- [ ] T10. Answer intake — **consent check first** (403 if no `consent_records` row for the candidate) → **audio file** persisted → **STT via Groq `whisper-large-v3`** (`language=id`) → transcript. Recruiter can fetch raw audio + transcript.
- [ ] T11. **Rubric scoring** (Deepseek V4 Pro): **3 criteria — clarity, relevance, technical depth — 1-5 scale, anchored level descriptions**. Prompt for consistent scoring, **temperature=0** for determinism. Output score + rationale per criterion.
- [ ] T12. Human-in-the-loop endpoints: HR views AI outputs + records final decision. **AI never auto-rejects** — enforce in code, not just UI.

### Report & delivery
- [ ] T13. Development report generation — **gated on an `hr_decisions` row existing** (not just skill-gap): hybrid competency-framework + curated-resource-DB lookup (Area 3 datasets) → **deterministic** report (select/order from library, don't free-generate). For every *decided* candidate, pass or fail.
- [ ] T14. Report delivery — rendered as **real PDF via `weasyprint`** (HTML/CSS template → PDF; verify Windows Pango/Cairo requirements Day 1), delivered via **Telegram Bot API only** (`sendDocument` for the PDF, `sendMessage` for the summary). No email/SMTP. HR triggers with one click; system sends. Trigger tied to consent record.

### Orchestration & contract
- [ ] T15. Async pipeline wiring (FastAPI async), error handling, retries, and LLM response caching (cost control).
- [ ] T16. OpenAPI contract published for frontend (Area 1) integration.

## Determinism & Transparency Requirements (non-negotiable — tie to submission claims)
- Rubric scoring at temperature=0 with fixed prompts → same answer yields same score (testable in QA, Area 5).
- Learning report is assembled from curated data, not freely generated → consistent + measurable.
- Every AI decision point writes to the audit log (Area 3).

## Decisions — RESOLVED
- ~~KGE vs semantic-first (T7)~~ → **semantic similarity + lightweight competency-graph**; no KGE porting.
- ~~Text vs audio (T10)~~ → **audio** → **Groq `whisper-large-v3` STT** (`id`).
- Embedding model → **multilingual** `paraphrase-multilingual-MiniLM-L12-v2` (Bahasa Indonesia).
- ~~Free local model per step~~ → **no** — all via SumoPod + caching (negligible saving vs solo hours).
