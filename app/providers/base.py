from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class KnowledgeProvider(ABC):
    @abstractmethod
    def analyze(self, text: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError
