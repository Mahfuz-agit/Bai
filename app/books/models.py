from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class Page:
    page_number: int
    text: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class Chunk:
    chunk_id: str
    page_number: int
    text: str
    start_char: int
    end_char: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
