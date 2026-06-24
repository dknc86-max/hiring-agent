"""
Utility functions for LLM providers.
"""

import logging
from typing import Any, Dict, Optional
from models import ModelProvider, OllamaProvider, GeminiProvider, OpenAIProvider, MockProvider
from prompt import MODEL_PROVIDER_MAPPING, GEMINI_API_KEY, OPENAI_API_KEY, OPENAI_BASE_URL, GROQ_API_KEY
from config import MOCK_MODE, DEVELOPMENT_MODE

logger = logging.getLogger(__name__)


def extract_json_from_response(response_text: str) -> str:
    """
    Extract JSON content from markdown code blocks.

    Args:
        response_text: Text that may contain JSON wrapped in markdown code blocks

    Returns:
        Text with markdown code block syntax removed
    """

    response_text = response_text.strip()
    if "<think>" in response_text:
        think_start = response_text.find("<think>")
        think_end = response_text.find("</think>")
        if think_start != -1 and think_end != -1:
            response_text = response_text[:think_start] + response_text[think_end + 8 :]

    # Remove leading ```json if present
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    # Remove trailing ``` if present
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    return response_text


def initialize_llm_provider(model_name: str) -> Any:
    """
    Initialize the appropriate LLM provider based on the model name.

    Args:
        model_name: The name of the model to use

    Returns:
        An initialized LLM provider (OllamaProvider, GeminiProvider, OpenAIProvider, or MockProvider)
    """
    if MOCK_MODE:
        logger.info("🔄 Using Mock provider (no LLM API calls)")
        return MockProvider()

    model_provider = MODEL_PROVIDER_MAPPING.get(model_name, ModelProvider.OLLAMA)

    if model_provider == ModelProvider.GEMINI:
        if not GEMINI_API_KEY:
            logger.warning("⚠️ Gemini API key not found. Falling back to Ollama.")
            provider = OllamaProvider()
        else:
            logger.info(f"🔄 Using Google Gemini API provider with model {model_name}")
            provider = GeminiProvider(api_key=GEMINI_API_KEY)
    elif model_provider == ModelProvider.OPENAI:
        api_key = GROQ_API_KEY if "groq" in OPENAI_BASE_URL else OPENAI_API_KEY
        if not api_key:
            logger.warning("⚠️ OpenAI/Groq API key not found. Falling back to Ollama.")
            provider = OllamaProvider()
        else:
            provider_name = "Groq" if "groq" in OPENAI_BASE_URL else "OpenAI"
            logger.info(f"🔄 Using {provider_name} provider with model {model_name}")
            provider = OpenAIProvider(
                api_key=api_key,
                base_url=OPENAI_BASE_URL if OPENAI_BASE_URL else None,
            )
    else:
        logger.info(f"🔄 Using Ollama provider with model {model_name}")
        provider = OllamaProvider()

    return provider
