from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger

from app.core.config import settings
from app.api.endpoints import ingestion, retrieval, generation

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
    from app.core.embeddings import embedding_service
    from app.services.llm_service import llm_service
    
    return {
        "status": "healthy",
        "vector_store": vector_store.store_type,
        "embedding_model": embedding_service.model_name,
        "llm_provider": llm_service.provider,
        "timestamp": datetime.utcnow()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)