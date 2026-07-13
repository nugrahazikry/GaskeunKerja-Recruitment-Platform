"""Matching engine (Area 2 T7): semantic similarity (Qdrant) + competency-graph boost.

overall_score = 0.7 * semantic_similarity + 0.3 * graph_boost
"""

import numpy as np
from sqlalchemy.orm import Session

from db import repositories as repo
from db.vector_store import CANDIDATE_VECTORS_COLLECTION, JD_VECTORS_COLLECTION, client

SEMANTIC_WEIGHT = 0.7
GRAPH_WEIGHT = 0.3


def _normalize(name: str) -> str:
    return name.strip().lower()


def compute_graph_boost(candidate_skills: list[str], job_id: int, db: Session) -> tuple[float, list[str]]:
    """Credit for candidate skills that relate (via competency_framework relations) to the
    JD's required competencies, even without an exact name match.

    Returns (boost in [0,1], list of competency names that drove the boost).
    """
    jd_competencies = repo.jd_competencies.list(db, job_id=job_id)
    if not jd_competencies:
        return 0.0, []

    candidate_skill_set = {_normalize(s) for s in candidate_skills}

    # Map competency_framework rows by normalized name, for relation lookups
    all_framework_rows = repo.competency_framework.list(db)
    name_to_row = {_normalize(row.competency_name): row for row in all_framework_rows}
    id_to_row = {row.id: row for row in all_framework_rows}

    matched_competencies: list[str] = []
    for jd_comp in jd_competencies:
        jd_name_norm = _normalize(jd_comp.competency_name)

        # Direct match: candidate has this exact competency
        if jd_name_norm in candidate_skill_set:
            matched_competencies.append(jd_comp.competency_name)
            continue

        # Graph match: candidate has a skill that IS a related competency of this JD competency
        framework_row = name_to_row.get(jd_name_norm)
        if framework_row:
            for related_id in framework_row.related_competency_ids:
                related_row = id_to_row.get(related_id)
                if related_row and _normalize(related_row.competency_name) in candidate_skill_set:
                    matched_competencies.append(jd_comp.competency_name)
                    break

    if not jd_competencies:
        return 0.0, []

    boost = len(matched_competencies) / len(jd_competencies)
    return boost, matched_competencies


def compute_match_score(db: Session, candidate_id: int, job_id: int) -> dict:
    """Computes and persists overall_score + competency_breakdown for one candidate vs one job."""
    profiles = repo.parsed_profiles.list(db, candidate_id=candidate_id)
    if not profiles:
        raise ValueError(f"No parsed_profiles for candidate {candidate_id}")
    profile = profiles[0]

    # Semantic similarity: cosine similarity between the candidate's and JD's own vectors,
    # computed directly (both are already unit-normalized by the embedding model's cosine
    # distance setup, but we normalize explicitly here to not depend on that assumption).
    candidate_point = client.retrieve(
        collection_name=CANDIDATE_VECTORS_COLLECTION, ids=[candidate_id], with_vectors=True
    )
    if not candidate_point:
        raise ValueError(f"No embedding for candidate {candidate_id} — run T6 embedding first")

    jd_point = client.retrieve(collection_name=JD_VECTORS_COLLECTION, ids=[job_id], with_vectors=True)
    if not jd_point:
        raise ValueError(f"No embedding for job {job_id} — run T6 embedding first")

    cand_vec = np.array(candidate_point[0].vector)
    jd_vec = np.array(jd_point[0].vector)
    semantic_similarity = float(
        np.dot(cand_vec, jd_vec) / (np.linalg.norm(cand_vec) * np.linalg.norm(jd_vec))
    )

    graph_boost, matched = compute_graph_boost(profile.skills, job_id, db)

    overall_score = SEMANTIC_WEIGHT * semantic_similarity + GRAPH_WEIGHT * graph_boost

    breakdown = {
        "semantic_similarity": semantic_similarity,
        "graph_boost": graph_boost,
        "matched_competencies": matched,
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
