---
name: blog-post
description: Write technical blog posts in the style of elite data science consultancies. Transform research, experiments, or source material into polished, business-focused technical content. Use for blog posts, tutorials, case studies, or technical articles that balance rigor with accessibility.
---

# Technical Blog Post Writing

Write technical blog posts that balance rigor with accessibility.

**CRITICAL INSTRUCTION:** This skill teaches *structure and principles*, not content. Follow the structural patterns described, but invent your own wording, metaphors, and examples. Do not copy phrases from this document.

---

## What Makes Technical Posts Great (Principles Only)

1. **Business-First Framing** — Open with why anyone should care, not definitions
2. **Progressive Complexity** — Layer understanding: analogy → framework → details
3. **Question-Driven Structure** — Headers often frame what the section answers
4. **Heavy Visualization** — Diagrams before equations, comparisons over descriptions
5. **Honest Uncertainty** — Acknowledge limitations; hedge appropriately

---

## Post Structure (Follow This Order)

### Section 1: Opening Hook
**Purpose:** Make the reader care in 30 seconds.

**Structural requirements:**
- First sentence: provocative question, pain point, or counterintuitive claim
- Second-third sentences: establish stakes for target audience
- Final sentence: promise what they'll learn

**Rhetorical moves to use (pick one):**
- "What if" aspiration + current pain + transformation promise
- Relatable frustration + numbered obstacles + transition to solution
- Flawed assumption + reality + consequence

### Section 2: Conceptual Framework
**Purpose:** Build mental model before technical details.

**Structural requirements:**
- One-sentence accessible definition
- "Unlike [old approach]... this approach..." contrast
- 3-5 key components as bold terms with plain explanations
- Optional: visual diagram described or referenced

### Section 3: Technical Deep-Dive
**Purpose:** Explain the "how" progressively.

**Structural requirements:**
- Open with accessible analogy
- Reference supporting visual
- Break mechanism into numbered steps or bullet components
- Include math notation only after intuition is established
- Each formula followed by plain-English interpretation

### Section 4: Implications/Benefits
**Purpose:** Connect technical work to decisions.

**Structural requirements:**
- Segment by persona if multiple audiences exist
- Each benefit: bold name + specific capability + concrete example
- Synthesis statement at end

### Section 5: Limitations/Challenges
**Purpose:** Build credibility through honesty.

**Structural requirements:**
- Acknowledge what the method can't do
- List 2-4 challenges practitioners face
- Frame as "things to consider" not "failures"

### Section 6: Conclusion
**Purpose:** Synthesize and point forward.

**Structural requirements:**
- One paragraph restating core insight
- Concrete results if applicable
- Forward-looking statement about applications

---

## Anti-Patterns (What NOT to Do)

These patterns weaken technical posts. Each includes a negative example.

### ❌ Opening with Definitions

**BAD:**
```
Media Mix Modeling (MMM) is a statistical technique used to measure 
the effectiveness of marketing channels. It was first developed in 
the 1960s and has evolved to incorporate Bayesian methods...
```

**Why it fails:** Reader has no reason to care. Definitions belong after motivation.

**Fix:** Start with a problem, question, or pain point first.

---

### ❌ Wall of Math Before Intuition

**BAD:**
```
The model is defined as:

$$y_t = \alpha + \sum_{m=1}^{M}\beta_m \cdot \text{Hill}(x_{m,t}; K_m, S_m) \cdot \text{Adstock}(\theta_m, L) + \gamma Z_t + \epsilon_t$$

where $\text{Hill}(x; K, S) = \frac{1}{1 + (x/K)^{-S}}$ and...
```

**Why it fails:** Reader is lost before understanding what the equation represents.

**Fix:** Build intuition with analogy and plain language, THEN show math, THEN interpret.

---

### ❌ Passive Voice Dominance

**BAD:**
```
The model was trained on the dataset. It was observed that convergence 
was achieved after 2000 iterations. The results were then analyzed 
and it was found that the parameters were recovered successfully.
```

**Why it fails:** Distant, bureaucratic, hard to follow. No human presence.

**Fix:** Use first person plural ("We trained...", "We observed...").

---

### ❌ Hedge Word Soup

**BAD:**
```
It could potentially perhaps be suggested that in some cases there may 
be a tendency toward somewhat improved performance under certain 
conditions, though this would require further investigation.
```

