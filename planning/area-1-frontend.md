# Area 1 — Frontend UI/UX

> **Resolved 2026-07-12 (solo/1-week):** build **money-shot screens only** — recruiter question edit/approve, HR shortlist w/ explainability, candidate **audio interview**, HR decision (with audio player + transcript + summary), report view. Everything else driven by seed data. **Audio interview is CORE** (MediaRecorder voice recording — revised from the earlier text-only call). Design system minimal / reuse Tahap 2.
>
> **Resolved 2026-07-12 (Area-3 session):** JD posting (T6 below) is now a **full CRUD screen** — list + guided create/edit + delete, scoped to HR's company — not a single one-shot form.
>
> **Resolved 2026-07-12 (Area-3 second pass):** **No self-service CV upload** for MVP — candidates are HR/seed-imported, so the candidate token page is **consent + interview only** (T8/T13 below drop the CV-upload step). Of the 30 seed candidates, only **1 live candidate** actually walks the full token-page flow during demo recording; the rest never touch the frontend at all.
>
> **Resolved 2026-07-12 (Area-1 session):** **⚠️ Correction — Tahap 2 has NO React frontend** (verified by reading the actual code: a static `index.html`/`style.css`/`script.js` site, nginx, no build tooling, branded "SkillGap AI"). **The frontend is built fresh in React + Vite**, reusing only the old visual language (colors/layout), not any code. Published a 4-way HTML design-comparison artifact (old recreation vs. 3 new directions) for the HR Shortlist screen. **Three gaps closed**: new **invite modal (T5c in checklist)**, Shortlist now shows **per-candidate tier status**, and **report delivery moved to the HR candidate-detail screen** (was wrongly on the candidate's own consent page).
>
> **Resolved 2026-07-12 (design locked):** **"Enterprise Trust" confirmed** as the final visual direction — teal `#0f6b5c` + gold `#c98a2c`, Georgia serif headings, teal-tinted paper, top-nav dossier layout. Two separate artifacts (kept apart per user request, each linking to the other): the full **8-page preview** at `https://claude.ai/code/artifact/c3799402-5780-4573-a7e7-801149ffb90a`, and the original **4-way comparison** (decision record) at `https://claude.ai/code/artifact/c0a5be48-4a7e-46fd-a68e-8ea757b48b0e`. Live task status + steps: `execution-checklist.md` → Area 1.

**Goal:** local React app covering the demo happy-path for two personas (HR + Candidate), wired to the local backend.
**Stack:** React + Vite, built fresh. No cloud hosting — runs on local dev server.
**Depends on:** backend API contract (Area 2). Can start on design system + static screens before the API is ready.

## Screens Required (from the end-to-end flow)

**HR side (login required):** login → JD list/CRUD → ranked candidate shortlist w/ tier status → invite modal → approve interview questions → candidate detail (CV, skill-gap, audio+transcript+summary, interview score, decision, **send report**).
**Candidate side (NO login — token link):** open link → consent (PDP) + link Telegram (required) → AI **audio** interview (2-3 questions) → completion.
**Conventions:** Bahasa Indonesia everywhere. Candidate has no account; results delivered automatically via Telegram only (`sendDocument`/`sendMessage`) once HR triggers it from the candidate-detail screen — no email.
**Shared:** minimal design system, async/loading states, error states, responsive layout.

## Task List (first draft — see `execution-checklist.md` for the numbered/current version)

### Foundation
- [ ] T1. Audit Tahap 2 frontend — **corrected: no code to reuse**, visual-language only (colors, layout ideas).
- [ ] T2. Define design system: palette, typography, component library (buttons, cards, tables, score badges, status pills, forms), built in React. Pick the direction from the design-comparison artifact.
- [ ] T3. Set up Vite project structure: routing, state management, API client layer.
- [ ] T4. Auth screens: HR login only; candidate has no account.

### HR persona
- [ ] T4b. JD **full CRUD**: list view + guided create/edit form (structured fields) + soft-delete action, scoped to HR's company.
- [ ] T5. Candidate shortlist view: ranked list with match score + **explainability** (Q17) + **per-candidate tier status pill** (Belum diundang / Menunggu wawancara / Selesai wawancara).
- [ ] T5c. **Invite modal** — opened from a Shortlist row, generates + shows the copyable token link (Area 2 T9c).
- [ ] T5b. Recruiter question edit/approve screen.
- [ ] T7. Candidate detail view: parsed CV, skill-gap breakdown, audio player + transcript + AI summary + rubric score, decision controls (AI only *recommends*), **and report delivery** ("Kirim Laporan" once a decision exists).

### Candidate persona
- [ ] T6-landing. Invite landing page (accessed via link/token). Reached only by the **1 live demo candidate** — the other 29 seed candidates never touch this screen.
- [ ] T8. Consent screen with explicit PDP checkbox + Telegram-linking button — gates the interview; must be recorded. **No CV upload, no report-sending here** (moved to T7).
- [ ] `[cut for MVP]` CV upload component — no self-service upload; all candidates (including the live one) are HR/seed-imported.
- [ ] T6. AI Interview UI: display approved question, capture answer via **audio recording (MediaRecorder API)** with playback/re-record. Include timer + submit, loops 2-3x.
- [ ] T6-done. Completion/confirmation screen (report will arrive via Telegram, not email).

### Integration & polish
- [ ] T15. Wire all screens to backend endpoints; handle async AI latency with loading states; error handling; responsive pass; usability polish.

## Decisions — RESOLVED
- ~~UI kit / reuse Tahap 2~~ → **Tahap 2 has no React code** (static site only) — build fresh in React + Vite, visual-language reuse only.
- ~~Audio vs text-only (T6)~~ → **audio voice recording** (MediaRecorder); text-only reversed.
- ~~Candidate report view vs email-only~~ → **report shown + downloadable in UI, sent via Telegram from T7** (email dropped entirely).
- ~~UI polish level~~ → **demo-happy-path polish only**; the money-shot screens must look clean on camera, the rest functional.
- ~~Invite UI~~ → modal on Shortlist (T5c), not a separate page.
- ~~Tier visibility~~ → Shortlist shows status per candidate, derived from row presence not a stored field.
- ~~Report-delivery placement~~ → HR candidate-detail screen (T7), not the candidate's consent page (T8).
- ~~Interview re-entry~~ → T6 checks for existing `interview_answers`; shows a completed screen instead of the recorder if the candidate reopens the link after submitting.
- ~~Synthetic candidates' decision state~~ → seed script also writes `hr_decisions` for the 2-3 synthetic candidates; T7's send-report button shows disabled "Terkirim" for them / disabled "belum menautkan Telegram" for anyone with no `chat_id`.
- ~~Invite link loss~~ → T5c's modal is re-viewable (button relabels once a token exists) instead of one-shot.
- ~~Audio timer~~ → **count-up soft limit** (guidance only, no auto-stop). ~~Audio upload~~ → **per-question** (background STT, isolated retries). ~~Matching trigger~~ → **pre-computed** (Shortlist instant, no button). ~~Demo browser~~ → **Chrome/Edge**, test recorder Day 1.
- ~~Loading/error/empty/token-edge/refresh~~ → resolved with defaults: skeletons + spinner-with-label, shared error+retry component, shared expired/invalid-token screen + consent route-guard, manual-refresh (no polling), empty states, JD-form validation (title + ≥1 field). New cross-cutting task **T9**.
- **Non-goals**: single theme (no in-app dark toggle), desktop-only (no mobile recorder), Indonesian UI over English-sourced CV content (accepted).
- ⚠️ **Highest-risk component**: the audio recorder (T6) — mic-permission flow + MediaRecorder/webm compatibility; test in the demo browser on frontend Day 1, not late.
