---
id: quickstart
title: Quick Start
sidebar_position: 2
---

Follow this sequence to launch RAG Loom locally in minutes. It assumes you have completed the [Prerequisites & Environment Setup](./requirements).

## Option A — Guided Script

The `utilscripts/quick_start.sh` helper orchestrates dependency installation, service start-up, and verification.

```bash
# Ensure the script is executable
chmod +x utilscripts/quick_start.sh

# Install dependencies, prepare the environment, and run smoke checks
./utilscripts/quick_start.sh setup

# Start the FastAPI service with sensible defaults
./utilscripts/quick_start.sh start
```

Common subcommands:

| Command | Description |
| --- | --- |
| `./utilscripts/quick_start.sh status` | Report service status and essential diagnostics |
| `./utilscripts/quick_start.sh logs` | Tail application logs |
| `./utilscripts/quick_start.sh test` | Run the Python test suite |
| `./utilscripts/quick_start.sh clean` | Stop services and remove temporary assets |

## Option B — Manual Steps

1. **Ensure your Python environment is active** (see [Prerequisites](./requirements)).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy and configure environment variables:
   ```bash
   cp docs/static/files/env.example .env
   # update .env with provider credentials and vector store settings
   ```
4. Start the API in development mode:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Verifying the Installation

Once the server is running, validate the stack.

```bash
# Health probe
curl http://localhost:8000/health

# Upload a sample document (replace path with your file)
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.pdf"

# Perform a semantic search
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Summarise the architecture",
    "top_k": 3,
    "similarity_threshold": 0.65
  }'
```

Expect a `200` response from the health check, successful ingestion confirmation, and JSON search results containing relevant passages.

## Running the Test Suite

Smoke tests ensure the deployment is wired correctly:

```bash
pytest test_service.py          # API smoke tests
pytest                          # Full suite
```

For continuous integration, add `pytest --maxfail=1 --disable-warnings` to fail early on regressions.

## Useful Endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Service availability, vector store, and provider diagnostics |
| `GET /docs` | Interactive OpenAPI schema |
| `POST /api/v1/ingest` | Upload content for indexing |
| `POST /api/v1/search` | Semantic search across indexed documents |
| `POST /api/v1/generate` | Retrieve + generate answers using the configured LLM |

Continue to [Project Structure](./structure) for an annotated map of the codebase, or jump ahead to the [REST API reference](../api/rest-api) when you are ready to integrate clients.
