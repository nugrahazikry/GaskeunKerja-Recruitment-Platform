"""Skill-gap analysis (Area 2 T8): candidate profile vs JD competencies -> structured gap.

Adapted from the Tahap 2 `_build_seed_gap()`/`_is_skill_match()` technique: compute a cheap
deterministic gap first (token-overlap), then use it to ground/constrain the LLM's structured
output, rather than trusting the LLM's judgment of "missing skills" unchecked.
"""

import json
import logging
from collections import Counter

from services import llm_client

logger = logging.getLogger("skillgap")

_VOTES = 3  # self-consistency sample count — see analyze_skill_gap() docstring


def _normalize(s: str) -> str:
    return s.strip().lower()


def _is_skill_match(candidate_skill: str, required_skill: str) -> bool:
    """Deterministic token-overlap match — not an LLM judgment call."""
    c, r = _normalize(candidate_skill), _normalize(required_skill)
    return c == r or c in r or r in c


def build_seed_gap(candidate_skills: list[str], required_competencies: list[str]) -> list[str]:
    """Deterministic seed: which required competencies have NO matching candidate skill at all."""
    missing = []
    for req in required_competencies:
        if not any(_is_skill_match(cand_skill, req) for cand_skill in candidate_skills):
            missing.append(req)
    return missing


_GAP_PROMPT = """\
Kandidat memiliki keterampilan berikut: {candidate_skills}.
Posisi ini membutuhkan kompetensi berikut: {required_competencies}.
Berdasarkan analisis deterministik, kompetensi berikut TIDAK ditemukan pada kandidat: {seed_gap}.

Tulis analisis skill-gap singkat dalam Bahasa Indonesia. Kembalikan HANYA JSON:
{{"gap_summary": "<ringkasan singkat 2-3 kalimat>", "missing_competencies": ["<nama kompetensi>", ...], \
"development_priority": "<satu kompetensi paling prioritas untuk dikembangkan>"}}

PENTING: "missing_competencies" HARUS berupa subset dari daftar kompetensi yang tidak ditemukan di atas \
({seed_gap}) — jangan menambahkan kompetensi lain yang tidak ada di daftar tersebut."""


def _analyze_once(
    candidate_skills: list[str], required_competencies: list[str], seed_gap: list[str], bypass_cache: bool
) -> dict:
    prompt = _GAP_PROMPT.format(
        candidate_skills=", ".join(candidate_skills) or "(tidak ada)",
        required_competencies=", ".join(required_competencies),
        seed_gap=", ".join(seed_gap),
    )
    raw = llm_client.chat_pro([{"role": "user", "content": prompt}], bypass_cache=bypass_cache)

    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("analyze_skill_gap: failed to parse JSON, raw=%r", raw)
        parsed = {}

    # Ground the LLM output against the deterministic seed — never trust an LLM-invented
    # "missing competency" that isn't actually in the seed gap.
    llm_missing = parsed.get("missing_competencies", [])
    if not isinstance(llm_missing, list):
        llm_missing = []
    seed_gap_normalized = {_normalize(g) for g in seed_gap}
    grounded_missing = [m for m in llm_missing if _normalize(m) in seed_gap_normalized]
    if not grounded_missing:
        grounded_missing = seed_gap  # fall back to the deterministic seed itself

    return {
        "gap_summary": parsed.get("gap_summary", f"Kompetensi yang perlu dikembangkan: {', '.join(seed_gap)}."),
        "missing_competencies": grounded_missing,
        "development_priority": parsed.get("development_priority") or (seed_gap[0] if seed_gap else None),
    }


def analyze_skill_gap(
    candidate_skills: list[str], required_competencies: list[str], bypass_cache: bool = False
) -> dict:
    """Self-consistency voting (added 2026-07-13, closes a real gap found during Area 5
    QA T4): a single Deepseek Pro call's `missing_competencies` set and
    `development_priority` were measured to vary across independent calls on identical
    input — same root cause as rubric.score_answer's finding (provider-level
    temperature=0 non-determinism on batched/distributed inference, not a code bug).

    Calls the LLM _VOTES times and takes MAJORITY VOTE per competency (a competency
    survives into the final list only if at least half the votes included it) and the
    MOST COMMON development_priority value — more stable than trusting any single call.

    bypass_cache controls whether vote 1 hits the cache; votes 2+ are always independent
    (otherwise they'd just replay vote 1's cached response).
    """
    seed_gap = build_seed_gap(candidate_skills, required_competencies)

    if not seed_gap:
        return {
            "gap_summary": "Kandidat memiliki seluruh kompetensi yang dibutuhkan untuk posisi ini.",
            "missing_competencies": [],
            "development_priority": None,
        }

    votes = [_analyze_once(candidate_skills, required_competencies, seed_gap, bypass_cache=bypass_cache)]
    votes.extend(
        _analyze_once(candidate_skills, required_competencies, seed_gap, bypass_cache=True)
        for _ in range(_VOTES - 1)
    )

    # Majority vote on which competencies appear in missing_competencies, preserving the
    # seed_gap's original order for a stable, non-arbitrary final ordering.
    competency_vote_counts = Counter()
    for vote in votes:
        competency_vote_counts.update(_normalize(m) for m in vote["missing_competencies"])
    majority_threshold = len(votes) / 2
    majority_missing = [
        g for g in seed_gap if competency_vote_counts[_normalize(g)] >= majority_threshold
    ]
    if not majority_missing:
        majority_missing = seed_gap

    priority_votes = Counter(v["development_priority"] for v in votes if v["development_priority"])
    development_priority = priority_votes.most_common(1)[0][0] if priority_votes else (
        seed_gap[0] if seed_gap else None
    )

    # gap_summary: pick the summary from whichever vote's missing_competencies matches
    # the final majority result most closely, falling back to vote 1.
    summary_vote = next(
        (v for v in votes if set(_normalize(m) for m in v["missing_competencies"]) == set(_normalize(m) for m in majority_missing)),
        votes[0],
    )

    return {
        "gap_summary": summary_vote["gap_summary"],
        "missing_competencies": majority_missing,
        "development_priority": development_priority,
    }
