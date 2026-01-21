"""
Response analysis utilities for the second-opinion skill.

This module provides basic utilities for extracting structural info
from responses. The actual analysis is performed by Claude.
"""


def extract_response_metadata(response: str) -> dict:
    """
    Extract basic metadata from a response for display purposes.

    Args:
        response: The model's response text

    Returns:
        Dictionary with basic metrics
    """
    if not response:
        return {
            'word_count': 0,
            'has_code': False,
            'has_lists': False,
        }

    words = response.split()

    return {
        'word_count': len(words),
        'has_code': '```' in response,
        'has_lists': '\n-' in response or '\n*' in response or '\n1.' in response,
    }


def identify_structural_differences(
    claude_response: str,
    chatgpt_response: str | None,
    gemini_response: str | None
) -> list[str]:
    """
    Identify basic structural differences between responses.

    Args:
        claude_response: Claude's response
        chatgpt_response: ChatGPT's response (None if failed)
        gemini_response: Gemini's response (None if failed)

    Returns:
        List of structural observations
    """
    observations = []

    if not chatgpt_response and not gemini_response:
        return ["Only Claude's response available"]

    if not chatgpt_response:
        observations.append("ChatGPT response unavailable")
    if not gemini_response:
        observations.append("Gemini response unavailable")

    claude_meta = extract_response_metadata(claude_response)
    chatgpt_meta = extract_response_metadata(chatgpt_response) if chatgpt_response else None
    gemini_meta = extract_response_metadata(gemini_response) if gemini_response else None

    # Note code usage differences
    if chatgpt_meta and claude_meta['has_code'] != chatgpt_meta['has_code']:
        observations.append("Claude and ChatGPT differ in code example usage")
    if gemini_meta and claude_meta['has_code'] != gemini_meta['has_code']:
        observations.append("Claude and Gemini differ in code example usage")

    # Note list usage differences
    if chatgpt_meta and claude_meta['has_lists'] != chatgpt_meta['has_lists']:
        observations.append("Claude and ChatGPT differ in list formatting")
    if gemini_meta and claude_meta['has_lists'] != gemini_meta['has_lists']:
        observations.append("Claude and Gemini differ in list formatting")

    return observations if observations else ["All responses use similar formatting"]
