import json
import logging
import re

from services import llm_client

logger = logging.getLogger("interview_questions")

_BASE_HEADER = """\
Anda adalah recruiter yang menyusun pertanyaan wawancara untuk posisi berikut:

Judul: {title}
Tanggung Jawab: {responsibilities}
Kualifikasi: {qualifications}
Persyaratan: {requirements}
"""

# Used when a slot HAS a hint (HR's own topic note for that slot). Deliberately does NOT tell the
# model to "use all three JD sections" the way _NO_HINT_INSTRUCTION does — that instruction is
# exactly what caused a slot hinted "QC pengalaman" to drift into ISO content pulled from the JD's
# Persyaratan section instead of staying a general experience question. The JD is now scoped to
# clarifying/enriching the hint's own topic only, not a second source of topics to introduce.
_HINT_INSTRUCTION = """
HR telah menuliskan catatan/topik berikut sebagai SATU-SATUNYA dasar untuk pertanyaan wawancara \
slot ini:
"{hint}"

TUGAS ANDA: ubah catatan "{hint}" di atas menjadi SATU pertanyaan wawancara yang lengkap dan jelas \
dalam Bahasa Indonesia, bisa dijawab lisan dalam 1-2 menit.

ATURAN KETAT — WAJIB DIPATUHI:
- Pertanyaan HARUS tetap membahas topik "{hint}" saja. DILARANG mengganti atau memperluas ke topik \
lain dari JD di atas — jika catatan hanya menyebut "{hint}", JANGAN membuat pertanyaan tentang ISO, \
alat ukur, atau kompetensi/standar lain yang TIDAK disebutkan dalam catatan "{hint}" ini sendiri.
- Judul/Tanggung Jawab/Kualifikasi/Persyaratan di atas HANYA boleh dipakai untuk membantu \
memperjelas atau memperkaya KALIMAT pertanyaan seputar topik "{hint}" — BUKAN untuk menambahkan \
kompetensi atau topik baru yang tidak ada di catatan ini.
"""

_NO_HINT_INSTRUCTION = """
Buat TEPAT SATU pertanyaan wawancara singkat dalam Bahasa Indonesia yang menguji kompetensi \
teknis dan pengalaman yang relevan untuk posisi ini. Gunakan KETIGA bagian di atas (Tanggung \
Jawab, Kualifikasi, dan Persyaratan) sebagai sumber — jangan hanya berpatokan pada satu bagian \
saja. Pertanyaan harus bisa dijawab lisan dalam 1-2 menit.
"""

_FORMAT_RULES = """
ATURAN FORMAT PENTING — pertanyaan HARUS berupa SATU pertanyaan tunggal saja:
- DILARANG menggabungkan dua pertanyaan dalam satu kalimat dengan kata sambung seperti "dan", \
"serta", "juga". Contoh SALAH (dua pertanyaan digabung): "Ceritakan pengalaman Anda menggunakan \
alat ukur, dan bagaimana Anda memastikan hasilnya akurat?" — ini harus dipecah, pilih SATU fokus \
saja, misalnya hanya: "Bagaimana Anda memastikan hasil pengukuran menggunakan alat ukur tetap \
akurat?"
- Hanya boleh ada SATU tanda tanya (?) di akhir kalimat.
- Pertanyaan menanyakan SATU hal spesifik saja (satu kompetensi/pengalaman), bukan beberapa \
sub-pertanyaan sekaligus.
"""

_OUTPUT_INSTRUCTION = """
Kembalikan HANYA JSON array berisi TEPAT SATU string pertanyaan, contoh:
["Pertanyaan ini?"]"""

_EXISTING_SECTION_TEMPLATE = """
Pertanyaan-pertanyaan berikut SUDAH ADA dan akan tetap dipakai bersama pertanyaan baru ini dalam \
satu sesi wawancara yang sama:
{existing_list}

Pertanyaan BARU yang Anda buat HARUS membahas topik/kompetensi yang BERBEDA dari daftar di atas — \
jangan menghasilkan pertanyaan yang temanya tumpang tindih atau mengulang salah satu pertanyaan \
yang sudah ada.
"""


