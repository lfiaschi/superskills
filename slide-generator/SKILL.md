---
name: slide-generator
description: This skill generates professional presentation slides from any content using Google's Gemini image generation API. Use this skill when users ask to create slides, presentations, slide decks, or visual summaries of content. It analyzes source material, designs cohesive narratives with full slide content, and generates visually coherent slide images.
---

# Slide Generator

Generate professional slides from any content using a two-pass approach: story first, then visual design.

## Before You Start

```bash
# Verify API key is set
[ -n "$GEMINI_API_KEY" ] && echo "Ready" || echo "Set GEMINI_API_KEY first"
```

If not set, tell the user to run `export GEMINI_API_KEY='...'` and stop.

---

## Architecture

This skill uses two specialized agents in sequence, with context discovery upfront:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                          │
│   INPUT            CLARIFY           PASS 1             PASS 2             OUTPUT        │
│   ─────            ───────           ──────             ──────             ──────        │
│                                                                                          │
│   Source      ┌───────────┐    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│   Material    │  Context  │    │ Story Agent  │   │ Design Agent │   │   Gemini     │   │
│   ─────────►  │  Questions│ ─► │              │ ─►│              │ ─►│   Image      │   │
│               │  (≤5)     │    │ Storyboard & │   │ Visual       │   │   Generation │   │
│               └───────────┘    │ Content      │   │ Design       │   │              │   │
│                    │           └──────────────┘   └──────────────┘   └──────────────┘   │
│                    ▼                  │                  │                  │           │
│               [User Input]       story.md         design_system.md      slides/         │
│                                                   visual_specs.md       ├─ slide_01.png │
│                                       │           prompts.json          └─ slides.pdf  │
│                                       ▼                  │                              │
│                                [User Review]      [User Review]                         │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

**Why this flow?**
- **Context first** — Understanding goals shapes everything else
- **Separation of concerns** — Each agent does one thing well
- **Better iteration** — Change the story without redoing visuals, or restyle without rewriting

---

## The Process

```
0. CLARIFY  →  1. STORY AGENT  →  2. REVIEW  →  3. DESIGN AGENT  →  4. REVIEW  →  5. GENERATE  →  6. REVIEW
   ───────      ───────────        ──────        ────────────        ──────        ────────        ──────
   Context      Storyboard &       User          Visual system       User          Create          Fix
   questions    content            approves      & specifications    approves      images          issues
   (≤5)                            story                             design
```

---

## 0. Context Discovery

**Goal:** Understand the presentation context before creating content.

After receiving source material, do a **quick scan** to understand what's there, then ask the user **up to 5 clarifying questions** about context.

### What to Scan For

Quickly identify:
- What type of content is this? (data, research, proposal, report, etc.)
- What's the apparent subject matter?
- How much detail/data is available?

### Questions to Ask

Ask **only what you need** — skip questions where the answer is obvious from context. Maximum 5 questions total.

**Question bank (choose relevant ones):**

| Category | Question | Why It Matters |
|----------|----------|----------------|
| **Event/Setting** | "Where will this be presented? (conference talk, board meeting, team sync, async document, etc.)" | Formality, depth, tone |
| **Goal** | "What's the primary goal? (inform/educate, persuade/sell, enable a decision, document for reference)" | Shapes the entire structure |
| **Presentation Mode** | "Will this be presented live or read independently?" | Live = bold points, speaker fills gaps. Read = detailed, self-contained |
| **Density** | "Should slides be dense with details or minimal with key points?" | Affects how much content per slide |
| **Audience** | "Who's the audience and what do they already know about this topic?" | Technical depth, context needed |
| **Constraints** | "Any constraints? (number of slides, time limit, must-include elements)" | Hard requirements |
| **Tone** | "What tone fits best? (formal, conversational, urgent, neutral)" | Voice throughout |

### Question Format

