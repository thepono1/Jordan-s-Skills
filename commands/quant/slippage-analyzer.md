---
name: quant:slippage-analyzer
description: Analyze execution slippage
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== SLIPPAGE ANALYSIS ==="
echo "Comparing expected vs actual execution prices"
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  symbol,
  side,
  COUNT(*) as trades,
  ROUND(AVG(ABS(entry_price - expected_price)) / AVG(entry_price) * 10000, 2) as avg_slippage_bps
FROM trades
WHERE expected_price IS NOT NULL
  AND timestamp > datetime('now', '-7 days')
GROUP BY symbol, side
ORDER BY avg_slippage_bps DESC" 2>/dev/null || echo "No expected_price data available"
```
</process>
