"""One-off cleanup (2026-07-17): remove duplicate jd_competencies rows created by the
re-extraction/restore duplicate-name bug fixed the same day (see routers/jobs.py
_extract_and_store_competencies / _active_duplicate_exists).

For each (job_id, normalized name) group with more than one row, keeps exactly one:
prefers a row with status='active' (there should only ever be one after this cleanup); if none
is active, keeps the most recently created (highest id) dismissed row. Deletes the rest.

Run: python -m seed.dedupe_competencies (from backend/, with .venv active)
"""

from collections import defaultdict

from db import repositories as repo
from db.session import SessionLocal


def dedupe() -> None:
    db = SessionLocal()
    try:
        all_rows = repo.jd_competencies.list(db)
        groups: dict[tuple[int, str], list] = defaultdict(list)
        for row in all_rows:
            key = (row.job_id, row.competency_name.strip().lower())
            groups[key].append(row)

        removed = 0
        for (job_id, name), rows in groups.items():
            if len(rows) <= 1:
                continue

            active_rows = [r for r in rows if r.status == "active"]
            if active_rows:
                keep = min(active_rows, key=lambda r: r.id)
            else:
                keep = max(rows, key=lambda r: r.id)

            for row in rows:
                if row.id == keep.id:
                    continue
                print(
                    f"  removing duplicate id={row.id} job_id={job_id} name={row.competency_name!r} "
                    f"status={row.status} source={row.source} (keeping id={keep.id})"
                )
                db.delete(row)
                removed += 1

        db.commit()
        print(f"Dedupe done: {removed} duplicate row(s) removed.")
    finally:
        db.close()


if __name__ == "__main__":
    dedupe()
