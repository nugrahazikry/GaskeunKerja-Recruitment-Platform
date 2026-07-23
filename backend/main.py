import asyncio
import logging
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import models  # noqa: F401  (registers all models on Base.metadata)
from config import TELEGRAM_ENABLED
from db.session import create_all
from db.vector_store import create_collections
from services.job_folder_watcher import run_job_folder_watcher
from routers import (
    auth,
    candidate_detail,
    candidates,
    dashboard,
    decisions,
    interview_answers,
    interview_questions,
    jobs,
    matching,
    report,
    rubric,
)
from services.telegram_poller import run_telegram_poller

# Python's root logger defaults to WARNING with no handler configured, which was
# silently swallowing every logger.info() call across the whole app (found while
# verifying Area 1 T8's Telegram poller — its "linked chat_id" log line never
# appeared despite the underlying DB write succeeding correctly).
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

logger = logging.getLogger("gaskeun")

app = FastAPI(title="GaskeunKerja for Business — MVP")

_ALLOWED_ORIGIN = "http://localhost:5173"

# Local-only MVP: frontend (Vite dev server) and backend run on different ports/origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[_ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _cors_headers(request: Request) -> dict:
    """FastAPI's @app.exception_handler responses bypass CORSMiddleware's normal
    response-wrapping (a known Starlette interaction) — verified directly during Area 1
    T7: a real 500 from a route dispatched via run_in_threadpool came back with zero
    Access-Control-Allow-* headers, which the browser then reports as a CORS error,
    masking the real 500 and its error_id from the frontend entirely. Every custom
    exception handler must attach these headers explicitly."""
    origin = request.headers.get("origin")
    if origin == _ALLOWED_ORIGIN:
        return {"Access-Control-Allow-Origin": origin, "Access-Control-Allow-Credentials": "true"}
    return {}

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(candidates.router)
app.include_router(matching.router)
app.include_router(interview_questions.router)
app.include_router(interview_answers.router)
app.include_router(rubric.router)
app.include_router(decisions.router)
app.include_router(report.router)
app.include_router(candidate_detail.router)
app.include_router(dashboard.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Deliberate passthrough for our own intentional HTTPExceptions (404/400/401/403 etc.) —
    these already carry a safe, purposeful detail message, not a leaked internal."""
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}, headers=_cors_headers(request)
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Global catch-all for anything NOT already an HTTPException — i.e. a genuine bug.

    Per the 2026-07-12 Tahap 2 audit finding: Tahap 2's handler returned raw Python
    tracebacks as JSON in 500 responses (a real security anti-pattern — leaks internal
    file paths, code structure, potentially secrets in local variables). This handler
    logs the full traceback server-side only and returns a generic, non-leaking message
    with a correlation id the user/HR could reference when reporting a bug.
    """
    error_id = str(uuid.uuid4())
    logger.exception("Unhandled exception [error_id=%s] on %s %s", error_id, request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred.", "error_id": error_id},
        headers=_cors_headers(request),
    )


@app.on_event("startup")
def on_startup():
    create_all()
    create_collections()
    if TELEGRAM_ENABLED:
        asyncio.create_task(run_telegram_poller())
    asyncio.create_task(run_job_folder_watcher())


@app.get("/health")
def health():
    return {"status": "ok"}
