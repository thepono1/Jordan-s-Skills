---
name: quant:hourly-performance
description: Analyze performance by hour of day
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== HOURLY PERFORMANCE ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strftime('%H', timestamp) as hour_utc,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(SUM(CASE WHEN pnl > 0 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) as win_rate,
  ROUND(SUM(pnl), 2) as total_pnl
FROM trades
WHERE timestamp > datetime('now', '-7 days')
GROUP BY hour_utc
ORDER BY total_pnl DESC"
```
</process>
