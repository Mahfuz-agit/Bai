from __future__ import annotations
from typing import Any
from .base import KnowledgeProvider

class MockProvider(KnowledgeProvider):
    def analyze(self, text: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        words = [w for w in text.split() if w]
        return {"summary": " ".join(words[:80]), "word_count": len(words)}
