---
name: quant:evening-report
description: Generate end-of-day trading summary
allowed-tools:
  - Bash
  - Read
---

<objective>
Generate comprehensive end-of-day report: day's performance, position status, system health, and overnight preparation.
</objective>

<process>

## 1. Today's Performance

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== TODAY'S TRADING SUMMARY ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  'Today' as period,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losses,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_trade,
  ROUND(MAX(pnl), 2) as best,
  ROUND(MIN(pnl), 2) as worst
FROM trades
WHERE date(timestamp, 'unixepoch') = date('now')"
```

## 2. Strategy Performance Today

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== STRATEGY PERFORMANCE ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 0) as win_pct
FROM trades
WHERE date(timestamp, 'unixepoch') = date('now')
GROUP BY strategy_name
ORDER BY pnl DESC"
```

## 3. Open Positions EOD

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== POSITIONS HELD OVERNIGHT ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  symbol,
  strategy_name,
  side,
  quantity,
  entry_price,
  ROUND((julianday('now') - julianday(datetime(entry_time, 'unixepoch'))) * 24, 1) as hours_held
FROM positions
WHERE status='OPEN'"
```

## 4. Week-to-Date

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== WEEK TO DATE ==="
sqlite3 efg_paper_trading/trading.db "
SELECT
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate
FROM trades
WHERE timestamp > strftime('%s', 'now', 'weekday 0', '-7 days')"
```

## 5. System Status

```bash
echo "=== SYSTEM STATUS ==="
# Local
pgrep -f "adaptive_beast" > /dev/null && echo "Paper Trader: RUNNING" || echo "Paper Trader: STOPPED"

# VPS
ssh quantpod "systemctl is-active enhanced-trader 2>/dev/null" && echo "VPS Trader: RUNNING" || echo "VPS Trader: CHECK"

# Disk
df -h / | awk 'NR==2 {print "Disk: " $5 " used"}'
```

## 6. Format Report

```
# Evening Report - [DATE]

## Today's Results
- Trades: [N]
- PnL: $[X] ([+/-X]%)
- Win Rate: [X]%
- Best Trade: $[X] ([strategy])
- Worst Trade: $[X] ([strategy])

## Strategy Breakdown
| Strategy | Trades | PnL | Win% |
|----------|--------|-----|------|

## Overnight Positions
[table or "No positions held"]

## Week-to-Date
- PnL: $[X]
- Trades: [N]
- Win Rate: [X]%

## System Health
- All systems: [GO/ISSUES]
- Overnight mode: [ACTIVE/INACTIVE]

## Tomorrow's Focus
- [Any strategies to watch]
- [Any positions needing attention]
```

</process>

<success_criteria>
- [ ] Day's complete performance captured
- [ ] All positions accounted for
- [ ] WTD context provided
- [ ] System health verified
- [ ] Overnight preparation noted
</success_criteria>
