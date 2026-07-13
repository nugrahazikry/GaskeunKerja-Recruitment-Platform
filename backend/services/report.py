"""Deterministic development report assembly (Area 2 T13).

Assembles report content by SELECTING/ORDERING curated items (skill-gap output +
competency_framework + resource_library) — no free-form LLM generation of the report
itself. Gated on an hr_decisions row existing for the candidate.
"""

from sqlalchemy.orm import Session

from db import repositories as repo
from services.skillgap import analyze_skill_gap


def build_report(db: Session, candidate_id: int, job_id: int, bypass_cache: bool = False) -> dict:
    """Requires an hr_decisions row to already exist for this candidate (checked by caller).

    Returns a structured report dict — the deterministic content that gets rendered to PDF
    in T14. Same skill-gap input always produces the same report (QA T4's determinism claim)
    because this function only selects/orders existing data, no LLM call happens here beyond
    the already-grounded analyze_skill_gap() call.

    bypass_cache is exposed for Area 5 QA T4 — same reasoning as elsewhere: a determinism
    test that hits the Area 4 disk cache proves nothing about the underlying LLM call.
    """
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate:
        raise ValueError(f"Candidate {candidate_id} not found")

    profiles = repo.parsed_profiles.list(db, candidate_id=candidate_id)
    candidate_skills = profiles[0].skills if profiles else []

    jd_competencies = repo.jd_competencies.list(db, job_id=job_id)
    required_competency_names = [c.competency_name for c in jd_competencies]

    gap_result = analyze_skill_gap(candidate_skills, required_competency_names, bypass_cache=bypass_cache)

    # For each missing competency, select the matching competency_framework row (by name)
    # and its curated resources — deterministic lookup, not generation.
    all_framework_rows = repo.competency_framework.list(db)
    name_to_framework = {row.competency_name.strip().lower(): row for row in all_framework_rows}

    development_plan = []
    for missing_name in gap_result["missing_competencies"]:
        framework_row = name_to_framework.get(missing_name.strip().lower())
        if not framework_row:
            continue  # no curated content exists for this competency — skip, don't invent

        resources = repo.resource_library.list(db, competency_id=framework_row.id)
        development_plan.append(
            {
                "competency_name": framework_row.competency_name,
                "level_description": framework_row.level_description,
                "resources": [
                    {"title": r.title, "duration": r.duration, "milestone": r.milestone_description, "url": r.url}
                    for r in resources
                ],
            }
        )

    interview_summaries = repo.interview_summaries.list(db, candidate_id=candidate_id)
    interview_score = interview_summaries[0].overall_score if interview_summaries else None

    return {
        "candidate_alias": candidate.alias,
        "gap_summary": gap_result["gap_summary"],
        "development_priority": gap_result["development_priority"],
        "development_plan": development_plan,
        "interview_overall_score": interview_score,
    }
