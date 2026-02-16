---
name: mascot-generator
description: Generates project mascots, banners, and social preview images with transparent backgrounds using Gemini image generation and chromakey green screen removal. Use this skill when users want to create branding assets (mascots, logos, banners) for their project or repository.
---

# Mascot Generator

Generate transparent mascots, banners, and social preview images for any project using Gemini image generation + chromakey green screen removal.

## Before You Start

```bash
# Verify API key is set
[ -n "$GEMINI_API_KEY" ] && echo "Ready" || echo "Set GEMINI_API_KEY first"
```

If not set, tell the user to run `export GEMINI_API_KEY='...'` and stop.

**Required Python packages** (install if missing):
```bash
pip install Pillow scipy numpy
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  PHASE 0        PHASE 1          PHASE 2       PHASE 3        PHASE 4      │
│  ────────       ────────         ────────      ────────       ────────      │
│                                                                             │
│  ┌──────────┐  ┌───────────┐   ┌─────────┐  ┌──────────┐  ┌────────────┐  │
│  │ Repo     │  │ Creative  │   │  User   │  │ Iterate  │  │ Final      │  │
│  │ Analyst  │→ │ Director  │ → │  Picks  │→ │ & Refine │→ │ Assets     │  │
│  │          │  │ (5 ideas) │   │ Winner  │  │ (5 vars) │  │ PNG + SVG  │  │
│  └──────────┘  └───────────┘   └─────────┘  └──────────┘  └────────────┘  │
│       │              │              │              │              │         │
│  Identity        Concepts       Selection     Variations     Mascot 256²   │
│  Brief           with palette                                Banner 1200×  │
│                                                              Social 1280×  │
│                                                                             │
│  PHASE 5: README Integration — embed banner at top of README               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## The Process

```
0. DISCOVER  →  1. BRAINSTORM  →  2. SELECT  →  3. REFINE  →  4. ASSETS  →  5. README
   ────────      ──────────       ────────      ──────────     ────────      ──────
   Repo          5 mascot         User picks    5 variations   Generate      Embed
   identity      concepts         direction     on chosen      final PNGs    banner
```

---

## Phase 0: Repo Discovery

**Goal:** Understand the project's identity and branding context.

**Launch the agent:**

Use the Task tool to spawn the `repo-analyst` subagent:
- **subagent_type:** Reference `agents/repo_analyst.md`
- **prompt:** Include the repo root path and ask for a Project Identity Brief

**What the Repo Analyst does:**
1. Reads README.md, CLAUDE.md, pyproject.toml, package.json, etc.
2. Identifies: project name, tagline, tech stack, domain, existing branding/colors
3. Outputs a structured **Project Identity Brief**

**Output:** Project Identity Brief (name, tagline, domain, tech stack, personality, existing colors)

---

## Phase 1: Creative Brainstorm

**Goal:** Generate 5 diverse mascot concepts that fit the project's identity.

**Launch the agent:**

Use the Task tool to spawn the `creative-director` subagent:
- **subagent_type:** Reference `agents/creative_director.md`
- **prompt:** Include the Project Identity Brief from Phase 0

**What the Creative Director does:**
1. Receives the Project Identity Brief
2. Brainstorms 5 diverse mascot concepts (different animals/characters, different metaphors)
3. For each: name, description, why it fits, color palette, pose at multiple sizes
4. **Avoids green/teal tones** in all palette suggestions (see Color Palette Warning below)

**Output:** 5 mascot concepts with full descriptions

### Present to User

```markdown
## Mascot Concepts

Here are 5 directions for your project mascot:

### 1. [Name] — [Animal/Character]
**Character:** [Description]
**Why it fits:** [Connection to project]
**Palette:** [Colors — NO GREENS]
**Poses:** Small (favicon): [pose] | Large (banner): [pose]

### 2. [Name] — [Animal/Character]
...

---

