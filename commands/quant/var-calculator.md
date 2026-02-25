---
name: quant:var-calculator
description: Calculate Value at Risk for positions
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== VALUE AT RISK (VaR) ==="
echo "Based on recent price movements"
sqlite3 -header -column efg_paper_trading/state/l2_data.db "
WITH price_changes AS (
  SELECT
    symbol,
    (mid_price - LAG(mid_price) OVER (PARTITION BY symbol ORDER BY timestamp)) /
      LAG(mid_price) OVER (PARTITION BY symbol ORDER BY timestamp) * 100 as pct_change
  FROM order_book_snapshots
  WHERE timestamp > datetime('now', '-24 hours')
)
SELECT
  symbol,
  COUNT(*) as samples,
  ROUND(AVG(pct_change), 4) as avg_return,
  ROUND(AVG(pct_change) - 1.645 *
    SQRT(SUM((pct_change - (SELECT AVG(pct_change) FROM price_changes pc2 WHERE pc2.symbol = price_changes.symbol)) *
             (pct_change - (SELECT AVG(pct_change) FROM price_changes pc2 WHERE pc2.symbol = price_changes.symbol))) / COUNT(*)), 4) as var_95
FROM price_changes
WHERE pct_change IS NOT NULL
GROUP BY symbol"
```
</process>
