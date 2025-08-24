import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Microservice"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Chunking settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Vector database settings
    VECTOR_STORE_TYPE: str = "chroma"  # Options: chroma, qdrant, redis
    CHROMA_PATH: str = "./chroma_db"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = None
    REDIS_URL: str = "redis://localhost:6379"
    
    # Embedding settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384
    
    # LLM settings
    LLM_PROVIDER: str = "openai"  # Options: openai, cohere, huggingface
    OPENAI_API_KEY: str = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    COHERE_API_KEY: str = None
    COHERE_MODEL: str = "command-xlarge"
    HUGGINGFACE_MODEL: str = "google/flan-t5-large"
    
    # Retrieval settings
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        case_sensitive = True

settings = Settings()