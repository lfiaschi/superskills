---
name: conference-proposal-generator
description: Generates tailored conference talk proposals for data science and AI conferences (Databricks Data+AI Summit, ODSC, KDD, NeurIPS, etc.) from a vague initial idea. Brainstorms angles via agents, researches the target conference, and writes a polished submission-ready proposal. Use when a user wants help creating a conference CFP submission.
---

# Conference Proposal Generator

Transform a vague idea into a polished, submission-ready conference talk proposal through multi-agent brainstorming, research, and iterative writing.

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                          │
│   INPUT            CLARIFY           PASS 1             PASS 2             PASS 3        │
│   ─────            ───────           ──────             ──────             ──────        │
│                                                                                          │
│   Vague       ┌───────────┐    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│   Idea        │  Context  │    │  Brainstorm  │   │   Writer     │   │   Critic     │   │
│   ─────────►  │  Questions│ ─► │  Agent       │ ─►│   Agent      │ ─►│   Agent      │   │
│               │  (≤6)     │    │              │   │              │   │              │   │
│               └───────────┘    │ 3-5 angles   │   │ Full draft   │   │ CFP review   │   │
│                    │           └──────────────┘   └──────────────┘   └──────────────┘   │
│                    ▼                  │                  │                  │             │
│               [User Input]      [User Picks]       proposal.md      [Loop if needed]    │
│                                                                            │             │
│                                                                       FINAL OUTPUT      │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

**Why this flow?**
- **Context first** — Conference requirements and speaker background shape everything
- **Brainstorm before writing** — Explore multiple angles before committing to one
- **Critic loop** — Catches CFP anti-patterns (AI-sounding language, vague abstracts, missing takeaways)

---

## The Process

```
0. CLARIFY  →  1. BRAINSTORM  →  2. SELECT  →  3. WRITE  →  4. CRITIQUE  →  5. OUTPUT
   ───────      ──────────        ──────        ─────        ────────        ──────
   Context      3-5 angles        User          Full         Review &        Final
   questions    with hooks        picks one     proposal     revise loop     proposal
   (≤6)                           or blends     draft        (max 3 iter)
```

---

## 0. Context Discovery

**Goal:** Understand the idea, the target conference, and the speaker's background before brainstorming.

After receiving the user's vague idea, ask **up to 6 clarifying questions** to build context.

### Questions to Ask

Ask **only what you need** — skip questions where the answer is obvious from context. Maximum 6 questions total.

**Question bank (choose relevant ones):**

| Category | Question | Why It Matters |
|----------|----------|----------------|
| **Conference** | "Which conference are you targeting? (e.g., Databricks Data+AI Summit, ODSC, KDD, PyCon, internal)" | Shapes format, length, tone, topic alignment |
| **Format** | "What session format? (lightning talk ~10-20min, breakout ~40min, workshop ~90min, tutorial)" | Determines depth and structure |
| **Audience** | "Who's your ideal audience? What should they already know?" | Sets technical depth and prerequisites |
| **Your angle** | "What's your unique perspective? Have you built something, solved a hard problem, gotten surprising results?" | The 'why you' question reviewers ask |
| **Evidence** | "Do you have concrete results, metrics, or a real project to reference?" | Specificity is what separates accepted from rejected |
| **Constraints** | "Any requirements? (word limits, specific fields to fill, deadline)" | Hard constraints for the output format |

### Question Format

```markdown
Before I brainstorm angles, I need some context:

1. **[Question]**
   *If you skip this, I'll assume: [default]*

2. **[Question]**
   *If you skip this, I'll assume: [default]*

[up to 6 questions]

Feel free to answer briefly or skip any — I'll use sensible defaults.
```

### Defaults (When User Doesn't Answer)

| Question | Default Assumption |
|----------|-------------------|
| Conference | Generic data science / AI conference |
| Format | 40-minute breakout session |
| Audience | Data practitioners with some ML/AI experience |
| Your angle | Practitioner sharing learnings |
| Evidence | Will work with what's provided |
| Constraints | Standard CFP: title, abstract (250-300 words), outline, takeaways |

**Wait for user response before proceeding to Brainstorm Agent.**

---

## 1. Brainstorm Agent: Generate Angles

**Goal:** Take the vague idea + context and produce 3-5 distinct proposal angles, each with a working title and hook.

**Launch the agent:**

Use the Task tool to spawn the `brainstorm-agent` subagent:
- **subagent_type:** Reference the `brainstorm-agent` defined in `agents/brainstorm_agent.md`
- **prompt:** Include:
  1. The user's vague idea (verbatim)
  2. All context answers from Step 0
  3. Any conference-specific information you know about the target conference
  4. Instruction to output structured angle options

