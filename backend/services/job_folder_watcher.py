"""Background watcher for the job_lists/ folder-drop CV ingestion convention (see
seed/process_job_folders.py for the manual/on-demand equivalent, and
services/job_folder_ingest.py for the shared per-file logic both use).

Started as an asyncio task from main.py::on_startup — polls job_lists/ every POLL_SECONDS for PDFs
not yet in the DB (dedup via Candidate.source_file_path) and dispatches each new one to a thread
pool, so CVs dropped into ANY job folders — same job or different — process concurrently instead
of queueing. Polling rather than filesystem-event APIs (no new dependency, and a human dropping
files by hand doesn't need sub-second reaction time) — 5s is frequent enough that a new CV starts
processing well within one human "did it work?" glance.

Concurrency model: full parallelism, including multiple CVs for the SAME job — process_one() only
holds its per-job lock briefly around the two operations that actually touch job-wide shared state
(alias-number reservation, final rank recompute), not around the ~166s CV-extraction/skill-gap LLM
work in between, so N candidates for one job now run that work fully in parallel instead of one at
a time. Each worker opens its own DB session — SQLAlchemy sessions are not thread-safe to share
across threads.
"""

import asyncio
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from db import repositories as repo
from db.session import SessionLocal
from services.job_folder_ingest import process_one
from services.job_folders import JOB_LISTS_DIR

logger = logging.getLogger("gaskeun")

POLL_SECONDS = 5.0
MAX_WORKERS = 10

_executor = ThreadPoolExecutor(max_workers=MAX_WORKERS, thread_name_prefix="cv-ingest")

_in_flight: set[str] = set()
_in_flight_lock = threading.Lock()

_job_locks: dict[int, threading.Lock] = {}
_job_locks_meta = threading.Lock()


def _get_job_lock(job_id: int) -> threading.Lock:
    with _job_locks_meta:
        if job_id not in _job_locks:
            _job_locks[job_id] = threading.Lock()
        return _job_locks[job_id]


def _worker(job_id: int, resolved_path: str) -> None:
    pdf_path = Path(resolved_path)
    db = SessionLocal()
    try:
        job = repo.jobs.get(db, job_id)
        if not job:
            logger.warning("job folder watcher: no job id=%s for %s", job_id, pdf_path.name)
            return
        alias = process_one(db, job, pdf_path, lock=_get_job_lock(job_id))
        if alias:
            logger.info("job folder watcher: %s -> %s (job=%s) ready", pdf_path.name, alias, job.title)
    except Exception:
        db.rollback()
        logger.exception("job folder watcher: failed processing %s", pdf_path.name)
    finally:
        db.close()
        with _in_flight_lock:
            _in_flight.discard(resolved_path)


def _scan_and_dispatch() -> None:
    if not JOB_LISTS_DIR.exists():
        return

    db = SessionLocal()
    try:
        for folder in JOB_LISTS_DIR.iterdir():
            if not folder.is_dir():
                continue
            job_id_part = folder.name.split("_", 1)[0]
            if not job_id_part.isdigit():
                continue
            job_id = int(job_id_part)

            for pdf_path in folder.glob("*.pdf"):
                resolved = str(pdf_path.resolve())
                with _in_flight_lock:
                    if resolved in _in_flight:
                        continue
                if repo.candidates.list(db, job_id=job_id, source_file_path=resolved):
                    continue
                with _in_flight_lock:
                    _in_flight.add(resolved)
                _executor.submit(_worker, job_id, resolved)
    finally:
        db.close()


async def run_job_folder_watcher(poll_seconds: float = POLL_SECONDS) -> None:
    logger.info("job folder watcher started - polling %s every %ss", JOB_LISTS_DIR, poll_seconds)
    while True:
        try:
            _scan_and_dispatch()
        except Exception:
            logger.exception("job folder watcher: scan failed")
        await asyncio.sleep(poll_seconds)
