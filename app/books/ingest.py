from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.books.chunking import chunk_pages
from app.books.pdf import inspect_pdf


def discover_pdfs(books_dir: Path) -> list[Path]:
    """Discover PDFs recursively; filenames are never used as a required convention."""
    return sorted(p for p in books_dir.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def ingest(repo_root: Path) -> dict:
    books_dir = repo_root / "books"
    output_dir = repo_root / "data" / "library"
    output_dir.mkdir(parents=True, exist_ok=True)

    documents: list[dict] = []
    chunks: list[dict] = []
    warnings: list[dict] = []

    for pdf in discover_pdfs(books_dir):
        try:
            book, pages = inspect_pdf(pdf, repo_root)
            documents.append(book.model_dump())
            if book.likely_scanned:
                warnings.append({
                    "book_id": book.book_id,
                    "path": book.path,
                    "warning": "Very little extractable text was found; OCR may be required for this book."
                })
            chunks.extend(c.model_dump() for c in chunk_pages(book.book_id, pages))
        except Exception as exc:
            warnings.append({"path": pdf.relative_to(repo_root).as_posix(), "warning": f"PDF parse failed: {exc}"})

    write_jsonl(output_dir / "documents.jsonl", documents)
    write_jsonl(output_dir / "chunks.jsonl", chunks)
    (output_dir / "index.json").write_text(
        json.dumps({
            "document_count": len(documents),
            "chunk_count": len(chunks),
            "warnings": warnings,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {"document_count": len(documents), "chunk_count": len(chunks), "warnings": warnings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest every PDF under books/ into the Masterpiece knowledge library.")
    parser.add_argument("--repo", default=".", help="Repository root")
    args = parser.parse_args()
    result = ingest(Path(args.repo).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
