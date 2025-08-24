# RAG Platform Kit - Comprehensive Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start Guide](#quick-start-guide)
4. [API Reference](#api-reference)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

## Overview

The RAG (Retrieval-Augmented Generation) Platform Kit is a production-ready microservice that provides document ingestion, semantic search, and AI-powered answer generation capabilities. Built with FastAPI, it supports multiple vector databases, embedding models, and LLM providers.

### Key Features
- **Document Ingestion**: PDF and TXT file processing with configurable chunking
- **Vector Search**: Semantic similarity search with multiple backend options
- **AI Generation**: Context-aware answer generation using retrieved documents
- **Scalable Architecture**: Microservice design with health monitoring
- **Multiple Providers**: Support for ChromaDB, Qdrant, Redis, OpenAI, Cohere, and HuggingFace

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App  │    │   Vector Store  │    │   LLM Service   │
│                 │    │                 │    │                 │
│ ├─────────────┤ │    │ ├─────────────┤ │    │ ├─────────────┤ │
│ │ Ingestion  │ │    │ │ ChromaDB    │ │    │ │ OpenAI      │ │
│ │ Retrieval  │ │◄──►│ │ Qdrant      │ │    │ │ Cohere      │ │
│ │ Generation │ │    │ │ Redis       │ │    │ │ HuggingFace │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   File Utils   │    │   Embeddings    │    │   Monitoring    │
│                 │    │                 │    │                 │
│ ├─────────────┤ │    │ ├─────────────┤ │    │ ├─────────────┤ │
│ │ PDF Proc   │ │    │ │ Sentence    │ │    │ │ Prometheus  │ │
│ │ Text Proc  │ │    │ │ Transformers│ │    │ │ Logging     │ │
│ │ Chunking   │ │    │ │ Custom      │ │    │ │ Health      │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start Guide

### Prerequisites
- Python 3.9+
- pip
- Git

### Step 1: Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd rag-platform-kit

# Create virtual environment
python3 -m venv renv

# Activate virtual environment
source renv/bin/activate  # On Windows: renv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

**Required Environment Variables:**
```env
# OpenAI (if using OpenAI)
OPENAI_API_KEY=your_openai_api_key_here

# Cohere (if using Cohere)
COHERE_API_KEY=your_cohere_api_key_here

# Vector Database (choose one)
VECTOR_STORE_TYPE=chroma  # Options: chroma, qdrant, redis

# For Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key

# For Redis
REDIS_URL=redis://localhost:6379
```

### Step 3: Start the Service
```bash
# Start the service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or using Python directly
python app/main.py
```

### Step 4: Verify Installation
```bash
# Check health endpoint
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs
```

## API Reference

### Base URL
```
http://localhost:8000
```

### API Version
```
/api/v1
```

### Authentication
Currently, the API does not require authentication. In production, implement proper authentication middleware.

---

## Endpoints

### 1. Health Check

#### GET `/health`
Check the health status of the service and its components.

**Response:**
```json
{
  "status": "healthy",
  "vector_store": "chroma",
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "llm_provider": "openai",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Test with curl:**
```bash
curl -X GET "http://localhost:8000/health" \
  -H "accept: application/json"
```

---

### 2. Document Ingestion

#### POST `/api/v1/ingest`
Upload and process a single document for ingestion.

**Request Body:**
- `file`: File upload (PDF or TXT)
- `chunk_params` (optional): Chunking parameters

**Chunking Parameters:**
```json
{
  "chunk_size": 1000,
  "chunk_overlap": 200
}
```

**Response:**
```json
{
  "message": "Document processed successfully",
  "file_id": "document.pdf",
  "chunks_created": 15,
  "processing_time": 2.34
}
```

**Test with curl:**
```bash
# Test with PDF file
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.pdf" \
  -F 'chunk_params={"chunk_size": 1000, "chunk_overlap": 200}'

# Test with TXT file
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.txt"
```

#### POST `/api/v1/ingest/batch`
Process multiple documents in batch.

**Request Body:**
- `files`: Multiple file uploads
- `chunk_params` (optional): Chunking parameters

**Response:**
```json
[
  {
    "message": "Document processed successfully",
    "file_id": "doc1.pdf",
    "chunks_created": 10,
    "processing_time": 1.23
  },
  {
    "message": "Document processed successfully",
    "file_id": "doc2.txt",
    "chunks_created": 5,
    "processing_time": 0.87
  }
]
```

**Test with curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/ingest/batch" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@doc1.pdf" \
  -F "files=@doc2.txt" \
  -F 'chunk_params={"chunk_size": 800, "chunk_overlap": 150}'
```

---

### 3. Document Retrieval

#### POST `/api/v1/search`
Search for documents similar to a query.

**Request Body:**
```json
{
  "query": "What is machine learning?",
  "top_k": 5,
  "similarity_threshold": 0.7,
  "filters": {
    "document_type": "pdf",
    "category": "technology"
  }
}
```

**Response:**
```json
[
  {
    "id": "uuid-here",
    "content": "Machine learning is a subset of artificial intelligence...",
    "metadata": {
      "document_type": "pdf",
      "filename": "ml_intro.pdf",
      "page": 1
    },
    "similarity_score": 0.89,
    "document_id": "doc-uuid-here"
  }
]
```

**Test with curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "top_k": 5,
    "similarity_threshold": 0.7
  }'
