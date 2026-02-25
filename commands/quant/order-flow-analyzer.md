---
name: quant:order-flow-analyzer
description: Analyze order flow and trade aggression
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== ORDER FLOW ANALYSIS ==="
sqlite3 -header -column efg_paper_trading/state/l2_data.db "
SELECT
  symbol,
  ROUND(AVG(imbalance), 3) as avg_imbalance,
  ROUND(MIN(imbalance), 3) as min_imbalance,
  ROUND(MAX(imbalance), 3) as max_imbalance,
  COUNT(*) as samples
FROM order_book_snapshots
WHERE timestamp > datetime('now', '-1 hour')
GROUP BY symbol"
```
</process>
