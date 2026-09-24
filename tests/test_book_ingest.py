from pathlib import Path

from app.books.identity import make_chunk_id
from app.books.ingest import discover_pdfs


def test_pdf_discovery_ignores_filename_convention(tmp_path: Path):
    (tmp_path / "books" / "anything-at-all.pdf").parent.mkdir()
    (tmp_path / "books" / "anything-at-all.pdf").write_bytes(b"%PDF-placeholder")
    (tmp_path / "books" / "another name.pdf").write_bytes(b"%PDF-placeholder")
    (tmp_path / "books" / "UPPER.PDF").write_bytes(b"%PDF-placeholder")
    found = discover_pdfs(tmp_path / "books")
    assert len(found) == 3


def test_chunk_id_is_stable():
    assert make_chunk_id("book_abc", 1, 2, 1) == make_chunk_id("book_abc", 1, 2, 1)
