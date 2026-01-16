---
name: slide-generator
description: This skill generates professional presentation slides from any content using Google's Gemini image generation API. Use this skill when users ask to create slides, presentations, slide decks, or visual summaries of content. It analyzes source material, designs cohesive narratives with full slide content, and generates visually coherent slide images.
---

# Slide Generator

Generate professional slides from any content using Gemini's image generation API.

## Before You Start

```bash
# Verify API key is set
[ -n "$GEMINI_API_KEY" ] && echo "Ready" || echo "Set GEMINI_API_KEY first"
```

If not set, tell the user to run `export GEMINI_API_KEY='...'` and stop.

---

## The Process

```
┌───────────────────────────────────────────────────────────────────────────────┐
│  1. ANALYZE  →  2. CLARIFY  →  3. DESIGN  →  4. APPROVE  →  5. GENERATE  →  6. REVIEW  │
│                                                                               │
│  Deep dive     ≤5 questions   Full content   User gate     Create images   Fix issues │
│  into content  (if needed)    + narrative    before API    via Gemini      with user  │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Analyze: Deep Content Review

When the user provides source material (document, transcript, notes, brief, or verbal description), perform a thorough analysis before anything else.

### What to Extract

| Element | What You're Looking For |
|---------|------------------------|
| **Core message** | The single sentence that captures everything. If the material doesn't have one, identify what it *should* be. |
| **Audience signals** | Who is this for? Technical depth, decision-making authority, familiarity with domain. |
| **Tensions & opportunities** | Problems, risks, counterintuitive truths, opportunity costs — the raw material for narrative. |
| **Evidence inventory** | Data points, examples, case studies, quotes — what's available to support claims. |
| **Gaps & ambiguities** | What's missing or unclear that would affect slide design. |

### Output: Analysis Summary

Produce a structured summary:

```markdown
### Content Analysis

**Core Message (Draft):** [One sentence — the thing everything else supports]

**Audience Assumptions:**
- [Who they appear to be]
- [What they likely need to decide/understand/believe]
- [Their probable familiarity with the domain]

**Key Tensions Identified:**
- [Tension 1: e.g., "Current approach feels safe but is measurably inefficient"]
- [Tension 2: if applicable]

**Available Evidence:**
- [Data point or example 1]
- [Data point or example 2]
- [...]

**Gaps Flagged:**
- [Gap 1: e.g., "No clear success metrics provided"]
- [Gap 2: if applicable]
```

**Do not proceed to Clarify until this analysis is complete.**

---

## 2. Clarify: Batched Questions (If Needed)

Based on your analysis, determine if you need user input to proceed effectively.

### Rules

1. **Ask only if genuinely needed** — If you can make reasonable assumptions, do so
2. **Maximum 5 questions** — Prioritize ruthlessly
3. **One batch only** — No back-and-forth; ask all questions at once
4. **State your defaults** — For each question, indicate what you'll assume if the user doesn't answer

### Question Format

```markdown
### Clarifying Questions

Before I design the slides, I need your input on a few things:

1. **[Specific question]**
   *If you don't specify, I'll assume: [default assumption]*

2. **[Specific question]**
   *If you don't specify, I'll assume: [default assumption]*

[... up to 5 questions maximum]
```

### What's Worth Asking

| Worth asking | Not worth asking |
|--------------|------------------|
| "Is the goal to get budget approval or alignment on strategy?" | "Who is the audience?" (you should infer this) |
| "Should I emphasize the 40% waste finding or the reallocation opportunity?" | "What's the main message?" (you should identify this) |
| "Is there sensitivity around naming the underperforming channels?" | Generic questions you can answer yourself |

### If No Questions Needed

State briefly: "I have enough context to proceed. Moving to slide design." Then continue to Design.

**Wait for user response before proceeding to Design.**

---

## 3. Design: Full Content + Narrative

This is where the presentation takes shape. You will produce **complete slide content** — not just an outline.

### Pick Your Narrative Shape

| If the goal is... | Use this structure |
|-------------------|-------------------|
| **Decision/approval** | Pyramid: Lead with recommendation, then evidence |
| **Persuasion/buy-in** | Narrative: Problem → Failed approaches → This solution → Proof |
| **Education/understanding** | Journey: Setup → Concepts (building) → Synthesis → Application |

Most decks are hybrids. Open with tension (narrative), earn trust with evidence (pyramid), close with action.

### Slide Content Template

For **each slide**, produce this complete markdown:

```markdown
---

