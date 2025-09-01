from fastapi import APIRouter, HTTPException, Depends
import logging
from ..services.elasticsearch_service import ElasticSearchService
from ..services.data_processing import DataProcessingService
from ..models.document import DocumentResponse, MaliciousDocument

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/documents", tags=["documents"])

def get_services():
    return {
        "es_service": ElasticSearchService(),
        "processing_service": DataProcessingService()
    }

@router.get("/antisemitic-with-weapons", response_model=DocumentResponse)
async def get_antisemistic_with_weapons(services=Depends(get_services)):
    """Get all antisemitic documents that contain weapon keywords."""
    try:
        # Check if data processing is complete
        status = await services["processing_service"].get_processing_status()
        is_complete = status["status"] == "completed"
        status_message = status["message"]

        if not is_complete:
            # Return empty response if processing not complete
            return DocumentResponse(
                documents=[],
                total_count=0,
                message=f"Data processing not complete. Status: {status_message}"
            )

        # Fetch documents from Elasticsearch
        documents = await services["es_service"].get_antisemistic_with_weapons()

        # Convert raw dicts to MaliciousDocument objects
        malicious_documents = []
        for doc in documents:
            malicious_documents.append(MaliciousDocument(**doc))

        # Build and return the response
        total = len(malicious_documents)
        return DocumentResponse(
            documents=malicious_documents,
            total_count=total,
            message=f"Found {total} antisemitic documents with weapons"
        )

    except Exception as e:
        logger.error(f"Error getting antisemitic documents with weapons: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/multiple-weapons", response_model=DocumentResponse)
async def get_documents_with_multiple_weapons(services=Depends(get_services)):
    """Get all documents that contain 2 or more weapon keywords."""
    try:
        # Check if data processing is complete
        status = await services["processing_service"].get_processing_status()
        is_complete = status["status"] == "completed"
        status_message = status["message"]

        if not is_complete:
            # Return empty response if processing not complete
            return DocumentResponse(
                documents=[],
                total_count=0,
                message=f"Data processing not complete. Status: {status_message}"
            )

        # Fetch documents from Elasticsearch
        documents = await services["es_service"].get_documents_with_multiple_weapons()

        # Convert raw dicts to MaliciousDocument objects
        malicious_documents = []
        for doc in documents:
            malicious_documents.append(MaliciousDocument(**doc))

        # Build and return the response
        total = len(malicious_documents)
        return DocumentResponse(
            documents=malicious_documents,
            total_count=total,
            message=f"Found {total} documents with 2 or more weapons"
        )

    except Exception as e:
        logger.error(f"Error getting documents with multiple weapons: {e}")
        raise HTTPException(status_code=500, detail=str(e))