**Which direction appeals to you?** Pick a number (or mix elements from multiple).
```

---

## Phase 2: User Selection

**This is a hard stop.** Wait for the user to:
1. Pick a concept number
2. Request modifications or mix elements
3. Provide additional direction

**Do not proceed until the user explicitly chooses a direction.**

---

## Phase 3: Refinement

**Goal:** Generate 5 visual variations of the chosen concept.

For each variation, use the `generate_image.py` script with the green screen technique:

```bash
python scripts/generate_image.py \
  --api-key "$GEMINI_API_KEY" \
  --prompt "[Detailed mascot prompt with green screen instructions]" \
  --output ./iterations/variation_01.png \
  --size 512x512 \
  --green-screen \
  --model pro
```

**Prompt template for mascot generation:**
```
Create a [STYLE] illustration of [CHARACTER DESCRIPTION].
The character should be [POSE DESCRIPTION].
Color palette: [SPECIFIC COLORS — NO GREENS].
Style: [ART STYLE — e.g., flat vector, soft watercolor, pixel art].

CRITICAL: The background MUST be solid pure chromakey green (#00FF00).
The ENTIRE background must be uniform #00FF00 green with NO gradients,
NO shadows on the background, NO ground plane. Only the character itself
should have non-green colors. The character must NOT contain any green
or teal colors (no greens, no teals, no lime, no emerald, no mint).
```

### Present Variations

Show all 5 variations to the user. Ask them to:
1. Pick a favorite
2. Request tweaks (pose, expression, color adjustments)
3. Generate more variations if needed

**Do not proceed until user approves a final mascot.**

---

## Phase 4: Final Assets

**Goal:** Generate production-ready assets at exact dimensions with transparent backgrounds.

### Asset Specifications

| Asset | Dimensions | Aspect Ratio | Format | Max Size |
|-------|-----------|--------------|--------|----------|
| Mascot | 256×256 | 1:1 | PNG (transparent) | — |
| Banner | 1200×400 | 3:1 | PNG (transparent) | — |
| Social Preview (OG) | 1280×640 | 2:1 | PNG (transparent) | 1 MB |

See `references/format_guide.md` for full specifications.

### Generation Workflow

For each asset:

1. **Generate** with green screen background:
```bash
python scripts/generate_image.py \
  --api-key "$GEMINI_API_KEY" \
  --prompt "[Asset-specific prompt]" \
  --output ./assets/mascot_raw.png \
  --size 512x512 \
  --green-screen \
  --model pro
```

2. The script automatically:
   - Removes green screen → transparent PNG
   - Resizes to target dimensions with LANCZOS resampling
   - Generates SVG wrapper with embedded PNG

### Banner Prompt Template

```
Create a wide banner image (3:1 aspect ratio) featuring [MASCOT NAME],
the [PROJECT NAME] mascot. [MASCOT DESCRIPTION] is positioned on the
[left/right] side. Next to the character, display the text "[PROJECT NAME]"
in [FONT STYLE]. Below: "[TAGLINE]" in smaller text.

Color palette: [SPECIFIC COLORS — NO GREENS].

CRITICAL: The background MUST be solid pure chromakey green (#00FF00).
The ENTIRE background must be uniform green. No shadows, no ground plane,
no gradients. The character and text must NOT contain any green or teal colors.
```

### Verify Assets

After generation, verify:
- [ ] Real alpha channel (not fake checkerboard)
- [ ] Dimensions match specs exactly
- [ ] File sizes are reasonable (mascot ~50-80 KB, banner ~300-500 KB)
- [ ] SVGs render correctly in browser
- [ ] No green fringing at character edges

---

## Phase 5: README Integration

Embed the banner at the top of the project's README.md:

```markdown
<p align="center">
  <img src="images/banner.png" alt="[Project Name]" width="600">
</p>
```

Also suggest adding the mascot as a favicon or profile image where applicable.

---

## Green Screen Technique

Gemini cannot generate images with native transparency. The workaround:

1. **Generate** with solid chromakey green (#00FF00) background
2. **Detect** green pixels using HSV color space thresholds
3. **Remove** detected pixels → set alpha to 0
4. **Clean edges** with morphological operations to remove green fringing

### Why This Works

- Chromakey green is rarely found in natural subjects
- HSV detection is precise and fast
- Edge cleanup handles anti-aliasing artifacts
- Result: clean transparent PNGs with proper alpha channels

### HSV Detection Parameters

The script uses 0-180 hue scale (OpenCV convention) where pure green = 60:
- **Hue center:** 60 (pure green in 0-180 scale)
- **Hue range:** ±25 (35-85) — catches yellow-green through teal
- **Min saturation:** 75 (ignores desaturated colors)
- **Min value:** 70 (ignores very dark colors)

---

## Color Palette Warning

**All mascot color palettes must avoid the green-teal spectrum.**

Specifically, avoid any color whose HSV hue falls in the green range (35-85 on 0-180 scale, or 70°-170° on 0-360° scale):
- No greens, lime, emerald, forest green
- No teals, cyan, turquoise, mint
- No seafoam, sage, olive (borderline)

**Safe palettes:** Warm tones (reds, oranges, yellows), cool tones (blues, purples, magentas), neutrals (grays, browns, blacks, whites).

If the project's branding includes green, the mascot character itself must use alternative colors. Green branding can appear in text overlays added after green screen removal.

---

## Script Usage

### Single Image Generation

```bash
python scripts/generate_image.py \
  --api-key "$GEMINI_API_KEY" \
  --prompt "A friendly owl mascot, purple and gold palette, flat vector style" \
  --output mascot.png \
  --size 256x256 \
  --green-screen \
  --model pro
```

### With Reference Images

```bash
python scripts/generate_image.py \
  --api-key "$GEMINI_API_KEY" \
  --prompt "Same owl character but in a banner composition" \
  --output banner.png \
  --size 1200x400 \
  --green-screen \
  --model pro \
  --references mascot.png
```

### Generate SVG Wrapper

```bash
python scripts/generate_image.py \
  --api-key "$GEMINI_API_KEY" \
  --prompt "..." \
  --output mascot.png \
  --size 256x256 \
  --green-screen \
  --svg
```

This creates both `mascot.png` and `mascot.svg` (PNG embedded as base64 in SVG).

### Without Green Screen (for testing)

```bash
python scripts/generate_image.py \
  --api-key "$GEMINI_API_KEY" \
  --prompt "A test image" \
  --output test.png
```

---

## Subagents

| Name | File | Purpose |
|------|------|---------|
| `repo-analyst` | `agents/repo_analyst.md` | Reads repo files, outputs Project Identity Brief |
| `creative-director` | `agents/creative_director.md` | Brainstorms 5 diverse mascot concepts |

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| **Fake transparency** (checkerboard pattern baked in) | Gemini drew a checkered background instead of solid green | Add stronger green screen instructions to prompt; emphasize "solid pure #00FF00" |
| **Green fringing** at edges | Anti-aliasing mixed green into edge pixels | Increase `hue_range` parameter or run edge cleanup twice |
| **Character has green parts** | Palette included green/teal tones | Redesign palette to exclude HSV hue 80-160° |
| **Aspect ratio wrong** | Gemini ignores aspect ratio instructions | Generate at square, then resize/crop to target dimensions |
| **Model 404 error** | Wrong model name | Use `gemini-2.5-flash-image` (flash) or `gemini-3-pro-image-preview` (pro) |
| **Text not rendering** | Gemini struggles with text | Use `pro` model; reduce text length; add text as overlay after generation |
| **Style drift across assets** | Each generation is independent | Use `--references` flag to pass the approved mascot as reference |
| **SVG not rendering** | SVG wrapper malformed | Verify base64 encoding; check dimensions match |
| **File too large** | High resolution + complex scene | Resize to target dimensions; use PNG optimization |

### Model Selection

- **`pro`** (`gemini-3-pro-image-preview`) — Better quality, better text rendering. Use for final assets.
- **`flash`** (`gemini-2.5-flash-image`) — Faster, cheaper. Use for drafts and iterations.

---

## File Structure

```
project/
├── iterations/              # Phase 3 variations
│   ├── variation_01.png
│   ├── variation_02.png
│   └── ...
├── assets/                  # Phase 4 final assets
│   ├── mascot.png           # 256×256 transparent
│   ├── mascot.svg           # SVG wrapper
│   ├── banner.png           # 1200×400 transparent
│   ├── banner.svg           # SVG wrapper
│   ├── social_preview.png   # 1280×640
│   └── social_preview.svg   # SVG wrapper
└── scripts/
    └── generate_image.py    # Image generation + green screen removal
```
