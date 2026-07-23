"""Matching engine (Area 2 T7, replaced 2026-07-19).

Round-3 follow-up: overall_score used to be 0.7*semantic_similarity + 0.3*graph_boost (embedding
cosine similarity + a curated exact-name-or-graph-relation check). User-requested replacement
after finding real cases where semantic similarity ranked a candidate poorly despite the detail
page's grounded skill-gap analysis correctly showing they had the required competency (e.g. "Cloud
Deployment") — semantic similarity is a single fuzzy number over the WHOLE profile blob vs the
WHOLE JD blob (see candidate_embedding.py), so it can't reflect one specific missing/present skill
accurately, and is prone to false positives (topical similarity isn't skill possession).

New formula reuses the ALREADY-GROUNDED skill-gap analysis (services/skillgap.py) that the
candidate-detail page already shows — same matched/missing list, same source of truth, no second
disagreeing system.

Round-3 follow-up #2 (2026-07-19, user-requested redesign): the first version of this formula
(sum of proficiency points / (3 × required)) let a low proficiency rating on MOST matched
competencies drag the score down disproportionately — e.g. 7/10 matched, mostly rated "Pemula"
(1 star), scored only 33%, which read as "Kurang Cocok" despite matching 70% of requirements. User
wanted coverage (did they match the skill AT ALL) to dominate, with proficiency as a secondary
refinement — but a naive "coverage% + level bonus" risks exceeding 100 when a candidate is fully
matched at max level. Solved with a WEIGHTED CONVEX COMBINATION of two independent 0-100(%) scores,
which is mathematically guaranteed to never exceed 100 (a weighted average of two numbers ≤100,
with weights summing to 1, can never exceed the larger input):

    coverage_score = (matched_count / total_required) × 100
    quality_score  = (avg proficiency of matched competencies / 3) × 100
    overall_score  = COVERAGE_WEIGHT × coverage_score + QUALITY_WEIGHT × quality_score

Round-3 follow-up #3 (2026-07-19, weight retune, two steps same day): first moved 70/30 -> 80/20,
then user asked to go further to 90/10 coverage-dominant — coverage should matter almost
exclusively, proficiency only a light tiebreaker. With COVERAGE_WEIGHT=0.9, QUALITY_WEIGHT=0.1:
7/10 matched at mostly "Pemula" (avg ~1.43/3) now scores 0.9×70 + 0.1×47.6 = 63 + 4.76 = ~67.8%,
not 33% — coverage dominates almost entirely, proficiency still nudges apart two candidates with
the identical match count. At 10/10 matched all "Mahir" (max): coverage=100, quality=100,
overall=100 exactly — no overflow at any weight split that sums to 1, by construction, not by
clamping.
"""

from sqlalchemy.orm import Session

from db import repositories as repo
from services.skillgap import combine_skills, persist_skill_gap

COVERAGE_WEIGHT = 0.9
QUALITY_WEIGHT = 0.1


def compute_match_score(db: Session, candidate_id: int, job_id: int) -> dict:
    """Computes and persists overall_score + competency_breakdown for one candidate vs one job.

    Always (re)computes the skill-gap analysis first (persist_skill_gap) — the ranking score is
    now entirely derived from its output, so there is no other data source needed here."""
    profiles = repo.parsed_profiles.list(db, candidate_id=candidate_id)
    if not profiles:
        raise ValueError(f"No parsed_profiles for candidate {candidate_id}")
    profile = profiles[0]

    jd_competencies = repo.jd_competencies.list(db, job_id=job_id, status="active")
    required_names = [c.competency_name for c in jd_competencies]

    gap = persist_skill_gap(
        db,
        candidate_id,
        job_id,
        combine_skills(profile.skills, profile.skills_implicit),
        required_names,
        candidate_experience=profile.experience,
    )

    overall_score = _score_from_skill_gap(gap["matched_competencies"], gap["competency_proficiency"], required_names)

    breakdown = {
        "matched_competencies": gap["matched_competencies"],
        "missing_competencies": gap["missing_competencies"],
        "competency_proficiency": gap["competency_proficiency"],
    }

    existing = repo.match_scores.list(db, candidate_id=candidate_id, job_id=job_id)
    for row in existing:
        db.delete(row)
    db.commit()

    repo.match_scores.create(
        db,
        candidate_id=candidate_id,
        job_id=job_id,
        overall_score=overall_score,
        competency_breakdown=breakdown,
        rank=0,  # rank is assigned in bulk by rank_candidates_for_job()
    )

    return {"overall_score": overall_score, "competency_breakdown": breakdown}


