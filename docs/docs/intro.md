---
id: intro
title: Documentation Index
sidebar_position: 1
---

Welcome to the comprehensive documentation for the RAG Loom! This directory contains everything you need to understand, set up, test, and deploy your RAG microservice.

## 📚 Documentation Files

### 🚀 Getting Started
- **[Comprehensive Documentation](./overview)** - Architecture, APIs, and workflows
- **Environment Template:** [env.example](/files/env.example) - Copy to `.env` and customise
- **Quick Start Script:** [utilscripts/quick_start.sh](https://github.com/SynapseFluxLab/rag-loom/blob/main/utilscripts/quick_start.sh) - Automated setup helpers

### 🧪 Testing & Development
- **Test Suite:** Run `pytest` (or `pytest test_service.py` for a quick smoke test)

## 🎯 Quick Start Guide

### 1. **One-Command Setup** (Recommended)
```bash
# Make script executable and run setup
chmod +x utilscripts/quick_start.sh
./utilscripts/quick_start.sh setup
```

### 2. **Manual Setup**
```bash
# Create and activate virtual environment
python3 -m venv renv
source renv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp docs/static/files/env.example .env
# Edit .env with your API keys

# Start service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. **Test Your Setup**
```bash
# Run unit and integration tests
pytest
```

## 🔧 Available Commands

### Quick Start Script Commands
```bash
./utilscripts/quick_start.sh setup      # Initial setup
./utilscripts/quick_start.sh start      # Start service
./utilscripts/quick_start.sh stop       # Stop service
./utilscripts/quick_start.sh restart    # Restart service
./utilscripts/quick_start.sh status     # Check status
./utilscripts/quick_start.sh test       # Run tests
./utilscripts/quick_start.sh logs       # View logs
./utilscripts/quick_start.sh clean      # Cleanup
./utilscripts/quick_start.sh help       # Show help
```

## 📖 What's Included

### **Core Features**
- ✅ **Document Ingestion**: PDF and TXT processing with configurable chunking
- ✅ **Vector Search**: Semantic similarity search with multiple backends
- ✅ **AI Generation**: Context-aware answer generation
- ✅ **Multiple Providers**: OpenAI, Cohere, HuggingFace support
- ✅ **Vector Databases**: ChromaDB, Qdrant, Redis support

### **API Endpoints**
- `GET /health` - Service health check
- `POST /api/v1/ingest` - Single document ingestion
- `POST /api/v1/ingest/batch` - Batch document ingestion
- `POST /api/v1/search` - Document search
- `POST /api/v1/generate` - Answer generation

### **Testing Coverage**
- 🧪 **Unit Tests**: Component-level testing
- 🔗 **Integration Tests**: API endpoint testing
- 🌐 **E2E Tests**: Complete workflow testing
- 📊 **Coverage Reports**: Test coverage analysis

## 🚀 Development Workflow

### **Local Development**
1. **Setup**: `./utilscripts/quick_start.sh setup`
2. **Start**: `./utilscripts/quick_start.sh start`
3. **Develop**: Make changes to your code
4. **Test**: `./utilscripts/quick_start.sh test`
5. **Stop**: `./utilscripts/quick_start.sh stop`

### **Testing Workflow**
1. **Unit Tests**: `pytest tests/unit/`
2. **Integration Tests**: `pytest tests/integration/`
3. **API Smoke Test**: `pytest test_service.py`
4. **Coverage**: `pytest --cov=app --cov-report=html`

## 🔍 Troubleshooting

### **Common Issues**
- **Service won't start**: Check port availability and dependencies
- **Import errors**: Ensure virtual environment is activated
- **API key issues**: Verify .env configuration
- **Test failures**: Check service status and logs

### **Getting Help**
- Check service logs: `./utilscripts/quick_start.sh logs`
- Verify service status: `./utilscripts/quick_start.sh status`
- Run tests: `./utilscripts/quick_start.sh test`
- Review API docs: http://localhost:8000/docs

## 📁 Project Structure

```
rag-platform-kit/
├── app/                   # Application source code
├── docs/                  # Docusaurus documentation site
│   ├── docs/              # Markdown sources (you're here)
│   ├── src/               # Site customisations
│   └── static/files/      # Downloadable assets (e.g. env.example)
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
└── Dockerfile             # Container configuration
```

## 🌟 Next Steps

1. **Read the [Comprehensive Documentation](./overview)** for detailed information
2. **Run the setup script** to get started quickly
3. **Configure your environment** with API keys
4. **Test your endpoints** with the testing suite
5. **Explore the API** at http://localhost:8000/docs
6. **Customize and extend** for your specific use case

## 📞 Support

- **Documentation**: Check the [Comprehensive Documentation](./overview) for detailed guides
- **Testing**: Use the test suite to verify functionality
- **Issues**: Check logs and test results for troubleshooting
- **Development**: Use the quick start script for automation

---

**Happy Building! 🚀**

Your RAG Loom is ready to transform how you work with documents and AI-powered search.
