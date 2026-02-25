---
name: quant:regime-history
description: View historical market regime data
argument-hint: [today|week|month]
allowed-tools:
  - Bash
  - Read
---

<objective>
Historical view of market regime transitions. Understand regime patterns over time.
</objective>

<process>

## 1. Parse Period

Default: last 7 days

Options:
- `today` - Today's regime changes
- `week` - Last 7 days
- `month` - Last 30 days

## 2. Get Regime History

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== REGIME HISTORY ==="

sqlite3 -header -column data/social_sentiment.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  regime,
  confidence,
  ROUND(sentiment_score, 2) as sentiment
FROM regime_state
WHERE timestamp > strftime('%s', 'now', '-7 days')
ORDER BY timestamp DESC
LIMIT 50" 2>/dev/null || echo "No regime history available"
```

## 3. Regime Duration Analysis

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== REGIME DURATION ==="

sqlite3 data/social_sentiment.db "
SELECT
  regime,
  COUNT(*) as occurrences,
  ROUND(AVG(duration_hours), 1) as avg_duration_hours
FROM (
  SELECT
    regime,
    (LEAD(timestamp) OVER (ORDER BY timestamp) - timestamp) / 3600.0 as duration_hours
  FROM regime_state
  WHERE timestamp > strftime('%s', 'now', '-30 days')
)
WHERE duration_hours IS NOT NULL
GROUP BY regime
ORDER BY occurrences DESC" 2>/dev/null
```

## 4. Regime vs Performance

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== REGIME PERFORMANCE ==="

# This would require joining regime data with trades
python3 << 'EOF'
import sqlite3

try:
    conn_sentiment = sqlite3.connect('data/social_sentiment.db')
    conn_trading = sqlite3.connect('efg_paper_trading/trading.db')

    # Get regimes
    regimes = conn_sentiment.execute('''
        SELECT timestamp, regime FROM regime_state
        ORDER BY timestamp
    ''').fetchall()

    if regimes:
        print("Trade performance by regime coming soon...")
        print(f"Regimes tracked: {len(regimes)}")
except Exception as e:
    print(f"Analysis not available: {e}")
EOF
```

## 5. Present Results

```
# Regime History

## Recent Transitions
| Time | From | To | Duration |
|------|------|-----|----------|

## Statistics (30d)
| Regime | Count | Avg Duration |
|--------|-------|--------------|
| NEUTRAL | 45 | 8.2h |
| OPTIMISM | 20 | 4.1h |

## Current
- Regime: [current]
- Since: [timestamp]
- Duration: [hours]
```

</process>

<success_criteria>
- [ ] History retrieved
- [ ] Transitions tracked
- [ ] Duration analyzed
- [ ] Patterns identified
</success_criteria>
