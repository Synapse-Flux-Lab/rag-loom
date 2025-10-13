---
id: rest-api
title: REST API Reference
sidebar_position: 1
---

RAG Loom exposes a REST API for document ingestion, semantic search, and answer generation. All endpoints are prefixed with `/api/v1` unless noted otherwise.

- **Base URL (local)**: `http://localhost:8000`
- **OpenAPI documentation**: `GET /docs`

## Health

### `GET /health`

Returns service status and dependency diagnostics.

```json
{
  "status": "healthy",
  "vector_store": "chroma",
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "llm_provider": "ollama",
  "timestamp": "2024-03-01T10:15:00Z"
}
```

## Ingestion

### `POST /api/v1/ingest`

Uploads a single document for processing and indexing.

**Request** (multipart form):

- `file`: binary file (`pdf`, `txt`, etc.)
- `chunk_params` (optional JSON): overrides default chunk size and overlap.

**Response**:

```json
{
  "document_id": "doc_123",
  "chunks_processed": 12,
  "status": "indexed"
}
```

### `POST /api/v1/ingest/batch`

Accepts a batch of documents. Payload is the same as the single ingest endpoint, repeated per file.

## Search

### `POST /api/v1/search`

Performs a semantic similarity search across ingested content.

**Request**:

```json
{
  "query": "Summarise the data ingestion pipeline",
  "top_k": 5,
  "similarity_threshold": 0.7
}
```

**Response**:

```json
{
  "results": [
    {
      "chunk_id": "chunk_42",
      "content": "The ingestion pipeline extracts text...",
      "score": 0.83,
      "metadata": {
        "document_id": "doc_123",
        "source": "deployment_guide.pdf"
      }
    }
  ]
}
```

## Generation

### `POST /api/v1/generate`

Combines retrieval and language model inference to produce an answer.

**Request**:

```json
{
  "query": "How do I deploy RAG Loom to production?",
  "search_params": {
    "top_k": 5,
    "similarity_threshold": 0.7
  },
  "temperature": 0.7,
  "max_tokens": 500
}
```

**Response**:

```json
{
  "answer": "To deploy RAG Loom...",
  "sources": [
    {
      "document_id": "doc_123",
      "chunk_id": "chunk_91",
      "excerpt": "For production deployments..."
    }
  ],
  "metadata": {
    "provider": "ollama",
    "generation_time_ms": 1432,
    "token_usage": {
      "prompt": 950,
      "completion": 320
    }
  }
}
```

## Errors

API responses follow standard FastAPI error formats. Handle the following status codes:

| Status | Meaning |
| --- | --- |
| `400` | Invalid payload or missing required fields |
| `401` | Authentication failed (when `ENABLE_AUTH=true`) |
| `404` | Requested resource not found |
| `422` | Validation error |
| `500` | Unexpected server error |

## Testing Endpoints

Use the bundled `test_service.py` or quick curl commands:

```bash
pytest test_service.py

curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "What models are supported?", "top_k": 3}'
```

For SDK or client library integration, see [Client Recipes](./client-recipes).
