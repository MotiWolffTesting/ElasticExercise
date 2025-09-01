import nltk
from textblob import TextBlob
from typing import List
import logging

logger = logging.getLogger(__name__)

class SentimentService:
    """Service for sentiment analysis using NLTK and TextBlob"""
    
    def __init__(self):
        "Initiaite sentiment"
        try:
            # Download required NLTK data (only needed once)
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            logger.info("NLTK data loaded successfully")
        except Exception as e:
            logger.warning(f"Could not download NLTK data: {e}")
            
    def analyze_sentiment(self, text: str) -> str:
        "Analyze sentiment using TextBlob"
        if not text or not text.strip():
            return 'neutral'
        
        try:
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity # type: ignore
            
            # Convert polarity to sentiment categories
            if polarity > 0.1:
                return 'positive'
            elif polarity < -0.1:
                return 'negative'
            else:
                return 'neutral'
                
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return 'neutral'
        
    def batch_analyze_sentiment(self, texts: List[str]) -> List[str]:
        "Analyze sentiment for multiple texts"
        return [self.analyze_sentiment(text) for text in texts]
    
    def get_sentiment_score(self, text: str) -> float:
        "Get detailed sentiment polarity score (-1.0 to 1.0)"
        if not text or not text.strip():
            return 0.0
        
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity # type: ignore
        except Exception as e:
            logger.error(f"Error getting sentiment score: {e}")
            return 0.0