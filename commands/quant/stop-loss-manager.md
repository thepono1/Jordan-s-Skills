---
name: quant:stop-loss-manager
description: Review and manage stop losses
allowed-tools:
  - Bash
  - Read
---

<objective>
Review stop loss placements, trailing stops, and adjustments.
</objective>

<process>

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== STOP LOSS STATUS ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  id,
  symbol,
  strategy_name,
  side,
  entry_price,
  stop_loss,
  ROUND((entry_price - stop_loss) / entry_price * 100, 2) as stop_pct
FROM positions
WHERE status='OPEN' AND stop_loss IS NOT NULL
ORDER BY stop_pct DESC"

echo ""
echo "Positions without stops:"
sqlite3 efg_paper_trading/trading.db "
SELECT COUNT(*) FROM positions
WHERE status='OPEN' AND stop_loss IS NULL"
```

</process>
