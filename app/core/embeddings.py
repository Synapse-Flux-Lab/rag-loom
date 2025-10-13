import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import cohere
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIM
        self._initialize_model()
    
    def _status_template(self):
        return {
            "status": "up",
            "model": self.model_name,
            "provider": self.model_type
        }
    
    def _initialize_model(self):
        try:
            if self.model_name.startswith("text-embedding-"):
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.model_type = "openai"
            elif self.model_name.startswith("embed-english"):
                self.client = cohere.Client(settings.COHERE_API_KEY)
                self.model_type = "cohere"
            else:
                self.model = SentenceTransformer(self.model_name)
                self.model_type = "local"
            logger.info(f"Initialized embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        try:
            if self.model_type == "openai":
                response = self.client.embeddings.create(
                    input=texts,
                    model=self.model_name
                )
                return [data.embedding for data in response.data]
            elif self.model_type == "cohere":
                response = self.client.embed(
                    texts=texts,
                    model=self.model_name
                )
                return response.embeddings
            else:
                embeddings = self.model.encode(texts, convert_to_numpy=True)
                return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def health(self) -> dict:
        """Validate connectivity for the embedding service."""
        status = self._status_template()
        try:
            if self.model_type == "openai":
                if not settings.OPENAI_API_KEY:
                    raise ValueError("Missing OPENAI_API_KEY")
                # Lightweight metadata call to confirm connectivity
                if hasattr(self.client, "models"):
                    self.client.models.list()  # type: ignore[attr-defined]
                else:
                    raise ValueError("OpenAI client does not expose a models endpoint")
            elif self.model_type == "cohere":
                if not settings.COHERE_API_KEY:
                    raise ValueError("Missing COHERE_API_KEY")
                if hasattr(self.client, "check_api_key"):
                    self.client.check_api_key()
                else:
                    # Fallback: perform minimal embed to validate credentials
                    self.client.embed(texts=["health-check"], model=self.model_name)
            elif self.model_type == "local":
                if not hasattr(self, "model"):
                    raise ValueError("Local embedding model not initialized")
            else:
                status["status"] = "down"
                status["error"] = f"Unsupported embedding provider '{self.model_type}'"
        except Exception as exc:
            status["status"] = "down"
            status["error"] = str(exc)
        return status

embedding_service = EmbeddingService()