```markdown
Before I create the storyboard, I have a few questions:

1. **[Question]**
   *If you skip this, I'll assume: [default]*

2. **[Question]**
   *If you skip this, I'll assume: [default]*

[up to 5 questions]

Feel free to answer briefly or skip any — I'll use sensible defaults.
```

### Defaults (When User Doesn't Answer)

| Question | Default Assumption |
|----------|-------------------|
| Event/Setting | Professional meeting |
| Goal | Inform/educate |
| Presentation Mode | Presented live |
| Density | Balanced (not too dense, not too sparse) |
| Audience | Knowledgeable but needs context |
| Constraints | ~10-15 slides |
| Tone | Professional, neutral |

**Wait for user response before proceeding to Story Agent.**

---

## 1. Story Agent: Storyboard & Content

**Goal:** Transform source material into a well-structured storyboard, tailored to the context from Step 0.

**Launch the agent:**

Use the Task tool to spawn the `story-agent` subagent:
- **subagent_type:** Reference the `story-agent` defined in `agents/story_agent.md`
- **prompt:** Include:
  1. The user's source material
  2. The context answers from Step 0 (event, goal, mode, density, audience, constraints, tone)
  3. Instruction to save output to `story.md`

**What the Story Agent does:**
1. **Evidence extraction** — Inventories all data, facts, and claims from the source
2. **Structure selection** — Chooses approach based on the GOAL (inform → explanatory, persuade → argumentative, decide → comparative, document → comprehensive)
3. **Slide content** — Writes each slide with appropriate density for the MODE
4. **Quality checks** — Ensures content matches the stated goal and audience

**How context shapes the output:**

| Context | Impact on Storyboard |
|---------|---------------------|
| **Goal: Inform** | Neutral presentation of facts, no "call to action," balanced perspective |
| **Goal: Persuade** | Clear thesis, supporting evidence, addresses objections, ends with ask |
| **Goal: Decide** | Options laid out fairly, pros/cons, recommendation with reasoning |
| **Goal: Document** | Comprehensive, self-contained, detailed for future reference |
| **Mode: Presented** | Bold headlines, 3-4 points max per slide, speaker notes carry detail |
| **Mode: Read** | More text per slide, self-explanatory, annotations and context included |
| **Density: High** | Data-rich, tables, detailed breakdowns |
| **Density: Low** | Key messages only, one idea per slide |

**Story Agent output:** `story.md`
```markdown
# [Presentation Title]

## Context
- Event: [from user]
- Goal: [from user]
- Mode: [presented/read]
- Density: [high/balanced/low]
- Audience: [from user]
- Constraints: [from user]
- Tone: [from user]

## Executive Summary
[What this deck covers and why]

## Evidence Inventory
[Data and facts extracted from source]

## Structure
[Chosen approach and why it fits the goal]

## Slides
[All slides with: title, content, data points, speaker notes (if presented mode)]
```

**Key constraint:** The Story Agent writes NO visual instructions. It may note inherently visual content ("this is a comparison of 4 options") but doesn't prescribe how to show it.

---

## 2. Story Review: User Gate

**This is a hard stop.** Present the story to the user before proceeding.

```markdown
## Story Ready for Review

I've developed a [N]-slide narrative with the following arc:

**Thesis:** [Core message in one sentence]
**Arc:** [Structure description]
**The Turn:** Slide [N] — [What shifts]
**The Peak:** Slide [N] — [Highest impact moment]

### Slide Sequence
1. [Slide 1 title] — [Purpose]
2. [Slide 2 title] — [Purpose]
...

[FULL STORY.MD CONTENT]

---

**Please review and let me know:**
1. Approve → I'll proceed to visual design
2. Content changes → Tell me what to adjust
3. Restructure → Tell me what's not working with the narrative
```

**Do not proceed to Design Agent until user explicitly approves the story.**

---

## 3. Design Agent: Visual System & Specifications

**Goal:** Transform approved content into detailed visual specifications.

**Launch the agent:**

