import os
from typing import List

class Settings:
    """Application Settings"""
    
    # ElasticSearch Configuration
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST", "http://localhost")
    ELASTICSEARCH_PORT: str = os.getenv("ELASTICSEARCH_PORT", "9200")
    ELASTICSEARCH_USERNAME: str = os.getenv("ELASTICSEARCH_USERNAME", "elastic")
    ELASTICSEARCH_PASSWORD: str = os.getenv("ELASTICSEARCH_PASSWORD", "password")
    ELASTICSEARCH_INDEX: str = os.getenv("ELASTICSEARCH_INDEX", "malicious_documents")
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8080"))
    API_TITLE: str = "Malicious Text Analysis API"
    API_VERSION: str = "1.0.0"
    
    # Data file Configuration
    DATA_FILE_PATH: str = os.getenv("DATA_FILE_PATH", "data/tweets_injected_3.csv")

settings = Settings()