def _score_from_skill_gap(
    matched_competencies: list[str], competency_proficiency: dict[str, int], required_names: list[str]
) -> float:
    """0-1 score: COVERAGE_WEIGHT × coverage_score + QUALITY_WEIGHT × quality_score (see module
    docstring for the full derivation). Returns 0.0 for a job with no required competencies
    (nothing to score against) rather than dividing by zero.

    Real bug found via live testing (2026-07-19): matched_competencies comes from a persisted
    skill_gap_results row, which can go STALE relative to the job's CURRENT active competency list
    if the JD was edited (competencies added/dismissed) after that row was computed — a known,
    documented limitation (see point #12's "Analisis Ulang" escape hatch, and _extract_and_store_
    competencies' scope-guard note that match_scores was never auto-invalidated on JD edit either).
    Concretely: a candidate's stale matched_competencies contained 2 competency names that were no
    longer in the job's active list at all, and the score was counting them anyway — 9 stale matches
    summed against a 10-item CURRENT required count, producing a score inconsistent with the "7/10"
    the UI actually shows (which correctly filters to current active competencies). Fixed by
    intersecting matched_competencies with required_names (normalized) before scoring, so a
    since-removed competency can never inflate the score — coverage/quality are now always
    consistent with what the checklist displays."""
    if not required_names:
        return 0.0
    required_normalized = {name.strip().lower() for name in required_names}
    relevant_matched = [name for name in matched_competencies if name.strip().lower() in required_normalized]

    coverage_score = len(relevant_matched) / len(required_names) * 100

    if relevant_matched:
        avg_proficiency = sum(competency_proficiency.get(name, 2) for name in relevant_matched) / len(
            relevant_matched
        )
        quality_score = avg_proficiency / 3 * 100
    else:
        quality_score = 0.0

    overall_percent = COVERAGE_WEIGHT * coverage_score + QUALITY_WEIGHT * quality_score
    return overall_percent / 100


def rescore_from_existing_skill_gap(db: Session, candidate_id: int, job_id: int) -> dict | None:
    """Round-3 follow-up (2026-07-19): re-derives overall_score from an ALREADY-PERSISTED
    skill_gap_results row, without triggering a new LLM analysis — used by the one-off rescoring
    script to migrate existing candidates from the old semantic+graph formula to the new
    proficiency-weighted one, scoped to only candidates whose skill-gap is already cached ("Data
    siap"), per explicit user instruction not to force a bulk recompute for everyone else."""
    existing = repo.skill_gap_results.list(db, candidate_id=candidate_id, job_id=job_id)
    if not existing:
        return None
    gap = existing[0]

    jd_competencies = repo.jd_competencies.list(db, job_id=job_id, status="active")
    required_names = [c.competency_name for c in jd_competencies]

    overall_score = _score_from_skill_gap(
        gap.matched_competencies, gap.competency_proficiency or {}, required_names
    )
    breakdown = {
        "matched_competencies": gap.matched_competencies,
        "missing_competencies": gap.missing_competencies,
        "competency_proficiency": gap.competency_proficiency or {},
    }

    scores = repo.match_scores.list(db, candidate_id=candidate_id, job_id=job_id)
    if scores:
        scores[0].overall_score = overall_score
        scores[0].competency_breakdown = breakdown
        db.commit()
    else:
        repo.match_scores.create(
            db,
            candidate_id=candidate_id,
            job_id=job_id,
            overall_score=overall_score,
            competency_breakdown=breakdown,
            rank=0,
        )
        db.commit()

    return {"overall_score": overall_score, "competency_breakdown": breakdown}


def rank_candidates_for_job(db: Session, job_id: int) -> list[dict]:
    """Recomputes rank for all candidates of a job, based on their already-computed overall_score."""
    scores = repo.match_scores.list(db, job_id=job_id)
    scores.sort(key=lambda s: s.overall_score, reverse=True)

    for rank, score in enumerate(scores, start=1):
        score.rank = rank
    db.commit()

    return [
        {"candidate_id": s.candidate_id, "overall_score": s.overall_score, "rank": s.rank}
        for s in scores
    ]
