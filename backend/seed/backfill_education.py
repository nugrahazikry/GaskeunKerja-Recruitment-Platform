"""Round-3 Task 20: one-off backfill for education_level/major/required_education_level/
required_major on the pre-existing (~36-candidate) demo pool — these columns didn't exist when
those rows were created, so they're all NULL until backfilled.

Two independent passes:
  1. Jobs: re-runs extract.extract_education_requirement() against each job's existing
     `qualifications` text — one cheap LLM call per job, no PDF re-read needed.
  2. Candidates: re-reads each candidate's stored raw CV PDF (raw_cv_path), re-runs the same
     extract -> redact -> parse steps candidate_ingest.ingest_cv() runs at upload time, and
     writes only education_level/major onto the existing parsed_profiles row (skills/experience/
     qualifications/raw_cv_path are left untouched).

Idempotent: skips any row that already has education_level / required_education_level set.
Real LLM cost (a vision-fallback pass may trigger for scanned CVs, plus one parse call per
candidate) — flagged, not auto-run. Run only to warm a demo:
  python -m seed.backfill_education (from backend/, with .venv active)
"""

from pathlib import Path

from db import repositories as repo
from db.session import SessionLocal
from services import cv_parser, extract, pii_redaction
from services.pdf_captioning import merge_pdf_text_and_captions
from services.pdf_extraction import extract_pdf


def backfill_jobs() -> None:
    db = SessionLocal()
    try:
        jobs = repo.jobs.list(db)
        updated = skipped = 0
        for job in jobs:
            if job.required_education_level is not None:
                skipped += 1
                continue
            education = extract.extract_education_requirement(job.qualifications)
            job.required_education_level = education["required_education_level"]
            job.required_major = education["required_major"]
            db.commit()
            updated += 1
            print(f"  job={job.id} -> required_education_level={education['required_education_level']!r}")
        print(f"Jobs backfill done: {updated} updated, {skipped} already had a value.")
    finally:
        db.close()


def backfill_candidates() -> None:
    db = SessionLocal()
    try:
        profiles = repo.parsed_profiles.list(db)
        updated = skipped = missing_file = 0
        for profile in profiles:
            if profile.education_level is not None:
                skipped += 1
                continue

            path = Path(profile.raw_cv_path)
            if not path.exists():
                missing_file += 1
                print(f"  skip candidate={profile.candidate_id}: CV file not found on disk")
                continue

            candidate = repo.candidates.get(db, profile.candidate_id)
            alias = candidate.alias if candidate else "kandidat"

            file_bytes = path.read_bytes()
            extraction = extract_pdf(file_bytes)
            merged_text = merge_pdf_text_and_captions(extraction)
            candidate_name = pii_redaction.detect_candidate_name(merged_text)
            redacted_text = pii_redaction.redact_pii(merged_text, alias=alias, candidate_name=candidate_name)
            parsed = cv_parser.parse_cv_text(redacted_text, alias=alias)

            profile.education_level = parsed["education_level"]
            profile.major = parsed["major"]
            db.commit()
            updated += 1
            print(f"  candidate={profile.candidate_id} -> education_level={parsed['education_level']!r}")

        print(f"Candidates backfill done: {updated} updated, {skipped} already had a value, {missing_file} missing files.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill_jobs()
    backfill_candidates()
