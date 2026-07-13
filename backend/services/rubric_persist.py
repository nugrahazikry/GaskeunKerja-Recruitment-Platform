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
    transcript_text = transcripts[0].transcript_text

    question = repo.interview_questions.get(db, answer.question_id)
    question_text = question.question_text if question else ""

    result = score_answer(question_text, transcript_text)

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


def compute_and_persist_interview_summary(db: Session, candidate_id: int, per_answer_summaries: list[str]) -> dict:
    """Aggregates all of a candidate's scored answers into one interview_summaries row.

    per_answer_summaries: the "summary" field score_and_persist_answer() returned for each
    of this candidate's answers, in order — collected by the caller (no dedicated DB column
    exists for per-answer summaries, so this avoids a schema change for something transient).
    """
    answers = repo.interview_answers.list(db, candidate_id=candidate_id)
    if not answers:
        raise ValueError(f"No interview_answers for candidate {candidate_id}")

    all_scores: list[int] = []
    for answer in answers:
        scores = repo.rubric_scores.list(db, answer_id=answer.id)
        all_scores.extend(s.score for s in scores)

    overall_score = sum(all_scores) / len(all_scores) if all_scores else 0.0

    combined_summary = " ".join(s for s in per_answer_summaries if s) or (
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
