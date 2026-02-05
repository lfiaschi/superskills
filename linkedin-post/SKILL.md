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
INPUT → Extract Core Insight → Analyze Author Voice → Identify Intent & Audience → Choose Framework → Apply Structure → OUTPUT
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

### Step 3: Analyze the Author's Voice (Critical Step)

Before generating anything, analyze the input to identify:

1. **Sentence rhythm** — Does the author write short punchy sentences? Long flowing ones? Mixed?
2. **Vocabulary level** — Technical jargon or accessible language? Formal or conversational?
3. **Distinctive phrases** — Any unique expressions, metaphors, or turns of phrase to preserve?
4. **Tone markers** — Confident? Reflective? Provocative? Self-deprecating?

This analysis informs how you write, not what you write. The framework handles the "what."

### Step 4: Identify Intent and Audience

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

### Step 5: Choose a Framework

Select the framework that best matches:
- Audience sophistication
- Emotional posture (defensive, curious, overloaded)
- Desired reaction

See [references/frameworks.md](references/frameworks.md) for the complete list of 12 frameworks with their mechanical structures and use cases.

### Step 6: Apply the Framework

**CRITICAL: Structure, not phrasing.** The frameworks define the *sequence of moves* your argument should make. They do not define vocabulary, sentence patterns, or phrasing. Every word you write should come from the author's voice profile (Step 3) or your own original composition — never from framework templates or any examples you've seen.

Apply the framework by:

1. **Follow the logical sequence** — each framework has 3-4 moves (e.g., "state belief → contradict → reveal truth"). Hit each move in order.
2. **Generate original language** — write as if you've never seen an example of this framework. Use vocabulary natural to the author and topic.
3. **Preserve the author's phrasing** — if they wrote something well, keep it exactly
4. **Write in prose by default** — full sentences, real paragraphs, not choppy fragments
5. **Tighten, don't chop** — remove fluff without fragmenting the prose

### Step 7: Return Output

Return:
1. **Chosen framework** and why it fits the intent/audience
2. **The rewritten post** using that framework

If the user requests multiple versions, provide **up to 3 versions** using different frameworks, explaining why each was chosen.

## The 12 Frameworks

Quick reference (see [references/frameworks.md](references/frameworks.md) for full details):

| Framework | Best For | Core Move |
|-----------|----------|-----------|
| Hacker Trap | Expert audience, contrarian insight | Expose a mistake that competence causes |
| Wrong-But-True | Contradicting mainstream beliefs | State belief → declare it wrong → reveal truth |
| Expert Fallacy | Senior audience, seniority blind spots | Tie the mistake to experience level |
| Reversal | Metrics/KPIs, second-order effects | Show optimization creating opposite result |
| Open Loop | Narrative buildup, satisfying reveal | Withhold explanation to pull reader forward |
| Withheld Mechanism | Counterintuitive cause-effect | State outcome, delay revealing the cause |
| Pattern Interrupt | Saturated audience, bold statements | Short disruptive declaration |
| Silent Failure | Subtle errors, false confidence | Frame risk around invisible failures |
| Insight Compression | Mental models, quotable content | Compress complex idea into sharp reframe |
| Narrative Trigger | Trust-building, humanizing | Start at moment of realization |
| Constraint-Based | Execution-focused, practical limits | Frame insight through tradeoffs/limits |
| Meta/Category Error | Noisy discourse, reframing debates | Challenge how topic is framed |

## Output Guidelines

### Originality Rule (Critical)

**Never anchor to examples.** This skill contains structural skeletons and framework templates — these exist to show the *sequence of argumentative moves*, not to provide copyable language.

When generating a post:
- Invent fresh vocabulary appropriate to the author's topic and voice
- If you catch yourself using a phrase from a skeleton or template, replace it
- The test: someone reading your output should not be able to guess which framework you used from the phrasing alone — only from the argument structure

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

## Structural Skeletons (Not Examples)

These skeletons show the **sequence of moves** for each framework. The bracketed placeholders indicate what type of content goes there — never copy specific wording.

### Reversal Skeleton
```
[STATE THE OPTIMIZATION: what you/they deliberately improved]
[INTUITIVE APPEAL: 1-2 sentences on why it seemed right]

[TIME/EVENT MARKER], [INVERTED OUTCOME: the opposite of what was expected]

[DIAGNOSIS: what actually went wrong, the mechanism]

[RESOLUTION or REFRAME: what you learned, what to do instead]

[OPTIONAL: genuine question to the reader]
```

### Hacker Trap Skeleton
```
[PATTERN BREAK: short statement that disrupts a comfortable belief]

[ACKNOWLEDGE THE LOGIC: why smart people do this — validate, don't mock]

[HINT AT COUNTER-TRUTH: signal there's more without fully explaining]

[BODY: develop the insight with specifics from your experience]

[TAKEAWAY: the non-obvious lesson]
```

### Wrong-But-True Skeleton
```
[STATE THE COMMON BELIEF: what most people accept]
[CONTRADICTION: declare it wrong — be direct]

[THE REAL ISSUE: what's actually true]

[EVIDENCE/REASONING: why you believe this]

[IMPLICATION: what changes if you accept this view]
```

### Insight Compression Skeleton
```
[COMPRESSED INSIGHT: "Most X problems are actually Y problems" form — your original phrasing]

[UNPACK: what this means in practice]

[EXAMPLE or EVIDENCE: make it concrete]

[SO WHAT: the actionable implication]
```

Use the framework reference file for all 12 frameworks. These skeletons demonstrate structure only — generate all actual language fresh.

## Multiple Versions

When asked for alternatives, present each version with:
1. Framework name
2. One sentence on why this framing works
3. The rewritten post

Format:
```
## Version 1: [Framework Name]
[Why this framing fits the insight and audience]

[Full post — original language, following the framework's structural moves]

---

## Version 2: [Framework Name]
...
```
