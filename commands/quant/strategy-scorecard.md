---
name: quant:strategy-scorecard
description: Generate a go/no-go scorecard before enabling a strategy
---

<objective>
Evaluate a strategy against key criteria and produce a clear GO/NO-GO recommendation.
This prevents enabling underperforming or risky strategies.
</objective>

<parameters>
Ask user for: strategy_id (or "all" to score all strategies)
</parameters>

<process>

## Step 1: Gather Strategy Data

Query the trading database for the specified strategy:

```bash
sqlite3 ~/Developer/quant_master/quant_v4/efg_paper_trading/state/trading.db "
SELECT
    strategy_id,
    COUNT(*) as total_trades,
    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
    SUM(CASE WHEN pnl <= 0 THEN 1 ELSE 0 END) as losses,
    ROUND(AVG(pnl), 4) as avg_pnl,
    ROUND(SUM(pnl), 4) as total_pnl,
    ROUND(MIN(pnl), 4) as worst_trade,
    ROUND(MAX(pnl), 4) as best_trade
FROM trades
WHERE strategy_id = '[STRATEGY_ID]'
GROUP BY strategy_id
"
```

## Step 2: Calculate Scorecard Metrics

For each metric, assign a score (0-2):

### Win Rate Score
- >= 50% → 2 points (STRONG)
- 35-49% → 1 point (MARGINAL)
- < 35% → 0 points (WEAK)

### Profit Factor Score (wins/losses dollar ratio)
- >= 1.5 → 2 points (STRONG)
- 1.0-1.49 → 1 point (MARGINAL)
- < 1.0 → 0 points (WEAK)

### Sample Size Score
- >= 30 trades → 2 points (SUFFICIENT)
- 15-29 trades → 1 point (LIMITED)
- < 15 trades → 0 points (INSUFFICIENT)

### Risk/Reward Score (best trade / |worst trade|)
- >= 2.0 → 2 points (FAVORABLE)
- 1.0-1.99 → 1 point (NEUTRAL)
- < 1.0 → 0 points (UNFAVORABLE)

### Consistency Score (no losing streaks > 5)
- Max streak <= 3 → 2 points
- Max streak 4-5 → 1 point
- Max streak > 5 → 0 points

## Step 3: Generate Scorecard

```
╔═══════════════════════════════════════════════════╗
║          STRATEGY SCORECARD                       ║
║          [strategy_id]                            ║
╠═══════════════════════════════════════════════════╣
║ METRIC              │ VALUE      │ SCORE │ GRADE ║
╠═════════════════════╪════════════╪═══════╪═══════╣
║ Win Rate            │ XX.X%      │  X/2  │ [●○○] ║
║ Profit Factor       │ X.XX       │  X/2  │ [●○○] ║
║ Sample Size         │ XX trades  │  X/2  │ [●○○] ║
║ Risk/Reward         │ X.XX       │  X/2  │ [●○○] ║
║ Consistency         │ X streak   │  X/2  │ [●○○] ║
╠═════════════════════╪════════════╪═══════╧═══════╣
║ TOTAL SCORE         │            │    X/10       ║
╠═══════════════════════════════════════════════════╣
║ RECOMMENDATION:                                   ║
║                                                   ║
║   8-10: ✅ GO - Enable with full allocation      ║
║   5-7:  ⚠️  CAUTION - Enable with reduced size   ║
║   0-4:  ❌ NO-GO - Do not enable                 ║
║                                                   ║
║   >>> [RECOMMENDATION HERE] <<<                   ║
╚═══════════════════════════════════════════════════╝
```

## Step 4: Provide Actionable Insight

If GO:
- Suggest position size based on score
- Note any weak areas to monitor

If CAUTION:
- Specify which metrics are dragging score down
- Suggest what would improve the score

If NO-GO:
- Explain why strategy fails
- Suggest: more backtesting, parameter tuning, or discard

</process>

<success_criteria>
- [ ] Strategy data retrieved from database
- [ ] All 5 metrics calculated
- [ ] Scorecard formatted clearly
- [ ] Clear GO/CAUTION/NO-GO recommendation
- [ ] Actionable next steps provided
</success_criteria>
