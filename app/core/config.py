import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

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
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379"
    
    # Embedding settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384
    
    # LLM settings
    LLM_PROVIDER: str = "ollama"  # Options: openai, cohere, huggingface, ollama
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    COHERE_API_KEY: Optional[str] = None
    COHERE_MODEL: str = "command-xlarge"
    HUGGINGFACE_API_KEY: Optional[str] = None
    HUGGINGFACE_MODEL: str = "google/flan-t5-large"
    
    # Ollama settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mixtral:latest"
    OLLAMA_NUM_PARALLEL: int = 2
    
    # Retrieval settings
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./rag_platform.db"
    
    # Service settings
    SERVICE_PORT: int = 8000
    SERVICE_HOST: str = "0.0.0.0"
    LOG_LEVEL: str = "INFO"
    
    # Production settings
    DEBUG: bool = False
    RELOAD: bool = False
    WORKER_PROCESSES: int = 4
    MAX_CONCURRENT_REQUESTS: int = 100
    REQUEST_TIMEOUT: int = 300
    
    # Security settings
    ENABLE_AUTH: bool = False
    SECRET_KEY: str = "your_production_secret_key_here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Monitoring
    ENABLE_METRICS: bool = True
    ENABLE_TRACING: bool = False
    
    # Storage
    UPLOAD_DIR: str = "./uploads"
    PROCESSED_DIR: str = "./processed"
    CACHE_DIR: str = "./cache"
    LOGS_DIR: str = "./logs"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_and_warn_api_keys()
    
    def _validate_and_warn_api_keys(self):
        """Validate API keys and display user-friendly warnings"""
        missing_keys = []
        
        # Check vector store API keys
        if self.VECTOR_STORE_TYPE == "qdrant" and not self.QDRANT_API_KEY:
            missing_keys.append("QDRANT_API_KEY")
        
        # Check AI provider API keys based on selected provider
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        elif self.LLM_PROVIDER == "cohere" and not self.COHERE_API_KEY:
            missing_keys.append("COHERE_API_KEY")
        elif self.LLM_PROVIDER == "huggingface" and not self.HUGGINGFACE_API_KEY:
            missing_keys.append("HUGGINGFACE_API_KEY")
        elif self.LLM_PROVIDER == "ollama":
            # Ollama doesn't need API keys, but check if service is accessible
            try:
                import requests
                response = requests.get(f"{self.OLLAMA_BASE_URL}/api/tags", timeout=5)
                if response.status_code != 200:
                    print(f"⚠️  Warning: Ollama service may not be accessible at {self.OLLAMA_BASE_URL}")
            except Exception:
                print(f"⚠️  Warning: Cannot connect to Ollama service at {self.OLLAMA_BASE_URL}")
        
        # Display warnings for missing keys
        if missing_keys:
            print("\n" + "="*60)
            print("⚠️  WARNING: Missing API Keys")
            print("="*60)
            print("The following API keys are required but not found:")
            for key in missing_keys:
                print(f"   • {key}")
            print("\nTo fix this:")
            print("1. Create a .env file in your project root")
            print("2. Add your API keys:")
            for key in missing_keys:
                print(f"   {key}=your_api_key_here")
            print("3. Restart the service")
            print("\nNote: Some features may not work without valid API keys.")
            print("="*60 + "\n")
        
        # Display current configuration
        print("🔧 Current Configuration:")
        print(f"   • Vector Store: {self.VECTOR_STORE_TYPE}")
        print(f"   • LLM Provider: {self.LLM_PROVIDER}")
        if self.LLM_PROVIDER == "ollama":
            print(f"   • Ollama Model: {self.OLLAMA_MODEL}")
            print(f"   • Ollama URL: {self.OLLAMA_BASE_URL}")
        elif self.LLM_PROVIDER == "openai":
            print(f"   • OpenAI Model: {self.OPENAI_MODEL}")
        elif self.LLM_PROVIDER == "huggingface":
            print(f"   • HuggingFace Model: {self.HUGGINGFACE_MODEL}")
        elif self.LLM_PROVIDER == "cohere":
            print(f"   • Cohere Model: {self.COHERE_MODEL}")
        print(f"   • Service Port: {self.SERVICE_PORT}")
        print()

settings = Settings()