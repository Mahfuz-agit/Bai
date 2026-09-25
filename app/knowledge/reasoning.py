from __future__ import annotations
import re
from dataclasses import asdict, dataclass
from .models import Claim

@dataclass
class ReasoningStep:
    step_id: str
    kind: str
    text: str
    page_number: int
    evidence: str

_PATTERNS = [
    ("definition", r"\b(is|are|means|refers to|defined as)\b"),
    ("cause", r"\b(because|therefore|thus|leads to|causes|results in|due to)\b"),
    ("recommendation", r"\b(should|must|need to|recommended|avoid|prefer)\b"),
    ("evidence", r"\b(research|study|studies|evidence|data|experiment|observed|shows|found)\b"),
    ("condition", r"\b(if|when|unless|provided that|only when)\b"),
]

def classify_claim(text: str) -> str:
    for kind, pattern in _PATTERNS:
        if re.search(pattern, text, re.I):
            return kind
    return "observation"

def extract_reasoning(claims: list[Claim], limit: int = 60) -> list[ReasoningStep]:
    steps: list[ReasoningStep] = []
    for claim in claims[:limit]:
        steps.append(ReasoningStep(
            step_id=f"r{len(steps)+1:04d}",
            kind=classify_claim(claim.text),
            text=claim.text,
            page_number=claim.page_number,
            evidence=claim.evidence,
        ))
    return steps

def reasoning_summary(steps: list[ReasoningStep]) -> dict:
    counts: dict[str, int] = {}
    for step in steps:
        counts[step.kind] = counts.get(step.kind, 0) + 1
    return {"step_count": len(steps), "by_kind": counts}

def steps_to_dict(steps: list[ReasoningStep]) -> list[dict]:
    return [asdict(step) for step in steps]
