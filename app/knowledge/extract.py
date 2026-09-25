from __future__ import annotations
import re
from collections import Counter
from .models import Concept, Claim, Relation

STOP = {"the","and","that","this","with","from","have","will","their","about","which","into","than","when","where","what","your","there","they","them","also","then","were","been","more","most","some","such","only","very","just","over","under","between","using","used","use","each","other","these","those","because","while","through","would","could","should"}

def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

def extract_concepts(text: str, limit: int = 12) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z'-]{3,}", text.lower())
    counts = Counter(w for w in words if w not in STOP)
    return [w for w, _ in counts.most_common(limit)]

def extract_claims(page_texts: list[tuple[int, str]], max_claims: int = 40) -> list[Claim]:
    claims: list[Claim] = []
    for page_no, text in page_texts:
        for s in _sentences(text):
            if 8 <= len(s.split()) <= 70 and re.search(r"\b(is|are|means|because|therefore|leads|causes|can|cannot|should|must|often|usually|research|study|evidence|suggests|shows)\b", s, re.I):
                cid = f"c{len(claims)+1:04d}"
                claims.append(Claim(cid, s, page_no, s))
                if len(claims) >= max_claims:
                    return claims
    return claims

def extract_questions(concepts: list[str]) -> list[str]:
    return [f"How does {c} work in this book?" for c in concepts[:8]]

def infer_relations(concepts: list[str], claims: list[Claim]) -> list[Relation]:
    relations: list[Relation] = []
    for claim in claims[:20]:
        present = [c for c in concepts if re.search(rf"\b{re.escape(c)}\b", claim.text, re.I)]
        if len(present) >= 2:
            relations.append(Relation(present[0], "related_to", present[1], claim.evidence))
    return relations[:50]
