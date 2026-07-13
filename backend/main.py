import logging
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

import models  # noqa: F401  (registers all models on Base.metadata)
from db.session import create_all
from db.vector_store import create_collections
from routers import (
    auth,
    candidates,
    decisions,
    interview_answers,
    interview_questions,
    jobs,
    matching,
    report,
    rubric,
)

logger = logging.getLogger("gaskeun")

app = FastAPI(title="GaskeunKerja for Business — MVP")
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(candidates.router)
app.include_router(matching.router)
app.include_router(interview_questions.router)
app.include_router(interview_answers.router)
app.include_router(rubric.router)
app.include_router(decisions.router)
app.include_router(report.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Deliberate passthrough for our own intentional HTTPExceptions (404/400/401/403 etc.) —
    these already carry a safe, purposeful detail message, not a leaked internal."""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


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
    )


@app.on_event("startup")
def on_startup():
    create_all()
    create_collections()


@app.get("/health")
def health():
    return {"status": "ok"}