```

---

### 4. Answer Generation

#### POST `/api/v1/generate`
Generate an answer to a query using retrieved context.

**Request Body:**
```json
{
  "query": "Explain the benefits of machine learning",
  "context": null,
  "search_params": {
    "query": "machine learning benefits",
    "top_k": 3,
    "similarity_threshold": 0.8
  },
  "temperature": 0.7,
  "max_tokens": 500
}
```

**Response:**
```json
{
  "answer": "Machine learning offers several key benefits including...",
  "sources": [
    {
      "id": "uuid-here",
      "content": "Machine learning provides automation...",
      "metadata": {...},
      "similarity_score": 0.92,
      "document_id": "doc-uuid-here"
    }
  ],
  "generation_time": 1.45
}
```

**Test with curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain the benefits of machine learning",
    "search_params": {
      "query": "machine learning benefits",
      "top_k": 3
    },
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PROJECT_NAME` | "RAG Microservice" | Service name |
| `VERSION` | "1.0.0" | API version |
| `API_V1_STR` | "/api/v1" | API version prefix |
| `CHUNK_SIZE` | 1000 | Default chunk size in characters |
| `CHUNK_OVERLAP` | 200 | Default chunk overlap in characters |
| `MAX_FILE_SIZE` | 10485760 | Maximum file size in bytes (10MB) |
| `VECTOR_STORE_TYPE` | "chroma" | Vector database type |
| `EMBEDDING_MODEL` | "sentence-transformers/all-MiniLM-L6-v2" | Embedding model |
| `LLM_PROVIDER` | "openai" | LLM provider |

### Vector Database Configuration

#### ChromaDB (Default)
```env
VECTOR_STORE_TYPE=chroma
CHROMA_PATH=./chroma_db
```

#### Qdrant
```env
VECTOR_STORE_TYPE=qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key
```

#### Redis
```env
VECTOR_STORE_TYPE=redis
REDIS_URL=redis://localhost:6379
```

### LLM Provider Configuration

#### OpenAI
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-3.5-turbo
```

#### Cohere
```env
LLM_PROVIDER=cohere
COHERE_API_KEY=your_api_key
COHERE_MODEL=command-xlarge
```

#### HuggingFace
```env
LLM_PROVIDER=huggingface
HUGGINGFACE_MODEL=google/flan-t5-large
```

## Testing

### Running Tests

```bash
# Install test dependencies
pip install -r tests/requirements-test.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/e2e/           # End-to-end tests
```

### Test Endpoints Manually

```bash
# Start the service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Test health endpoint
curl http://localhost:8000/health

# Test ingestion with sample file
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -F "file=@tests/data/sample.txt"

# Test search
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "top_k": 3}'

# Test generation
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"query": "test question", "search_params": {"query": "test", "top_k": 2}}'
```

## Deployment

### Docker Deployment

```bash
# Build the image
docker build -t rag-microservice .

# Run the container
docker run -p 8000:8000 rag-microservice

# With environment variables
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e VECTOR_STORE_TYPE=chroma \
  rag-microservice
```

### Docker Compose

```bash
# Start with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Considerations

1. **Environment Variables**: Use proper secret management
2. **Database**: Use production-grade vector databases
3. **Monitoring**: Enable Prometheus metrics and logging
4. **Scaling**: Use load balancers and multiple instances
5. **Security**: Implement authentication and rate limiting

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Ensure virtual environment is activated
source renv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 2. Vector Database Connection Issues
```bash
# Check if ChromaDB directory exists
ls -la chroma_db/

# For Qdrant, ensure service is running
curl http://localhost:6333/health

# For Redis, check connection
redis-cli ping
```

#### 3. API Key Issues
```bash
# Verify environment variables
echo $OPENAI_API_KEY
echo $COHERE_API_KEY

# Check .env file
cat .env
```

#### 4. File Upload Issues
```bash
# Check file size limits
ls -lh your_file.pdf

# Verify file format
file your_file.pdf
```

### Logs and Debugging

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# View application logs
tail -f logs/app.log

# Check system resources
htop
df -h
```

### Performance Optimization

1. **Chunking**: Adjust chunk size and overlap for your use case
2. **Embeddings**: Use appropriate embedding models for your domain
3. **Vector Database**: Choose the right vector database for your scale
4. **Caching**: Implement caching for frequently accessed embeddings
5. **Batch Processing**: Use batch endpoints for multiple documents

## Support and Contributing

### Getting Help
- Check the logs for error messages
- Review the API documentation at `/docs`
- Test endpoints individually to isolate issues
- Verify configuration and environment variables

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### License
This project is licensed under the MIT License - see the LICENSE file for details.

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Maintainer**: Your Team
