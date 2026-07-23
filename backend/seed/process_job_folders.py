"""Folder-drop CV ingestion — the manual/on-demand entry point. For automatic processing whenever
a new CV lands in a job folder (no need to run this by hand), see services/job_folder_watcher.py,
started automatically with the backend (main.py::on_startup). This script is still useful for a
one-off catch-up pass (e.g. the server was off when files were dropped in) or CI/local runs without
a live backend process.

Usage: drop CV PDFs into backend/seed/job_lists/<job_id>_<any-label>/ (the label is only for
your own readability — e.g. "12_data-scientist-2026-07-22" — matching is done on the leading
job_id, everything after the first underscore is ignored). Then run:

    python -m seed.process_job_folders   (from backend/, with .venv active)

For every PDF found, this runs the exact same pipeline as the live POST /candidates endpoint
(routers/candidates.py::create_candidate) — CV extraction, PII redaction, parsing, skill-gap
analysis, and match scoring/ranking (services/job_folder_ingest.py::process_one, shared with the
watcher) — so candidates show up on the Shortlist with a "Data siap"/"Belum diproses" badge
immediately, no extra step.

Idempotent: re-running only processes files not yet seen. Dedup is by each file's resolved path,
stored in the Candidate.source_file_path column (internal only, never exposed via any API) — not
by filename, since a CV's original filename may contain the candidate's real name and we don't
want that leaking into the alias shown to HR.

Processes one job folder at a time, in order — unlike the watcher, this does NOT run jobs
concurrently (a single one-off script run isn't latency-sensitive the way live ingestion is).
"""

import sys
import time
from pathlib import Path

from db import repositories as repo
from db.session import SessionLocal
from services.job_folder_ingest import process_one
from services.job_folders import JOB_LISTS_DIR


def _process_folder(db, job_id: int, folder: Path) -> None:
    job = repo.jobs.get(db, job_id)
    if not job:
        print(f"[{folder.name}] SKIPPED — no job with id={job_id}", flush=True)
        return

    pdfs = sorted(p for p in folder.iterdir() if p.suffix.lower() == ".pdf")
    if not pdfs:
        print(f"[{folder.name}] no PDFs found", flush=True)
        return

    for pdf_path in pdfs:
        t0 = time.time()
        try:
            alias = process_one(db, job, pdf_path)
        except Exception as e:
            db.rollback()
            print(f"[{folder.name}] {pdf_path.name} FAILED ({time.time()-t0:.1f}s): {e}", flush=True)
            continue

        if alias is None:
            print(f"[{folder.name}] {pdf_path.name} already processed, skipping", flush=True)
            continue

        print(f"[{folder.name}] {pdf_path.name} -> {alias} ({time.time()-t0:.1f}s)", flush=True)


def main() -> None:
    if not JOB_LISTS_DIR.exists():
        print(f"No {JOB_LISTS_DIR} directory yet — create it and drop job folders inside.")
        sys.exit(0)

    folders = sorted(p for p in JOB_LISTS_DIR.iterdir() if p.is_dir())
    if not folders:
        print(f"{JOB_LISTS_DIR} is empty — nothing to process.")
        return

    db = SessionLocal()
    try:
        for folder in folders:
            job_id_part = folder.name.split("_", 1)[0]
            if not job_id_part.isdigit():
                print(f"[{folder.name}] SKIPPED — folder name must start with the numeric job_id (e.g. \"12_data-scientist\")", flush=True)
                continue
            _process_folder(db, int(job_id_part), folder)
    finally:
        db.close()


if __name__ == "__main__":
    main()
