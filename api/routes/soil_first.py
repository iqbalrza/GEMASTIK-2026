from fastapi import APIRouter, HTTPException
from api.schemas.request_models import RecommendRequest
from api.schemas.response_models import RecommendResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/recommend", response_model=RecommendResponse)
async def recommend_crops(request: RecommendRequest):
    """
    Mode 2: Soil-First Recommender.
    Recommends suitable crops based on soil sensor data.
    """
    from api.app import recommender, summarizer
    
    try:
        # Run recommendation (KNN)
        recommendations = recommender.recommend(
            temperature=request.sensor_data.temperature,
            humidity=request.sensor_data.humidity,
            ph=request.sensor_data.ph,
            top_n=request.top_n
        )
        
        if not recommendations or "error" in recommendations[0]:
            error_msg = recommendations[0].get("error", "Failed to generate recommendations")
            return RecommendResponse(success=False, error=error_msg)
            
        # Generate LLM summary
        summary = summarizer.generate_recommender_summary(
            top_crops=recommendations,
            sensor_data=request.sensor_data.dict()
        )
        
        return RecommendResponse(
            success=True,
            recommendations=recommendations,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Error in recommend endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
