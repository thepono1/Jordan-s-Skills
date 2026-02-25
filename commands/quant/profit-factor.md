---
name: quant:profit-factor
description: Calculate profit factor for strategies
allowed-tools:
  - Bash
---

<objective>
Quick profitability metric - gross profit / gross loss.
</objective>

<process>

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== PROFIT FACTOR ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END), 2) as gross_profit,
  ROUND(ABS(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END)), 2) as gross_loss,
  ROUND(
    SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END) /
    NULLIF(ABS(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END)), 0),
    2
  ) as profit_factor
FROM trades
GROUP BY strategy_name
HAVING trades >= 5
ORDER BY profit_factor DESC"
```

</process>
