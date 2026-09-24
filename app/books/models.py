from __future__ import annotations

from pydantic import BaseModel, Field


class PageRecord(BaseModel):
    page_number: int = Field(ge=1)
    text: str
    char_count: int = Field(ge=0)


class BookRecord(BaseModel):
    book_id: str
    path: str
    title: str | None = None
    author: str | None = None
    subject: str | None = None
    producer: str | None = None
    page_count: int = Field(ge=0)
    extracted_characters: int = Field(ge=0)
    extraction_mode: str
    likely_scanned: bool
    pages_with_text: int = Field(ge=0)


class ChunkRecord(BaseModel):
    chunk_id: str
    book_id: str
    page_start: int
    page_end: int
    text: str
    char_count: int = Field(ge=0)
