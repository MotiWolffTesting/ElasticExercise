import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .controllers.document_controller import router as document_router
from .config.settings import settings

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    "Create and configure the FastAPI application"
    
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="ElasticSearch-based malicious text analysis system for Iranian database data"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(document_router)
    
    @app.get("/")
    async def root():
        "Root endpoint with API information"
        return {
            "message": "Malicious Text Analysis API",
            "version": settings.API_VERSION,
            "endpoints": {
                "antisemitic_with_weapons": "/api/documents/antisemitic-with-weapons",
                "multiple_weapons": "/api/documents/multiple-weapons"
            }
        }
        
    @app.get("/health")
    async def health_check():
        "Health check endpoint"
        return {"status": "healthy", "service": "malicious-text-analyzer"}
    
    return app

# Create the app instance
app = create_app()


if __name__ == "__main__":
    logger.info("Starting Malicious Text Analysis API...")
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info"
    )
