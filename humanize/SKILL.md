---
name: humanize
description: Transforms text through an iterative actor-critic loop until it cannot be distinguished from human writing and contains no logical fallacies.
---

# Humanize Skill

This skill takes input text and runs an iterative actor-critic loop to transform it into natural, human-like writing while ensuring logical consistency.

## Overview

The skill spawns two types of subagents in a loop:

1. **Critic Agent**: Evaluates text for AI-generated characteristics and logical fallacies
2. **Actor Agent**: Rewrites text based solely on the critic's feedback

The loop continues until the critic determines that:
- The text cannot be distinguished from human writing, AND
- There are no logical fallacies, OR the critic cannot determine authorship

## Workflow

```
INPUT TEXT → CRITIC → (needs work?) → ACTOR → CRITIC → ... → FINAL TEXT
                ↓ (pass)
            OUTPUT
```

### Step 0: Receive Input

Receive the text to be humanized from the user. The text can be any length and on any topic.

### Step 1: Initial Critic Evaluation

Spawn the `critic-agent` subagent to evaluate the input text.

Use the Task tool to spawn the `critic-agent`:
- **subagent_type:** Reference the `critic-agent` defined in `agents/critic_agent.md`
- **prompt:** Include the full text to be evaluated

The critic will return a structured evaluation containing:
- `verdict`: Either `PASS` or `NEEDS_REVISION`
- `ai_markers`: List of detected AI-generated characteristics (if any)
- `logical_issues`: List of logical fallacies or inconsistencies (if any)
- `confidence`: How confident the critic is in their assessment
- `feedback`: Specific, actionable feedback for improvement (if verdict is NEEDS_REVISION)

### Step 2: Check Termination Condition

If the critic's verdict is `PASS`, proceed to Step 5 (Output).

If the critic's verdict is `NEEDS_REVISION`, proceed to Step 3.

### Step 3: Actor Rewrite

Spawn the `actor-agent` subagent to rewrite the text.

Use the Task tool to spawn the `actor-agent`:
- **subagent_type:** Reference the `actor-agent` defined in `agents/actor_agent.md`
- **prompt:** Include:
  1. The current version of the text
  2. The critic's feedback (ONLY the feedback, not the original text analysis)

The actor will return the rewritten text.

**IMPORTANT**: The actor receives ONLY the critic's feedback, not the original evaluation details. This ensures the actor focuses on addressing specific issues rather than gaming detection criteria.

### Step 4: Loop Back to Critic

Spawn a NEW `critic-agent` subagent to evaluate the rewritten text.

This must be a fresh critic instance to ensure unbiased evaluation.

Return to Step 2.

### Step 5: Output

Return the final text to the user along with:
- Number of iterations performed
- Summary of improvements made across iterations

## Iteration Limits

To prevent infinite loops, the skill enforces:
- **Maximum iterations**: 5
- If the maximum is reached, return the best version with a note that the limit was reached

## Agent Definitions

The subagents are defined in the `agents/` directory:
- `agents/critic_agent.md` - The critic that evaluates text
- `agents/actor_agent.md` - The actor that rewrites text

## Example Usage

```
User: /humanize

The implementation of machine learning algorithms necessitates a comprehensive
understanding of the underlying mathematical frameworks. It is important to note
that neural networks, in particular, require substantial computational resources.
Furthermore, the optimization of hyperparameters is a crucial step in the model
development process.
```

Expected behavior:
1. Critic identifies AI markers (formal language, "it is important to note", "furthermore", passive voice)
2. Actor rewrites with more natural language
3. New critic evaluates the rewrite
4. Loop continues until text passes or limit reached
5. Final humanized text returned
