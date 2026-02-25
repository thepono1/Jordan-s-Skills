---
name: quant:quick-stats
description: Quick overview of key trading statistics
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== QUICK STATS ==="
sqlite3 efg_paper_trading/trading.db "
SELECT
  'Today' as period,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(SUM(pnl), 2) as pnl
FROM trades
WHERE DATE(timestamp) = DATE('now')
UNION ALL
SELECT
  '7 Days',
  COUNT(*),
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END),
  ROUND(SUM(pnl), 2)
FROM trades
WHERE timestamp > datetime('now', '-7 days')
UNION ALL
SELECT
  '30 Days',
  COUNT(*),
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END),
  ROUND(SUM(pnl), 2)
FROM trades
WHERE timestamp > datetime('now', '-30 days')"

echo ""
echo "=== OPEN POSITIONS ==="
sqlite3 efg_paper_trading/trading.db "SELECT COUNT(*) || ' positions open' FROM positions WHERE status='OPEN'"
```
</process>
