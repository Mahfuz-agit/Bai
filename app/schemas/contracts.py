from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class InputCase(BaseModel):
    case_id: str
    content: str
    context: dict[str, Any] = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)


class Evidence(BaseModel):
    source_id: str
    claim: str
    relevance: float = Field(ge=0, le=1)
    reliability: float = Field(ge=0, le=1)


class Finding(BaseModel):
    statement: str
    importance: Literal["low", "medium", "high", "critical"]
    rationale: str
    evidence_ids: list[str] = Field(default_factory=list)


class Critique(BaseModel):
    vulnerabilities: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    alternative_hypotheses: list[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    case_id: str
    normalized_problem: str
    decomposition: list[str]
    findings: list[Finding]
    evidence: list[Evidence]
    critique: Critique
    uncertainty: list[str] = Field(default_factory=list)
    synthesis: str
    confidence: float = Field(ge=0, le=1)
