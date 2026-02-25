---
name: quant:portfolio-summary
description: Complete portfolio overview with positions and equity
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== PORTFOLIO SUMMARY ==="
echo "Capital: \$500"
echo ""

echo "--- Open Positions ---"
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT symbol, side, size, ROUND(entry_price, 2) as entry,
       ROUND(size * entry_price, 2) as notional
FROM positions WHERE status = 'OPEN'"

echo ""
echo "--- Realized PnL ---"
sqlite3 efg_paper_trading/trading.db "
SELECT 'Today: \$' || ROUND(COALESCE(SUM(pnl), 0), 2)
FROM trades WHERE DATE(timestamp) = DATE('now')
UNION ALL
SELECT 'Week: \$' || ROUND(COALESCE(SUM(pnl), 0), 2)
FROM trades WHERE timestamp > datetime('now', '-7 days')
UNION ALL
SELECT 'Month: \$' || ROUND(COALESCE(SUM(pnl), 0), 2)
FROM trades WHERE timestamp > datetime('now', '-30 days')"
```
</process>
