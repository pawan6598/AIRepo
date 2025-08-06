"""RAG interaction routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ...services.rag_chain import RAGChain
from ...core.logging import get_logger

router = APIRouter(prefix="/rag", tags=["rag"])
logger = get_logger(__name__)


def get_chain() -> RAGChain:
    """Dependency injection for RAGChain."""
    return RAGChain()


@router.post("/ask")
async def ask(question: str, chain: RAGChain = Depends(get_chain)) -> dict[str, str]:
    """Ask a question using RAG chain."""
    logger.info("Question received", extra={"question": question})
    answer = chain.ask(question)
    return {"answer": answer}
