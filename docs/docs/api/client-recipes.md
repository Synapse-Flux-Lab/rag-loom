---
id: client-recipes
title: Client Recipes
sidebar_position: 2
---

This page provides ready-made examples for interacting with RAG Loom using curl and Python. Adapt them to your environment by updating hostnames, credentials, and file paths.

## Curl Examples

### Build & Run with Docker

```bash
docker build -t rag-loom .
docker run -p 8000:8000 rag-loom
```

### Upload a Document

```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F 'chunk_params={"chunk_size": 1000, "chunk_overlap": 200}'
```

### Search Indexed Content

```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Describe the deployment process",
    "top_k": 5,
    "similarity_threshold": 0.7
  }'
```

### Generate an Answer

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I scale the service?",
    "search_params": {
      "top_k": 5,
      "similarity_threshold": 0.7
    },
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

## Python Example

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

def health():
    response = requests.get("http://localhost:8000/health", timeout=10)
    response.raise_for_status()
    return response.json()

def ingest(path: str):
    with open(path, "rb") as f:
        files = {"file": (path, f, "application/pdf")}
        resp = requests.post(f"{BASE_URL}/ingest", files=files, timeout=30)
    resp.raise_for_status()
    return resp.json()

def search(query: str):
    payload = {"query": query, "top_k": 3, "similarity_threshold": 0.7}
    resp = requests.post(f"{BASE_URL}/search", json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()

def generate(query: str):
    payload = {
        "query": query,
        "search_params": {"top_k": 5, "similarity_threshold": 0.7},
        "temperature": 0.6,
        "max_tokens": 400,
    }
    resp = requests.post(f"{BASE_URL}/generate", json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()
```

## Tips

- Batch ingestion saves round trips; refer to [`POST /api/v1/ingest/batch`](./rest-api#post-apiv1ingestbatch).
- Include metadata (titles, tags) in ingestion payloads to improve retrieval filters.
- Use exponential backoff when interacting with hosted providers that enforce rate limits.

Continue to [REST API Reference](./rest-api) for full endpoint details or [Production Deployment](../operations/deployment) once you begin integrating in staging environments.
