import logging
import joblib
import pandas as pd
from typing import List, Dict, Any
from ai.utils import constants

logger = logging.getLogger(__name__)

class SoilFirstRecommender:
    def __init__(self):
        self.model = None
        self.scaler = None
        self._load_model()

    def _load_model(self):
        try:
            if constants.MODEL_PATH.exists() and constants.SCALER_PATH.exists():
                self.model = joblib.load(constants.MODEL_PATH)
                self.scaler = joblib.load(constants.SCALER_PATH)
                logger.info("Recommender model and scaler loaded successfully.")
            else:
                logger.warning("Model or scaler not found. Please run train_model.py first.")
        except Exception as e:
            logger.error(f"Error loading recommender model: {e}")

    def recommend(self, temperature: float, humidity: float, ph: float, top_n: int = constants.TOP_N_DEFAULT) -> List[Dict[str, Any]]:
        """
        Recommends crops based on soil sensor data.
        Returns top N recommendations with probabilities.
        """
        if not self.model or not self.scaler:
            return [{"error": "Model not loaded"}]

        # Prepare input
        input_data = pd.DataFrame(
            [[temperature, humidity, ph]], 
            columns=constants.FEATURE_COLUMNS
        )
        
        # Scale input
        input_scaled = self.scaler.transform(input_data)
        
        # Get probabilities for all classes
        probs = self.model.predict_proba(input_scaled)[0]
        classes = self.model.classes_
        
        # Map probabilities to classes
        crop_probs = []
        for i, crop_class in enumerate(classes):
            if probs[i] > 0:  # Only include non-zero probabilities
                crop_probs.append({
                    "crop": crop_class,
                    "display_name": constants.CROP_DISPLAY_NAMES.get(crop_class, crop_class.replace("_", " ").title()),
                    "probability": float(probs[i])
                })
                
        # Sort by probability descending
        crop_probs.sort(key=lambda x: x["probability"], reverse=True)
        
        # Return top N
        return crop_probs[:top_n]
