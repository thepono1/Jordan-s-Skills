---
name: quant:strategy-analyzer
description: Analyze strategy performance metrics and trends
argument-hint: [strategy-name|top|bottom|compare]
allowed-tools:
  - Bash
  - Read
---

<objective>
Deep analysis of strategy performance: win rates, PnL trends, drawdowns, regime performance. Know what's working.
</objective>

<process>

## 1. Parse Request

Default: show top 10 strategies by PnL

Options:
- `top` - Top 10 performing strategies
- `bottom` - Bottom 10 performing strategies
- `[name]` - Detailed analysis of specific strategy
- `compare [s1] [s2]` - Compare two strategies
- `regime` - Performance by market regime

## 2. Execute Analysis

### top
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_pnl,
  ROUND(MAX(pnl), 2) as best_trade,
  ROUND(MIN(pnl), 2) as worst_trade
FROM trades
GROUP BY strategy_name
HAVING trades >= 3
ORDER BY total_pnl DESC
LIMIT 10"
```

### bottom
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_pnl
FROM trades
GROUP BY strategy_name
HAVING trades >= 3
ORDER BY total_pnl ASC
LIMIT 10"
```

### specific strategy
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== STRATEGY: $STRATEGY_NAME ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  COUNT(*) as total_trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_pnl,
  ROUND(MAX(pnl), 2) as best_trade,
  ROUND(MIN(pnl), 2) as worst_trade,
  ROUND(SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END) / ABS(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END)), 2) as profit_factor
FROM trades
WHERE strategy_name LIKE '%$STRATEGY_NAME%'"

echo ""
echo "=== RECENT TRADES ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  side,
  ROUND(pnl, 2) as pnl
FROM trades
WHERE strategy_name LIKE '%$STRATEGY_NAME%'
ORDER BY timestamp DESC
LIMIT 10"

echo ""
echo "=== DAILY PERFORMANCE ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  date(timestamp, 'unixepoch') as date,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl
FROM trades
WHERE strategy_name LIKE '%$STRATEGY_NAME%'
GROUP BY date
ORDER BY date DESC
LIMIT 7"
```

## 3. Calculate Advanced Metrics

```bash
cd ~/Developer/quant_master/quant_v4
python3 -c "
import sqlite3
conn = sqlite3.connect('efg_paper_trading/trading.db')
df = conn.execute('SELECT pnl FROM trades WHERE strategy_name LIKE \"%$STRATEGY_NAME%\" ORDER BY timestamp').fetchall()
if df:
    pnls = [x[0] for x in df]
    cumulative = 0
    max_val = 0
    max_dd = 0
    for p in pnls:
        cumulative += p
        max_val = max(max_val, cumulative)
        dd = max_val - cumulative
        max_dd = max(max_dd, dd)
    print(f'Max Drawdown: \${max_dd:.2f}')
    print(f'Cumulative PnL: \${cumulative:.2f}')
" 2>/dev/null
```

## 4. Present Results

```
# Strategy Analysis

## Top Performers
| Strategy | Trades | Win% | PnL | Avg |
|----------|--------|------|-----|-----|
| strat1 | 50 | 62% | $125 | $2.50 |

## Metrics
- Best Strategy: [name] ($X)
- Most Consistent: [name] (X% win rate)
- Most Active: [name] (N trades)

## Recommendations
- Consider: [strategies to increase]
- Review: [strategies underperforming]
- Disable: [strategies losing consistently]
```

</process>

<success_criteria>
- [ ] Performance metrics calculated
- [ ] Trend analysis included
- [ ] Actionable recommendations
- [ ] Clear visualizations
</success_criteria>
