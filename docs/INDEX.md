# RAG Platform Kit - Documentation Index

Welcome to the comprehensive documentation for the RAG Platform Kit! This directory contains everything you need to understand, set up, test, and deploy your RAG microservice.

## 📚 Documentation Files

### 🚀 Getting Started
- **[README.md](README.md)** - Comprehensive project documentation with API reference
- **[env.example](env.example)** - Environment configuration template
- **[quick_start.sh](quick_start.sh)** - Automated setup and testing script

### 🧪 Testing & Development
- **[test_api.py](test_api.py)** - Comprehensive API testing suite with sample data

## 🎯 Quick Start Guide

### 1. **One-Command Setup** (Recommended)
```bash
# Make script executable and run setup
chmod +x docs/quick_start.sh
./docs/quick_start.sh setup
```

### 2. **Manual Setup**
```bash
# Create and activate virtual environment
python3 -m venv renv
source renv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp docs/env.example .env
# Edit .env with your API keys

# Start service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. **Test Your Setup**
```bash
# Run comprehensive API tests
python docs/test_api.py

# Or use the quick start script
./docs/quick_start.sh test
```

## 🔧 Available Commands

### Quick Start Script Commands
```bash
./docs/quick_start.sh setup      # Initial setup
./docs/quick_start.sh start      # Start service
./docs/quick_start.sh stop       # Stop service
./docs/quick_start.sh restart    # Restart service
./docs/quick_start.sh status     # Check status
./docs/quick_start.sh test       # Run tests
./docs/quick_start.sh logs       # View logs
./docs/quick_start.sh clean      # Cleanup
./docs/quick_start.sh help       # Show help
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
1. **Setup**: `./docs/quick_start.sh setup`
2. **Start**: `./docs/quick_start.sh start`
3. **Develop**: Make changes to your code
4. **Test**: `./docs/quick_start.sh test`
5. **Stop**: `./docs/quick_start.sh stop`

### **Testing Workflow**
1. **Unit Tests**: `pytest tests/unit/`
2. **Integration Tests**: `pytest tests/integration/`
3. **API Tests**: `python docs/test_api.py`
4. **Coverage**: `pytest --cov=app --cov-report=html`

## 🔍 Troubleshooting

### **Common Issues**
- **Service won't start**: Check port availability and dependencies
- **Import errors**: Ensure virtual environment is activated
- **API key issues**: Verify .env configuration
- **Test failures**: Check service status and logs

### **Getting Help**
- Check service logs: `./docs/quick_start.sh logs`
- Verify service status: `./docs/quick_start.sh status`
- Run tests: `./docs/quick_start.sh test`
- Review API docs: http://localhost:8000/docs

## 📁 Project Structure

```
rag-platform-kit/
├── app/                    # Application source code
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── docs/                  # Documentation (this directory)
│   ├── README.md          # Comprehensive docs
│   ├── test_api.py        # API testing suite
│   ├── quick_start.sh     # Setup script
│   └── env.example        # Environment template
├── tests/                 # Test suite
├── requirements.txt        # Python dependencies
└── Dockerfile             # Container configuration
```

## 🌟 Next Steps

1. **Read the [README.md](README.md)** for detailed information
2. **Run the setup script** to get started quickly
3. **Configure your environment** with API keys
4. **Test your endpoints** with the testing suite
5. **Explore the API** at http://localhost:8000/docs
6. **Customize and extend** for your specific use case

## 📞 Support

- **Documentation**: Check the README.md for detailed guides
- **Testing**: Use the test suite to verify functionality
- **Issues**: Check logs and test results for troubleshooting
- **Development**: Use the quick start script for automation

---

**Happy Building! 🚀**

Your RAG Platform Kit is ready to transform how you work with documents and AI-powered search.
