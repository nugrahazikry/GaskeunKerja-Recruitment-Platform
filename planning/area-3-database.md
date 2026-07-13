# Area 3 — Database Management

> **Resolved 2026-07-12 (solo/1-week):** **PostgreSQL (Docker)** via SQLAlchemy, **no Alembic** (`create_all` on fresh demo DB; SQLite = ORM fallback). Reference datasets scoped to **ONE demo job role**. Solo owns **both** the schema (code) and the curation (content).
>
> **Resolved 2026-07-12 (Area-3 session):** Demo role = **Data Analyst (IT category)**. CVs sourced from **Kaggle `snehaanbhawal/resume-dataset`**, category `INFORMATION-TECHNOLOGY`, real PDFs, **30 candidates, manually curated for a match-quality spread**. **Mandatory PII redaction before the CV ever reaches the LLM** (Area 2 T5); raw stored PDF stays HR-facing as-is. CV parsing supports **text + scanned/image PDFs via `pypdf` extraction + vision-LLM caption fallback** (replicated from `NalarX-ai-engine`, **no Tesseract/OCR binary**). **JDs are authored by HR in-app with full CRUD, structured fields**, not seeded directly.
>
> **Resolved 2026-07-12 (Area-3 second pass):** Of the 30 candidates — **27 profile-only** (no interview data), **2-3 pre-seeded with synthetic interview data** (populates the HR-review screen without live recording), **1 live candidate** with no pre-seeded interview data (walked through the real flow for the demo video). **Consent records only exist for the 1 live candidate** — no fabricated consent for seed-only candidates. **No self-service CV upload** — all 30 go through the same parse pipeline but called HR/admin-side. **Single company** — no isolation-demo seed data. Full schema reference: see "Database Schema Reference" section below.
>
> **Resolved 2026-07-12 (gap-closing pass):** **Audio format = WebM (Opus), universal** — the 2-3 synthetic candidates get real, distinct, manually pre-recorded clips (not duplicated, not TTS). **Kaggle sourcing is manual** — no API credential; 30 curated PDFs go into `../seed/raw/cv/`, 2-3 pre-recorded `.webm` clips go into `../seed/raw/audio/` (both created). **T9 retention policy scoped**: applies only to the 1 live candidate's real recording — the synthetic clips are fixtures, not consented personal data. Live task status + steps: `execution-checklist.md` → Area 3.

**Goal:** all data persisted locally — structured DB + vector DB + file storage — plus the two NEW reference datasets the learning-report feature needs.
**Stack (local, no cloud):** PostgreSQL (Docker) via SQLAlchemy; local Qdrant (Docker); local filesystem for files.
**Blocks Area 2** — schema and reference datasets should be ready early on the critical path.

## Three Stores (local substitutes for the cloud design)

| Data type | Cloud design | MVP local |
|---|---|---|
| Structured/tabular | BigQuery | PostgreSQL (Docker) or SQLite |
| Vectors/embeddings | Qdrant (managed) | Qdrant (local Docker) |
| Files (CV, audio) | GCS | Local filesystem |

## Data Inventory (from `direction B summary.md` §4)

Structured: companies, jobs/JDs, extracted JD competencies, candidates, parsed profiles, match scores (+ per-competency detail), interview questions, transcripts, rubric scores + AI summary, HR decisions, consent records, audit log.
Vectors: candidate + JD embeddings (Qdrant collections).
Files: raw CVs, interview audio recordings.

## Task List (first draft)

### Core stores
- [ ] T1. ✅ DB = **PostgreSQL (Docker)** via SQLAlchemy; `create_all` on boot, **no Alembic**.
- [ ] T2. Design schema for all structured entities above. Explicit tables for consent records and audit log (compliance-relevant).
- [ ] T3. Set up local Qdrant (Docker); define collections + payload schema for candidate/JD vectors.
- [ ] T4. Local file storage structure for CV **+ interview audio** (audio is core): folder layout, naming convention, access control (candidates isolated from each other); recruiter can fetch raw audio back.
- [ ] T5. Data access layer: SQLAlchemy repository pattern. **No Alembic** (fresh demo DB).

