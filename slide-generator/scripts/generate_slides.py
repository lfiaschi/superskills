#!/usr/bin/env python3
"""
Slide Generator using Google's Gemini Image Generation API.

This script generates professional presentation slides by calling the Gemini API
with optimized prompts for slide creation.

Usage:
    # Single slide from prompt
    python generate_slides.py --api-key KEY --prompt "Your prompt" --output slide.png

    # Batch generation from JSON file (recommended)
    python generate_slides.py --api-key KEY --prompts-file prompts.json --output-dir ./slides

    # With style consistency (default: anchor strategy)
    python generate_slides.py --api-key KEY --prompts-file prompts.json \
        --output-dir ./slides --model pro --reference-strategy anchor

Reference Strategies:
    - anchor: Slide 1 always included + previous slide (RECOMMENDED - prevents style drift)
    - progressive: Each slide references only the previous slide (causes style drift)
    - none: No reference images used

Environment:
    GEMINI_API_KEY: API key for Gemini (alternative to --api-key flag)
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError


# Model configurations
MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
}

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

# Resolution mappings
RESOLUTIONS = {
    "1K": "1024x1024",
    "2K": "2048x2048",
    "4K": "4096x4096",
}

# Style consistency instructions (appended when reference images are provided)
STYLE_INSTRUCTIONS = """
CRITICAL STYLE INSTRUCTIONS:
You are provided with reference slide(s) from this presentation deck.
You MUST maintain overall visual cohesive style that is EXACTLY consistent with these reference images:
- Analyze the reference images and use the EXACT same background color
- Use the EXACT same typography style, font family, and font weights
- Use the EXACT same color palette for text and accent elements
- Maintain the same spacing, margins, padding, and layout grid
- Keep the same visual hierarchy, text sizing ratios, and element positioning
- Match the same style for callout boxes, bullet points, and visual elements
- The new slide MUST look like it belongs in the same professional deck as the reference slides
- Do NOT deviate from the established visual language
"""


def generate_image(
    api_key: str,
    prompt: str,
    model: str = "pro",
    aspect_ratio: str = "16:9",
    resolution: str = "4K",
    reference_image_paths: Optional[list[str]] = None,
) -> bytes:
    """
    Generate a slide image using the Gemini API.

    Args:
        api_key: Gemini API key
        prompt: Text prompt describing the slide
        model: Model to use ('flash' or 'pro')
        aspect_ratio: Slide aspect ratio (e.g., '16:9')
        resolution: Output resolution ('1K', '2K', '4K')
        reference_image_paths: Optional list of paths to reference images for style consistency

    Returns:
        Image bytes (PNG format)

    Raises:
        HTTPError: If API request fails
        ValueError: If model or resolution is invalid
    """
    if model not in MODELS:
        raise ValueError(f"Invalid model: {model}. Choose from: {list(MODELS.keys())}")

    if resolution not in RESOLUTIONS:
        raise ValueError(f"Invalid resolution: {resolution}. Choose from: {list(RESOLUTIONS.keys())}")

    model_id = MODELS[model]
    url = f"{API_BASE}/{model_id}:generateContent?key={api_key}"

    # Build request content with aspect ratio and resolution in prompt
    enhanced_prompt = f"{prompt}\n\nIMPORTANT: Generate as a {aspect_ratio} aspect ratio slide at {resolution} resolution."

    # Add style consistency instructions if reference images are provided
    if reference_image_paths:
        enhanced_prompt += STYLE_INSTRUCTIONS

    # Build request parts - reference images first, then text prompt
    parts = []

    # Add reference images
    if reference_image_paths:
        for ref_path in reference_image_paths:
            with open(ref_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")
            parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": image_data
                }
            })

    # Add text prompt
    parts.append({"text": enhanced_prompt})

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"]
        }
    }

    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))

    # Extract image from response
    candidates = result.get("candidates", [])
    if not candidates:
        raise ValueError("No image generated in response")

    parts = candidates[0].get("content", {}).get("parts", [])
    for part in parts:
        if "inlineData" in part:
            image_b64 = part["inlineData"]["data"]
            return base64.b64decode(image_b64)

    raise ValueError("No image data found in response")


def load_prompts_file(path: str) -> list[dict]:
    """
    Load prompts from a JSON file.

    Expected format:
    [
        {"name": "slide_01", "prompt": "Create a title slide..."},
        {"name": "slide_02", "prompt": "Create a content slide..."}
    ]

    Or simple list of prompts:
    ["Create a title slide...", "Create a content slide..."]
    """
    with open(path, "r") as f:
        data = json.load(f)

    if isinstance(data, list):
        if all(isinstance(item, str) for item in data):
            # Simple list of prompts
            return [{"name": f"slide_{i+1:02d}", "prompt": p} for i, p in enumerate(data)]
        return data

    raise ValueError("Prompts file must be a JSON array")


def get_reference_paths(
    strategy: str,
    slide_index: int,
    generated_slides: list[str],
    first_slide_path: Optional[str],
) -> Optional[list[str]]:
    """
    Determine which reference images to use based on strategy.

    Args:
        strategy: Reference strategy ('anchor', 'progressive', 'none')
        slide_index: Current slide index (0-based)
        generated_slides: List of paths to previously generated slides
        first_slide_path: Path to the first slide (style anchor)

    Returns:
        List of reference image paths, or None if no references
    """
    if strategy == "none" or slide_index == 0:
        return None

    if strategy == "progressive":
        # Each slide references only the previous slide (causes style drift!)
        return [generated_slides[-1]]

    if strategy == "anchor":
        # Slide 1 always included + previous slide (RECOMMENDED)
        if slide_index == 1:
            return [first_slide_path]
        else:
            return [first_slide_path, generated_slides[-1]]

    return None


def generate_batch(
    api_key: str,
    prompts: list[dict],
    output_dir: str,
    model: str = "pro",
    aspect_ratio: str = "16:9",
    resolution: str = "4K",
    reference_strategy: str = "anchor",
    delay_between_requests: float = 2.0,
) -> list[str]:
    """
    Generate multiple slides from a list of prompts.

    Args:
        api_key: Gemini API key
        prompts: List of prompt dictionaries with 'name' and 'prompt' keys
        output_dir: Directory to save generated images
        model: Model to use
        aspect_ratio: Slide aspect ratio
        resolution: Output resolution
        reference_strategy: How to use reference images ('anchor', 'progressive', 'none')
        delay_between_requests: Seconds to wait between API calls

    Returns:
        List of generated file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    generated_files = []
    first_slide_path = None

    for i, item in enumerate(prompts):
        name = item.get("name", f"slide_{i+1:02d}")
        prompt = item["prompt"]

        # Get reference images based on strategy
        reference_paths = get_reference_paths(
            strategy=reference_strategy,
            slide_index=i,
            generated_slides=generated_files,
            first_slide_path=first_slide_path,
        )

        # Build info string for logging
        if reference_paths:
            ref_names = [Path(p).stem for p in reference_paths]
            ref_info = f"refs: {', '.join(ref_names)}"
        else:
            ref_info = "no reference"

        print(f"Generating {name} ({ref_info})... ", end="", flush=True)

        image_bytes = generate_image(
            api_key=api_key,
            prompt=prompt,
            model=model,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            reference_image_paths=reference_paths,
        )

        output_file = output_path / f"{name}.png"
        with open(output_file, "wb") as f:
            f.write(image_bytes)

        generated_files.append(str(output_file))

        # Store first slide as style anchor
        if i == 0:
            first_slide_path = str(output_file)

        print(f"saved to {output_file}")

        # Rate limiting
        if i < len(prompts) - 1:
            time.sleep(delay_between_requests)

    return generated_files