**What the Brainstorm Agent does:**
1. **Deconstructs the idea** — Identifies the core insight, potential sub-topics, and unique angles
2. **Researches framing** — Considers what's trending, what's been overdone, and what's fresh
3. **Generates 3-5 angles** — Each with a distinct hook, title, and one-paragraph pitch
4. **Ranks them** — By likely acceptance probability, with reasoning

**Brainstorm Agent output:**

```markdown
## Angle 1: [Working Title]
**Hook:** [One sentence that makes a reviewer stop scrolling]
**Pitch:** [One paragraph summary of this angle]
**Why it works:** [Why this angle is strong for the target conference]
**Risk:** [Why it might not land]

## Angle 2: [Working Title]
...

## Recommended: Angle [N]
[Brief reasoning for the top recommendation]
```

---

## 2. Angle Selection: User Gate

**This is a hard stop.** Present the angles to the user before writing.

```markdown
## Brainstormed Angles Ready for Review

I've developed [N] distinct angles for your talk:

### Angle 1: "[Title]"
**Hook:** [hook]
[Brief pitch]

### Angle 2: "[Title]"
**Hook:** [hook]
[Brief pitch]

[Continue for all angles]

---

**Recommendation:** I'd go with Angle [N] because [reason].

**Please let me know:**
1. Pick one → I'll write the full proposal
2. Blend elements → Tell me what to combine
3. Different direction → Tell me what's missing
```

**Do not proceed to Writer Agent until user explicitly selects a direction.**

---

## 3. Writer Agent: Draft Full Proposal

**Goal:** Write a complete, submission-ready conference proposal based on the selected angle.

**Launch the agent:**

Use the Task tool to spawn the `writer-agent` subagent:
- **subagent_type:** Reference the `writer-agent` defined in `agents/writer_agent.md`
- **prompt:** Include:
  1. The selected angle (title, hook, pitch)
  2. Full context from Step 0 (conference, format, audience, speaker background, evidence)
  3. Any conference-specific formatting requirements
  4. Instruction to save output to `proposal.md`

**What the Writer Agent does:**
1. **Title** — Crafts an attention-grabbing, specific title
2. **Abstract** — Writes 250-300 word abstract with problem, approach, results, takeaways
3. **Detailed outline** — Timed slide-by-slide or section-by-section outline
4. **Audience takeaways** — 3 concrete, actionable things attendees will learn
5. **Speaker bio** — Tailored to the topic, emphasizing relevant credibility
6. **Reviewer notes** — Optional private notes for the review committee

**Writer Agent output:** `proposal.md`

```markdown
# [Title]

## Abstract
[250-300 words]

## Detailed Outline
[Timed, section-by-section breakdown]

## Audience Takeaways
1. [Concrete takeaway]
2. [Concrete takeaway]
3. [Concrete takeaway]

## Target Audience & Prerequisites
[Who this is for and what they need to know]

## Speaker Bio
[Relevant bio tailored to this topic]

## Notes for Reviewers
[Optional: why this talk matters now, what makes it unique]
```

---

## 4. Critic Agent: Review & Iterate

**Goal:** Review the draft proposal against CFP best practices and catch common rejection reasons.

**Launch the agent:**

Use the Task tool to spawn the `critic-agent` subagent:
- **subagent_type:** Reference the `critic-agent` defined in `agents/critic_agent.md`
- **prompt:** Include:
  1. The full proposal from Step 3
  2. The target conference name and any specific requirements
  3. Instruction to evaluate against the CFP review criteria

**What the Critic Agent does:**
1. **Title review** — Is it specific enough? Does it grab attention? Is it too clickbaity?
2. **Abstract review** — Does it clearly state problem, approach, and takeaways? Is it the right length?
3. **Outline review** — Is it detailed enough to show the speaker has thought this through?
4. **Takeaway review** — Are they concrete and actionable, not vague platitudes?
5. **Voice check** — Does it sound authentically human? (Critical: ODSC and others reject AI-generated submissions)
6. **Anti-pattern scan** — Checks for sales pitches, vague claims, buzzword overload, missing specificity

**Critic Agent output:**

```
VERDICT: [READY or NEEDS_REVISION]

STRENGTHS:
- [What's working well]

ISSUES:
- [Each issue with specific location and fix direction]

VOICE_CHECK: [PASS or FLAG]
- [Any AI-sounding phrases detected]

CONFIDENCE: [HIGH, MEDIUM, LOW]

FEEDBACK:
[Detailed, actionable revision guidance]
```

### Iteration Loop

If the critic returns `NEEDS_REVISION`:

1. Pass the critic's feedback back to the Writer Agent for revision
2. Re-run the Critic Agent on the revised version
3. Maximum 3 iterations

