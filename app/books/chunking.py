from __future__ import annotations

from app.books.identity import make_chunk_id
from app.books.models import ChunkRecord, PageRecord


def chunk_pages(book_id: str, pages: list[PageRecord], max_chars: int = 4500) -> list[ChunkRecord]:
    chunks: list[ChunkRecord] = []
    buffer: list[str] = []
    start_page: int | None = None
    end_page: int | None = None
    ordinal = 0

    def flush() -> None:
        nonlocal buffer, start_page, end_page, ordinal
        if not buffer or start_page is None or end_page is None:
            return
        text = "\n\n".join(buffer).strip()
        if text:
            ordinal += 1
            chunks.append(ChunkRecord(
                chunk_id=make_chunk_id(book_id, start_page, end_page, ordinal),
                book_id=book_id,
                page_start=start_page,
                page_end=end_page,
                text=text,
                char_count=len(text),
            ))
        buffer = []
        start_page = None
        end_page = None

    for page in pages:
        text = page.text.strip()
        if not text:
            continue
        if start_page is None:
            start_page = page.page_number
        candidate = "\n\n".join(buffer + [text])
        if buffer and len(candidate) > max_chars:
            flush()
            start_page = page.page_number
            buffer = [text]
        else:
            buffer.append(text)
        end_page = page.page_number

    flush()
    return chunks
