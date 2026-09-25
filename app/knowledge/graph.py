from __future__ import annotations
from collections import defaultdict
from .models import KnowledgeBook

def build_graph(books: list[KnowledgeBook]) -> dict:
    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    for book in books:
        for concept in book.concepts:
            nodes.setdefault(concept.label.lower(), {"label": concept.label, "books": []})
            nodes[concept.label.lower()]["books"].append(book.book_id)
        for rel in book.relations:
            edges.append({"source": rel.source, "relation": rel.relation, "target": rel.target, "book_id": book.book_id})
    return {"nodes": list(nodes.values()), "edges": edges}

def cross_book_links(books: list[KnowledgeBook]) -> list[dict]:
    index: dict[str, list[str]] = defaultdict(list)
    for book in books:
        for c in book.concepts:
            index[c.label.lower()].append(book.book_id)
    return [{"concept": c, "book_ids": sorted(set(ids))} for c, ids in index.items() if len(set(ids)) > 1]
