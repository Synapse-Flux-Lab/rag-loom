# RAG Loom - Production Deployment Guide

## 🚀 Quick Start

### 1. Prerequisites
- Docker and Docker Compose installed
- Ollama installed locally (`brew install ollama`)
- At least 16GB RAM available
- 50GB+ free disk space

### 2. Start Production Services
```bash
# Make script executable (first time only)
chmod +x start_production.sh

# Start all production services
./start_production.sh
```

### 3. Verify Deployment
```bash
# Check service health
curl http://localhost:8000/health

# View all services
docker-compose ps
```

## 🏗️ Architecture

### Production Stack
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   RAG Service  │    │   Qdrant        │    │   Redis         │
│   (FastAPI)    │◄──►│   (Vector DB)   │◄──►│   (Cache)       │
│   Port: 8000   │    │   Port: 6333    │    │   Port: 6379    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ollama        │    │   Prometheus    │    │   Grafana       │
│   (Local LLM)   │    │   (Metrics)     │    │   (Dashboard)   │
│   Port: 11434   │    │   Port: 9090    │    │   Port: 3000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Monitoring & Observability

### Prometheus Metrics
- **Endpoint**: http://localhost:9090
- **Metrics**: Request counts, response times, error rates
- **Retention**: 200 hours of historical data

### Grafana Dashboards
- **URL**: http://localhost:3000
- **Credentials**: admin/admin
- **Features**: Real-time monitoring, alerting, custom dashboards

### Health Checks
All services include health checks with automatic restart on failure:
- **RAG Service**: HTTP health endpoint
- **Qdrant**: Vector database health
- **Redis**: Cache service health
- **Ollama**: LLM service health

## 🔧 Configuration

### Environment Variables
```bash
# Copy production config
cp env.production .env

# Edit configuration
nano .env
```

### Key Production Settings
```bash
# Performance
WORKER_PROCESSES=4                    # Number of worker processes
MAX_CONCURRENT_REQUESTS=100           # Max concurrent requests
REQUEST_TIMEOUT=300                   # Request timeout in seconds

# Security
DEBUG=false                           # Disable debug mode
ENABLE_AUTH=false                     # Enable authentication (recommended)
SECRET_KEY=your_secret_key_here      # Secret key for JWT tokens

# Monitoring
ENABLE_METRICS=true                   # Enable Prometheus metrics
ENABLE_TRACING=false                  # Enable distributed tracing
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale RAG service to 3 instances
docker-compose up -d --scale rag-service=3

# Scale with load balancer
docker-compose up -d --scale rag-service=5
```

### Resource Limits
```yaml
# Ollama: 8GB-32GB RAM
deploy:
  resources:
    reservations:
      memory: 8G
    limits:
      memory: 32G

# RAG Service: 1GB-4GB RAM
deploy:
  resources:
    reservations:
      memory: 1G
    limits:
      memory: 4G
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Service Won't Start
```bash
# Check logs
docker-compose logs rag-service

# Check resource usage
docker stats

# Restart services
docker-compose restart
```

#### 2. Ollama Model Issues
```bash
# Check available models
ollama list

# Download missing model
ollama pull mixtral:latest

# Test model locally
ollama run mixtral:latest "Hello"
```

#### 3. Memory Issues
```bash
# Check memory usage
docker stats

# Reduce Ollama memory
# Edit docker-compose.yml: memory: 16G

# Use smaller model
export OLLAMA_MODEL=mistral:latest
```

#### 4. Port Conflicts
```bash
# Check port usage
lsof -i:8000
lsof -i:6333
lsof -i:6379

# Kill conflicting processes
sudo lsof -ti:8000 | xargs sudo kill -9
```

### Debug Commands
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f rag-service

# Check service status
docker-compose ps

# Restart specific service
docker-compose restart rag-service

# View resource usage
docker stats
```

## 🔒 Security

