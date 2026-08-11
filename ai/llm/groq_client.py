import logging
import time
from typing import Optional
from groq import Groq
from ai.utils import constants

logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self):
        self.api_key = constants.GROQ_API_KEY
        self.is_active = bool(self.api_key)
        self.client = None
        
        if self.is_active:
            try:
                self.client = Groq(api_key=self.api_key)
                logger.info("Groq client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                self.is_active = False
        else:
            logger.warning("GROQ_API_KEY not found. LLM features will be disabled (fallback mode).")

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
        """Generates text using the Groq API."""
        if not self.is_active or not self.client:
            return None

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.client.chat.completions.create(
                        model=constants.GROQ_MODEL,
                        messages=messages,
                        temperature=constants.GROQ_TEMPERATURE,
                        max_tokens=constants.GROQ_MAX_TOKENS
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    if "429" in str(e) and attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 2
                        logger.warning(f"Rate limited (429). Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise e
                        
        except Exception as e:
            logger.error(f"Groq API error during text generation: {e}")
            return None
