import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Initialize AI instances
from ai.models.evaluator.evaluator_engine import PlantFirstEvaluator
from ai.models.recommender.recommender_engine import SoilFirstRecommender
from ai.llm.groq_client import GroqClient
from ai.llm.summarizer import InsightSummarizer
from ai.llm.chatbot import TaniBot

evaluator = PlantFirstEvaluator()
recommender = SoilFirstRecommender()
groq_client = GroqClient()
summarizer = InsightSummarizer(groq_client)
chatbot = TaniBot(groq_client)

def create_app() -> FastAPI:
    app = FastAPI(
        title="IoT Soil Probe AI Engine",
        description="Backend intelligence for P2L Urban Farming App",
        version="1.0.0"
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    from api.routes import plant_first, soil_first, chatbot as chat_route
    
    app.include_router(plant_first.router, prefix="/api", tags=["Mode 1: Plant-First"])
    app.include_router(soil_first.router, prefix="/api", tags=["Mode 2: Soil-First"])
    app.include_router(chat_route.router, prefix="/api", tags=["Mode 3: Chatbot"])

    @app.get("/health")
    async def health_check():
        """Basic health check endpoint."""
        return {
            "status": "healthy",
            "llm_active": groq_client.is_active,
            "recommender_model_loaded": recommender.model is not None
        }

    return app

app = create_app()
