import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from config import EMAIL_ENABLED
from db import repositories as repo
from db.session import SessionLocal
from services import storage, stt_client
from services.consent import ConsentRequiredError, require_consent
from services.delivery import send_interview_finished_email
from services.rubric_persist import compute_and_persist_interview_summary, score_and_persist_answer
from services.skillgap import update_recommendation_extras_after_interview

logger = logging.getLogger("interview_answers")


def _delete_answer(db: Session, answer) -> None:
    """Wipes an interview_answers row and everything that points at it (transcripts, rubric
    scores) plus its video file. Children are deleted in their OWN commit before the parent —
    there's no SQLAlchemy `relationship()` between these models (just raw FK columns, per this
    codebase's flat-repository style), so the unit-of-work has no dependency graph to order a
    single flush correctly, and deleting the answer row first 500s on the FK from transcripts/
    rubric_scores still pointing at it."""
    for t in repo.transcripts.list(db, answer_id=answer.id):
        db.delete(t)
    for r in repo.rubric_scores.list(db, answer_id=answer.id):
        db.delete(r)
    db.commit()
    db.delete(answer)
    db.commit()
    storage.delete_audio(answer.audio_path)


def save_answer(db: Session, candidate_id: int, question_id: int, audio_bytes: bytes, session: str):
    """Round-3 follow-up #22 (2026-07-19): FAST synchronous half of the old submit_answer() —
    consent gate, write the file, create the interview_answers row. Returns as soon as the video
    is safely on disk; transcription/scoring (the genuinely slow part — STT + 3x self-consistency
    LLM scoring calls, measured at 10-20+ seconds per answer) now happen in process_answer()
    afterward, via a FastAPI BackgroundTask, so the candidate's upload request returns almost
    immediately instead of blocking on all of that.

    Raises ConsentRequiredError if the candidate has no consent record (the caller maps this to
    a 403, per the plan's explicit consent-gate requirement).

    Real bug found 2026-07-21: a candidate whose interview_completed flag was already stale (see
    routers/candidates.py's `interview_completed=len(answers) > 0` — true after the FIRST answer
    ever submitted, not after every APPROVED question is answered) could still POST here again —
    nothing server-side ever rejected a second submission for a question that already had an
    answer, only the frontend's one-time "Wawancara selesai" screen discouraged it, and that guard
    is trivially bypassed by a stale/already-loaded tab, a direct API call, or HR reopening +
    adding more questions after a candidate had already "completed" a shorter version. The result:
    duplicate interview_answers rows for the same question_id, both surfaced in the report as if
    they were separate questions. Deleting the STALE answer here — same question_id, same
    candidate_id — before creating the new one makes resubmission idempotent per question: the
    latest recording always wins, and the superseded one never survives to pollute a report.
    """
    require_consent(db, candidate_id)

    for old in repo.interview_answers.list(db, candidate_id=candidate_id, question_id=question_id):
        _delete_answer(db, old)

    answers_so_far = repo.interview_answers.list(db, candidate_id=candidate_id)
    answer_index = len(answers_so_far) + 1

    audio_path = storage.save_audio(candidate_id, session, answer_index, audio_bytes)

    return repo.interview_answers.create(
        db, candidate_id=candidate_id, question_id=question_id, audio_path=audio_path
    )


