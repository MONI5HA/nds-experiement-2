"""Gemini LLM module for text generation."""

from typing import Any, Dict, Union

from . import client, config


def generate_response(prompt: str, **kwargs: Union[str, float, int]) -> str:
    """
    Generate a response using Gemini API.

    Args:
        prompt: The input text prompt
        **kwargs: Optional configuration parameters
            - model: str, the model to use
            - temperature: float, controls randomness (0-1)
            - top_p: float, nucleus sampling parameter (0-1)
            - top_k: int, number of tokens to consider
            - max_output_tokens: int, maximum tokens in response

    Returns:
        str: The generated response text

    Raises:
        GeminiError: If the API request fails
    """
    # Convert kwargs to proper types if needed
    configs: Dict[str, Any] = {}
    for key, value in kwargs.items():
        if key in config.get_default_config():
            configs[key] = value

    # Get response from Gemini
    return client.get_gemini_response(prompt, configs)


__all__ = ["generate_response"]
