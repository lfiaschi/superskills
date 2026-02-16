# Image Format & Specification Guide

Reference document for mascot generator asset specifications, green screen parameters, and best practices.

---

## Asset Dimensions

| Asset | Width | Height | Aspect Ratio | Format | Notes |
|-------|-------|--------|-------------|--------|-------|
| **Mascot** | 256 | 256 | 1:1 | PNG (RGBA) | Transparent background |
| **Banner** | 1200 | 400 | 3:1 | PNG (RGBA) | Transparent background, for README header |
| **Social Preview (OG)** | 1280 | 640 | 2:1 | PNG (RGBA) | Under 1 MB, transparent or with background |
| **Favicon** | 32 | 32 | 1:1 | PNG / ICO | Simplified silhouette version |

### Size Guidelines

- **Mascot PNG:** Typically 50-80 KB
- **Banner PNG:** Typically 300-500 KB
- **Social Preview PNG:** Must be under 1 MB for GitHub/social platforms
- **SVG wrappers:** Roughly 1.33x the PNG size (base64 encoding overhead)

---

## Green Screen Specifications

### Generation Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Background color | `#00FF00` (pure chromakey green) | Must be uniform, no gradients |
| Background RGB | `(0, 255, 0)` | Maximum green channel |
| Background HSV | `(120°, 100%, 100%)` | Pure green in HSV space |

### HSV Detection Thresholds

Uses the 0-180 hue scale (OpenCV convention) where pure green = 60. These parameters control which pixels are identified as "green background" and converted to transparent:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `hue_center` | 60 | Center of green hue (0-180 scale, pure green) |
| `hue_range` | 25 | Half-width of hue window → detects 35-85 |
| `min_saturation` | 75 | Minimum saturation (0-255 scale) to count as green |
| `min_value` | 70 | Minimum brightness (0-255 scale) to count as green |

### HSV Hue Ranges Affected (0-180 scale)

```
0          35     60     85              180
├──────────┤██████████████┤───────────────┤
   Safe        REMOVED        Safe
   (reds,      (greens,       (blues,
    oranges,    teals)         purples,
    yellows)                   magentas)
```

**Scale conversion:** 0-180 scale × 2 = 0-360° degrees. So 35-85 on 0-180 = 70°-170° on 0-360°.

### Edge Cleanup

After initial green removal, apply morphological operations to clean anti-aliased edges:

1. **Binary erosion** (1 iteration, 3×3 kernel) — shrinks the alpha mask slightly to remove green fringe
2. **Gaussian blur** on alpha channel (sigma=0.5) — smooths jagged edges
3. **Threshold** alpha at 128 — re-binarize after blur for clean edges

---

## SVG Wrapper Format

SVGs are created by embedding the PNG as a base64 data URI inside an SVG container. This preserves the raster quality while providing a scalable container.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="[WIDTH]" height="[HEIGHT]"
     viewBox="0 0 [WIDTH] [HEIGHT]">
  <image width="[WIDTH]" height="[HEIGHT]"
         href="data:image/png;base64,[BASE64_DATA]"/>
</svg>
```

### Why PNG-in-SVG?

- SVG format is expected by many design tools and documentation systems
- Preserves the exact raster quality of the Gemini-generated image
- Maintains transparency information
- Scales cleanly in browsers and renderers
- GitHub renders SVGs natively in README files

---

## Prompt Engineering for Green Screen

### Effective Prompt Patterns

**Strong green screen instructions (include in every prompt):**
```
CRITICAL: The background MUST be solid pure chromakey green (#00FF00).
The ENTIRE background must be uniform #00FF00 green with NO gradients,
NO shadows on the background, NO ground plane. Only the character itself
should have non-green colors. The character must NOT contain any green
or teal colors (no greens, no teals, no lime, no emerald, no mint).
```

**For banner/wide compositions:**
```
The composition should have the character on one side and text on the other.
ALL empty space must be filled with solid #00FF00 green. No floor, no surface,
no shadow casting onto the background. The character floats on pure green.
```

### Common Pitfalls

| Pitfall | What Happens | Prevention |
|---------|-------------|------------|
| Saying "transparent background" | Gemini draws a checkerboard pattern | Always say "chromakey green #00FF00" |
| Mentioning "ground" or "floor" | Gemini adds a surface/shadow | Say "floating on pure green, no ground" |
| Using "green" in character description | Character gets green parts removed | Exclude all green/teal from character palette |
| Requesting gradients | Background gets gradient green | Specify "uniform, solid, single color" |
| Complex scenes | Green bleeds into reflections | Keep compositions simple and flat |

---

## README Integration

### Banner Embedding

```markdown
<p align="center">
  <img src="images/banner.png" alt="[Project Name]" width="600">
</p>
```

### With Dark/Light Mode Support

If you generate both themed versions:
```markdown
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="images/banner-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="images/banner-light.png">
    <img src="images/banner-light.png" alt="[Project Name]" width="600">
  </picture>
</p>
```

### Transparent banners work on both themes by default — no need for separate versions unless the text color needs to change.

---

## Gemini API Reference

### Models

| Model | ID | Best For |
|-------|----|----------|
| Pro | `gemini-3-pro-image-preview` | Final assets, text-heavy images |
| Flash | `gemini-2.5-flash-image` | Drafts, iterations, quick tests |

### API Configuration

```python
generation_config = {
    "responseModalities": ["IMAGE"]
}
```

### Supported Aspect Ratios

`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

### Supported Resolutions (Pro model only)

`1K` (1024), `2K` (2048), `4K` (4096)

### Reference Images

- Up to 14 reference images supported (Pro model)
- Include the approved mascot as reference when generating banner/social assets
- Reference images go first in the `parts` array, text prompt last
