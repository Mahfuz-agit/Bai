# Masterpiece AI — Personal Knowledge Engine

A model-agnostic intelligence engine designed to turn books into a connected, recallable knowledge base.

## Book workflow

Put any PDF anywhere under `books/`. **There is no filename convention.** The system discovers PDFs recursively, creates a stable content-based `book_id`, reads embedded PDF metadata when available, extracts page text, creates page-aware chunks, and writes a machine-readable library under `data/library/`.

```text
books/*.pdf
   ↓
PDF discovery (filename-independent)
   ↓
content hash → stable book_id
   ↓
page extraction + metadata
   ↓
page-aware chunking
   ↓
data/library/documents.jsonl
data/library/chunks.jsonl
data/library/index.json
```

Scanned/image-heavy PDFs are not silently treated as readable text. They are flagged in the ingestion summary for a later OCR stage.

## GitHub

- `zip-ingest.yml` installs project archives.
- `ingest-books.yml` automatically rebuilds the knowledge library when PDFs change.
- `analyze.yml` remains the reasoning pipeline entry point.

## Local run

```bash
pip install -r requirements.txt
python -m app.books.ingest --repo .
python -m app.main --input examples/sample.json
```
