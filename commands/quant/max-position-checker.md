---
name: quant:max-position-checker
description: Check if positions exceed maximum limits
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== MAX POSITION CHECK ==="
echo "Limits: Single position 20%, Total exposure 100%"
echo ""
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  symbol,
  strategy_name,
  side,
  size,
  entry_price,
  ROUND(size * entry_price, 2) as notional,
  ROUND(size * entry_price / 500 * 100, 1) as pct_of_capital
FROM positions
WHERE status = 'OPEN'
ORDER BY notional DESC"

echo ""
echo "=== TOTAL EXPOSURE ==="
sqlite3 efg_paper_trading/trading.db "
SELECT
  ROUND(SUM(size * entry_price), 2) as total_notional,
  ROUND(SUM(size * entry_price) / 500 * 100, 1) as pct_of_capital
FROM positions
WHERE status = 'OPEN'"
```
</process>
