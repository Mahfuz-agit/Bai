from __future__ import annotations
from itertools import combinations
from collections import defaultdict
from .models import KnowledgeBook
from .contradictions import detect_contradictions

def _claim_terms(text: str) -> set[str]:
    import re
    stop = {"the","and","that","this","with","from","have","will","their","about","which","into","than","when","where","what","your","there","they","them","also","then","were","been","more","most","some","such","only","very","just"}
    return {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]{3,}", text) if w.lower() not in stop}

def _cross_book_claim_matches(books: list[KnowledgeBook], limit: int = 80) -> list[dict]:
    rows = []
    for a, b in combinations(books, 2):
        for ca in a.claims:
            ta = _claim_terms(ca.text)
            if not ta:
                continue
            for cb in b.claims:
                overlap = ta & _claim_terms(cb.text)
                if len(overlap) >= 3:
                    rows.append({
                        "books": [a.book_id, b.book_id],
                        "claim_a": ca.text,
                        "claim_b": cb.text,
                        "shared_terms": sorted(overlap)[:12],
                    })
                    if len(rows) >= limit:
                        return rows
    return rows

def synthesize(books: list[KnowledgeBook]) -> dict:
    links = []
    concept_index: dict[str, list[str]] = defaultdict(list)
    for book in books:
        for c in book.concepts:
            concept_index[c.label.lower()].append(book.book_id)
    for a, b in combinations(books, 2):
        ca = {c.label.lower() for c in a.concepts}
        cb = {c.label.lower() for c in b.concepts}
        shared = sorted(ca & cb)
        if shared:
            links.append({"books": [a.book_id, b.book_id], "shared_concepts": shared[:20]})
    contradictions = detect_contradictions(books)
    claim_matches = _cross_book_claim_matches(books)
    return {
        "book_count": len(books),
        "cross_book_links": links,
        "cross_book_claim_matches": claim_matches,
        "potential_contradictions": contradictions,
        "open_questions": [q for b in books for q in b.questions][:50],
        "synthesis_status": "heuristic-draft",
        "synthesis_note": "Shared concepts and claim matches are candidate links, not final conclusions. An LLM verifier can validate context later.",
    }
