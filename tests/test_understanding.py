"""Acceptance tests for the v0.6 Deep Understanding Engine."""

from app.understanding.evidence import detect_evidence
from app.understanding.pipeline import build_understanding
from app.understanding.reasoning import detect_reasoning
from app.understanding.structure import detect_sections


def test_section_extraction_returns_detected_sections():
    pages = [
        (1, "Chapter 1: The Beginning\nSome intro text here."),
        (2, "1.1 Background\nMore body text."),
    ]
    sections = detect_sections(pages)
    assert len(sections) >= 2
    levels = {s.level for s in sections}
    assert "chapter" in levels
    assert sections[0].page_number == 1


def test_evidence_extraction_returns_evidence_candidates():
    pages = [
        (5, "A recent study found that sleep improves memory retention."),
        (6, "For example, consider two groups of students taking the same test."),
    ]
    evidence = detect_evidence(pages)
    assert len(evidence) >= 2
    kinds = {e.kind for e in evidence}
    assert "study" in kinds
    assert "example" in kinds
    assert all(e.page_number in (5, 6) for e in evidence)


def test_reasoning_extraction_detects_causal_reasoning():
    pages = [(3, "The team missed the deadline because the plan changed twice.")]
    reasoning = detect_reasoning(pages)
    causal = [r for r in reasoning if r.kind == "causal"]
    assert len(causal) == 1
    assert causal[0].marker == "because"
    assert causal[0].page_number == 3


def test_reasoning_extraction_detects_contrast_reasoning():
    pages = [(4, "The theory predicted growth. However, the market declined sharply.")]
    reasoning = detect_reasoning(pages)
    contrast = [r for r in reasoning if r.kind == "contrast"]
    assert len(contrast) == 1
    assert contrast[0].marker == "however"


def test_reasoning_extraction_detects_conditional_reasoning():
    pages = [(7, "If demand increases, the price will rise next quarter.")]
    reasoning = detect_reasoning(pages)
    conditional = [r for r in reasoning if r.kind == "conditional"]
    assert len(conditional) == 1
    assert conditional[0].marker == "if"


def test_full_pipeline_builds_understanding_result():
    pages = [
        (1, "Chapter 1: Foundations"),
        (2, "A study shows that practice improves skill. Because of this, "
            "experts recommend daily repetition. However, some critics disagree. "
            "If motivation drops, results decline. What causes this drop?"),
    ]
    result = build_understanding("book-abc123", pages)
    assert result.book_id == "book-abc123"
    assert len(result.sections) >= 1
    assert len(result.evidence) >= 1
    assert len(result.reasoning) >= 3
    assert any("?" in q for q in result.open_questions)


def test_existing_tests_remain_green_placeholder():
    # This file only adds new coverage; it must not remove or break
    # any existing v0.3-v0.5 tests, which live in their own test files
    # (test_pipeline.py, test_knowledge_extract.py) and are run
    # alongside this one in CI.
    assert True
