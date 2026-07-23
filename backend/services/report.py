"""Development report assembly (Area 2 T13).

Round 8 (2026-07-21, user decision): the "Estimasi Waktu Upskilling" section used to be built here
by deterministically joining `missing_competencies` against a hand-curated `competency_framework` +
`resource_library` table (~10 competencies total, one demo role) — anything outside that fixed list
silently produced nothing. Replaced with `skill_gap_results.upskilling_plan`, a fully LLM-generated
plan (see services/skillgap.py::generate_upskilling_plan()) computed once, after the candidate's
interview completes (services/skillgap.py::update_recommendation_extras_after_interview()), and read
here exactly like key_strengths/resume_action_items already were — still no live LLM call in this
function itself, just reads what's already persisted.
"""

from sqlalchemy.orm import Session

from db import repositories as repo
from services.skillgap import combine_skills, get_or_compute_skill_gap


def build_interview_answers(db: Session, candidate_id: int) -> list[dict]:
    """Per-question interview breakdown (question text, transcript, AI summary, rubric scores),
    sorted chronologically — single source of truth shared by the JSON report endpoint (which adds
    a video_url on top, routers/report.py::_build_interview_answers) and the PDF (services.report_pdf
    — no video, since a static PDF can't embed one)."""
    answers = repo.interview_answers.list(db, candidate_id=candidate_id)
    result = []
    for answer in sorted(answers, key=lambda a: a.submitted_at):
        question = repo.interview_questions.get(db, answer.question_id)
        transcripts = repo.transcripts.list(db, answer_id=answer.id)
        rubric_rows = repo.rubric_scores.list(db, answer_id=answer.id)
        result.append(
            {
                "answer_id": answer.id,
                "question_text": question.question_text if question else "?",
                "summary_text": transcripts[0].summary_text if transcripts else None,
                "transcript_text": transcripts[0].transcript_text if transcripts else None,
                "rubric_scores": [
                    {"criterion_name": r.criterion_name, "score": r.score, "rationale": r.rationale}
                    for r in rubric_rows
                ],
            }
        )
    return result


def build_report(db: Session, candidate_id: int, job_id: int) -> dict:
    """Requires the candidate's interview + post-interview LLM chain to be fully done (checked by
    the caller, routers/report.py::_require_report_ready) — an HR decision is NOT required to view
    a report, only to email one (routers/report.py::send_candidate_report still gates on that).

    Returns a structured report dict — the deterministic content that gets rendered to PDF
    in T14. Same skill-gap input always produces the same report (QA T4's determinism claim)
    because this function only selects/orders existing data.

    Round-2 polish (2026-07-17): reads the persisted skill_gap_results row (computed once,
    alongside the match score) instead of calling analyze_skill_gap() live on every report
    view/generation — the user explicitly asked for the report to be free of any live AI calls
    after the candidate's initial CV upload.
    """
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate:
        raise ValueError(f"Candidate {candidate_id} not found")

    job = repo.jobs.get(db, job_id)

    profiles = repo.parsed_profiles.list(db, candidate_id=candidate_id)
    profile = profiles[0] if profiles else None
    candidate_skills = profile.skills if profile else []
    candidate_experience = profile.experience if profile else []

    jd_competencies = repo.jd_competencies.list(db, job_id=job_id, status="active")
    required_competency_names = [c.competency_name for c in jd_competencies]

    gap_result = get_or_compute_skill_gap(
        db,
        candidate_id,
        job_id,
        combine_skills(candidate_skills, profile.skills_implicit if profile else None),
        required_competency_names,
        candidate_experience=candidate_experience,
    )

    interview_summaries = repo.interview_summaries.list(db, candidate_id=candidate_id)
    interview_score = interview_summaries[0].overall_score if interview_summaries else None

    return {
        "candidate_alias": candidate.alias,
        "job_title": job.title if job else "?",
        "gap_summary": gap_result["gap_summary"],
        "development_priority": gap_result["development_priority"],
        "matched_competencies": gap_result["matched_competencies"],
        "missing_competencies": gap_result["missing_competencies"],
        # Round-3 follow-up #4 (2026-07-19): key_strengths now comes from the LLM-grounded,
        # experience-evidenced narrative persisted alongside the rest of skill-gap analysis
        # (services/skillgap.py::generate_recommendation_extras) — replaces the old deterministic
        # "matched competency name + curated framework description" version, which was thinner
        # and identical across every candidate matching the same competency.
        "key_strengths": gap_result["key_strengths"],
        "resume_action_items": gap_result["resume_action_items"],
        # Round 7 (2026-07-21): interview-performance counterparts — empty until the candidate's
        # interview is complete (see skillgap.py::update_recommendation_extras_after_interview).
        "interview_key_strengths": gap_result["interview_key_strengths"],
        "interview_feedback": gap_result["interview_feedback"],
        "upskilling_plan": gap_result["upskilling_plan"],
        "interview_overall_score": interview_score,
        "cv_summary": profile.cv_summary if profile else None,
        "skills": candidate_skills,
        "skills_implicit": (profile.skills_implicit or []) if profile else [],
        "experience": candidate_experience,
        "qualifications": profile.qualifications if profile else [],
        "education_level": profile.education_level if profile else None,
        "major": profile.major if profile else None,
        "education_history": (profile.education_history or []) if profile else [],
        "certifications": (profile.certifications or []) if profile else [],
        "featured_projects": (profile.featured_projects or []) if profile else [],
        "organization_experience": (profile.organization_experience or []) if profile else [],
    }
