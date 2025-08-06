"""Document upload routes."""
from __future__ import annotations

from fastapi import APIRouter, UploadFile

from ...services.rag_chain import RAGChain
from ...core.logging import get_logger

router = APIRouter(prefix="/documents", tags=["documents"])
logger = get_logger(__name__)
chain = RAGChain()


@router.post("/upload")
async def upload(file: UploadFile) -> dict[str, str]:
    """Upload and ingest a document."""
    content = await file.read()
    text = content.decode("utf-8")
    chain.ingest(text, file.filename)
    logger.info("Document ingested", extra={"file": file.filename})
    return {"status": "ingested"}
