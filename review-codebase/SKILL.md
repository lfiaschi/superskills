---
name: review-codebase
description: "Performs a deep, comprehensive codebase review acting as both architect and principal engineer. This skill should be used when users ask for a codebase review, architecture review, code audit, or any request to evaluate the overall health, quality, and design of a codebase. Covers architecture, code health, bugs, security, performance, testing, observability, and developer experience. Produces a prioritized, actionable report."
---

# Review Codebase

**IMPORTANT DIRECTIVE: This is a READ-ONLY review. ABSOLUTELY DO NOT modify any existing code in any circumstance. Running existing tests and writing temporary test scripts to verify assumptions is permitted, but all such intermediate test scripts MUST be cleaned up (deleted) when done.**

## Mission

Understand how the system really works (not just how it is supposed to work). Expose architectural weaknesses, bugs, edge cases, dead code, and risky dependencies. Propose concrete, pragmatic changes that maximize long-term leverage. Operate as both architect and principal engineer: zoom out to system design, zoom in to implementation details where it matters most.

## Review Process

### Phase 1: Reconnaissance

Before any analysis, build a mental model of the codebase.

1. Discover project structure: use Glob to map top-level directories, key config files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `docker-compose.yml`, CI configs, etc.).
2. Identify the language(s), framework(s), and build system.
3. Read the README, CONTRIBUTING, and any architecture docs if they exist.
4. Scan entry points: main files, route definitions, CLI entry points, serverless handlers.
5. Map module/package boundaries and their import relationships.

Output a **System Map** (bulleted) covering:
- Main responsibilities of the system.
- Key components/services/modules and their responsibilities.
- Primary data flows, APIs, and boundaries between components.
- Mismatches between the apparent business domain and the current structure.
- Areas where the mental model of the system is unclear, contradictory, or undocumented.

Include a few sentences describing how data and control flow through the system.

### Phase 2: Parallel Deep-Dive Analysis

Launch focused sub-agents in parallel using the Task tool with `subagent_type=general-purpose`. Each sub-agent receives the System Map from Phase 1 plus its specific analysis brief below. Provide each sub-agent with the working directory and enough file paths/context to begin immediately.

**CRITICAL — READ-ONLY ENFORCEMENT FOR SUB-AGENTS:**

Every sub-agent prompt MUST include ALL THREE of the following blocks — at the START, in the MIDDLE (after the analysis brief), and at the END of the prompt. This triple-reinforcement is mandatory because sub-agents do not inherit the parent context and have a tendency to "helpfully" modify code.

**Block to paste at the START of every sub-agent prompt:**
```
=== MANDATORY CONSTRAINT — READ BEFORE DOING ANYTHING ===
This is a READ-ONLY code review. You are an auditor, not a developer.
- DO NOT use the Edit tool. DO NOT use the Write tool to modify existing files.
- DO NOT create, rename, move, or delete any existing file in the codebase.
- DO NOT run any command that modifies code (no sed, awk, patch, git checkout, git apply, etc.).
- You MAY use Read, Glob, Grep to inspect the codebase.
- You MAY run existing test suites (e.g., pytest, npm test) to observe behavior.
- You MAY write NEW temporary test scripts to verify assumptions, but you MUST delete them before finishing.
- If you feel the urge to "fix" something — STOP. Write it as a finding instead.
=== END CONSTRAINT ===
```

**Block to paste in the MIDDLE of every sub-agent prompt (after the analysis brief):**
```
REMINDER: Do NOT modify any existing code. Report findings only. Delete any temporary test scripts you created.
```

**Block to paste at the END of every sub-agent prompt:**
```
=== FINAL CHECK ===
Before returning your response, confirm:
1. You did NOT modify any existing file in the codebase.
2. You deleted any temporary test scripts you created.
3. Your output contains ONLY analysis, findings, and recommendations — no code changes were applied.
If you violated any of these, UNDO immediately before responding.
=== END FINAL CHECK ===
```

#### Sub-agent 1: Architecture and Design

Analyze the architecture as if evaluating it for a scaling, multi-team organization.

