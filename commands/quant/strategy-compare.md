---
name: quant:strategy-compare
description: Compare performance across strategies side by side
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== STRATEGY COMPARISON (7 days) ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name as strategy,
  COUNT(*) as trades,
  ROUND(SUM(CASE WHEN pnl>0 THEN 1.0 ELSE 0 END)/COUNT(*)*100,0) as 'win%',
  ROUND(SUM(pnl), 2) as pnl,
  ROUND(AVG(pnl), 3) as avg,
  ROUND(MAX(pnl), 2) as best,
  ROUND(MIN(pnl), 2) as worst
FROM trades
WHERE timestamp > datetime('now', '-7 days')
GROUP BY strategy_name
HAVING trades >= 2
ORDER BY pnl DESC"
```
</process>