If the critic returns `READY`, proceed to output.

**IMPORTANT:** Each critic evaluation must be a fresh agent instance to ensure unbiased assessment.

---

## 5. Output: Final Proposal

Present the final proposal to the user:

```markdown
## Your Conference Proposal is Ready

**Conference:** [target]
**Format:** [session type]
**Iterations:** [N] rounds of review

---

[FULL PROPOSAL.MD CONTENT]

---

### Submission Checklist

- [ ] Title is under [N] characters (check conference limit)
- [ ] Abstract is [N] words (check conference requirement)
- [ ] Outline covers the full session time
- [ ] 3 concrete audience takeaways included
- [ ] Speaker bio emphasizes relevant experience
- [ ] No product pitches or sales language
- [ ] Written in authentic voice (not AI-generated sounding)
- [ ] Proofread for typos and clarity

### Tips for Submission

- **Submit early** — Many conferences review on a rolling basis
- **Submit multiple proposals** — Increases your odds; committees may pick the one that fills a gap
- **Customize per conference** — Don't copy-paste the same abstract everywhere
- **Get a peer review** — Have a colleague read it before submitting
```

---

## Conference-Specific Knowledge

The agents are informed about common data science / AI conference requirements:

### Databricks Data+AI Summit
- **Formats:** 20-min lightning talk, 40-min breakout session
- **Focus:** Practical, real-world solutions using data + AI
- **Values:** Specific metrics, architecture details, before/after outcomes
- **Hot topics:** Agentic AI, LLM applications, Unity Catalog, data governance, real-time streaming, data democratization
- **Technologies to reference:** Apache Spark, Delta Lake, MLflow, Mosaic AI, Lakeflow, Agent Bricks, Databricks SQL, Unity Catalog
- **Review:** Complete and thorough submissions receive priority; practical practitioner stories highly valued
- **Avoid:** Generic overviews, theory without practice, talks without concrete outcomes
- **Tip:** "Are you solving real-world problems with data and AI?" is their guiding question

### ODSC (Open Data Science Conference)
- **Abstract minimum:** 250 words (strictly enforced)
- **Critical: AI-generated submissions are disqualified** — flagged submissions are removed from consideration
- **No product/sales pitches** — you must confirm your proposal is not a sales pitch upon submission
- **Workshop proposals** require teaching credentials (university, bootcamp, or core contributor experience)
- **Two rounds:** Submit in Round 1 for best acceptance odds; Round 2 fills gaps
- **Abstract must match presentation** — committee reserves the right to reject if talk doesn't match abstract
- **Materials deadline:** Draft slides due ~6 weeks before conference, final slides ~4 weeks before
- **Original content preferred** — recycled presentations unlikely to be accepted
- **Also has:** GenAI X Summit (business/executive track) — different audience, different tone

### PyData (Global, London, Berlin, Amsterdam, etc.)
- **Formats:** 30-min talks (Global), 40-min talks (London), 90-min tutorials
- **Review process:** Double-blind — do NOT include identifying information in abstract/description
- **Abstract fields:** Brief summary (few lines, for program) + longer description (structured, with objective, outline, thesis, key takeaways, and required background knowledge)
- **Open source focus:** Community of creators and users of open-source scientific computing tools
- **Mention libraries:** If your system uses open source tools, name them and clarify if it's a case study or library deep-dive
- **First-time speakers:** Indicate in your proposal — PyData offers a speaker mentorship program pairing you with experienced presenters
- **Sales pitches rejected:** You can reference closed-source products but the talk must focus on techniques and insights
- **Strong preference for new talks** — if your talk is already available online, it's unlikely to be accepted
- **Keep proposals focused:** Good proposals typically provide all important information within 200 words (not a strict limit)
- **Tip:** The community values practical, reproducible work with open-source tools

### PyCon US
- **Formats:** 30-min or 45-min talks, 90-min tutorials, posters, charlas (Spanish-language talks)
- **Proposal limit:** Maximum 3 proposals per person (including all types)
- **Max speakers:** 2 per proposal (exceptions for panels/podcasts)
- **Special tracks (2026):** "The Future of AI with Python" and "Trailblazing Python Security"
- **Audience levels:** "Just starting out" (introductory), "Some experience" (intermediate), "Advanced experience"
- **Mentorship program:** Submit early to participate in proposal mentorship before the deadline
- **Past proposals available:** PyCon publishes accepted AND rejected proposals for reference
- **Speaker grants:** Travel grant available (1 per accepted proposal in 2026)
- **Values:** Diversity of speakers, practical Python content, community building
- **Tip:** "What excites you about Python? What do you wish someone had told you?" — lean into genuine enthusiasm

