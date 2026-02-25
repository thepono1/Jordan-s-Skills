---
name: quant:db-query
description: Query trading databases with pre-built common queries
argument-hint: [query-type or custom SQL]
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

<objective>
Execute common database queries or custom SQL against trading databases. Provides quick access to positions, trades, strategies, and performance data.
</objective>

<context>
Databases:
- `efg_paper_trading/trading.db` - Active paper trades and positions
- `data/unified_alpha_v4.db` - Alpha engine state
- `data/strategy_validation.db` - Walk-forward results
- `data/circuit_breaker.db` - Risk circuit state
</context>

<process>

## 1. Parse Query Type

If $ARGUMENTS is empty, offer menu:

```
Common Queries:
1. open-positions - Show all open positions
2. recent-trades - Last 20 trades
3. strategy-pnl - PnL by strategy
4. daily-summary - Today's trading summary
5. winners - Best performing strategies
6. losers - Worst performing strategies
7. custom - Run custom SQL
```

## 2. Execute Query

### open-positions
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  symbol,
  strategy_name,
  side,
  quantity,
  entry_price,
  datetime(entry_time, 'unixepoch') as entry_time,
  ROUND((julianday('now') - julianday(datetime(entry_time, 'unixepoch'))) * 24, 1) as hours_held
FROM positions
WHERE status='OPEN'
ORDER BY entry_time DESC"
```

### recent-trades
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  datetime(timestamp, 'unixepoch') as time,
  symbol,
  strategy_name,
  side,
  quantity,
  price,
  ROUND(pnl, 2) as pnl
FROM trades
ORDER BY timestamp DESC
LIMIT 20"
```

### strategy-pnl
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_pnl
FROM trades
GROUP BY strategy_name
ORDER BY total_pnl DESC"
```

### daily-summary
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  date(timestamp, 'unixepoch') as date,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(SUM(pnl), 2) as total_pnl
FROM trades
WHERE date(timestamp, 'unixepoch') = date('now')
GROUP BY date"
```

### winners
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  ROUND(SUM(pnl), 2) as total_pnl,
  COUNT(*) as trades,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate
FROM trades
GROUP BY strategy_name
HAVING total_pnl > 0
ORDER BY total_pnl DESC
LIMIT 10"
```

### losers
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  ROUND(SUM(pnl), 2) as total_pnl,
  COUNT(*) as trades,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate
FROM trades
GROUP BY strategy_name
HAVING total_pnl < 0
ORDER BY total_pnl ASC
LIMIT 10"
```

### custom
Prompt user for SQL and target database, then execute.

</process>

<success_criteria>
- [ ] Query type identified
- [ ] Correct database targeted
- [ ] Results formatted clearly
- [ ] No SQL injection if custom query
</success_criteria>
