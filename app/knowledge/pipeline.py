from __future__ import annotations
import argparse, json
from pathlib import Path
from .models import KnowledgeBook, Concept
from .extract import extract_concepts, extract_claims, extract_questions, infer_relations
from .reasoning import extract_reasoning, reasoning_summary
from .graph import build_graph, cross_book_links
from .synthesis import synthesize
from app.books.identity import book_id
from app.books.pdf import extract_pages

def analyze_pdf(path: Path) -> KnowledgeBook:
    bid = book_id(path)
    pages = extract_pages(path)
    text = "\n".join(p.text for p in pages)
    labels = extract_concepts(text)
    concepts = [Concept(f"k{i+1:03d}", label, []) for i, label in enumerate(labels)]
    claims = extract_claims([(p.page_number, p.text) for p in pages])
    relations = infer_relations(labels, claims)
    reasoning = extract_reasoning(claims)
    return KnowledgeBook(
        book_id=bid,
        filename=path.name,
        concepts=concepts,
        claims=claims,
        relations=relations,
        questions=extract_questions(labels),
        insights=[],
        reasoning=[{
            "step_id": s.step_id, "kind": s.kind, "text": s.text,
            "page_number": s.page_number, "evidence": s.evidence
        } for s in reasoning],
    )

def build_library(input_dir: str | Path, output_dir: str | Path) -> dict:
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    books: list[KnowledgeBook] = []
    for pdf in sorted(input_dir.glob("*.pdf")):
        kb = analyze_pdf(pdf)
        books.append(kb)
        book_dir = output_dir / kb.book_id
        book_dir.mkdir(parents=True, exist_ok=True)
        (book_dir / "knowledge.json").write_text(json.dumps(kb.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        (book_dir / "reasoning.json").write_text(json.dumps({
            "summary": reasoning_summary([type("S", (), r)() for r in kb.reasoning]),
            "steps": kb.reasoning,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    synthesis = synthesize(books)
    index = {
        "books": [b.to_dict() for b in books],
        "graph": build_graph(books),
        "cross_book_links": cross_book_links(books),
        "synthesis": synthesis,
        "reasoning_engine": "v0.5",
    }
    (output_dir / "library_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return index

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="books")
    parser.add_argument("--output", default="data/library")
    args = parser.parse_args()
    result = build_library(args.input, args.output)
    print(json.dumps({
        "books": result["synthesis"]["book_count"],
        "cross_book_links": len(result["cross_book_links"]),
        "potential_contradictions": len(result["synthesis"]["potential_contradictions"]),
        "cross_book_claim_matches": len(result["synthesis"]["cross_book_claim_matches"]),
    }, indent=2))

if __name__ == "__main__":
    main()
