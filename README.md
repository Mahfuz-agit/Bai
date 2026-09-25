# Masterpiece AI v0.5 — Reasoning Engine

A domain-specific personal knowledge engine for turning many books/PDFs into structured, cross-book knowledge.

Pipeline:

`PDFs → pages/chunks → concepts → claims → reasoning → relations → contradiction candidates → cross-book claim matches → synthesis`

v0.5 adds a deterministic reasoning layer and candidate contradiction detector. It deliberately marks heuristic results as candidates so a later LLM verifier can check full context before conclusions are stored.

Put any `.pdf` files in `books/`. Filenames do not need a naming convention.

Run:

```bash
pip install -r requirements.txt
pytest -q
python -m app.knowledge.pipeline --input books --output data/library
```