### TED / TEDx
- **Fundamentally different format** — not a traditional CFP process
- **TED main stage:** By nomination/invitation only via [speaker-nominations.ted.com](https://speaker-nominations.ted.com/)
- **TEDx Global Idea Search:** Submit a 1-minute video pitching your idea; finalists get coaching; one speaker per region invited to TED Vancouver
- **TEDx local events:** Each independently organized with its own application process; many accept year-round
- **Talk length:** Typically 7-15 minutes (max 18 minutes); most are under 12 minutes
- **What they want:** NEW and NOVEL ideas that change attitudes, minds, or lives — must offer a unique insight or new way of thinking
- **The Venn diagram test:** Your idea must sit at the intersection of: (1) your domain of expertise, (2) something you're passionate about sharing, (3) something with real value to the audience
- **Coaching:** Selected speakers go through 3-4 months of talk development with a speaker coach
- **What disqualifies:** Motivational talks, canned talks given elsewhere, self-promotion, fundraising, political/religious agendas, unproven pseudo-science, traumatic events not adequately processed
- **Key difference from other conferences:** TED is about ONE powerful idea, not technical depth. The proposal is about the idea, not the methodology.
- **Speakers are unpaid** — this is a platform for ideas, not a speaking engagement
- **Tip:** Lead with "What is the ONE idea?" — if you can't state it in one sentence, it's not ready for TED

### KDD (Knowledge Discovery and Data Mining)
- **Tracks:** Research Track, Applied Data Science (ADS) Track, AI for Sciences Track, Datasets & Benchmarks Track
- **ADS Track key requirement:** Must include quantification of **post-launch performance** — submissions without this are desk-rejected
- **Format:** 8-page papers (not talk proposals) submitted via OpenReview
- **Double-blind review** for research track
- **Reviewer obligation:** Each submission must nominate at least one qualified reviewer from the author list
- **Resubmission rules:** Strict policies on revisions from previous cycles
- **Multiple cycles per year:** Two deadlines annually
- **Tip:** KDD ADS is for deployed systems with real metrics — not prototypes or theoretical work

### NeurIPS / ICML (Academic ML Conferences)
- **Format:** Paper submissions (not talk proposals) — 8-10 pages
- **Workshop proposals:** Due 4-5 months before conference; require topic description, invited speakers, organizer bios, diversity plan
- **Workshop papers:** Extended abstracts (4-6 pages) submitted to individual accepted workshops
- **Review:** Double-blind via OpenReview
- **Focus:** Novel research contributions, not practitioner talks
- **Tip:** These are academic venues — focus on novelty, rigor, and reproducibility rather than practical deployment stories

### General Best Practices (All Conferences)
- Detailed outlines correlate almost perfectly with acceptance
- Concrete takeaways differentiate accepted from rejected proposals
- The "why you" question must be answered in the bio
- Specificity > breadth: "How We Reduced Inference Latency 10x" beats "ML Optimization Tips"
- Submit early — many conferences have mentorship programs for early submissions
- Submit multiple proposals — committees know their gaps better than you do
- Get peer feedback before submitting
- Don't recycle proposals across conferences without tailoring them

---

## File Structure

```
conference-proposal-generator/
├── SKILL.md                    # This file — orchestration workflow
└── agents/
    ├── brainstorm_agent.md     # Generates 3-5 proposal angles
    ├── writer_agent.md         # Writes the full proposal draft
    └── critic_agent.md         # Reviews against CFP best practices
```

---

## Quick Reference

### Subagents
| Name | File | Model | Purpose |
|------|------|-------|---------|
| `brainstorm-agent` | `agents/brainstorm_agent.md` | opus | Generates multiple creative angles from a vague idea |
| `writer-agent` | `agents/writer_agent.md` | opus | Writes the complete proposal draft |
| `critic-agent` | `agents/critic_agent.md` | sonnet | Reviews proposal against CFP best practices |

### Common Rejection Reasons (What the Critic Catches)
| Reason | What It Looks Like | Fix |
|--------|-------------------|-----|
| **Too vague** | "Learn about ML best practices" | Add specific techniques, metrics, outcomes |
| **No unique angle** | Generic topic anyone could present | Add your specific experience or results |
| **Sales pitch** | Product name in title, feature-focused abstract | Focus on the problem solved, not the tool |
| **Missing takeaways** | "Attendees will gain insights" | List 3 concrete things they'll be able to do |
| **No outline** | Just a title and abstract | Add timed section-by-section breakdown |
| **AI-generated voice** | "In today's rapidly evolving landscape..." | Rewrite with authentic human voice |
| **Wrong audience** | Too basic for advanced track, too advanced for beginners | Align depth with stated audience |
| **Too broad** | Covers 10 topics in 40 minutes | Pick one thing and go deep |
