from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

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

class IngestionResponse(BaseModel):
    message: str
    file_id: str
    chunks_created: int
    processing_time: float

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None