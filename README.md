# Jordan's Skills

⭐ **If this vault saves you time, drop a star. It helps others find it.**

A complete vault of Claude Code skills for serious builders — covering product development, AI-assisted workflows, trading systems, writing, debugging, and deployment.

These are the skills I use daily. They make Claude significantly more capable by giving it precise, repeatable instructions for complex workflows. Treat each skill as a specialized expert you can summon on demand.

---

## Credits & Attribution

This vault is a compilation. Full credit to the original creators — I've only built what's mine, and I've tried to be honest about the line.

| Source | What They Built | Skills in This Vault |
|--------|----------------|----------------------|
| **[ReScienceLab](https://github.com/ReScienceLab/opc-skills)** | OPC Skills — open plugin collection for Claude Code | `project-skills/` — twitter, reddit, producthunt, nanobanana, seo-geo, logo-creator, domain-hunter, banner-creator, requesthunt |
| **[Anthropic](https://github.com/anthropics/claude-code)** (Claude Code plugins) | Official Claude Code plugin marketplace | Superpowers framework, figma, frontend-design, feature-dev, ralph-loop, claude-md-management, code-review plugins |
| **[@agentic.james](https://www.tiktok.com/@agentic.james)** | 142 TikTok videos on Claude Code mastery and agentic workflows | `commands/other/agentic-james/` |
| **[@ariacodez](https://www.instagram.com/ariacodez/)** | 93 Instagram reels on AI tools, cybersecurity, and rapid dev | `commands/other/ariacodez/` |
| **[GSD](https://github.com/botingw/gsd)** | Get Shit Done — hierarchical project management for solo agentic dev | `commands/other/gsd/` |
| **Jordan Bee + Claude** | Built from scratch for a live quant trading system | `commands/quant/` (100+ commands), `ghostwriter/`, `solomon/`, core workflow skills |

**If I've missed a credit or misattributed anything, open an issue and I'll fix it immediately.**

---

---

## How Skills Work

Skills are invoked via the `Skill` tool inside Claude Code, or using the `/skill-name` slash command shorthand.

```
/ghostwriter path/to/document.md
/ship-it
/verify-plan
/gap-analysis "my trading risk system"
```

Place skills in `~/.claude/skills/` to make them globally available across all projects.

---

## Highlight Skills

The most powerful and most used skills in this vault.

---

### `/tap` — Turn Any Video Into Stored Expertise ⚡ Try This First

**One of the most unique skills in this vault. Highly recommended.**

Give it any YouTube, TikTok, or Instagram URL. It downloads the audio, transcribes it with Whisper, runs a deep expert analysis, and stores everything in your local knowledge vault — ready to query later.

What it produces from a single video:
- Full raw transcript stored and tagged
- Expert analysis with core concepts, key takeaways, technical details, and connections to existing knowledge
- A dense "expert summary" paragraph you can reference later without re-watching

Run 10 videos in parallel. Your vault compounds over time.

**Setup required:** `yt-dlp` + `whisper` + the memory MCP. See `tap/SKILL.md` for full setup.

**Use when:** You want to extract and keep knowledge from any video — tutorials, talks, podcasts, courses, short-form content.

```
/tap https://youtube.com/watch?v=...
/tap https://www.tiktok.com/@user/video/...
```

**To install:** Copy `tap/SKILL.md` to `~/.claude/commands/tap.md`

---

### `/ghostwriter` — Transform AI Writing Into Human Voice

**The most used skill in this vault.**

Takes any AI-generated document and rewrites it in a polished, professional human voice. Zero detectable AI patterns. Applies a 5-phase pipeline:

1. Context extraction — understands the document's purpose and audience
2. AI-pattern audit — removes 24 known AI writing tells (hedging, filler, em-dash abuse, etc.)
3. Voice profile application — matches tone, rhythm, and register to the target voice
4. Craft enhancement — tightens sentences, sharpens specificity, improves flow
5. Self-audit — verifies no AI patterns remain

**Use when:** Any document needs to sound like a professional human wrote it — emails, LinkedIn posts, client memos, proposals, docs.

```
/ghostwriter [text or file path]
/ghostwriter "Here's my draft..."
/ghostwriter docs/proposal.md
```

---

### `/verify-plan` — Production-Grade Plan Verification

Stress-tests any implementation plan to the standard: *after this passes, any remaining issues are subjective design choices, not bugs.*

Dispatches 4 parallel verification agents simultaneously:
- **Logic Auditor** — finds logical flaws, contradictions, impossible states
- **Security Reviewer** — identifies injection, auth gaps, data exposure
- **Race Condition Detector** — surfaces concurrency and timing bugs
- **Completeness Checker** — finds missing error paths, edge cases, gaps

Returns a structured go/no-go verdict with prioritized findings.

**Use when:** You've written an implementation plan and need to know if it's actually buildable before writing a single line of code.

```
/verify-plan
```

---

### `/ship-it` — Production Readiness Gate

One command before every deploy. Runs 4 parallel audits and returns a unified go/no-go verdict:

1. Security scan — OWASP top 10, secrets exposure, auth gaps
2. Code review — logic errors, anti-patterns, tech debt
3. Test verification — confirms tests pass with evidence
4. Gap check — compares against best-in-class for the domain

**Use when:** About to deploy, launch, or merge to main.

```
/ship-it
/ship-it "payment feature"
/ship-it --full
```

---

### `/gap-analysis` — Close the Gap to World-Class

Finds what separates your current state from best-in-class in any domain. Dispatches parallel research agents to benchmark against top performers, then returns a prioritized action plan sorted by impact.

Works for: code quality, tooling, trading systems, product, marketing, personal skills, ops.

**Use when:** You want to know what the top 1% does that you don't.

```
/gap-analysis "my CI/CD pipeline"
/gap-analysis "trading risk management"
/gap-analysis "SaaS onboarding flow"
```

---

### `/brainstorming` — Design Before You Build

Mandatory before any creative work. Guides you through intent, constraints, and design before a single line of code is written. Prevents the most common failure mode in AI-assisted development: building the wrong thing confidently.

Hard gate: **no code until design is approved.**

Workflow:
1. Explore project context
2. Ask clarifying questions one at a time
3. Propose 2-3 approaches with trade-offs
4. Present design and get approval
5. Save design doc to `docs/plans/`

**Use when:** Starting any new feature, component, or system.

```
/brainstorming
```

---

### `/solomon` — Cross-Domain Wisdom Engine

Query a wisdom vault built from AI/engineering, finance, theology, psychology, and geopolitics. Returns first-principles thinking, mental models, and frameworks — not surface-level advice.

4 modes:
- **Wisdom Query** — "What does Solomon say about X?"
- **Decision Review** — "Should I do X?" — structured analysis before you commit
- **Pattern Detection** — flags recurring mistakes across sessions
- **Proactive Challenge** — pushes back on weak reasoning

**Use when:** Facing a non-trivial decision, strategic question, or want a second opinion grounded in depth rather than vibes.

```
/solomon "Should I scale before profitability?"
/solomon "review my decision to..."
```

---

### `/launch-checklist` — Ship Products Like a Pro

Full product launch checklist that chains 4 specialized agents in parallel:

- `/ship-it` — technical readiness
- `/seo-geo` — SEO and AI search engine optimization
- `/gap-analysis` — launch readiness vs. best-in-class
- `/domain-hunter` — domain availability and pricing

Returns a unified checklist across technical, marketing, SEO, and go-to-market.

**Use when:** Preparing to publicly launch a product, SaaS, or major feature.

```
/launch-checklist
/launch-checklist "product name"
```

---

### `/systematic-debugging` — Root Cause First, Always

Enforces disciplined debugging. The iron law: **no fixes without root cause investigation first.** Symptom fixes are failure.

Follows a structured process:
1. Reproduce the bug reliably
2. Isolate variables
3. Trace to root cause
4. Fix the root, not the symptom
5. Verify fix doesn't break adjacent systems

**Use when:** Hitting any bug, test failure, or unexpected behavior — before proposing fixes.

```
/systematic-debugging
```

---

### `/dispatching-parallel-agents` — Run Independent Tasks Concurrently

When you have 2+ independent problems, investigating them one at a time is wasteful. This skill dispatches one specialized agent per problem domain, runs them concurrently, and synthesizes results.

**Use when:** Multiple failures, multiple research threads, or any situation with 2+ independent tasks.

```
/dispatching-parallel-agents
```

---

### `/verification-before-completion` — Evidence Before Claims

The iron law: **no completion claims without fresh verification evidence.** Stops you from claiming something works based on memory or assumption.

Requires actually running tests and capturing output before saying anything is "done", "fixed", or "passing".

**Use when:** About to claim work is complete, before committing, before creating PRs.

```
/verification-before-completion
```

---

### `/writing-plans` — Structured Implementation Plans

Turns a spec or set of requirements into a full, bite-sized implementation plan. Written for an engineer with zero context on your codebase — covers which files to touch, how to test, edge cases, and commit strategy.

Saves plans to `docs/plans/YYYY-MM-DD-<feature>.md`.

**Use when:** You have requirements and need a plan before touching code.

```
/writing-plans
```

---

### `/subagent-driven-development` — Parallel Plan Execution

Executes an implementation plan by dispatching one fresh subagent per task. Each task gets a two-stage review: spec compliance first, then code quality. Faster than sequential execution, higher quality than doing it yourself.

**Use when:** You have a written plan with mostly independent tasks and want to execute in the current session.

```
/subagent-driven-development
```

---

## Full Skill Index

### Core Development Skills (`skills/`)

| Skill | What It Does |
|-------|-------------|
| `tap` | Transcribe any video URL → deep analysis → stored in knowledge vault |
| `brainstorming` | Design-first workflow before any implementation |
| `writing-plans` | Structured implementation plans from requirements |
| `subagent-driven-development` | Parallel plan execution with per-task agents |
| `dispatching-parallel-agents` | Run independent investigations concurrently |
| `executing-plans` | Sequential batched execution across sessions |
| `systematic-debugging` | Root cause investigation before any fix |
| `verification-before-completion` | Evidence-required completion gate |
| `verify-plan` | 4-agent parallel plan stress test |
| `ship-it` | Production readiness gate before deploy |
| `gap-analysis` | Benchmark against best-in-class |
| `launch-checklist` | Full product launch workflow |
| `requesting-code-review` | Dispatch code review subagent |
| `receiving-code-review` | Handle feedback with technical rigor |
| `test-driven-development` | Write tests before implementation |
| `ghostwriter` | Transform AI writing into human voice |
| `solomon` | Cross-domain wisdom and decision review |
| `strategic-compact` | Context management across long sessions |
| `python-patterns` | Pythonic best practices and PEP 8 |
| `json-canvas` | Create and edit Obsidian Canvas files |
| `obsidian-markdown` | Obsidian-flavored markdown (wikilinks, callouts) |
| `obsidian-bases` | Obsidian Bases with views, filters, formulas |
| `obsidian-cli` | Vault operations via CLI |
| `defuddle` | Extract clean markdown from web pages |

### Additional Skills (`_skills_available/`)

| Skill | What It Does |
|-------|-------------|
| `backend-patterns` | Backend architecture and API patterns |
| `frontend-patterns` | Frontend component and state patterns |
| `golang-patterns` | Go idioms and best practices |
| `golang-testing` | Go testing patterns and table-driven tests |
| `postgres-patterns` | PostgreSQL query and schema patterns |
| `clickhouse-io` | ClickHouse analytics query patterns |
| `coding-standards` | Language-agnostic code quality standards |
| `security-review` | Security audit and vulnerability detection |
| `prd` | Product requirements document creation |
| `eval-harness` | LLM evaluation harness construction |
| `iterative-retrieval` | Progressive document retrieval patterns |
| `continuous-learning` | AI-assisted learning loop setup |
| `tdd-workflow` | Full TDD cycle with failing tests first |
| `terminal-control` | Terminal and shell automation patterns |
| `using-git-worktrees` | Isolated feature branches via git worktrees |
| `finishing-a-development-branch` | Branch completion and merge/PR options |
| `writing-skills` | Skill authoring and deployment |
| `verification-loop` | Continuous verification patterns |
| `ralph` | Ralph Loop self-improvement cycle |

### Quant Trading Commands (`commands/quant/`)

100+ specialized commands for trading system operations:

**Performance & Reporting**
`morning-report` · `evening-report` · `daily-performance` · `weekly-report` · `monthly-report` · `pnl-calculator` · `quick-stats` · `portfolio-summary` · `leaderboard`

**Strategy Management**
`best-performers` · `worst-performers` · `strategy-analyzer` · `strategy-compare` · `strategy-scorecard` · `strategy-enabler` · `active-strategies` · `bulk-scorecard` · `parameter-tuner`

**Risk & Execution**
`circuit-breaker` · `drawdown-monitor` · `kill-loser` · `stop-loss-manager` · `position-manager` · `position-sizer` · `kelly-calculator` · `var-calculator` · `max-position-checker` · `exposure-monitor`

**System & Infrastructure**
`health-check` · `system-snapshot` · `process-manager` · `vps-manager` · `deploy-vps` · `sync-local-vps` · `pco` · `git-manager` · `rollback-manager` · `config-validator`

**Market Intelligence**
`market-intel` · `momentum-scanner` · `regime-detector` · `fear-greed-tracker` · `whale-watcher` · `social-scanner` · `funding-monitor` · `order-flow-analyzer` · `l2-monitor`

**Analytics**
`trade-query` · `trade-timeline` · `trade-histogram` · `slippage-analyzer` · `execution-quality` · `entry-analyzer` · `exit-analyzer` · `pair-correlation` · `correlation-analyzer` · `sharpe-calculator`

**Utilities**
`db-query` · `db-explorer` · `log-parser` · `recent-errors` · `alert-router` · `imessage-sender` · `obsidian-checkpoint` · `data-export` · `fee-tracker` · `cost-report`

### Other Commands (`commands/other/`)

| Command | What It Does |
|---------|-------------|
| `build` | Full 6-layer architecture reasoning before any code |
| `verify` | General verification command |
| `plan` | Quick planning command |
| `eval` | LLM evaluation runner |
| `tdd` | TDD workflow shortcut |
| `code-review` | Code review command |
| `refactor-clean` | Clean refactor with safety checks |
| `checkpoint` | Save session state |
| `orchestrate` | Multi-agent orchestration |
| `learn` | Learning loop command |
| `e2e` | End-to-end test runner |
| `gsd` | Get Stuff Done project management system |

### Project Skills (`project-skills/`)

Skills with full API integrations, scripts, and reference data:

| Skill | What It Does |
|-------|-------------|
| `twitter` | Search tweets, users, threads, trends via twitterapi.io |
| `reddit` | Search posts, comments, subreddits via public API |
| `producthunt` | Get posts, topics, users via GraphQL API |
| `nanobanana` | AI image generation via Google Gemini |
| `logo-creator` | Logo design, iteration, SVG export |
| `banner-creator` | Banner and header image creation |
| `domain-hunter` | Domain search, pricing, registrar comparison |
| `seo-geo` | SEO + GEO (AI search engine optimization) |
| `requesthunt` | User demand research from Reddit, X, GitHub |

---

## Workflow Chains

These skills are designed to chain together:

**Feature Development**
```
/brainstorming → /writing-plans → /verify-plan → /subagent-driven-development → /ship-it
```

**Bug Fixing**
```
/systematic-debugging → test-driven-development → fix → /verification-before-completion
```

**Product Launch**
```
/gap-analysis → /ship-it → /seo-geo → /launch-checklist
```

**Content Creation**
```
draft → /ghostwriter → publish
```

---

## Installation

```bash
# Clone to your Claude skills directory
git clone https://github.com/thepono1/Jordan-s-Skills ~/.claude/skills

# Skills are immediately available in Claude Code
# Invoke with: /skill-name or via the Skill tool
```

---

## Structure

```
├── skills/              # Core skills (brainstorming, ghostwriter, verify-plan, etc.)
├── _skills_available/   # Additional skills (golang, postgres, backend, security, etc.)
├── commands/
│   ├── quant/           # 100+ trading system commands
│   └── other/           # General dev commands (build, verify, gsd, etc.)
└── project-skills/      # Skills with full API integrations (twitter, reddit, seo, etc.)
```

---

Built for Claude Code. Works with any Claude model.

---

If this vault made Claude more useful for you, hit the ⭐ star button at the top of the page. It takes two seconds and helps other builders find it.
