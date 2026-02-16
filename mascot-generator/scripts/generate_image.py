#!/usr/bin/env python3
"""
Mascot image generator with chromakey green screen removal.

Generates images via the Gemini API with a green background, then removes
the green to produce transparent PNGs. Optionally resizes and wraps in SVG.

Usage:
    # Generate mascot with green screen removal
    python generate_image.py --prompt "A friendly owl mascot" --output mascot.png --green-screen

    # Generate banner at specific size
    python generate_image.py --prompt "Banner with owl" --output banner.png --size 1200x400 --green-screen

    # With reference images for style consistency
    python generate_image.py --prompt "Same owl in banner" --output banner.png --green-screen \
        --references mascot.png

    # Generate SVG wrapper alongside PNG
    python generate_image.py --prompt "Owl mascot" --output mascot.png --green-screen --svg

Environment:
    GEMINI_API_KEY: API key for Gemini (alternative to --api-key flag)
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import numpy as np
from PIL import Image
from scipy.ndimage import binary_erosion


MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
}

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

GREEN_SCREEN_PROMPT_SUFFIX = (
    "\n\nCRITICAL: The background MUST be solid pure chromakey green (#00FF00). "
    "The ENTIRE background must be uniform #00FF00 green with NO gradients, "
    "NO shadows on the background, NO ground plane. Only the subject itself "
    "should have non-green colors."
)


def generate_image(
    api_key: str,
    prompt: str,
    model: str = "pro",
    green_screen: bool = False,
    reference_image_paths: Optional[list[str]] = None,
) -> bytes:
    """Call Gemini API to generate an image. Returns raw PNG bytes."""
    if model not in MODELS:
        raise ValueError(f"Invalid model: {model}. Choose from: {list(MODELS.keys())}")

    model_id = MODELS[model]
    url = f"{API_BASE}/{model_id}:generateContent?key={api_key}"

    enhanced_prompt = prompt
    if green_screen:
        enhanced_prompt += GREEN_SCREEN_PROMPT_SUFFIX

    # Reference images go first in parts array, text prompt last
    parts: list[dict] = []

    if reference_image_paths:
        for ref_path in reference_image_paths:
            with open(ref_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")
            parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": image_data,
                }
            })

    parts.append({"text": enhanced_prompt})

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
        },
    }

    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))

    candidates = result.get("candidates", [])
    if not candidates:
        raise ValueError("No image generated in response")

    for part in candidates[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])

    raise ValueError("No image data found in response")


def remove_green_screen(
    image: Image.Image,
    hue_center: int = 60,
    hue_range: int = 25,
    min_saturation: int = 75,
    min_value: int = 70,
) -> Image.Image:
    """Remove chromakey green background using HSV thresholds.

    Converts green pixels to transparent, then applies edge cleanup
    (erosion) for clean anti-aliased edges.

    Uses 0-180 hue scale (OpenCV convention) where pure green = 60.
    Default range of ±25 detects hues 35-85 (yellow-green through teal).

    Args:
        image: Input PIL Image (RGB or RGBA).
        hue_center: Center of green hue (0-180 scale). Default 60 (pure green).
        hue_range: Half-width of hue detection window. Default 25 → detects 35-85.
        min_saturation: Minimum saturation to count as green (0-255). Default 75.
        min_value: Minimum brightness to count as green (0-255). Default 70.

    Returns:
        RGBA PIL Image with green pixels replaced by transparency.
    """
    rgba = image.convert("RGBA")
    arr = np.array(rgba)

    # Convert RGB to HSV manually (avoid OpenCV dependency)
    rgb_float = arr[:, :, :3].astype(np.float32) / 255.0
    r, g, b = rgb_float[:, :, 0], rgb_float[:, :, 1], rgb_float[:, :, 2]

    cmax = np.maximum(np.maximum(r, g), b)
    cmin = np.minimum(np.minimum(r, g), b)
    delta = cmax - cmin

    # Hue calculation (0-180 scale to match OpenCV convention)
    hue = np.zeros_like(delta)
    mask_r = (cmax == r) & (delta > 0)
    mask_g = (cmax == g) & (delta > 0)
    mask_b = (cmax == b) & (delta > 0)

    hue[mask_r] = 30 * (((g[mask_r] - b[mask_r]) / delta[mask_r]) % 6)
    hue[mask_g] = 30 * (((b[mask_g] - r[mask_g]) / delta[mask_g]) + 2)
    hue[mask_b] = 30 * (((r[mask_b] - g[mask_b]) / delta[mask_b]) + 4)

    # Saturation (0-255 scale)
    saturation = np.zeros_like(delta)
    nonzero_max = cmax > 0
    saturation[nonzero_max] = (delta[nonzero_max] / cmax[nonzero_max]) * 255

    # Value (0-255 scale)
    value = cmax * 255

    # Detect green pixels
    hue_low = hue_center - hue_range
    hue_high = hue_center + hue_range

    if hue_low < 0:
        hue_mask = (hue >= (hue_low % 180)) | (hue <= hue_high)
    elif hue_high > 180:
        hue_mask = (hue >= hue_low) | (hue <= (hue_high % 180))
    else:
        hue_mask = (hue >= hue_low) & (hue <= hue_high)

    green_mask = hue_mask & (saturation >= min_saturation) & (value >= min_value)

    # Step 1: Set green pixels to fully transparent
    arr[green_mask, 3] = 0

    # Step 2: Erode the opaque region by 1px to remove green fringe
    opaque_mask = arr[:, :, 3] > 0
    eroded = binary_erosion(opaque_mask, iterations=1)
    fringe = opaque_mask & ~eroded

    # Step 3: Green spill reduction on fringe pixels adjacent to green
    from scipy.ndimage import binary_dilation
    near_green = binary_dilation(green_mask, iterations=1) & ~green_mask
    spill_pixels = fringe & near_green

    for coord_y, coord_x in zip(*np.where(spill_pixels)):
        pixel = arr[coord_y, coord_x, :3].astype(np.float32)
        green_excess = max(0.0, pixel[1] - max(pixel[0], pixel[2]))
        arr[coord_y, coord_x, 1] = int(max(0, pixel[1] - green_excess * 0.7))
        arr[coord_y, coord_x, 3] = 200  # partial transparency at spill edges

    # Step 4: Fully remove remaining fringe pixels (not near green spill)
    arr[fringe & ~spill_pixels, 3] = 0

    return Image.fromarray(arr)


def resize_to_png(image: Image.Image, width: int, height: int) -> Image.Image:
    """Resize image to exact dimensions using LANCZOS resampling."""
    return image.resize((width, height), Image.LANCZOS)


def png_to_svg_embed(png_path: str, width: int, height: int) -> str:
    """Create an SVG file that embeds a PNG as base64.

    Returns the SVG content as a string.
    """
    with open(png_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg"\n'
        '     xmlns:xlink="http://www.w3.org/1999/xlink"\n'
        f'     width="{width}" height="{height}"\n'
        f'     viewBox="0 0 {width} {height}">\n'
        f'  <image width="{width}" height="{height}"\n'
        f'         href="data:image/png;base64,{b64_data}"/>\n'
        '</svg>\n'
    )


def parse_size(size_str: str) -> tuple[int, int]:
    """Parse a 'WIDTHxHEIGHT' string into (width, height) tuple."""
    parts = size_str.lower().split("x")
    if len(parts) != 2:
        raise ValueError(f"Invalid size format: {size_str}. Use WIDTHxHEIGHT (e.g., 256x256)")
    return int(parts[0]), int(parts[1])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate mascot images with optional green screen removal",
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
        required=True,
        help="Text prompt describing the image to generate",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path (e.g., mascot.png)",
    )
    parser.add_argument(
        "--size",
        help="Target size as WIDTHxHEIGHT (e.g., 256x256, 1200x400). "
             "Image is generated then resized to these exact dimensions.",
    )
    parser.add_argument(
        "--references",
        nargs="+",
        help="Reference image paths for style consistency",
    )
    parser.add_argument(
        "--model",
        choices=["flash", "pro"],
        default="pro",
        help="Model to use: flash (fast, drafts) or pro (quality, final assets)",
    )
    parser.add_argument(
        "--green-screen",
        action="store_true",
        help="Generate on green background and remove it for transparency",
    )
    parser.add_argument(
        "--svg",
        action="store_true",
        help="Also generate an SVG wrapper with embedded PNG",
    )
    parser.add_argument(
        "--hue-center",
        type=int,
        default=60,
        help="HSV hue center for green detection, 0-180 scale (default: 60 = pure green)",
    )
    parser.add_argument(
        "--hue-range",
        type=int,
        default=25,
        help="HSV hue half-width for green detection (default: 25 → detects 35-85)",
    )
    parser.add_argument(
        "--min-saturation",
        type=int,
        default=75,
        help="Minimum saturation for green detection (default: 75)",
    )
    parser.add_argument(
        "--min-value",
        type=int,
        default=70,
        help="Minimum value/brightness for green detection (default: 70)",
    )

    args = parser.parse_args()

    if not args.api_key:
        print("Error: API key required. Use --api-key or set GEMINI_API_KEY")
        return 1

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate image
    print(f"Generating image with {args.model} model... ", end="", flush=True)
    image_bytes = generate_image(
        api_key=args.api_key,
        prompt=args.prompt,
        model=args.model,
        green_screen=args.green_screen,
        reference_image_paths=args.references,
    )
    print("done.")

    # Load as PIL Image
    import io
    image = Image.open(io.BytesIO(image_bytes))

    # Remove green screen if requested
    if args.green_screen:
        print("Removing green screen... ", end="", flush=True)
        image = remove_green_screen(
            image,
            hue_center=args.hue_center,
            hue_range=args.hue_range,
            min_saturation=args.min_saturation,
            min_value=args.min_value,
        )
        print("done.")

    # Resize if target size specified
    if args.size:
        width, height = parse_size(args.size)
        print(f"Resizing to {width}x{height}... ", end="", flush=True)
        image = resize_to_png(image, width, height)
        print("done.")

    # Save PNG
    image.save(str(output_path), "PNG")
    file_size_kb = output_path.stat().st_size / 1024
    print(f"Saved: {output_path} ({file_size_kb:.0f} KB)")

    # Verify transparency if green screen was used
    if args.green_screen:
        arr = np.array(image)
        if arr.shape[2] == 4:
            transparent_pct = (arr[:, :, 3] == 0).sum() / arr[:, :, 3].size * 100
            print(f"Transparency: {transparent_pct:.1f}% of pixels are transparent")

    # Generate SVG wrapper if requested
    if args.svg:
        svg_path = output_path.with_suffix(".svg")
        img_width, img_height = image.size
        svg_content = png_to_svg_embed(str(output_path), img_width, img_height)
        svg_path.write_text(svg_content)
        svg_size_kb = svg_path.stat().st_size / 1024
        print(f"Saved: {svg_path} ({svg_size_kb:.0f} KB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
