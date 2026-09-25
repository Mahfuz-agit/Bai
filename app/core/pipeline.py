from __future__ import annotations
from app.knowledge.pipeline import build_library

def run(input_dir: str = "books", output_dir: str = "data/library"):
    return build_library(input_dir, output_dir)
