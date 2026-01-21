"""
Async API clients for querying OpenAI and Google Gemini models.

Uses httpx for OpenAI (handles brotli compression) and aiohttp for Gemini.
"""

import asyncio
import os
import time
from typing import TypedDict, Callable, Awaitable

import aiohttp
import httpx


class ModelResponse(TypedDict):
    """Response from a model API call."""
    model: str
    content: str
    success: bool
    error: str | None
    response_time_ms: int


# Model configurations
OPENAI_MODEL = "gpt-5.2-pro"
GEMINI_MODEL = "gemini-3-pro-preview"


def _get_openai_api_key() -> str | None:
    """Get OpenAI API key from environment."""
    return os.getenv("OPENAI_API_KEY")


def _get_gemini_api_key() -> str | None:
    """Get Gemini API key from environment."""
    return os.getenv("GEMINI_API_KEY")


def validate_api_keys() -> tuple[bool, str]:
    """
    Validate that required API keys are set.

    Returns:
        Tuple of (is_valid, error_message)
    """
    openai_key = _get_openai_api_key()
    gemini_key = _get_gemini_api_key()

    missing = []
    if not openai_key:
        missing.append("OPENAI_API_KEY")
    if not gemini_key:
        missing.append("GEMINI_API_KEY")

    if missing:
        error_lines = [f"ERROR: Missing required environment variable(s): {', '.join(missing)}"]
        error_lines.append("\nSet them with:")
        if "OPENAI_API_KEY" in missing:
            error_lines.append("  export OPENAI_API_KEY='your-openai-key'")
        if "GEMINI_API_KEY" in missing:
            error_lines.append("  export GEMINI_API_KEY='your-gemini-key'")
        return False, "\n".join(error_lines)

    return True, ""


async def query_openai(prompt: str, timeout: int = 60) -> ModelResponse:
    """
    Query OpenAI GPT-5.2 Pro via the Responses API asynchronously.

    Args:
        prompt: The prompt to send to the model
        timeout: Request timeout in seconds

    Returns:
        ModelResponse with content or error information
    """
    api_key = _get_openai_api_key()
    if not api_key:
        return ModelResponse(
            model="GPT-5.2 Pro",
            content="",
            success=False,
            error="OPENAI_API_KEY not set",
            response_time_ms=0
        )

    start_time = time.perf_counter()

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "input": prompt
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)

            if response.status_code != 200:
                return ModelResponse(
                    model="GPT-5.2 Pro",
                    content="",
                    success=False,
                    error=f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time_ms=elapsed_ms
                )

            data = response.json()
            # Extract text from Responses API structure
            content = data["output"][0]["content"][0]["text"]

            return ModelResponse(
                model="GPT-5.2 Pro",
                content=content,
                success=True,
                error=None,
                response_time_ms=elapsed_ms
            )

    except httpx.TimeoutException:
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return ModelResponse(
            model="GPT-5.2 Pro",
            content="",
            success=False,
            error=f"Request timed out after {timeout}s",
            response_time_ms=elapsed_ms
        )
    except httpx.HTTPError as e:
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return ModelResponse(
            model="GPT-5.2 Pro",
            content="",
            success=False,
            error=f"HTTP error: {str(e)}",
            response_time_ms=elapsed_ms
        )
    except KeyError as e:
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return ModelResponse(
            model="GPT-5.2 Pro",
            content="",
            success=False,
            error=f"Unexpected response structure: missing key {e}",
            response_time_ms=elapsed_ms
        )


