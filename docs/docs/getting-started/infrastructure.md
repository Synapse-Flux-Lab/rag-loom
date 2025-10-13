---
id: infrastructure
title: Infrastructure
sidebar_position: 4
---

## Configuration Loading Order

`./utilscripts/quick_start.sh` simply activates the virtual environment and launches `uvicorn app.main:app`. Runtime configuration is resolved inside `app/core/config.py` using Pydantic Settings with `load_dotenv()`:

1. **Environment variables** present in the shell take highest priority.
2. Values from a project `.env` file (for example the one copied from `docs/static/files/env.example`) override code defaults.
3. If neither is provided, the hard-coded defaults in `Settings` are used.

This means the service will run with sensible defaults out of the box, but any value you place in `.env` or export before running the service immediately replaces the default without editing code.

## Environment Variables and Defaults

| Variable | Default | Purpose |
| --- | --- | --- |
| `PROJECT_NAME` | `RAG Loom API` | Branding for generated docs and metadata. |
| `VERSION` | `0.1.0` | API/version banner returned by `/` and `/health`. |
| `API_V1_STR` | `/api/v1` | Prefix for all routed endpoints. |
| `CHUNK_SIZE` | `1000` | Default characters per chunk during ingestion. |
| `CHUNK_OVERLAP` | `200` | Overlap between consecutive chunks. |
| `MAX_FILE_SIZE` | `10485760` | Maximum upload size (bytes). |
| `VECTOR_STORE_TYPE` | `chroma` | Vector backend (`chroma`, `qdrant`, or `redis`). |
| `CHROMA_PERSIST_DIRECTORY` | `./chroma_db` | Path for embedded Chroma database. |
| `QDRANT_URL` | `http://localhost:6333` | Remote Qdrant endpoint. |
| `QDRANT_API_KEY` | `None` | Auth token for secured Qdrant clusters. |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection string with RediSearch. |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Default embedding model identifier. |
| `EMBEDDING_DIM` | `384` | Dimensionality matching the embedding model. |
| `LLM_PROVIDER` | `ollama` | Active LLM adapter (`ollama`, `openai`, `cohere`, `huggingface`). |
| `OPENAI_API_KEY` | `None` | Required when `LLM_PROVIDER=openai`. |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | Default OpenAI chat model. |
| `COHERE_API_KEY` | `None` | Required when `LLM_PROVIDER=cohere`. |
| `COHERE_MODEL` | `command-xlarge` | Cohere generation model. |
| `HUGGINGFACE_API_KEY` | `None` | Required for private Hugging Face models. |
| `HUGGINGFACE_MODEL` | `google/flan-t5-large` | Transformers pipeline model. |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama daemon address. |
| `OLLAMA_MODEL` | `gemma2:2b` | Default Ollama model tag. |
| `OLLAMA_NUM_PARALLEL` | `2` | Concurrency hint for Ollama requests. |
| `TOP_K` | `5` | Default number of retrieval results. |
| `SIMILARITY_THRESHOLD` | `0.7` | Minimum similarity score before fallback. |
| `CORS_ORIGINS` | `["http://localhost:3000", "http://127.0.0.1:3000"]` | Allowed front-end origins. |
| `DATABASE_URL` | `sqlite:///./rag_platform.db` | Path to the SQLite metadata database. |
| `SERVICE_PORT` | `8000` | Port bound by Uvicorn. |
| `SERVICE_HOST` | `0.0.0.0` | Listen address (0.0.0.0 to expose externally). |
| `LOG_LEVEL` | `INFO` | Log verbosity for FastAPI/uvicorn. |
| `DEBUG` | `False` | Enable additional debug features. |
| `RELOAD` | `False` | Uvicorn auto-reload flag (set `True` for local dev). |
| `WORKER_PROCESSES` | `4` | Number of Uvicorn worker processes. |
| `MAX_CONCURRENT_REQUESTS` | `100` | Back-pressure guard for FastAPI. |
| `REQUEST_TIMEOUT` | `300` | Maximum request processing time in seconds. |
| `ENABLE_AUTH` | `False` | Toggle authentication middleware. |
| `SECRET_KEY` | `your_production_secret_key_here` | Signing key used when auth is enabled. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token lifetime for auth flows. |
| `ENABLE_METRICS` | `True` | Expose Prometheus `/metrics` endpoint. |
| `ENABLE_TRACING` | `False` | Hook for tracing integrations. |
| `UPLOAD_DIR` | `./uploads` | Temporary storage for incoming files. |
| `PROCESSED_DIR` | `./processed` | Location for processed document artifacts. |
| `CACHE_DIR` | `./cache` | General cache directory. |
| `LOGS_DIR` | `./logs` | Directory for runtime logs. |

> Tip: copy `docs/static/files/env.example` to `.env` and adjust only the values you need. Everything else will automatically fall back to the defaults above.

## Production Environment Template

The repository ships with `env.production` at the project root as a ready-made template for hardened deployments. It pins sensible production choices—such as `VECTOR_STORE_TYPE=qdrant`, the Ollama provider defaults, and conservative worker limits. To adopt it:

1. Duplicate the file (`cp env.production .env`) and populate any empty secrets such as `QDRANT_API_KEY` or OAuth tokens.
2. Adjust values that depend on your hosting (for example `QDRANT_URL`, `REDIS_URL`, or `CORS_ORIGINS`).
3. Restart the service; `Settings` in `app/core/config.py` will ingest the overrides automatically.

Every key in `env.production` maps directly to an attribute in `Settings`. The defaults shown above originate from `app/core/config.py`, so you can verify behaviour or introduce new configuration flags in a single place while keeping documentation in sync.

## Local Infrastructure via Docker Compose

For local development the repository includes `docker-compose.infra.yml`, which provisions Qdrant and Ollama (pre-configured with the `gemma2:2b` model). The helper script `./utilscripts/dev-infra.sh` orchestrates the workflow:

```bash
./utilscripts/dev-infra.sh up       # copy env.production -> .env, pull images, start services, preload Gemma 2B
./utilscripts/dev-infra.sh status   # inspect container state
./utilscripts/dev-infra.sh logs     # tail logs from both services
./utilscripts/dev-infra.sh down     # stop and remove the containers
```

The script performs the following steps:

- Copies `env.production` to `.env` (creating it if necessary) and enforces the Ollama/Qdrant connection parameters expected by the FastAPI service.
- Ensures the required Docker images are downloaded, then calls `docker compose -f docker-compose.infra.yml up -d`.
- Waits for the Qdrant (`http://localhost:6333/health`) and Ollama (`http://localhost:11434/api/tags`) endpoints to respond.
- Downloads the `gemma2:2b` model via Ollama's REST API (blocking until complete) so subsequent requests succeed immediately.

After the script reports success, you can launch the API (`./utilscripts/quick_start.sh start`) or run tests—the `.env` file now points at the containerised services.
