"""Section / chapter structure detection.

Deterministic, heuristic candidate extraction. Detects lines that look
like part/chapter/section headings or numbered headings. Does not rely
on filenames — only on page text content.
"""

from __future__ import annotations

import re
from typing import List, Sequence, Tuple

from app.understanding.models import Section

# Ordered so more specific patterns are checked before generic ones.
_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("part", re.compile(r"^\s*part\s+([ivxlcdm]+|\d+)\b[:\-\.]?\s*(.*)$", re.IGNORECASE)),
    ("chapter", re.compile(r"^\s*chapter\s+(\d+|[ivxlcdm]+)\b[:\-\.]?\s*(.*)$", re.IGNORECASE)),
    ("section", re.compile(r"^\s*section\s+(\d+(\.\d+)*)\b[:\-\.]?\s*(.*)$", re.IGNORECASE)),
    # Numbered heading like "3.2 Reinforcement Learning" or "4 Conclusion"
    ("heading", re.compile(r"^\s*(\d+(\.\d+)*)\s+([A-Z][A-Za-z0-9 ,'\-]{2,80})\s*$")),
]

_MAX_HEADING_WORDS = 12


def _looks_like_heading_case(line: str) -> bool:
    """Short, title-cased or all-caps standalone lines often are headings."""
    stripped = line.strip()
    if not stripped or len(stripped.split()) > _MAX_HEADING_WORDS:
        return False
    if stripped.endswith((".", ",", ";")):
        return False
    if stripped.isupper() and len(stripped) > 2:
        return True
    words = stripped.split()
    cap_words = [w for w in words if w[:1].isupper()]
    return len(words) >= 2 and len(cap_words) == len(words)


def detect_sections(pages: Sequence[Tuple[int, str]]) -> List[Section]:
    """Detect section/chapter-like headings from (page_number, text) pairs.

    Args:
        pages: sequence of (page_number, page_text).

    Returns:
        List of Section candidates, in page order.
    """
    sections: List[Section] = []

    for page_number, text in pages:
        if not text:
            continue
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            matched = False
            for level, pattern in _PATTERNS:
                m = pattern.match(line)
                if m:
                    title = line
                    sections.append(
                        Section(
                            title=title,
                            level=level,
                            page_number=page_number,
                            raw_line=raw_line,
                        )
                    )
                    matched = True
                    break

            if not matched and _looks_like_heading_case(line):
                sections.append(
                    Section(
                        title=line,
                        level="heading",
                        page_number=page_number,
                        raw_line=raw_line,
                    )
                )

    return sections
