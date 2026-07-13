# Kickoff Prompt — Implementation Planning Session

Open a new Claude Code session with the working directory set to the `implementation/` folder, then paste the prompt below.

---

## Prompt to paste

```
We are starting the implementation-planning brainstorming session for DIGDAYA 2026
Tahap 3, team P0804 — the "GaskeunKerja for Business" (Direction B, company-focused)
MVP. The direction is already decided; this session is about planning HOW to build it.

Before anything, read these files for full context:
- CLAUDE.md (session context + the hard "local MVP, no cloud" constraint)
- planning/plan.md (master plan: local stack, critical path, milestones, open decisions)
- planning/area-1-frontend.md, planning/area-2-backend-ai.md, planning/area-3-database.md,
  planning/area-4-cost-tooling.md, planning/area-5-qa.md (first-draft task lists per area)

Also read the master reference from the previous phase:
- ../brainstorming idea/proposal sekarang/direction B summary.md
And, for what we're claiming we'll build:
- ../brainstorming idea/proposal sekarang/tahap 3 jawaban.md

Key constraint: this MVP is LOCAL ONLY, NO CLOUD. Cloud services are replaced by local
substitutes (BigQuery->Postgres/SQLite, GCS->filesystem, Cloud Run->local uvicorn,
Google STT->local Whisper, Qdrant local Docker). Deepseek LLM API is the one likely
external cost. Deadline ~2026-07-26 (about 2 weeks). Existing team, reusing Tahap 2 code
(github.com/nugrahazikry/AI-Powered-Skill-Gap-Analysis).

What I want from this session:
1. Turn the first-draft task lists in the 5 area files into a detailed, sequenced
   execution plan — per task: what it is, what it depends on, rough effort, who/what's
   needed, and how it maps to the end-to-end flow.
2. Resolve the open decisions first, because they swing the 2-week scope the most:
   - KGE relational matching vs semantic-vector-similarity-first
   - audio vs text-only AI interview answers
   - PostgreSQL (Docker) vs SQLite
   - whether any LLM step can use a free local model to cut Deepseek cost
   - scope/ownership of the two reference datasets (competency framework + resource
     library) — remember these are CONTENT curation, not code, and they're on the
     critical path.
3. Identify the true critical path and a realistic day-by-day-ish milestone breakdown.

Work as a balanced sparring partner: propose task breakdowns AND pressure-test feasibility
against the 2-week window and the local/free constraint. Flag when a task is bigger than it
looks or when a submission claim risks not being buildable in time. Keep conclusions written
into planning/plan.md (and the area files), not just in chat.

Please go into plan mode. Start by reading the files above, then help me resolve the open
decisions and build the detailed execution plan. Ask me anything you need clarified before
finalizing the plan.
```

---

## Notes
- The project memory (persisted across sessions) already records that Direction B is locked and the MVP is local-only, so the new session will have that baseline even before reading these files.
- If you want the session to focus on just ONE area first (e.g. backend+AI), add a line like: "For this session, focus only on Area 2 (backend & AI) — we'll do the others separately."
