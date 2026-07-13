# Area 5 — QA Process

> **Resolved 2026-07-12 (solo/1-week):** QA collapses to the highest-stakes claim tests + one e2e + a demo-readiness checklist. Broad unit/integration coverage and the full security matrix are deferred to spot-checks.
>
> **⚠️ Rewritten 2026-07-12 (Area-5 session):** the original version predated most of the Area 1-4 gap-closing passes and referenced a flow that no longer exists (e.g. "report email" — dropped for Telegram). This version matches the actual current product, and closes 4 real gaps found on review. Live task status + steps: `execution-checklist.md` → Area 5.

**Goal:** verify the local MVP works end-to-end and that the specific claims made in the Tahap 3 submission (`../../brainstorming idea/proposal sekarang/tahap 3 jawaban.md`) are actually true — especially determinism, transparency, PII handling, and human-in-the-loop.
**Runs:** alongside each area (unit-level) and after integration (end-to-end + usability). Culminates in demo readiness.

## Gaps found and resolved

| Gap | Decision |
|---|---|
| PII redaction had zero test coverage despite being a load-bearing UU PDP claim | **Promoted to a required claim test (new T3b)** |
| Area 2 T10 already cites "the consent gate Area 5 QA T8 tests" — but T8 was deferred/smoke-only | **Promoted to a required automated test** |
| Frontend demo-safety states (mic-denied, empty-submit, completion-guard, expired-token, invite re-view, missing-Telegram) were never verified before recording | **T12 now explicitly walks through all of them** |
| Matching formula / curated strong-mid-weak tiers were only "light manual check" | **Promoted to an asserted check (T5)** |
| All claim tests scheduled for Day 6 despite depending on Day 2-4 work — a real bug found Day 6 leaves no runway | **Shifted left: each test runs as soon as its dependency lands (Day 2-5); Day 6 is a re-run/confirmation pass** |
| T5's test had no ground truth to assert against (seed script didn't record intended tiers) | **Area 3 T10's seed manifest now tags each candidate's intended match-quality tier** |
| Telegram delivery only checked for "the API call didn't error," not "the message actually arrived" | **T12 rehearsal now includes checking the real Telegram chat** |
| "5 repeated runs" would trivially pass via the Area 4 response cache without re-querying the LLM | **T3/T4 now bypass the cache** for their own runs (new `bypass_cache` param on the LLM client, Area 4 T3) |
| T3b's fixture (a curated seed CV) created a same-day dependency on Area 3's full curation finishing | **T3b uses its own dedicated minimal test fixture**, decoupled from curation |
| T5's strict per-candidate ordering risked false failures on real, messy CV data | **Changed to an aggregate/average tier comparison** |
| Shifting tests left only helps if a failure blocks progress | **New rule: a failing claim test must be fixed the same day, before starting the next day's tasks** |
| T3b didn't say whether it hits the real SumoPod API or mocks it | **Mock the outgoing request** — no live call, zero cost |
| T4's "identical report" comparison could false-fail on non-deterministic PDF metadata if it diffed rendered bytes | **Compare underlying report data, before PDF rendering — not the PDF bytes** |
| T3/T4's cache-bypassed tests have a real recurring cost with no guardrail against careless repeat runs | **Explicit note: run once per feature, not in a tight edit-test loop** |

**Failure gate:** if any claim test (T3, T3b, T4, T5, T6, T8) fails on the day it's run, fix it before starting the next day's build tasks — the entire point of shifting them left.

**Cost guardrail:** T3 and T4 each make 5 genuinely independent, cache-bypassed Deepseek calls per run. Run them once when the feature is believed complete — not repeatedly inside a debug loop. This is exactly the repeated-spend pattern Area 4's caching strategy exists to avoid.

## Task List

