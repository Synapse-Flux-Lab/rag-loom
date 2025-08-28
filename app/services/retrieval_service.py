from typing import List, Dict, Any, Optional
from app.core.embeddings import embedding_service
from app.core.vector_store import vector_store
from app.models.schemas import SearchResult, SearchQuery
from app.models.document_models import DocumentChunk
from loguru import logger

class RetrievalService:
    def __init__(self):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
    
    def retrieve(self, query: SearchQuery) -> List[SearchResult]:
        """Retrieve relevant documents for a query"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_service.generate_embeddings([query.query])[0]
            
            # Search similar chunks
            results = self.vector_store.search_similar(
                query_embedding=query_embedding,
                top_k=query.top_k,
                filters=query.filters
            )
            
            # Build SearchResult objects
            ordered_results: List[SearchResult] = [
                SearchResult(
                    id=result["id"],
                    content=result["content"],
                    metadata=result["metadata"],
                    similarity_score=result["similarity_score"],
                    document_id=result["metadata"].get("document_id")
                )
                for result in results
            ]

            # Apply similarity threshold
            filtered_results = [r for r in ordered_results if r.similarity_score >= (query.similarity_threshold or 0.0)]

            # Fallback: if no results pass the threshold, return the top results anyway
            if not filtered_results:
                filtered_results = ordered_results[: query.top_k or 5]
            
            logger.info(f"Retrieved {len(filtered_results)} relevant chunks for query")
            return filtered_results
        
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise

retrieval_service = RetrievalService()