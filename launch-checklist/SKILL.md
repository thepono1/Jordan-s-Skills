---
name: launch-checklist
description: "Full product launch checklist combining technical readiness, marketing, SEO, and go-to-market. Chains ship-it + seo-geo + gap-analysis + domain-hunter into unified launch flow. Use when preparing to launch a product, SaaS, or feature publicly."
user_invocable: true
---

# /launch-checklist — Ship Products Like a Pro

Unified launch flow that combines technical readiness, SEO, marketing prep, and go-to-market into one checklist. Dispatches specialized agents in parallel.

## Usage

```
/launch-checklist                     # Full launch audit
/launch-checklist "product name"      # Named product
/launch-checklist --technical-only    # Skip marketing, just tech (only Track 1)
```

## Step 1: Gather Context

1. Ask (if not clear): "What are you launching? URL? Target audience?"
2. Read project configs (package.json, pyproject.toml, Dockerfile, etc.) to understand the stack
3. Identify: is this a new product, a feature launch, or an update?
4. Store answers as variables: `PRODUCT_NAME`, `PRODUCT_URL`, `PRODUCT_TYPE`, `TARGET_AUDIENCE`

## Step 2: Parallel Audit Dispatch

Launch **all tracks as Task tool calls in a single message** so they run in parallel.

### Track 1: Technical Readiness

Invoke the `/ship-it` skill flow inline — dispatch the same 4 sub-agents (security-reviewer, code-reviewer, test verification, infra check) as defined in `/ship-it`. Pass the file list from Step 1.

The ship-it flow returns a verdict: SHIP IT / CONDITIONAL SHIP / HOLD. Capture this as `TECH_VERDICT`.

### Track 2: SEO & Discoverability

```
Task(
  description="Launch SEO audit",
  subagent_type="general-purpose",
  prompt="""
Analyze [PRODUCT_URL] for search visibility. If no URL, analyze the project's HTML/templates.

Check each item and mark PASS / FAIL / MISSING:
1. Meta tags (title, description) present and descriptive
2. Open Graph tags (og:title, og:description, og:image)
3. Twitter Card tags (twitter:card, twitter:title, twitter:image)
4. robots.txt exists and allows crawling
5. sitemap.xml exists and is valid
6. JSON-LD structured data present
7. Canonical URLs set on all pages
8. Heading hierarchy correct (single H1, logical H2-H6)
9. Page speed assessment (check for large images, unminified JS/CSS)
10. Mobile responsive (viewport meta tag, no horizontal scroll)
11. AI search engine readiness (clear FAQ sections, structured content for LLM extraction)

Return in this exact format:
## SEO & Discoverability Audit
| # | Check | Status | Detail |
|---|-------|--------|--------|
[rows with PASS/FAIL/MISSING]
Score: [X]/11 passed
"""
)
```

### Track 3: Launch Marketing Prep

```
Task(
  description="Launch marketing prep",
  subagent_type="general-purpose",
  prompt="""
Create a launch marketing checklist for [PRODUCT_NAME] ([PRODUCT_TYPE] targeting [TARGET_AUDIENCE]).

Search the web for best practices on launching this type of product in 2025-2026. Limit research to 5 minutes / top 5 sources.

Check each item and mark READY / NOT READY / N/A:
1. Landing page: hero section, clear CTA, social proof, pricing
2. Launch channels: Product Hunt, Hacker News, Reddit, X/Twitter, Indie Hackers — which are relevant?
3. Email list / waitlist: capture mechanism exists?
4. Analytics: PostHog, Plausible, or GA4 configured?
5. Error tracking: Sentry or equivalent configured?
6. Customer support: email, chat widget, Discord, or GitHub Issues?
7. Legal: Terms of Service exists?
8. Legal: Privacy Policy exists?
9. Legal: Cookie consent (required if EU users)?
10. Social media: profiles created and linked from product?

Return in this exact format:
## Marketing Readiness
| # | Item | Status | Detail / Recommendation |
|---|------|--------|------------------------|
[rows with READY/NOT READY/N/A]
Score: [X]/10 ready
"""
)
```

### Track 4: Competitive Positioning

```
Task(
  description="Launch competitive analysis",
  subagent_type="general-purpose",
  prompt="""
Search the web for competitors to: [PRODUCT_NAME] — [one-line product description].

Find the top 3-5 competitors (limit scope — don't research more than 5). For each:
- Name and URL
- Pricing model
- Key strength (what they do best)
- Key weakness (what users complain about — check Reddit, X, G2 reviews)
- How [PRODUCT_NAME] differentiates

Return in this exact format:
## Competitive Landscape
| Competitor | URL | Pricing | Strength | Weakness | Our Advantage |
|------------|-----|---------|----------|----------|---------------|
[rows — max 5 competitors]

Bottom line: [one sentence on competitive positioning]
"""
)
```

## Step 3: Synthesize

Merge all tracks into one unified checklist. Calculate the readiness score:

**Readiness Score formula:**
- Technical: SHIP IT = 3pts, CONDITIONAL SHIP = 1pt, HOLD = 0pts (out of 3)
- SEO: [passed checks] / 11 * 3 (out of 3)
- Marketing: [ready items] / 10 * 2 (out of 2)
- Legal: [ready items] / 3 * 2 (out of 2)
- **Total: X / 10**

Output:

```
## Launch Checklist: [Product Name]
**Date**: [today]
**Readiness Score**: [X/10]

### Technical [TECH_VERDICT]
- [ ] Security audit passed (0 critical, 0 high)
- [ ] Tests passing with meaningful coverage
- [ ] Error tracking configured (Sentry)
- [ ] Logging and monitoring active
- [ ] SSL/HTTPS configured
- [ ] Backups configured
- [ ] Health check endpoint exists
- [ ] Rate limiting on API endpoints

### SEO & Discoverability [X/11 passed]
- [ ] Meta tags and Open Graph
- [ ] Sitemap.xml and robots.txt
- [ ] JSON-LD structured data
- [ ] Page speed acceptable (<3s LCP)
- [ ] Mobile responsive
- [ ] AI search engine optimized

### Marketing [X/10 ready]
- [ ] Landing page with clear CTA
- [ ] Analytics configured
- [ ] Launch post drafted for [relevant channels]
- [ ] Social media profiles linked
- [ ] Email capture / waitlist

### Legal [X/3 ready]
- [ ] Terms of Service
- [ ] Privacy Policy
- [ ] Cookie consent (if EU users)

### Competitive Position
[matrix table from Track 4]

### Verdict
[see decision logic below]

### Recommended Launch Order
1. [highest-impact action first]
2. [second action]
3. ...
```

**Verdict decision logic:**

| Score | Verdict |
|-------|---------|
| 8-10 | **READY TO LAUNCH** — Go ship it. |
| 5-7 | **NEEDS WORK** — Fix [list top 3 blockers], then launch. |
| 0-4 | **NOT READY** — Major gaps in [categories]. Address these first. |

Override: If Technical verdict is HOLD, overall verdict is always **NOT READY** regardless of score.

## Rules

- Don't let perfect be the enemy of shipped. Flag what matters, skip what doesn't.
- For solo/indie products: Legal is MEDIUM priority, not CRITICAL (unless handling payments/health data).
- For products handling money: Security is non-negotiable. Everything else can wait.
- Always recommend a launch channel strategy based on the product type.
- Limit competitive research to 5 competitors max — avoid analysis paralysis.
- If `--technical-only` flag: skip Tracks 2-4, only run Track 1.
