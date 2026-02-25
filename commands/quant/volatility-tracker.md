---
name: quant:volatility-tracker
description: Track realized volatility across timeframes
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== VOLATILITY TRACKING ==="
sqlite3 -header -column efg_paper_trading/state/l2_data.db "
SELECT
  symbol,
  ROUND(AVG(spread), 4) as avg_spread,
  ROUND(MAX(spread) - MIN(spread), 4) as spread_range,
  COUNT(*) as ticks
FROM order_book_snapshots
WHERE timestamp > datetime('now', '-1 hour')
GROUP BY symbol"

echo ""
echo "=== Price Range (1h) ==="
sqlite3 -header -column efg_paper_trading/state/l2_data.db "
SELECT
  symbol,
  ROUND(MIN(mid_price), 2) as low,
  ROUND(MAX(mid_price), 2) as high,
  ROUND(MAX(mid_price) - MIN(mid_price), 2) as range
FROM order_book_snapshots
WHERE timestamp > datetime('now', '-1 hour')
GROUP BY symbol"
```
</process>
