import logging
import time
from typing import Optional
from google import genai
from google.genai import types
from ai.utils import constants

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.api_key = constants.GEMINI_API_KEY
        self.is_active = bool(self.api_key)
        self.client = None
        
        if self.is_active:
            try:
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Gemini client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.is_active = False
        else:
            logger.warning("GEMINI_API_KEY not found. LLM features will be disabled (fallback mode).")

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
        """Generates text using the Gemini API."""
        if not self.is_active or not self.client:
            return None

        try:
            config_kwargs = {
                "temperature": constants.GEMINI_TEMPERATURE,
                "max_output_tokens": constants.GEMINI_MAX_TOKENS
            }
            if system_instruction:
                config_kwargs["system_instruction"] = system_instruction
                
            config = types.GenerateContentConfig(**config_kwargs)

            # Retry logic for rate limits
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.client.models.generate_content(
                        model=constants.GEMINI_MODEL,
                        contents=prompt,
                        config=config
                    )
                    return response.text
                except Exception as e:
                    if "429" in str(e) and attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 2
                        logger.warning(f"Rate limited (429). Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise e
                        
        except Exception as e:
            logger.error(f"Gemini API error during text generation: {e}")
            return None
