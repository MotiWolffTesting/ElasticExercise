import json
import os
from typing import List, Dict, Any
from datetime import datetime
import logging
import aiofiles

from ..models.document import MaliciousDocument
from .elasticsearch_service import ElasticSearchService
from .csv_converter_service import CSVConverterService
from .sentiment import SentimentService
from .weapons import WeaponsService
from ..config.settings import settings

logger = logging.getLogger(__name__)

class DataProcessingService:
    """Service for processing malicious text data"""
    
    def __init__(self):
        "Initialize data processing service"
        self.es_service = ElasticSearchService()
        self.sentiment_service = SentimentService()
        self.weapon_service = WeaponsService()
        self.csv_converter = CSVConverterService()
        
    async def load_data_from_file(self, file_path = None) -> List[MaliciousDocument]:
        "Load data from CSV or JSON file and convert to MaliciousDocument objects"
        if file_path is None:
            file_path = settings.DATA_FILE_PATH
            
        try:
            # Check file extension to determine format
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.csv':
                # Convert CSV to JSON first
                logger.info(f"Converting CSV file {file_path} to JSON...")
                json_file_path = self.csv_converter.convert_csv_to_json(file_path)
                data_file_path = json_file_path
            elif file_extension == '.json':
                data_file_path = file_path
            else:
                logger.error(f"Unsupported file format: {file_extension}. Supported formats: .csv, .json")
                return []
            # Load JSON data asynchronously
            async with aiofiles.open(data_file_path, 'r', encoding='utf-8') as f:
                file_content = await f.read()
                data = json.loads(file_content)
                
            documents = []
            for item in data:
                try:
                    # Parse the data
                    text = item.get('text', '')
                    doc = MaliciousDocument(
                        text=text,
                        is_antisemitic=item.get('is_antisemitic', False),
                        created_at=datetime.fromisoformat(item.get('created_at', datetime.now().isoformat())),
                        sentiment=self.sentiment_service.analyze_sentiment(text)
                    )
                    documents.append(doc)
                except Exception as e:
                    logger.error(f"Error parsing document: {e}")
                    continue
                
            logger.info(f"Loaded {len(documents)} documents from {file_path}")
            return documents
                    
        except FileNotFoundError:
            logger.error(f"Data file not found: {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading data from file: {e}")
            return []
            
    async def process_all_documents(self) -> Dict[str, Any]:
        "Complete processing pipeline for all documents"
        try:
            # Create index
            logger.info("Creating ElasticSearch index...")
            await self.es_service.create_index()
            
            # Load the data file
            logger.info("Loading data from file...")
            documents = await self.load_data_from_file()
            if not documents:
                return {"status": "error", "message": "No documents loaded"}
            
            # Index documents
            logger.info("Indexing documents to ElasticSearch...")
            success = await self.es_service.bulk_index_documents(doucments=documents)
            if not success:
                return {"status": "error", "message": "Failed to index documents"}
            
            # Perform sentiment analysis
            logger.info("Performing sentiment analysis...")
            all_docs = await self.es_service.get_all_documents()
            for doc_data in all_docs:
                doc_id = doc_data.get('_id')
                text = doc_data.get('text', '')
                sentiment = self.sentiment_service.analyze_sentiment(text)
                if doc_id is not None:
                    await self.es_service.update_document_sentiment(doc_id, int(sentiment))
                
            # Detect weapons
            logger.info("Detecting weapons keywords...")
            all_docs = await self.es_service.get_all_documents()
            for doc_data in all_docs:
                doc_id = doc_data.get('_id')
                text = doc_data.get('text', '')
                weapons = self.weapon_service.detect_weapons(text)
                if doc_id is not None:
                    await self.es_service.update_document_weapons(doc_id, weapons)
            
            # Delete irrelevant documents
            logger.info("Deleting irrelevant documents...")
            deleted_count = await self.es_service.delete_irrelevant_documents()
            
            # Get final statistics
            final_count = await self.es_service.get_document_count()
            
            return {
                "status": "success",
                "message": "Processing completed successfully",
                "initial_count": len(documents),
                "deleted_count": deleted_count,
                "final_count": final_count
            }
            
        except Exception as e:
            logger.error(f"Error in processing pipeline: {e}")
            return {"status": "error", "message": str(e)}
        
    async def get_processing_status(self) -> Dict[str, Any]:
        "Get current processing status"
        try:
            total_count = await self.es_service.get_document_count()
            
            if total_count == 0:
                return {
                    "status": "not_processed",
                    "message": "No documents have been processed yet",
                    "total_count": 0
                }
            
            # Check if processing is complete by looking for documents with sentiment and weapons
            all_docs = await self.es_service.get_all_documents()
            processed_count = 0
            
            for doc in all_docs:
                if doc.get('sentiment') and doc.get('detected_weapons') is not None:
                    processed_count += 1
            
            if processed_count == total_count:
                return {
                    "status": "completed",
                    "message": "All documents have been processed",
                    "total_count": total_count,
                    "processed_count": processed_count
                }
            else:
                return {
                    "status": "in_progress",
                    "message": f"Processing in progress: {processed_count}/{total_count} documents processed",
                    "total_count": total_count,
                    "processed_count": processed_count
                }
                
        except Exception as e:
            logger.error(f"Error getting processing status: {e}")
            return {"status": "error", "message": str(e)}