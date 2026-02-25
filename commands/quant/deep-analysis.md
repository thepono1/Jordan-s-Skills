---
name: quant:deep-analysis
description: Sub-agent orchestrated deep analysis of trading system (demonstrates agentic.james pattern)
---

<objective>
Perform comprehensive analysis of trading performance using sub-agent orchestration pattern.
This skill demonstrates the @agentic.james workflow: main agent orchestrates, sub-agents execute, main agent audits.
</objective>

<architecture>
```
MAIN AGENT (you)
├── Spawns: strategy-analyzer sub-agent
├── Spawns: trade-quality sub-agent
├── Spawns: risk-audit sub-agent
├── Audits each result
├── Reprompts if incomplete
└── Synthesizes final report
```
</architecture>

<process>

## Phase 1: Spawn Sub-Agents in Parallel

Use the Task tool to spawn THREE sub-agents simultaneously:

### Sub-Agent 1: Strategy Performance Analyzer
```
Prompt for Task tool:
"Analyze strategy performance from the trading database at ~/Developer/quant_master/quant_v4/efg_paper_trading/trading.db

Instructions:
1. Query all trades grouped by strategy_id
2. Calculate per-strategy: win rate, avg profit, max drawdown, sharpe ratio
3. Identify top 3 performers and bottom 3 performers
4. Return structured JSON with all metrics

Output format:
{
  "strategies": [...],
  "top_performers": [...],
  "underperformers": [...],
  "total_strategies_analyzed": N
}

Do not stop until you have analyzed ALL strategies in the database."
```

### Sub-Agent 2: Trade Quality Auditor
```
Prompt for Task tool:
"Audit trade execution quality from ~/Developer/quant_master/quant_v4/efg_paper_trading/trading.db

Instructions:
1. Calculate slippage (expected vs actual fill price)
2. Measure time-to-fill for each trade
3. Identify any failed or partial fills
4. Check for trades during high-spread periods
5. Return quality score and issues found

Output format:
{
  "avg_slippage_bps": N,
  "avg_fill_time_ms": N,
  "failed_trades": [...],
  "quality_score": "A/B/C/D/F",
  "recommendations": [...]
}

Analyze the last 100 trades minimum."
```

### Sub-Agent 3: Risk Metrics Calculator
```
Prompt for Task tool:
"Calculate risk metrics from ~/Developer/quant_master/quant_v4/efg_paper_trading/trading.db

Instructions:
1. Calculate portfolio VaR (95% and 99%)
2. Measure max drawdown and recovery time
3. Check position sizing compliance
4. Verify stop-loss adherence
5. Calculate risk-adjusted returns

Output format:
{
  "var_95": N,
  "var_99": N,
  "max_drawdown_pct": N,
  "recovery_days": N,
  "position_size_violations": [...],
  "stop_loss_breaches": [...],
  "sharpe_ratio": N
}

This is critical risk data - be thorough."
```

## Phase 2: Audit Sub-Agent Results

After each sub-agent returns, verify:

1. **Completeness Check:**
   - Did strategy analyzer cover ALL strategies? If not, reprompt.
   - Did trade auditor analyze 100+ trades? If not, reprompt.
   - Did risk calculator provide all metrics? If not, reprompt.

2. **Quality Check:**
   - Are numbers reasonable (no NaN, no impossible values)?
   - Do totals add up correctly?
   - Are there any error messages in the output?

3. **Reprompt Pattern (if incomplete):**
   ```
   "Your previous analysis was incomplete. You only covered [X] items but there are [Y] total.
   Continue from where you left off and complete the remaining [Y-X] items.
   Return the COMPLETE results this time."
   ```

## Phase 3: Synthesize Final Report

Combine all sub-agent outputs into executive summary:

```markdown
# Deep Analysis Report
Generated: [timestamp]

## Executive Summary
- Total Strategies Analyzed: [N]
- Overall Win Rate: [X%]
- Portfolio Health: [GOOD/WARNING/CRITICAL]

## Strategy Performance
### Top Performers
1. [strategy] - [metrics]
2. [strategy] - [metrics]
3. [strategy] - [metrics]

### Underperformers (Consider Disabling)
1. [strategy] - [metrics]

## Trade Execution Quality
- Quality Score: [A-F]
- Average Slippage: [X] bps
- Issues Found: [list]

## Risk Assessment
- Current Drawdown: [X%]
- VaR (95%): $[X]
- Position Sizing: [COMPLIANT/VIOLATIONS]
- Stop-Loss Adherence: [X%]

## Recommendations
1. [actionable recommendation]
2. [actionable recommendation]
3. [actionable recommendation]
```

</process>

<key_pattern>
THE RECURSIVE CALLING PATTERN (from @agentic.james):

When spawning sub-agents, always include:
"Continue until the task is FULLY complete. Do not return partial results."

When auditing, always check:
- Did we get everything we asked for?
- If not, spawn the sub-agent again with specific instructions to complete the missing parts.

This is how you run long-horizon tasks without the main agent timing out.
</key_pattern>

<success_criteria>
- [ ] All 3 sub-agents spawned in parallel
- [ ] Each sub-agent result audited for completeness
- [ ] Any incomplete results triggered a reprompt
- [ ] Final synthesis combines all data
- [ ] Actionable recommendations provided
</success_criteria>
