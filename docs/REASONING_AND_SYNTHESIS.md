# Masterpiece AI v0.5 — Reasoning & Cross-Book Synthesis

v0.5 keeps the v0.4 PDF/knowledge pipeline and adds:

- reasoning-step classification for definitions, causes, recommendations, evidence, conditions, and observations
- heuristic cross-book claim matching
- heuristic contradiction candidates with explicit verification warnings
- richer library-level synthesis output

These are deterministic candidate generators, not truth judges. The next layer can attach an LLM verifier to validate context and produce deeper explanations.
