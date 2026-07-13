from qdrant_client.models import PointStruct
from sqlalchemy.orm import Session

from db import repositories as repo
from db.vector_store import CANDIDATE_VECTORS_COLLECTION, JD_VECTORS_COLLECTION, client
from services.embeddings import embed_text


def _profile_to_text(skills: list, experience: list, qualifications: list) -> str:
    parts = []
    if skills:
        parts.append("Keterampilan: " + ", ".join(str(s) for s in skills))
    if experience:
        exp_lines = []
        for e in experience:
            if isinstance(e, dict):
                exp_lines.append(f"{e.get('role', '')} - {e.get('summary', '')}")
            else:
                exp_lines.append(str(e))
        parts.append("Pengalaman: " + "; ".join(exp_lines))
    if qualifications:
        parts.append("Kualifikasi: " + ", ".join(str(q) for q in qualifications))
    return "\n".join(parts)


def embed_candidate_profile(db: Session, candidate_id: int) -> None:
    profiles = repo.parsed_profiles.list(db, candidate_id=candidate_id)
    if not profiles:
        return
    profile = profiles[0]

    text = _profile_to_text(profile.skills, profile.experience, profile.qualifications)
    vector = embed_text(text)

    client.upsert(
        collection_name=CANDIDATE_VECTORS_COLLECTION,
        points=[
            PointStruct(
                id=candidate_id,
                vector=vector,
                payload={"candidate_id": candidate_id, "skills": profile.skills},
            )
        ],
    )


def embed_jd_competencies(db: Session, job_id: int) -> None:
    competencies = repo.jd_competencies.list(db, job_id=job_id)
    if not competencies:
        return

    text = "Kompetensi yang dibutuhkan: " + ", ".join(c.competency_name for c in competencies)
    vector = embed_text(text)

    client.upsert(
        collection_name=JD_VECTORS_COLLECTION,
        points=[
            PointStruct(
                id=job_id,
                vector=vector,
                payload={
                    "job_id": job_id,
                    "competencies": [c.competency_name for c in competencies],
                },
            )
        ],
    )
