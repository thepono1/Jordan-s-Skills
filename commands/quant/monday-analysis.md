---
name: quant:monday-analysis
description: Analyze weekend trading data and rank pairs by performance
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Task
---

<objective>
Comprehensive Monday morning analysis of weekend trading. Query all databases, rank pairs by performance, identify winners/losers, and update Obsidian with recommendations.
</objective>

<process>

## 1. Query Hybrid Trader Results

```bash
cd ~/Developer/quant_master/quant_v4/efg_paper_trading

echo "=== HYBRID TRADER WEEKEND RESULTS ==="
sqlite3 -header -column state/hybrid_trader.db "
SELECT
  symbol,
  COUNT(*) as trades,
  SUM(CASE WHEN net_pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(100.0 * SUM(CASE WHEN net_pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  ROUND(SUM(net_pnl), 2) as total_pnl,
  ROUND(AVG(net_pnl), 4) as avg_pnl,
  ROUND(MAX(highest_price / entry_price - 1) * 100, 1) as max_gain_pct
FROM trades
WHERE datetime(exit_time) > datetime('now', '-3 days')
GROUP BY symbol
ORDER BY total_pnl DESC
"
```

## 2. Query ProvenTrader Results

```bash
echo "=== PROVEN TRADER V2 WEEKEND RESULTS ==="
sqlite3 -header -column state/proven_trader_v2.db "
SELECT
  symbol,
  COUNT(*) as trades,
  SUM(CASE WHEN net_pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(100.0 * SUM(CASE WHEN net_pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  ROUND(SUM(net_pnl), 2) as total_pnl,
  regime as dominant_regime
FROM trades
WHERE datetime(exit_time) > datetime('now', '-3 days')
GROUP BY symbol
ORDER BY total_pnl DESC
"
```

## 3. Identify Winners and Losers

Create a ranking:

**WINNERS (keep/increase capital):**
- Positive PnL
- Win rate > 40%
- Multiple trades (statistically significant)

**LOSERS (disable/reduce capital):**
- Negative PnL
- Win rate < 30%
- Consistent losses

**INCONCLUSIVE (need more data):**
- Less than 3 trades
- Break-even

## 4. Generate Recommendations

Based on results, recommend:
1. Which pairs to keep trading
2. Which pairs to disable
3. Capital reallocation suggestions
4. Parameter adjustments (BB width, RSI threshold)

## 5. Update Obsidian

Update `~/Obsidian/ClaudeContext/knowledge/weekend-hybrid-trading-system.md`:
- Add "Weekend Results" section
- Include performance table
- Document recommendations
- Set next actions

## 6. Prepare Go-Live Decision

If results are positive:
```
GO LIVE CRITERIA:
✅ Total trades > 20
✅ Win rate > 35%
✅ Net PnL positive
✅ No single pair > 50% of losses
✅ System ran without crashes

RECOMMENDATION: [GO / NO-GO / MORE DATA NEEDED]
```

</process>

<success_criteria>
- [ ] All databases queried
- [ ] Pairs ranked by performance
- [ ] Winners and losers identified
- [ ] Recommendations generated
- [ ] Obsidian updated
- [ ] Go-live decision documented
</success_criteria>