def generate_one_question(
    title: str,
    responsibilities: str,
    requirements: str,
    qualifications: str,
    hint: str | None = None,
    existing_questions: list[str] | None = None,
) -> str | None:
    """Deepseek Flash -> exactly ONE Indonesian interview question for a JD. Returns None if the
    model's response couldn't be parsed into a usable question.

    Round-3 polish (2026-07-18): previously only received title/responsibilities/requirements —
    job.qualifications was silently ignored, so questions never reflected the Kualifikasi section.
    Now receives all three JD text fields.

    Round-3 follow-up (2026-07-19, real user finding): a targeted regenerate of one slot had no
    idea what topics sibling questions already covered, and could produce a thematically
    overlapping/duplicate question. existing_questions is passed to the prompt so the model
    explicitly avoids repeating topics already covered by the questions being kept.

    Round-3 follow-up (2026-07-19, real user finding — batching abandoned): asking for multiple
    questions in one call (even with an explicit "stay distinct from each other" rule) still
    produced mixed/inconsistent results in practice. Switched to generating ONE question per call —
    the frontend (QuestionsPage.tsx::handleGenerateConfirm) now loops this endpoint once per slot,
    IN ORDER, accumulating every question generated so far as existing_questions for the next call.
    Deliberately looped client-side rather than server-side so the UI can show live per-question
    progress ("AI sedang membuat pertanyaan 2 dari 4...") instead of one opaque multi-second wait.
    Costs one chat_flash() call per question instead of one call for the whole batch — a real
    latency tradeoff the user explicitly accepted after the batched approach didn't hold up.

    Round-3 follow-up (2026-07-19, real user finding — the actual root cause of "unrelated
    questions"): each HR-facing question slot can carry its OWN topic note the HR typed in
    (e.g. "QC pengalaman", "ISO 45001") — the generate call was completely discarding that slot's
    own text once checked for regeneration and generating a generic JD-grounded question instead,
    which is why a slot HR had labeled "QC pengalaman" came back as a generic "alat ukur" question
    with no connection to what HR had written. `hint`, when non-blank, is now that slot's own
    current text, and the prompt is instructed to build specifically off of it instead of ignoring
    it. A blank/whitespace-only hint (an empty slot) falls back to the plain JD-grounded prompt.
    """
    core_instruction = (
        _HINT_INSTRUCTION.format(hint=hint.strip())
        if hint and hint.strip()
        else _NO_HINT_INSTRUCTION
    )

    existing_section = ""
    if existing_questions:
        existing_list = "\n".join(f"- {q}" for q in existing_questions)
        existing_section = _EXISTING_SECTION_TEMPLATE.format(existing_list=existing_list)

    prompt = (
        _BASE_HEADER.format(
            title=title, responsibilities=responsibilities,
            qualifications=qualifications, requirements=requirements,
        )
        + core_instruction
        + _FORMAT_RULES
        + existing_section
        + _OUTPUT_INSTRUCTION
    )
    raw = llm_client.chat_flash([{"role": "user", "content": prompt}])

    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("generate_one_question: failed to parse JSON, raw=%r", raw)
        return None

    if not isinstance(parsed, list) or not parsed or not isinstance(parsed[0], str):
        return None
    return _single_question(parsed[0])


# Narrow form: "dan/serta" directly followed by a question-word/verb ("dan bagaimana", "serta
# ceritakan") — catches mid-sentence question joins even without a preceding comma.
_COMPOUND_JOIN_VERB_RE = re.compile(
    r",?\s+(?:dan|serta)\s+(?:bagaimana|apa|jelaskan|ceritakan|mengapa|kenapa)\b", re.IGNORECASE
)
# Broader form: a COMMA followed by "dan/serta" at all (regardless of the next word) — real example
# that slipped past the narrow form above: "...sesuai SOP, dokumentasi memenuhi ISO 9001 dan ISO
# 45001, serta tetap teliti saat bekerja shift?" (a 3-way clause list, "serta tetap..." isn't one
# of the whitelisted verbs). A comma immediately before "dan"/"serta" reliably marks a CLAUSE-level
# join in these compound questions (a plain word-list like "jangka sorong dan mikrometer" never has
# a comma before "dan"), so this is safe to always cut at.
_COMPOUND_JOIN_CLAUSE_RE = re.compile(r",\s+(?:dan|serta)\s+", re.IGNORECASE)


def _single_question(text: str) -> str:
    """Deterministic backstop for the "one question per item" prompt rule above. Real examples
    seen from the model only ever have ONE terminal "?" even though they ask two (or three)
    distinct things joined by "dan"/"serta" — so counting "?" marks can't detect this. Instead,
    cut at the EARLIEST compound-join point found by either pattern above, keeping only the first
    clause."""
    matches = [m.start() for m in (_COMPOUND_JOIN_VERB_RE.search(text), _COMPOUND_JOIN_CLAUSE_RE.search(text)) if m]
    if not matches:
        return text
    trimmed = text[: min(matches)].rstrip(" ,")
    return trimmed if trimmed.endswith("?") else trimmed + "?"
