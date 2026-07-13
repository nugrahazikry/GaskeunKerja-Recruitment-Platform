"""Loads the Web Developer competency framework + resource library into Postgres (Area 3 T6/T7).

Idempotent: skips loading if the framework for this job_role already has rows.
Run: python -m seed.load_competency_framework (from backend/, with .venv active)
"""

import sys

from db import repositories as repo
from db.session import SessionLocal
from seed.competency_framework_data import COMPETENCIES, JOB_ROLE, RESOURCES


def load() -> None:
    db = SessionLocal()
    try:
        existing = repo.competency_framework.list(db, job_role=JOB_ROLE)
        if existing:
            print(f"Competency framework for '{JOB_ROLE}' already has {len(existing)} rows — skipping.")
            return

        # Pass 1: create all competency rows (related_competency_ids filled in pass 2, once all ids exist)
        key_to_id: dict[str, int] = {}
        for key, (name, level_description, _related_keys) in COMPETENCIES.items():
            row = repo.competency_framework.create(
                db,
                job_role=JOB_ROLE,
                competency_name=name,
                level_description=level_description,
                related_competency_ids=[],
            )
            key_to_id[key] = row.id

        # Pass 2: fill in related_competency_ids now that every competency has an id
        for key, (_name, _level_description, related_keys) in COMPETENCIES.items():
            row = repo.competency_framework.get(db, key_to_id[key])
            row.related_competency_ids = [key_to_id[rk] for rk in related_keys]
        db.commit()

        # Resources, keyed to the now-known competency ids
        resource_count = 0
        for key, resources in RESOURCES.items():
            competency_id = key_to_id[key]
            for title, duration, milestone_description, url in resources:
                repo.resource_library.create(
                    db,
                    competency_id=competency_id,
                    title=title,
                    duration=duration,
                    milestone_description=milestone_description,
                    url=url,
                )
                resource_count += 1

        print(f"Loaded {len(COMPETENCIES)} competencies and {resource_count} resources for '{JOB_ROLE}'.")
    finally:
        db.close()


if __name__ == "__main__":
    load()
    sys.exit(0)
