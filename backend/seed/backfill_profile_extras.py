"""One-off backfill (Round-3 follow-up #4, 2026-07-19): populate the new candidate-detail/laporan
redesign fields (cv_summary, skills_implicit, education_history, certifications, featured_projects,
organization_experience) on parsed_profiles rows created BEFORE this feature — those rows have
NULL/empty values for all of them since the old cv_parser prompt never asked for them.

Re-reads each candidate's already-stored raw CV file, re-runs the (now-extended) cv_parser LLM
call, and UPDATES the existing parsed_profiles row's new columns only (skills/experience/
qualifications/education_level/major are left untouched — no need to disturb already-correct,
already-matched-against data). Costs one deepseek-v4-flash call per candidate — real but cheap
LLM cost, flagged here rather than auto-run broadly; run with a --limit for a quick spot check
first.

Usage: python -m seed.backfill_profile_extras [--limit N] [--force] [--candidate-id ID]

--force reprocesses rows that already have cv_summary set (e.g. after a prompt change like
Round-3 follow-up #6's bullets/Indonesian-language extraction) instead of only filling in NULLs.
--candidate-id restricts to one candidate, for a cheap spot-check before a broad re-run.
"""

import argparse
import logging

from db import repositories as repo
from db.session import SessionLocal
from services import cv_parser, pii_redaction
from services.pdf_captioning import merge_pdf_text_and_captions
from services.pdf_extraction import extract_pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backfill_profile_extras")


def run(limit: int | None = None, force: bool = False, candidate_id: int | None = None) -> None:
    db = SessionLocal()
    try:
        profiles = repo.parsed_profiles.list(db)
        if candidate_id is not None:
            todo = [p for p in profiles if p.candidate_id == candidate_id]
        else:
            todo = profiles if force else [p for p in profiles if not p.cv_summary]
        if limit is not None:
            todo = todo[:limit]

        print(f"Backfilling {len(todo)} of {len(profiles)} parsed_profiles rows (already-enriched rows skipped)")

        for profile in todo:
            candidate = repo.candidates.get(db, profile.candidate_id)
            if not candidate:
                print(f"  skip profile={profile.id}: candidate {profile.candidate_id} not found")
                continue

            try:
                with open(profile.raw_cv_path, "rb") as f:
                    file_bytes = f.read()
            except OSError as e:
                print(f"  skip profile={profile.id} candidate={candidate.id}: cannot read raw_cv_path ({e})")
                continue

            extraction = extract_pdf(file_bytes)
            merged_text = merge_pdf_text_and_captions(extraction)
            candidate_name = pii_redaction.detect_candidate_name(merged_text)
            redacted_text = pii_redaction.redact_pii(merged_text, alias=candidate.alias, candidate_name=candidate_name)

            parsed = cv_parser.parse_cv_text(redacted_text, alias=candidate.alias)

            profile.cv_summary = parsed["cv_summary"]
            profile.skills_implicit = parsed["skills_implicit"]
            profile.education_history = parsed["education_history"]
            profile.certifications = parsed["certifications"]
            profile.featured_projects = parsed["featured_projects"]
            profile.organization_experience = parsed["organization_experience"]
            # experience gains a "tags" key per item in the new prompt — refresh it too so the
            # redesigned UI's work-experience tag chips aren't empty for backfilled candidates.
            profile.experience = parsed["experience"]
            db.commit()

            print(f"  backfilled profile={profile.id} candidate={candidate.id} ({candidate.alias})")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--candidate-id", type=int, default=None)
    args = parser.parse_args()
    run(limit=args.limit, force=args.force, candidate_id=args.candidate_id)
