---
name: quant:sharpe-calculator
description: Calculate rolling Sharpe ratio and risk-adjusted returns
argument-hint: [daily|weekly|strategy]
allowed-tools:
  - Bash
  - Read
---

<objective>
Calculate Sharpe ratio for rolling performance measurement. Risk-adjusted returns metric.
</objective>

<process>

## 1. Parse Period

Default: daily for last 30 days

Options:
- `daily` - Daily returns Sharpe
- `weekly` - Weekly returns Sharpe
- `strategy` - Sharpe by strategy
- `[N]` - Custom N-day window

## 2. Calculate Sharpe Ratio

### Daily Sharpe (30-day rolling)
```bash
cd ~/Developer/quant_master/quant_v4
python3 << 'EOF'
import sqlite3
import numpy as np

conn = sqlite3.connect('efg_paper_trading/trading.db')

# Get daily PnL
daily_pnl = conn.execute('''
    SELECT date(timestamp, 'unixepoch') as date, SUM(pnl) as daily_pnl
    FROM trades
    WHERE timestamp > strftime('%s', 'now', '-30 days')
    GROUP BY date
    ORDER BY date
''').fetchall()

if len(daily_pnl) < 2:
    print("Insufficient data for Sharpe calculation")
else:
    returns = [x[1] for x in daily_pnl]
    mean_return = np.mean(returns)
    std_return = np.std(returns)

    if std_return > 0:
        daily_sharpe = mean_return / std_return
        annual_sharpe = daily_sharpe * np.sqrt(365)
        print(f"Period: Last 30 days")
        print(f"Trading Days: {len(returns)}")
        print(f"Mean Daily PnL: ${mean_return:.2f}")
        print(f"Std Daily PnL: ${std_return:.2f}")
        print(f"Daily Sharpe: {daily_sharpe:.2f}")
        print(f"Annualized Sharpe: {annual_sharpe:.2f}")
    else:
        print("Zero volatility - cannot calculate Sharpe")

conn.close()
EOF
```

### Strategy Sharpe
```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== SHARPE BY STRATEGY ==="
python3 << 'EOF'
import sqlite3
import numpy as np

conn = sqlite3.connect('efg_paper_trading/trading.db')

strategies = conn.execute('''
    SELECT DISTINCT strategy_name FROM trades
    WHERE timestamp > strftime('%s', 'now', '-30 days')
''').fetchall()

results = []
for (strat,) in strategies:
    pnls = conn.execute('''
        SELECT pnl FROM trades
        WHERE strategy_name = ? AND timestamp > strftime('%s', 'now', '-30 days')
    ''', (strat,)).fetchall()

    if len(pnls) >= 5:
        returns = [x[0] for x in pnls]
        mean_r = np.mean(returns)
        std_r = np.std(returns)
        if std_r > 0:
            sharpe = mean_r / std_r
            results.append((strat, len(pnls), sharpe, mean_r))

results.sort(key=lambda x: x[2], reverse=True)
print(f"{'Strategy':<30} {'Trades':<8} {'Sharpe':<10} {'Avg PnL':<10}")
print("-" * 60)
for strat, n, sharpe, avg in results[:15]:
    print(f"{strat[:28]:<30} {n:<8} {sharpe:<10.2f} ${avg:<10.2f}")

conn.close()
EOF
```

## 3. Rolling Sharpe Trend

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== ROLLING SHARPE TREND ==="
python3 << 'EOF'
import sqlite3
import numpy as np

conn = sqlite3.connect('efg_paper_trading/trading.db')

# Weekly rolling Sharpe
weeks = conn.execute('''
    SELECT
        strftime('%Y-W%W', timestamp, 'unixepoch') as week,
        SUM(pnl) as weekly_pnl,
        COUNT(*) as trades
    FROM trades
    WHERE timestamp > strftime('%s', 'now', '-8 weeks')
    GROUP BY week
    ORDER BY week
''').fetchall()

if len(weeks) >= 2:
    pnls = [x[1] for x in weeks]
    print(f"{'Week':<12} {'PnL':<12} {'Trades':<8}")
    print("-" * 35)
    for week, pnl, trades in weeks:
        print(f"{week:<12} ${pnl:<11.2f} {trades:<8}")

    rolling_mean = np.mean(pnls)
    rolling_std = np.std(pnls)
    if rolling_std > 0:
        weekly_sharpe = rolling_mean / rolling_std
        print(f"\nWeekly Sharpe (8-week): {weekly_sharpe:.2f}")

conn.close()
EOF
```

## 4. Present Results

```
# Sharpe Ratio Analysis

## Current Sharpe
- Daily (30d): [X]
- Annualized: [X]
- Interpretation: [excellent/good/poor]

## By Strategy
| Strategy | Sharpe | Trades |
|----------|--------|--------|

## Benchmarks
- > 2.0: Excellent
- 1.0-2.0: Good
- 0.5-1.0: Average
- < 0.5: Poor
```

</process>

<success_criteria>
- [ ] Sharpe ratio calculated
- [ ] Strategy breakdown provided
- [ ] Trend analysis included
- [ ] Context/benchmarks given
</success_criteria>
