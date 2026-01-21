"""
Context extraction module for the second-opinion skill.

Extracts the original task, Claude's response, and determines
content type and length from conversation history.
"""

import json
import re
from typing import TypedDict


class ExtractedContext(TypedDict):
    """Extracted context from conversation."""
    original_task: str
    claude_response: str
    content_type: str  # 'qa', 'creative', 'code', 'strategic', 'analysis'
    response_length: str  # 'short', 'medium', 'long'
    word_count: int


def classify_content_type(text: str) -> str:
    """Classify the type of content based on characteristics."""
    text_lower = text.lower()

    # Check for code indicators
    if any(pattern in text for pattern in ['```', 'def ', 'class ', 'function ', 'import ', 'async ', 'await ']):
        return 'code'

    # Check for creative content indicators
    creative_markers = ['draft', 'write', 'compose', 'post', 'email', 'letter', 'story', 'poem']
    if any(marker in text_lower for marker in creative_markers):
        return 'creative'

    # Check for strategic/advisory indicators
    strategic_markers = ['recommend', 'strategy', 'approach', 'decision', 'plan', 'should', 'best practice']
    if any(marker in text_lower for marker in strategic_markers):
        return 'strategic'

    # Check for analysis indicators
    analysis_markers = ['analyze', 'explain', 'breakdown', 'comparison', 'evaluate', 'assessment']
    if any(marker in text_lower for marker in analysis_markers):
        return 'analysis'

    # Default to Q&A
    return 'qa'


def categorize_length(word_count: int) -> str:
    """Categorize content length."""
    if word_count < 200:
        return 'short'
    elif word_count < 1000:
        return 'medium'
    else:
        return 'long'


def count_words(text: str) -> int:
    """Count words in text."""
    words = text.split()
    return len(words)


def extract_context(conversation_history: list, last_claude_message: str) -> ExtractedContext:
    """
    Extract context from conversation history and Claude's last response.

    Args:
        conversation_history: List of conversation messages in format:
                              [{'role': 'user'/'assistant', 'content': 'text'}, ...]
        last_claude_message: Claude's most recent response text

    Returns:
        ExtractedContext with extracted task, response, type, and length info
    """
    # Find the original user task (usually the first or most recent substantive user message)
    original_task = ""
    for msg in reversed(conversation_history):
        if msg.get('role') == 'user' and len(msg.get('content', '')) > 20:
            original_task = msg.get('content', '')
            break

    # If no good task found, look for the most recent user message
    if not original_task:
        for msg in reversed(conversation_history):
            if msg.get('role') == 'user':
                original_task = msg.get('content', '')
                if original_task:
                    break

    # Classify content
    word_count = count_words(last_claude_message)
    content_type = classify_content_type(last_claude_message)
    response_length = categorize_length(word_count)

    return ExtractedContext(
        original_task=original_task,
        claude_response=last_claude_message,
        content_type=content_type,
        response_length=response_length,
        word_count=word_count
    )


def extract_from_json(conversation_json: str, last_claude_message: str) -> ExtractedContext:
    """
    Extract context from JSON conversation format.

    Args:
        conversation_json: JSON string of conversation history
        last_claude_message: Claude's most recent response text

    Returns:
        ExtractedContext with extracted data
    """
    try:
        history = json.loads(conversation_json)
        return extract_context(history, last_claude_message)
    except json.JSONDecodeError:
        # Fallback: treat as plain text
        return ExtractedContext(
            original_task="Unable to parse conversation history",
            claude_response=last_claude_message,
            content_type="qa",
            response_length=categorize_length(count_words(last_claude_message)),
            word_count=count_words(last_claude_message)
        )
