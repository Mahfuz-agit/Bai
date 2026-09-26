# Deep Understanding Engine (v0.6)

## Goal
Move from extracted claims/concepts (v0.4-v0.5) to reconstructing a
book's internal structure and reasoning.

## Pipeline
```
PDF pages -> section/chapter structure -> evidence candidates
          -> reasoning steps -> themes -> open questions
```

## New files
- `app/understanding/models.py` — Page, Section, EvidenceCandidate,
  ReasoningCandidate, UnderstandingResult data classes.
- `app/understanding/structure.py` — detects part/chapter/section and
  numbered headings from page text.
- `app/understanding/evidence.py` — detects study/example/data/citation
  style evidence candidates, each with a page reference.
- `app/understanding/reasoning.py` — detects causal, contrast, and
  conditional reasoning candidates via marker words.
- `app/understanding/pipeline.py` — `build_understanding(book_id, pages)`
  orchestrates the above and adds a first-pass theme list and open
  questions.
- `tests/test_understanding.py` — acceptance tests.

## Design notes
- No filename dependency. Input is `(page_number, page_text)` pairs and
  a stable content-based `book_id` produced upstream (v0.3 identity).
- Every extracted item keeps a `page_number` reference back to source.
- All extraction here is **deterministic heuristics** — regex and
  marker-word matching. It is candidate data, not verified truth.
  Verification/enrichment by an LLM/provider is planned for v0.7+.
- Provider/model abstraction from earlier versions is untouched; this
  module has no provider calls yet.

## Usage
```python
from app.understanding import build_understanding

pages = [(1, "Chapter 1: Foundations"), (2, "A study shows... Because...")]
result = build_understanding("book-abc123", pages)

result.sections     # list[Section]
result.evidence      # list[EvidenceCandidate]
result.reasoning     # list[ReasoningCandidate]
result.themes        # list[str]
result.open_questions  # list[str]
```

## Test status
7/7 tests pass (6 acceptance tests + 1 full-pipeline integration test).
Existing v0.3-v0.5 tests are untouched and still run in CI.

## Next
- v0.7 Evidence verification (LLM/provider confirms candidates)
- v0.8 Contradiction engine
- v0.9 Cross-book reasoning graph
- v1.0 Synthesis + personal learning/memory system
