---
name: quant:exit-analyzer
description: Exit efficiency analysis
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as exits,
  ROUND(AVG(pnl), 2) as avg_pnl,
  ROUND(AVG(CASE WHEN pnl > 0 THEN pnl END) / ABS(AVG(CASE WHEN pnl < 0 THEN pnl END)), 2) as rr_ratio
FROM trades
WHERE side = 'SELL'
GROUP BY strategy_name
HAVING exits >= 3
ORDER BY avg_pnl DESC"
```
</process>
