from sqlalchemy.orm import Session

from db import repositories as repo
from services.rubric import score_answer


def score_and_persist_answer(db: Session, answer_id: int) -> dict:
    """Scores one interview_answers row and persists rubric_scores (one row per criterion)."""
    answer = repo.interview_answers.get(db, answer_id)
    if not answer:
        raise ValueError(f"No interview_answers row for id {answer_id}")

    transcripts = repo.transcripts.list(db, answer_id=answer_id)
    if not transcripts:
        raise ValueError(f"No transcript for answer {answer_id} — run STT first (T10)")
    transcript = transcripts[0]
    transcript_text = transcript.transcript_text

    question = repo.interview_questions.get(db, answer.question_id)
    question_text = question.question_text if question else ""

    result = score_answer(question_text, transcript_text)

    # Round-3 Task 21: persist the per-answer summary next to the raw transcript — previously
    # only ever returned to the caller and dropped, which meant only the LAST answer scored in
    # a session ever had its summary available (see submit_answer()'s prior caller-collected
    # per_answer_summaries, now fixed to read this column instead).
    transcript.summary_text = result["summary"]
    db.commit()

    existing = repo.rubric_scores.list(db, answer_id=answer_id)
    for row in existing:
        db.delete(row)
    db.commit()

    for criterion_key in ("clarity", "relevance", "technical_depth"):
        repo.rubric_scores.create(
            db,
            answer_id=answer_id,
            criterion_name=criterion_key,
            score=result[criterion_key],
            rationale=result[f"{criterion_key}_rationale"],
        )

    return result


def compute_and_persist_interview_summary(db: Session, candidate_id: int) -> dict:
    """Aggregates all of a candidate's scored answers into one interview_summaries row.

    Round-3 Task 21: reads each answer's persisted transcripts.summary_text (now written by
    score_and_persist_answer above) rather than relying on the caller to collect summaries —
    fixes a real gap where only the LAST answer scored in a session had its summary available
    (transcripts.summary_text didn't exist yet, so nothing else could be read back later).
    """
    answers = repo.interview_answers.list(db, candidate_id=candidate_id)
    if not answers:
        raise ValueError(f"No interview_answers for candidate {candidate_id}")

    all_scores: list[int] = []
    per_answer_summaries: list[str] = []
    for answer in answers:
        scores = repo.rubric_scores.list(db, answer_id=answer.id)
        all_scores.extend(s.score for s in scores)
        transcripts = repo.transcripts.list(db, answer_id=answer.id)
        if transcripts and transcripts[0].summary_text:
            per_answer_summaries.append(transcripts[0].summary_text)

    overall_score = sum(all_scores) / len(all_scores) if all_scores else 0.0

    combined_summary = " ".join(per_answer_summaries) or (
        "Ringkasan wawancara berdasarkan seluruh jawaban kandidat."
    )

    existing = repo.interview_summaries.list(db, candidate_id=candidate_id)
    for row in existing:
        db.delete(row)
    db.commit()

    summary_row = repo.interview_summaries.create(
        db, candidate_id=candidate_id, ai_summary_text=combined_summary, overall_score=overall_score
    )
    return {"overall_score": overall_score, "ai_summary_text": summary_row.ai_summary_text}
