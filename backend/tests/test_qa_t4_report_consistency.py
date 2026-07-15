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

Cost guardrail: each call to build_report() now makes 3 real Deepseek Pro calls
internally (self-consistency voting inside analyze_skill_gap), so this test's N outer
runs cost 3xN real API calls. Kept to 3 outer runs (9 total calls) rather than 5 (15
calls) to bound cost/time — also added a 60s client-level timeout to llm_client.py after
this test hung for 35+ minutes on a stalled network call with no timeout configured.
"""

from db import repositories as repo
from db.session import SessionLocal
from services.report import build_report
from seed.load_t5_fixture import FIXTURE_JOB_TITLE

_OUTER_RUNS = 3
_MAX_TOLERATED_MISSING_COMPETENCY_DRIFT = 1  # entries — safety margin, not an expected outcome


def test_report_data_consistent_after_self_consistency_fix():
    db = SessionLocal()
    try:
        jobs = repo.jobs.list(db, title=FIXTURE_JOB_TITLE)
        assert jobs, f"Fixture JD '{FIXTURE_JOB_TITLE}' not found — run seed.load_t5_fixture first"
        job = jobs[0]

        candidates = repo.candidates.list(db, job_id=job.id, alias="FIXTURE-WEAK-1")
        assert candidates, "FIXTURE-WEAK-1 not found — run seed.load_t5_fixture first"
        candidate = candidates[0]

        existing_decisions = repo.hr_decisions.list(db, candidate_id=candidate.id)
        if not existing_decisions:
            hr_users = repo.hr_users.list(db, company_id=job.company_id)
            assert hr_users, "no HR user found for the fixture company"
            repo.hr_decisions.create(
                db, candidate_id=candidate.id, decision="reject", decided_by=hr_users[0].id,
                notes="Area 5 QA T4 fixture decision",
            )

        results = [
            build_report(db, candidate.id, job.id, bypass_cache=True) for _ in range(_OUTER_RUNS)
        ]

        first = results[0]
        for i, result in enumerate(results[1:], start=2):
            first_missing = {item["competency_name"] for item in first["development_plan"]}
            this_missing = {item["competency_name"] for item in result["development_plan"]}
            drift = len(first_missing.symmetric_difference(this_missing))
            assert drift <= _MAX_TOLERATED_MISSING_COMPETENCY_DRIFT, (
                f"run {i} development_plan competency set differs from run 1 by {drift} "
                f"entries (tolerance {_MAX_TOLERATED_MISSING_COMPETENCY_DRIFT}): "
                f"{this_missing} vs {first_missing}"
            )
    finally:
        db.close()