Use the Task tool to spawn the `design-agent` subagent:
- **subagent_type:** Reference the `design-agent` defined in `agents/design_agent.md`
- **prompt:** Include:
  1. The approved `story.md` content
  2. Instruction to save outputs to:
     - `design_system.md` (visual language)
     - `visual_specs.md` (per-slide specifications)
     - `prompts.json` (ready for generation)

**What the Design Agent does:**
1. **Design system** — Defines colors (with semantic meaning), typography personality, spacing, visual elements, signature details
2. **Per-slide design** — Information hierarchy, visual concept/metaphor, composition, detailed specification
3. **Visual rhythm** — Plans variety (Heavy/Medium/Light/Dramatic), ensures pacing
4. **Prompt construction** — Creates generation-ready prompts with design system embedded

**Design Agent outputs:**

### `design_system.md`
```markdown
## Design System

### Mood & Personality
[Visual feeling description]

### Color Palette
- Primary Background: [hex + usage]
- Accent 1: [hex + semantic meaning]
- ...

### Typography
[Personality descriptions, not font names]

### Visual Elements
[Shapes, lines, icons, illustration style]

### Signature Elements
[1-2 distinctive details]
```

### `visual_specs.md`
```markdown
## Slide [N]: [Title]

### Information Hierarchy
1. [Primary]
2. [Secondary]
3. [Tertiary]

### Visual Concept
[Why this approach serves the content]

### Visual Specification
[Detailed description: composition, elements, colors, spacing, micro-details]

### Visual Weight
[Heavy/Medium/Light/Dramatic]
```

### `prompts.json`
```json
[
  {
    "name": "slide_01_title",
    "prompt": "Create a [MOOD] presentation slide, 16:9 aspect ratio, 4K resolution.\n\nDESIGN LANGUAGE:\n[Design system summary with hex codes]\n\nCONTENT:\nTitle: \"[Exact title]\"\n[Other content]\n\nVISUAL COMPOSITION:\n[Detailed specification]\n\nKEY DETAILS:\n[Critical elements]"
  }
]
```

**Key principle:** Each prompt carries the design system DNA (colors, typography, mood) so visual consistency is maintained even without reference images — but reference images provide additional reinforcement.

---

## 4. Design Review: User Gate

**This is a hard stop.** Present the visual approach to the user before generating.

```markdown
## Visual Design Ready for Review

I've designed a visual system for [N] slides:

**Mood:** [Description]
**Color Palette:** [Key colors and their meanings]
**Visual Rhythm:** [How the deck flows]

### Design System Summary
[Key elements from design_system.md]

### Slide Designs

**Slide 1: [Title]**
- Visual weight: [Heavy/Medium/Light/Dramatic]
- Concept: [Brief description of approach]

**Slide 2: [Title]**
- Visual weight: [...]
- Concept: [...]

[Continue for all slides]

### Full Specifications
[VISUAL_SPECS.MD CONTENT]

---

**Please review and let me know:**
1. Approve → I'll generate the slide images
2. Specific changes → Tell me which slides to redesign
3. System changes → Tell me what to adjust in the overall visual approach
```

**Do not proceed to Generate until user explicitly approves the design.**

---

## 5. Generate: Create Slide Images

### Prerequisites

Ensure you have:
- `prompts.json` from the Design Agent
- `GEMINI_API_KEY` environment variable set

### Generate Slides

```bash
python scripts/generate_slides.py \
  --api-key "$GEMINI_API_KEY" \
  --prompts-file prompts.json \
  --output-dir ./slides \
  --model pro \
  --reference-strategy anchor
```

**Model selection:**
- `pro` — Better text rendering, use for text-heavy slides (recommended default)
- `flash` — Faster iteration, use for drafts or image-heavy slides

**Reference strategy:**
- `anchor` — Slide 1 always included + previous slide (RECOMMENDED)
- `progressive` — Each slide references only previous (causes drift — avoid)
- `none` — No references (each slide independent)

