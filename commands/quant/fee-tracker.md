---
name: quant:fee-tracker
description: Trading fee analysis
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 efg_paper_trading/trading.db "
SELECT
  strftime('%Y-%m', timestamp, 'unixepoch') as month,
  COUNT(*) as trades,
  ROUND(SUM(quantity * price), 2) as volume,
  ROUND(SUM(quantity * price) * 0.002, 2) as est_fees
FROM trades
GROUP BY month
ORDER BY month DESC
LIMIT 6"
```
</process>
