---
name: quant:trade-duration
description: Hold time analysis
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(AVG(hold_duration_hours), 1) as avg_hours,
  ROUND(MIN(hold_duration_hours), 1) as min_hours,
  ROUND(MAX(hold_duration_hours), 1) as max_hours
FROM (
  SELECT strategy_name,
    (exit_time - entry_time) / 3600.0 as hold_duration_hours
  FROM positions
  WHERE status='CLOSED' AND exit_time IS NOT NULL
)
GROUP BY strategy_name
HAVING trades >= 3
ORDER BY avg_hours"
```
</process>
