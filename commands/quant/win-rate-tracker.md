---
name: quant:win-rate-tracker
description: Track win rates across strategies and time periods
argument-hint: [overall|strategy|daily|trend]
allowed-tools:
  - Bash
  - Read
---

<objective>
Quick strategy pulse on win rates. Track success rates across different dimensions.
</objective>

<process>

## 1. Parse View

Default: overall

Options:
- `overall` - Overall win rate stats
- `strategy` - Win rate by strategy
- `daily` - Win rate by day
- `trend` - Win rate trend over time

## 2. Execute Query

### overall
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== OVERALL WIN RATE ==="
sqlite3 efg_paper_trading/trading.db "
SELECT
  COUNT(*) as total_trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losses,
  SUM(CASE WHEN pnl = 0 THEN 1 ELSE 0 END) as breakeven,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  ROUND(AVG(CASE WHEN pnl > 0 THEN pnl END), 2) as avg_win,
  ROUND(AVG(CASE WHEN pnl < 0 THEN pnl END), 2) as avg_loss
FROM trades"
```

### strategy
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== WIN RATE BY STRATEGY ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_pct,
  ROUND(AVG(CASE WHEN pnl > 0 THEN pnl END), 2) as avg_win,
  ROUND(AVG(CASE WHEN pnl < 0 THEN pnl END), 2) as avg_loss,
  ROUND(
    AVG(CASE WHEN pnl > 0 THEN pnl END) / ABS(AVG(CASE WHEN pnl < 0 THEN pnl END)),
    2
  ) as rr_ratio
FROM trades
GROUP BY strategy_name
HAVING trades >= 5
ORDER BY win_pct DESC"
```

### daily
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== DAILY WIN RATE (Last 14 days) ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  date(timestamp, 'unixepoch') as date,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 0) as win_pct,
  ROUND(SUM(pnl), 2) as pnl
FROM trades
WHERE timestamp > strftime('%s', 'now', '-14 days')
GROUP BY date
ORDER BY date DESC"
```

### trend
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== WIN RATE TREND ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  'Last 7 days' as period,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  COUNT(*) as trades
FROM trades
WHERE timestamp > strftime('%s', 'now', '-7 days')
UNION ALL
SELECT
  'Previous 7 days',
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1),
  COUNT(*)
FROM trades
WHERE timestamp BETWEEN strftime('%s', 'now', '-14 days') AND strftime('%s', 'now', '-7 days')
UNION ALL
SELECT
  'Last 30 days',
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1),
  COUNT(*)
FROM trades
WHERE timestamp > strftime('%s', 'now', '-30 days')"
```

## 3. Calculate Quality Metrics

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== QUALITY METRICS ==="
sqlite3 efg_paper_trading/trading.db "
SELECT
  'Profit Factor' as metric,
  ROUND(
    SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END) /
    ABS(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END)),
    2
  ) as value
FROM trades
WHERE pnl != 0
UNION ALL
SELECT
  'Expectancy',
  ROUND(AVG(pnl), 2)
FROM trades
UNION ALL
SELECT
  'Risk/Reward',
  ROUND(
    AVG(CASE WHEN pnl > 0 THEN pnl END) /
    ABS(AVG(CASE WHEN pnl < 0 THEN pnl END)),
    2
  )
FROM trades"
```

## 4. Present Results

```
# Win Rate Analysis

## Overall
- Win Rate: [X]%
- Total Trades: [N]
- Wins/Losses: [W]/[L]

## Quality Metrics
- Profit Factor: [X]
- Expectancy: $[X]
- Risk/Reward: [X]:1

## By Strategy
| Strategy | Trades | Win% | R:R |
|----------|--------|------|-----|

## Trend
- Recent (7d): [X]%
- Previous (7d): [X]%
- Direction: [improving/declining/stable]
```

</process>

<success_criteria>
- [ ] Overall win rate calculated
- [ ] Strategy breakdown provided
- [ ] Trend identified
- [ ] Quality metrics included
</success_criteria>
