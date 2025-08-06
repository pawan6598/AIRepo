"""Semantic chunking using sentence embeddings."""
from __future__ import annotations

from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter


class ChunkingService:
    """Split documents into semantically coherent chunks."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def chunk(self, text: str) -> List[str]:
        """Chunk a single document into segments."""
        return self.splitter.split_text(text)
