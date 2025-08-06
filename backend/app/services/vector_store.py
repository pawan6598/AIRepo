"""Vector store integration using FAISS."""
from __future__ import annotations

from typing import List, Tuple

import faiss
import numpy as np


class VectorStore:
    """Simple in-memory FAISS index wrapper."""

    def __init__(self, dimension: int) -> None:
        self.index = faiss.IndexFlatL2(dimension)
        self.vectors: list[Tuple[int, str]] = []

    def add(self, embeddings: List[List[float]], metadatas: List[str]) -> None:
        """Add embeddings with metadata."""
        arr = np.array(embeddings).astype("float32")
        self.index.add(arr)
        for i, meta in enumerate(metadatas):
            self.vectors.append((len(self.vectors) + i, meta))

    def search(self, query: List[float], k: int = 5) -> List[Tuple[str, float]]:
        """Search similar vectors."""
        q = np.array([query]).astype("float32")
        distances, indices = self.index.search(q, k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.vectors):
                results.append((self.vectors[idx][1], float(dist)))
        return results
