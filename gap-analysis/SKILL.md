---
name: gap-analysis
description: "Find the gap between current state and world-class in any domain. Dispatches parallel research agents, compares against best-in-class, outputs prioritized action plan. Use when user wants to close gaps, level up, benchmark, or compare their setup to top performers."
user_invocable: true
---

# /gap-analysis — Close the Gap to World-Class

Find what you have, what the best have, and the Pareto-optimal path to close the delta. Works for any domain: tooling, code quality, trading systems, product development, personal skills, business operations.

## Usage

```
/gap-analysis <domain>
/gap-analysis "my CI/CD pipeline"
/gap-analysis "trading risk management"
/gap-analysis "product launch readiness"
```

If no domain is specified, ask the user what they want to gap-analyze.

## Step 0: Scope the Domain

1. Parse the user's domain from the argument or conversation context
2. If ambiguous, ask ONE clarifying question: "What specific area? [options]"
3. Define the boundary — what's IN scope and what's OUT

## Step 1: Audit Current State (Internal)

Before any external research, map what exists NOW. Use available tools:

**For code/tooling domains:**
- Read CLAUDE.md, project configs, package.json, requirements.txt, Makefile, CI configs
- Glob for relevant config files (.eslintrc, pytest.ini, Dockerfile, terraform/, .github/workflows/)
- Check what skills, hooks, MCPs, and agents are already configured
- Read `.claude/settings.json`, `.claude/skills/`, `.claude/commands/`

**For knowledge/process domains:**
- Search memory vault for related decisions and observations
- Check `.planning/` for existing plans and references
- Query knowledge engine if available

**For trading/quant domains:**
- Read SHARED_STATE.json, exchange configs, risk engine settings
- Check active strategies, circuit breakers, position sizing

Output a structured inventory:
```
### Current State Inventory
| Category | What Exists | Maturity (1-5) |
|----------|-------------|----------------|
```

## Step 2: Research World-Class (External)

Dispatch **3 parallel research agents** using the Task tool:

### Agent 1: Best-in-Class Benchmark (subagent_type: "general-purpose")
```
Search the web for what the best companies and developers use for [DOMAIN] in 2025-2026.
Focus on: Stripe, Vercel, Linear, Cloudflare, top indie hackers, and leaders in [DOMAIN].
Return a structured list:
| Tool/Practice | Who Uses It | Why It's Best-in-Class | URL |
Be specific — names, versions, configurations, not vague advice.
```

### Agent 2: Community Wisdom (subagent_type: "general-purpose")
```
Search GitHub, Reddit, Hacker News, and dev blogs for the most recommended tools and
practices for [DOMAIN]. Look for:
- "awesome-[domain]" repos with high stars
- Reddit threads: "what do you use for [domain]?"
- Recent blog posts from practitioners (not vendors)
Return: tool name, GitHub URL, star count, why people recommend it.
```

### Agent 3: Anti-Patterns & Pitfalls (subagent_type: "general-purpose")
```
Search for common mistakes, anti-patterns, and pitfalls in [DOMAIN].
What do people get wrong? What do they skip? What causes production incidents?
Focus on postmortems, "lessons learned" posts, and "I wish I knew" threads.
Return structured findings:
| Anti-Pattern | Consequence | How to Avoid |
```

## Step 3: Identify Gaps

Compare Step 1 (current) against Step 2 (world-class). For each gap:

```
### Gap Analysis Matrix
| # | Gap | Current State | World-Class State | Impact (1-10) | Effort (1-10) | Priority |
|---|-----|--------------|-------------------|---------------|---------------|----------|
```

**Scoring rules:**
- **Impact**: How much does closing this gap improve outcomes? (10 = game-changing)
- **Effort**: How hard is it to close? (1 = quick win, 10 = major project)
- **Priority**: Impact / Effort ratio. Higher = do first.

**Classification:**
- **Quick Wins** (Impact >= 7, Effort <= 3): Do TODAY
- **Strategic Investments** (Impact >= 7, Effort >= 7): Plan and schedule
- **Nice-to-Have** (Impact <= 4): Backlog or skip
- **Traps** (Impact <= 3, Effort >= 7): DO NOT DO — effort exceeds value

## Step 4: Build the Action Plan

Sort gaps by Priority (descending). Output:

```
## Action Plan: [DOMAIN]

### Quick Wins (do this week)
1. [Gap] — [specific action] — [expected outcome]
2. ...

### Strategic Investments (plan and schedule)
1. [Gap] — [approach] — [timeline estimate]
2. ...

### Already Strong (maintain)
- [thing that's already world-class]

### Consciously Skipping (not worth the effort)
- [thing with bad impact/effort ratio] — [why]
```

## Step 5: Generate Artifacts (Optional)

If the gap analysis reveals tool/skill gaps in the Claude Code setup:

- **Missing skills**: Draft SKILL.md files for recommended skills
- **Missing MCPs**: Provide install commands
- **Missing hooks**: Provide hook configurations
- **Missing CI steps**: Provide GitHub Actions YAML

Ask: "Want me to implement the Quick Wins now?"

## Rules

- **Pareto principle**: 20% of changes drive 80% of improvement. Always find the 20%.
- **No tool hoarding**: More tools != better. Only recommend tools that solve REAL gaps.
- **Specificity over generality**: "Install Semgrep and add to pre-commit" beats "add security scanning."
- **Current state is honest**: Don't inflate maturity scores. A 2 is a 2.
- **World-class is contextualized**: Solo dev world-class != Fortune 500 world-class. Match the user's scale.
- **Evidence over opinion**: Link to sources, star counts, and adoption data. No "I think you should."
- **Store findings**: After analysis, offer to store key insights in memory vault for future reference.
