# Slide Prompt Templates

Comprehensive prompt templates for generating professional, McKinsey-style slides with the Nano Banana API.

## Master Style Template (McKinsey Default)

Prepend this base style to ALL prompts for consistency:

```
[BASE_STYLE]: McKinsey-style consulting presentation slide, 16:9 aspect ratio,
deep navy (#1a365d) and white color scheme, clean Helvetica/Arial typography,
data-driven professional aesthetic, structured layout with clear visual hierarchy.
```

## Key Principles for Compelling Slides

1. **Action titles**: State the insight, not the topic
2. **Data-driven**: Include specific numbers, percentages, comparisons
3. **Visual hierarchy**: Most important element is largest/boldest
4. **White space**: Don't crowd - less is more
5. **One idea per slide**: If you need "and", split into two slides

---

## 1. Title/Cover Slides

### Corporate Title

```
Create a modern minimalist presentation cover slide, 16:9 aspect ratio.
Title: "[MAIN TITLE]"
Subtitle: "[SUBTITLE OR DATE]"
Visual style: Clean corporate design with subtle gradient background
Color scheme: [PRIMARY COLOR] to [SECONDARY COLOR] gradient
Include: Company logo placeholder in bottom right corner
Typography: Bold sans-serif title, light weight subtitle
```

**Example:**
```
Create a modern minimalist presentation cover slide, 16:9 aspect ratio.
Title: "Q4 2025 Business Review"
Subtitle: "Strategic Initiatives & Performance Metrics"
Visual style: Clean corporate design with subtle gradient background
Color scheme: Deep navy (#1a365d) to slate blue (#475569) gradient
Include: Company logo placeholder in bottom right corner
Typography: Bold sans-serif title, light weight subtitle
```

### Creative Title

```
Create an eye-catching presentation cover slide, 16:9 aspect ratio.
Title: "[TITLE]"
Visual style: [CREATIVE STYLE - e.g., watercolor, geometric, abstract]
Include: [VISUAL ELEMENTS]
Mood: [MOOD - e.g., energetic, sophisticated, playful]
```

---

## 2. Agenda/Overview Slides

### Numbered Agenda

```
Create a presentation agenda slide, 16:9 aspect ratio.
Title: "Agenda" or "Today's Topics"
Items (numbered list):
1. [TOPIC 1]
2. [TOPIC 2]
3. [TOPIC 3]
4. [TOPIC 4]
Visual style: Clean layout with numbered items vertically aligned
Color scheme: [COLORS]
Include: Subtle icons next to each item representing the topic
```

### Visual Roadmap

```
Create a presentation roadmap slide, 16:9 aspect ratio.
Title: "[TITLE]"
Show horizontal timeline with these milestones:
- [MILESTONE 1]
- [MILESTONE 2]
- [MILESTONE 3]
- [MILESTONE 4]
Visual style: Connected pathway or timeline design
Include: Icons at each milestone point
```

---

## 3. Content Slides

### Single Key Point

```
Create a presentation content slide, 16:9 aspect ratio.
Title: "[SLIDE TITLE]"
Main message: "[KEY POINT - one sentence]"
Supporting text: "[2-3 bullet points]"
Visual style: Large title, prominent key message, smaller supporting text
Color scheme: [COLORS]
Layout: Title top, key message center, bullets below
```

### Three Columns

```
Create a presentation slide with three columns, 16:9 aspect ratio.
Title: "[TITLE]"
Column 1: "[HEADING 1]" - [Description 1]
Column 2: "[HEADING 2]" - [Description 2]
Column 3: "[HEADING 3]" - [Description 3]
Visual style: Equal-width columns with icons above each heading
Include: Relevant icon for each column
Color scheme: [COLORS]
```

### Quote Slide

```
Create a presentation quote slide, 16:9 aspect ratio.
Quote: "[EXACT QUOTE TEXT]"
Attribution: "- [SPEAKER NAME], [TITLE/COMPANY]"
Visual style: Large quotation marks, centered text, elegant typography
Background: [SOLID COLOR OR SUBTLE PATTERN]
```

---

## 4. Data Visualization Slides

### Bar Chart

```
Create a presentation slide with a bar chart, 16:9 aspect ratio.
Title: "[CHART TITLE]"
Data:
- [Category 1]: [Value 1]
- [Category 2]: [Value 2]
- [Category 3]: [Value 3]
- [Category 4]: [Value 4]
Chart type: Horizontal/Vertical bar chart
Include: Value labels on each bar
Color scheme: [COLORS]
Y-axis label: "[UNIT]"
```

**Example:**
```
Create a presentation slide with a bar chart, 16:9 aspect ratio.
Title: "Revenue by Region"
Data:
- North America: $2.4M
- Europe: $1.8M
- Asia Pacific: $1.2M
- Latin America: $0.6M
Chart type: Horizontal bar chart
Include: Value labels on each bar
Color scheme: Blue gradient (darkest for highest value)
```

