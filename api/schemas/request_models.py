from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class SensorData(BaseModel):
    temperature: float = Field(..., description="Soil temperature in Celsius")
    humidity: float = Field(..., description="Soil humidity percentage")
    ph: float = Field(..., description="Soil pH level")

class EvaluateRequest(BaseModel):
    crop_name: str = Field(..., description="Target crop to evaluate against (e.g., 'tomat')")
    sensor_data: SensorData

class RecommendRequest(BaseModel):
    sensor_data: SensorData
    top_n: int = Field(5, description="Number of recommendations to return")

class ChatTurn(BaseModel):
    role: str = Field(..., description="Role of the sender ('user' or 'model')")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message to TaniBot")
    sensor_context: Optional[SensorData] = Field(None, description="Current sensor data for context")
    history: Optional[List[ChatTurn]] = Field(None, description="Previous chat history")
