from fastapi import APIRouter, UploadFile, File, HTTPException, status
import time
from typing import List, Optional

from app.core.config import settings
from app.models.schemas import IngestionResponse, ErrorResponse, ChunkRequest
from app.utils.file_processing import FileProcessor
from app.core.chunking import TextChunker
from app.core.embeddings import embedding_service
from app.core.vector_store import vector_store
from app.models.document_models import DocumentChunk
from loguru import logger
from uuid import uuid4

router = APIRouter()
file_processor = FileProcessor()


async def _process_upload_file(
    file: UploadFile,
    chunk_params: Optional[ChunkRequest],
) -> IngestionResponse:
    """Shared ingestion logic for single and batch uploads."""
    start_time = time.time()

    await file.seek(0)
    file_content = await file.read()
    if len(file_content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE} bytes",
        )

    file_type = file_processor.get_file_type(file.filename)

    if file_type == "pdf":
        text = file_processor.extract_text_from_pdf(file_content)
    elif file_type == "txt":
        text = file_processor.extract_text_from_txt(file_content)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type",
        )

    cleaned_text = file_processor.clean_text(text)

    chunker_params = chunk_params.dict() if chunk_params else {}
    chunker = TextChunker(**chunker_params)
    chunks = chunker.sliding_window_chunk(cleaned_text)

    document_id = uuid4()
    doc_chunks: List[DocumentChunk] = []
    for idx, chunk_text in enumerate(chunks):
        metadata = {
            "document_id": str(document_id),
            "file_name": file.filename,
            "file_type": file_type,
            "chunk_index": idx,
        }
        doc_chunks.append(
            DocumentChunk(
                document_id=document_id,
                content=chunk_text,
                metadata=metadata,
            )
        )

    embeddings = (
        embedding_service.generate_embeddings([c.content for c in doc_chunks])
        if doc_chunks
        else []
    )
    for idx, embedding in enumerate(embeddings):
        doc_chunks[idx].embedding = embedding

    if doc_chunks:
        vector_store.store_chunks(doc_chunks)

    processing_time = time.time() - start_time
    logger.info(f"Processed file {file.filename}: {len(chunks)} chunks created")

    return IngestionResponse(
        message="Document processed successfully",
        file_id=file.filename,
        file_name=file.filename,
        file_type=file_type,
        chunks_created=len(chunks),
        processing_time=round(processing_time, 2),
        metadata={"document_id": str(document_id)} if doc_chunks else None,
    )


@router.post(
    "/ingest",
    response_model=IngestionResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def ingest_document(
    file: UploadFile = File(...),
    chunk_params: ChunkRequest = None
):
    """
    Upload and process documents for ingestion into the RAG system.
    
    Supports PDF and TXT files. Files are chunked with configurable
    size and overlap parameters.
    """
    try:
        return await _process_upload_file(file, chunk_params)
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Value error processing file: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error processing file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during file processing"
        )



@router.post("/ingest/batch", response_model=List[IngestionResponse])
async def ingest_batch_documents(
    files: List[UploadFile] = File(...),
    chunk_params: ChunkRequest = None
):
    """Process multiple documents in batch"""
    results = []
    
    for file in files:
        try:
            result = await _process_upload_file(file, chunk_params)
            results.append(result)
        except HTTPException as e:
            # Continue processing other files even if one fails
            results.append(IngestionResponse(
                message=f"Failed to process {file.filename}: {e.detail}",
                file_id=file.filename or "unknown_file",
                file_name=file.filename or "unknown_file",
                file_type="unknown",
                chunks_created=0,
                processing_time=0.0,
                metadata={"error": e.detail} if e.detail else None
            ))
        except Exception as e:
            results.append(IngestionResponse(
                message=f"Error processing {file.filename}: {str(e)}",
                file_id=file.filename or "unknown_file",
                file_name=file.filename or "unknown_file",
                file_type="unknown",
                chunks_created=0,
                processing_time=0.0,
                metadata={"error": str(e)}
            ))
    
    return results
