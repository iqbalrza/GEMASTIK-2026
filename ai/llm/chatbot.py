import logging
from typing import List, Dict
from ai.llm.groq_client import GroqClient
from ai.llm.prompts import chatbot_system
from ai.utils import constants

logger = logging.getLogger(__name__)

class TaniBot:
    def __init__(self, groq_client: GroqClient):
        self.client = groq_client

    def chat(self, message: str, context: dict = None, history: List[Dict[str, str]] = None) -> str:
        """
        Handles chat interactions for Mode 3.
        history format: [{"role": "user", "content": "..."}, {"role": "model", "content": "..."}]
        """
        if not self.client.is_active:
            return "Maaf, fitur TaniBot sedang tidak tersedia saat ini. Silakan cek koneksi atau konfigurasi sistem (API Key tidak ditemukan)."
            
        # Truncate overly long messages
        if len(message) > constants.CHATBOT_MAX_INPUT_LENGTH:
            message = message[:constants.CHATBOT_MAX_INPUT_LENGTH] + "..."

        # Build prompt
        prompt = ""
        
        # Add context if available
        if context:
            prompt += f"Konteks Sensor Tanah Saat Ini:\n"
            prompt += f"- Suhu: {context.get('temperature', 'N/A')}°C\n"
            prompt += f"- Kelembapan: {context.get('humidity', 'N/A')}%\n"
            prompt += f"- pH: {context.get('ph', 'N/A')}\n\n"
            
        # Add history
        if history:
            prompt += "Riwayat Percakapan Sebelumnya:\n"
            for turn in history[-constants.CHATBOT_MAX_HISTORY:]:
                role_name = "User" if turn["role"] == "user" else "TaniBot"
                prompt += f"{role_name}: {turn['content']}\n"
            prompt += "\n"
            
        prompt += f"Pertanyaan Baru User: {message}"
        
        # Generate response
        response = self.client.generate_text(prompt, system_instruction=chatbot_system.SYSTEM_PROMPT)
        
        if not response:
            return "Maaf, TaniBot sedang mengalami gangguan sistem. Silakan coba lagi nanti."
            
        return response