### The two NEW reference datasets (content work — NOT just schema)
- [ ] T6. **Competency framework / skill taxonomy — ONE demo role** (~8-12 competencies with levels + lightweight parent/related relations that feed the matching graph layer, Area 2 T7). Powers deterministic skill-gap → report mapping. `[content]`
- [ ] T7. **Curated learning-resource library — same role** (~3 resources per competency: title, duration, milestone), keyed to competencies. Powers the deterministic report (select/order, don't free-generate). `[content]`

### Integrity, compliance, seed
- [ ] T8. Consent + audit write paths: every AI decision and every candidate-data access logged. **Consent rows are written only for candidates who reach the interview gate** — i.e. only the 1 live demo candidate; the 29 seed-only candidates (profile-only or synthetic-interview) get no `consent_records` row, since fabricating one would misrepresent the compliance claim.
- [ ] T9. Retention/cleanup policy for interview audio (light) — simple rule tied to consent record; manual cleanup helper is enough for MVP (supports UU PDP).
- [ ] T10. Seed data: **1 company** + seeded HR account (JD created via in-app CRUD, not raw insert); **30 candidate CVs** from Kaggle `snehaanbhawal/resume-dataset` (category `INFORMATION-TECHNOLOGY`), each anonymized + parsed through the pipeline before seeding, **HR/admin-side (no self-apply)**; competency + resource entries (T6/T7). **Tiered:** 27 profile+match only, 2-3 with fabricated interview data (audio/transcript/rubric/summary, written directly not via live pipeline) + a fabricated `hr_decisions` row each, 1 with no pre-seeded interview data (real live flow during recording). **Match-quality tier (strong/mid/weak) recorded per candidate in the seed manifest itself** (resolved 2026-07-12) — this is the ground truth Area 5 QA T5's matching test asserts against.

## Decisions — RESOLVED
- ~~Postgres vs SQLite (T1)~~ → **Postgres, no Alembic** (SQLite = ORM fallback).
- ~~Reference dataset size (T6/T7)~~ → **one role**, ~8-12 competencies, ~3 resources each.
- ~~Who owns curation vs schema~~ → **solo owns both**; datasets start Day 2, gate the report — don't slip.
- Vector payload → store competency ids/metadata needed for **explainable** matching (per-competency detail).

---

## Database Schema Reference (detailed)

### Datastores

| Datastore | Type | Purpose |
|---|---|---|
| `gaskeun` (PostgreSQL, Docker) | Relational DB | All structured data — companies, jobs, candidates, scores, decisions, compliance records, reference content |
| Qdrant (Docker) | Vector DB | Candidate + JD embeddings for semantic matching |
| Local filesystem (`storage/`) | File storage | Raw CV PDFs + interview audio recordings (DB stores only the path pointer) |

### PostgreSQL Tables

| Table | Description |
|---|---|
| `companies` | One row per client company using the platform |
| `hr_users` | HR/recruiter login accounts, scoped to a company (the ONLY accounts with a login — candidates never get one) |
| `jobs` | Job descriptions (JDs), full CRUD by HR, structured fields |
| `jd_competencies` | Competencies extracted from a JD by the LLM (Flash) |
| `candidates` | One row per candidate invited/uploaded for a job; reached via an unguessable token link, not login |
| `parsed_profiles` | Structured CV data (skills/experience/qualifications) produced by the CV-parse pipeline, tagged to an anonymized alias |
| `match_scores` | Candidate ↔ JD ranking score, with per-competency breakdown for explainability |
| `interview_questions` | AI-generated interview questions per job, editable/approvable by HR |
| `interview_answers` | One row per candidate's audio answer to a question |
| `transcripts` | STT output (Groq) for each interview answer |
| `rubric_scores` | Per-criterion rubric score + rationale for each interview answer (temperature=0) |
| `interview_summaries` | AI-generated summary of a candidate's full interview, shown to HR |
| `hr_decisions` | HR's final human decision per candidate (advance/reject) — separate from any AI score |
| `consent_records` | Candidate's PDP consent record, gates interview processing |
| `audit_log` | Every AI decision point + candidate-data access, for auditability |
| `competency_framework` | `[content]` Reference: skill taxonomy for the one demo role (Data Analyst), with lightweight relations |
| `resource_library` | `[content]` Reference: curated learning resources keyed to competencies, powers the deterministic report |

### Column Detail

**`companies`**
| Column | Type | Description |
|---|---|---|
| `id` | PK (uuid/int) | |
| `name` | text | Company display name |
| `created_at` | timestamp | |

**`hr_users`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `company_id` | FK → `companies` | |
| `email` | text, unique | Login identifier |
| `password_hash` | text | |
| `created_at` | timestamp | |

**`jobs`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `company_id` | FK → `companies` | Scopes the JD to one company |
| `title` | text | Structured field |
| `responsibilities` | text | Structured field |
| `requirements` | text | Structured field |
| `qualifications` | text | Structured field |
| `status` | enum (`draft`/`active`/`closed`) | |
| `created_at` / `updated_at` | timestamp | |

**`jd_competencies`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `job_id` | FK → `jobs` | |
| `competency_name` | text | |
| `importance_level` | text/int | Weight used in matching (Area 2 T7) |

**`candidates`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `job_id` | FK → `jobs` | |
| `alias` | text | Anonymized display name (e.g. `Kandidat IT-07`) — never the real name |
| `token` | text, unique | Unguessable link for the candidate's own consent/interview session |
| `token_expires_at` | timestamp | `CANDIDATE_TOKEN_TTL_HOURS` from `.env` |
| `telegram_chat_id` | text, nullable | Captured after the candidate links via the `t.me/<bot>?start=<token>` deep-link |
| `created_at` | timestamp | |

**`parsed_profiles`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `candidate_id` | FK → `candidates` | |
| `skills` | jsonb/array | Structured LLM output |
| `experience` | jsonb/text | Structured LLM output |
| `qualifications` | jsonb/text | Structured LLM output |
| `raw_cv_path` | text | Pointer to `storage/cv/<candidate_id>/original.pdf` — the ORIGINAL file, un-redacted, still HR-facing |
| `parsed_at` | timestamp | |

**`match_scores`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `candidate_id` | FK → `candidates` | |
| `job_id` | FK → `jobs` | |
| `overall_score` | float | |
| `competency_breakdown` | jsonb | Per-competency detail — the explainability data for Q17 |
| `rank` | int | |
| `computed_at` | timestamp | |

**`interview_questions`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `job_id` | FK → `jobs` | |
| `question_text` | text | Editable by HR |
| `order_index` | int | |
| `status` | enum (`draft`/`approved`) | Candidate only sees `approved` questions |
| `created_at` | timestamp | |

**`interview_answers`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `candidate_id` | FK → `candidates` | |
| `question_id` | FK → `interview_questions` | |
| `audio_path` | text | Pointer to `storage/audio/<candidate_id>/<session>/answer_<n>.webm` |
| `submitted_at` | timestamp | |

**`transcripts`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `answer_id` | FK → `interview_answers` | |
| `transcript_text` | text | Groq `whisper-large-v3` output, `language=id` |
| `created_at` | timestamp | |

**`rubric_scores`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `answer_id` | FK → `interview_answers` | |
| `criterion_name` | text | e.g. clarity, relevance, technical depth |
| `score` | float | Scored at temperature=0 for determinism |
| `rationale` | text | |

**`interview_summaries`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `candidate_id` | FK → `candidates` | |
| `ai_summary_text` | text | Main-points summary shown to HR alongside audio + transcript |
| `overall_score` | float | Aggregate across `rubric_scores` |
| `created_at` | timestamp | |

**`hr_decisions`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `candidate_id` | FK → `candidates` | |
| `decision` | enum (`advance`/`reject`/`pending`) | Human-entered only — no code path sets this automatically |
| `decided_by` | FK → `hr_users` | |
| `decided_at` | timestamp | |
| `notes` | text, nullable | |

**`consent_records`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `candidate_id` | FK → `candidates` | |
| `consent_given` | bool | |
| `consent_text_version` | text | Which PDP consent wording was shown |
| `consented_at` | timestamp | |

**`audit_log`**
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `actor` | text | `hr_user_id`, `"system"`, or `"candidate"` |
| `action` | text | e.g. `cv_parsed`, `match_computed`, `interview_scored`, `decision_recorded` |
| `entity_type` / `entity_id` | text / id | What the action touched |
| `metadata` | jsonb | Extra context |
| `created_at` | timestamp | |

**`competency_framework`** `[content]`
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `job_role` | text | `"Data Analyst"` (the one demo role) |
| `competency_name` | text | |
| `level_description` | text | |
| `related_competency_ids` | jsonb array | Lightweight graph relations feeding Area 2 T7's matching boost |

**`resource_library`** `[content]`
| Column | Type | Description |
|---|---|---|
| `id` | PK | |
| `competency_id` | FK → `competency_framework` | |
| `title` | text | |
| `duration` | text | |
| `milestone_description` | text | |
| `url` | text, nullable | |

### Qdrant Collections

| Collection | Payload | Purpose |
|---|---|---|
| `jd_vectors` | `job_id`, competency metadata | JD embedding for semantic matching |
| `candidate_vectors` | `candidate_id`, competency metadata | Candidate profile embedding for semantic matching |
