"""
Main orchestrator for the second-opinion skill.

This module coordinates the workflow:
1. Validates API keys
2. Extracts context from conversation
3. Queries ChatGPT and Gemini IN PARALLEL via asyncio
4. Formats responses for Claude to analyze

Claude performs the actual comparative analysis.
"""

import asyncio
import json
import sys

from extract_context import extract_context
from api_clients import (
    validate_api_keys,
    query_models_parallel,
    generate_prompt,
)
from format_output import format_responses, format_analysis_prompt


async def run_second_opinion_async(
    conversation_history: list,
    claude_response: str,
    timeout: int = 300
) -> str:
    """
    Fetch responses from ChatGPT and Gemini, format for Claude to analyze.

    Args:
        conversation_history: List of conversation messages
        claude_response: Claude's response
        timeout: Timeout for API calls in seconds

    Returns:
        Formatted output string for Claude to analyze
    """
    # Step 1: Validate environment
    is_valid, error_msg = validate_api_keys()
    if not is_valid:
        return error_msg

    # Step 2: Extract context
    context = extract_context(conversation_history, claude_response)
    original_task = context['original_task']

    # Step 3: Prepare prompt
    prompt = generate_prompt(original_task, f"Claude's response:\n{claude_response}")

    # Step 4: Query both models IN PARALLEL
    openai_result, gemini_result = await query_models_parallel(
        prompt, prompt, timeout=timeout, use_retry=True
    )

    # Step 5: Extract responses and metadata
    chatgpt_response = openai_result["content"] if openai_result["success"] else None
    gemini_response = gemini_result["content"] if gemini_result["success"] else None

    response_times = {
        "GPT-5.2 Pro": openai_result["response_time_ms"],
        "Gemini 3 Pro": gemini_result["response_time_ms"]
    }

    errors = {}
    if not openai_result["success"]:
        errors["GPT-5.2 Pro"] = openai_result["error"]
    if not gemini_result["success"]:
        errors["Gemini 3 Pro"] = gemini_result["error"]

    # If both failed, return error
    if not chatgpt_response and not gemini_response:
        return _format_total_failure(errors)

    # Step 6: Format responses for Claude
    formatted = format_responses(
        claude_response=claude_response,
        chatgpt_response=chatgpt_response,
        gemini_response=gemini_response,
        original_task=original_task,
        response_times=response_times,
        errors=errors if errors else None
    )

    # Step 7: Add analysis prompt for Claude
    formatted += format_analysis_prompt()

    return formatted


def _format_total_failure(errors: dict) -> str:
    """Format error message when both models fail."""
    output = "# Second Opinion - Error\n\n"
    output += "Both external models failed to respond:\n\n"

    for model, error in errors.items():
        output += f"- **{model}**: {error}\n"

    output += "\nPlease check your API keys and network connection, then try again.\n"
    return output


def run_second_opinion(
    conversation_history: list,
    claude_response: str,
    timeout: int = 300
) -> str:
    """
    Synchronous wrapper for run_second_opinion_async.

    Args:
        conversation_history: List of conversation messages
        claude_response: Claude's response
        timeout: Timeout for API calls in seconds

    Returns:
        Formatted output string for Claude to analyze
    """
    return asyncio.run(
        run_second_opinion_async(conversation_history, claude_response, timeout)
    )


def main():
    """
    Main entry point.

    Accepts JSON input via stdin with the following structure:
    {
        "conversation_history": [{"role": "user", "content": "..."}, ...],
        "claude_response": "..."
    }

    If no stdin input is provided, runs a test example.
    """
    # Check if there's input from stdin
    if not sys.stdin.isatty():
        try:
            input_data = json.load(sys.stdin)
            conversation_history = input_data.get("conversation_history", [])
            claude_response = input_data.get("claude_response", "")

            if not conversation_history or not claude_response:
                print("ERROR: JSON input must contain 'conversation_history' and 'claude_response'")
                sys.exit(1)

            result = run_second_opinion(conversation_history, claude_response)
            print(result)
            return
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON input: {e}")
            sys.exit(1)

    # Fallback to test mode
    example_conversation = [
        {'role': 'user', 'content': 'What is the capital of France?'},
        {'role': 'assistant', 'content': 'The capital of France is Paris.'}
    ]

    example_claude_response = "The capital of France is Paris."

    print("Second-Opinion Skill - Test Run\n")
    result = run_second_opinion(example_conversation, example_claude_response)
    print(result)


if __name__ == '__main__':
    main()
