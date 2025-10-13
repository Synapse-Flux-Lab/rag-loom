from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger

from app.core.config import settings
from app.api.endpoints import ingestion, retrieval, generation
from app.core.vector_store import vector_store
from app.core.embeddings import embedding_service
from app.services.llm_service import llm_service

# Display startup information
print("🚀 Starting RAG Loom...")
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
    """Expose service dependencies and current readiness state."""
    timestamp = datetime.now(timezone.utc).isoformat()
    
    vector_status = vector_store.health()
    embedding_status = embedding_service.health()
    llm_status = llm_service.health()
    
    overall_status = "healthy" if all(
        subsystem.get("status") == "up"
        for subsystem in (vector_status, embedding_status, llm_status)
    ) else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": timestamp,
        "vector_store": vector_status,
        "embedding": embedding_status,
        "llm": llm_status,
        "version": settings.VERSION,
        "service": settings.PROJECT_NAME
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=settings.RELOAD,
        workers=settings.WORKER_PROCESSES
    )