def assemble_pdf(image_paths: list[str], output_path: str) -> None:
    """
    Assemble slide images into a PDF document.

    Requires: Pillow library
    """
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow library required for PDF assembly.")
        print("Install with: pip install Pillow")
        sys.exit(1)

    if not image_paths:
        print("No images to assemble")
        return

    images = [Image.open(p).convert("RGB") for p in sorted(image_paths)]
    images[0].save(output_path, save_all=True, append_images=images[1:])
    print(f"PDF assembled: {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate presentation slides using Gemini Image Generation API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--api-key",
        default=os.environ.get("GEMINI_API_KEY"),
        help="Gemini API key (or set GEMINI_API_KEY env var)",
    )
    parser.add_argument(
        "--prompt",
        help="Single prompt for slide generation",
    )
    parser.add_argument(
        "--prompts-file",
        help="JSON file containing list of prompts",
    )
    parser.add_argument(
        "--output",
        help="Output file path (for single slide)",
    )
    parser.add_argument(
        "--output-dir",
        default="./slides",
        help="Output directory (for batch generation)",
    )
    parser.add_argument(
        "--model",
        choices=["flash", "pro"],
        default="pro",
        help="Model to use: flash (fast) or pro (high quality)",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        help="Slide aspect ratio (e.g., 16:9, 4:3, 1:1)",
    )
    parser.add_argument(
        "--resolution",
        choices=["1K", "2K", "4K"],
        default="4K",
        help="Output resolution (default: 4K)",
    )
    parser.add_argument(
        "--reference-strategy",
        choices=["anchor", "progressive", "none"],
        default="anchor",
        help="Reference strategy for style consistency: "
             "'anchor' (recommended) always includes slide 1 + previous slide, "
             "'progressive' uses only previous slide (causes drift), "
             "'none' uses no references",
    )
    parser.add_argument(
        "--assemble",
        action="store_true",
        help="Assemble generated images into PDF",
    )
    parser.add_argument(
        "--format",
        choices=["pdf"],
        default="pdf",
        help="Output format for assembly",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay between API requests (seconds)",
    )
    # Keep --progressive for backwards compatibility, but mark as deprecated
    parser.add_argument(
        "--progressive",
        action="store_true",
        help="DEPRECATED: Use --reference-strategy=progressive instead",
    )

    args = parser.parse_args()

    if not args.api_key:
        print("Error: API key required. Use --api-key or set GEMINI_API_KEY")
        return 1

    # Handle deprecated --progressive flag
    reference_strategy = args.reference_strategy
    if args.progressive:
        print("Warning: --progressive is deprecated. Use --reference-strategy=progressive instead.")
        reference_strategy = "progressive"

    # Single slide generation
    if args.prompt:
        output = args.output or "slide.png"
        print(f"Generating slide... ", end="", flush=True)

        image_bytes = generate_image(
            api_key=args.api_key,
            prompt=args.prompt,
            model=args.model,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
        )

        with open(output, "wb") as f:
            f.write(image_bytes)
        print(f"saved to {output}")
        return 0

    # Batch generation from file
    if args.prompts_file:
        prompts = load_prompts_file(args.prompts_file)
        generated = generate_batch(
            api_key=args.api_key,
            prompts=prompts,
            output_dir=args.output_dir,
            model=args.model,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
            reference_strategy=reference_strategy,
            delay_between_requests=args.delay,
        )

        if args.assemble and generated:
            pdf_path = Path(args.output_dir) / "slides.pdf"
            assemble_pdf(generated, str(pdf_path))

        return 0

    # Assembly only mode
    if args.assemble:
        output_dir = Path(args.output_dir)
        images = sorted(output_dir.glob("*.png"))
        if images:
            pdf_path = output_dir / "slides.pdf"
            assemble_pdf([str(p) for p in images], str(pdf_path))
        else:
            print(f"No PNG files found in {args.output_dir}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
