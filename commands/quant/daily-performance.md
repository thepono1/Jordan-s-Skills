---
name: quant:daily-performance
description: Daily performance breakdown
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== DAILY PERFORMANCE (Last 14 days) ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  DATE(timestamp) as date,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(SUM(CASE WHEN pnl > 0 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) as win_rate,
  ROUND(SUM(pnl), 2) as pnl
FROM trades
WHERE timestamp > datetime('now', '-14 days')
GROUP BY DATE(timestamp)
ORDER BY date DESC"
```
</process>
