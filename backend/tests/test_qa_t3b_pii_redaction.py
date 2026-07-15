"""Area 5 QA T3b: PII redaction test.

Feeds CV text containing a known fake name/email/phone through the real ingest pipeline,
mocking only the outgoing structured-parse LLM call (services.cv_parser.llm_client.chat_flash)
to capture the exact payload it would send — no live API call for that step, zero cost.

Name detection (services.pii_redaction.detect_candidate_name) makes ONE real, cheap
Flash call to find the name before redaction — this is the actual fix for the gap found
2026-07-13 (see plan.md decision log): `ingest_cv()` never had any way to know a
candidate's real name, since it's never captured as structured input anywhere (HR only
ever supplies job_id/alias/file) — the name only exists inside the raw CV text, and
nothing detected it before redaction ran. A "first line = name" heuristic was tested and
found unreliable on real seed CV text (Kaggle's public Resume Dataset is itself already
PII-stripped, which is exactly why using it for a hackathon demo was safe in the first
place — but it also meant this gap was invisible against the demo data specifically).
User chose an LLM-based extraction fix over a NER library or leaving it undocumented.
"""

from unittest.mock import patch

from services import pii_redaction
from services.cv_parser import parse_cv_text

FAKE_NAME = "Budi Santoso Fixture"
FAKE_EMAIL = "budi.santoso.fixture@example.com"
FAKE_PHONE = "0812-3456-7890"

_FIXTURE_CV_TEXT = f"""{FAKE_NAME}
Web Developer

Kontak: {FAKE_EMAIL}, telepon {FAKE_PHONE}

PENGALAMAN KERJA
Frontend Developer, PT Contoh (2021 - Sekarang)
Membangun antarmuka web menggunakan React dan JavaScript.

KEAHLIAN
HTML, CSS, JavaScript, React, Git
"""

_CANNED_LLM_RESPONSE = '{"skills": ["HTML", "CSS", "JavaScript"], "experience": [], "qualifications": []}'


def test_email_and_phone_never_reach_the_llm_payload():
    """Proves the UU PDP claim for email/phone: these are genuinely stripped before the
    LLM ever sees them."""
    candidate_name = pii_redaction.detect_candidate_name(_FIXTURE_CV_TEXT)
    redacted_text = pii_redaction.redact_pii(
        _FIXTURE_CV_TEXT, alias="FIXTURE-PII-TEST", candidate_name=candidate_name
    )

    captured_messages = []

    def fake_chat_flash(messages):
        captured_messages.append(messages)
        return _CANNED_LLM_RESPONSE

    with patch("services.cv_parser.llm_client.chat_flash", side_effect=fake_chat_flash):
        parse_cv_text(redacted_text, alias="FIXTURE-PII-TEST")

    assert captured_messages, "chat_flash was never called — test setup is broken"
    sent_payload = captured_messages[0][0]["content"]

    assert FAKE_EMAIL not in sent_payload, "raw email leaked into the LLM payload"
    assert FAKE_PHONE not in sent_payload, "raw phone leaked into the LLM payload"
    assert "[FIXTURE-PII-TEST-email]" in sent_payload
    assert "[FIXTURE-PII-TEST-phone]" in sent_payload


def test_name_is_now_detected_and_redacted():
    """✅ GAP CLOSED 2026-07-13: detect_candidate_name() makes a real Flash call to find
    the name, then redact_pii() (which already worked correctly once given a name)
    replaces it. This is the real fix — not a mock of the detection step, since the whole
    point is proving the LLM-based detection itself actually works on real-shaped text."""
    candidate_name = pii_redaction.detect_candidate_name(_FIXTURE_CV_TEXT)
    assert candidate_name == FAKE_NAME, f"name detection failed or found the wrong name: {candidate_name!r}"

    redacted_text = pii_redaction.redact_pii(
        _FIXTURE_CV_TEXT, alias="FIXTURE-PII-TEST", candidate_name=candidate_name
    )
    assert FAKE_NAME not in redacted_text, "raw name leaked into the redacted text"
    assert "FIXTURE-PII-TEST" in redacted_text


def test_name_detection_correctly_declines_on_name_free_text():
    """The real seed CVs (Kaggle's public Resume Dataset) are already PII-stripped and
    contain no name at all — detect_candidate_name() must return None rather than
    hallucinate a name from job titles/company names, matching real behavior measured
    against 5 real seed CVs during this fix."""
    name_free_text = (
        "PRODUCTION ASSOCIATE\nSummary\nConclude your application letter by thanking "
        "the employer for considering you for the position."
    )
    result = pii_redaction.detect_candidate_name(name_free_text)
    assert result is None, f"expected no name detected on name-free text, got {result!r}"
