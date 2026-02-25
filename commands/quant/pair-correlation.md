---
name: quant:pair-correlation
description: Analyze correlation between trading pairs
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== PAIR CORRELATION (Price Movements) ==="
sqlite3 -header -column efg_paper_trading/state/l2_data.db "
WITH eth AS (
  SELECT timestamp, mid_price as eth_price
  FROM order_book_snapshots
  WHERE symbol = 'ETH/USD' AND timestamp > datetime('now', '-1 hour')
),
btc AS (
  SELECT timestamp, mid_price as btc_price
  FROM order_book_snapshots
  WHERE symbol = 'BTC/USD' AND timestamp > datetime('now', '-1 hour')
)
SELECT
  'ETH/BTC' as pair,
  COUNT(*) as samples,
  ROUND(AVG(eth_price / btc_price), 6) as avg_ratio,
  ROUND(MIN(eth_price / btc_price), 6) as min_ratio,
  ROUND(MAX(eth_price / btc_price), 6) as max_ratio
FROM eth e
JOIN btc b ON e.timestamp = b.timestamp"
```
</process>
