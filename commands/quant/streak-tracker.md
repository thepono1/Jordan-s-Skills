---
name: quant:streak-tracker
description: Track winning and losing streaks
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== STREAK ANALYSIS ==="
sqlite3 efg_paper_trading/trading.db "
WITH streaks AS (
  SELECT
    strategy_name,
    CASE WHEN pnl > 0 THEN 'W' ELSE 'L' END as result,
    timestamp
  FROM trades
  WHERE timestamp > datetime('now', '-30 days')
  ORDER BY timestamp DESC
  LIMIT 50
)
SELECT
  strategy_name,
  GROUP_CONCAT(result, '') as recent_results
FROM streaks
GROUP BY strategy_name"

echo ""
echo "Legend: W=Win, L=Loss (most recent first)"
```
</process>
