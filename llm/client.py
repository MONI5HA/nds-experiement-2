"""Local LM Studio client for making completion requests."""

import os

import openai

# Configure OpenAI client for LM Studio's OpenAI-compatible API
openai.base_url = "http://localhost:1234/v1/"
openai.api_key = (
    "not-needed"  # LM Studio doesn't require an API key for local inference
)


def get_gemini_response(prompt: str, configs: dict = None) -> str:
    """
    Send a completion request to LM Studio's local API.

    Args:
        prompt: The input text prompt
        configs: Optional configuration parameters (temperature, model, etc.)

    Returns:
        String containing the API response text
    """
    try:
        # Set up default configuration parameters
        temperature = 0.7
        max_tokens = 1024

        # Override defaults with any provided configs
        if configs:
            if "temperature" in configs:
                temperature = configs["temperature"]
            if "max_output_tokens" in configs:
                max_tokens = configs["max_output_tokens"]

        # Make request to local LM Studio API
        response = openai.chat.completions.create(
            model="gemma-3-4b-it",  # LM Studio uses this identifier for the loaded model
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

        # Stream the response
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content

        return full_response

    except Exception as e:
        raise Exception(f"Failed to get response from LM Studio: {str(e)}")