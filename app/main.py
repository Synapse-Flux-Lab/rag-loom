from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger

from app.core.config import settings
from app.api.endpoints import ingestion, retrieval, generation

# Display startup information
print("🚀 Starting RAG Platform Kit...")
print(f"📍 Service will run on: {settings.SERVICE_HOST}:{settings.SERVICE_PORT}")
print(f"🔧 Vector Store: {settings.VECTOR_STORE_TYPE}")
print(f"🤖 LLM Provider: {settings.LLM_PROVIDER}")
print()

# Check if essential services are available
if settings.VECTOR_STORE_TYPE == "qdrant":
    try:
        import requests
        response = requests.get(f"{settings.QDRANT_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Qdrant vector store is accessible")
        else:
            print("⚠️  Qdrant vector store may not be running")
    except Exception as e:
        print("❌ Cannot connect to Qdrant vector store")
        print("   Make sure Qdrant is running on:", settings.QDRANT_URL)

print("="*50)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingestion.router, prefix=settings.API_V1_STR, tags=["ingestion"])
app.include_router(retrieval.router, prefix=settings.API_V1_STR, tags=["retrieval"])
app.include_router(generation.router, prefix=settings.API_V1_STR, tags=["generation"])

# Add Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    return {"message": "RAG Microservice API", "version": settings.VERSION}

@app.get("/health")
async def health_check():
    from app.core.vector_store import vector_store
    
    try:
        # Basic health check
        health_status = {
            "status": "healthy",
            "vector_store": settings.VECTOR_STORE_TYPE,
            "embedding_model": settings.EMBEDDING_MODEL,
            "llm_provider": settings.LLM_PROVIDER,
            "timestamp": "2024-01-15T10:30:00Z"
        }
        
        # Add Ollama-specific info
        if settings.LLM_PROVIDER == "ollama":
            health_status["ollama_model"] = settings.OLLAMA_MODEL
            health_status["ollama_url"] = settings.OLLAMA_BASE_URL
        
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=settings.RELOAD,
        workers=settings.WORKER_PROCESSES
    )