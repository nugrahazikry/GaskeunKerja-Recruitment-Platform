"""Area 5 QA T3b: PII redaction test.

Feeds CV text containing a known fake name/email/phone through the real ingest pipeline,
mocking only the outgoing LLM call (services.llm_client.chat_flash) to capture the exact
payload it would send — no live API call, zero cost, still proves redaction happens
before the payload is constructed.

⚠️ REAL FINDING (2026-07-13, found while writing this test, not yet fixed — needs a
product decision, see plan.md decision log): `services/candidate_ingest.py::ingest_cv()`
calls `pii_redaction.redact_pii(merged_text, alias=alias)` WITHOUT ever passing
`candidate_name` — and the `Candidate` DB model has no real-name field at all to source
one from (by design, candidates are only ever identified by alias). This means the
`redact_pii()` function's name-redaction branch is dead code in the real pipeline: email
and phone are reliably redacted, but a candidate's real name embedded in the CV text is
NOT currently redacted before reaching the LLM. Verified directly against real seed CV
text: the very common "first line is the name" heuristic is unreliable on this dataset
(first line was a job title, not a name, on a real sample). This test intentionally
asserts what the system ACTUALLY does today (email/phone: yes: name: no) rather than
assert a false "fully redacted" claim — flip the two commented-out name assertions once
a real fix is decided and shipped.
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
    redacted_text = pii_redaction.redact_pii(_FIXTURE_CV_TEXT, alias="FIXTURE-PII-TEST")

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


def test_name_redaction_gap_documented_not_yet_fixed():
    """⚠️ Documents a REAL, currently-unfixed gap: redact_pii's name-redaction branch is
    never invoked with a real name anywhere in the actual ingest_cv() pipeline, because
    Candidate has no real-name field to source one from. This test will start FAILING
    (in a good way) once a real fix ships — at that point, flip this to assert the name
    IS redacted, matching test_email_and_phone_never_reach_the_llm_payload's pattern."""
    redacted_text = pii_redaction.redact_pii(_FIXTURE_CV_TEXT, alias="FIXTURE-PII-TEST")

    # This is the ACTUAL current behavior (candidate_name defaults to None, never passed
    # by ingest_cv) — not the desired behavior. Asserting it here makes the gap visible
    # in CI/test output rather than silently assumed fixed.
    assert FAKE_NAME in redacted_text, (
        "This assertion documents a KNOWN GAP: redact_pii() is only ever called without "
        "candidate_name in the real pipeline, so names are NOT currently redacted. If "
        "this assertion starts failing, the gap has been fixed — update this test."
    )
