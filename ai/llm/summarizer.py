import logging
from typing import Optional, List, Dict, Any
from ai.llm.groq_client import GroqClient
from ai.llm.prompts import insight_generation, summarization

logger = logging.getLogger(__name__)

class InsightSummarizer:
    def __init__(self, groq_client: GroqClient):
        self.client = groq_client

    def generate_evaluator_insight(self, crop_name: str, verdict: str, sensor_data: dict, eval_details: dict) -> Optional[str]:
        """Generates natural language insight for Mode 1."""
        if not self.client.is_active:
            # Fallback: Just return a generic string or use the rule-based remediation directly in the UI
            return None
            
        prompt = insight_generation.get_insight_prompt(crop_name, verdict, sensor_data, eval_details)
        return self.client.generate_text(prompt)

    def generate_recommender_summary(self, top_crops: List[Dict[str, Any]], sensor_data: dict) -> Optional[str]:
        """Generates natural language summary for Mode 2."""
        if not self.client.is_active or not top_crops:
            return None
            
        prompt = summarization.get_summarization_prompt(top_crops, sensor_data)
        return self.client.generate_text(prompt)
