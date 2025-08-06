"""Embedding service using OpenAI API."""
from __future__ import annotations

from typing import List

import openai

from ..core.config import settings


class EmbeddingService:
    """Service for generating embeddings."""

    def __init__(self, model: str = "text-embedding-ada-002") -> None:
        openai.api_key = settings.openai_api_key
        self.model = model

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of texts."""
        response = openai.Embedding.create(input=texts, model=self.model)
        return [d["embedding"] for d in response["data"]]
