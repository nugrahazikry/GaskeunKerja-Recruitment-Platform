"""One-off rescoring script (2026-07-19): migrates existing match_scores rows from the old
semantic-similarity + graph-boost formula to the new proficiency-weighted skill-gap formula (see
services/matching.py's module docstring for why the formula changed).

Scoped to "Data siap" candidates ONLY, per explicit user instruction: this does NOT trigger a new
skill-gap LLM analysis for candidates that don't have one yet — it only re-derives overall_score
from an ALREADY-PERSISTED skill_gap_results row (rescore_from_existing_skill_gap). Candidates
without one keep their old score until they're visited individually (self-heals, same lazy-backfill
design as skill-gap itself) or until seed.backfill_skill_gap is run for them.

Idempotent: safe to run multiple times — always re-derives from whatever is currently persisted.

Run: python -m seed.rescore_from_skill_gap (from backend/, with .venv active)
"""

from db import repositories as repo
from db.session import SessionLocal
from services.matching import rank_candidates_for_job, rescore_from_existing_skill_gap


def rescore() -> None:
    db = SessionLocal()
    try:
        all_match_scores = repo.match_scores.list(db)
        job_ids_touched: set[int] = set()

        rescored = 0
        skipped = 0
        for score in all_match_scores:
            result = rescore_from_existing_skill_gap(db, score.candidate_id, score.job_id)
            if result is None:
                skipped += 1
                print(f"  skip candidate={score.candidate_id} job={score.job_id}: no skill_gap_results yet")
                continue
            rescored += 1
            job_ids_touched.add(score.job_id)
            print(f"  rescored candidate={score.candidate_id} job={score.job_id} -> {result['overall_score']:.3f}")

        for job_id in job_ids_touched:
            rank_candidates_for_job(db, job_id)

        print(
            f"Rescore done: {rescored} candidates rescored across {len(job_ids_touched)} job(s), "
            f"{skipped} skipped (not yet 'Data siap')."
        )
    finally:
        db.close()


if __name__ == "__main__":
    rescore()
