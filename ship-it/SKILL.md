---
name: ship-it
description: "Production-readiness gate. Chains security scan + code review + test verification + gap check before shipping. Use when about to deploy, launch, or ship a product/feature to production. Combines security-reviewer, code-reviewer, verification-before-completion, and gap-analysis into one command."
user_invocable: true
---

# /ship-it — Production Readiness Gate

One command to verify a project/feature is production-ready. Chains multiple specialized agents in parallel, then synthesizes a go/no-go verdict.

## Usage

```
/ship-it                    # Check current project
/ship-it "feature name"     # Check specific feature
/ship-it --full             # Full audit (slower, more thorough)
```

## Step 1: Scope

1. Identify what's being shipped: the full project, a specific feature, or recent changes
2. If recent changes: `git diff main...HEAD` or `git diff --cached` to identify the blast radius
3. List all files that will be part of the ship
4. If no changes found (empty diff, no staged files), tell user: "Nothing to ship — no changes detected." and stop.

## Step 2: Parallel Audit (4 agents)

Launch **4 Task tool calls in a single message** so they run in parallel. Each agent MUST return findings in this exact format:

```
## [Agent Name] Findings

| # | Severity | Finding | Detail |
|---|----------|---------|--------|
| 1 | CRITICAL | [short title] | [explanation + file:line if applicable] |
| 2 | HIGH | ... | ... |

Summary: [N] critical, [N] high, [N] medium
```

### Agent 1: Security Scanner

```
Task(
  description="Ship-it security scan",
  subagent_type="security-reviewer",
  prompt="""
Review these files for security vulnerabilities: [LIST FILES FROM STEP 1]

Focus on:
- Hardcoded secrets, API keys, tokens
- SQL injection, XSS, CSRF
- OWASP Top 10
- Unsafe deserialization
- Missing input validation at system boundaries
- Missing rate limiting on endpoints
- Error messages that leak internal state

Return findings in this exact format:
## Security Scanner Findings
| # | Severity | Finding | Detail |
|---|----------|---------|--------|
[rows]
Summary: [N] critical, [N] high, [N] medium
"""
)
```

### Agent 2: Code Quality

```
Task(
  description="Ship-it code review",
  subagent_type="code-reviewer",
  prompt="""
Review these files for production readiness: [LIST FILES FROM STEP 1]

Check for:
- Error handling: are all failure paths covered?
- Logging: is there enough to debug production issues?
- Configuration: are all settings externalized (not hardcoded)?
- Dependencies: any deprecated or vulnerable packages?
- Performance: any obvious N+1 queries, missing indexes, unbounded loops?
- Concurrency: any race conditions or shared mutable state?

Return findings in this exact format:
## Code Quality Findings
| # | Severity | Finding | Detail |
|---|----------|---------|--------|
[rows]
Summary: [N] critical, [N] high, [N] medium
"""
)
```

### Agent 3: Test Verification

```
Task(
  description="Ship-it test check",
  subagent_type="general-purpose",
  prompt="""
Check test coverage and quality for this project at [PROJECT ROOT]:

1. Find all test files (glob for *test*, *spec*, test_*)
2. Run the test suite if a test command exists (pytest, npm test, etc.)
3. Check for:
   - Do critical paths have tests?
   - Are there integration tests, not just unit tests?
   - Do tests actually assert behavior (not just "runs without error")?
   - Are there tests for error cases, not just happy paths?

Edge cases:
- If NO test files found: return CRITICAL finding "No tests exist"
- If tests exist but test runner fails to start: return HIGH finding with error output
- If tests run but some fail: return HIGH finding listing failed tests

Return findings in this exact format:
## Test Verification Findings
| # | Severity | Finding | Detail |
|---|----------|---------|--------|
[rows]
Test count: [N] | Passing: [N] | Failing: [N]
Summary: [N] critical, [N] high, [N] medium
"""
)
```

### Agent 4: Infra & Config Check

```
Task(
  description="Ship-it infra check",
  subagent_type="general-purpose",
  prompt="""
Check infrastructure readiness for project at [PROJECT ROOT]:

1. Verify environment configs exist (env vars, config files)
2. Check for .env files that shouldn't be committed (check .gitignore)
3. Verify Dockerfile / docker-compose if containerized
4. Check CI/CD config exists and is valid
5. Verify database migrations are up to date
6. Check for health check endpoints
7. Verify logging/monitoring is configured

Edge cases:
- If no CI/CD config found: return MEDIUM finding for solo projects, HIGH for team projects (check git log --format='%ae' | sort -u | wc -l to determine team size)
- If .env file is tracked by git: return CRITICAL finding

Return findings in this exact format:
## Infra & Config Findings
| # | Severity | Finding | Detail |
|---|----------|---------|--------|
[rows]
Summary: [N] critical, [N] high, [N] medium
"""
)
```

## Step 3: Synthesize

After all 4 agents return:

1. **Merge and deduplicate** findings across agents — if two agents flag the same issue (e.g., security says "no input validation" and code quality says "missing validation on endpoint X"), keep the more detailed one
2. **Rank by severity**: CRITICAL → HIGH → MEDIUM
3. **Count totals** across all agents

## Step 4: Verdict

Output this report:

```
## Ship-It Report
**Project**: [name]
**Scope**: [what was checked — file count, feature name, or "full project"]
**Agents**: 4 | **Total findings**: [N]

### CRITICAL (blocks ship)
| # | Finding | Category | Detail |
[findings or "None — all clear"]

### HIGH (should fix before ship)
| # | Finding | Category | Detail |
[findings or "None"]

### MEDIUM (fix soon after ship)
| # | Finding | Category | Detail |
[findings or "None"]

### Verdict
[see decision logic below]
```

**Verdict decision logic** (exhaustive):

| Critical | High | Medium | Verdict |
|----------|------|--------|---------|
| 0 | 0 | any | **SHIP IT** — Production-ready. Fix MEDIUM items post-launch. |
| 0 | 1-2 | any | **CONDITIONAL SHIP** — No blockers, but [N] high-severity findings. Ship if deadline demands it, but schedule fixes this week. |
| 0 | 3+ | any | **HOLD** — Too many high-severity findings. Fix these first — they will cause problems under real load. |
| 1+ | any | any | **HOLD** — [N] critical findings must be resolved. These will break or create vulnerabilities in production. |

## Rules

- CRITICAL = will break or create security vulnerability in production
- HIGH = will cause problems under real-world conditions
- MEDIUM = should be fixed but won't cause immediate harm
- Be honest. Don't inflate findings to seem thorough. Don't minimize to seem positive.
- If the project has no tests, that's automatically a HIGH finding.
- If there's no CI/CD, that's a MEDIUM finding for solo projects, HIGH for team projects.
- MEDIUM-only findings never block a ship. Shipping > perfection.
