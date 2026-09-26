"""Reasoning candidate detection.

Detects causal, contrast, and conditional reasoning patterns in text
using marker words. Deterministic candidate extraction only — meaning
should be verified later by a provider/LLM stage.
"""

from __future__ import annotations

import re
from typing import List, Sequence, Tuple

from app.understanding.models import ReasoningCandidate

_CAUSAL_MARKERS = [
    "because", "therefore", "as a result", "leads to", "causes",
    "due to", "consequently", "thus", "hence", "results in",
]
_CONTRAST_MARKERS = [
    "however", "but", "on the other hand", "in contrast",
    "whereas", "although", "nevertheless", "yet",
]
_CONDITIONAL_MARKERS = [
    "if", "unless", "provided that", "as long as", "assuming that",
]


def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    return [p.strip() for p in parts if p.strip()]


def _find_marker(sentence: str, markers: Sequence[str]) -> str:
    lower = sentence.lower()
    for marker in markers:
        pattern = r"\b" + re.escape(marker) + r"\b"
        if re.search(pattern, lower):
            return marker
    return ""


def detect_reasoning(pages: Sequence[Tuple[int, str]]) -> List[ReasoningCandidate]:
    """Detect causal, contrast, and conditional reasoning candidates."""
    results: List[ReasoningCandidate] = []

    for page_number, text in pages:
        if not text:
            continue
        for sentence in _split_sentences(text):
            causal_marker = _find_marker(sentence, _CAUSAL_MARKERS)
            if causal_marker:
                results.append(
                    ReasoningCandidate(
                        kind="causal",
                        text=sentence,
                        page_number=page_number,
                        marker=causal_marker,
                        confidence=0.6,
                    )
                )

            contrast_marker = _find_marker(sentence, _CONTRAST_MARKERS)
            if contrast_marker:
                results.append(
                    ReasoningCandidate(
                        kind="contrast",
                        text=sentence,
                        page_number=page_number,
                        marker=contrast_marker,
                        confidence=0.6,
                    )
                )

            conditional_marker = _find_marker(sentence, _CONDITIONAL_MARKERS)
            if conditional_marker:
                results.append(
                    ReasoningCandidate(
                        kind="conditional",
                        text=sentence,
                        page_number=page_number,
                        marker=conditional_marker,
                        confidence=0.55,
                    )
                )

    return results
