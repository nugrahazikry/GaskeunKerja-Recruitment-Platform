"""Round-2 polish (2026-07-17): one-off backfill for skill_gap_results.

compute_match_score() now persists a skill_gap_results row as of this session's change, but
every match_scores row created BEFORE this change (the ~30-candidate demo pool, the T5 fixture,
etc.) has no corresponding skill_gap_results row yet. candidate_detail.py/report.py self-heal by
computing on first read, but that means the FIRST click into each such candidate is still a real
~25-30s wait. This script pre-warms all of them ahead of a demo so nothing is slow on first view.

Idempotent: skips any (candidate_id, job_id) pair that already has a skill_gap_results row.

Run: python -m seed.backfill_skill_gap (from backend/, with .venv active)
"""

from db import repositories as repo
from db.session import SessionLocal
from services.skillgap import persist_skill_gap


def backfill() -> None:
    db = SessionLocal()
    try:
        all_match_scores = repo.match_scores.list(db)
        existing_pairs = {
            (row.candidate_id, row.job_id) for row in repo.skill_gap_results.list(db)
        }

        computed = 0
        skipped = 0
        for score in all_match_scores:
            key = (score.candidate_id, score.job_id)
            if key in existing_pairs:
                skipped += 1
                continue

            profiles = repo.parsed_profiles.list(db, candidate_id=score.candidate_id)
            if not profiles:
                print(f"  skip candidate={score.candidate_id}: no parsed profile")
                continue

            jd_competencies = repo.jd_competencies.list(db, job_id=score.job_id)
            required = [c.competency_name for c in jd_competencies]

            persist_skill_gap(
                db, score.candidate_id, score.job_id, profiles[0].skills, required,
                candidate_experience=profiles[0].experience,
            )
            existing_pairs.add(key)
            computed += 1
            print(f"  computed candidate={score.candidate_id} job={score.job_id}")

        print(f"Backfill done: {computed} computed, {skipped} already had a row.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
