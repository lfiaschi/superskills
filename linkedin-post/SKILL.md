---
name: linkedin-post
description: Transforms drafts or raw content into effective LinkedIn posts using proven hook frameworks. Applies framework structure while preserving the author's natural voice.
---

# LinkedIn Post Skill

This skill transforms any draft or raw content into an effective LinkedIn post by applying proven hook frameworks while preserving authentic voice.

## Overview

The goal is **structured thinking, authentic voice**.

Frameworks provide cognitive scaffolding for *argument structure*—how to sequence ideas for impact. But structure is not style. Never sacrifice the author's natural voice for "LinkedIn-optimized" writing.

## Core Principle: Structure ≠ Style

**Structure** = the logical flow of the argument (hook → tension → insight → implication)
**Style** = sentence length, paragraph shape, word choice, tone

Frameworks dictate structure. The author's voice dictates style.

A Reversal framework can be written as choppy fragments OR as flowing prose. Default to prose. Only use fragmented style if the author writes that way naturally or explicitly requests it.

## Workflow

```
INPUT → Extract Core Insight → Identify Intent & Audience → Choose Framework → Apply Structure → OUTPUT
```

### Step 1: Receive Input

Accept the user's input, which can be:
- A rough draft of a LinkedIn post
- Raw content (notes, ideas, bullet points)
- A topic or insight they want to share
- An existing post they want to improve

### Step 2: Extract the Core Insight

Distill the input into one sentence that is:
- **Non-obvious**: Not something everyone already knows
- **Actionable or perspective-shifting**: Gives the reader something to do or think differently about

Ask yourself: "What is the one thing this post should make the reader realize?"

### Step 3: Identify Intent and Audience

**Intent** - What does the author want to achieve?
- Teach
- Provoke
- Warn
- Signal expertise
- Start discussion

**Audience** - Who is this for?
- Junior vs senior
- Technical vs business
- Builder vs leader
- General vs niche

### Step 4: Choose a Framework

Select the framework that best matches:
- Audience sophistication
- Emotional posture (defensive, curious, overloaded)
- Desired reaction

See [references/frameworks.md](references/frameworks.md) for the complete list of 12 frameworks with their mechanical structures and use cases.

### Step 5: Apply the Framework

Apply the **argument structure** of the chosen framework while preserving the author's voice:

1. **Use the framework's logic** — the sequence of moves (e.g., state belief → contradict → reveal truth)
2. **Keep the author's phrasing** — if they wrote something well, don't rewrite it
3. **Write in prose by default** — full sentences, real paragraphs, not choppy fragments
4. **Tighten, don't chop** — remove fluff without fragmenting the prose

### Step 6: Return Output

Return:
1. **Chosen framework** and why it fits the intent/audience
2. **The rewritten post** using that framework

If the user requests multiple versions, provide **up to 3 versions** using different frameworks, explaining why each was chosen.

## The 12 Frameworks

Quick reference (see [references/frameworks.md](references/frameworks.md) for full details):

| Framework | Best For | Template Starter |
|-----------|----------|------------------|
| Hacker Trap | Expert audience, contrarian insight | "Smart teams often do X..." |
| Wrong-But-True | Contradicting mainstream beliefs | "Everyone believes X. It's wrong." |
| Expert Fallacy | Senior audience, seniority blind spots | "This mistake doesn't show up early..." |
| Reversal | Metrics/KPIs, second-order effects | "We optimized for X..." |
| Open Loop | Narrative buildup, satisfying reveal | "We thought the problem was X. It wasn't." |
| Withheld Mechanism | Counterintuitive cause-effect | "This worked. Not for the reason we expected." |
| Pattern Interrupt | Saturated audience, bold statements | "Your dashboard is lying." |
| Silent Failure | Subtle errors, false confidence | "Nothing crashed. Everything was wrong." |
| Insight Compression | Mental models, quotable content | "Most X problems aren't X problems." |
| Narrative Trigger | Trust-building, humanizing | "I knew something was wrong when..." |
| Constraint-Based | Execution-focused, practical limits | "You only get one metric." |
| Meta/Category Error | Noisy discourse, reframing debates | "We keep debating X. That's the wrong question." |

## Output Guidelines

### Voice and Style
- **Default to prose** — full sentences, real paragraphs, natural flow
- **Preserve the author's phrasing** — if they said it well, keep it
- **Tighten, don't rewrite** — remove fluff, don't replace voice
- Only use fragmented/choppy style if the author writes that way or requests it

### Plain English Over Cleverness
- **Use plain English by default.** Say what you mean directly. Don't reach for metaphors when simple words work.
- If a metaphor needs explaining, replace it with plain language
- Abstract phrases that sound smart but mean nothing should be simplified
- The reader should understand every sentence on first read
- **Never try to sound smarter than the reader.** Clever-sounding phrases that obscure meaning are worse than plain statements. "People who think differently" beats "people who maintain their own maps of reality."
- **Test every sentence:** Could you say this more simply? If yes, do it.

### Cliché Blacklist
Never use these overused phrases:
- "The uncomfortable truth"
- "The results are brutal"
- "Here's the thing"
- "Let that sink in"
- "Read that again"
- "This is huge"
- "Game changer"
- "Hot take"
- "Unpopular opinion" (when the opinion is popular)
- "I'll say it louder for the people in the back"

If you find yourself reaching for these, just delete them. The sentence usually works better without the throat-clearing.

### Post Structure
- First line is crucial — it appears in the feed preview
- Aim for 150-300 words
- End with a question only if it's genuine, not performative

### Preserve the Core Insight
All versions must convey the same underlying insight — only the structure changes.

## Example Usage

**Input:**
```
I've noticed that the teams that document everything often ship slower than teams with less documentation. It seems counterintuitive but I think too much process kills momentum.
```

**Analysis:**
- Core insight: Over-documentation slows teams down despite feeling productive
- Intent: Warn/provoke
- Audience: Engineering leaders, senior ICs
- Best framework: Reversal (showing how optimizing for something sensible backfires)

**Output using Reversal Framework:**
```
We optimized for documentation. Every decision captured, every meeting summarized. It felt like the right move.

Six months later, we were shipping half as fast.

The teams spending hours writing docs were the same teams not writing code. Documentation had become a proxy for progress—we confused activity with output.

The fix wasn't less documentation. It was asking a simple question: who actually reads this?

What process have you seen backfire?
```

Note: The output uses the Reversal structure (optimization → intuitive appeal → inverted outcome) but preserves natural prose flow instead of fragmenting every thought into its own line.

## Multiple Versions

When asked for alternatives, present each version with:
1. Framework name
2. One sentence on why this framing works
3. The rewritten post

Example:
```
## Version 1: Reversal Framework
Best for showing how a sensible optimization backfired.

[Post content]

---

## Version 2: Hacker Trap Framework
Best for attracting experienced readers who might make this mistake.

[Post content]

---

## Version 3: Insight Compression Framework
Best for creating a quotable mental model.

[Post content]
```
