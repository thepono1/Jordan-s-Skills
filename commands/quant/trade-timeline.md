---
name: quant:trade-timeline
description: Show recent trades in timeline format
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== TRADE TIMELINE (Last 20) ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strftime('%H:%M', timestamp) as time,
  symbol,
  side,
  ROUND(size, 4) as size,
  ROUND(entry_price, 2) as price,
  ROUND(pnl, 2) as pnl,
  CASE WHEN pnl > 0 THEN '✓' ELSE '✗' END as result
FROM trades
ORDER BY timestamp DESC
LIMIT 20"
```
</process>
