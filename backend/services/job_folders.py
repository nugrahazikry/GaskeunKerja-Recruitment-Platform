"""Shared job_lists/ folder-drop conventions (see seed/process_job_folders.py for the ingestion
side) — folder naming/creation lives here so both the live job-create endpoint
(routers/jobs.py::create_job) and the batch script agree on the exact same path for a given job.
"""

import re
from pathlib import Path

JOB_LISTS_DIR = Path(__file__).resolve().parent.parent / "seed" / "job_lists"


def _slug(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "job"


def job_folder_path(job_id: int, title: str) -> Path:
    return JOB_LISTS_DIR / f"{job_id}_{_slug(title)}"


def ensure_job_folder(job_id: int, title: str) -> Path:
    """Called right after a job is created so HR can drop CVs in immediately — no manual mkdir."""
    path = job_folder_path(job_id, title)
    path.mkdir(parents=True, exist_ok=True)
    return path
