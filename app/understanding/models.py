"""Data models for the Deep Understanding Engine.

Every extracted item carries a page reference back to the source PDF,
per project requirement: "Keep source page references for every
extracted item."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Page:
    """One page of extracted book text."""

    page_number: int
    text: str


@dataclass
class Section:
    """A detected chapter / part / heading in the book."""

    title: str
    level: str  # "part" | "chapter" | "section" | "heading"
    page_number: int
    raw_line: str


@dataclass
class EvidenceCandidate:
    """A candidate piece of supporting evidence (study, example, data, citation)."""

    kind: str  # "study" | "example" | "data" | "citation"
    text: str
    page_number: int
    confidence: float = 0.5


@dataclass
class ReasoningCandidate:
    """A candidate reasoning step detected in the text."""

    kind: str  # "causal" | "contrast" | "conditional"
    text: str
    page_number: int
    marker: str = ""
    confidence: float = 0.5


@dataclass
class UnderstandingResult:
    """Full deep-understanding output for one book."""

    book_id: str
    sections: List[Section] = field(default_factory=list)
    evidence: List[EvidenceCandidate] = field(default_factory=list)
    reasoning: List[ReasoningCandidate] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    open_questions: List[str] = field(default_factory=list)