The `anchor` strategy ensures visual consistency:
- Slide 1: No reference (establishes the visual identity from the prompt)
- Slide 2: References slide 1
- Slide 3+: References slide 1 (style anchor) + previous slide (layout continuity)

### Assemble PDF (Optional)

```bash
python scripts/generate_slides.py \
  --output-dir ./slides \
  --assemble
```

---

## 6. Review: Quality Check & Iteration

### Visual Quality Checks

| Check | What to Look For | Fix |
|-------|------------------|-----|
| **Text rendering** | Is all text legible and correct? | Regenerate with `pro` model; simplify text in prompt |
| **Color consistency** | Does the palette match across slides? | Check reference strategy; verify hex codes in prompts |
| **Layout accuracy** | Does composition match specification? | Add more explicit positioning in prompt |
| **Visual weight** | Does rhythm feel right? | Adjust specifications for variety |
| **Style drift** | Do later slides match earlier ones? | Ensure slide 1 is always in reference chain |

### The Flip Test

View all slides as thumbnails:
- Can you follow the argument from titles alone?
- Is there visual variety within consistency?
- Does the eye know where to go on each slide?

### The Presentation Test

Click through as if presenting:
- Does each transition feel earned?
- Would you need to say "so anyway..." anywhere?
- Do data visualizations communicate clearly?

### Iteration

If slides need changes:

1. **Content issues** → Go back to Story Agent, update story.md
2. **Visual concept issues** → Go back to Design Agent, update specifications
3. **Rendering issues** → Refine prompts and regenerate specific slides

To regenerate a single slide:
```bash
python scripts/generate_slides.py \
  --api-key "$GEMINI_API_KEY" \
  --prompt "[Updated prompt for single slide]" \
  --output ./slides/slide_03.png \
  --model pro
```

---

## File Structure

```
project/
├── input/                    # User's source material
│   └── brief.md              # Or transcript.txt, notes.docx, etc.
├── story.md                  # Pass 1 output: narrative & content
├── design_system.md          # Pass 2 output: visual language
├── visual_specs.md           # Pass 2 output: per-slide specifications
├── prompts.json              # Pass 2 output: generation-ready prompts
├── slides/                   # Generated images
│   ├── slide_01_title.png
│   ├── slide_02_problem.png
│   ├── ...
│   └── slides.pdf            # Assembled deck
└── scripts/
    └── generate_slides.py    # Image generation script
```

---

## Quick Reference

### Subagents
| Name | File | Purpose |
|------|------|---------|
| `story-agent` | `agents/story_agent.md` | Analyzes source material, creates storyboard with slide content |
| `design-agent` | `agents/design_agent.md` | Creates design system and visual specifications for each slide |

### API
```
Endpoint: POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent

Models:
- gemini-2.5-flash-image (fast, drafts)
- gemini-3-pro-image-preview (quality, text-heavy)

Config:
generation_config = {"responseModalities": ["IMAGE"]}
```

### Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Text not rendering | Model limitation | Use `pro` model; reduce text density |
| Style drift | Reference chain broken | Use `anchor` strategy; always include slide 1 |
| Colors inconsistent | Hex codes vary | Verify exact hex codes in all prompts |
| Layout wrong | Vague specification | Add explicit proportions and positions |
| Visuals too similar | No rhythm planning | Vary visual weight across slides |
| Prompts too long | Over-specification | Focus on key elements; trust the model |

### Design System Checklist

Before generating, verify design_system.md includes:
- [ ] Color palette with hex codes AND semantic meanings
- [ ] Typography personality (not font names)
- [ ] Spacing philosophy
- [ ] Visual element style (shapes, lines, icons)
- [ ] Signature elements for recognition

### Prompt Quality Checklist

Before generating, verify each prompt in prompts.json includes:
- [ ] Mood and aspect ratio
- [ ] Design language summary (colors, typography, style)
- [ ] Exact text content (verbatim from story.md)
- [ ] Composition with proportions
- [ ] Key details for critical elements
