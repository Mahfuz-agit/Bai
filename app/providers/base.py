from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ModelProvider(ABC):
    @abstractmethod
    def generate(self, *, system: str, user: str, temperature: float = 0.2, **kwargs: Any) -> str:
        raise NotImplementedError
