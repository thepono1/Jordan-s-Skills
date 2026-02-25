---
name: quant:best-performers
description: Show best performing strategies and pairs
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== TOP STRATEGIES (by PnL) ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(SUM(CASE WHEN pnl > 0 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) as win_rate,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 3) as avg_pnl
FROM trades
WHERE timestamp > datetime('now', '-7 days')
GROUP BY strategy_name
HAVING trades >= 5
ORDER BY total_pnl DESC
LIMIT 10"

echo ""
echo "=== TOP PAIRS ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  symbol,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as total_pnl
FROM trades
WHERE timestamp > datetime('now', '-7 days')
GROUP BY symbol
ORDER BY total_pnl DESC"
```
</process>
