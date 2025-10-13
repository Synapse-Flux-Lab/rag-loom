---
id: rest-api
title: REST API Reference
sidebar_position: 1
---

RAG Loom exposes a REST API for document ingestion, semantic search, and answer generation. All endpoints are prefixed with `/api/v1` unless noted otherwise.

- **Base URL (local)**: `http://localhost:8000`
- **OpenAPI documentation**: `GET /docs`
- **Prometheus metrics**: `GET /metrics`

## Service Health

### `GET /`

Returns a lightweight banner confirming the service is running.

```json
{
  "message": "RAG Microservice API",
  "version": "0.1.0"
}
```

### `GET /health`

Returns service status and dependency diagnostics.

```json
{
  "status": "healthy",
  "timestamp": "2024-03-01T10:15:00.123456+00:00",
  "service": "RAG Loom API",
  "version": "0.1.0",
  "vector_store": {
    "status": "up",
    "type": "chroma"
  },
  "embedding": {
    "status": "up",
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "provider": "local"
  },
  "llm": {
    "status": "up",
    "provider": "ollama",
    "model": "gemma2:2b"
  }
}
```

If any dependency test fails, the top-level `status` is set to `degraded` and the impacted subsystem reports `"status": "down"` along with an error message.

## Ingestion API

### `POST /api/v1/ingest`

Uploads a single document for processing and indexing.

**Request** (multipart form):

- `file`: binary file (`pdf` or `txt`)
- `chunk_params` (optional JSON): `{ "chunk_size": 1000, "chunk_overlap": 200 }`

**Response** (`200 OK`):

```json
{
  "message": "Document processed successfully",
  "file_id": "playbook.pdf",
  "file_name": "playbook.pdf",
  "file_type": "pdf",
  "chunks_created": 12,
  "processing_time": 1.42,
  "metadata": {
    "document_id": "a4bf2c30-23f1-40cc-8d40-9b8c8338ff49"
  }
}
```

> Maximum upload size is governed by `MAX_FILE_SIZE` in `.env`.

### `POST /api/v1/ingest/batch`

Accepts multiple files in a single multipart request. Each file is processed independently and returns an array of per-file ingestion results.

**Request** (multipart form):

- `files`: repeatable binary field for each document (`pdf` or `txt`)
- `chunk_params` (optional JSON string): `{ "chunk_size": 1000, "chunk_overlap": 200 }`

Each uploaded file is chunked, embedded, and stored in the configured vector store in the same way as the single-file endpoint.

**Response** (`200 OK`):

```json
[
  {
    "message": "Document processed successfully",
    "file_id": "handbook.pdf",
    "file_name": "handbook.pdf",
    "file_type": "pdf",
    "chunks_created": 18,
    "processing_time": 2.11
  },
  {
    "message": "Failed to process notes.txt",
    "file_id": "notes.txt",
    "file_name": "notes.txt",
    "file_type": "unknown",
    "chunks_created": 0,
    "processing_time": 0.0
  }
]
```

## Search

### `POST /api/v1/search`

Performs a semantic similarity search across ingested content.

**Request**:

```json
{
  "query": "Summarise the data ingestion pipeline",
  "top_k": 5,
  "similarity_threshold": 0.7,
  "filters": {
    "file_name": "handbook.pdf"
  }
}
```

**Response** (`200 OK`):

```json
[
  {
    "id": "cb8b0dd5-7a49-4a75-a705-6fe2f3fc51fa",
    "content": "The ingestion pipeline extracts text...",
    "metadata": {
      "document_id": "21f5329e-86c7-42b0-938a-4c815b635f2c",
      "file_name": "handbook.pdf",
      "chunk_index": 3
    },
    "similarity_score": 0.83,
    "document_id": "21f5329e-86c7-42b0-938a-4c815b635f2c"
  }
]
```

Results are filtered by `similarity_threshold`. If no chunks meet the threshold, the top `top_k` results are returned as a fallback.

## Generation

### `POST /api/v1/generate`

Combines retrieval and language model inference to produce an answer.

**Request**:

```json
{
  "query": "How do I deploy RAG Loom to production?",
  "search_params": {
    "top_k": 5,
    "similarity_threshold": 0.7,
    "filters": {
      "document_id": "21f5329e-86c7-42b0-938a-4c815b635f2c"
    }
  },
  "temperature": 0.7,
  "max_tokens": 500
}
```

**Response** (`200 OK`):

```json
{
  "answer": "To deploy RAG Loom...",
  "sources": [
    {
      "id": "cb8b0dd5-7a49-4a75-a705-6fe2f3fc51fa",
      "content": "For production deployments...",
      "metadata": {
        "document_id": "21f5329e-86c7-42b0-938a-4c815b635f2c",
        "file_name": "deployment_guide.pdf",
        "chunk_index": 9
      },
      "similarity_score": 0.82,
      "document_id": "21f5329e-86c7-42b0-938a-4c815b635f2c"
    }
  ],
  "generation_time": 1.86
}
```

If the request omits `context`, the service automatically retrieves context using the provided `search_params` or defaults from configuration.

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

For SDK integrations, explore the ready-made snippets in the [API Script Playbook](./script-examples).
