# Synthetic Consumers Meet Bayesian AI: 90% Brand Panel Accuracy on the Lakehouse

## Abstract

Brand measurement is broken. Traditional consumer panels cost six figures, take weeks to deliver, and by the time results reach a CMO's desk, the market has already moved. Every brand leader says the same thing: "I need faster reads on how my brand is performing." But until recently, faster meant less reliable -- and unreliable brand data is worse than no data at all.

This talk presents an open-source architecture for AI-powered synthetic consumers that simulate real brand perception and purchasing behavior. The system runs distributed persona generation across Spark, tracks all calibration experiments in MLflow, and versions both synthetic and validation datasets in Delta Lake. A Bayesian uncertainty layer quantifies confidence on every output: when the model interpolates from strong data, confidence intervals tighten; when it extrapolates into unfamiliar territory, the system flags the gap and recommends a real panel. Synthetic insights then feed into Marketing Mix Models as calibrated priors, and an AI agent co-pilot -- served via Databricks Model Serving -- takes practitioners from raw data to budget allocation recommendations.

The results held up. Validated against Colgate's consumer panels, synthetic respondents achieved a 73-74% direct agreement rate on brand metrics. Across a U.S. synthetic panel of 100,000+ respondents generated in under four hours on a standard Databricks cluster, the system replicated up to 90% of real consumer behavior patterns -- at roughly one-tenth the cost of traditional panels. A major fashion brand adopted the full pipeline in production.

Attendees will leave with a lakehouse-native architecture blueprint for uncertainty-aware synthetic research, concrete validation frameworks, and a clear path from brand intelligence to MMM budget optimization -- built on open-source tools including PyMC-Marketing (Apache 2.0).

## Detailed Outline

### Opening: The Six-Figure Question (5 minutes)
- A single brand tracking wave can cost $150K+ and take 4-6 weeks. By the time you act on it, you're already behind.
- Why "just survey faster" doesn't work: cheaper panels sacrifice sample quality. Online panels have fraud rates above 30% in some categories.
- The provocation: What if you could generate brand perception data in hours, at a fraction of the cost, and know exactly when to trust it?

### Section 1: Synthetic Consumers -- How They Work and Why Now (8 minutes)
- What synthetic consumers actually are: LLM-generated personas calibrated against real demographic, psychographic, and behavioral distributions.
- The calibration pipeline: distributed persona generation on Spark, with calibration datasets stored in Delta Lake and all experiments tracked in MLflow. [Architecture diagram #1: Synthetic consumer generation and calibration pipeline on Databricks]
- Scalability benchmarks: generating 100K+ synthetic respondents in under four hours on a 32-node Spark cluster, with per-respondent Bayesian scoring latency under 150ms.
- Why the timing is right: foundation models crossed a capability threshold in 2025.

### Section 2: Bayesian Uncertainty -- Quantifying Confidence on Every Output (8 minutes)
- The core problem: point estimates alone mask the uncertainty that matters most for decision-making. The Bayesian layer produces calibrated confidence intervals on every synthetic output.
- Interpolation vs. extrapolation detection in practice: how the system identifies when it's operating within well-supported demographic segments vs. stretching beyond training data. [Architecture diagram #2: Uncertainty quantification and interpolation/extrapolation classification]
- The Colgate validation: 73-74% direct agreement rate, with uncertainty intervals that correctly flagged the metrics where synthetic and real panels diverged.

### Section 3: From Brand Signals to Budget Decisions -- The Full Stack (10 minutes)
- Feeding synthetic insights into Marketing Mix Models as calibrated priors, with model artifacts versioned in MLflow and results landing in Delta Lake for downstream analytics. [Architecture diagram #3: End-to-end lakehouse architecture]
- The AI MMM Agent co-pilot, served via Databricks Model Serving. [Live demo or recorded demo: 3-minute walkthrough]
- Pipeline orchestration: Databricks Workflows scheduling synthetic panel generation, Bayesian calibration, and MMM refresh on a weekly cadence.
- Production case study: fashion brand adoption arc -- from pilot to replacing their quarterly panel process.

### Section 4: Validation Frameworks (5 minutes)
- The 90% replication benchmark: which brand perception patterns replicate reliably, and which categories need real panel supplementation.
- A practical validation checklist: three concrete statistical tests any team can run against their own Delta Lake panel data.
- When to NOT use synthetic data: honest boundaries.

### Closing: Open-Source Tools and Your Implementation Path (4 minutes)
- PyMC-Marketing (Apache 2.0) and the open-source ecosystem.
- Concrete next steps: setting up the calibration pipeline on your Databricks workspace, connecting to your existing MMM, and running your first validation benchmark.
- Q&A teaser.

## Audience Takeaways

1. A validation playbook for synthetic consumer research -- including specific statistical thresholds and the interpolation/extrapolation heuristic for deciding when to supplement with real panels.
2. A lakehouse-native architecture blueprint for connecting brand measurement to media spend optimization -- how synthetic brand perception outputs become calibrated Bayesian priors for MMMs, with components mapped to Spark, Delta Lake, MLflow, and Databricks Model Serving.
3. A clear-eyed assessment of where synthetic research works today and where it doesn't -- no overselling, with uncertainty-aware guardrails and reproducible benchmarks you can run on your own cluster.

## Target Audience & Prerequisites

**Ideal attendee:** Marketing science leaders, data science managers, and senior practitioners responsible for brand measurement, media mix optimization, or consumer insights.

**Prerequisites:** Familiarity with basic marketing analytics concepts and a general understanding of Bayesian statistics. Some experience with Databricks or Spark is helpful but not required.

**Difficulty level:** Intermediate.

## Speaker Bio

Dr. Luca Fiaschi leads the generative AI vertical at PyMC Labs and is a core contributor to PyMC, one of the most widely adopted open-source libraries for Bayesian modeling. His work sits at the intersection of probabilistic AI, causal inference, and real-world marketing science, and the synthetic consumer + MMM system in this talk is something he architected and shipped to production.

Before his current role, Luca served as VP of Data Science at Stitch Fix, where he built personalization systems at scale, and held senior roles at Alibaba and Rocket Internet. He holds a PhD in Computer Science from Heidelberg University.

Luca's talks tend to be heavy on architecture details and honest about what didn't work the first time -- because he thinks the failures are where the actual lessons live.

## Notes for Reviewers

**Why timely:** Synthetic data for market research crossed from experiment to production deployment in 2025.

**Why this talk fits the Summit:** The entire architecture runs on the Databricks stack -- Spark for distributed inference, MLflow for experiment tracking, Delta Lake for data versioning, Model Serving for the agent, and Workflows for orchestration. This is a real production system on the lakehouse, not a theoretical integration.

**Why this speaker:** Built and deployed this system. Direct experience validating against Colgate panels.

**Format flexibility:** Can adapt to 25-min or expand to 90-120 min workshop (workshop version would include a hands-on Databricks notebook for building a small synthetic panel).