### Pie/Donut Chart

```
Create a presentation slide with a donut chart, 16:9 aspect ratio.
Title: "[TITLE]"
Data:
- [Segment 1]: [Percentage]%
- [Segment 2]: [Percentage]%
- [Segment 3]: [Percentage]%
Include: Percentage labels, legend on right side
Center text: "[TOTAL OR KEY METRIC]"
Color scheme: [DISTINCT COLORS FOR EACH SEGMENT]
```

### Line Chart/Trend

```
Create a presentation slide showing a trend line, 16:9 aspect ratio.
Title: "[TITLE]"
X-axis: [TIME PERIOD - e.g., Q1 2024 to Q4 2025]
Y-axis: [METRIC]
Data points:
- [Period 1]: [Value]
- [Period 2]: [Value]
- [Period 3]: [Value]
Include: Data point markers, trend direction indicator
Highlight: [KEY INSIGHT - e.g., "25% growth"]
```

### KPI Dashboard

```
Create a presentation slide with key metrics, 16:9 aspect ratio.
Title: "[TITLE]"
Metrics (display as large numbers with labels):
- [METRIC 1 NAME]: [VALUE 1]
- [METRIC 2 NAME]: [VALUE 2]
- [METRIC 3 NAME]: [VALUE 3]
Include: Trend arrows (up/down) for each metric
Visual style: Dashboard-style cards or tiles
Color scheme: [COLORS - green for positive, red for negative trends]
```

---

## 5. Comparison Slides

### Two-Column Comparison

```
Create a presentation comparison slide, 16:9 aspect ratio.
Title: "[COMPARISON TITLE]"
Left column - "[OPTION A]":
- [Feature 1]
- [Feature 2]
- [Feature 3]
Right column - "[OPTION B]":
- [Feature 1]
- [Feature 2]
- [Feature 3]
Visual style: Clear division, matching layout for both columns
Include: Checkmarks or icons for features
```

### Before/After

```
Create a presentation before-and-after slide, 16:9 aspect ratio.
Title: "[TITLE]"
Left side - "Before":
[DESCRIPTION OR METRICS]
Right side - "After":
[DESCRIPTION OR METRICS]
Visual style: Clear contrast between sides
Include: Arrow or transformation indicator between sides
Highlight: Key improvements or changes
```

### Feature Matrix

```
Create a presentation comparison matrix slide, 16:9 aspect ratio.
Title: "[TITLE]"
Compare: [OPTION 1] vs [OPTION 2] vs [OPTION 3]
Features to compare:
- [Feature A]: [✓/✗ for each option]
- [Feature B]: [✓/✗ for each option]
- [Feature C]: [✓/✗ for each option]
Visual style: Clean table with checkmarks and X marks
Highlight: [RECOMMENDED OPTION] column
```

---

## 6. Process/Workflow Slides

### Linear Process

```
Create a presentation process flow slide, 16:9 aspect ratio.
Title: "[PROCESS NAME]"
Steps (show as connected horizontal flow):
1. [STEP 1]
2. [STEP 2]
3. [STEP 3]
4. [STEP 4]
Visual style: Numbered circles or boxes connected by arrows
Include: Brief description under each step
Color scheme: [COLORS - progression from light to dark]
```

### Circular Process

```
Create a presentation slide showing a cyclical process, 16:9 aspect ratio.
Title: "[TITLE]"
Cycle stages:
1. [STAGE 1]
2. [STAGE 2]
3. [STAGE 3]
4. [STAGE 4]
Visual style: Circular diagram with arrows connecting stages
Include: Icons for each stage
```

### Funnel

```
Create a presentation funnel diagram slide, 16:9 aspect ratio.
Title: "[TITLE]"
Funnel stages (top to bottom):
- [STAGE 1]: [VALUE/PERCENTAGE]
- [STAGE 2]: [VALUE/PERCENTAGE]
- [STAGE 3]: [VALUE/PERCENTAGE]
- [STAGE 4]: [VALUE/PERCENTAGE]
Visual style: Tapering funnel shape
Include: Conversion rates between stages
Color scheme: Gradient from [TOP COLOR] to [BOTTOM COLOR]
```

---

## 7. Summary/Conclusion Slides

### Key Takeaways

```
Create a presentation summary slide, 16:9 aspect ratio.
Title: "Key Takeaways"
Points (3-5 items with icons):
1. [TAKEAWAY 1]
2. [TAKEAWAY 2]
3. [TAKEAWAY 3]
Visual style: Large numbered list with relevant icons
Layout: Generous whitespace, easy to read
```

### Call to Action

