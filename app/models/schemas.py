from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import UUID

class FileType(str, Enum):
    PDF = "pdf"
    TXT = "txt"

class ChunkRequest(BaseModel):
    chunk_size: int = 1000
    chunk_overlap: int = 200

class ChunkResponse(BaseModel):
    chunks: List[str]
    total_chunks: int
    original_size: int

class SearchQuery(BaseModel):
    query: str
    top_k: Optional[int] = 5
    similarity_threshold: Optional[float] = 0.7
    filters: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    id: UUID
    content: str
    metadata: Dict[str, Any]
    similarity_score: float
    document_id: UUID

class GenerationRequest(BaseModel):
    query: str
    context: Optional[List[SearchResult]] = None
    search_params: Optional[SearchQuery] = None
    temperature: float = 0.7
    max_tokens: int = 500

class GenerationResponse(BaseModel):
    answer: str
    sources: List[SearchResult]
    generation_time: float

class HealthResponse(BaseModel):
    status: str
    vector_store: str
    embedding_model: str
    llm_provider: str
    timestamp: datetime

class IngestionRequest(BaseModel):
    file: Any  # This will be handled by FastAPI's File upload
    chunk_size: Optional[int] = 1000
    chunk_overlap: Optional[int] = 200

class IngestionResponse(BaseModel):
    message: str
    file_id: str
    file_name: str
    file_type: str
    chunks_created: int
    processing_time: float
    metadata: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = datetime.now()

class BatchIngestionRequest(BaseModel):
    files: List[Any]  # Multiple files for batch upload
    chunk_size: Optional[int] = 1000
    chunk_overlap: Optional[int] = 200

class BatchIngestionResponse(BaseModel):
    results: List[IngestionResponse]
    total_files: int
    successful_uploads: int
    failed_uploads: int
    total_processing_time: float