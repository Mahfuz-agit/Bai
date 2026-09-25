from __future__ import annotations
from pathlib import Path
from .identity import book_id
from .pdf import extract_pages
from .chunking import chunk_pages

def ingest_pdf(path: str | Path, output_root: str | Path) -> Path:
    path = Path(path)
    bid = book_id(path)
    out = Path(output_root) / bid
    out.mkdir(parents=True, exist_ok=True)
    pages = extract_pages(path)
    chunks = chunk_pages(pages)
    (out / "source.json").write_text(
        __import__("json").dumps({"book_id": bid, "filename": path.name, "pages": len(pages)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out / "chunks.json").write_text(
        __import__("json").dumps([c.to_dict() for c in chunks], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out
