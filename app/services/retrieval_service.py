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
            
            # Filter by similarity threshold
            filtered_results = [
                SearchResult(
                    id=result["id"],
                    content=result["content"],
                    metadata=result["metadata"],
                    similarity_score=result["similarity_score"],
                    document_id=result["metadata"].get("document_id")
                )
                for result in results
                if result["similarity_score"] >= query.similarity_threshold
            ]
            
            logger.info(f"Retrieved {len(filtered_results)} relevant chunks for query")
            return filtered_results
        
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise

retrieval_service = RetrievalService()