**Why it fails:** Says nothing. No actionable information. Sounds evasive.

**Fix:** Be direct. "This suggests X. However, [specific caveat]."

---

### ❌ No Visuals for Technical Concepts

**BAD:**
```
The saturation function has an asymptotic property where initial 
investments yield high returns but additional investments show 
diminishing returns as the channel approaches saturation. The 
adstock function captures temporal carryover effects where 
marketing impact decays geometrically over time.
```

**Why it fails:** Dense. Reader must build mental picture from scratch.

**Fix:** Reference or describe a figure. "As shown in Figure 2, initial spend..."

---

### ❌ Burying the Key Insight

**BAD:**
```
First, we preprocessed the data (Section 2). Then we explored various 
model architectures (Section 3). We tried several optimization 
strategies (Section 4). Finally, we evaluated on held-out data (Section 5).

[Three pages later...]

The key finding was that time-varying parameters dramatically improve 
forecast accuracy.
```

**Why it fails:** Reader may never reach the insight. No hook.

**Fix:** Lead with the insight. "Time-varying parameters dramatically improve accuracy. Here's how we discovered this..."

---

### ❌ Corporate Buzzword Speak

**BAD:**
```
By leveraging synergistic capabilities across our integrated platform, 
we enable stakeholders to actualize transformative paradigm shifts 
that drive best-in-class outcomes in the data-driven decision space.
```

**Why it fails:** Meaningless. No specifics. Sounds like marketing copy.

**Fix:** Use plain language. What specifically happens? What specific outcome?

---

### ❌ Point Estimates Without Uncertainty

**BAD:**
```
The ROI of Channel A is 3.2x. Channel B is 1.8x. Therefore, shift 
budget from B to A.
```

**Why it fails:** Ignores uncertainty. What if confidence intervals overlap?

**Fix:** "Channel A shows ROI of 3.2x (95% CI: 2.1-4.5). Channel B shows 1.8x (95% CI: 1.5-2.2). The non-overlapping intervals suggest reallocation would likely improve performance."

---

### ❌ No Business Connection

**BAD:**
```
We achieved an RMSE of 0.023 and an R² of 0.94. The Gelman-Rubin 
diagnostic showed all R-hat values below 1.01. ESS exceeded 1000 
for all parameters.
```

**Why it fails:** Reader doesn't know if these numbers are good or what to do.

**Fix:** Connect to decisions. "Model fits well (R² = 0.94), giving us confidence to use it for budget optimization. If we follow its recommendations, projected revenue increase is..."

---

## Voice Guidelines

### Publication Context Matters

**Personal website (lucafiaschi.com):**
- First person singular ("I")
- Luca's individual voice and experience
- "I've seen this pattern at three companies..."
- "Here's what I learned..."
- Personal opinions and reactions

**PyMC Labs blog:**
- First person plural ("we")
- Team voice representing the consultancy
- "We built this for a client..."
- "Our team discovered..."
- Collective expertise

### DO:
- Active voice ("I/We fit the model...")
- Direct statements ("This suggests...")
- Acknowledge uncertainty ("The estimates are uncertain because...")
- Credit prior work

### DON'T:
- Third person passive ("It was observed...")
- Overclaiming ("This proves...")
- False confidence ("Obviously...")
- Buzzwords ("leverage", "synergize", "paradigm")

---

## Code Presentation Principles

**When to show code:**
- Implementation IS the insight
- Choices are non-obvious
- Reader needs to reproduce

**When to describe without code:**
- Standard operations
- Focus is on concepts
- Non-technical audience

**Code block structure:**
- Comment explaining "why" not "what"
- Meaningful variable names
- Section breaks with `# ---` for visual grouping

---

## Generating Posts from Source Material

### From GitHub Repos/Experiments:
1. Identify the "so what" — why should anyone care?
2. Extract the key insight — one thing to remember
3. Find visualizations that tell the story
4. Simplify the entry point — minimum viable explanation
5. Build to technical details progressively

### From Research/Articles:
1. Translate abstract to plain business terms
2. Identify applications — where would someone use this?
3. Find the comparison — what's the "before" that makes "after" impressive?
4. Surface limitations honestly

---

## Final Instruction

**When writing a blog post using this skill:**

1. Follow the section structure (Opening → Framework → Deep-Dive → Implications → Limitations → Conclusion)
2. Apply the principles (business-first, progressive complexity, honest uncertainty)
3. Avoid every anti-pattern listed above
4. Invent your own wording, metaphors, examples, and transitions
5. Do not copy phrases from this document

