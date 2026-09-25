from __future__ import annotations
import hashlib
from .models import Chunk, Page

def chunk_pages(pages: list[Page], max_chars: int = 2400, overlap: int = 250) -> list[Chunk]:
    chunks: list[Chunk] = []
    for page in pages:
        text = " ".join(page.text.split())
        if not text:
            continue
        start = 0
        while start < len(text):
            end = min(len(text), start + max_chars)
            piece = text[start:end].strip()
            if piece:
                cid = hashlib.sha1(f"{page.page_number}:{start}:{piece}".encode("utf-8")).hexdigest()[:14]
                chunks.append(Chunk(cid, page.page_number, piece, start, end))
            if end >= len(text):
                break
            start = max(0, end - overlap)
    return chunks
