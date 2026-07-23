"""Skill-gap analysis (Area 2 T8): candidate profile vs JD competencies -> structured gap.

Round 7 (2026-07-21, user decision): the deterministic seed-gap layer (`build_seed_gap()` +
`_is_skill_match()` word-containment + a hand-curated `_COMPETENCY_SYNONYMS` table) was removed on
purpose. It caught obvious cases (SQL -> Database) but had no way to generalize past its own
12-entry list — a candidate listing "Azure"/"GCP" against a required "Cloud Deployment" only
matched because "aws"/"azure"/"gcp" happened to be hand-typed into that one dictionary entry; any
required competency without a matching entry silently fell back to literal word-matching. The LLM
already knows AWS/Azure/GCP are cloud providers without anyone enumerating that by hand, so
`_GAP_PROMPT` below now asks it to judge the match directly, with explicit examples of the kind of
semantic (not literal) matching expected.

The known tradeoff, accepted explicitly: without a deterministic floor, the "no majority" fallback
in `analyze_skill_gap()` below can no longer fall back to a known-correct answer — it falls back to
the UNION of everything any of the 3 votes flagged (favors surfacing a possible gap over silently
hiding one, consistent with every other bug fix in this module's history, but it is a real
consistency trade against the old grounded version).

Round-3 follow-up (2026-07-19): this module's matched/missing list is now ALSO the basis for the
shortlist ranking score (services/matching.py), replacing semantic-similarity+graph-boost — see
that module's docstring for why. A per-matched-competency proficiency rating (1-3) was added so two
candidates who match the same competency set can still be told apart by depth of experience, not
just a raw count.
"""

import json
import logging
from collections import Counter

from sqlalchemy.orm import Session

from services import llm_client

logger = logging.getLogger("skillgap")

_VOTES = 3  # self-consistency sample count — see analyze_skill_gap() docstring


def _normalize(s: str) -> str:
    return s.strip().lower()


def combine_skills(skills: list[str], skills_implicit: list[str] | None) -> list[str]:
    """Round-3 follow-up #5 (2026-07-19, real bug found via live testing): skill-gap matching
    used to only ever see `parsed_profiles.skills` (explicit) — a candidate whose CV parse
    classified "Team Collaboration"/"Communication" as skills_implicit (soft/inferred) was shown
    those exact skills in the "Keahlian Tersirat" UI section, yet the SAME page's skill-gap
    analysis said "Team Collaboration and Communication" was missing — visibly contradictory to
    the user, since matching never looked at skills_implicit at all. Every matching-related call
    site now passes combine_skills(skills, skills_implicit) instead of skills alone, so implicit
    skills count as real evidence for matching."""
    if not skills_implicit:
        return list(skills)
    seen = {_normalize(s) for s in skills}
    combined = list(skills)
    for s in skills_implicit:
        if _normalize(s) not in seen:
            combined.append(s)
            seen.add(_normalize(s))
    return combined


_GAP_PROMPT = """\
Kandidat memiliki keterampilan berikut: {candidate_skills}.
Posisi ini membutuhkan kompetensi berikut: {required_competencies}.

Bandingkan keterampilan kandidat dengan setiap kompetensi yang dibutuhkan. JANGAN hanya mencocokkan \
kata secara harfiah — pertimbangkan juga kemiripan makna/konteks. Contoh: jika kandidat menyebutkan \
"AWS", "Azure", atau "GCP", itu berarti kandidat SUDAH memenuhi kompetensi "Cloud Deployment". Jika \
kandidat menyebutkan "SQL" atau "MySQL", itu berarti kandidat SUDAH memenuhi kompetensi "Database". \
Jika kandidat menyebutkan "React", "Vue", atau "Angular", itu berarti kandidat SUDAH memenuhi \
kompetensi "Frontend Framework". Terapkan penalaran serupa untuk kompetensi lain — kenali kapan \
sebuah tool/teknologi spesifik adalah instance dari kategori/kompetensi yang lebih umum.

Tulis analisis skill-gap dalam Bahasa Indonesia dengan struktur TEPAT 3 kalimat berikut:
- Kalimat 1: gambaran umum fondasi/kekuatan kandidat berdasarkan keseluruhan keterampilan yang dimiliki.
- Kalimat 2: sebutkan secara spesifik kompetensi mana yang SUDAH selaras dengan kebutuhan posisi ini, \
dan bagaimana keterampilan kandidat menunjukkan hal tersebut.
- Kalimat 3: sebutkan area pengembangan utama — kompetensi yang masih kurang dan mengapa hal itu \
penting untuk posisi ini (atau nyatakan bahwa kandidat sudah memenuhi seluruh kompetensi, jika memang \
tidak ada yang kurang).

Kembalikan HANYA JSON:
{{"gap_summary": "<paragraf 3 kalimat mengikuti struktur di atas>", \
"missing_competencies": ["<nama kompetensi yang TIDAK dimiliki kandidat — salin PERSIS dari daftar \
kompetensi yang dibutuhkan di atas, jangan menulis ulang dengan kata lain>", ...], \
"development_priority": "<satu kompetensi paling prioritas untuk dikembangkan, atau null jika \
kandidat sudah memenuhi semua kompetensi>"}}"""

