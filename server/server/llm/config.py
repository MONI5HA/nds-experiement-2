"""Configuration settings for LM Studio local inference."""

from typing import Any, Dict

# Default model settings
DEFAULT_TEMPERATURE: float = 0.7
DEFAULT_MAX_OUTPUT_TOKENS: int = 1024

def get_default_config() -> Dict[str, Any]:
    """Get the default configuration settings."""
    return {
        "temperature": DEFAULT_TEMPERATURE,
        "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS,
    }