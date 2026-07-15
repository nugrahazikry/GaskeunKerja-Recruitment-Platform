"""Regression test for a real CV-content leak found 2026-07-15, verified against the
user's own real CVs (never committed to this repo).

Root cause: pdf_captioning.merge_pdf_text_and_captions() used to choose between
describe_image() (short caption) and transcribe_image() (verbatim read) based on whether
the image's PAGE also had separately-extracted real text — the assumption being that an
image alongside real text must be decorative (a logo/photo). One of the user's real CVs
disproved this: the page had a short typed summary paragraph AND the full CV content was
ALSO embedded as an image on that same page. Because the page "had text," the old logic
picked describe_image() and silently dropped the entire image's content.

Fix: transcribe_image() is now called unconditionally on every embedded image, regardless
of whether its page also has text. describe_image() was removed (zero callers left).

This test reproduces the same shape with a synthetic generated image (real readable text
rendered via PIL, not the user's actual CV) sitting on a page that also has real text —
exactly the combination that broke the old routing.
"""

import io

from PIL import Image, ImageDraw, ImageFont

from services.pdf_captioning import merge_pdf_text_and_captions
from services.pdf_extraction import ExtractedImage, PdfExtractionResult

_SYNTHETIC_CV_TEXT_IN_IMAGE = "Regression Test Person\nSkills: Testing, QA, Regression"


def _make_synthetic_cv_image_bytes() -> bytes:
    """Renders real readable text into a PNG, simulating a CV embedded as an image."""
    img = Image.new("RGB", (600, 200), color="white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        font = ImageFont.load_default()
    draw.text((20, 20), _SYNTHETIC_CV_TEXT_IN_IMAGE, fill="black", font=font)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_image_on_a_text_bearing_page_is_still_transcribed_not_just_described():
    """The regression: a page has BOTH real extracted text (a short summary paragraph,
    like the user's real CV had) AND an embedded image containing separate, substantive
    text. Both must survive into the merged text — the image must not be reduced to a
    generic one-line caption just because the page wasn't text-empty."""
    image_bytes = _make_synthetic_cv_image_bytes()

    extraction = PdfExtractionResult(
        page_texts=["Ringkasan singkat: saya seorang penguji perangkat lunak."],
        empty_text_pages=frozenset(),  # page has text — this is exactly what broke the old logic
        images=[ExtractedImage(page_number=0, image_bytes=image_bytes)],
    )

    merged = merge_pdf_text_and_captions(extraction)

    assert "Ringkasan singkat" in merged, "the page's own real text should still be present"
    assert "Regression Test Person" in merged, (
        "the image's real content was NOT transcribed — the old describe-only-on-text-pages "
        "bug may have regressed"
    )
    assert "Testing, QA, Regression" in merged, (
        "the image's skill list was NOT transcribed — the old bug may have regressed"
    )


def test_no_image_means_no_vision_call_at_all():
    """Sanity check on the other half of the fix: pages with zero embedded images never
    trigger a vision call — this only affects pages where pypdf actually found an image."""
    extraction = PdfExtractionResult(
        page_texts=["Plain text CV with no images at all."],
        empty_text_pages=frozenset(),
        images=[],
    )

    merged = merge_pdf_text_and_captions(extraction)

    assert merged.strip() == "Plain text CV with no images at all."
    assert "[Image on page" not in merged, "no image existed, so no vision caption should appear"