# Round-3 follow-up #7 (2026-07-19): the no-gap case used to return a hardcoded flat sentence
# ("Kandidat memiliki seluruh kompetensi...") instead of a real analysis — user compared this
# directly against a reference implementation (an earlier personal project, "Skill gap analysis
# prod_v1") whose "Summary Analysis" is ALWAYS one LLM call producing a 2-3 sentence paragraph
# discussing fit/strengths, with or without a gap. Ported that behavior here: even with zero
# missing competencies, one direct call (no self-consistency needed — there's no missing-list to
# ground/protect here, unlike the has-gap path) produces a real narrative instead of a static line.
_NO_GAP_SUMMARY_PROMPT = """\
Kandidat memiliki keterampilan berikut: {candidate_skills}.
Posisi ini membutuhkan kompetensi berikut: {required_competencies}.
Kandidat sudah memenuhi SELURUH kompetensi yang dibutuhkan untuk posisi ini.

Tulis analisis kecocokan kandidat dalam Bahasa Indonesia dengan struktur TEPAT 3 kalimat berikut:
- Kalimat 1: gambaran umum fondasi/kekuatan kandidat berdasarkan keseluruhan keterampilan yang dimiliki.
- Kalimat 2: sebutkan secara spesifik kompetensi mana yang selaras dengan kebutuhan posisi ini, dan \
bagaimana keterampilan kandidat menunjukkan hal tersebut.
- Kalimat 3: tegaskan bahwa kandidat sudah memenuhi SELURUH kompetensi yang dibutuhkan, dan soroti \
mengapa hal ini menjadikan kandidat sangat cocok untuk posisi ini secara keseluruhan.

Kembalikan HANYA teks paragraf 3 kalimat mengikuti struktur di atas, tanpa JSON, tanpa tanda kutip \
pembuka/penutup."""


def _summarize_no_gap(candidate_skills: list[str], required_competencies: list[str]) -> str:
    prompt = _NO_GAP_SUMMARY_PROMPT.format(
        candidate_skills=", ".join(candidate_skills) or "(tidak ada)",
        required_competencies=", ".join(required_competencies),
    )
    raw = llm_client.chat_pro([{"role": "user", "content": prompt}])
    text = raw.strip().strip('"')
    return text or "Kandidat memiliki seluruh kompetensi yang dibutuhkan untuk posisi ini."


