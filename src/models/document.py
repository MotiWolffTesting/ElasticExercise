from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class MaliciousDocument(BaseModel):
    """Document model representing a malicious text entry from the Iranian database"""
    id: Optional[str] = None
    text: str = Field(..., description="The text content to analyze")
    is_antisemitic: bool = Field(..., description="Whether the text is classified as antisemitic")
    created_at: datetime = Field(..., description="Timestamp when the message was added to database")
    sentiment: Optional[str] = Field(None, description="Detected sentiment (positive, negative, neutral)")
    detected_weapons: Optional[List[str]] = Field(default_factory=list, description="List of detected weapon keywords")
    weapon_count: int = Field(default=0, description="Number of weapons detected in the text")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
class DocumentResponse(BaseModel):
    """Response model for document queries"""
    documents: List[MaliciousDocument]
    total_count: int
    message: Optional[str] = None


class ProcessingStatus(BaseModel):
    """Status model for processing operations"""
    status: str
    message: str
    processed_count: int = 0
    total_count: int = 0