- **Boundaries, coupling, and cohesion**: Where are responsibilities tangled? Where do cross-cutting concerns (auth, logging, validation, caching) leak across layers? Where are modules too big, too generic, or too granular?
- **Architectural smells and anti-patterns**: God objects/services. Anemic domain models vs. over-engineered abstractions. Inconsistent layering (e.g., controllers reaching into persistence directly). Cyclic dependencies, spaghetti imports.
- **Specific refactorings**: New or adjusted boundaries (extract module X, split service Y, consolidate feature flags). Better placement of logic (move business rules out of controllers, move DB logic out of UI). Introduction of patterns where appropriate (adapters, ports, event-driven interactions) and removal of patterns where they add no value.
- For each major architectural issue, suggest a **realistic migration path** (phased, backwards-compatible where possible), not just an ideal end state.

*Reminder: READ-ONLY. Do not modify code. Report findings only.*

#### Sub-agent 2: Code Health and Dead Code

Systematically assess code quality and cleanliness.

- **Dead or low-value code**: Unused functions, classes, modules, endpoints, configs, feature flags, DB tables/columns. Abstractions that add indirection without clear benefit.
- **Removal/containment plan**: How to verify code is unused (static analysis, search, logs, telemetry). Steps to deprecate and delete safely. Opportunities to simplify call chains or APIs after removal.
- **Code health**: Violations of single-responsibility or obvious SOLID violations. Overly clever or opaque logic that will be hard to maintain. Duplicated logic that should be centralized. Places where adding a small, well-named helper or type would clarify intent.
- Call out the **highest-leverage cleanups** (those that unlock many small wins downstream).

*Reminder: READ-ONLY. Do not modify code. Report findings only.*

#### Sub-agent 3: Bugs, Correctness, and Edge Cases

Actively hunt for correctness issues.

- **Look for**: Logic bugs, race conditions, and data consistency issues. Misuse of async/concurrency primitives, locking, and transactions. Unclear or inconsistent error-handling paths. Off-by-one, nullability, boundary conditions, and input-validation gaps.
- For each suspected bug or risky area: describe a **concrete failing scenario** (inputs, state, sequence of calls). Explain potential **impact** (data loss, security issue, downtime, subtle corruption).
- **Explicitly list**: Unhandled edge cases. Assumptions in the code not enforced by types, validation, or invariants. Surprising behavior (anything a new engineer would not reasonably expect).
- Where appropriate, suggest how to enforce invariants (types, assertions, validation layers).

*Reminder: READ-ONLY. Do not modify code. Report findings only.*

#### Sub-agent 4: Security

Treat the system as if it will be Internet-facing, multi-tenant, and under load.

- **Identify**: Authn/authz gaps, over-broad permissions, and missing checks. Injection risks, unsafe deserialization, direct use of user input in sensitive operations. Insecure handling of secrets, tokens, and credentials. Data exposure via logs, error messages, or APIs.
- **Propose** specific mitigations and, where possible, centralization of security concerns.

*Reminder: READ-ONLY. Do not modify code. Report findings only.*

#### Sub-agent 5: Performance and Reliability

- **Performance**: N+1 queries and unnecessary round-trips. Inefficient data structures, needless allocations or copies. Hot paths doing work that could be cached, batched, or moved offline. Blocking operations in latency-sensitive paths. Suggest clear, targeted optimizations and metrics/profiling points needed to verify and monitor performance.
- **Reliability**: Missing timeouts, retries, circuit breakers, and backoff. Non-idempotent operations that may be retried by clients or infrastructure. Error handling that drops or swallows failures silently. Risky startup/shutdown behavior, migrations, and deployment scripts. Recommend how to make critical flows more robust and observable.

*Reminder: READ-ONLY. Do not modify code. Report findings only.*

#### Sub-agent 6: Testing and Observability

This sub-agent performs the deepest analysis of any category. It must produce a standalone **Test Suite Recommendations** section in its output.

**Part A — Test Inventory and Current State**

Map the current test landscape by category:
- **Unit tests**: What modules/functions are covered? What is actually being asserted (not just executed)?
- **Integration tests**: Which component boundaries are tested (service-to-DB, service-to-service, service-to-queue)?
- **E2E / system tests**: Which user journeys or API flows are covered end-to-end?
- **Acceptance / regression tests**: Are bug fixes locked in with tests? Are business rules codified?
- **Non-functional tests**: Do performance, load, security, or smoke tests exist?

