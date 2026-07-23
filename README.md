# GaskeunKerja for Business — MVP (Local)

Local-only MVP build. See `planning/plan.md` for the full plan and `CLAUDE.md` for the working
constraints. This file only documents how to actually run the thing.

## Prerequisites

- Docker Desktop running
- Python 3.11+, Node 22+ (see `planning/execution-checklist.md` § Area 4 T1 for exact versions)
- `.env` filled in (copy from `.env.example`)

## Dev mode (day-to-day development)

Databases run in Docker; backend and frontend run directly on the host for fast reload.

```bash
# 1. Start Postgres + Qdrant
docker compose --env-file .env up -d

# 2. Backend (from backend/, with .venv activated)
cd backend
python -m venv .venv               # first time only
./.venv/Scripts/pip install -r requirements.txt   # first time only
./.venv/Scripts/python -m uvicorn main:app --reload --port 8000

# 3. Frontend (from frontend/)
cd frontend
npm install                        # first time only
npm run dev
```

- Backend: http://localhost:8000 (health check: `/health`)
- Frontend: http://localhost:5173
- Postgres: `localhost:5433` (remapped from the default 5432 — see note below)
- Qdrant: http://localhost:6333

**Note on the Postgres port**: this project's Docker Postgres is exposed on host port **5433**, not
the default 5432, because some dev machines (this one included) already run a native PostgreSQL
service on 5432 which silently intercepts connections meant for the container. `POSTGRES_PORT` /
`DATABASE_URL` in `.env.example` are already set to 5433 — don't change them back to 5432 unless
you've confirmed nothing else on the host is listening there.

## Finalization mode (one-command run for the demo)

`[deferred until closer to demo]` — will add `backend` (and optionally `frontend`) as Compose
services for a single `docker compose up` command. Dev mode above is the working mode for now.

## Stopping

```bash
docker compose down          # stops DBs, keeps data (named volumes)
docker compose down -v       # stops DBs AND wipes data — only for a full reset
```

## Loading demo data

The app is not usable with an empty database — there's no self-service company signup, so you
need a seeded HR account before you can log in.

```bash
cd backend
./.venv/Scripts/python -m seed.load_demo_data
```

This creates one demo company, one HR login, one job description, and 30 candidates run through
the real CV parsing/matching pipeline. It's idempotent — safe to re-run, it skips if the demo
company already exists. On success it prints the HR login to use:

```
HR login: hr@gaskeundemo.test / demo12345
```

## How to use the platform

Two separate people use this app: **HR** (logs in, has the nav bar below) and a **candidate**
(never logs in — reaches their pages only via a one-off link sent by HR/the system).

### HR side

1. **Login** (`/login`) — use the seeded credentials above.
2. **Dashboard** (`/dashboard`) — landing page after login. Shows the candidate funnel across all
   jobs (parsed → shortlisted → interviewed → decided) and links into the rest of the app.
3. **Lowongan** ("Jobs", `/jobs`) — list of job descriptions. "Lowongan Baru" opens a form to
   create one (title, responsibilities, requirements, qualifications); the backend extracts
   structured competencies from that text automatically. Creating a job also creates its CV
   drop folder (`backend/seed/job_lists/<job_id>_<slug>/`) — copy candidate CV PDFs in there and
   they're picked up automatically by a background watcher (or run
   `python -m seed.process_job_folders` for a one-off catch-up pass) and scored against the JD.
4. **Job Detail** (click a job → `/jobs/:jobId/detail`) — view the parsed JD and open **Kelola
   Pertanyaan** ("Manage Questions", `/jobs/:jobId/questions`) to review/edit the AI-generated
   interview questions for that job before candidates are invited.
5. **Kandidat** ("Candidates" / shortlist, `/jobs/:jobId`) — ranked candidate list for the
   current job with explainable match scores. From here you can invite a candidate to interview
   (sends them a link by email/Telegram) and open a candidate's detail page
   (`/jobs/:jobId/candidates/:candidateId`) to see their parsed CV
   (`.../cv`) and skill-gap breakdown.
6. **Laporan** ("Reports", `/jobs/:jobId/reports`) — once a candidate has completed their
   interview, open their report (`.../report`, or `.../report/pdf` for the downloadable version)
   to see the AI interview summary + rubric scores and make the final accept/reject call. The
   nav's Kandidat/Laporan links always point at whichever job you last viewed.

### Candidate side (no login — link-based)

A candidate never sees the HR nav. They receive a link (email or Telegram) that walks them
through, in order:

1. **Consent** (`/candidate/:candidateId/consent`) — accept before anything else happens.
2. **Camera/mic test** (`/candidate/:candidateId/camera-test`) — verify recording works.
3. **Interview** (`/candidate/:candidateId/interview`) — answer each question on camera; each
   answer is recorded, transcribed, and scored automatically.

After the interview, HR reviews the result on the Laporan page above and the candidate receives
their development report by email (or Telegram, if enabled) once HR decides.
