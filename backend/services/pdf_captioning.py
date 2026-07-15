import logging

from services import vision_client
from services.pdf_extraction import PdfExtractionResult

logger = logging.getLogger("pdf_captioning")


def merge_pdf_text_and_captions(extraction: PdfExtractionResult) -> str:
    """Merge per-page text with vision-LLM transcriptions of embedded images.

    Every embedded image is transcribed verbatim (2026-07-15, fixed a real leak found by
    testing against the user's own real CVs) — no image is ever just "described" based on
    whether its page also has typed text. The previous page-has-text heuristic assumed an
    image alongside real text must be decorative (logo/photo), but a real CV was found
    where the page had a short typed summary AND the full CV content was ALSO embedded as
    an image on that same page — the old logic silently dropped the entire image's content
    because the page "already had text." Always-transcribe has no such blind spot: a
    genuinely decorative image (headshot, logo) just costs one vision call that comes back
    with little or no extractable text, which is a negligible real cost (~$0.0002/image on
    the current SumoPod gemini-2.5-flash-lite provider) compared to the risk of silently
    losing real CV content again.

    If a page has NO embedded image at all, vision is never called for that page — this
    only affects pages where pypdf's own image detector actually found something.
    """
    parts: list[str] = []

    for page_number, text in enumerate(extraction.page_texts):
        if text.strip():
            parts.append(text.strip())

    for image in extraction.images:
        try:
            caption = vision_client.transcribe_image(image.image_bytes)
        except Exception as e:
            logger.warning("caption failed for page %d: %s", image.page_number, e)
            continue
        parts.append(f"[Image on page {image.page_number}]: {caption}")

    return "\n\n".join(parts)
