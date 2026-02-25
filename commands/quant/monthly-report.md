---
name: quant:monthly-report
description: Generate comprehensive monthly performance report
allowed-tools:
  - Bash
  - Read
---

<objective>
Comprehensive monthly trading report for performance review and tax preparation.
</objective>

<process>

## 1. Monthly Overview

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== MONTHLY OVERVIEW ==="

sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strftime('%Y-%m', timestamp, 'unixepoch') as month,
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(AVG(pnl), 2) as avg_trade
FROM trades
WHERE timestamp > strftime('%s', 'now', '-90 days')
GROUP BY month
ORDER BY month DESC"
```

## 2. This Month Details

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== THIS MONTH ==="

sqlite3 efg_paper_trading/trading.db "
SELECT
  COUNT(*) as trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(SUM(pnl), 2) as total_pnl,
  ROUND(MAX(pnl), 2) as best_trade,
  ROUND(MIN(pnl), 2) as worst_trade,
  ROUND(SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END), 2) as gross_profit,
  ROUND(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END), 2) as gross_loss
FROM trades
WHERE strftime('%Y-%m', timestamp, 'unixepoch') = strftime('%Y-%m', 'now')"
```

## 3. Weekly Breakdown

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== WEEKLY BREAKDOWN ==="

sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strftime('%Y-W%W', timestamp, 'unixepoch') as week,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 0) as win_pct
FROM trades
WHERE strftime('%Y-%m', timestamp, 'unixepoch') = strftime('%Y-%m', 'now')
GROUP BY week
ORDER BY week"
```

## 4. Strategy Performance

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== STRATEGY PERFORMANCE (This Month) ==="

sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 0) as win_pct,
  ROUND(
    SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END) /
    NULLIF(ABS(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END)), 0),
    2
  ) as profit_factor
FROM trades
WHERE strftime('%Y-%m', timestamp, 'unixepoch') = strftime('%Y-%m', 'now')
GROUP BY strategy_name
ORDER BY pnl DESC"
```

## 5. Symbol Performance

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== BY SYMBOL ==="

sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  symbol,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl,
  ROUND(AVG(pnl), 2) as avg_pnl
FROM trades
WHERE strftime('%Y-%m', timestamp, 'unixepoch') = strftime('%Y-%m', 'now')
GROUP BY symbol
ORDER BY pnl DESC"
```

## 6. Drawdown Analysis

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== MONTHLY DRAWDOWN ==="

python3 << 'EOF'
import sqlite3

conn = sqlite3.connect('efg_paper_trading/trading.db')

trades = conn.execute('''
    SELECT pnl FROM trades
    WHERE strftime('%Y-%m', timestamp, 'unixepoch') = strftime('%Y-%m', 'now')
    ORDER BY timestamp
''').fetchall()

if trades:
    cumulative = 0
    peak = 0
    max_dd = 0

    for (pnl,) in trades:
        cumulative += pnl
        peak = max(peak, cumulative)
        dd = peak - cumulative
        max_dd = max(max_dd, dd)

    print(f"Final PnL: ${cumulative:.2f}")
    print(f"Peak PnL: ${peak:.2f}")
    print(f"Max Drawdown: ${max_dd:.2f}")

conn.close()
EOF
```

## 7. Format Report

```
# Monthly Report - [MONTH YEAR]

## Summary
- Total PnL: $[X]
- Trades: [N]
- Win Rate: [X]%
- Best Day: $[X]
- Worst Day: $[X]

## Weekly Performance
| Week | Trades | PnL | Win% |
|------|--------|-----|------|

## Top Strategies
| Strategy | PnL | Trades | PF |
|----------|-----|--------|-----|

## Risk Metrics
- Max Drawdown: $[X]
- Profit Factor: [X]
- Sharpe Ratio: [X]

## YTD Performance
- Total PnL: $[X]
- Months Positive: [N]/[N]
```

</process>

<success_criteria>
- [ ] Full month captured
- [ ] Weekly breakdown included
- [ ] Strategy analysis complete
- [ ] Risk metrics calculated
- [ ] YTD context provided
</success_criteria>