For each category assess: coverage of critical features, reliability (flaky or stable), speed, and ease of extension. Produce a concise **test inventory** mapping test categories to system components.

**Part B — Target Testing Strategy**

Design the ideal test architecture for this system:
- Define what each layer should be responsible for (unit = isolated logic with no external deps; integration = component interactions; E2E = key user journeys through the full stack; non-functional = performance/load/security).
- Propose the right **test pyramid (or diamond)** shape for this system, with rough proportions. Some systems need heavier integration coverage than unit — be opinionated about which applies here.
- Propose how tests should be organized: directory layout, naming conventions, tagging/markers for CI selection.

**Part C — Coverage Gaps and Specific Tests to Add**

Identify under-tested or untested risk areas:
- Core business logic and data-critical flows.
- Security-sensitive behavior (auth, permissions, data access).
- Integration points (external APIs, queues, databases, third-party services).
- Error handling paths and edge cases.

For each gap, propose **specific tests** with:
- Type (unit, integration, E2E, property-based, regression, fuzz, load).
- Scenario description (inputs, edge cases, expected outputs/side effects).
- Where in the test tree it should live.

Also identify **low-value tests** that should be rewritten, merged, or deleted (overlapping, fragile, or testing at the wrong level).

**Part D — Flakiness, Speed, and Reliability**

Diagnose sources of flakiness:
- Time-dependent tests, random data, network dependencies, shared mutable state, test order dependence.
- External services not properly isolated or mocked.

Recommend concrete fixes:
- Making tests deterministic (controlling time, randomness, environment).
- Isolating slow/external dependencies.
- Splitting tests into fast vs. slow suites with clear execution profiles.
- Suggest target runtime budgets (e.g., max runtime for the "fast" suite in CI).

**Part E — Test Design Quality**

Review existing tests for:
- Clarity of intent (good naming, Arrange-Act-Assert structure).
- Overuse of mocking or fragile setups that break on any refactor.
- Duplication of setup code and fixtures.

Propose improvements:
- Better fixtures/factories/builders to make tests expressive and DRY.
- Helper utilities for common assertions and scenarios.
- Patterns for testing async, concurrent, or event-driven code.
- Where property-based or fuzz testing would add substantial value (complex parsing, algorithms, data transformations).

**Part F — Tooling and CI Integration**

Evaluate current tooling: test runners, coverage tools, mocking frameworks, data generators.

Recommend:
- Standardizing on a single test runner and assertion library where helpful.
- Adding coverage thresholds and useful reports.
- Using tagging/markers to select test subsets in CI.
- Which suites should run on PRs vs. main branch vs. nightly vs. pre-release.
- Gates (coverage minimums, failure policies).

**Part G — Phased Migration Plan**

Propose a 3-5 phase plan to get from the current test suite to the target state:
- Each phase has: focus areas, expected impact vs. effort, and success criteria.
- Identify quick wins (immediate) vs. larger refactors (coordinated effort).
- Call out risks or dependencies (e.g., production code needs refactoring to become testable).

**Part H — Observability**

- Logging: signal vs. noise, presence of structured/contextual logs.
- Metrics: key rates, latencies, errors, saturation.
- Tracing/correlation of requests across components.
- Suggest specific events, metrics, and spans to add.
- A minimal set of golden signals for each critical component.

*Reminder: READ-ONLY. Do not modify code. Report findings only.*

#### Sub-agent 7: Standards, Consistency, and Developer Experience

Consider how this codebase feels to a new engineer joining the team.

- **Evaluate**: Naming clarity and consistency. Directory/project layout and module boundaries. Adherence to language/framework conventions. Presence and quality of inline docs, comments, and higher-level docs.
- **Suggest**: Linters, formatters, and static-analysis rules that would catch common issues. Simple contribution guidelines that would prevent future divergence. Small structural changes that materially improve navigation and understanding.

*Reminder: READ-ONLY. Do not modify code. Report findings only.*

### Phase 3: External Libraries and APIs

