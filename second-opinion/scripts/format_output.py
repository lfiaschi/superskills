"""
Output formatting module for the second-opinion skill.

Formats responses for presentation to Claude, who will perform
the actual comparative analysis.
"""


def _format_response_time(ms: int) -> str:
    """Format response time in human-readable format."""
    if ms == 0:
        return "N/A"
    if ms < 1000:
        return f"{ms}ms"
    return f"{ms / 1000:.1f}s"


def _format_error_notice(errors: dict) -> str:
    """Format error notice for partial failures."""
    if not errors:
        return ""

    notice = "\n## Partial Failures\n\n"
    for model, error in errors.items():
        notice += f"- **{model}**: {error}\n"
    return notice


def _format_timing_info(response_times: dict) -> str:
    """Format response timing information."""
    if not response_times:
        return ""

    times = []
    for model, ms in response_times.items():
        times.append(f"{model}: {_format_response_time(ms)}")

    return f"\n*Response times: {' | '.join(times)}*\n"


def format_responses(
    claude_response: str,
    chatgpt_response: str | None,
    gemini_response: str | None,
    original_task: str,
    response_times: dict | None = None,
    errors: dict | None = None
) -> str:
    """
    Format all responses for Claude to analyze.

    Args:
        claude_response: Claude's original response
        chatgpt_response: ChatGPT's response (None if failed)
        gemini_response: Gemini's response (None if failed)
        original_task: The original user task
        response_times: Dict of model -> response time in ms
        errors: Dict of model -> error message for failures

    Returns:
        Formatted markdown string for Claude to analyze
    """
    output = """# Second Opinion Results

## Original Task

"""
    output += original_task + "\n"

    # Add error notice if any
    if errors:
        output += _format_error_notice(errors)

    output += """
---

## Claude's Response

"""
    output += claude_response + "\n"

    output += """
---

## GPT-5.2 Pro's Response

"""
    if chatgpt_response:
        output += chatgpt_response + "\n"
    else:
        output += "*[Response unavailable]*\n"

    output += """
---

## Gemini 3 Pro's Response

"""
    if gemini_response:
        output += gemini_response + "\n"
    else:
        output += "*[Response unavailable]*\n"

    output += "\n---\n"

    # Add timing info
    if response_times:
        output += _format_timing_info(response_times)

    return output


def format_analysis_prompt() -> str:
    """
    Return the prompt for Claude to analyze the responses.

    Returns:
        Analysis instruction string
    """
    return """
---

## Your Analysis Task

Please provide an objective comparative analysis of the three responses above:

1. **Accuracy**: Which response(s) are factually correct? Are there any errors?
2. **Completeness**: Which response best addresses all aspects of the task?
3. **Clarity**: Which response is most clear and well-organized?
4. **Best Response**: Which response would you recommend and why?

Be impartial - acknowledge if your original response was not the best.
"""
