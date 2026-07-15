"""Seed data for the demo (Area 3 T10).

Loads: 1 company + 1 HR account + 1 Web Developer JD (via the real JD-creation path,
Area 2 T4's extract_competencies, not a raw insert) + 30 candidates from
seed/raw/cv/ run through the real CV parsing pipeline (Area 2 T5) + embeddings (T6) +
match scores (T7).

Candidate interview-data tiers (revised 2026-07-13 — see execution-checklist.md Area 3 T10):
  - 27 profile-only: parsed_profiles + match_scores only
  - 2 pre-seeded synthetic interviews: real distinct audio clips (seed/raw/audio/),
    written with transcripts + rubric_scores + interview_summaries + hr_decisions
  - 1 live candidate: NO interview data — walked through the real flow during the demo recording

Idempotent: skips entirely if the demo company already exists.

Run: python -m seed.load_demo_data (from backend/, with .venv active)
"""

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from db import repositories as repo
from db.session import SessionLocal
from services import auth
from services.candidate_embedding import embed_candidate_profile, embed_jd_competencies
from services.candidate_ingest import ingest_cv
from services.extract import extract_competencies
from services.matching import compute_match_score, rank_candidates_for_job
from services.rubric_persist import compute_and_persist_interview_summary, score_and_persist_answer
from services.stt_client import transcribe
from services import storage
from seed.job_description_data import QUALIFICATIONS, REQUIREMENTS, RESPONSIBILITIES, TITLE

DEMO_COMPANY_NAME = "PT Gaskeun Demo"
DEMO_HR_EMAIL = "hr@gaskeundemo.test"
DEMO_HR_PASSWORD = "demo12345"  # local-only demo credential, never used in production

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CV_DIR = REPO_ROOT / "seed" / "raw" / "cv"
AUDIO_DIR = REPO_ROOT / "seed" / "raw" / "audio"

# The 2 synthetic interview candidates use these real, distinct pre-recorded clips.
SYNTHETIC_AUDIO_CLIPS = [
    AUDIO_DIR / "Recording 50 tahun pengalaman.m4a",
    AUDIO_DIR / "Recording dari web.mp3",
]

# A single canned interview question used for the synthetic candidates (real JD questions
# are generated once the job exists — see load(), which reuses the same question for all
# pre-seeded synthetic answers rather than calling the LLM 2x more than necessary).
SYNTHETIC_QUESTION_TEXT = "Ceritakan pengalaman Anda yang paling relevan dengan posisi ini."


def _seed_company_hr_job(db):
    company = repo.companies.create(db, name=DEMO_COMPANY_NAME)
    hr = repo.hr_users.create(
        db, company_id=company.id, email=DEMO_HR_EMAIL, password_hash=auth.hash_password(DEMO_HR_PASSWORD)
    )
    job = repo.jobs.create(
        db,
        company_id=company.id,
        title=TITLE,
        responsibilities=RESPONSIBILITIES,
        requirements=REQUIREMENTS,
        qualifications=QUALIFICATIONS,
        status="active",
    )
    # Real competency extraction (Area 2 T4), not a raw insert.
    competencies = extract_competencies(job.title, job.responsibilities, job.requirements, job.qualifications)
    for c in competencies:
        repo.jd_competencies.create(
            db, job_id=job.id, competency_name=c["competency_name"], importance_level=c["importance_level"]
        )
    embed_jd_competencies(db, job.id)
    return company, hr, job


def _seed_candidate_from_cv(db, job_id: int, cv_path: Path, alias: str):
    with open(cv_path, "rb") as f:
        file_bytes = f.read()

    token, expires_at = auth.generate_candidate_token()
    candidate = repo.candidates.create(
        db, job_id=job_id, alias=alias, token=token, token_expires_at=expires_at
    )
    ingest_cv(db, candidate.id, file_bytes, alias=alias)
    embed_candidate_profile(db, candidate.id)
    compute_match_score(db, candidate.id, job_id)
    return candidate


