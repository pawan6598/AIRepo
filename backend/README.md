# Backend Service

## Overview
FastAPI-based microservice implementing Retrieval-Augmented Generation.

## Modules

- `core`: configuration, logging, security, exceptions.
- `api/v1/endpoints`: REST endpoints for authentication, document ingestion, and querying.
- `services`: embedding, vector store, semantic chunking, database access, RAG chain.
- `tests`: unit and integration tests.

## API Specification

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/token` | POST | Obtain JWT token. |
| `/documents/upload` | POST | Upload and ingest document. |
| `/rag/ask` | POST | Query documents using RAG. |
| `/health` | GET | Service health check. |

## External Dependencies

- OpenAI API for embeddings and language model.
- FAISS for vector similarity search.
- MongoDB for metadata storage.

## Running Locally

```bash
uvicorn app.main:app --reload
```
