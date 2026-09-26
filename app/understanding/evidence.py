"""Evidence candidate detection.

Finds study/example/data/citation style evidence with page references.
Deterministic keyword + pattern based candidate extraction.
"""

from __future__ import annotations

import re
from typing import List, Sequence, Tuple

from app.understanding.models import EvidenceCandidate

_STUDY_RE = re.compile(
    r"\b(study|studies|research|experiment|survey|trial|researchers?)\b",
    re.IGNORECASE,
)
_EXAMPLE_RE = re.compile(
    r"\b(for example|for instance|e\.g\.|such as|consider the case)\b",
    re.IGNORECASE,
)
_DATA_RE = re.compile(
    r"(\d+(\.\d+)?\s?%|\b\d{2,}(,\d{3})*\b)",
)
_CITATION_RE = re.compile(
    r"\(([A-Z][a-zA-Z]+(?:\s(?:&|and)\s[A-Z][a-zA-Z]+)?,?\s*\d{4}[a-z]?)\)|\[\d+\]",
)


def _split_sentences(text: str) -> List[str]:
    # Simple sentence split; good enough for candidate extraction.
    parts = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    return [p.strip() for p in parts if p.strip()]


def detect_evidence(pages: Sequence[Tuple[int, str]]) -> List[EvidenceCandidate]:
    """Detect evidence candidates from (page_number, page_text) pairs."""
    results: List[EvidenceCandidate] = []

    for page_number, text in pages:
        if not text:
            continue
        for sentence in _split_sentences(text):
            if _CITATION_RE.search(sentence):
                results.append(
                    EvidenceCandidate(
                        kind="citation",
                        text=sentence,
                        page_number=page_number,
                        confidence=0.7,
                    )
                )
                continue
            if _STUDY_RE.search(sentence):
                results.append(
                    EvidenceCandidate(
                        kind="study",
                        text=sentence,
                        page_number=page_number,
                        confidence=0.6,
                    )
                )
                continue
            if _EXAMPLE_RE.search(sentence):
                results.append(
                    EvidenceCandidate(
                        kind="example",
                        text=sentence,
                        page_number=page_number,
                        confidence=0.55,
                    )
                )
                continue
            if _DATA_RE.search(sentence):
                results.append(
                    EvidenceCandidate(
                        kind="data",
                        text=sentence,
                        page_number=page_number,
                        confidence=0.5,
                    )
                )

    return results