Write the post on the user's topic. Use the same structural order and level of rigor, but create entirely new content.

---

## Post-Writing: Humanizer Pass (MANDATORY)

After completing the first draft, apply the **humanizer** skill to remove AI writing patterns.

**Key patterns to eliminate in final pass:**

1. **AI vocabulary words:** delve, crucial, pivotal, landscape, tapestry, testament, underscore, showcase, foster, enhance, vibrant, intricate
2. **Copula avoidance:** Replace "serves as", "stands as", "marks" with simple "is"
3. **-ing phrase padding:** Cut "highlighting", "underscoring", "showcasing", "reflecting"
4. **Em dash overuse:** Replace most em dashes with commas or periods
5. **Rule of three:** Break up forced triplets
6. **Significance inflation:** Cut "pivotal moment", "key turning point", "broader trends"
7. **Negative parallelisms:** Cut "It's not just X, it's Y" patterns
8. **Generic conclusions:** Cut "the future looks bright", "exciting times ahead"

**Add soul:**
- Vary sentence rhythm (short punchy + longer flowing)
- Include first-person reactions where appropriate
- Acknowledge mixed feelings and uncertainty
- Be specific about opinions, not neutrally balanced

**Read the humanizer skill for full pattern list:** `skills/humanizer/SKILL.md`

---

## Publishing: Open PR on Personal Website

After humanizing the draft, publish to Luca's website.

**Repo:** `Rise-AI-Consulting/luca-personal-website`
**Format:** Quarto (.qmd)
**Location:** `blog/posts/<post-slug>/index.qmd`

### Required Frontmatter

```yaml
---
title: "Post Title Here"
description: "One-line description for SEO and preview cards"
author: "Luca Fiaschi"
date: "YYYY-MM-DD"
categories: [Category1, Category2]
image: "preview-image.png"
reading-time: true
---
```

### Workflow

```bash
cd /home/molt/workspace/luca-personal-website
git checkout main && git pull origin main
git checkout -b blog/<post-slug>

# Create post directory and files
mkdir -p blog/posts/<post-slug>
# Write index.qmd
# Add images (nano-banana skill or from source)

# Commit and push
git add blog/posts/<post-slug>/
git commit -m "Blog: <Post Title>"
git push -u origin blog/<post-slug>

# Open PR with BLOG label
gh pr create --title "Blog: <Post Title>" --label BLOG --body "New blog post: <description>"
```

### Image Requirements

- **Preview image required** — Shows on blog index cards
- **Generate with nano-banana** — For conceptual/illustrative images
- **From source content** — If transforming existing material with figures
- **Code-generated plots** — Save with `plt.savefig('filename.png', dpi=150, bbox_inches='tight', facecolor='white')`

### Quarto Features Available

- Python code blocks with `{python}` — executed and rendered
- `#| label: chunk-name` — for cross-references
- `#| fig-cap: "Caption"` — figure captions
- LaTeX math: inline `$...$` and block `$$...$$`
- `code-fold: true` — collapsible code blocks

---

## ⚠️ POST-WRITING CHECKLIST (MANDATORY)

Before opening a PR, verify ALL of these:

### 1. HUMANIZE THE TEXT
Run the humanizer skill (`skills/humanizer/SKILL.md`) or manually check:
- [ ] No em dashes — use periods, commas, or parentheses instead
- [ ] No "Here's what..." / "Let's..." / "But here's..." patterns
- [ ] No AI vocab: crucial, pivotal, delve, landscape, tapestry, foster, underscore
- [ ] No copula avoidance: "serves as" → "is", "stands as" → "is"
- [ ] No excessive bold on key phrases
- [ ] Voice matches publication (personal site = "I", PyMC Labs = "we")

### 2. ADD PREVIEW IMAGE
- [ ] Preview image exists as `preview.png` in post folder
- [ ] Style: Simple, clean, meaningful imagery
- [ ] NOT: Complex, crowded, "AI-generated feeling" aesthetic

### 3. VERIFY BEFORE PR
- [ ] Frontmatter complete (title, description, author, date, categories, image)
- [ ] Code blocks execute without errors
- [ ] Plots save correctly with white background

**DO NOT SKIP THESE STEPS.** They are as important as the writing itself.
