from openai import OpenAI
import cohere
from transformers import pipeline
import ollama  # Add Ollama import
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.models.schemas import SearchResult
from loguru import logger

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self._initialize_client()
    
    def _status_template(self):
        return {
            "status": "up",
            "provider": self.provider,
            "model": getattr(self, "model_name", None)
        }
    
    def _initialize_client(self):
        try:
            if self.provider == "openai":
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.model_name = settings.OPENAI_MODEL
            elif self.provider == "cohere":
                self.client = cohere.Client(settings.COHERE_API_KEY)
                self.model_name = settings.COHERE_MODEL
            elif self.provider == "huggingface":
                self.client = pipeline(
                    "text2text-generation",
                    model=settings.HUGGINGFACE_MODEL,
                    device=-1  # Use CPU by default
                )
                self.model_name = settings.HUGGINGFACE_MODEL
            elif self.provider == "ollama":  # Add Ollama support
                self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)
                self.model_name = settings.OLLAMA_MODEL
            logger.info(f"Initialized LLM service with provider: {self.provider}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_response(self, query: str, context: List[SearchResult], 
                         temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Generate a response based on query and context"""
        try:
            # Prepare context text
            context_text = "\n\n".join([
                f"Source {i+1}: {result.content}" 
                for i, result in enumerate(context)
            ])
            
            if self.provider == "openai":
                prompt = self._create_openai_prompt(query, context_text)
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content.strip()
            
            elif self.provider == "cohere":
                prompt = self._create_cohere_prompt(query, context_text)
                response = self.client.generate(
                    model=self.model_name,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.generations[0].text.strip()
            
            elif self.provider == "huggingface":
                prompt = self._create_hf_prompt(query, context_text)
                response = self.client(
                    prompt,
                    max_length=max_tokens,
                    temperature=temperature,
                    do_sample=True
                )
                return response[0]['generated_text'].strip()
            
            elif self.provider == "ollama":  # Add Ollama generation
                prompt = self._create_ollama_prompt(query, context_text)
                response = self.client.generate(
                    model=self.model_name,
                    prompt=prompt,
                    options={
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                )
                return response['response'].strip()
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def health(self) -> dict:
        """Validate connectivity for the configured LLM provider."""
        status = self._status_template()
        try:
            if self.provider == "openai":
                if not settings.OPENAI_API_KEY:
                    raise ValueError("Missing OPENAI_API_KEY")
                if hasattr(self.client, "models"):
                    self.client.models.list()  # type: ignore[attr-defined]
                else:
                    raise ValueError("OpenAI client does not expose a models endpoint")
            elif self.provider == "cohere":
                if not settings.COHERE_API_KEY:
                    raise ValueError("Missing COHERE_API_KEY")
                if hasattr(self.client, "check_api_key"):
                    self.client.check_api_key()
                else:
                    self.client.generate(
                        model=self.model_name,
                        prompt="health-check",
                        max_tokens=1
                    )
            elif self.provider == "huggingface":
                if not hasattr(self, "client"):
                    raise ValueError("HuggingFace pipeline not initialized")
            elif self.provider == "ollama":
                import requests
                response = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
                if response.status_code != 200:
                    raise ValueError(f"Ollama responded with status {response.status_code}")
            else:
                status["status"] = "down"
                status["error"] = f"Unsupported LLM provider '{self.provider}'"
        except Exception as exc:
            status["status"] = "down"
            status["error"] = str(exc)
        return status
    
    def _create_openai_prompt(self, query: str, context: str) -> str:
        return f"""Context:
{context}

Query: {query}

Answer:"""
    
    def _create_cohere_prompt(self, query: str, context: str) -> str:
        return f"""Context: {context}

Question: {query}

Answer the question based on the context above. If the context doesn't contain the answer, say so. Answer:"""
    
    def _create_hf_prompt(self, query: str, context: str) -> str:
        return f"""answer the question based on the context. If you don't know the answer, say you don't know.

context: {context}

question: {query}

answer:"""

    def _create_ollama_prompt(self, query: str, context: str) -> str:
        return f"""You are a helpful AI assistant for RAG (Retrieval-Augmented Generation) tasks.

Context information:
{context}

Question: {query}

Please answer the question based on the context above. If the context doesn't contain enough information to answer the question, say so. Be concise and accurate.

Answer:"""

llm_service = LLMService()
