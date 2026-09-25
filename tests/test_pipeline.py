from app.knowledge.pipeline import build_library

def test_build_empty_library(tmp_path):
    out = tmp_path / "out"
    result = build_library(tmp_path, out)
    assert result["synthesis"]["book_count"] == 0
    assert (out / "library_index.json").exists()
