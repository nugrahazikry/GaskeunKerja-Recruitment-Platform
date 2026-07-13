"""PDF text + embedded-image extraction (Area 2 T5), replicated from the NalarX pattern:
native text extraction + per-page empty-text detection + embedded-image extraction,
merged with vision-LLM captions instead of an OCR binary.
"""

import io
from dataclasses import dataclass

from pypdf import PdfReader


@dataclass
class ExtractedImage:
    page_number: int
    image_bytes: bytes


@dataclass
class PdfExtractionResult:
    page_texts: list[str]
    empty_text_pages: frozenset[int]
    images: list[ExtractedImage]

    @property
    def combined_text(self) -> str:
        return "\n\n".join(t for t in self.page_texts if t.strip())


def extract_pdf(file_bytes: bytes) -> PdfExtractionResult:
    reader = PdfReader(io.BytesIO(file_bytes))

    page_texts: list[str] = []
    empty_pages: set[int] = set()
    images: list[ExtractedImage] = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        page_texts.append(text)
        if not text.strip():
            empty_pages.add(page_number)

        for image_file in page.images:
            try:
                images.append(ExtractedImage(page_number=page_number, image_bytes=image_file.data))
            except Exception:
                continue  # per-image error isolation — one bad image doesn't lose the rest

    return PdfExtractionResult(
        page_texts=page_texts, empty_text_pages=frozenset(empty_pages), images=images
    )
