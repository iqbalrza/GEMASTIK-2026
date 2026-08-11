from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class EvaluateResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    insight: Optional[str] = None
    error: Optional[str] = None

class RecommendResponse(BaseModel):
    success: bool
    recommendations: Optional[List[Dict[str, Any]]] = None
    summary: Optional[str] = None
    error: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    reply: Optional[str] = None
    error: Optional[str] = None
