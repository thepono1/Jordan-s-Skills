---
name: quant:momentum-scanner
description: Scan for momentum signals across pairs
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== MOMENTUM SCANNER ==="
sqlite3 -header -column efg_paper_trading/state/l2_data.db "
WITH recent AS (
  SELECT symbol, mid_price, timestamp,
    ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp DESC) as rn
  FROM order_book_snapshots
  WHERE timestamp > datetime('now', '-10 minutes')
)
SELECT
  a.symbol,
  ROUND(a.mid_price, 2) as current_price,
  ROUND(b.mid_price, 2) as price_10m_ago,
  ROUND((a.mid_price - b.mid_price) / b.mid_price * 100, 3) as pct_change
FROM recent a
JOIN recent b ON a.symbol = b.symbol
WHERE a.rn = 1 AND b.rn = (SELECT MAX(rn) FROM recent WHERE symbol = a.symbol)
ORDER BY pct_change DESC"
```
</process>
