"""Skill-gap analysis (Area 2 T8): candidate profile vs JD competencies -> structured gap.

Adapted from the Tahap 2 `_build_seed_gap()`/`_is_skill_match()` technique: compute a cheap
deterministic gap first (token-overlap), then use it to ground/constrain the LLM's structured
output, rather than trusting the LLM's judgment of "missing skills" unchecked.
"""

import json
import logging

from services import llm_client

logger = logging.getLogger("skillgap")


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


def analyze_skill_gap(
    candidate_skills: list[str], required_competencies: list[str], bypass_cache: bool = False
) -> dict:
    """bypass_cache is exposed for Area 5 QA T4 (report consistency test) — same
    reasoning as rubric.score_answer: a determinism test hitting the Area 4 disk cache
    after its first call proves nothing about the LLM's actual behavior."""
    seed_gap = build_seed_gap(candidate_skills, required_competencies)

    if not seed_gap:
        return {
            "gap_summary": "Kandidat memiliki seluruh kompetensi yang dibutuhkan untuk posisi ini.",
            "missing_competencies": [],
            "development_priority": None,
        }

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
