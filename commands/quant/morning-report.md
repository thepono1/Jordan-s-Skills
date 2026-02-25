---
name: quant:morning-report
description: Generate comprehensive morning trading report
allowed-tools:
  - Bash
  - Read
  - WebFetch
---

<objective>
Generate a complete morning briefing covering overnight activity, current positions, market conditions, and today's opportunities.
</objective>

<process>

## 1. Overnight Trading Summary

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== OVERNIGHT TRADES (Last 12 hours) ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  strategy_name,
  side,
  ROUND(pnl, 2) as pnl
FROM trades
WHERE timestamp > strftime('%s', 'now', '-12 hours')
ORDER BY timestamp DESC"
```

## 2. Current Positions

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== OPEN POSITIONS ==="
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

## 3. Portfolio Summary

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== PORTFOLIO SUMMARY ==="
sqlite3 efg_paper_trading/trading.db "
SELECT
  ROUND(SUM(pnl), 2) as total_pnl,
  COUNT(*) as total_trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate
FROM trades
WHERE timestamp > strftime('%s', 'now', '-7 days')"
```

## 4. System Health

```bash
echo "=== SYSTEM STATUS ==="
# Local
ps aux | grep -E "adaptive_beast" | grep -v grep > /dev/null && echo "Paper Trader: RUNNING" || echo "Paper Trader: STOPPED"

# VPS
ssh quantpod "systemctl is-active enhanced-trader" 2>/dev/null && echo "VPS Trader: RUNNING" || echo "VPS Trader: CHECK NEEDED"
```

## 5. Strategy Performance (7-day)

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== TOP STRATEGIES (7-day) ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  ROUND(SUM(pnl), 2) as pnl_7d,
  COUNT(*) as trades,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_pct
FROM trades
WHERE timestamp > strftime('%s', 'now', '-7 days')
GROUP BY strategy_name
ORDER BY pnl_7d DESC
LIMIT 5"
```

## 6. Format Report

Present as:

```
# Morning Report - [DATE]

## Overnight Summary
- Trades: [N]
- PnL: $[X]
- Notable: [any large wins/losses]

## Current Positions
[table of open positions]

## Portfolio (7-day)
- Total PnL: $[X]
- Win Rate: [X]%
- Trades: [N]

## System Status
- Paper Trader: [status]
- VPS: [status]
- All systems: [GO/ISSUES]

## Top Strategies
[top 5 by 7-day PnL]

## Action Items
- [any positions needing attention]
- [any system issues]
```

</process>

<success_criteria>
- [ ] Overnight activity captured
- [ ] All positions listed
- [ ] Portfolio metrics calculated
- [ ] System health verified
- [ ] Actionable summary provided
</success_criteria>
