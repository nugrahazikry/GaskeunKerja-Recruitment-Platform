"""Area 5 QA T4: report consistency test.

Same skill-gap input -> same development report DATA (not rendered PDF bytes) across
genuinely independent (cache-bypassed) runs. Diffing raw PDF bytes would risk a false
failure from non-deterministic metadata (creation timestamp, producer string) that
ReportLab can embed even when visible content is identical — so this compares
services.report.build_report()'s structured dict, before report_pdf.py renders it.

⚠️ REAL FINDING (2026-07-13, measured directly, same root cause as T3's finding): the
ORIGINAL single-call analyze_skill_gap() showed BOTH `development_priority` AND the
`development_plan`'s actual competency-name SET varying across independent runs — e.g.
one run's plan included "Responsive & Mobile-First Design" and another run's didn't, not
just a different priority pick among a stable set. Consistent with provider-level
temperature=0 non-determinism (same as T3), not a bug in report assembly itself.

✅ FIX SHIPPED 2026-07-13 (user-chosen: extend the same self-consistency voting fix from
T3 to skill-gap analysis): `analyze_skill_gap()` now calls the LLM 3x internally and takes
a MAJORITY VOTE per competency + the most-common development_priority, rather than
trusting a single call — see services/skillgap.py. This test now re-measures against the
FIXED function and tightens the tolerance accordingly.

Uses one of the T5-fixture candidates (weak-tier, guaranteed to have a real skill gap
against the fixture JD) rather than a real demo-pool candidate. Creates an hr_decisions
row for it if one doesn't already exist yet (build_report requires one).

⚠️ UPDATED 2026-07-17 (Round-2 polish): build_report() no longer calls the LLM at all — it now
reads a persisted skill_gap_results row (computed once, at match time, via
services.matching.persist_skill_gap()) instead of calling analyze_skill_gap() live on every
call. That was the whole point of the change (the user explicitly asked for reports to be free
of live AI calls after initial CV upload), but it means build_report(..., bypass_cache=True) no
longer exists — calling it twice now trivially returns the same DB row every time, which proves
nothing about the underlying LLM's determinism. This test is split in two: (1) the original
self-consistency-voting claim is now tested directly against analyze_skill_gap() (still takes
bypass_cache, still does the real 3-vote internal call), which is the actual place that
determinism risk lives; (2) a new, cheap assertion that build_report() itself is now
byte-consistent across repeated calls with ZERO additional LLM calls (the new architecture's
actual contract).

Cost guardrail: each call to analyze_skill_gap() makes 3 real Deepseek Pro calls internally
(self-consistency voting), so this test's N outer runs cost 3xN real API calls. Kept to 3 outer
runs (9 total calls) rather than 5 (15 calls) to bound cost/time — also added a 60s client-level
timeout to llm_client.py after this test hung for 35+ minutes on a stalled network call with no
timeout configured.
"""

from db import repositories as repo
from db.session import SessionLocal
from services.report import build_report
from services.skillgap import analyze_skill_gap
from seed.load_t5_fixture import FIXTURE_JOB_TITLE

_OUTER_RUNS = 3
_MAX_TOLERATED_MISSING_COMPETENCY_DRIFT = 1  # entries — safety margin, not an expected outcome


def _get_fixture_candidate_and_job(db):
    jobs = repo.jobs.list(db, title=FIXTURE_JOB_TITLE)
    assert jobs, f"Fixture JD '{FIXTURE_JOB_TITLE}' not found — run seed.load_t5_fixture first"
    job = jobs[0]

    candidates = repo.candidates.list(db, job_id=job.id, alias="FIXTURE-WEAK-1")
    assert candidates, "FIXTURE-WEAK-1 not found — run seed.load_t5_fixture first"
    candidate = candidates[0]
    return candidate, job


def test_analyze_skill_gap_consistent_after_self_consistency_fix():
    """The original T4 claim, now tested at its real source: analyze_skill_gap()'s internal
    3-vote self-consistency, called directly (bypass_cache=True forces genuinely independent
    LLM calls each outer run, not a cache replay)."""
    db = SessionLocal()
    try:
        candidate, job = _get_fixture_candidate_and_job(db)
        profiles = repo.parsed_profiles.list(db, candidate_id=candidate.id)
        assert profiles, "fixture candidate has no parsed profile"
        candidate_skills = profiles[0].skills

        jd_competencies = repo.jd_competencies.list(db, job_id=job.id)
        required = [c.competency_name for c in jd_competencies]

        results = [
            analyze_skill_gap(candidate_skills, required, bypass_cache=True) for _ in range(_OUTER_RUNS)
        ]

        first_missing = set(results[0]["missing_competencies"])
        for i, result in enumerate(results[1:], start=2):
            this_missing = set(result["missing_competencies"])
            drift = len(first_missing.symmetric_difference(this_missing))
            assert drift <= _MAX_TOLERATED_MISSING_COMPETENCY_DRIFT, (
                f"run {i} missing_competencies set differs from run 1 by {drift} entries "
                f"(tolerance {_MAX_TOLERATED_MISSING_COMPETENCY_DRIFT}): {this_missing} vs {first_missing}"
            )
    finally:
        db.close()


def test_build_report_reads_persisted_row_consistently():
    """New contract (Round-2 polish): build_report() reads a persisted skill_gap_results row —
    repeated calls must return byte-identical development_plan data with no LLM variance,
    since no LLM call happens in build_report() itself anymore."""
    db = SessionLocal()
    try:
        candidate, job = _get_fixture_candidate_and_job(db)

        existing_decisions = repo.hr_decisions.list(db, candidate_id=candidate.id)
        if not existing_decisions:
            hr_users = repo.hr_users.list(db, company_id=job.company_id)
            assert hr_users, "no HR user found for the fixture company"
            repo.hr_decisions.create(
                db, candidate_id=candidate.id, decision="reject", decided_by=hr_users[0].id,
                notes="Area 5 QA T4 fixture decision",
            )

        first = build_report(db, candidate.id, job.id)
        second = build_report(db, candidate.id, job.id)
        assert first == second, "build_report() should be byte-identical across calls — it only reads a stored row"
    finally:
        db.close()