def process_answer(db: Session, answer_id: int, candidate_id: int) -> None:
    """The slow half: transcribe -> persist transcript -> score. Runs AFTER the upload response
    has already been sent (see process_answer_background below) — the candidate is never waiting
    on this.

    Interview-summary computation is guarded by checking that EVERY answer has actually finished
    scoring (not just that N answer rows exist) — with answers now processed in the background,
    multiple answers' background tasks can genuinely run concurrently (the frontend uploads
    sequentially, but each upload returns almost instantly, so background processing for answer 1
    can still be running when answer 4's background task starts). Whichever background task
    happens to finish scoring LAST is the one that ends up computing the summary — self-electing,
    no separate coordination needed. compute_and_persist_interview_summary() is idempotent
    (deletes+recreates its row) so even a rare near-simultaneous double-trigger is harmless.
    """
    answer = repo.interview_answers.get(db, answer_id)
    if not answer:
        raise ValueError(f"No interview_answers row for id {answer_id}")

    transcript_text = stt_client.transcribe(answer.audio_path)
    repo.transcripts.create(db, answer_id=answer.id, transcript_text=transcript_text)

    score_and_persist_answer(db, answer.id)

    candidate = repo.candidates.get(db, candidate_id)
    approved_questions = repo.interview_questions.list(db, job_id=candidate.job_id, status="approved")
    all_answers = repo.interview_answers.list(db, candidate_id=candidate_id)
    if len(all_answers) < len(approved_questions):
        return

    all_scored = all(repo.rubric_scores.list(db, answer_id=a.id) for a in all_answers)
    if not all_scored:
        return

    compute_and_persist_interview_summary(db, candidate_id)

    # Round 7 (2026-07-21, user decision): key_strengths/resume_action_items (CV-based) and the new
    # interview_key_strengths/interview_feedback only get (re)computed here, now that the interview
    # is genuinely finished — see skillgap.py::update_recommendation_extras_after_interview()'s
    # docstring for why this replaced computing them at CV-upload/match time.
    update_recommendation_extras_after_interview(db, candidate_id)


def process_answer_background(answer_id: int, candidate_id: int) -> None:
    """Entry point for FastAPI's BackgroundTasks. Owns its own DB session — the request's
    session (from the `Depends(get_db)` that handled the upload) is already closed by the time
    background tasks run (they execute after the response is sent), so it can't be reused here."""
    db = SessionLocal()
    try:
        process_answer(db, answer_id, candidate_id)
    except Exception:
        logger.exception("process_answer_background failed for answer_id=%s candidate_id=%s", answer_id, candidate_id)
    finally:
        db.close()


def notify_interview_finished(db: Session, candidate_id: int) -> None:
    """2026-07-22 (user decision): fires as soon as the candidate's LAST video answer is confirmed
    stored (routers/interview_answers.py::submit_interview_answer) — NOT once the post-interview
    LLM chain finishes. An earlier version of this feature waited for the full chain (including
    the upskilling plan) before notifying, with a blocking "please wait" screen on the candidate
    side; the user reversed that decision because it made candidates wait too long for something
    that doesn't need their attention — the LLM chain now runs fully invisibly in the background,
    and only HR-facing surfaces gate on it (routers/jobs.py's processing_complete,
    routers/report.py's _require_report_ready).

    Guarded by interview_finished_notified_at so re-submitting an already-answered question
    (save_answer's resubmission path) can't send this twice."""
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate or not EMAIL_ENABLED or not candidate.contact_email:
        return
    if candidate.interview_finished_notified_at is not None:
        return

    job = repo.jobs.get(db, candidate.job_id)
    company = repo.companies.get(db, job.company_id) if job else None
    try:
        send_interview_finished_email(
            candidate.alias,
            candidate.contact_email,
            job_title=job.title if job else "",
            company_name=company.name if company else "",
        )
    except Exception:
        logger.exception("notify_interview_finished: send failed for candidate_id=%s", candidate_id)
    else:
        candidate.interview_finished_notified_at = datetime.now(timezone.utc)
        db.commit()


def notify_interview_finished_background(candidate_id: int) -> None:
    """Entry point for FastAPI's BackgroundTasks — same rationale as process_answer_background
    (owns its own DB session since the request's session is already closed by the time background
    tasks run)."""
    db = SessionLocal()
    try:
        notify_interview_finished(db, candidate_id)
    except Exception:
        logger.exception("notify_interview_finished_background failed for candidate_id=%s", candidate_id)
    finally:
        db.close()