def _seed_synthetic_interview(db, candidate, question, audio_clip_path: Path, session_name: str, decision: str, hr_id: int):
    with open(audio_clip_path, "rb") as f:
        audio_bytes = f.read()

    audio_path = storage.save_audio(candidate.id, session_name, 1, audio_bytes)
    answer = repo.interview_answers.create(
        db, candidate_id=candidate.id, question_id=question.id, audio_path=audio_path
    )
    transcript_text = transcribe(audio_path)
    repo.transcripts.create(db, answer_id=answer.id, transcript_text=transcript_text)

    scored = score_and_persist_answer(db, answer.id)
    compute_and_persist_interview_summary(db, candidate.id, [scored["summary"]])

    decision_row = repo.hr_decisions.create(
        db, candidate_id=candidate.id, decision=decision, decided_by=hr_id, notes="Seed data — synthetic candidate"
    )

    # Demo them as fully-processed examples (Area 1 T7/T12's "Terkirim" — disabled,
    # already-sent — state), not re-triggerable on camera. A fabricated chat_id is fine
    # since send_report() is never actually called for these candidates.
    candidate.telegram_chat_id = f"synthetic-{candidate.id}"
    decision_row.report_sent_at = datetime.now(timezone.utc)
    db.commit()


def load():
    db = SessionLocal()
    try:
        existing = repo.companies.list(db, name=DEMO_COMPANY_NAME)
        if existing:
            print(f"Demo company '{DEMO_COMPANY_NAME}' already exists — skipping (idempotent).", flush=True)
            return

        cv_files = sorted(CV_DIR.glob("*.pdf"))
        if len(cv_files) < 30:
            print(f"WARNING: expected 30 CVs in {CV_DIR}, found {len(cv_files)}. Proceeding anyway.", flush=True)

        print("Seeding company, HR account, and JD (real extraction call)...", flush=True)
        company, hr, job = _seed_company_hr_job(db)
        print(f"  company_id={company.id} hr_id={hr.id} job_id={job.id}", flush=True)

        # A single approved question, reused for the 2 synthetic candidates' answers.
        question = repo.interview_questions.create(
            db, job_id=job.id, question_text=SYNTHETIC_QUESTION_TEXT, order_index=0, status="approved"
        )

        print(f"Ingesting {len(cv_files)} candidate CVs through the real parse pipeline...", flush=True)
        candidates = []
        failed = []
        for i, cv_path in enumerate(cv_files, start=1):
            alias = f"Kandidat WD-{i:02d}"
            t0 = time.time()
            try:
                candidate = _seed_candidate_from_cv(db, job.id, cv_path, alias)
            except Exception as e:
                db.rollback()
                failed.append((cv_path.name, str(e)))
                print(f"  [{i}/{len(cv_files)}] {alias} <- {cv_path.name} FAILED ({time.time()-t0:.1f}s): {e}", flush=True)
                continue
            candidates.append(candidate)
            print(
                f"  [{i}/{len(cv_files)}] {alias} <- {cv_path.name} "
                f"(candidate_id={candidate.id}, {time.time()-t0:.1f}s)",
                flush=True,
            )

        if failed:
            print(f"\n{len(failed)} CV(s) failed to ingest and were skipped:", flush=True)
            for name, err in failed:
                print(f"  - {name}: {err}", flush=True)

        rank_candidates_for_job(db, job.id)
        print("Ranked all candidates.", flush=True)

        # Tier assignment: last 2 candidates get synthetic interviews (arbitrary but fixed
        # choice — order doesn't carry meaning since the CVs are confirmed untiered/random).
        synthetic_candidates = candidates[-2:]
        live_candidate = candidates[-3] if len(candidates) >= 3 else None

        decisions_cycle = ["advance", "reject"]
        print("Seeding 2 synthetic interview candidates with real distinct audio...", flush=True)
        for i, (candidate, audio_clip) in enumerate(zip(synthetic_candidates, SYNTHETIC_AUDIO_CLIPS)):
            _seed_synthetic_interview(
                db, candidate, question, audio_clip, session_name=f"synthetic-{i+1}",
                decision=decisions_cycle[i], hr_id=hr.id,
            )
            print(f"  {candidate.alias}: interview seeded, decision={decisions_cycle[i]}", flush=True)

        if live_candidate:
            print(f"Live candidate (no interview data pre-seeded): {live_candidate.alias} (candidate_id={live_candidate.id})", flush=True)

        print()
        print(f"Done. {len(candidates)} candidates seeded: {len(candidates)-2} profile-only, 2 synthetic-interview, 1 designated live.", flush=True)
        print(f"HR login: {DEMO_HR_EMAIL} / {DEMO_HR_PASSWORD}", flush=True)
    finally:
        db.close()


if __name__ == "__main__":
    load()
    sys.exit(0)
