"""Main FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api.v1.endpoints import auth, rag, documents
from .core.logging import configure_logging, get_logger
from .core.exceptions import ApplicationError

configure_logging()
logger = get_logger(__name__)

app = FastAPI(title="RAG Service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(rag.router)


@app.exception_handler(ApplicationError)
async def app_exception_handler(_, exc: ApplicationError) -> JSONResponse:
    """Handle application errors uniformly."""
    logger.error("Application error", exc_info=exc)
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
