---
id: ollama
title: Ollama Integration
sidebar_position: 1
---

Ollama enables high-quality language models to run locally without third-party API calls. This guide explains how to install Ollama, connect it to RAG Loom, and optimise performance.

## When to Use Ollama

- Offline inference or strict data residency requirements.
- Avoiding per-token API charges from hosted providers.
- Rapid experimentation with community-maintained models before promoting to production.

If you prefer hosted providers, configure the relevant environment variables for OpenAI, Cohere, or Hugging Face instead.

## System Requirements

| Tier | CPU | Memory | Storage | Notes |
| --- | --- | --- | --- | --- |
| Development | 4 cores | 16 GB | 20 GB | Suitable for 7B models |
| Staging | 8 cores | 32 GB | 50 GB | Recommended for 13B models |
| Production | 16 cores | 64 GB | 100 GB SSD | Supports 34B+ models; consider dedicated hardware |

Apple Silicon (M1/M2) or GPU-backed Linux servers deliver the best throughput.

## Installation

### macOS (Homebrew)

```bash
brew install ollama
brew services start ollama
ollama --version
```

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
```

### Docker

```bash
docker run -d --name ollama \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama:latest
```

## Model Management

```bash
# List installed models
ollama list

# Download recommended options
ollama pull mistral:7b
ollama pull llama2:13b

# Remove unused models
ollama rm llama2:70b
```

Create custom variants with a `Modelfile`:

```bash
cat <<'FILE' > Modelfile
FROM mistral:7b
PARAMETER temperature 0.6
PARAMETER top_p 0.9
SYSTEM "You are a retrieval-augmented assistant. Cite sources when available."
FILE

ollama create rag-assistant -f Modelfile
```

## Configuring RAG Loom

Update `.env` to point to the Ollama runtime:

```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=rag-assistant
VECTOR_STORE_TYPE=chroma
```

Within Docker Compose, ensure the services can communicate:

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

  rag-service:
    build: .
    environment:
      - LLM_PROVIDER=ollama
      - OLLAMA_BASE_URL=http://ollama:11434
      - OLLAMA_MODEL=rag-assistant
    depends_on:
      - ollama
```

Install the Python client only if your application code calls Ollama directly:

```bash
pip install ollama
```

## Verification

```bash
# Confirm Ollama responds
ollama run mistral:7b "Summarise RAG Loom in two sentences."

# Validate the FastAPI integration
curl http://localhost:8000/health
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "List the deployment steps",
    "search_params": {"top_k": 3}
  }'
```

## Performance Tuning

- Set concurrency: `export OLLAMA_NUM_PARALLEL=2`.
- Optimise chunk size and overlap to limit prompt length.
- Use SSD storage so large models load quickly.
- Combine with the [Scaling guide](../operations/scaling) when running multiple instances.

Model selection quick reference:

| Model | RAM | Recommended Use |
| --- | --- | --- |
| `mistral:7b` | 8–10 GB | Fast development iteration |
| `llama2:13b` | 16–20 GB | Balanced accuracy and speed |
| `codellama:34b` | 32 GB+ | Code-centric knowledge bases |

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| `connection refused` | Ensure the service is running (`ps aux | grep ollama`) and port 11434 is available |
| Model download stalls | Retry `ollama pull`, check connectivity, or switch mirrors |
| High memory usage | Switch to a smaller model or decrease `OLLAMA_NUM_PARALLEL` |
| Slow inference | Reduce temperature/top-p, upgrade hardware, or lower concurrent requests |

Restart the runtime with `brew services restart ollama` (macOS) or `docker compose restart ollama` on Linux.

## Security Notes

- Restrict port 11434 to trusted networks or bind to localhost.
- Keep the Ollama binary and models up to date.
- Snapshot downloaded models regularly so you can roll back when needed.

Once Ollama is configured, monitor its health alongside other services using the observability tooling covered in the [Operations guides](../operations/scaling).