```
Create a presentation call-to-action slide, 16:9 aspect ratio.
Headline: "[ACTION STATEMENT]"
Supporting text: "[BRIEF CONTEXT]"
Action items:
- [ACTION 1]
- [ACTION 2]
Contact: "[EMAIL/WEBSITE]"
Visual style: Bold, attention-grabbing, centered layout
```

### Thank You/Q&A

```
Create a presentation closing slide, 16:9 aspect ratio.
Main text: "Thank You" or "Questions?"
Include: [PRESENTER NAME], [TITLE]
Contact info: [EMAIL], [PHONE/SOCIAL]
Visual style: Clean, professional, consistent with deck theme
Include: Company logo
```

---

## 8. Specialized Slides

### Timeline

```
Create a presentation timeline slide, 16:9 aspect ratio.
Title: "[TIMELINE TITLE]"
Events (chronological):
- [DATE 1]: [EVENT 1]
- [DATE 2]: [EVENT 2]
- [DATE 3]: [EVENT 3]
- [DATE 4]: [EVENT 4]
Visual style: Horizontal timeline with markers
Current position: Highlight [CURRENT DATE/MILESTONE]
```

### Org Chart

```
Create a presentation organizational chart slide, 16:9 aspect ratio.
Title: "[TITLE]"
Structure:
Top: [TOP ROLE/NAME]
Second level: [ROLE 1], [ROLE 2], [ROLE 3]
Third level: [REPORTS]
Visual style: Clean hierarchical boxes with connecting lines
Include: Role titles, names optional
```

### Map/Geographic

```
Create a presentation map slide, 16:9 aspect ratio.
Title: "[TITLE]"
Show: [REGION/WORLD MAP]
Highlight locations:
- [LOCATION 1]: [DATA/LABEL]
- [LOCATION 2]: [DATA/LABEL]
- [LOCATION 3]: [DATA/LABEL]
Visual style: Clean map with data overlays
Color scheme: [COLORS]
```

---

## Style Variations

### McKinsey/Consulting Style (Recommended Default)

Add to any prompt:
```
Visual style: McKinsey consulting presentation format, data-driven,
deep navy (#1a365d) and white color scheme, clean sans-serif typography,
structured layouts with clear hierarchy, executive-ready aesthetic
```

---

## 9. McKinsey-Style Complete Examples

### Insight-Led Title Slide

```
Create a McKinsey-style presentation cover slide, 16:9 aspect ratio.
Title: "Gamified Loyalty Platforms Unlock $223M+ in User Value"
Subtitle: "How three-sided marketplaces align incentives to drive 3x retention"
Footer: "Strategic Analysis | January 2025"
Visual style: Executive consulting presentation, bold confident typography
Color scheme: Deep navy (#1a365d) gradient background, white text
Typography: Large bold title (dominant), lighter subtitle, small footer
Include: Subtle geometric accent shapes suggesting growth/connection
```

### Data-Driven Problem Slide

```
Create a McKinsey-style problem statement slide, 16:9 aspect ratio.
Title: "Mobile gaming's $100B market runs on broken unit economics"
Display as prominent stat callout boxes (4 boxes in a row):
- Box 1: "$100B+" label "Annual Revenue"
- Box 2: "30-50%" label "YoY UA Cost Increase" (with red up arrow)
- Box 3: "Week 1" label "Majority Churn Window"
- Box 4: "$Billions" label "Wasted on Non-Retaining Users"
Bottom insight text: "Traditional CPI model pays regardless of user value, creating systematic inefficiency"
Visual style: McKinsey consulting, data-forward, clean stat cards
Color scheme: Deep navy background, white cards with navy text, red accent for negative metrics
```

### KPI Dashboard Slide

```
Create a McKinsey-style metrics dashboard slide, 16:9 aspect ratio.
Title: "Platform achieved scale while maintaining quality and user satisfaction"
Four large KPI cards in a grid:
- Card 1: "10M+" with label "Active Users" and green up arrow
- Card 2: "$223M+" with label "Rewards Distributed" and green up arrow
- Card 3: "4.3★" with label "App Store Rating (945K reviews)"
- Card 4: "30+" with label "Gift Card Partners"
Visual style: Executive dashboard, large bold numbers, clean cards with subtle shadows
Color scheme: Navy header, white background, navy text, green trend indicators
Layout: Title at top, 2x2 grid of metric cards below
```

### Framework/Matrix Slide (2x2)

```
Create a McKinsey-style 2x2 matrix slide, 16:9 aspect ratio.
Title: "Four user archetypes require tailored engagement strategies"
2x2 matrix with quadrants:
- Top-left: "CASUAL EARNER" - "Entertainment + bonus" - Icon: game controller
- Top-right: "OPTIMIZER" - "Maximize earnings" - Icon: calculator
- Bottom-left: "EXPLORER" - "Game discovery" - Icon: compass
- Bottom-right: "STATUS SEEKER" - "Achievement & recognition" - Icon: trophy
Axes: X-axis "Earning Focus →", Y-axis "Engagement Depth →"
Visual style: Classic consulting 2x2 framework, clean quadrants
Color scheme: Navy labels, each quadrant has distinct but harmonious blue shade
Include: Simple icons in each quadrant, axis labels outside matrix
```

