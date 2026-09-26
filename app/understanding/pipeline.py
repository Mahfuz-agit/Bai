"""Deep Understanding Engine pipeline.

Orchestrates section, evidence, and reasoning candidate extraction into
one UnderstandingResult per book. Deterministic only — this stage does
not call any LLM/provider. That verification/enrichment is a later
version (v0.7+).
"""

from __future__ import annotations

import re
from typing import List, Sequence, Tuple

from app.understanding.evidence import detect_evidence
from app.understanding.models import UnderstandingResult
from app.understanding.reasoning import detect_reasoning
from app.understanding.structure import detect_sections

_QUESTION_RE = re.compile(r"[^.!?]*\?")


def _extract_open_questions(pages: Sequence[Tuple[int, str]]) -> List[str]:
    """Pull literal questions out of the text as open-question candidates."""
    questions: List[str] = []
    for _, text in pages:
        if not text:
            continue
        for match in _QUESTION_RE.findall(text.replace("\n", " ")):
            q = match.strip()
            if len(q.split()) >= 3:
                questions.append(q)
    return questions


def _derive_themes(sections) -> List[str]:
    """Use top-level section titles as a first-pass theme list."""
    themes: List[str] = []
    for section in sections:
        if section.level in ("part", "chapter") and section.title not in themes:
            themes.append(section.title)
    return themes


def build_understanding(
    book_id: str,
    pages: Sequence[Tuple[int, str]],
) -> UnderstandingResult:
    """Build the deep-understanding result for one book.

    Args:
        book_id: stable content-based book identifier (never a filename).
        pages: sequence of (page_number, page_text) tuples for the book.

    Returns:
        UnderstandingResult with sections, evidence, reasoning,
        themes, and open questions.
    """
    sections = detect_sections(pages)
    evidence = detect_evidence(pages)
    reasoning = detect_reasoning(pages)
    themes = _derive_themes(sections)
    open_questions = _extract_open_questions(pages)

    return UnderstandingResult(
        book_id=book_id,
        sections=sections,
        evidence=evidence,
        reasoning=reasoning,
        themes=themes,
        open_questions=open_questions,
    )
