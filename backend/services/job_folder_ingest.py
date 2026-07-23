"""Shared per-file CV ingestion logic for the job_lists/ folder-drop convention — used by both
the manual batch script (seed/process_job_folders.py) and the background watcher
(services/job_folder_watcher.py), so the two never drift out of sync.
"""

from __future__ import annotations

import contextlib
import threading
from pathlib import Path

from db import repositories as repo
from services import auth
from services.candidate_ingest import ingest_cv
from services.matching import compute_match_score, rank_candidates_for_job


def job_code(title: str) -> str:
    """Mirrors load_demo_data.py's "WD-01" alias convention — initials of the job title."""
    words = [w for w in title.split() if w]
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return title[:2].upper() if title else "JB"


def process_one(db, job, pdf_path: Path, lock: threading.Lock | None = None) -> str | None:
    """Ingests one CV for `job` (skill-gap analysis + match scoring included) unless it's already
    been processed (dedup via Candidate.source_file_path, keyed on the file's resolved path — not
    filename, since a filename may contain the candidate's real name).

    `lock`, if given, is a per-job_id lock — held only around the two operations that touch
    job-wide shared state (alias-number reservation, and the final rank recompute), NOT around the
    ~166s CV-extraction/skill-gap LLM work in between. That work only ever touches rows scoped to
    THIS candidate (its own parsed_profiles/skill_gap_results/match_scores rows) plus a read-only
    look at the job's competencies, so it's safe to run fully concurrently even for two CVs in the
    SAME job — only the alias counter and rank_candidates_for_job() (which reads/rewrites every
    candidate's rank for the job at once) are actually racy. Pass None when called from a
    single-threaded context (seed/process_job_folders.py) where no locking is needed at all.

    Returns the new candidate's alias, or None if this file was already processed.
    """
    resolved = str(pdf_path.resolve())
    if repo.candidates.list(db, job_id=job.id, source_file_path=resolved):
        return None

    lock_cm = lock if lock is not None else contextlib.nullcontext()

    # Locked (milliseconds): reserve the next dense sequence number and create the candidate row.
    # job_id is baked into the alias so it can never collide across two DIFFERENT jobs whose titles
    # happen to reduce to the same code (e.g. two "Data Scientist" postings) — job_id is globally
    # unique, so "DS-50-01" and "DS-61-01" can never refer to different CVs under the same label.
    with lock_cm:
        code = job_code(job.title)
        next_seq = len(repo.candidates.list(db, job_id=job.id)) + 1
        alias = f"{code}-{job.id}-{next_seq:02d}"
        token, expires_at = auth.generate_candidate_token()
        candidate = repo.candidates.create(
            db, job_id=job.id, alias=alias, token=token, token_expires_at=expires_at,
            source_file_path=resolved,
        )

    # Unlocked (~166s): CV extraction, PII redaction, parsing, skill-gap self-consistency voting —
    # all scoped to this candidate alone, safe to run in parallel with any other candidate's pipeline.
    file_bytes = pdf_path.read_bytes()
    ingest_cv(db, candidate.id, file_bytes, alias=alias)
    compute_match_score(db, candidate.id, job.id)

    # Locked (milliseconds): rewrites every candidate's rank for this job — the one truly job-wide
    # shared-state write in this whole pipeline.
    with lock_cm:
        rank_candidates_for_job(db, job.id)

    return alias
