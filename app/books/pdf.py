from __future__ import annotations
from pathlib import Path
from pypdf import PdfReader
from .models import Page

def extract_pages(path: str | Path) -> list[Page]:
    reader = PdfReader(str(path))
    pages: list[Page] = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").replace("\x00", " ").strip()
        pages.append(Page(i, text))
    return pages
