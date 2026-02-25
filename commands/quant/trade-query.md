---
name: quant:trade-query
description: Pre-built queries for trade analysis
argument-hint: [last|today|winners|losers|symbol]
allowed-tools:
  - Bash
  - Read
---

<objective>
Quick access to common trade queries. Pre-built for speed.
</objective>

<process>

## 1. Parse Query Type

Commands:
- `last [N]` - Last N trades (default: 10)
- `today` - Today's trades
- `winners` - Best trades all time
- `losers` - Worst trades all time
- `symbol [SYM]` - Trades for symbol
- `hour` - Last hour's trades

## 2. Execute Query

### last [N]
```bash
cd ~/Developer/quant_master/quant_v4
N=${N:-10}
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  id,
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  strategy_name,
  side,
  quantity,
  price,
  ROUND(pnl, 2) as pnl
FROM trades
ORDER BY timestamp DESC
LIMIT $N"
```

### today
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  strategy_name,
  side,
  ROUND(pnl, 2) as pnl
FROM trades
WHERE date(timestamp, 'unixepoch') = date('now')
ORDER BY timestamp DESC"
```

### winners
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  strategy_name,
  side,
  quantity,
  ROUND(pnl, 2) as pnl
FROM trades
WHERE pnl > 0
ORDER BY pnl DESC
LIMIT 10"
```

### losers
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  strategy_name,
  side,
  quantity,
  ROUND(pnl, 2) as pnl
FROM trades
WHERE pnl < 0
ORDER BY pnl ASC
LIMIT 10"
```

### symbol
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  strategy_name,
  side,
  quantity,
  price,
  ROUND(pnl, 2) as pnl
FROM trades
WHERE symbol LIKE '%$SYMBOL%'
ORDER BY timestamp DESC
LIMIT 20"
```

### hour
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  strategy_name,
  side,
  ROUND(pnl, 2) as pnl
FROM trades
WHERE timestamp > strftime('%s', 'now', '-1 hour')
ORDER BY timestamp DESC"
```

## 3. Summary Stats

Always append summary:
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 efg_paper_trading/trading.db "
SELECT
  COUNT(*) || ' trades, $' || ROUND(SUM(pnl), 2) || ' PnL' as summary
FROM trades
WHERE [same filter as query]"
```

</process>

<success_criteria>
- [ ] Query executed quickly
- [ ] Results formatted clearly
- [ ] Summary stats included
</success_criteria>
