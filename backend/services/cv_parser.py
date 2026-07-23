import json
import logging

from services import llm_client

logger = logging.getLogger("cv_parser")

_PARSE_PROMPT = """\
Anda membaca teks CV kandidat berikut (nama asli sudah diganti dengan alias "{alias}" untuk privasi). \
Ekstrak informasi berikut dan kembalikan HANYA JSON (tanpa teks lain) berbentuk:
{{
  "cv_summary": "<ringkasan profil profesional TEPAT 3 kalimat: peran, tahun pengalaman, kekuatan utama>",
  "skills": ["<keterampilan yang DISEBUTKAN SECARA EKSPLISIT di CV, mis. bahasa/tools/teknologi>", ...],
  "skills_implicit": ["<keterampilan lunak/manajerial yang TERSIRAT dari deskripsi pengalaman tapi TIDAK ditulis eksplisit sebagai skill, mis. manajemen proyek, komunikasi stakeholder>", ...],
  "experience": [{{"role": "<posisi>", "company": "<jika ada, else null>", "duration": "<jika ada, else null>", "summary": "<ringkasan 1 kalimat>", "bullets": ["<poin tanggung jawab/pencapaian 1, kalimat singkat>", "<poin 2>", "..."], "tags": ["<1-4 kata kunci teknologi/kompetensi utama pada pekerjaan ini>"]}}],
  "qualifications": ["<kualifikasi/pendidikan 1>", ...],
  "education_level": "<jenjang pendidikan TERAKHIR/TERTINGGI, HARUS salah satu dari: SMA, SMK, D3, S1, S2, S3, atau null jika tidak disebutkan>",
  "major": "<jurusan/bidang studi pendidikan terakhir, atau null jika tidak disebutkan>",
  "education_history": [{{"degree": "<jenjang + jurusan>", "institution": "<nama institusi>", "period": "<jika ada, else null>", "gpa": "<jika ada, else null>"}}],
  "certifications": [{{"name": "<nama sertifikasi>", "issuer": "<penerbit, jika ada, else null>"}}],
  "featured_projects": [{{"name": "<nama proyek>", "description": "<deskripsi singkat>", "url": "<jika ada, else null>"}}],
  "organization_experience": [{{"role": "<posisi>", "organization": "<nama organisasi>", "period": "<jika ada, else null>", "description": "<deskripsi singkat>"}}]
}}

ATURAN BAHASA: seluruh teks naratif yang Anda TULIS SENDIRI (cv_summary, experience[].summary, \
experience[].bullets, featured_projects[].description, organization_experience[].description) HARUS \
dalam Bahasa Indonesia, walaupun teks asli CV berbahasa Inggris — terjemahkan maknanya, jangan \
menyalin kalimat Inggris apa adanya. JANGAN terjemahkan nama entitas (nama perusahaan, institusi, \
sertifikasi, produk, teknologi/tools) — biarkan seperti aslinya.

"experience[].bullets": IKUTI jumlah poin tanggung jawab/pencapaian PERSIS SEPERTI di CV asli — jika CV \
asli sudah menulis pengalaman tersebut sebagai bullet point, pecah SEMUA poin tersebut apa adanya \
(jangan menggabungkan atau memotong; jika ada 10 poin di CV asli, kembalikan 10 poin, JANGAN dibatasi \
2-6). Hanya jika deskripsi pengalaman di CV asli ditulis sebagai PARAGRAF (bukan bullet point), pecah \
paragraf tersebut sendiri menjadi bullet point, MAKSIMAL 6 poin. \
"summary" tetap diisi 1 kalimat ringkas sebagai fallback jika bullets tidak bisa dipecah.

Jika suatu bagian tidak ada di CV, kembalikan array kosong [] untuk bagian tersebut (bukan null, kecuali disebutkan null).

Teks CV:
{cv_text}"""


def parse_cv_text(cv_text: str, alias: str) -> dict:
    """Deepseek Flash -> structured {skills, experience, qualifications} from redacted CV text.

    cv_text MUST already be PII-redacted before calling this — this function does not redact.
    """
    prompt = _PARSE_PROMPT.format(alias=alias, cv_text=cv_text)
    raw = llm_client.chat_flash([{"role": "user", "content": prompt}])

    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    empty = {
        "cv_summary": None,
        "skills": [],
        "skills_implicit": [],
        "experience": [],
        "qualifications": [],
        "education_level": None,
        "major": None,
        "education_history": [],
        "certifications": [],
        "featured_projects": [],
        "organization_experience": [],
    }

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("parse_cv_text: failed to parse JSON, raw=%r", raw)
        return empty

    if not isinstance(parsed, dict):
        return empty

    _VALID_LEVELS = {"SMA", "SMK", "D3", "S1", "S2", "S3"}
    education_level = parsed.get("education_level")
    if not isinstance(education_level, str) or education_level.upper() not in _VALID_LEVELS:
        education_level = None
    else:
        education_level = education_level.upper()

    major = parsed.get("major")
    if not isinstance(major, str) or not major.strip():
        major = None

    cv_summary = parsed.get("cv_summary")
    if not isinstance(cv_summary, str) or not cv_summary.strip():
        cv_summary = None

    def _list_field(key: str) -> list:
        value = parsed.get(key)
        return value if isinstance(value, list) else []

    return {
        "cv_summary": cv_summary,
        "skills": _list_field("skills"),
        "skills_implicit": _list_field("skills_implicit"),
        "experience": _list_field("experience"),
        "qualifications": _list_field("qualifications"),
        "education_level": education_level,
        "major": major,
        "education_history": _list_field("education_history"),
        "certifications": _list_field("certifications"),
        "featured_projects": _list_field("featured_projects"),
        "organization_experience": _list_field("organization_experience"),
    }
