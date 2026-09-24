from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: Path, block_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(block_size)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def make_book_id(path: Path) -> str:
    """Stable identity from PDF content, not filename."""
    return f"book_{sha256_file(path)[:20]}"


def make_chunk_id(book_id: str, page_start: int, page_end: int, ordinal: int) -> str:
    raw = f"{book_id}:{page_start}:{page_end}:{ordinal}".encode()
    return hashlib.sha256(raw).hexdigest()[:20]
