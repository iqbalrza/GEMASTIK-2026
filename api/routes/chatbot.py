from fastapi import APIRouter, HTTPException
from api.schemas.request_models import ChatRequest
from api.schemas.response_models import ChatResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_tanibot(request: ChatRequest):
    """
    Mode 3: TaniBot Agricultural Chatbot.
    Context-aware agricultural consultation.
    """
    from api.app import chatbot
    
    try:
        sensor_context = request.sensor_context.dict() if request.sensor_context else None
        
        # Convert Pydantic models to dicts for the chatbot
        history = [turn.dict() for turn in request.history] if request.history else None
        
        reply = chatbot.chat(
            message=request.message,
            context=sensor_context,
            history=history
        )
        
        return ChatResponse(
            success=True,
            reply=reply
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
