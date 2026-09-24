# Book Knowledge Engine

## Identity

Book identity is derived from a SHA-256 content hash. Filenames are descriptive only and are not part of the required naming contract. Duplicate copies with identical bytes receive the same `book_id`.

## Extraction

The first stage uses `pypdf` for embedded metadata and page text extraction. The engine records page numbers so later reasoning can cite the original location. It flags likely scanned PDFs rather than inventing text.

## Chunking

Chunks are built from consecutive non-empty pages with a target character ceiling. Each chunk stores the source `book_id` and page range. This creates the provenance layer needed for retrieval, comparison, contradiction checking, and later synthesis.

## Next layers

1. OCR fallback for scanned PDFs.
2. Semantic embeddings and retrieval.
3. Concepts/entities/claims extraction.
4. Cross-book relationship graph.
5. Claim-level contradiction and evidence checking.
6. Recall/learning engine that turns the library into personal memory.
