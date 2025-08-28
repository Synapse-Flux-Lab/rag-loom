from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4

class DocumentChunk(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    content: str
    metadata: Dict[str, Any] = {}
    embedding: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Document(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    filename: str
    content: str
    chunks: List[DocumentChunk] = []
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)