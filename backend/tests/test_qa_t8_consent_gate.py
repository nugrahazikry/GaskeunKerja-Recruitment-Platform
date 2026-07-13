"""Area 5 QA T8: consent-gate enforcement test.

Submit an interview answer for a candidate with no consent_records row -> assert it's
rejected (ConsentRequiredError, which routers/interview_answers.py maps to a real HTTP
403). Submit again after a valid consent record exists -> assert success. This is the
exact test Area 2 T10 already assumes exists.

Uses a T5-fixture candidate (FIXTURE-MID-1) rather than the real demo pool, and reuses
one of the existing real seed audio clips for the success-path STT call (small real
cost — one real Groq Whisper call) rather than fabricating new audio.
"""

from pathlib import Path

import pytest

from db import repositories as repo
from db.session import SessionLocal
from services.consent import ConsentRequiredError, record_consent
from services.interview_answers import submit_answer
from seed.load_t5_fixture import FIXTURE_JOB_TITLE

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
AUDIO_CLIP = REPO_ROOT / "seed" / "raw" / "audio" / "Recording dari web.mp3"


def _get_fixture_candidate_and_question(db):
    jobs = repo.jobs.list(db, title=FIXTURE_JOB_TITLE)
    assert jobs, f"Fixture JD '{FIXTURE_JOB_TITLE}' not found — run seed.load_t5_fixture first"
    job = jobs[0]

    candidates = repo.candidates.list(db, job_id=job.id, alias="FIXTURE-MID-1")
    assert candidates, "FIXTURE-MID-1 not found — run seed.load_t5_fixture first"
    candidate = candidates[0]

    questions = repo.interview_questions.list(db, job_id=job.id, status="approved")
    if not questions:
        question = repo.interview_questions.create(
            db, job_id=job.id, question_text="Pertanyaan uji T8.", order_index=0, status="approved"
        )
    else:
        question = questions[0]

    return candidate, question


def test_submit_without_consent_is_rejected():
    db = SessionLocal()
    try:
        candidate, question = _get_fixture_candidate_and_question(db)

        # Ensure no consent record exists for this run
        for record in repo.consent_records.list(db, candidate_id=candidate.id):
            db.delete(record)
        db.commit()

        with pytest.raises(ConsentRequiredError):
            submit_answer(db, candidate.id, question.id, b"fake-audio-bytes", session="qa-t8-no-consent")
    finally:
        db.close()


def test_submit_with_valid_consent_succeeds():
    db = SessionLocal()
    try:
        candidate, question = _get_fixture_candidate_and_question(db)

        if not repo.consent_records.list(db, candidate_id=candidate.id):
            record_consent(db, candidate.id, consent_text_version="qa-t8-test")

        audio_bytes = AUDIO_CLIP.read_bytes()
        result = submit_answer(db, candidate.id, question.id, audio_bytes, session="qa-t8-with-consent")

        assert result["answer_id"] is not None
        assert result["transcript_text"] != ""
    finally:
        # Clean up the answer/transcript this test created, leave the consent record
        # (harmless, fixture-only data) and the audio file on disk (small, test-owned dir).
        # Delete transcripts BEFORE their parent interview_answers rows (FK order).
        answers = repo.interview_answers.list(db, candidate_id=candidate.id)
        for answer in answers:
            for transcript in repo.transcripts.list(db, answer_id=answer.id):
                db.delete(transcript)
        db.commit()
        for answer in answers:
            db.delete(answer)
        db.commit()
        db.close()
