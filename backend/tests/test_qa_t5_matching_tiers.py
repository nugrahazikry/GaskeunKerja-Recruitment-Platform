"""Area 5 QA T5: matching formula / curated-tier check.

Asserts the strong-tier fixture candidates' average match score is meaningfully higher
than the weak-tier average — an aggregate comparison, not strict per-candidate ordering
(per the 2026-07-12 resolution: brittle per-candidate ordering risks false failures on
real, messy CV data even within a deliberately curated fixture).

Requires seed/load_t5_fixture.py to have been run first (creates the "Web Developer (QA
Fixture)" JD with 6 tiered candidates, fully separate from the 30-CV demo pool).
"""

from db import repositories as repo
from db.session import SessionLocal
from seed.fixture_cv_content import ALL_FIXTURE_CVS
from seed.load_t5_fixture import FIXTURE_JOB_TITLE

MEANINGFUL_GAP = 0.05  # minimum required average-score gap between strong and weak tiers


def test_strong_tier_meaningfully_outscores_weak_tier():
    db = SessionLocal()
    try:
        jobs = repo.jobs.list(db, title=FIXTURE_JOB_TITLE)
        assert jobs, f"Fixture JD '{FIXTURE_JOB_TITLE}' not found — run seed.load_t5_fixture first"
        job = jobs[0]

        alias_to_tier = {alias: tier for tier, alias, _ in ALL_FIXTURE_CVS}

        scores = repo.match_scores.list(db, job_id=job.id)
        assert len(scores) == 6, f"expected 6 fixture match_scores, found {len(scores)}"

        tier_scores: dict[str, list[float]] = {"strong": [], "mid": [], "weak": []}
        for score in scores:
            candidate = repo.candidates.get(db, score.candidate_id)
            tier = alias_to_tier[candidate.alias]
            tier_scores[tier].append(score.overall_score)

        for tier, values in tier_scores.items():
            assert len(values) == 2, f"expected 2 {tier}-tier candidates, found {len(values)}"

        strong_avg = sum(tier_scores["strong"]) / len(tier_scores["strong"])
        weak_avg = sum(tier_scores["weak"]) / len(tier_scores["weak"])

        gap = strong_avg - weak_avg
        assert gap >= MEANINGFUL_GAP, (
            f"strong-tier average ({strong_avg:.4f}) does not meaningfully outscore "
            f"weak-tier average ({weak_avg:.4f}) — gap {gap:.4f} < required {MEANINGFUL_GAP}"
        )
    finally:
        db.close()
