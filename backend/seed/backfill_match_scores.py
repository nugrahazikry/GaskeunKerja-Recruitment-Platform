"""One-off backfill (Round-3 follow-up #9, 2026-07-19): runs the CURRENT skill-gap + match-scoring
pipeline (compute_match_score) for every candidate that has never been analyzed under it.

Root cause this closes: compute_match_score() was historically only ever invoked by one-off seed
scripts (load_demo_data.py, load_t5_fixture.py) at initial demo setup, using whatever formula
existed at that time. Every ranking-formula change this session (semantic+graph -> proficiency-
weighted -> coverage/quality 90/10) was only ever re-applied to job 16's "Data siap" candidates
that got manually reanalyzed during live testing — every other job's candidates still carry a
stale match_scores row from that original one-time seed run, with no skill_gap_results at all
(hence "Belum diproses" on Shortlist despite showing an old score number).

Scoped to candidates that (a) have a parsed_profiles row (nothing to score without one) and
(b) do NOT already have a skill_gap_results row for their job (already-analyzed candidates, e.g.
job 16's 6 "Data siap" ones, are left untouched — this only fills the actual gap). Real LLM cost:
5 calls per candidate (3 skill-gap votes + 1 proficiency + 1 recommendation-extras) — flagged here
rather than auto-run without visibility; run with --limit for a partial pass first.

Run: python -m seed.backfill_match_scores [--limit N] (from backend/, with .venv active)
"""

import argparse

from db import repositories as repo
from db.session import SessionLocal
from services.matching import compute_match_score, rank_candidates_for_job


def run(limit: int | None = None) -> None:
    db = SessionLocal()
    try:
        candidates = repo.candidates.list(db)
        todo = []
        for candidate in candidates:
            profiles = repo.parsed_profiles.list(db, candidate_id=candidate.id)
            if not profiles:
                continue
            existing_gap = repo.skill_gap_results.list(db, candidate_id=candidate.id, job_id=candidate.job_id)
            if existing_gap:
                continue
            todo.append(candidate)

        if limit is not None:
            todo = todo[:limit]

        print(f"Backfilling match scores for {len(todo)} of {len(candidates)} candidates (already-analyzed skipped)")

        job_ids_touched: set[int] = set()
        skipped_no_competencies = 0
        for candidate in todo:
            required = repo.jd_competencies.list(db, job_id=candidate.job_id, status="active")
            if not required:
                skipped_no_competencies += 1
                print(f"  skip candidate={candidate.id} job={candidate.job_id}: job has no active competencies")
                continue
            try:
                result = compute_match_score(db, candidate.id, candidate.job_id)
            except ValueError as e:
                print(f"  skip candidate={candidate.id} job={candidate.job_id}: {e}")
                continue
            job_ids_touched.add(candidate.job_id)
            print(f"  scored candidate={candidate.id} job={candidate.job_id} -> {result['overall_score']:.3f}")

        for job_id in job_ids_touched:
            rank_candidates_for_job(db, job_id)

        print(
            f"Backfill done: {len(todo) - skipped_no_competencies} candidates scored across "
            f"{len(job_ids_touched)} job(s), {skipped_no_competencies} skipped (job has no competencies)."
        )
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    run(limit=args.limit)
