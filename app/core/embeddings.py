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

embedding_service = EmbeddingService()