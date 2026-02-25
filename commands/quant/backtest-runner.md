---
name: quant:backtest-runner
description: Run on-demand backtests for strategies
argument-hint: [strategy] --period [7d|30d|90d]
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

<objective>
Run backtests for specific strategies or parameters. On-demand validation before deployment.
</objective>

<context>
Backtest script: backtest_tournament.py
Results: backtest_results.json
</context>

<process>

## 1. Parse Parameters

If no $ARGUMENTS, prompt for:
- Strategy name or "all"
- Time period (default: 30d)
- Symbol (default: ETH/USD)

## 2. Configure Backtest

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== BACKTEST CONFIGURATION ==="
echo "Strategy: $STRATEGY"
echo "Period: $PERIOD"
echo "Symbol: $SYMBOL"
```

## 3. Run Backtest

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== RUNNING BACKTEST ==="

# Check if backtest script exists
if [ -f "backtest_tournament.py" ]; then
  python3 backtest_tournament.py \
    --strategy "$STRATEGY" \
    --period "$PERIOD" \
    --symbol "$SYMBOL" \
    2>&1 | tee /tmp/backtest_output.txt

elif [ -f "strategies/backtest.py" ]; then
  python3 strategies/backtest.py \
    --strategy "$STRATEGY" \
    --days "${PERIOD%d}" \
    2>&1 | tee /tmp/backtest_output.txt

else
  echo "No backtest script found. Creating simple backtest..."

  python3 << EOF
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('efg_paper_trading/trading.db')

# Get historical trades for strategy
trades = conn.execute('''
    SELECT timestamp, pnl, symbol
    FROM trades
    WHERE strategy_name LIKE '%$STRATEGY%'
    ORDER BY timestamp
''').fetchall()

if not trades:
    print("No historical trades found for this strategy")
else:
    total_pnl = sum(t[1] for t in trades)
    wins = sum(1 for t in trades if t[1] > 0)
    win_rate = wins / len(trades) * 100 if trades else 0

    print(f"Strategy: $STRATEGY")
    print(f"Trades: {len(trades)}")
    print(f"Total PnL: \${total_pnl:.2f}")
    print(f"Win Rate: {win_rate:.1f}%")
    print(f"Avg Trade: \${total_pnl/len(trades):.2f}")

conn.close()
EOF
fi
```

## 4. Parse Results

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== BACKTEST RESULTS ==="

if [ -f "backtest_results.json" ]; then
  cat backtest_results.json | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f\"Total Return: {data.get('total_return', 'N/A')}%\")
    print(f\"Sharpe Ratio: {data.get('sharpe', 'N/A')}\")
    print(f\"Max Drawdown: {data.get('max_drawdown', 'N/A')}%\")
    print(f\"Win Rate: {data.get('win_rate', 'N/A')}%\")
    print(f\"Profit Factor: {data.get('profit_factor', 'N/A')}\")
except:
    print('Could not parse results')
  "
fi
```

## 5. Present Results

```
# Backtest Results

## Configuration
- Strategy: [name]
- Period: [dates]
- Symbol: [symbol]

## Performance
- Return: [X]%
- Sharpe: [X]
- Max Drawdown: [X]%
- Win Rate: [X]%
- Profit Factor: [X]

## Trades
- Total: [N]
- Winners: [N]
- Losers: [N]

## Recommendation
- [deploy/review/reject based on metrics]
```

</process>

<success_criteria>
- [ ] Backtest executed
- [ ] Key metrics calculated
- [ ] Results presented clearly
- [ ] Recommendation provided
</success_criteria>
