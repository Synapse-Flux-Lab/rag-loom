from openai import OpenAI
import cohere
from transformers import pipeline
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.models.schemas import SearchResult
from loguru import logger

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self._initialize_client()
    
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
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def _create_openai_prompt(self, query: str, context: str) -> str:
        return f"""Based on the following context, answer the query. If the context doesn't contain the answer, say so.

Context:
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

llm_service = LLMService()