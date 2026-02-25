---
name: quant:market-intel
description: Comprehensive market intelligence using sub-agents and browser automation
---

<objective>
Gather comprehensive market intelligence from multiple sources using the @agentic.james
sub-agent orchestration pattern combined with Playwright browser automation.
</objective>

<architecture>
```
MAIN AGENT (you - the orchestrator)
│
├── Sub-Agent 1: Fear & Greed Scraper (Playwright)
│   └── Scrapes alternative.me for current sentiment
│
├── Sub-Agent 2: Database Analyzer (Bash)
│   └── Queries local trading database for recent performance
│
├── Sub-Agent 3: Position Checker (Bash)
│   └── Gets current open positions and exposure
│
├── [All 3 run in PARALLEL]
│
├── AUDIT: Verify each sub-agent returned complete data
│   └── Reprompt any incomplete results
│
└── SYNTHESIZE: Combine into actionable intelligence report
```
</architecture>

<process>

## Phase 1: Spawn Sub-Agents in Parallel

Use Task tool to spawn THREE sub-agents simultaneously:

### Sub-Agent 1: Fear & Greed (Browser)
```
Prompt:
"Use Playwright to navigate to https://alternative.me/crypto/fear-and-greed-index/
and extract:
1. Current Fear & Greed value
2. Yesterday's value
3. Last week's value
4. Last month's value

Return as JSON:
{
  'current': {'value': X, 'classification': '...'},
  'yesterday': {'value': X, 'classification': '...'},
  'last_week': {'value': X, 'classification': '...'},
  'last_month': {'value': X, 'classification': '...'},
  'trend': 'IMPROVING' | 'STABLE' | 'DETERIORATING'
}

Close browser when done."
```

### Sub-Agent 2: Performance (Bash)
```
Prompt:
"Query ~/Developer/quant_master/quant_v4/efg_paper_trading/state/trading.db

Calculate for last 7 days:
- Total trades
- Win rate
- Total PnL
- Best performing strategy
- Worst performing strategy

Return as JSON."
```

### Sub-Agent 3: Exposure (Bash)
```
Prompt:
"Query ~/Developer/quant_master/quant_v4/efg_paper_trading/state/trading.db

Get:
- Count of open positions
- Total exposure (sum of position values)
- Breakdown by symbol
- Breakdown by strategy

Return as JSON."
```

## Phase 2: Audit Results

For each sub-agent result, verify:
- Fear & Greed: Has all 4 timeframes?
- Performance: Has trades, win rate, PnL?
- Exposure: Has position count and values?

Reprompt any incomplete results.

## Phase 3: Generate Intelligence Report

```
╔══════════════════════════════════════════════════════════════╗
║                    MARKET INTELLIGENCE                       ║
║                    [timestamp]                               ║
╠══════════════════════════════════════════════════════════════╣
║ MARKET SENTIMENT                                             ║
╠══════════════════════════════════════════════════════════════╣
║ Fear & Greed Index: [XX] - [CLASSIFICATION]                  ║
║ Trend: [↑ IMPROVING / → STABLE / ↓ DETERIORATING]           ║
║                                                              ║
║ Timeline:                                                    ║
║   Now:        [XX] [████████░░] [CLASS]                     ║
║   Yesterday:  [XX] [████████░░] [CLASS]                     ║
║   Last Week:  [XX] [████████░░] [CLASS]                     ║
║   Last Month: [XX] [████████░░] [CLASS]                     ║
╠══════════════════════════════════════════════════════════════╣
║ YOUR PERFORMANCE (7d)                                        ║
╠══════════════════════════════════════════════════════════════╣
║ Trades: [X]  |  Win Rate: [XX%]  |  PnL: [$XX.XX]           ║
║ Best:  [strategy_name] (+$XX.XX)                             ║
║ Worst: [strategy_name] (-$XX.XX)                             ║
╠══════════════════════════════════════════════════════════════╣
║ CURRENT EXPOSURE                                             ║
╠══════════════════════════════════════════════════════════════╣
║ Open Positions: [X]                                          ║
║ Total Exposure: $[XXX.XX]                                    ║
║ By Symbol: ETH [XX%] | BTC [XX%]                            ║
╠══════════════════════════════════════════════════════════════╣
║ RECOMMENDATION                                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ [Based on sentiment + performance + exposure:]               ║
║                                                              ║
║ IF Fear & Greed < 25 AND performance positive:              ║
║   → OPPORTUNITY: Increase position size (fear = buying opp) ║
║                                                              ║
║ IF Fear & Greed > 75 AND high exposure:                     ║
║   → CAUTION: Consider taking profits (greed = correction)   ║
║                                                              ║
║ IF performance negative AND Fear & Greed declining:         ║
║   → DEFENSIVE: Reduce exposure, tighten stops               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

</process>

<the_agentic_james_pattern>
This skill demonstrates the complete pattern:

1. ORCHESTRATION: Main agent coordinates, doesn't do the work
2. PARALLELIZATION: Multiple sub-agents run simultaneously
3. SPECIALIZATION: Each sub-agent has one job
4. AUDIT LOOP: Verify completeness, reprompt if needed
5. SYNTHESIS: Combine results into actionable output

This is how you build workflows that run for hours without timing out.
</the_agentic_james_pattern>

<success_criteria>
- [ ] All 3 sub-agents spawned in parallel
- [ ] Fear & Greed data scraped from web
- [ ] Performance data queried from database
- [ ] Exposure data queried from database
- [ ] All results audited for completeness
- [ ] Intelligence report synthesized
- [ ] Clear recommendation provided
</success_criteria>
