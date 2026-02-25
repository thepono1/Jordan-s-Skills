---
name: quant:drawdown-monitor
description: Monitor current and historical drawdown levels
argument-hint: [current|history|alert]
allowed-tools:
  - Bash
  - Read
---

<objective>
Real-time drawdown awareness. Monitor peak-to-trough declines for risk management.
</objective>

<process>

## 1. Calculate Current Drawdown

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== DRAWDOWN ANALYSIS ==="

python3 << 'EOF'
import sqlite3
from datetime import datetime

conn = sqlite3.connect('efg_paper_trading/trading.db')

# Get all trades ordered by time
trades = conn.execute('''
    SELECT timestamp, pnl
    FROM trades
    ORDER BY timestamp
''').fetchall()

if not trades:
    print("No trades to analyze")
    exit()

# Calculate running equity and drawdown
cumulative = 0
peak = 0
max_dd = 0
max_dd_pct = 0
current_dd = 0

equity_curve = []
for ts, pnl in trades:
    cumulative += pnl
    equity_curve.append((ts, cumulative))
    peak = max(peak, cumulative)
    dd = peak - cumulative
    if peak > 0:
        dd_pct = (dd / peak) * 100
    else:
        dd_pct = 0
    if dd > max_dd:
        max_dd = dd
        max_dd_pct = dd_pct

# Current drawdown
current_peak = peak
current_dd = peak - cumulative
if current_peak > 0:
    current_dd_pct = (current_dd / current_peak) * 100
else:
    current_dd_pct = 0

print(f"Current Equity: ${cumulative:.2f}")
print(f"Peak Equity: ${peak:.2f}")
print(f"Current Drawdown: ${current_dd:.2f} ({current_dd_pct:.1f}%)")
print(f"Max Drawdown: ${max_dd:.2f} ({max_dd_pct:.1f}%)")
print(f"Total Trades: {len(trades)}")

# Today's drawdown
today_trades = conn.execute('''
    SELECT SUM(pnl)
    FROM trades
    WHERE date(timestamp, 'unixepoch') = date('now')
''').fetchone()[0] or 0

today_peak = conn.execute('''
    SELECT MAX(running_total) FROM (
        SELECT SUM(pnl) OVER (ORDER BY timestamp) as running_total
        FROM trades
        WHERE date(timestamp, 'unixepoch') = date('now')
    )
''').fetchone()[0] or 0

print(f"\nToday's PnL: ${today_trades:.2f}")
print(f"Today's Peak: ${today_peak:.2f}")
if today_peak > 0:
    today_dd = today_peak - today_trades
    print(f"Today's DD: ${today_dd:.2f}")

conn.close()
EOF
```

## 2. Drawdown by Period

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== DRAWDOWN BY PERIOD ==="
sqlite3 efg_paper_trading/trading.db "
SELECT
  'Today' as period,
  ROUND(MIN(running), 2) as max_loss,
  ROUND(MAX(running), 2) as max_gain
FROM (
  SELECT SUM(pnl) OVER (ORDER BY timestamp) as running
  FROM trades
  WHERE date(timestamp, 'unixepoch') = date('now')
)
UNION ALL
SELECT
  '7 Days',
  ROUND(MIN(running), 2),
  ROUND(MAX(running), 2)
FROM (
  SELECT SUM(pnl) OVER (ORDER BY timestamp) as running
  FROM trades
  WHERE timestamp > strftime('%s', 'now', '-7 days')
)
UNION ALL
SELECT
  '30 Days',
  ROUND(MIN(running), 2),
  ROUND(MAX(running), 2)
FROM (
  SELECT SUM(pnl) OVER (ORDER BY timestamp) as running
  FROM trades
  WHERE timestamp > strftime('%s', 'now', '-30 days')
)"
```

## 3. Drawdown Alerts

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== ALERT STATUS ==="

# Check thresholds from config
MAX_DD_THRESHOLD=10  # percent
DAILY_LOSS_THRESHOLD=50  # dollars

python3 << EOF
import sqlite3
conn = sqlite3.connect('efg_paper_trading/trading.db')

# Today's loss
today = conn.execute('''
    SELECT COALESCE(SUM(pnl), 0) FROM trades
    WHERE date(timestamp, 'unixepoch') = date('now')
''').fetchone()[0]

if today < -$DAILY_LOSS_THRESHOLD:
    print(f"WARNING: Daily loss ${-today:.2f} exceeds threshold \${$DAILY_LOSS_THRESHOLD}")
else:
    print(f"Daily loss within limits: \${-today:.2f} / \${$DAILY_LOSS_THRESHOLD}")

conn.close()
EOF
```

## 4. Present Results

```
# Drawdown Monitor

## Current State
- Equity: $[X]
- Peak: $[X]
- Drawdown: $[X] ([X]%)
- Status: [OK/WARNING/CRITICAL]

## Historical
| Period | Max DD | Max Gain |
|--------|--------|----------|
| Today | $X | $X |
| Week | $X | $X |
| Month | $X | $X |

## Alerts
- [any triggered alerts]
```

</process>

<success_criteria>
- [ ] Current drawdown calculated
- [ ] Peak equity tracked
- [ ] Alerts evaluated
- [ ] Historical context provided
</success_criteria>
