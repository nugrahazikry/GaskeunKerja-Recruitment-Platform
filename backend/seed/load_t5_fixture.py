"""Area 5 QA T5-fixture: a small dedicated tiered CV fixture, kept fully separate from
the 30-CV demo pool (which is confirmed random/untiered per the 2026-07-12 decision).

Creates its own test JD ("Web Developer (QA Fixture)") under the same demo company, so
it never appears mixed into the real Web Developer job's shortlist. Ingests 6 synthetic
CVs (2 strong/2 mid/2 weak fit) through the real pipeline (ingest_cv -> embed -> match),
tagging each candidate's intended tier in its alias so T5 can read it back directly
without a separate manifest.

Idempotent: skips if the fixture JD already exists. Not part of load_demo_data.py's main
seed path — run separately, on demand, only for QA test purposes.

Run: python -m seed.load_t5_fixture (from backend/, with .venv active)
"""

import io
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from db import repositories as repo
from db.session import SessionLocal
from services import auth
from services.candidate_embedding import embed_candidate_profile, embed_jd_competencies
from services.candidate_ingest import ingest_cv
from services.extract import extract_competencies
from services.matching import compute_match_score, rank_candidates_for_job
from seed.fixture_cv_content import ALL_FIXTURE_CVS
from seed.job_description_data import QUALIFICATIONS, REQUIREMENTS, RESPONSIBILITIES, TITLE

FIXTURE_JOB_TITLE = f"{TITLE} (QA Fixture)"
DEMO_COMPANY_NAME = "PT Gaskeun Demo"


def _text_to_pdf_bytes(alias: str, text: str) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica", 10)
    for line in text.strip().split("\n"):
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50
        c.drawString(50, y, line[:110])
        y -= 14
    c.save()
    return buf.getvalue()


def _seed_fixture_job(db, company_id: int):
    job = repo.jobs.create(
        db,
        company_id=company_id,
        title=FIXTURE_JOB_TITLE,
        responsibilities=RESPONSIBILITIES,
        requirements=REQUIREMENTS,
        qualifications=QUALIFICATIONS,
        status="active",
    )
    competencies = extract_competencies(job.title, job.responsibilities, job.requirements, job.qualifications)
    for c in competencies:
        repo.jd_competencies.create(
            db, job_id=job.id, competency_name=c["competency_name"], importance_level=c["importance_level"]
        )
    embed_jd_competencies(db, job.id)
    return job


def _seed_fixture_candidate(db, job_id: int, alias: str, cv_text: str):
    pdf_bytes = _text_to_pdf_bytes(alias, cv_text)
    token, expires_at = auth.generate_candidate_token()
    candidate = repo.candidates.create(
        db, job_id=job_id, alias=alias, token=token, token_expires_at=expires_at
    )
    ingest_cv(db, candidate.id, pdf_bytes, alias=alias)
    embed_candidate_profile(db, candidate.id)
    compute_match_score(db, candidate.id, job_id)
    return candidate


def load():
    db = SessionLocal()
    try:
        existing = repo.jobs.list(db, title=FIXTURE_JOB_TITLE)
        if existing:
            print(f"Fixture JD '{FIXTURE_JOB_TITLE}' already exists (job_id={existing[0].id}) — skipping (idempotent).", flush=True)
            return existing[0].id

        companies = repo.companies.list(db, name=DEMO_COMPANY_NAME)
        if not companies:
            print(f"ERROR: demo company '{DEMO_COMPANY_NAME}' not found. Run load_demo_data first.", flush=True)
            sys.exit(1)
        company = companies[0]

        print(f"Creating fixture JD under company_id={company.id}...", flush=True)
        job = _seed_fixture_job(db, company.id)
        print(f"  fixture job_id={job.id}", flush=True)

        print("Ingesting 6 tiered fixture CVs...", flush=True)
        for tier, alias, cv_text in ALL_FIXTURE_CVS:
            candidate = _seed_fixture_candidate(db, job.id, alias, cv_text)
            print(f"  [{tier}] {alias} -> candidate_id={candidate.id}", flush=True)

        rank_candidates_for_job(db, job.id)
        print("Ranked fixture candidates.", flush=True)
        print(f"\nDone. Fixture job_id={job.id}, 6 candidates seeded (2 strong/2 mid/2 weak).", flush=True)
        return job.id
    finally:
        db.close()


if __name__ == "__main__":
    load()
    sys.exit(0)
