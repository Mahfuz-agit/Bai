from __future__ import annotations
from itertools import combinations
from .models import KnowledgeBook

def synthesize(books: list[KnowledgeBook]) -> dict:
    links = []
    for a, b in combinations(books, 2):
        ca = {c.label.lower() for c in a.concepts}
        cb = {c.label.lower() for c in b.concepts}
        shared = sorted(ca & cb)
        if shared:
            links.append({"books": [a.book_id, b.book_id], "shared_concepts": shared[:20]})
    return {
        "book_count": len(books),
        "cross_book_links": links,
        "open_questions": [q for b in books for q in b.questions][:30],
    }
