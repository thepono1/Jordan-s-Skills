---
name: quant:pnl-calculator
description: Calculate PnL across different time periods and breakdowns
argument-hint: [today|week|month|strategy|all]
allowed-tools:
  - Bash
  - Read
---

<objective>
Calculate profit and loss across various dimensions: time periods, strategies, symbols. Always need this number.
</objective>

<process>

## 1. Parse Time Period

Default: today

Options:
- `today` - Today's PnL
- `week` - Last 7 days
- `month` - Last 30 days
- `strategy` - Breakdown by strategy
- `symbol` - Breakdown by symbol
- `all` - All-time PnL

## 2. Execute Calculations

### today
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 efg_paper_trading/trading.db "
SELECT
  'Today' as period,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losses,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_pnl,
  ROUND(MAX(pnl), 2) as best_trade,
  ROUND(MIN(pnl), 2) as worst_trade
FROM trades
WHERE date(timestamp, 'unixepoch') = date('now')"
```

### week
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  date(timestamp, 'unixepoch') as date,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(SUM(pnl), 2) as pnl
FROM trades
WHERE timestamp > strftime('%s', 'now', '-7 days')
GROUP BY date
ORDER BY date"
```

### month
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strftime('%Y-%m-%d', timestamp, 'unixepoch') as week_start,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate
FROM trades
WHERE timestamp > strftime('%s', 'now', '-30 days')
GROUP BY strftime('%W', timestamp, 'unixepoch')
ORDER BY week_start"
```

### strategy
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate
FROM trades
GROUP BY strategy_name
ORDER BY total_pnl DESC"
```

### symbol
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  symbol,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_pnl
FROM trades
GROUP BY symbol
ORDER BY total_pnl DESC"
```

### all
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 efg_paper_trading/trading.db "
SELECT
  'All Time' as period,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  MIN(date(timestamp, 'unixepoch')) as first_trade,
  MAX(date(timestamp, 'unixepoch')) as last_trade
FROM trades"
```

## 3. Present Results

Format based on query type:

```
# PnL Report - [Period]

## Summary
- Total PnL: $[X]
- Trades: [N]
- Win Rate: [X]%
- Avg Trade: $[X]

## Breakdown
[relevant table]

## Analysis
- Best: [trade/strategy/day]
- Worst: [trade/strategy/day]
- Trend: [improving/declining/stable]
```

</process>

<success_criteria>
- [ ] Correct time period calculated
- [ ] All metrics accurate
- [ ] Clear breakdown provided
- [ ] Trend analysis included
</success_criteria>
