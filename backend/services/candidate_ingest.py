"""End-to-end CV ingest pipeline (Area 2 T5): extract -> merge captions -> redact PII ->
parse structured profile -> save file + DB row.
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

    redacted_text = pii_redaction.redact_pii(merged_text, alias=alias)

    parsed = cv_parser.parse_cv_text(redacted_text, alias=alias)

    raw_cv_path = storage.save_cv(candidate_id, file_bytes)

    profile = repo.parsed_profiles.create(
        db,
        candidate_id=candidate_id,
        skills=parsed["skills"],
        experience=parsed["experience"],
        qualifications=parsed["qualifications"],
        raw_cv_path=raw_cv_path,
    )
    return profile
