---
name: quant:entry-analyzer
description: Entry timing analysis
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strftime('%H', timestamp, 'unixepoch') as hour,
  COUNT(*) as entries,
  ROUND(AVG(CASE WHEN pnl > 0 THEN 1.0 ELSE 0.0 END) * 100, 0) as win_pct,
  ROUND(AVG(pnl), 2) as avg_pnl
FROM trades
WHERE side = 'BUY'
GROUP BY hour
ORDER BY avg_pnl DESC"
```
</process>
