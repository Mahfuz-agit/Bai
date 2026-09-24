from __future__ import annotations

import json
from dataclasses import dataclass

from app.providers.base import ModelProvider
from app.schemas.contracts import AnalysisResult, Critique, Evidence, Finding, InputCase


@dataclass
class CognitivePipeline:
    provider: ModelProvider

    def normalize(self, case: InputCase) -> str:
        return case.content.strip()

    def decompose(self, normalized: str) -> list[str]:
        parts = [p.strip() for p in normalized.replace("?", ".").split(".") if p.strip()]
        return parts[:12] or [normalized]

    def retrieve(self, case: InputCase) -> list[Evidence]:
        # Domain-specific retrieval will replace this stub.
        return []

    def analyze(self, case: InputCase, normalized: str, decomposition: list[str], evidence: list[Evidence]) -> list[Finding]:
        payload = {"content": normalized, "decomposition": decomposition, "evidence": [e.model_dump() for e in evidence]}
        response = self.provider.generate(
            system="Analyze the case deeply. Identify important findings, causal links, hidden assumptions, and uncertainty. Do not invent evidence.",
            user=json.dumps(payload, ensure_ascii=False),
        )
        return [Finding(statement=response, importance="medium", rationale="Initial model analysis; structured domain extraction is a later milestone.")]

    def critique(self, case: InputCase, findings: list[Finding], evidence: list[Evidence]) -> Critique:
        payload = {"content": case.content, "findings": [f.model_dump() for f in findings], "evidence": [e.model_dump() for e in evidence]}
        response = self.provider.generate(
            system="Act as an adversarial critic. Try to falsify the analysis. Find unsupported assumptions, contradictions, missing information, and plausible alternatives.",
            user=json.dumps(payload, ensure_ascii=False),
        )
        return Critique(vulnerabilities=[response])

    def synthesize(self, case: InputCase, findings: list[Finding], critique: Critique, evidence: list[Evidence]) -> str:
        payload = {
            "case": case.model_dump(),
            "findings": [f.model_dump() for f in findings],
            "critique": critique.model_dump(),
            "evidence": [e.model_dump() for e in evidence],
        }
        return self.provider.generate(
            system="Synthesize the strongest defensible conclusion. Separate facts, inference, uncertainty, and alternatives. Prefer precision over verbosity.",
            user=json.dumps(payload, ensure_ascii=False),
        )

    def run(self, case: InputCase) -> AnalysisResult:
        normalized = self.normalize(case)
        decomposition = self.decompose(normalized)
        evidence = self.retrieve(case)
        findings = self.analyze(case, normalized, decomposition, evidence)
        critique = self.critique(case, findings, evidence)
        synthesis = self.synthesize(case, findings, critique, evidence)
        return AnalysisResult(
            case_id=case.case_id,
            normalized_problem=normalized,
            decomposition=decomposition,
            findings=findings,
            evidence=evidence,
            critique=critique,
            synthesis=synthesis,
            uncertainty=critique.missing_information,
            confidence=0.5,
        )
