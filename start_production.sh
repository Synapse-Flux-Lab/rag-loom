#!/bin/bash

# =============================================================================
# RAG Platform Kit - Production Startup Script
# =============================================================================

set -e  # Exit on any error

echo "🚀 Starting RAG Platform Kit in Production Mode..."
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Ollama is running locally
echo "🔍 Checking Ollama service..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama is not running locally. Starting Ollama..."
    if command -v ollama > /dev/null; then
        ollama serve &
        sleep 5
    else
        echo "❌ Ollama is not installed. Please install Ollama first:"
        echo "   brew install ollama"
        exit 1
    fi
fi

# Check if required models are available
echo "🔍 Checking Ollama models..."
if ! ollama list | grep -q "mixtral:latest"; then
    echo "📥 Downloading mixtral:latest model..."
    ollama pull mixtral:latest
fi

# Create production .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating production .env file..."
    cp env.production .env
    echo "✅ Production .env file created. Please review and update as needed."
fi

# Start production services
echo "🐳 Starting production services with Docker Compose..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ RAG service is healthy!"
    echo "📍 Service URL: http://localhost:8000"
    echo "📊 Prometheus: http://localhost:9090"
    echo "📈 Grafana: http://localhost:3000 (admin/admin)"
    echo "🔍 Qdrant: http://localhost:6333"
    echo "⚡ Redis: localhost:6379"
    echo "🤖 Ollama: http://localhost:11434"
else
    echo "❌ RAG service is not healthy. Check logs with:"
    echo "   docker-compose logs rag-service"
    exit 1
fi

echo ""
echo "🎉 Production RAG Platform Kit is running!"
echo "=========================================="
echo ""
echo "📚 Available endpoints:"
echo "   • Health: http://localhost:8000/health"
echo "   • API Docs: http://localhost:8000/docs"
echo "   • Ingest: http://localhost:8000/api/v1/ingest"
echo "   • Search: http://localhost:8000/api/v1/search"
echo "   • Generate: http://localhost:8000/api/v1/generate"
echo ""
echo "🔧 Management commands:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart: docker-compose restart"
echo "   • Scale: docker-compose up -d --scale rag-service=2"
echo ""
echo "📊 Monitoring:"
echo "   • Prometheus: http://localhost:9090"
echo "   • Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "🚀 Ready for production use!"
