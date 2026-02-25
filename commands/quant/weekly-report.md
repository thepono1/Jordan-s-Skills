---
name: quant:weekly-report
description: Generate automated weekly performance summary
allowed-tools:
  - Bash
  - Read
---

<objective>
Comprehensive weekly trading report with performance metrics, strategy analysis, and system health summary.
</objective>

<process>

## 1. Week Performance

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== WEEKLY PERFORMANCE ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  'This Week' as period,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_trade,
  ROUND(MAX(pnl), 2) as best,
  ROUND(MIN(pnl), 2) as worst
FROM trades
WHERE timestamp > strftime('%s', 'now', 'weekday 0', '-7 days')"
```

## 2. Daily Breakdown

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== DAILY BREAKDOWN ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strftime('%w', timestamp, 'unixepoch') as dow,
  CASE strftime('%w', timestamp, 'unixepoch')
    WHEN '0' THEN 'Sun'
    WHEN '1' THEN 'Mon'
    WHEN '2' THEN 'Tue'
    WHEN '3' THEN 'Wed'
    WHEN '4' THEN 'Thu'
    WHEN '5' THEN 'Fri'
    WHEN '6' THEN 'Sat'
  END as day,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 0) as win_pct
FROM trades
WHERE timestamp > strftime('%s', 'now', 'weekday 0', '-7 days')
GROUP BY dow
ORDER BY dow"
```

## 3. Strategy Performance

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== TOP STRATEGIES THIS WEEK ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 0) as win_pct
FROM trades
WHERE timestamp > strftime('%s', 'now', 'weekday 0', '-7 days')
GROUP BY strategy_name
ORDER BY pnl DESC
LIMIT 10"
```

## 4. Week vs Previous

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== WEEK COMPARISON ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  'This Week' as period,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate
FROM trades
WHERE timestamp > strftime('%s', 'now', 'weekday 0', '-7 days')
UNION ALL
SELECT
  'Last Week',
  COUNT(*),
  ROUND(SUM(pnl), 2),
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1)
FROM trades
WHERE timestamp BETWEEN strftime('%s', 'now', 'weekday 0', '-14 days') AND strftime('%s', 'now', 'weekday 0', '-7 days')"
```

## 5. System Uptime

```bash
echo ""
echo "=== SYSTEM UPTIME ==="
# Check log gaps for downtime
cd ~/Developer/quant_master/quant_v4
if [ -f efg_paper_trading/logs/beast.log ]; then
  first=$(head -1 efg_paper_trading/logs/beast.log 2>/dev/null | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
  last=$(tail -1 efg_paper_trading/logs/beast.log 2>/dev/null | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
  echo "Log range: $first to $last"
fi

# VPS uptime
ssh quantpod "uptime" 2>/dev/null || echo "VPS: Unable to check"
```

## 6. Format Report

```
# Weekly Report - Week of [DATE]

## Summary
- Total PnL: $[X]
- Trades: [N]
- Win Rate: [X]%
- vs Last Week: [+/-X]%

## Daily Performance
| Day | Trades | PnL | Win% |
|-----|--------|-----|------|

## Top Strategies
| Strategy | Trades | PnL | Win% |
|----------|--------|-----|------|

## System Health
- Uptime: [X]%
- Errors: [N]
- Data Quality: [status]

## Key Observations
- [notable patterns]
- [strategies to watch]
- [issues to address]
```

</process>

<success_criteria>
- [ ] Full week captured
- [ ] Daily breakdown included
- [ ] Strategy analysis complete
- [ ] Comparison provided
- [ ] Actionable insights
</success_criteria>
