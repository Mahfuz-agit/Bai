# Masterpiece AI — Cognitive Architecture

A model-agnostic, domain-specialized intelligence engine designed around analysis quality rather than raw model size.

## Core pipeline

Input → Normalize → Decompose → Retrieve → Analyze → Critique → Verify → Synthesize → Explain

## Design principles

1. The LLM is a component, not the product.
2. Every important conclusion should carry evidence or an explicit uncertainty.
3. The system must challenge its own reasoning before producing the final answer.
4. Domain rules and knowledge must be separated from orchestration logic.
5. Evaluation is a first-class feature.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main --input examples/sample.json
```

The provider layer is intentionally abstract. Add OpenAI, Anthropic, local/open-weight, or other compatible providers without rewriting the cognitive pipeline.

## Next milestone

Add the exact target domain, ontology, retrieval corpus, domain rules, and a 50–100 case expert benchmark. Those become the system's real competitive core.
