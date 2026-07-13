from sqlalchemy.orm import Session

from db import repositories as repo
from services import storage, stt_client
from services.consent import ConsentRequiredError, require_consent


def submit_answer(db: Session, candidate_id: int, question_id: int, audio_bytes: bytes, session: str) -> dict:
    """Full T10 flow: consent gate -> store audio -> transcribe -> persist transcript.

    Raises ConsentRequiredError if the candidate has no consent record (the caller maps
    this to a 403, per the plan's explicit consent-gate requirement).
    """
    require_consent(db, candidate_id)  # raises ConsentRequiredError if no consent row

    answers_so_far = repo.interview_answers.list(db, candidate_id=candidate_id)
    answer_index = len(answers_so_far) + 1

    audio_path = storage.save_audio(candidate_id, session, answer_index, audio_bytes)

    answer = repo.interview_answers.create(
        db, candidate_id=candidate_id, question_id=question_id, audio_path=audio_path
    )

    transcript_text = stt_client.transcribe(audio_path)
    repo.transcripts.create(db, answer_id=answer.id, transcript_text=transcript_text)

    return {"answer_id": answer.id, "audio_path": audio_path, "transcript_text": transcript_text}
