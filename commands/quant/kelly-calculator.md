---
name: quant:kelly-calculator
description: Calculate optimal Kelly criterion position sizing
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== KELLY CRITERION CALCULATOR ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(SUM(CASE WHEN pnl > 0 THEN 1.0 ELSE 0 END) / COUNT(*), 3) as win_rate,
  ROUND(AVG(CASE WHEN pnl > 0 THEN pnl END), 2) as avg_win,
  ROUND(ABS(AVG(CASE WHEN pnl < 0 THEN pnl END)), 2) as avg_loss,
  ROUND(
    (SUM(CASE WHEN pnl > 0 THEN 1.0 ELSE 0 END) / COUNT(*)) -
    ((1 - SUM(CASE WHEN pnl > 0 THEN 1.0 ELSE 0 END) / COUNT(*)) /
     (AVG(CASE WHEN pnl > 0 THEN pnl END) / ABS(AVG(CASE WHEN pnl < 0 THEN pnl END)))), 3
  ) as kelly_fraction
FROM trades
WHERE timestamp > datetime('now', '-30 days')
GROUP BY strategy_name
HAVING trades >= 10
ORDER BY kelly_fraction DESC"
```
</process>
