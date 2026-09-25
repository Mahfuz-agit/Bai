# Architecture

The system separates ingestion, knowledge extraction, graph construction and synthesis.

1. `app/books/` handles PDF identity, page extraction and chunking.
2. `app/knowledge/` converts text into concepts, claims and relations.
3. `graph.py` creates cross-book concept links.
4. `synthesis.py` creates cross-book comparison structures.
5. GitHub Actions runs tests and book processing.

A future LLM provider can replace the heuristic extraction stage while keeping the same contracts.
