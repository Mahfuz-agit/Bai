# Masterpiece AI v0.4 — Knowledge Engine

A domain-specific personal knowledge engine for book/PDF understanding.

Pipeline:

`PDFs → pages/chunks → concepts → claims → reasoning → relations → contradictions → cross-book synthesis → structured knowledge`

This version is model-agnostic and deterministic by default. It builds a structured knowledge base from books and is designed to accept a stronger LLM provider later without changing the storage/graph contracts.

## Run locally

```bash
pip install -r requirements.txt
pytest -q
python -m app.knowledge.pipeline --input books --output data/library
```

Put any `.pdf` files in `books/`. Filenames do not need a special naming convention.
