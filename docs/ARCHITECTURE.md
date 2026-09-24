# Architecture: Masterpiece AI

## North-star

Build a domain-specific cognitive system whose differentiation comes from its analysis process, verification discipline, and domain model—not merely from the choice of foundation model.

## Non-negotiable invariants

- No fabricated evidence.
- Facts and inferences are represented separately.
- The critic is adversarial, not decorative.
- Uncertainty is explicit.
- Domain logic remains version-controlled.
- Every major behavior is benchmarkable.

## Planned modules

### Perception
Parse raw input into entities, events, claims, relationships, temporal markers, and constraints.

### Retrieval
Hybrid lexical + semantic retrieval, then reranking. Later: knowledge graph traversal.

### Reasoning
Generate hypotheses, causal chains, counterfactuals, and implications.

### Verification
Check source support, internal consistency, rule violations, and contradiction with retrieved evidence.

### Synthesis
Produce a layered explanation: core conclusion, reasoning, evidence, uncertainty, alternatives, and implications.

### Evaluation
Maintain expert-authored cases, expected evidence, forbidden assumptions, and scoring rubrics.
