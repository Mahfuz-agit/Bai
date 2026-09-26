"""Deep Understanding Engine (v0.6).

Reconstructs a book's internal structure and reasoning from page text:
sections, evidence candidates, and reasoning steps (causal, contrast,
conditional). All extraction here is deterministic and heuristic-based.
It is NOT final truth — later stages (LLM/provider verification) must
confirm and enrich these candidates.
"""

from app.understanding.models import (
    Section,
    EvidenceCandidate,
    ReasoningCandidate,
    UnderstandingResult,
)
from app.understanding.pipeline import build_understanding

__all__ = [
    "Section",
    "EvidenceCandidate",
    "ReasoningCandidate",
    "UnderstandingResult",
    "build_understanding",
]
