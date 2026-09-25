from app.knowledge.models import Claim, KnowledgeBook, Concept
from app.knowledge.reasoning import extract_reasoning
from app.knowledge.contradictions import detect_contradictions
from app.knowledge.synthesis import synthesize

def test_reasoning_classification():
    claims = [Claim("c1", "Memory improves recall because retrieval strengthens access.", 1, "e")]
    steps = extract_reasoning(claims)
    assert steps[0].kind == "cause"

def test_cross_book_contradiction_heuristic():
    a = KnowledgeBook("a", "a.pdf", claims=[Claim("c1", "Practice is necessary for skill improvement.", 1, "e")])
    b = KnowledgeBook("b", "b.pdf", claims=[Claim("c1", "Practice is not necessary for skill improvement.", 2, "e")])
    hits = detect_contradictions([a, b])
    assert hits

def test_synthesis_contains_conflicts():
    a = KnowledgeBook("a", "a.pdf", concepts=[Concept("k1", "memory")])
    b = KnowledgeBook("b", "b.pdf", concepts=[Concept("k1", "memory")])
    result = synthesize([a, b])
    assert result["book_count"] == 2
    assert result["cross_book_links"]
