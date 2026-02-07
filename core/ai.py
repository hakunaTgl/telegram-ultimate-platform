import os
import json
import logging
from typing import Dict, Any, List
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

class AIEngine:
    """
    Adaptive AI Engine for processing user intents and generating 
    context-aware responses using LLMs.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
        self.model = os.getenv("AI_MODEL", "gpt-4-turbo-preview")

    async def generate_response(self, prompt: str, context: Dict[str, Any], profile: Dict[str, Any]) -> str:
        """
        Generates a response based on the prompt, user context, and profile.
        """
        if not self.client:
            return "AI features are currently disabled. Please configure OPENAI_API_KEY."

        system_message = self._build_system_prompt(profile)
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Context: {json.dumps(context)}

Query: {prompt}"}
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI Generation Error: {e}")
            return "I encountered an error while processing your request. Please try again later."

    def _build_system_prompt(self, profile: Dict[str, Any]) -> str:
        """
        Creates a system prompt that adapts to the user's learned metadata.
        """
        metadata = profile.get("metadata", {}) or {}
        interests = metadata.get("interests", [])
        tone = metadata.get("preferred_tone", "professional and helpful")
        language = profile.get("language_code", "en")
        
        prompt = (
            f"You are the 'Ultimate Telegram Assistant', an advanced autonomous agent. "
            f"Your personality is {tone}. Respond in language: {language}. "
            "You have access to the user's context and profile to provide highly personalized support. "
        )
        
        if interests:
            prompt += f"The user has shown interest in: {', '.join(interests)}. "
            
        prompt += (
            "Be proactive, efficient, and respect all privacy constraints. "
            "If the context contains tasks, help prioritize them."
        )
        return prompt

    async def extract_metadata(self, text: str) -> Dict[str, Any]:
        """
        Uses AI to extract potential metadata from text.
        """
        if not self.client:
            return {}

        prompt = (
            "Extract user metadata from the following text in JSON format. "
            "Fields: interests (list), sentiment (string), topics (list), tone_preference (string).

"
            f"Text: {text}"
        )

        try:
            response = await self.client.chat.completions.create(
                model=\"gpt-3.5-turbo\",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            return {}
