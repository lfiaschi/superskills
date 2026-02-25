# Code Presentation Principles

**INSTRUCTION:** This reference describes WHEN and HOW to present code. The examples use dummy content to illustrate structure only. Do NOT copy variable names, comments, or code logic.

---

## When to Show Code

### Show Full Code When:
- The implementation IS the insight
- Choices are non-obvious and instructive
- Reader needs to reproduce exactly

### Show Snippets When:
- Illustrating a specific technique
- Highlighting configuration choices
- Full code available elsewhere (link it)

### Describe Without Code When:
- Focus is on results, not method
- Audience is non-technical
- Operations are standard/obvious

---

## Code Block Structure Principles

### Principle 1: Comments Explain "Why", Not "What"

**BAD (what):**
```python
# Loop through items
for item in items:
    # Call process function
    process(item)
```

**GOOD (why):**
```python
# Process items sequentially to preserve order dependency
for item in items:
    process(item)
```

---

### Principle 2: Meaningful Names Over Comments

**BAD:**
```python
x = get_data()  # Get the customer data
y = transform(x)  # Apply transformation
```

**GOOD:**
```python
customer_data = load_customer_records()
normalized_data = apply_normalization(customer_data)
```

---

### Principle 3: Visual Section Breaks

Use `# ---` or `# === Section Name ===` to group related code:

```
STRUCTURE PATTERN — DO NOT COPY CONTENT

# --- Configuration ---
[configuration code]

# --- Data Loading ---
[data code]

# --- Model Definition ---
[model code]

# --- Inference ---
[inference code]
```

---

### Principle 4: Annotate Non-Obvious Choices

```
STRUCTURE PATTERN — DO NOT COPY CONTENT

result = function_call(
    obvious_param=value,
    non_obvious_param=value,  # Explain why this value
)
```

---

## Mathematical Notation Principles

### Inline Math
Use for variables and simple expressions within sentences.
Pattern: "The parameter $[symbol]$ controls [plain meaning]."

### Block Equations
Use for important formulas that need emphasis.
Always follow with interpretation.

```
STRUCTURE PATTERN:

[Prose introducing what the equation represents]

$$
[equation]
$$

Where:
- $[symbol]$ = [plain meaning]
- $[symbol]$ = [plain meaning]

[Interpretation connecting equation back to intuition]
```

---

### Anti-Pattern: Math Before Intuition

**BAD:** Equation appears, then explanation

**GOOD:** Intuition → Equation → Interpretation

---

## Visualization Code Principles

### Principle: Every Plot Needs Purpose
Before showing plotting code, be clear what insight the plot reveals.

### Principle: Consistent Styling
Use consistent colors, labels, sizes across all figures in a post.

### Principle: Uncertainty Bands
When showing predictions, include confidence/credible intervals, not just point estimates.

---

## Import Section Principles

- Group by purpose (data, modeling, visualization)
- Standard library first, then third-party, then local
- Configuration (figure sizes, styles) at end of imports

---

## Collapsible Code

For long implementations that distract from narrative flow:

```markdown
<details>
<summary>Full implementation (click to expand)</summary>

[long code block]

</details>
```

Use when:
- Code is long but reader might want reference
- Implementation details are secondary to concepts
- Reproducibility matters but flow matters more

---

## Anti-Patterns in Code Presentation

### ❌ Unexplained Magic Numbers
```python
result = compute(x, 0.7, 12, 3)  # What are these?
```

### ❌ Code Without Context
Dropping a code block with no prose explaining what it does or why.

### ❌ Screenshots of Code
Always use copyable text blocks, never images of code.

### ❌ Untested Code
Code in posts should run. Test before publishing.

---

## Final Instruction

When presenting code in a blog post:
1. Decide: show, snippet, or describe?
2. If showing: structure with visual breaks and why-comments
3. If math: intuition → equation → interpretation
4. Create your own variable names and comments appropriate to your topic
5. Do NOT copy the placeholder patterns as actual code