### Process Flow Slide

```
Create a McKinsey-style process flow slide, 16:9 aspect ratio.
Title: "Checkpoint architecture transforms playtime into measurable value"
Horizontal flow with 4 stages (connected by arrows):
- Stage 1: "CHECKPOINT 1" - "Complete Tutorial" - "Signal: User tried game"
- Stage 2: "CHECKPOINTS 2-3" - "Reach Level 5-10" - "Signal: Core loop engagement"
- Stage 3: "CHECKPOINTS 4-6" - "Reach Level 15-25" - "Signal: Likely to retain"
- Stage 4: "CHECKPOINT 7+" - "Advanced Milestones" - "Signal: High-value user"
Visual style: Left-to-right progression, numbered circles connected by arrows
Color scheme: Gradient from light blue (stage 1) to deep navy (stage 4) showing increasing value
Include: Small text descriptions under each stage
```

### Three-Column Insight Slide

```
Create a McKinsey-style three-column slide, 16:9 aspect ratio.
Title: "Three psychological mechanisms drive sustainable engagement"
Three equal columns:
- Column 1: Icon (brain with progress bar), Heading "PROGRESS", Subtext "Endowed progress effect", Detail "Visible milestones increase completion rates by 2x"
- Column 2: Icon (slot machine/dice), Heading "VARIABLE REWARDS", Subtext "Intermittent reinforcement", Detail "Unpredictability sustains engagement without fatigue"
- Column 3: Icon (trophy/medal), Heading "STATUS", Subtext "Identity & belonging", Detail "Tier systems create aspirational progression paths"
Visual style: Clean three-column consulting layout, balanced spacing
Color scheme: Navy headers, gray detail text, blue icons
Include: Horizontal line separating title from content
```

### Comparison Slide (Before/After or Vs)

```
Create a McKinsey-style comparison slide, 16:9 aspect ratio.
Title: "Performance-based pricing shifts risk from publishers to platform"
Two-column comparison:
Left column - "TRADITIONAL CPI MODEL":
- "Pay per install regardless of quality"
- "5% Day-7 retention typical"
- "Effective cost: $60 per retained user"
- Red X icons for each point
Right column - "PERFORMANCE-BASED MODEL":
- "Pay only for demonstrated engagement"
- "Time spent, progression, monetization verified"
- "Lower effective cost, higher quality users"
- Green checkmark icons for each point
Visual style: Clear left/right division, contrasting evaluation
Color scheme: Navy background for headers, red tint left side, green tint right side
Include: Arrow or "vs" indicator between columns
```

### Key Takeaways Slide

```
Create a McKinsey-style summary slide, 16:9 aspect ratio.
Title: "Six principles for designing loyalty systems that users want"
Six numbered points (2 columns of 3):
1. "Make progress visible and achievable" - Milestones beat abstract points
2. "Layer variable rewards on stable foundations" - Surprise on top of reliability
3. "Create status that matters" - Tiers must unlock real value
4. "Design for multiple motivations" - Same mechanics, different psychological frames
5. "Experiment continuously" - Intuition fails; test everything
6. "Align all stakeholder incentives" - Positive-sum or it won't last
Visual style: Clean numbered list, generous whitespace, easy to scan
Color scheme: Navy numbers, black text, light gray background
Layout: Title at top, 2 columns of 3 takeaways below
```

### Call-to-Action Closing Slide

```
Create a McKinsey-style closing slide, 16:9 aspect ratio.
Main quote: "The future belongs to loyalty systems that users actually want to be part of."
Attribution: "Luca Fiaschi, Former Head of Economy & Experimentation"
Bottom text: "Engagement is not zero-sum. Systems designed for authentic user needs create value for everyone."
Visual style: Centered, elegant, confident closing statement
Color scheme: Deep navy gradient background, white text, subtle geometric accents
Typography: Large quote text, smaller attribution, medium insight text
```

### Startup/Modern Style

Add to any prompt:
```
Visual style: Modern startup aesthetic, bold gradients,
rounded shapes, vibrant accent colors, contemporary typography,
generous whitespace
```

### Technical/Engineering Style

Add to any prompt:
```
Visual style: Technical blueprint aesthetic, precise lines,
monospace typography for code/data, grid-based layout,
dark background with light text option
```

### Creative/Marketing Style

Add to any prompt:
```
Visual style: Creative marketing presentation, bold typography,
dynamic compositions, lifestyle imagery integration,
brand-forward design
```