### Production Security Checklist
- [ ] **Authentication**: Enable `ENABLE_AUTH=true`
- [ ] **Secret Key**: Change `SECRET_KEY` to strong random string
- [ ] **HTTPS**: Use reverse proxy with SSL termination
- [ ] **Firewall**: Restrict access to necessary ports only
- [ ] **Monitoring**: Enable security monitoring and alerting
- [ ] **Backups**: Regular backups of vector database and models

### Network Security
```bash
# Only expose necessary ports
# 8000: RAG Service (internal only)
# 6333: Qdrant (internal only)
# 6379: Redis (internal only)
# 11434: Ollama (internal only)
# 9090: Prometheus (internal only)
# 3000: Grafana (internal only)
```

## 📦 Deployment

### Production Deployment Steps
1. **Environment Setup**
   ```bash
   cp env.production .env
   # Edit .env with production values
   ```

2. **Start Services**
   ```bash
   ./start_production.sh
   ```

3. **Verify Health**
   ```bash
   curl http://localhost:8000/health
   ```

4. **Load Test**
   ```bash
   # Test with sample documents
   curl -X POST "http://localhost:8000/api/v1/ingest" \
     -F "file=@sample_document.pdf"
   ```

5. **Monitor Performance**
   - Check Grafana dashboards
   - Monitor resource usage
   - Set up alerts

### Backup & Recovery
```bash
# Backup vector database
docker-compose exec qdrant qdrant snapshot create

# Backup Redis data
docker-compose exec redis redis-cli BGSAVE

# Backup Ollama models
cp -r ~/.ollama ./backups/ollama-$(date +%Y%m%d)
```

## 📚 API Usage

### Production API Endpoints
```bash
# Health Check
GET http://localhost:8000/health

# Document Ingestion
POST http://localhost:8000/api/v1/ingest
Content-Type: multipart/form-data
file: <document_file>

# Document Search
POST http://localhost:8000/api/v1/search
Content-Type: application/json
{
  "query": "your search query",
  "top_k": 5,
  "similarity_threshold": 0.7
}

# Answer Generation
POST http://localhost:8000/api/v1/generate
Content-Type: application/json
{
  "query": "your question",
  "search_params": {
    "query": "related search",
    "top_k": 3
  }
}
```

## 🎯 Performance Optimization

### Recommended Settings
```bash
# For high-traffic production
WORKER_PROCESSES=8                    # Scale based on CPU cores
MAX_CONCURRENT_REQUESTS=500           # Increase for high load
REQUEST_TIMEOUT=600                   # Longer timeout for complex queries

# Ollama optimization
OLLAMA_NUM_PARALLEL=4                # Parallel model inference
```

### Monitoring KPIs
- **Response Time**: Target < 2 seconds
- **Throughput**: Requests per second
- **Error Rate**: Target < 1%
- **Resource Usage**: CPU, Memory, Disk I/O
- **Model Performance**: Inference latency

## 🆘 Support

### Getting Help
1. **Check Logs**: `docker-compose logs -f`
2. **Health Status**: `curl http://localhost:8000/health`
3. **Service Status**: `docker-compose ps`
4. **Resource Usage**: `docker stats`

### Emergency Procedures
```bash
# Stop all services
docker-compose down

# Restart specific service
docker-compose restart rag-service

# Scale down for resource issues
docker-compose up -d --scale rag-service=1

# Complete reset
docker-compose down -v
./start_production.sh
```

---

**🎉 Your RAG Loom is now production-ready with:**
- ✅ **Local LLM** (Ollama) - No API costs
- ✅ **Production Vector DB** (Qdrant) - Scalable search
- ✅ **Caching Layer** (Redis) - Performance optimization
- ✅ **Monitoring** (Prometheus + Grafana) - Observability
- ✅ **Health Checks** - Automatic failover
- ✅ **Resource Management** - Docker resource limits
- ✅ **Scalability** - Horizontal scaling support
