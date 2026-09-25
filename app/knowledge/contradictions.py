from __future__ import annotations
import re
from itertools import combinations
from .models import Claim

NEG = re.compile(r"\b(not|no|never|cannot|can't|doesn't|isn't|aren't|without|unlikely|fails|failure)\b", re.I)
WORD = re.compile(r"[A-Za-z][A-Za-z'-]{3,}")
STOP = {"this","that","these","those","with","from","about","because","therefore","their","there","which","when","where","what","should","could","would","often","usually","also","more","most","only","very"}

def _tokens(text: str) -> set[str]:
    return {w.lower() for w in WORD.findall(text) if w.lower() not in STOP}

def polarity(text: str) -> str:
    return "negative" if NEG.search(text) else "positive"

def detect_contradictions(books: list, min_overlap: int = 3, max_pairs: int = 100) -> list[dict]:
    findings: list[dict] = []
    items = []
    for book in books:
        for claim in book.claims:
            items.append((book.book_id, book.filename, claim))
    for (bid_a, file_a, a), (bid_b, file_b, b) in combinations(items, 2):
        if bid_a == bid_b:
            continue
        ta, tb = _tokens(a.text), _tokens(b.text)
        overlap = ta & tb
        if len(overlap) < min_overlap:
            continue
        if polarity(a.text) == polarity(b.text):
            continue
        findings.append({
            "books": [bid_a, bid_b],
            "files": [file_a, file_b],
            "claim_a": a.to_dict() if hasattr(a, "to_dict") else {
                "claim_id": a.claim_id, "text": a.text, "page_number": a.page_number, "evidence": a.evidence
            },
            "claim_b": b.to_dict() if hasattr(b, "to_dict") else {
                "claim_id": b.claim_id, "text": b.text, "page_number": b.page_number, "evidence": b.evidence
            },
            "shared_terms": sorted(overlap)[:15],
            "note": "Heuristic polarity conflict; verify the surrounding context before treating this as a true contradiction.",
        })
        if len(findings) >= max_pairs:
            return findings
    return findings