def _analyze_once(candidate_skills: list[str], required_competencies: list[str], bypass_cache: bool) -> dict:
    prompt = _GAP_PROMPT.format(
        candidate_skills=", ".join(candidate_skills) or "(tidak ada)",
        required_competencies=", ".join(required_competencies),
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

    # No deterministic grounding anymore (Round 7 decision, see module docstring) — trusted as-is,
    # only type-checked so a malformed response can't crash the caller.
    missing = parsed.get("missing_competencies", [])
    if not isinstance(missing, list):
        missing = []
    missing = [str(m) for m in missing if str(m).strip()]

    return {
        "gap_summary": parsed.get("gap_summary") or "Gagal menganalisis kesenjangan kompetensi.",
        "missing_competencies": missing,
        "development_priority": parsed.get("development_priority") or None,
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

    Round 7 (2026-07-21): no deterministic seed anymore (see module docstring) — every vote is a
    genuinely independent LLM judgment of candidate_skills vs required_competencies, nothing is
    pre-computed. This also means the "no gap" case can't be detected before calling the LLM
    (there's no seed to check emptiness of) — it's only known AFTER all 3 votes come back and
    unanimously agree on zero missing competencies.

    bypass_cache controls whether vote 1 hits the cache; votes 2+ are always independent
    (otherwise they'd just replay vote 1's cached response).
    """
    votes = [_analyze_once(candidate_skills, required_competencies, bypass_cache=bypass_cache)]
    votes.extend(_analyze_once(candidate_skills, required_competencies, bypass_cache=True) for _ in range(_VOTES - 1))

    # True consensus: every vote independently agreed there's nothing missing. Re-ask for a nicer
    # "you're fully qualified" narrative instead of reusing a has-gap vote's summary verbatim.
    if all(not v["missing_competencies"] for v in votes):
        return {
            "gap_summary": _summarize_no_gap(candidate_skills, required_competencies),
            "missing_competencies": [],
            "development_priority": None,
        }

    # Majority vote on which competencies appear in missing_competencies — a competency survives
    # only if at least half the votes independently named it. label_map keeps the first-seen
    # original casing/wording for whichever normalized key wins.
    competency_vote_counts = Counter()
    label_map: dict[str, str] = {}
    for vote in votes:
        for m in vote["missing_competencies"]:
            key = _normalize(m)
            competency_vote_counts[key] += 1
            label_map.setdefault(key, m)

    majority_threshold = len(votes) / 2
    majority_missing = [label_map[key] for key, count in competency_vote_counts.items() if count >= majority_threshold]

    # No majority (e.g. 3 votes named 3 different things, no overlap at all) — without a
    # deterministic seed to fall back to, fall back to the UNION of everything any vote flagged.
    # Deliberately biased toward surfacing a possible gap over silently hiding one (see module
    # docstring) — the alternative (fall back to vote 1, or to "no gap") risks dropping a real
    # missing competency just because the 3 calls happened to phrase it 3 different ways.
    if not majority_missing:
        majority_missing = list(label_map.values())

    priority_votes = Counter(v["development_priority"] for v in votes if v["development_priority"])
    development_priority = priority_votes.most_common(1)[0][0] if priority_votes else majority_missing[0]

    # gap_summary: pick the summary from whichever vote's missing_competencies matches the final
    # majority result most closely, falling back to vote 1.
    summary_vote = next(
        (v for v in votes if set(_normalize(m) for m in v["missing_competencies"]) == set(_normalize(m) for m in majority_missing)),
        votes[0],
    )

    return {
        "gap_summary": summary_vote["gap_summary"],
        "missing_competencies": majority_missing,
        "development_priority": development_priority,
    }


def _experience_to_text(candidate_experience: list | None) -> str:
    """Round-3 follow-up #4 (2026-07-19): now also includes per-bullet detail when available
    (experience[].bullets, added alongside the candidate-detail/laporan redesign) instead of just
    the one-sentence `summary` — this was flagged earlier as a real thinness problem (a candidate's
    detailed CV bullet points were being compressed into one generic sentence before reaching the
    proficiency-rating LLM call, quietly weakening its evidence). Bullets give that call the same
    level of detail the candidate actually wrote."""
    if not candidate_experience:
        return "(tidak ada riwayat pengalaman tercatat)"
    lines = []
    for e in candidate_experience:
        if isinstance(e, dict):
            header = f"- {e.get('role', '?')} di {e.get('company', '?')} ({e.get('duration', '?')}):"
            bullets = e.get("bullets")
            if isinstance(bullets, list) and bullets:
                lines.append(header)
                lines.extend(f"  * {b}" for b in bullets)
            else:
                lines.append(f"{header} {e.get('summary', '')}")
        else:
            lines.append(f"- {e}")
    return "\n".join(lines)


_PROFICIENCY_PROMPT = """\
Kandidat memiliki keterampilan berikut: {candidate_skills}.

Riwayat pengalaman kandidat:
{experience_text}

Untuk SETIAP kompetensi berikut yang sudah dikonfirmasi dimiliki kandidat: {matched_competencies}.

Nilai seberapa KUAT bukti kompetensi tersebut pada kandidat, HANYA berdasarkan bukti eksplisit yang \
tertulis di riwayat pengalaman/keterampilan di atas (jangan menebak atau mengasumsikan) — gunakan skala:
1 = disebutkan tetapi tidak ada bukti kedalaman (mis. hanya disebut di daftar skill tanpa konteks penggunaan)
2 = ada bukti penggunaan pada pekerjaan, tapi cakupan/durasi terbatas atau tidak jelas seberapa senior
3 = ada bukti penggunaan yang jelas, dengan durasi/tanggung jawab yang menunjukkan penguasaan kuat (mis. \
peran senior, proyek besar, tanggung jawab utama yang jelas berkaitan dengan kompetensi tersebut)

Kembalikan HANYA JSON, memetakan SETIAP nama kompetensi persis seperti tertulis di atas ke angka 1-3:
{{"<nama kompetensi 1>": <1-3>, "<nama kompetensi 2>": <1-3>}}"""


def rate_competency_proficiency(
    candidate_skills: list[str], candidate_experience: list | None, matched_competencies: list[str]
) -> dict[str, int]:
    """Round-3 follow-up (2026-07-19): one LLM call rating how strongly each already-matched
    competency is evidenced in the candidate's actual experience text (1=mentioned only, 2=some
    evidence of use, 3=strong/senior evidence) — this is what lets the new ranking formula (see
    services/matching.py) tell apart two candidates who match the identical competency SET but
    have very different depth of experience, instead of just counting matches.

    Not self-consistency-voted like analyze_skill_gap() — a 1-3 rating has much lower variance
    risk than an open-ended missing-competency judgment, so one call is enough here.
    """
    if not matched_competencies:
        return {}

    prompt = _PROFICIENCY_PROMPT.format(
        candidate_skills=", ".join(candidate_skills) or "(tidak ada)",
        experience_text=_experience_to_text(candidate_experience),
        matched_competencies=", ".join(matched_competencies),
    )
    raw = llm_client.chat_pro([{"role": "user", "content": prompt}])

    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("rate_competency_proficiency: failed to parse JSON, raw=%r", raw)
        parsed = {}

    if not isinstance(parsed, dict):
        parsed = {}

    # Ground + clamp: only accept ratings for competencies actually in matched_competencies (by
    # normalized name), clamp to 1-3, and default anything the LLM skipped to 2 (neutral/medium)
    # rather than silently dropping it from the score.
    by_normalized = {_normalize(k): v for k, v in parsed.items()}
    result: dict[str, int] = {}
    for name in matched_competencies:
        raw_value = by_normalized.get(_normalize(name))
        try:
            value = int(raw_value)
        except (TypeError, ValueError):
            value = 2
        result[name] = max(1, min(3, value))
    return result


_RECOMMENDATION_PROMPT = """\
Kandidat memiliki keterampilan berikut: {candidate_skills}.

Riwayat pengalaman kandidat (versi terjemahan Bahasa Indonesia — gunakan HANYA untuk instruksi #1 di bawah):
{experience_text}

Teks CV asli kandidat (bahasa aslinya, BELUM diterjemahkan — gunakan HANYA untuk instruksi #2 di bawah):
{raw_cv_text}

Kompetensi yang sudah dikonfirmasi dimiliki kandidat (relevan dengan posisi ini): {matched_competencies}.

Tulis dua hal berikut, HANYA berdasarkan bukti eksplisit di atas (jangan mengarang detail yang tidak ada):

1. "key_strengths": TEPAT 5 kekuatan utama kandidat, ditulis dalam Bahasa Indonesia. Setiap kekuatan \
punya "title" singkat (3-6 kata) dan "description" TEPAT 2 kalimat dengan struktur: Kalimat 1 = \
deskripsi kekuatan tersebut, Kalimat 2 = bukti konkret dari pengalaman kandidat yang mendukung klaim \
pada kalimat 1.

2. "resume_action_items": TEPAT 5 saran perbaikan kalimat CV bergaya ATS (Applicant Tracking System). \
Ambil kalimat "original" LANGSUNG dari "Teks CV asli kandidat" di atas — SALIN PERSIS apa adanya DALAM \
BAHASA ASLINYA (jangan diterjemahkan ke Bahasa Indonesia). Lalu tulis versi "improved" yang lebih kuat \
(action verb, hasil terukur jika memungkinkan) DALAM BAHASA YANG SAMA PERSIS dengan "original" — jika \
CV asli berbahasa Inggris maka "improved" juga HARUS berbahasa Inggris; jika CV asli berbahasa \
Indonesia maka "improved" juga HARUS berbahasa Indonesia. JANGAN mengarang pencapaian yang tidak \
disebutkan aslinya, hanya perkuat cara penulisannya.

Kembalikan HANYA JSON:
{{"key_strengths": [{{"title": "<judul>", "description": "<2 kalimat: deskripsi + bukti>"}}, ...], \
"resume_action_items": [{{"original": "<kalimat asli, salin persis dalam bahasa aslinya>", \
"improved": "<kalimat diperbaiki, dalam bahasa yang sama persis dengan original>"}}, ...]}}"""


def generate_recommendation_extras(
    candidate_skills: list[str],
    candidate_experience: list | None,
    matched_competencies: list[str],
    raw_cv_text: str | None = None,
) -> dict:
    """Round-3 follow-up #4 (2026-07-19): "Key Strengths" + "Resume Action Items (ATS)" sections
    from the Tahap 2 template (Agent 4 - Recommendation Report), adapted here as ONE additional
    LLM call grounded on the candidate's actual experience text and already-matched competencies.

    Round 7 (2026-07-21, user decision): no longer computed inside persist_skill_gap() at match
    time — see update_recommendation_extras_after_interview() below, called only once the
    candidate's interview is complete. raw_cv_text (services/candidate_ingest.py's redacted,
    PRE-translation text — see ParsedProfile.raw_text_redacted) is now also passed in so
    resume_action_items can quote+improve the candidate's ACTUAL CV wording in its ACTUAL original
    language, instead of the already-Indonesian-translated `experience` field (candidates parsed
    before this column existed have raw_cv_text=None — falls back to the translated text, so
    resume_action_items may come back in Indonesian for those older rows only)."""
    if not matched_competencies and not candidate_experience:
        return {"key_strengths": [], "resume_action_items": []}

    prompt = _RECOMMENDATION_PROMPT.format(
        candidate_skills=", ".join(candidate_skills) or "(tidak ada)",
        experience_text=_experience_to_text(candidate_experience),
        raw_cv_text=raw_cv_text or _experience_to_text(candidate_experience),
        matched_competencies=", ".join(matched_competencies) or "(tidak ada)",
    )
    raw = llm_client.chat_pro([{"role": "user", "content": prompt}])

    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("generate_recommendation_extras: failed to parse JSON, raw=%r", raw)
        parsed = {}

    if not isinstance(parsed, dict):
        parsed = {}

    key_strengths = parsed.get("key_strengths", [])
    if not isinstance(key_strengths, list):
        key_strengths = []
    key_strengths = [
        {"title": str(s.get("title", "")).strip(), "description": str(s.get("description", "")).strip()}
        for s in key_strengths
        if isinstance(s, dict) and s.get("title") and s.get("description")
    ]

    resume_action_items = parsed.get("resume_action_items", [])
    if not isinstance(resume_action_items, list):
        resume_action_items = []
    resume_action_items = [
        {"original": str(i.get("original", "")).strip(), "improved": str(i.get("improved", "")).strip()}
        for i in resume_action_items
        if isinstance(i, dict) and i.get("original") and i.get("improved")
    ]

    return {"key_strengths": key_strengths, "resume_action_items": resume_action_items}


_INTERVIEW_RECOMMENDATION_PROMPT = """\
Berikut adalah hasil wawancara AI kandidat, per pertanyaan — setiap pertanyaan dinilai pada 3 aspek \
(Kejelasan, Relevansi, Kedalaman Teknis, skala 1-5 beserta alasan penilaiannya), ditambah ringkasan AI \
atas jawaban kandidat:

{interview_data}

Berdasarkan HANYA hasil wawancara di atas (jangan mengarang detail yang tidak ada), tulis dua hal \
berikut dalam Bahasa Indonesia:

1. "interview_key_strengths": TEPAT 5 kekuatan utama kandidat SELAMA WAWANCARA. Setiap kekuatan punya \
"title" singkat (3-6 kata) dan "description" TEPAT 2 kalimat dengan struktur: Kalimat 1 = deskripsi \
kekuatan tersebut, Kalimat 2 = bukti konkret dari jawaban/penilaian wawancara yang mendukung klaim \
pada kalimat 1 (sebutkan pertanyaan atau aspek penilaian yang relevan).

2. "interview_feedback": TEPAT 5 catatan perbaikan/kelemahan kandidat SELAMA WAWANCARA. Setiap catatan \
punya "title" singkat (3-6 kata) dan "description" TEPAT 2 kalimat dengan struktur: Kalimat 1 = \
deskripsi kelemahan/area yang perlu diperbaiki, Kalimat 2 = bukti konkret dari jawaban/penilaian \
wawancara yang mendukung klaim pada kalimat 1.

Kembalikan HANYA JSON:
{{"interview_key_strengths": [{{"title": "<judul>", "description": "<2 kalimat: deskripsi + bukti>"}}, ...], \
"interview_feedback": [{{"title": "<judul>", "description": "<2 kalimat: deskripsi + bukti>"}}, ...]}}"""


def _interview_data_to_text(interview_answers: list[dict]) -> str:
    if not interview_answers:
        return "(tidak ada data wawancara)"
    lines = []
    for i, a in enumerate(interview_answers, start=1):
        lines.append(f"Pertanyaan {i}: {a['question_text']}")
        for r in a.get("rubric_scores", []):
            lines.append(f"  - {r['criterion_name']}: {r['score']}/5 — {r['rationale']}")
        if a.get("summary_text"):
            lines.append(f"  - Ringkasan AI: {a['summary_text']}")
    return "\n".join(lines)


def generate_interview_recommendation(interview_answers: list[dict]) -> dict:
    """Round 7 (2026-07-21, user decision): interview-performance counterpart to
    generate_recommendation_extras() above — same {"title", "description"} shape, but grounded on
    rubric_scores (clarity/relevance/technical_depth + rationale, see services/rubric.py) and each
    answer's AI summary (transcripts.summary_text) instead of the CV. Called only from
    update_recommendation_extras_after_interview() below, once the interview is fully scored —
    never at match time, since interview data doesn't exist yet then."""
    if not interview_answers:
        return {"interview_key_strengths": [], "interview_feedback": []}

    prompt = _INTERVIEW_RECOMMENDATION_PROMPT.format(interview_data=_interview_data_to_text(interview_answers))
    raw = llm_client.chat_pro([{"role": "user", "content": prompt}])

    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("generate_interview_recommendation: failed to parse JSON, raw=%r", raw)
        parsed = {}

    if not isinstance(parsed, dict):
        parsed = {}

    def _clean(field: str) -> list[dict]:
        items = parsed.get(field, [])
        if not isinstance(items, list):
            items = []
        return [
            {"title": str(s.get("title", "")).strip(), "description": str(s.get("description", "")).strip()}
            for s in items
            if isinstance(s, dict) and s.get("title") and s.get("description")
        ]

    return {
        "interview_key_strengths": _clean("interview_key_strengths"),
        "interview_feedback": _clean("interview_feedback"),
    }


_EFFORT_TIERS = ("low_effort", "medium_effort", "high_effort")

_UPSKILLING_PROMPT = """\
Kandidat belum memenuhi kompetensi-kompetensi berikut untuk posisi ini: {missing_competencies}.
{interview_feedback_block}
Untuk SETIAP kompetensi yang belum terpenuhi di atas, buat rencana upskilling yang detail dan \
actionable. Setiap kompetensi HARUS memiliki TEPAT 6 rencana pembelajaran, dengan pembagian:
- 2 rencana effort RENDAH (low_effort) — bisa dipelajari dalam hitungan jam/hari.
- 2 rencana effort SEDANG (medium_effort) — butuh waktu beberapa minggu.
- 2 rencana effort TINGGI (high_effort) — butuh waktu berbulan-bulan untuk dikuasai.
{interview_instruction}
Setiap rencana (baik untuk kompetensi maupun area wawancara) punya "title" (nama topik/skill/sumber \
belajar yang singkat dan jelas) dan "description" TEPAT 2 kalimat: Kalimat 1 = penjelasan apa yang \
dipelajari dari topik ini, Kalimat 2 = bagaimana topik ini membantu kandidat menutup kesenjangan \
tersebut secara konkret.

Kembalikan HANYA JSON dengan struktur berikut:
{{
  "kompetensi_belum_terpenuhi": {{"<nama kompetensi 1>": {{
     "low_effort": [{{"title": "...", "description": "..."}}, {{"title": "...", "description": "..."}}],
     "medium_effort": [{{"title": "...", "description": "..."}}, {{"title": "...", "description": "..."}}],
     "high_effort": [{{"title": "...", "description": "..."}}, {{"title": "...", "description": "..."}}]
   }}, "<nama kompetensi 2>": {{...}}, ... satu entri untuk SETIAP kompetensi yang belum terpenuhi \
di atas, jangan melewatkan satupun}},
  "area_pengembangan_wawancara": {{"<judul area 1>": {{...struktur sama seperti di atas...}}, ...}}
}}"""

_INTERVIEW_FEEDBACK_BLOCK = """
Selain itu, berikut adalah catatan area pengembangan kandidat berdasarkan hasil wawancara AI \
(setiap catatan sudah disertai bukti konkret):
{feedback_lines}
"""

_INTERVIEW_INSTRUCTION_WITH_FEEDBACK = """
Dari daftar catatan wawancara di atas, PILIH TEPAT 3 area yang PALING KRITIS untuk ditingkatkan \
(paling berdampak pada kinerja kandidat berdasarkan hasil wawancara), lalu buat rencana upskilling \
dengan struktur YANG SAMA (6 rencana per area: 2 effort rendah, 2 sedang, 2 tinggi) untuk \
masing-masing dari TEPAT 3 area yang dipilih tersebut."""

_INTERVIEW_INSTRUCTION_NO_FEEDBACK = """
Tidak ada catatan wawancara yang perlu ditindaklanjuti — kembalikan "area_pengembangan_wawancara" \
sebagai objek kosong {}."""


def generate_upskilling_plan(
    missing_competencies: list[str], interview_feedback: list[dict] | None = None
) -> dict[str, dict[str, dict[str, list[dict]]]]:
    """Round 8 (2026-07-21, user decision): fully LLM-generated upskilling plan, replacing the old
    deterministic competency_framework/resource_library lookup (services/report.py's old
    development_plan) — that lookup only ever covered ~10 hand-curated competencies for one demo
    role and silently produced nothing for anything else (see conversation history). One batched
    call covering ALL missing competencies at once (not one call per competency, unlike the
    interview-question generator elsewhere in this app, which found batching unreliable for
    generating multiple DISTINCT questions — this prompt's failure mode is different: each
    competency's 6 plans are independent of every other competency's, so there's no cross-item
    "stay distinct from each other" pressure that made batching unreliable there).

    Round 8 follow-up (2026-07-21, user decision): also folds in interview_feedback (the 5
    generate_interview_recommendation() items — title + evidence-backed weakness description) as
    additional input to the SAME call, with an explicit instruction for the LLM to pick the TOP 3
    most critical ones and build the same 6-plan structure for those — kept as a SEPARATE labeled
    group ("area_pengembangan_wawancara") in the response rather than merged into
    "kompetensi_belum_terpenuhi", since a CV skill gap ("REST API") and an interview weakness
    ("Kedalaman Teknis Sangat Dangkal") are different KINDS of gap (a skill to study vs. a
    communication/depth habit to practice) even though both get the same upskilling treatment.

    Returns {"kompetensi_belum_terpenuhi": {name: {tier: [...]}, ...},
             "area_pengembangan_wawancara": {name: {tier: [...]}, ...}} — entries only for
    competencies/areas the LLM actually returned a well-formed plan for; missing/malformed entries
    are logged, never silently fabricated. area_pengembangan_wawancara is capped at 3 entries
    defensively even if the LLM ignores the "pick exactly 3" instruction."""
    if not missing_competencies and not interview_feedback:
        return {"kompetensi_belum_terpenuhi": {}, "area_pengembangan_wawancara": {}}

    if interview_feedback:
        feedback_lines = "\n".join(f"- {f['title']}: {f['description']}" for f in interview_feedback)
        interview_feedback_block = _INTERVIEW_FEEDBACK_BLOCK.format(feedback_lines=feedback_lines)
        interview_instruction = _INTERVIEW_INSTRUCTION_WITH_FEEDBACK
    else:
        interview_feedback_block = ""
        interview_instruction = _INTERVIEW_INSTRUCTION_NO_FEEDBACK

    prompt = _UPSKILLING_PROMPT.format(
        missing_competencies=", ".join(missing_competencies) or "(tidak ada)",
        interview_feedback_block=interview_feedback_block,
        interview_instruction=interview_instruction,
    )
    raw = llm_client.chat_pro([{"role": "user", "content": prompt}])

    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("generate_upskilling_plan: failed to parse JSON, raw=%r", raw)
        parsed = {}

    if not isinstance(parsed, dict):
        parsed = {}

    def _clean_items(items) -> list[dict]:
        if not isinstance(items, list):
            return []
        return [
            {"title": str(s.get("title", "")).strip(), "description": str(s.get("description", "")).strip()}
            for s in items
            if isinstance(s, dict) and s.get("title") and s.get("description")
        ]

    parsed_cv = parsed.get("kompetensi_belum_terpenuhi", {})
    by_normalized_cv = {_normalize(k): v for k, v in parsed_cv.items()} if isinstance(parsed_cv, dict) else {}
    cv_result: dict[str, dict[str, list[dict]]] = {}
    for name in missing_competencies:
        entry = by_normalized_cv.get(_normalize(name))
        if not isinstance(entry, dict):
            logger.warning("generate_upskilling_plan: no plan returned for competency=%r", name)
            continue
        cv_result[name] = {tier: _clean_items(entry.get(tier)) for tier in _EFFORT_TIERS}

    # Not grounded against a fixed list — the LLM picks its own top-3 titles from the feedback it
    # was given, so there's nothing deterministic to validate the KEYS against (unlike missing
    # competencies, which come from an exact required-competency list). Just structure-validate and
    # defensively cap at 3, in case the model returns more despite the instruction.
    parsed_interview = parsed.get("area_pengembangan_wawancara", {})
    interview_result: dict[str, dict[str, list[dict]]] = {}
    if isinstance(parsed_interview, dict):
        for name, entry in list(parsed_interview.items())[:3]:
            if not isinstance(entry, dict):
                continue
            interview_result[name] = {tier: _clean_items(entry.get(tier)) for tier in _EFFORT_TIERS}

    return {"kompetensi_belum_terpenuhi": cv_result, "area_pengembangan_wawancara": interview_result}


def persist_skill_gap(
    db: Session,
    candidate_id: int,
    job_id: int,
    candidate_skills: list[str],
    required_names: list[str],
    candidate_experience: list | None = None,
) -> dict:
    """Computes skill-gap ONCE and persists it to skill_gap_results (Round-2 polish, 2026-07-17)
    — replaces the old pattern of calling analyze_skill_gap() live on every candidate-detail /
    report view. `matched_competencies` is derived from the already-grounded analyze_skill_gap()
    output, no extra LLM call needed.

    Round-3 follow-up (2026-07-19): also computes and persists competency_proficiency (1-3 per
    matched competency) — see rate_competency_proficiency()'s docstring. candidate_experience is
    optional (defaults to no evidence available, so proficiency ratings fall back to 1) so existing
    callers that don't have it handy don't break.

    Round 7 (2026-07-21, user decision): key_strengths/resume_action_items are NO LONGER computed
    here — this function runs at CV-upload/match time (services/matching.py::compute_match_score),
    before any interview exists, and the user explicitly wants those two fields (plus the new
    interview_key_strengths/interview_feedback) to only ever be generated AFTER the candidate's
    interview is fully transcribed+scored. Filled in later by
    update_recommendation_extras_after_interview() below, which updates this same row IN PLACE.

    Round 7 follow-up (2026-07-21, fixes a real regression the first version of this change
    introduced): this function ALSO runs from the manual "Analisis Ulang" escape hatch
    (routers/candidate_detail.py::reanalyze_skill_gap), used to refresh a candidate's gap analysis
    after the JD's competencies change — which can happen AFTER the candidate has already completed
    their interview and has real key_strengths/resume_action_items/interview_key_strengths/
    interview_feedback sitting on the row. Since this function always deletes+recreates the row, the
    first version hardcoded all extras fields to None on every call, silently wiping a
    completed interview's data every time HR re-analyzed a candidate for an unrelated reason (a JD
    edit). Fixed by carrying forward whatever was already on the row (if any) instead of always
    nulling — a fresh candidate (no prior row) still gets None as before; an already-interview-
    completed candidate keeps their extras across a JD-driven re-analysis; a not-yet-interviewed
    candidate re-matched again before their interview still correctly stays None (there was nothing
    to carry forward)."""
    from db import repositories as repo  # local import: avoids a module-load-order cycle with db/repositories.py

    gap_result = analyze_skill_gap(candidate_skills, required_names)
    matched = [name for name in required_names if name not in gap_result["missing_competencies"]]
    proficiency = rate_competency_proficiency(candidate_skills, candidate_experience, matched)

    existing = repo.skill_gap_results.list(db, candidate_id=candidate_id, job_id=job_id)
    prior_key_strengths = existing[0].key_strengths if existing else None
    prior_resume_action_items = existing[0].resume_action_items if existing else None
    prior_interview_key_strengths = existing[0].interview_key_strengths if existing else None
    prior_interview_feedback = existing[0].interview_feedback if existing else None
    prior_upskilling_plan = existing[0].upskilling_plan if existing else None
    for row in existing:
        db.delete(row)
    db.commit()

    repo.skill_gap_results.create(
        db,
        candidate_id=candidate_id,
        job_id=job_id,
        gap_summary=gap_result["gap_summary"],
        missing_competencies=gap_result["missing_competencies"],
        matched_competencies=matched,
        development_priority=gap_result["development_priority"],
        competency_proficiency=proficiency,
        key_strengths=prior_key_strengths,
        resume_action_items=prior_resume_action_items,
        interview_key_strengths=prior_interview_key_strengths,
        interview_feedback=prior_interview_feedback,
        upskilling_plan=prior_upskilling_plan,
    )
    return {
        **gap_result,
        "matched_competencies": matched,
        "competency_proficiency": proficiency,
        "key_strengths": prior_key_strengths or [],
        "resume_action_items": prior_resume_action_items or [],
        "interview_key_strengths": prior_interview_key_strengths or [],
        "interview_feedback": prior_interview_feedback or [],
        "upskilling_plan": prior_upskilling_plan or {},
    }


def update_recommendation_extras_after_interview(db: Session, candidate_id: int) -> dict:
    """Round 7 (2026-07-21, user decision): the CV-based key_strengths/resume_action_items AND the
    new interview-based interview_key_strengths/interview_feedback are computed HERE, once — only
    after the candidate's interview is fully transcribed+scored — instead of at CV-upload/match
    time. Called from services/interview_answers.py::process_answer(), right where
    compute_and_persist_interview_summary() already fires once every approved question has a
    scored answer.

    Updates the EXISTING skill_gap_results row IN PLACE (never deletes/recreates it) so the
    gap_summary/missing_competencies/matched_competencies/competency_proficiency computed at match
    time are left untouched — only the recommendation-extras fields (now including upskilling_plan) are written here."""
    from db import repositories as repo  # local import: avoids a module-load-order cycle with db/repositories.py

    candidate = repo.candidates.get(db, candidate_id)
    if not candidate:
        raise ValueError(f"Candidate {candidate_id} not found")

    existing = repo.skill_gap_results.list(db, candidate_id=candidate_id, job_id=candidate.job_id)
    if not existing:
        # Shouldn't normally happen — compute_match_score() always runs persist_skill_gap() before
        # a candidate can even be invited to interview — but don't crash the interview-scoring
        # pipeline over it; just skip, there's no row here to update onto.
        logger.warning(
            "update_recommendation_extras_after_interview: no skill_gap_results row for candidate_id=%s job_id=%s",
            candidate_id, candidate.job_id,
        )
        return {}
    row = existing[0]

    profiles = repo.parsed_profiles.list(db, candidate_id=candidate_id)
    profile = profiles[0] if profiles else None
    candidate_skills = combine_skills(profile.skills, profile.skills_implicit) if profile else []
    raw_cv_text = profile.raw_text_redacted if profile else None

    cv_extras = generate_recommendation_extras(
        candidate_skills,
        profile.experience if profile else None,
        row.matched_competencies,
        raw_cv_text=raw_cv_text,
    )

    interview_data = []
    for answer in repo.interview_answers.list(db, candidate_id=candidate_id):
        question = repo.interview_questions.get(db, answer.question_id)
        transcripts = repo.transcripts.list(db, answer_id=answer.id)
        rubric_rows = repo.rubric_scores.list(db, answer_id=answer.id)
        interview_data.append(
            {
                "question_text": question.question_text if question else "?",
                "summary_text": transcripts[0].summary_text if transcripts else None,
                "rubric_scores": [
                    {"criterion_name": r.criterion_name, "score": r.score, "rationale": r.rationale}
                    for r in rubric_rows
                ],
            }
        )
    interview_extras = generate_interview_recommendation(interview_data)

    # Real bug found 2026-07-22 (candidate 36): all three LLM calls used to be computed THEN
    # written to `row` together at the end — when the last (biggest/slowest) call, the upskilling
    # plan, timed out after retries, the exception propagated all the way up to
    # process_answer_background's bare except-log, so NONE of this got committed, including the
    # cv_extras/interview_extras work that had already finished successfully. Committing here,
    # before attempting the upskilling call, means a later timeout only leaves upskilling_plan
    # empty instead of silently discarding everything.
    row.key_strengths = cv_extras["key_strengths"]
    row.resume_action_items = cv_extras["resume_action_items"]
    row.interview_key_strengths = interview_extras["interview_key_strengths"]
    row.interview_feedback = interview_extras["interview_feedback"]
    db.commit()

    try:
        row.upskilling_plan = generate_upskilling_plan(row.missing_competencies, interview_extras["interview_feedback"])
    except Exception:
        logger.exception(
            "update_recommendation_extras_after_interview: generate_upskilling_plan failed for candidate_id=%s, "
            "leaving upskilling_plan empty",
            candidate_id,
        )
        row.upskilling_plan = {"kompetensi_belum_terpenuhi": {}, "area_pengembangan_wawancara": {}}
    db.commit()

    return {
        "key_strengths": row.key_strengths,
        "resume_action_items": row.resume_action_items,
        "interview_key_strengths": row.interview_key_strengths,
        "interview_feedback": row.interview_feedback,
        "upskilling_plan": row.upskilling_plan,
    }


def get_or_compute_skill_gap(
    db: Session,
    candidate_id: int,
    job_id: int,
    candidate_skills: list[str],
    required_names: list[str],
    candidate_experience: list | None = None,
) -> dict:
    """Reads the persisted skill_gap_results row if one exists; self-heals (computes + persists
    once) for older candidates that predate this table, so no separate backfill migration is
    required for the endpoint to work — only for making it warm/instant ahead of time.

    Round 7 (2026-07-21): key_strengths/resume_action_items/interview_key_strengths/
    interview_feedback can legitimately be None/empty here even for a fully-matched candidate — see
    persist_skill_gap()'s docstring — that's expected until the candidate's interview is complete."""
    from db import repositories as repo

    existing = repo.skill_gap_results.list(db, candidate_id=candidate_id, job_id=job_id)
    if existing:
        row = existing[0]
        return {
            "gap_summary": row.gap_summary,
            "missing_competencies": row.missing_competencies,
            "matched_competencies": row.matched_competencies,
            "development_priority": row.development_priority,
            "competency_proficiency": row.competency_proficiency or {},
            "key_strengths": row.key_strengths or [],
            "resume_action_items": row.resume_action_items or [],
            "interview_key_strengths": row.interview_key_strengths or [],
            "interview_feedback": row.interview_feedback or [],
            "upskilling_plan": row.upskilling_plan or {},
        }
    return persist_skill_gap(db, candidate_id, job_id, candidate_skills, required_names, candidate_experience)
