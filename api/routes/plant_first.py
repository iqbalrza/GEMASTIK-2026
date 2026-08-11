from fastapi import APIRouter, Depends, HTTPException
from api.schemas.request_models import EvaluateRequest
from api.schemas.response_models import EvaluateResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_soil(request: EvaluateRequest):
    """
    Mode 1: Plant-First Evaluator.
    Evaluates soil conditions against a specific crop's ideal profile.
    """
    from api.app import evaluator, summarizer
    
    try:
        # Run evaluation
        eval_result = evaluator.evaluate(
            crop_name=request.crop_name,
            temperature=request.sensor_data.temperature,
            humidity=request.sensor_data.humidity,
            ph=request.sensor_data.ph
        )
        
        if not eval_result.get("valid"):
            return EvaluateResponse(success=False, error=eval_result.get("error"))
            
        # Generate LLM insight
        insight = summarizer.generate_evaluator_insight(
            crop_name=eval_result["display_name"],
            verdict=eval_result["verdict"],
            sensor_data=request.sensor_data.dict(),
            eval_details=eval_result["details"]
        )
        
        return EvaluateResponse(
            success=True,
            data=eval_result,
            insight=insight
        )
        
    except Exception as e:
        logger.error(f"Error in evaluate endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/crops")
async def get_crop_profiles():
    """
    Returns the list of all supported crops and their ideal sensor ranges.
    Useful for the Mobile App to send dynamic thresholds to the ESP32 via Bluetooth.
    """
    from api.app import evaluator
    
    try:
        profiles = evaluator.crop_profiles
        
        # Format the response nicely
        crop_list = []
        for crop_id, data in profiles.items():
            crop_list.append({
                "id": crop_id,
                "display_name": data["display_name"],
                "thresholds": {
                    "temperature": data["temperature"],
                    "humidity": data["humidity"],
                    "ph": data["ph"]
                }
            })
            
        return {
            "success": True,
            "data": crop_list
        }
    except Exception as e:
        logger.error(f"Error getting crops: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve crop profiles.")
