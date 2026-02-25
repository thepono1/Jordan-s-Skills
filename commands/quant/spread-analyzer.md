---
name: quant:spread-analyzer
description: Analyze bid-ask spreads and liquidity
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== SPREAD ANALYSIS ==="
sqlite3 -header -column efg_paper_trading/state/l2_data.db "
SELECT
  symbol,
  ROUND(AVG(spread), 4) as avg_spread,
  ROUND(MIN(spread), 4) as min_spread,
  ROUND(MAX(spread), 4) as max_spread,
  ROUND(AVG(spread) / AVG(mid_price) * 10000, 2) as spread_bps,
  COUNT(*) as samples
FROM order_book_snapshots
WHERE timestamp > datetime('now', '-1 hour')
  AND spread > 0
GROUP BY symbol
ORDER BY spread_bps"
```
</process>
