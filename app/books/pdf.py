from __future__ import annotations

from pathlib import Path
from typing import Any

from pypdf import PdfReader

from app.books.identity import make_book_id
from app.books.models import BookRecord, PageRecord


def _clean_metadata_value(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def inspect_pdf(path: Path, repo_root: Path) -> tuple[BookRecord, list[PageRecord]]:
    reader = PdfReader(str(path))
    metadata = reader.metadata or {}
    pages: list[PageRecord] = []
    total_chars = 0
    pages_with_text = 0

    for number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").replace("\x00", "").strip()
        pages.append(PageRecord(page_number=number, text=text, char_count=len(text)))
        total_chars += len(text)
        if text:
            pages_with_text += 1

    page_count = len(reader.pages)
    # This is only a heuristic. We do not silently OCR books.
    likely_scanned = page_count > 0 and pages_with_text / page_count < 0.20
    extraction_mode = "text" if not likely_scanned else "text_with_possible_scan"

    record = BookRecord(
        book_id=make_book_id(path),
        path=path.relative_to(repo_root).as_posix(),
        title=_clean_metadata_value(metadata.get("/Title")),
        author=_clean_metadata_value(metadata.get("/Author")),
        subject=_clean_metadata_value(metadata.get("/Subject")),
        producer=_clean_metadata_value(metadata.get("/Producer")),
        page_count=page_count,
        extracted_characters=total_chars,
        extraction_mode=extraction_mode,
        likely_scanned=likely_scanned,
        pages_with_text=pages_with_text,
    )
    return record, pages