async def query_gemini(prompt: str, timeout: int = 60) -> ModelResponse:
    """
    Query Google Gemini 3 Pro asynchronously.

    Args:
        prompt: The prompt to send to the model
        timeout: Request timeout in seconds

    Returns:
        ModelResponse with content or error information
    """
    api_key = _get_gemini_api_key()
    if not api_key:
        return ModelResponse(
            model="Gemini 3 Pro",
            content="",
            success=False,
            error="GEMINI_API_KEY not set",
            response_time_ms=0
        )

    start_time = time.perf_counter()

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 8000,
            "temperature": 0.7
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                elapsed_ms = int((time.perf_counter() - start_time) * 1000)

                if response.status != 200:
                    error_text = await response.text()
                    return ModelResponse(
                        model="Gemini 3 Pro",
                        content="",
                        success=False,
                        error=f"HTTP {response.status}: {error_text[:200]}",
                        response_time_ms=elapsed_ms
                    )

                data = await response.json()
                content = data["candidates"][0]["content"]["parts"][0]["text"]

                return ModelResponse(
                    model="Gemini 3 Pro",
                    content=content,
                    success=True,
                    error=None,
                    response_time_ms=elapsed_ms
                )

    except asyncio.TimeoutError:
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return ModelResponse(
            model="Gemini 3 Pro",
            content="",
            success=False,
            error=f"Request timed out after {timeout}s",
            response_time_ms=elapsed_ms
        )
    except aiohttp.ClientError as e:
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return ModelResponse(
            model="Gemini 3 Pro",
            content="",
            success=False,
            error=f"Connection error: {str(e)}",
            response_time_ms=elapsed_ms
        )


async def query_with_retry(
    query_fn: Callable[[str, int], Awaitable[ModelResponse]],
    prompt: str,
    max_retries: int = 2,
    backoff_base: float = 2.0,
    timeout: int = 60
) -> ModelResponse:
    """
    Query a model with exponential backoff retry logic.

    Args:
        query_fn: Async function that performs the API call
        prompt: The prompt to send
        max_retries: Maximum number of retry attempts
        backoff_base: Base for exponential backoff calculation
        timeout: Request timeout in seconds

    Returns:
        ModelResponse from the last attempt
    """
    last_result: ModelResponse | None = None

    for attempt in range(max_retries + 1):
        result = await query_fn(prompt, timeout)

        if result["success"]:
            return result

        last_result = result

        # Don't sleep after the last attempt
        if attempt < max_retries:
            await asyncio.sleep(backoff_base ** attempt)

    # Return the last failed result
    return last_result  # type: ignore


async def query_models_parallel(
    openai_prompt: str,
    gemini_prompt: str,
    timeout: int = 60,
    use_retry: bool = True
) -> tuple[ModelResponse, ModelResponse]:
    """
    Query both OpenAI and Gemini models concurrently using asyncio.gather.

    Args:
        openai_prompt: Prompt for ChatGPT
        gemini_prompt: Prompt for Gemini
        timeout: Request timeout in seconds per model
        use_retry: Whether to use retry logic with backoff

    Returns:
        Tuple of (openai_response, gemini_response)
    """
    if use_retry:
        openai_task = query_with_retry(query_openai, openai_prompt, timeout=timeout)
        gemini_task = query_with_retry(query_gemini, gemini_prompt, timeout=timeout)
    else:
        openai_task = query_openai(openai_prompt, timeout)
        gemini_task = query_gemini(gemini_prompt, timeout)

    results = await asyncio.gather(openai_task, gemini_task, return_exceptions=True)

    # Handle any exceptions that were caught by return_exceptions=True
    openai_result = results[0]
    gemini_result = results[1]

    if isinstance(openai_result, Exception):
        openai_result = ModelResponse(
            model="GPT-5.2 Pro",
            content="",
            success=False,
            error=f"Unexpected error: {str(openai_result)}",
            response_time_ms=0
        )

    if isinstance(gemini_result, Exception):
        gemini_result = ModelResponse(
            model="Gemini 3 Pro",
            content="",
            success=False,
            error=f"Unexpected error: {str(gemini_result)}",
            response_time_ms=0
        )

    return openai_result, gemini_result


def generate_prompt(original_task: str, context_summary: str = "") -> str:
    """
    Generate a prompt for querying external models.

    Args:
        original_task: The original user task/question
        context_summary: Optional context about the task

    Returns:
        Formatted prompt string
    """
    prompt = f"""You are being asked to independently solve the following task:

TASK:
{original_task}

Please provide your complete answer or response to this task. Be thorough and clear.
Provide only your response - no meta-commentary about being an AI or comparing with other models.

YOUR RESPONSE:"""

    if context_summary:
        prompt = f"""CONTEXT:
{context_summary}

{prompt}"""

    return prompt