Do not guess about third-party behavior. For key libraries/frameworks/APIs where behavior, guarantees, or limits are not obvious:

- Look up official documentation before forming conclusions.
- Verify that usage matches recommended patterns, lifecycle, and error-handling.
- Call out misuse, reliance on undocumented behavior, deprecated APIs, and fragile defaults.
- Note upgrade risks and suggest safer abstraction layers or usage patterns.

### Phase 4: Synthesis and Report

As the orchestrator, merge and de-duplicate findings from all sub-agents. Resolve conflicts or trade-offs between recommendations. Surface cross-cutting issues that span multiple areas. Produce the final report in the output format below.

## Output Format

Structure the final report with these sections:

### 1. High-Level Summary (10-30 lines)

Cover all of the following:
- System purpose and scope.
- Technology stack and key frameworks.
- Overall architectural health assessment.
- Main strengths (what the codebase does well).
- Main risks and weaknesses (what needs attention).
- Current state of test coverage and observability.
- Developer experience assessment.
- Strategic outlook: where this system is headed and what will break first at scale.

### 2. System Map

The bulleted system map from Phase 1 plus data/control flow description.

### 3. Top 10-15 High-Leverage Changes

Present as a numbered list. For each item provide:

- **Title**: Short, descriptive title.
- **Category**: architecture / bugs / security / performance / code-health / testing / DX
- **Impact**: high / medium / low (on risk, maintainability, or performance)
- **Effort**: S / M / L
- **Next Steps**: Concrete actions, in rough order.

### 4. Test Suite Recommendations

A dedicated section (not buried in general findings) covering:

**4a. Test Inventory** — Table or list mapping each test category (unit, integration, E2E, acceptance, non-functional) to the system components it covers, with a reliability/speed/coverage grade.

**4b. Target Testing Strategy** — The recommended test pyramid shape, responsibilities of each layer, and proposed directory/naming/tagging conventions.

**4c. Top 10 Tests to Add** — Numbered list of the highest-value missing tests, each with: type, scenario, where it lives, and why it matters.

**4d. Tests to Remove or Reclassify** — Low-value, redundant, or wrong-level tests that should be deleted, merged, or moved to a different layer.

**4e. Flakiness and Speed Fixes** — Concrete actions to make the suite faster and more deterministic, with target runtime budgets.

**4f. Test Design Improvements** — Fixture/factory patterns, assertion helpers, and structural changes to make tests easier to write and maintain.

**4g. Tooling and CI Recommendations** — Test runner, coverage, mocking, and CI pipeline changes.

**4h. Phased Migration Plan** — 3-5 phases to reach the target test architecture, with quick wins first.

### 5. Detailed Findings by Category

Organized by the sub-agent categories:
- Architecture and Design
- Code Health and Dead Code
- Bugs, Correctness, and Edge Cases
- Security
- Performance and Reliability
- Observability
- Standards, Consistency, and Developer Experience
- External Libraries and APIs

### 6. Non-Obvious Insights

- Surprising constraints, architectural bets, or "time bombs" that may not hurt now but will at scale or over time.
- Strategic refactors to plan over the next 3-6 months, including suggested sequencing.

### 7. Open Questions and Assumptions

- Assumptions made due to missing context.
- Questions that, if answered, would significantly change recommendations.

## Guiding Principles

- **Be candid, pragmatic, and specific.** Every finding must include a concrete example from the codebase (file path + line reference where possible).
- **Maximize long-term clarity, resilience, and efficiency** with the smallest realistic set of well-chosen changes.
- **Prefer many small, focused passes** over one massive, unfocused one.
- **Do not guess about third-party behavior.** Look up documentation when unsure.
- **For each bug or risk, describe a concrete failing scenario** — not just "this could be a problem."
- **Suggest realistic migration paths**, not just ideal end states.
- **Prioritize ruthlessly.** The top 10-15 changes should be the ones that matter most, not everything found.

**IMPORTANT DIRECTIVE (REPEATED): This is a READ-ONLY review. ABSOLUTELY DO NOT modify any existing code in any circumstance. Running existing tests and writing temporary test scripts to verify assumptions is permitted, but all such intermediate test scripts MUST be cleaned up (deleted) when done.**