### Claim-verification tests (tie directly to submission claims — run incrementally, not bunched at the end)
- [ ] T3. **Determinism test (critical) — run Day 4, right after rubric scoring is built:** same transcript → same rubric score across **5 repeated runs, cache bypassed** (validates the temperature=0 / rubric claim in Q17 — bypassing the cache is required or the test just replays a cached response and proves nothing). If it fails, the transparency claim is false — fix before moving on. Run once per feature, not in a debug loop.
- [ ] T3b. **PII redaction test (NEW) — run Day 2, right after CV parsing is built:** feed a CV with a real name/email/phone through the parse pipeline, using **one dedicated standalone test fixture PDF** (not a curated seed CV — decouples this from Area 3's curation timeline); **mock the outgoing SumoPod request** (patch the LLM client, no live API call) and assert the captured payload never contains the raw name/email/phone, and that the structured `parsed_profiles` row contains only the alias. Proves the UU PDP claim rather than just asserting it — at zero cost.
- [ ] T4. **Report consistency test — run Day 5, right after report generation is built:** same skill-gap input → same development report **data** (compared before PDF rendering, not the rendered bytes — weasyprint can embed non-deterministic metadata like creation timestamps) across **5 repeated runs, cache bypassed** (validates the "deterministic learning plan" fix). Run once per feature, not in a debug loop.
- [ ] T5. **Matching formula / curated-tier check (promoted) — run Day 3, right after matching is built:** read the intended tier per candidate from the seed manifest (Area 3 T10); assert the curated strong-tier **average** score is meaningfully higher than the weak-tier **average** (aggregate, not strict per-candidate ordering — tolerates natural noise in real curated CVs) — catches a formula bug or bad curation before it's on camera.
- [ ] T6. **Human-in-the-loop test — run Day 4, right after decision endpoints exist:** confirm the system never auto-rejects — no code path finalizes a candidate without HR action (validates "assist, never decide").
- [ ] T8. **Consent-gate enforcement test (promoted) — run Day 4, right after answer intake exists:** submitting an interview answer with no `consent_records` row → 403; with a valid one → success. This is the exact test Area 2 T10 already assumes exists.

### End-to-end, usability, demo (Day 6 — re-runs the above as confirmation, doesn't run them for the first time)
- [ ] T10. **Full end-to-end run — rewritten to match the current flow**: seed loads (1 company, 1 JD, 30 tiered candidates, all with `parsed_profiles`) → HR creates/views JD → Shortlist (instant, tier pills) → HR approves questions → **invites the live candidate** → candidate consents + **links Telegram** → records/submits each audio answer → HR reviews (audio+transcript+summary+rubric) → decides → **sends report via Telegram**. No manual DB fiddling; no email anywhere.
- [ ] T11. Internal usability walkthrough with the seed data (1 JD, 30 candidates) — capture friction, iterate.
- [ ] T12. **Demo-readiness checklist — now includes the edge-state walkthrough + real Telegram check (promoted)**: happy-path script rehearsed; every frontend safety state seen at least once before recording (mic-denied, empty-submit block, completion-guard, expired/invalid token, invite re-view, missing-Telegram disabled state, synthetic-candidate "Terkirim" state); **and the Telegram chat itself checked** to confirm the live candidate's report (PDF + summary) actually arrived, not just that the send call returned success.

### Deferred (spot-check / trust-the-design only)
- [ ] `[deferred]` Broad backend unit tests per stage — only claim-critical stages tested.
- [ ] `[deferred]` Access-control matrix — thin auth smoke check only (Area2 T3); consent-gate (T8) is the one promoted exception.
- [ ] `[deferred]` Audit-log completeness — spot check only.
- [ ] `[deferred]` Vision-LLM fallback dedicated test — covered once via Area 4 T3d's Day-1 verification, not re-tested here.
- [ ] `[deferred]` JD soft-delete integrity test — trust the `status='closed'` design (Area 2 T4).

## Decisions — RESOLVED
- Test framework → **pytest** for the claim-tests; frontend e2e is a manual demo walkthrough (no Playwright in the solo week).
- ~~Automated vs manual~~ → **automate T3/T3b/T4/T5/T6/T8** (highest stakes, judge-pokeable or already promised by another area); everything else manual spot-check.
- Usability walkthrough → **solo plays both HR + candidate** on seed data (no real client yet).

## Note
T3, T3b, T4, T6, T8 verify the exact things the submission *claims* are true (determinism, transparency, PII handling, human-in-the-loop, consent). T5 protects the demo narrative itself (the curated ranking has to actually look right). A judge or pilot client could poke any of T3/T3b/T6/T8 directly — prioritize them over broad coverage.
