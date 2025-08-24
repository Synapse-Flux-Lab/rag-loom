import chromadb
from chromadb.config import Settings as ChromaSettings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from typing import List, Dict, Any, Optional
import numpy as np
from uuid import UUID
import json

from app.core.config import settings
from app.models.document_models import DocumentChunk
from loguru import logger

class VectorStoreService:
    def __init__(self):
        self.store_type = settings.VECTOR_STORE_TYPE
        self.embedding_dim = settings.EMBEDDING_DIM
        self._initialize_store()
    
    def _initialize_store(self):
        try:
            if self.store_type == "chroma":
                self.client = chromadb.PersistentClient(
                    path=settings.CHROMA_PATH,
                    settings=ChromaSettings(anonymized_telemetry=False)
                )
                self.collection = self.client.get_or_create_collection(
                    name="document_chunks",
                    metadata={"hnsw:space": "cosine"}
                )
            elif self.store_type == "qdrant":
                self.client = QdrantClient(
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY
                )
                # Ensure collection exists
                try:
                    self.client.get_collection("document_chunks")
                except Exception:
                    self.client.create_collection(
                        collection_name="document_chunks",
                        vectors_config=VectorParams(
                            size=self.embedding_dim,
                            distance=Distance.COSINE
                        )
                    )
            elif self.store_type == "redis":
                self.client = redis.Redis.from_url(settings.REDIS_URL)
                # Create index if it doesn't exist
                try:
                    self.client.ft("document_chunks").info()
                except Exception:
                    schema = (
                        TextField("$.content", as_name="content"),
                        TextField("$.metadata", as_name="metadata"),
                        VectorField("$.embedding", 
                                   "HNSW", 
                                   {"TYPE": "FLOAT32", 
                                    "DIM": self.embedding_dim, 
                                    "DISTANCE_METRIC": "COSINE"},
                                   as_name="embedding")
                    )
                    definition = IndexDefinition(prefix=["chunk:"], index_type=IndexType.JSON)
                    self.client.ft("document_chunks").create_index(
                        fields=schema, definition=definition
                    )
            logger.info(f"Initialized vector store: {self.store_type}")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    def store_chunks(self, chunks: List[DocumentChunk]):
        """Store document chunks in the vector database"""
        try:
            if self.store_type == "chroma":
                ids = [str(chunk.id) for chunk in chunks]
                documents = [chunk.content for chunk in chunks]
                metadatas = [{"document_id": str(chunk.document_id), **chunk.metadata} 
                            for chunk in chunks]
                embeddings = [chunk.embedding for chunk in chunks if chunk.embedding]
                
                if embeddings:
                    self.collection.add(
                        ids=ids,
                        documents=documents,
                        metadatas=metadatas,
                        embeddings=embeddings
                    )
                else:
                    self.collection.add(
                        ids=ids,
                        documents=documents,
                        metadatas=metadatas
                    )
            
            elif self.store_type == "qdrant":
                points = []
                for chunk in chunks:
                    point = PointStruct(
                        id=str(chunk.id),
                        vector=chunk.embedding or [],
                        payload={
                            "content": chunk.content,
                            "document_id": str(chunk.document_id),
                            "metadata": chunk.metadata
                        }
                    )
                    points.append(point)
                self.client.upsert(
                    collection_name="document_chunks",
                    points=points
                )
            
            elif self.store_type == "redis":
                for chunk in chunks:
                    key = f"chunk:{chunk.id}"
                    data = {
                        "content": chunk.content,
                        "document_id": str(chunk.document_id),
                        "metadata": json.dumps(chunk.metadata),
                        "embedding": np.array(chunk.embedding).astype(np.float32).tobytes() if chunk.embedding else b""
                    }
                    self.client.json().set(key, "$", data)
            
            logger.info(f"Stored {len(chunks)} chunks in vector store")
        
        except Exception as e:
            logger.error(f"Error storing chunks: {e}")
            raise
    
    def search_similar(self, query_embedding: List[float], top_k: int = 5, 
                      filters: Optional[Dict] = None) -> List[Dict]:
        """Search for similar chunks in the vector database"""
        try:
            if self.store_type == "chroma":
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=filters
                )
                return [
                    {
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "similarity_score": results["distances"][0][i] if "distances" in results else 0
                    }
                    for i in range(len(results["ids"][0]))
                ]
            
            elif self.store_type == "qdrant":
                results = self.client.search(
                    collection_name="document_chunks",
                    query_vector=query_embedding,
                    limit=top_k,
                    query_filter=filters
                )
                return [
                    {
                        "id": result.id,
                        "content": result.payload["content"],
                        "metadata": result.payload["metadata"],
                        "similarity_score": result.score
                    }
                    for result in results
                ]
            
            elif self.store_type == "redis":
                # Convert embedding to bytes for Redis
                query_vector = np.array(query_embedding).astype(np.float32).tobytes()
                # Build query
                base_query = f"*=>[KNN {top_k} @embedding $vec AS score]"
                if filters:
                    filter_query = " ".join([f"@{k}:{v}" for k, v in filters.items()])
                    base_query = f"({filter_query})=>[KNN {top_k} @embedding $vec AS score]"
                
                results = self.client.ft("document_chunks").search(
                    base_query,
                    {
                        "vec": query_vector
                    },
                    sort_by="score",
                    dialect=2
                )
                
                return [
                    {
                        "id": doc.id,
                        "content": doc.content,
                        "metadata": json.loads(doc.metadata),
                        "similarity_score": float(doc.score)
                    }
                    for doc in results.docs
                ]
        
        except Exception as e:
            logger.error(f"Error searching similar chunks: {e}")
            raise

vector_store = VectorStoreService()