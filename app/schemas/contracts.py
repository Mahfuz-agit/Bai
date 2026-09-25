from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class AnalysisResult:
    summary: str
    facts: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
