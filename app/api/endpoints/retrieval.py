from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.schemas import SearchQuery, SearchResult, ErrorResponse
from app.services.retrieval_service import retrieval_service
from loguru import logger

router = APIRouter()

@router.post(
    "/search",
    response_model=List[SearchResult],
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def search_documents(query: SearchQuery):
    """
    Search for documents similar to the query.
    
    Returns a list of document chunks ranked by similarity.
    """
    try:
        results = retrieval_service.retrieve(query)
        return results
    
    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching documents: {str(e)}"
        )