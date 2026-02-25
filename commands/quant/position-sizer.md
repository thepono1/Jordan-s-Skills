---
name: quant:position-sizer
description: Calculate optimal position sizes based on risk
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== POSITION SIZING CALCULATOR ==="
echo "Capital: \$500 | Risk per trade: 1-2%"
echo ""
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  symbol,
  COUNT(*) as trades,
  ROUND(AVG(ABS(pnl)), 2) as avg_move,
  ROUND(500 * 0.01 / NULLIF(AVG(ABS(pnl)), 0), 4) as size_1pct_risk,
  ROUND(500 * 0.02 / NULLIF(AVG(ABS(pnl)), 0), 4) as size_2pct_risk
FROM trades
WHERE timestamp > datetime('now', '-7 days')
GROUP BY symbol
HAVING trades >= 5"
```
</process>
