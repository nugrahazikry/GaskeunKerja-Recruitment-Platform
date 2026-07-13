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
