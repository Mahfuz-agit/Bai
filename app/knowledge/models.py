from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Literal

RelationType = Literal["supports", "contradicts", "depends_on", "causes", "example_of", "related_to"]

@dataclass
class Concept:
    concept_id: str
    label: str
    evidence: list[str] = field(default_factory=list)

@dataclass
class Claim:
    claim_id: str
    text: str
    page_number: int
    evidence: str
    kind: str = "claim"

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Relation:
    source: str
    relation: RelationType
    target: str
    evidence: str

@dataclass
class KnowledgeBook:
    book_id: str
    filename: str
    concepts: list[Concept] = field(default_factory=list)
    claims: list[Claim] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)
    insights: list[str] = field(default_factory=list)
    reasoning: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
