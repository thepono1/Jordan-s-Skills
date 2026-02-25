---
name: quant:trade-histogram
description: Show distribution of trade outcomes
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== TRADE PNL DISTRIBUTION ==="
sqlite3 efg_paper_trading/trading.db "
SELECT
  CASE
    WHEN pnl < -5 THEN '< -\$5'
    WHEN pnl < -2 THEN '-\$5 to -\$2'
    WHEN pnl < -1 THEN '-\$2 to -\$1'
    WHEN pnl < 0 THEN '-\$1 to \$0'
    WHEN pnl < 1 THEN '\$0 to \$1'
    WHEN pnl < 2 THEN '\$1 to \$2'
    WHEN pnl < 5 THEN '\$2 to \$5'
    ELSE '> \$5'
  END as bucket,
  COUNT(*) as count,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM trades), 1) as pct
FROM trades
WHERE pnl IS NOT NULL
GROUP BY bucket
ORDER BY MIN(pnl)"
```
</process>
