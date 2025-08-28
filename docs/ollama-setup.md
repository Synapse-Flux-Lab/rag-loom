# Ollama Local Setup Guide for RAG Platform Kit

This guide explains how to install and configure Ollama locally on macOS to run large language models (LLMs) without external API costs for your RAG service.

## Table of Contents

- [What is Ollama?](#what-is-ollama)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Model Management](#model-management)
- [Integration with RAG Service](#integration-with-rag-service)
- [Configuration](#configuration)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Performance Optimization](#performance-optimization)

## What is Ollama?

**Ollama** is an open-source tool that allows you to run large language models locally on your machine. It's perfect for RAG development because:

- ✅ **Completely Free** - No API costs or rate limits
- ✅ **Privacy** - All data stays on your machine
- ✅ **Offline** - Works without internet connection
- ✅ **Customizable** - Run various open-source models
- ✅ **Fast** - Local inference with no network latency

## System Requirements

### Minimum Requirements:
- **macOS**: 10.15 (Catalina) or later
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space for models
- **Architecture**: Intel (x86_64) or Apple Silicon (M1/M2)

### Recommended Requirements:
- **RAM**: 32GB or more
- **Storage**: 50GB+ free space
- **GPU**: Apple Silicon M1/M2 (for better performance)

## Installation

### Method 1: Official Installer (Recommended)

1. **Download Ollama**:
   ```bash
   # Visit the official website
   open https://ollama.ai/download
   ```

2. **Install the .dmg file**:
   - Download the macOS .dmg file
   - Double-click to mount
   - Drag Ollama to Applications folder
   - Launch Ollama from Applications

3. **Verify Installation**:
   ```bash
   # Check if Ollama is running
   ollama --version
   
   # Expected output: ollama version 0.1.x
   ```

### Method 2: Homebrew Installation

```bash
# Install via Homebrew
brew install ollama

# Start Ollama service
brew services start ollama
```

### Method 3: Manual Installation

```bash
# Download and install manually
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve
```

## Model Management

### Downloading Models

Ollama provides access to various open-source models. Here are recommended models for RAG:

#### **Small Models (Fast, Good for Development):**
```bash
# Llama 2 7B - Good balance of speed and quality
ollama pull llama2:7b

# Mistral 7B - Excellent performance for RAG
ollama pull mistral:7b

# Code Llama 7B - Good for technical documents
ollama pull codellama:7b
```

#### **Medium Models (Better Quality, Slower):**
```bash
# Llama 2 13B - Better quality, slower inference
ollama pull llama2:13b

# Mistral 7B Instruct - Optimized for instructions
ollama pull mistral:7b-instruct
```

#### **Large Models (Best Quality, Slowest):**
```bash
# Llama 2 70B - Best quality, requires more RAM
ollama pull llama2:70b

# Code Llama 34B - Excellent for technical content
ollama pull codellama:34b
```

### Managing Models

```bash
# List installed models
ollama list

# Remove a model
ollama rm llama2:70b

# Show model information
ollama show llama2:7b
```

## Integration with RAG Service

### 1. Update Configuration

Update your `.env` file to use Ollama:

```bash:.env
# LLM Provider Configuration
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2:7b

# Vector Store Configuration
VECTOR_STORE_TYPE=chroma
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Service Configuration
SERVICE_PORT=8000
SERVICE_HOST=0.0.0.0
LOG_LEVEL=INFO
```

### 2. Update Docker Compose

```yaml:docker-compose.yml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    restart: unless-stopped

  rag-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LLM_PROVIDER=ollama
      - OLLAMA_BASE_URL=http://ollama:11434
      - OLLAMA_MODEL=llama2:7b
      - VECTOR_STORE_TYPE=chroma
    volumes:
      - ./chroma_db:/app/chroma_db
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

### 3. Update Requirements

Add Ollama client to your `requirements.txt`:

```txt:requirements.txt
# ... existing requirements ...
ollama==0.1.7  # Ollama Python client
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LLM_PROVIDER` | LLM provider type | `ollama` | Yes |
| `OLLAMA_BASE_URL` | Ollama service URL | `http://localhost:11434` | Yes |
| `OLLAMA_MODEL` | Model to use | `llama2:7b` | Yes |

### Model Configuration

You can customize model behavior by creating a `Modelfile`:

```bash
# Create a custom model configuration
cat > Modelfile << EOF
FROM llama2:7b
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
SYSTEM "You are a helpful AI assistant for RAG (Retrieval-Augmented Generation) tasks."
EOF

# Create custom model
ollama create rag-assistant -f Modelfile

# Use custom model
export OLLAMA_MODEL=rag-assistant
```

## Testing

### 1. Test Ollama Installation

```bash
# Test basic functionality
ollama run llama2:7b "Hello, how are you?"

# Test with a simple prompt
ollama run llama2:7b "Explain what RAG means in AI"
```

### 2. Test RAG Service Integration

```bash
# Start the service
./utilscripts/quick_start.sh start

# Test health endpoint
curl http://localhost:8000/health

# Test generation endpoint
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is RAG?",
    "context": []
  }'
```

### 3. Test Document Processing

```bash
# Upload a test document
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -F "file=@test_document.txt"

# Search documents
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

## Troubleshooting

### Common Issues

#### **1. Ollama Not Starting**
```bash
# Check if Ollama is running
ps aux | grep ollama

# Restart Ollama
brew services restart ollama
# or
ollama serve
```

#### **2. Model Download Issues**
```bash
# Check available models
ollama list

# Remove corrupted model
ollama rm model_name

# Re-download model
ollama pull model_name
```

#### **3. Memory Issues**
```bash
# Check available RAM
top -l 1 | grep PhysMem

# Use smaller model
export OLLAMA_MODEL=llama2:7b
```

#### **4. Port Conflicts**
```bash
# Check if port 11434 is in use
lsof -i:11434

# Kill conflicting process
sudo lsof -ti:11434 | xargs sudo kill -9
```

### Performance Issues

#### **Slow Inference**
- Use smaller models (7B instead of 13B/70B)
- Ensure sufficient RAM (16GB+ recommended)
- Close other applications to free memory

#### **High Memory Usage**
- Monitor memory usage: `top -l 1 | grep PhysMem`
- Use models that fit in available RAM
- Consider using Apple Silicon for better performance

## Performance Optimization

### 1. Model Selection

| Model | RAM Usage | Speed | Quality | Use Case |
|-------|-----------|-------|---------|----------|
| `llama2:7b` | 4-8GB | Fast | Good | Development |
| `llama2:13b` | 8-16GB | Medium | Better | Production |
| `llama2:70b` | 32GB+ | Slow | Best | High-quality |

### 2. System Optimization

```bash
# Close unnecessary applications
# Ensure sufficient free RAM
# Use SSD storage for better I/O
# Keep macOS updated
```

### 3. Ollama Configuration

```bash
# Set environment variables for better performance
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_HOST=0.0.0.0

# Restart Ollama after changes
brew services restart ollama
```

## Monitoring and Logs

### Check Ollama Status

```bash
# Service status
brew services list | grep ollama

# Process status
ps aux | grep ollama

# Port status
lsof -i:11434
```

### View Logs

```bash
# Ollama logs
tail -f ~/.ollama/logs/ollama.log

# RAG service logs
tail -f service.log
```

## Security Considerations

### Local Deployment Benefits
- ✅ **No data leaves your machine**
- ✅ **No API rate limits**
- ✅ **No usage tracking**
- ✅ **Complete privacy control**

### Best Practices
- Keep Ollama updated
- Use trusted model sources
- Monitor system resources
- Regular backups of custom models

## Next Steps

After setting up Ollama:

1. **Test with different models** to find the best fit
2. **Create custom model configurations** for your use case
3. **Integrate with your RAG pipeline** for document processing
4. **Monitor performance** and optimize as needed
5. **Scale up** to larger models when resources allow

## Support and Resources

- **Ollama Documentation**: [ollama.ai/docs](https://ollama.ai/docs)
- **GitHub Repository**: [github.com/ollama/ollama](https://github.com/ollama/ollama)
- **Community Discord**: [discord.gg/ollama](https://discord.gg/ollama)
- **Model Library**: [ollama.ai/library](https://ollama.ai/library)

---

**Note**: Ollama provides a cost-effective way to run LLMs locally for RAG development. While it may be slower than cloud APIs, it offers unlimited usage and complete privacy for your development and testing needs.
