"""One-off backfill: creates job_lists/<job_id>_<slug>/ for every EXISTING job, and copies in the
already-uploaded CV for every candidate that's already been processed (has a parsed_profiles row)
under that job — so the folder-drop convention (see seed/process_job_folders.py) reflects reality
retroactively for jobs/candidates that predate it. Candidates without a parsed profile (never
actually CV-processed) are skipped, per the "processed ones only" ask.

The copied file is named after the candidate's own alias (e.g. "WD-14.pdf") — never the original
filename, which may contain the candidate's real name. Candidate.source_file_path is set to the
copy's path so a later `python -m seed.process_job_folders` run recognizes it as already-ingested
and does not try to recreate the candidate.

New jobs don't need this — routers/jobs.py::create_job already calls ensure_job_folder() at
creation time.

Idempotent: safe to re-run; already-copied files/rows are skipped.

Run: python -m seed.backfill_job_folders (from backend/, with .venv active)
"""

import shutil
from pathlib import Path

from db import repositories as repo
from db.session import SessionLocal
from services.job_folders import ensure_job_folder


def main() -> None:
    db = SessionLocal()
    try:
        jobs = repo.jobs.list(db)
        print(f"{len(jobs)} job(s) found.")

        for job in jobs:
            folder = ensure_job_folder(job.id, job.title)
            candidates = repo.candidates.list(db, job_id=job.id)
            copied = 0
            skipped = 0

            for candidate in candidates:
                if candidate.source_file_path:
                    skipped += 1
                    continue

                profiles = repo.parsed_profiles.list(db, candidate_id=candidate.id)
                if not profiles:
                    continue  # never actually CV-processed — nothing to backfill

                src = Path(profiles[0].raw_cv_path)
                if not src.exists():
                    print(f"[{folder.name}] {candidate.alias}: raw_cv_path missing on disk ({src}), skipping")
                    continue

                dest = folder / f"{candidate.alias}.pdf"
                shutil.copyfile(src, dest)
                candidate.source_file_path = str(dest.resolve())
                db.add(candidate)
                db.commit()
                copied += 1

            print(f"[{folder.name}] {job.title}: {copied} copied, {skipped} already done, {len(candidates)} candidate(s) total")
    finally:
        db.close()


if __name__ == "__main__":
    main()
