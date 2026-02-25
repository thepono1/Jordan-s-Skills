---
name: quant:correlation-analyzer
description: Analyze strategy correlation for diversification
argument-hint: [matrix|pairs|reduce]
allowed-tools:
  - Bash
  - Read
---

<objective>
Analyze correlation between strategies to optimize diversification and reduce redundancy.
</objective>

<process>

## 1. Calculate Strategy Returns

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== STRATEGY CORRELATION ANALYSIS ==="

python3 << 'EOF'
import sqlite3
import numpy as np
from collections import defaultdict

conn = sqlite3.connect('efg_paper_trading/trading.db')

# Get trades by strategy and date
trades = conn.execute('''
    SELECT
        strategy_name,
        date(timestamp, 'unixepoch') as date,
        SUM(pnl) as daily_pnl
    FROM trades
    WHERE timestamp > strftime('%s', 'now', '-30 days')
    GROUP BY strategy_name, date
    ORDER BY strategy_name, date
''').fetchall()

# Organize by strategy
strategy_returns = defaultdict(dict)
for strat, date, pnl in trades:
    strategy_returns[strat][date] = pnl

# Get strategies with enough data
strategies = [s for s, returns in strategy_returns.items() if len(returns) >= 5]

if len(strategies) < 2:
    print("Need at least 2 strategies with 5+ days of data")
else:
    # Get all dates
    all_dates = sorted(set(d for returns in strategy_returns.values() for d in returns.keys()))

    # Build return matrix
    matrix = []
    for strat in strategies:
        row = [strategy_returns[strat].get(d, 0) for d in all_dates]
        matrix.append(row)

    matrix = np.array(matrix)

    # Calculate correlation
    if matrix.shape[1] > 1:
        corr = np.corrcoef(matrix)

        print(f"Strategies analyzed: {len(strategies)}")
        print()
        print("Correlation Matrix:")
        print("-" * 50)

        # Print header
        print(f"{'':>20}", end="")
        for i, s in enumerate(strategies[:5]):
            print(f"{s[:8]:>10}", end="")
        print()

        # Print matrix
        for i, s in enumerate(strategies[:5]):
            print(f"{s[:18]:>20}", end="")
            for j in range(min(5, len(strategies))):
                print(f"{corr[i,j]:>10.2f}", end="")
            print()

        # Find highly correlated pairs
        print()
        print("Highly Correlated Pairs (>0.7):")
        for i in range(len(strategies)):
            for j in range(i+1, len(strategies)):
                if abs(corr[i,j]) > 0.7:
                    print(f"  {strategies[i][:20]} <-> {strategies[j][:20]}: {corr[i,j]:.2f}")

conn.close()
EOF
```

## 2. Diversification Score

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== DIVERSIFICATION SCORE ==="

python3 << 'EOF'
import sqlite3
import numpy as np
from collections import defaultdict

conn = sqlite3.connect('efg_paper_trading/trading.db')

# Get daily portfolio returns
daily = conn.execute('''
    SELECT
        date(timestamp, 'unixepoch') as date,
        SUM(pnl) as daily_pnl
    FROM trades
    WHERE timestamp > strftime('%s', 'now', '-30 days')
    GROUP BY date
    ORDER BY date
''').fetchall()

if len(daily) >= 5:
    returns = [d[1] for d in daily]
    volatility = np.std(returns)
    mean = np.mean(returns)

    # Count strategies
    strat_count = conn.execute('''
        SELECT COUNT(DISTINCT strategy_name) FROM trades
        WHERE timestamp > strftime('%s', 'now', '-30 days')
    ''').fetchone()[0]

    print(f"Active strategies: {strat_count}")
    print(f"Portfolio volatility: ${volatility:.2f}/day")
    print(f"Average return: ${mean:.2f}/day")

    # Simple diversification score
    if volatility > 0:
        div_score = mean / volatility
        print(f"Diversification score: {div_score:.2f}")

conn.close()
EOF
```

## 3. Present Results

```
# Correlation Analysis

## Correlation Matrix
[matrix visualization]

## Highly Correlated Pairs
- [strat1] <-> [strat2]: 0.85
- Consider reducing one

## Diversification
- Score: [X]
- Effective strategies: [N]

## Recommendations
- [redundant strategies to consider removing]
- [uncorrelated strategies to add]
```

</process>

<success_criteria>
- [ ] Correlations calculated
- [ ] Redundancies identified
- [ ] Diversification scored
- [ ] Recommendations provided
</success_criteria>
