"""RAG chain orchestration using LangChain."""
from __future__ import annotations

from typing import List

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

from .embedding import EmbeddingService
from .vector_store import VectorStore
from .chunking import ChunkingService


class RAGChain:
    """High-level RAG chain combining chunking, embeddings and vector search."""

    def __init__(self, vector_dim: int = 1536) -> None:
        self.chunker = ChunkingService()
        self.embedder = EmbeddingService()
        self.store = VectorStore(vector_dim)
        self.llm = OpenAI(temperature=0)
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="stuff", retriever=self.store, return_source_documents=True
        )

    def ingest(self, text: str, metadata: str) -> None:
        """Ingest a document into the vector store."""
        chunks = self.chunker.chunk(text)
        embeddings = self.embedder.embed(chunks)
        self.store.add(embeddings, [metadata] * len(chunks))

    def ask(self, question: str) -> str:
        """Query the chain."""
        return self.chain.run(question)