### Slide [N]: [TITLE THAT STATES AN INSIGHT]

**Subtitle:** [Optional — briefly clarifies the title's focus]

**Content:**
• [Bullet point 1: Key data or insight — concise, visual-friendly]
• [Bullet point 2: Supporting evidence or next step]
• [Bullet point 3: Another crucial element]
• [3-5 bullets maximum; reserve detail for speaker notes]

**Insight/Callout:** [Optional — a key takeaway or actionable insight to highlight visually]

**Visual Layout:**
[Describe the slide organization: e.g., "Bullets on left (60%), bar chart comparing channels on right (40%)" or "Full-bleed image with title overlay" or "2x2 grid with icons for each quadrant"]

**Speaker Notes:**
[Full narrative for voiceover — this is where detail lives]
- Contextual background and why this matters
- Detailed explanations supporting the bullet points
- Storytelling elements, examples, or analogies
- Transition to next slide: "[Bridge sentence to Slide N+1]"

---
```

### Title Quality Check

The title must be an **insight**, not a **label**.

| ❌ Label (reject) | ✅ Insight (accept) |
|-------------------|---------------------|
| "Market Overview" | "Mobile gaming's $100B market runs on a broken model" |
| "Our Solution" | "Rewarded play aligns user, publisher, and platform incentives" |
| "Key Findings" | "40% of ad spend is wasted on saturated channels" |
| "Recommendations" | "Reallocating $2M to emerging channels doubles expected ROI" |

If you catch yourself writing a label, stop and rewrite.

### Narrative Arc Annotation

After all slides, include a narrative summary:

```markdown
### Narrative Arc

**The Turn:** Slide [N] — [What shifts here: e.g., "Audience realizes current approach is failing"]
**The Peak:** Slide [N] — [Highest impact moment: e.g., "The 40% waste revelation"]
**The Resolution:** Slide [N] — [How it lands: e.g., "Clear path forward with specific reallocation"]

**Arc Shape:** [e.g., "Problem → Evidence → Solution → Proof → Action"]
```

### Self-Check Before Presenting to User

Run this check on your draft:

| Check | Question | If it fails... |
|-------|----------|----------------|
| **Unique job** | If I removed this slide, would the deck still work? | Cut or merge it |
| **Earned transition** | Can I articulate why this follows the previous slide? | Restructure |
| **Title test** | Would a smart colleague say "obviously" or "interesting"? | Rewrite title |
| **Energy death** | Are there 3+ consecutive info-heavy slides? | Add a break (quote, question, visual) |
| **Peak placement** | Is the most impactful moment buried in the middle? | Move it to a peak position |
| **Stakes clarity** | Does at least one slide explain why anyone should care? | Add cost of inaction |
| **Strong close** | Does the deck end with "summary" and "questions?" | End with callback, challenge, or CTA |

### Common Failure Patterns to Avoid

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Laundry list** | 5 slides listing features/benefits | Find the story: problem → solution |
| **Symmetric trap** | Every section has exactly 3 points | Match structure to content weight |
| **Buried insight** | Best point is on slide 4 of 12 | Move it to the peak position |
| **Missing stakes** | No slide explains why anyone should care | Add cost of inaction |
| **Anticlimax** | Last slides are "summary" and "questions?" | End with callback or emotional beat |

---

## 4. Approve: User Gate Before Image Generation

**This is a hard stop.** Present the complete deck to the user and wait for approval.

### What to Present

```markdown
## Slide Deck Ready for Review

I've designed [N] slides with the following narrative arc:

**Arc:** [Brief description: e.g., "Problem → Evidence → Solution → Proof → Action"]
**Peak:** Slide [N] — [What happens there]
**Total speaking time:** ~[X] minutes (at ~2 min/slide)

### Tradeoffs Made
- [Any decisions you made: e.g., "Prioritized the efficiency story over the growth story"]
- [Or: "Combined two data points into one slide to maintain pacing"]

[FULL SLIDE DECK IN MARKDOWN — all slides with content, visuals, speaker notes]

---

**Please review and let me know:**
1. Approve as-is → I'll generate the slide images
2. Specific changes → Tell me which slides to revise
3. Major restructure → Tell me what's not working
```

**Do not proceed to Generate until user explicitly approves.**

---

## 5. Generate: Create the Slide Images

### Style Setup

Define once, reuse for all slides:

```
STYLE: [minimalist | corporate | creative | technical]
ASPECT: 16:9
RESOLUTION: 4K
```

**Default style:** minimalist (dark backgrounds work well for professional decks)

**Important:** Do NOT hardcode colors in prompts. The first slide establishes the visual identity, and subsequent slides should reference it to maintain consistency. Let Gemini infer colors from reference images.

### Converting Approved Content to Image Prompts

For each approved slide, construct an image generation prompt:

```
Create a [STYLE] presentation slide, 16:9 aspect ratio, 4K resolution.

Title: "[EXACT TITLE FROM APPROVED CONTENT]"
Subtitle: "[EXACT SUBTITLE IF PRESENT]"
Content: [EXACT bullets/text from approved content — never improvise]
Layout: [From the Visual Layout field in approved content]
Visual style: [Style descriptors from setup]
```

**Critical:** The image prompt must match the approved content exactly. Do not add, remove, or modify text.

### Reference Strategy for Visual Consistency

**Why this matters:** Without proper referencing, slides will drift in style (different backgrounds, fonts, colors). The key is to always anchor to the first slide.

**Reference strategy (handled automatically by the script):**
- **Slide 1:** No reference (establishes the visual identity)
- **Slide 2:** Reference slide 1
- **Slide 3+:** Reference slide 1 (style anchor) + previous slide (layout continuity)

**Do NOT use `--reference-strategy=progressive`** - it causes style drift because slide 1 gets dropped from the reference chain. The default `anchor` strategy is correct.

### Generate

```bash
python scripts/generate_slides.py \
  --api-key "$GEMINI_API_KEY" \
  --output-dir ./slides \
  --prompts-file prompts.json \
  --model pro
```

Use `pro` model for text-heavy slides (better text rendering).
Use `flash` model for image-heavy or draft slides (faster iteration).

**Note:** The script supports multiple reference images per slide. See script documentation for `--reference-strategy` options.

---

## 6. Review: Fix Before Delivery

### The Flip Test

Scan all generated slides in 10 seconds, titles only:
- Can you grasp the argument from titles alone?
- Is there visual variety or does every slide look the same?

### The Flow Test

Walk through as if presenting:
- Does each transition feel earned?
- Would you need to say "so anyway..." anywhere?

### Image-Specific Checks

| Issue | Fix |
|-------|-----|
| Text didn't render correctly | Regenerate with `pro` model; simplify text |
| Visual doesn't match layout spec | Refine prompt with more explicit positioning |
| Style inconsistent across slides | Reuse exact style string; reference first slide |
| Blurry output | Ensure "4K resolution" is in prompt |

### Revision Triggers

| If you see... | Then... |
|---------------|---------|
| 3+ consecutive info-heavy slides | Add a provocative question, quote, or visual break |
| A title that's a label | Rewrite and regenerate |
| Visual monotony | Vary layouts; add full-bleed image or quote slide |
| Weak ending | Restructure: callback to opening, clear CTA, or emotional beat |

### Iterate with User

Present generated slides. Regenerate as needed based on feedback.

---

## Reference

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

| Issue | Fix |
|-------|-----|
| Text not rendering | Use pro model; simplify text |
| Inconsistent styles | Use proper reference strategy: always include slide 1 as anchor + previous slide. Do NOT use simple progressive (each slide refs only the previous one). |
| Style drift mid-deck | Slide 1 was dropped from references. Ensure slide 1 is always included as style anchor for all slides. |
| Blurry output | Specify 4K in prompt |
| API rate limits | Add delays between requests; batch during off-peak |
| Colors not matching | Do NOT hardcode colors in prompts. Let Gemini infer from reference images. |

### Slide Type Reference

| Content Type | Recommended Format |
|--------------|-------------------|
| Single insight | Bold headline, minimal supporting text |
| Comparison (2-4 items) | Columns or 2x2 grid |
| Metrics/KPIs | Dashboard cards with big numbers |
| Process/workflow | Flow diagram or numbered timeline |
| Trend over time | Line chart |
| Ranking/proportion | Bar chart or pie chart |
| Quote/testimonial | Full-bleed with large text |
| Section break | Bold title, minimal or no body text |

### Speaker Notes Best Practices

Speaker notes should:
- **Open with context:** Why this slide matters right now
- **Expand on bullets:** The story behind each point
- **Include signposts:** "The key thing here is..." or "What this means is..."
- **Bridge to next slide:** Never end abruptly; set up what's coming
- **Time guidance:** Roughly 100-150 words per slide ≈ 1-2 minutes

