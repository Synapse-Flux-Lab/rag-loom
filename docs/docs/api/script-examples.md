---
id: script-examples
title: API Script Playbook
sidebar_position: 2
---

Practical, copy-ready scripts for every RAG Loom endpoint. Each section starts with a shell example (powered by `curl`) followed by an equivalent Python snippet so you can pick the workflow that best fits your toolkit.

## Before You Start

- Examples assume the service is running at `http://localhost:8000`; update the URLs directly if your deployment differs.
- Install [`jq`](https://stedolan.github.io/jq/) if you want pretty JSON in the shell examples.
- Python snippets expect `requests` (`pip install requests`).

## Shell Scripts (curl)

### Service Banner — `GET /`

Confirms the API is running and returns the banner message and version.

```bash
curl -s "http://localhost:8000/" | jq
```

Sample response:

```json
{
  "message": "RAG Microservice API",
  "version": "0.2.0"
}
```

### Health Check — `GET /health`

Fetches dependency status for the vector store, embedding model, and LLM provider. Ideal for readiness probes.

```bash
curl -s "http://localhost:8000/health" | jq
```

Sample response:

```json
{
  "status": "healthy",
  "timestamp": "2024-03-01T10:15:00.123456+00:00",
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

### Single Document Ingest — `POST /api/v1/ingest`

Uploads a single PDF or TXT file, chunks it, generates embeddings, and stores the result in the configured vector store.

```bash
curl -s -X POST "http://localhost:8000/api/v1/ingest" \
  -H "accept: application/json" \
  -F "file=@./data/sample.txt" \
  | jq
```

with Chunk params:

```bash
curl -s -X POST "http://localhost:8000/api/v1/ingest" \
  -H "accept: application/json" \
  -F "file=@./data/sample.txt" \
  -F 'chunk_params={"chunk_size": 1000, "chunk_overlap": 200}' \
  | jq
```

Sample response:

```json
{
  "message": "Document processed successfully",
  "file_id": "sample.txt",
  "file_name": "sample.txt",
  "file_type": "txt",
  "chunks_created": 12,
  "processing_time": 1.42,
  "metadata": {
    "document_id": "a4bf2c30-23f1-40cc-8d40-9b8c8338ff49"
  }
}
```

### Batch Ingest — `POST /api/v1/ingest/batch`

Sends multiple files in one request. Each file is processed independently and persists its chunks to the vector store.

```bash
curl -s -X POST "http://localhost:8000/api/v1/ingest/batch" \
  -F "files=@./data/notes.txt" \
  -F "files=@./data/guide.pdf" \
  | jq
```

with chunk params

```bash
curl -s -X POST "http://localhost:8000/api/v1/ingest/batch" \
  -F "files=@./data/notes.txt" \
  -F "files=@./data/guide.pdf" \
  -F 'chunk_params={"chunk_size": 1200, "chunk_overlap": 150}' \
  | jq
```

Sample response:

```json
[
  {
    "message": "Document processed successfully",
    "file_id": "notes.txt",
    "file_name": "notes.txt",
    "file_type": "txt",
    "chunks_created": 9,
    "processing_time": 1.8
  },
  {
    "message": "Document processed successfully",
    "file_id": "guide.pdf",
    "file_name": "guide.pdf",
    "file_type": "pdf",
    "chunks_created": 18,
    "processing_time": 2.4
  }
]
```

### Semantic Search — `POST /api/v1/search`

Queries the vector store for the most relevant document chunks.

```bash
curl -s -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Summarise the data ingestion pipeline",
    "top_k": 5,
    "similarity_threshold": 0.7
  }' | jq
```

Sample response:

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

### Answer Generation — `POST /api/v1/generate`

Combines retrieval with LLM generation to craft an answer plus supporting sources.

```bash
curl -s -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I deploy RAG Loom to production?",
    "search_params": {
      "top_k": 5,
      "similarity_threshold": 0.7
    },
    "temperature": 0.7,
    "max_tokens": 500
  }' | jq
```

Sample response:

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

## Python Scripts (requests)

### Service Banner — `GET /`

```python
import requests

BASE_URL = "http://localhost:8000"

def fetch_banner() -> None:
    """Print the service banner and version."""
    response = requests.get(f"{BASE_URL}/", timeout=10)
    response.raise_for_status()
    print(response.json())

if __name__ == "__main__":
    fetch_banner()
```

Sample output:

```json
{"message": "RAG Microservice API", "version": "0.2.0"}
```

### Health Check — `GET /health`

```python
import requests

BASE_URL = "http://localhost:8000"

def verify_dependencies() -> None:
    """Display component status for vector store, embedding model, and LLM."""
    response = requests.get(f"{BASE_URL}/health", timeout=15)
    response.raise_for_status()
    print(response.json())

if __name__ == "__main__":
    verify_dependencies()
```

Expected JSON mirrors the shell example above.

### Single Document Ingest — `POST /api/v1/ingest`

```python
import os
import requests

BASE_URL = "http://localhost:8000"
DOCUMENT_PATH = "./data/sample.txt"

def ingest_single() -> None:
    """Upload one document and print the ingestion summary."""
    with open(DOCUMENT_PATH, "rb") as fh:
        files = {"file": (os.path.basename(DOCUMENT_PATH), fh, "text/plain")}
        data = {"chunk_params": '{"chunk_size": 1000, "chunk_overlap": 200}'}
        response = requests.post(
            f"{BASE_URL}/api/v1/ingest",
            files=files,
            data=data,
            timeout=60,
        )
    response.raise_for_status()
    print(response.json())

if __name__ == "__main__":
    ingest_single()
```

### Batch Ingest — `POST /api/v1/ingest/batch`

```python
import os
import requests

BASE_URL = "http://localhost:8000"
FILE_PATHS = ["./data/notes.txt", "./data/guide.pdf"]

def ingest_batch() -> None:
    """Upload multiple documents and print per-file results."""
    file_payload = []
    file_handles = []
    for path in FILE_PATHS:
        fh = open(path, "rb")
        file_handles.append(fh)
        file_payload.append(("files", (os.path.basename(path), fh)))

    try:
        data = {"chunk_params": '{"chunk_size": 1200, "chunk_overlap": 150}'}
        response = requests.post(
            f"{BASE_URL}/api/v1/ingest/batch",
            files=file_payload,
            data=data,
            timeout=120,
        )
        response.raise_for_status()
        print(response.json())
    finally:
        for fh in file_handles:
            fh.close()

if __name__ == "__main__":
    ingest_batch()
```

### Semantic Search — `POST /api/v1/search`

```python
import requests

BASE_URL = "http://localhost:8000"

def search_chunks() -> None:
    """Query the vector index for relevant passages."""
    payload = {
        "query": "Summarise the data ingestion pipeline",
        "top_k": 5,
        "similarity_threshold": 0.7,
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/search",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    print(response.json())

if __name__ == "__main__":
    search_chunks()
```

### Answer Generation — `POST /api/v1/generate`

```python
import requests

BASE_URL = "http://localhost:8000"

def generate_answer() -> None:
    """Run retrieval + generation and print the answer with supporting sources."""
    payload = {
        "query": "How do I deploy RAG Loom to production?",
        "search_params": {
            "top_k": 5,
            "similarity_threshold": 0.7,
        },
        "temperature": 0.7,
        "max_tokens": 500,
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/generate",
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    print(response.json())

if __name__ == "__main__":
    generate_answer()
```

Running each script will yield the same JSON structures shown in the shell section. Swap out file paths, parameters, or prompt settings to tailor the calls to your environment.
