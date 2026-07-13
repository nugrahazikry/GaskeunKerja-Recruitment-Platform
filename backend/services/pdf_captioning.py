import logging

from services import vision_client
from services.pdf_extraction import PdfExtractionResult

logger = logging.getLogger("pdf_captioning")


def merge_pdf_text_and_captions(extraction: PdfExtractionResult) -> str:
    """Merge per-page text with vision-LLM captions of embedded images.

    Images on empty-text pages (likely scanned) get a verbatim transcription;
    images on pages that already have text get a short descriptive caption.
    """
    parts: list[str] = []

    for page_number, text in enumerate(extraction.page_texts):
        if text.strip():
            parts.append(text.strip())

    for image in extraction.images:
        try:
            if image.page_number in extraction.empty_text_pages:
                caption = vision_client.transcribe_image(image.image_bytes)
            else:
                caption = vision_client.describe_image(image.image_bytes)
        except Exception as e:
            logger.warning("caption failed for page %d: %s", image.page_number, e)
            continue
        parts.append(f"[Image on page {image.page_number}]: {caption}")

    return "\n\n".join(parts)
