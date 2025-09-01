import json
from typing import List, Dict, Any, Optional
from elasticsearch import Elasticsearch
import logging

from ..config.settings import settings
from ..models.document import MaliciousDocument

logger = logging.getLogger(__name__)

class ElasticSearchService:
    """Service for ElasticSearch operations"""
    
    def __init__(self):
        "Initialize es client"
        self.client = Elasticsearch(
            hosts=[{
                'host': settings.ELASTICSEARCH_HOST.replace('http://', '').replace('https://', ''),
                'port': int(settings.ELASTICSEARCH_PORT),
                'scheme': 'http'
            }],
            basic_auth=(settings.ELASTICSEARCH_USERNAME, settings.ELASTICSEARCH_PASSWORD),
            verify_certs=False,
            ssl_show_warn=False
        )
        self.index_name = settings.ELASTICSEARCH_INDEX
        
    async def create_index(self) -> bool:
        "Create the malicious document index with mapping"
        try:
            # Check if index already exists
            if self.client.indices.exists(index=self.index_name):
                logger.info(f"Index {self.index_name} already exists")
                return True

            # Define mapping
            mapping = {
                "properties": {
                    "text": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "is_antisemitic": {
                        "type": "boolean"
                    },
                    "created_at": {
                        "type": "date",
                        "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ssZ"
                    },
                    "sentiment": {
                        "type": "text",
                        "analyzer": "keyword"
                    },
                    "detected_weapons": {
                        "type": "text",
                        "analyzer": "keyword"
                    },
                    "weapon_count": {
                        "type": "integer"
                    }
                }
            }
            
            # Create index
            response = self.client.indices.create(
                index=self.index_name,
                body=mapping
            )
            
            logger.info(f"Created index {self.index_name}: {response}")
            return True
        
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            return False
        
    async def bulk_index_documents(self, doucments: List[MaliciousDocument]) -> bool:
        "Bulk index document for ElasticSearch"
        try:
            actions = []
            for doc in doucments:
                # Add index action
                actions.append({
                    "index": {
                        "_index": self.index_name
                    }
                })
                # Add document source
                actions.append(doc.model_dump())
                
            # Perform bulk indexing
            response = self.client.bulk(body=actions)
            
            if response.get('errors'):
                logger.error(f"Bulk indexing errors: {response['errors']}")
                return False
            
            logger.info(f"Successfully indexed {len(doucments)} documents.")
            return True
        
        except Exception as e:
            logger.error(f"Error bulk indexing documents: {e}")
            return False
        
    async def update_document_sentiment(self, doc_id: str, sentiment: int) -> bool:
        "Update document sentiment"
        try:
            response = self.client.update(
                index=self.index_name,
                id=doc_id,
                body={
                    "doc": {
                        "sentiment": sentiment
                    }
                }
            )
            return response.get('result') == 'updated'
        except Exception as e:
            logger.error(f"Error updating sentiment for document {doc_id}: {e}")
            return False
        
    async def update_document_weapons(self, doc_id: str, weapons: List[str]) -> bool:
        "Update document detected weapons"
        try:
            response = self.client.update(
                index=self.index_name,
                id=doc_id,
                body={
                    "doc": {
                        "detected_weapons": weapons,
                        "weapon_count": len(weapons)
                    }
                }
            )
            return response.get('result') == 'updated'
        except Exception as e:
            logger.info(f"Error updating weapons for document {doc_id}: {e}")
            return False
        
    async def delete_irrelevant_documents(self) -> int:
        "Delete documents that are not antisemistic, have no weapons and neutral sentiment"
        try:
            query = {
                "query": {
                    "bool": {
                        "must_not": [
                            {"term": {"is_antisemitic": True}},
                            {"range": {"weapon_count": {"gt": 0}}},
                            {"term": {"sentiment": "negative"}}
                        ]
                    }
                }
            }
            
            # delete the index
            response = self.client.delete_by_query(
                index=self.index_name,
                body=query
            )
            
            
            deleted_count = response.get('deleted', 0)
            logger.info(f"Deleted {deleted_count} irrelevant documents")
            return deleted_count
        except Exception as e:
            logger.error(f"Error deleting irrelevant documents: {e}")
            return 0
        
    async def get_antisemistic_with_weapons(self) -> List[Dict[str, Any]]:
        "Get all antisemistic documents with weapons"
        try:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"is_antisemitic": True}},
                            {"range": {"weapon_count": {"gt": 0}}}
                        ]
                    }
                }
            }
            
            # Search for documents
            response = self.client.search(
                index=self.index_name,
                body=query,
                size=1000
            )
            
            return [hit['_source'] for hit in response['hits']['hits']]
            
        except Exception as e:
            logger.error(f"Error getting antisemitic documents with weapons: {e}")
            return []
        
    async def get_documents_with_multiple_weapons(self) -> List[Dict[str, Any]]:
        "Get all documents with 2 or more weapons"
        try:
            query = {
                "query": {
                    "range": {
                        "weapon_count": {"gte": 2}
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                body=query,
                size=1000
            )
            
            return [hit['_source'] for hit in response['hits']['hits']]
            
        except Exception as e:
            logger.error(f"Error getting documents with multiple weapons: {e}")
            return [] 
            
    async def get_all_documents(self) -> List[Dict[str, Any]]:
        "Get all documents for processing"
        try:
            response = self.client.search(
                index=self.index_name,
                body={"query": {"match_all": {}}},
                size=1000
            )
            
            return [hit['_source'] for hit in response['hits']['hits']]
            
        except Exception as e:
            logger.error(f"Error getting all documents: {e}")
            return []
    
    async def get_document_count(self) -> int:
        "Get total document count"
        try:
            response = self.client.count(index=self.index_name)
            return response['count']
        except Exception as e:
            logger.error(f"Error getting document count: {e}")
            return 0