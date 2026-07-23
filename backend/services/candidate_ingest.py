"""End-to-end CV ingest pipeline (Area 2 T5): extract -> merge captions -> detect name ->
redact PII -> parse structured profile -> save file + DB row.
"""

from sqlalchemy.orm import Session

from db import repositories as repo
from services import cv_parser, pii_redaction, storage
from services.pdf_captioning import merge_pdf_text_and_captions
from services.pdf_extraction import extract_pdf


def ingest_cv(db: Session, candidate_id: int, file_bytes: bytes, alias: str) -> dict:
    """Runs the full pipeline for one candidate's CV and persists a parsed_profiles row.

    Returns the created ParsedProfile-equivalent dict for convenience/testing.
    """
    extraction = extract_pdf(file_bytes)
    merged_text = merge_pdf_text_and_captions(extraction)

    # Round-3 Task 19: capture the real email BEFORE redaction scrubs it, so it can be stored on
    # the candidate row for email delivery — everything downstream of this line (the LLM parse
    # call) still only ever sees the redacted text, unchanged from before.
    contact_email = pii_redaction.detect_candidate_email(merged_text)

    candidate_name = pii_redaction.detect_candidate_name(merged_text)
    redacted_text = pii_redaction.redact_pii(merged_text, alias=alias, candidate_name=candidate_name)

    parsed = cv_parser.parse_cv_text(redacted_text, alias=alias)

    if contact_email:
        candidate = repo.candidates.get(db, candidate_id)
        if candidate:
            candidate.contact_email = contact_email
            db.commit()

    raw_cv_path = storage.save_cv(candidate_id, file_bytes)

    profile = repo.parsed_profiles.create(
        db,
        candidate_id=candidate_id,
        skills=parsed["skills"],
        experience=parsed["experience"],
        qualifications=parsed["qualifications"],
        education_level=parsed["education_level"],
        major=parsed["major"],
        cv_summary=parsed["cv_summary"],
        skills_implicit=parsed["skills_implicit"],
        education_history=parsed["education_history"],
        certifications=parsed["certifications"],
        featured_projects=parsed["featured_projects"],
        organization_experience=parsed["organization_experience"],
        raw_cv_path=raw_cv_path,
        raw_text_redacted=redacted_text,
    )
    return profile
