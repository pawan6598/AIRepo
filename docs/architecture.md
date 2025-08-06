# Architecture

```mermaid
graph TD
  A[Client] -->|HTTP| B[API Gateway]
  B --> C[Auth Service]
  B --> D[RAG Service]
  D --> E[Vector Store]
  D --> F[MongoDB]
  D --> G[OpenAI]
```

## Microservices

- **Auth Service**: Handles JWT issuance and validation.
- **RAG Service**: Exposes endpoints for document ingestion and querying.
- **Vector Store**: FAISS index for embeddings.
- **Database**: MongoDB storing document metadata.

