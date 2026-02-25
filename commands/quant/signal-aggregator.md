---
name: quant:signal-aggregator
description: View combined signals from all data sources
argument-hint: [current|breakdown|history]
allowed-tools:
  - Bash
  - Read
---

<objective>
Aggregated view of all trading signals. Combined view from 35 data providers.
</objective>

<process>

## 1. Get Current Aggregated Signal

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== AGGREGATED SIGNAL ==="

# Try master edge
python3 -c "
import sys
sys.path.insert(0, 'integrations')
try:
    from master_edge import get_aggregated_signal
    signal = get_aggregated_signal()
    print(f'Direction: {signal.get(\"direction\", \"N/A\")}')
    print(f'Strength: {signal.get(\"strength\", \"N/A\")}')
    print(f'Confidence: {signal.get(\"confidence\", \"N/A\")}')
except Exception as e:
    print(f'Could not get signal: {e}')
" 2>/dev/null || echo "Master edge not available"
```

## 2. Signal Breakdown by Source

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== SIGNAL BREAKDOWN ==="

# Check master edge report
if [ -f "rl_engine/master_edge_report.json" ]; then
  cat rl_engine/master_edge_report.json | python3 -c "
import json, sys
data = json.load(sys.stdin)

signals = data.get('signals', data.get('sources', []))
print(f'Total sources: {len(signals)}')
print()
print(f'{\"Source\":<20} {\"Signal\":<10} {\"Confidence\":<10}')
print('-' * 45)
for s in signals[:15]:
    name = s.get('source', s.get('name', 'unknown'))[:18]
    signal = s.get('signal', s.get('direction', 'N/A'))
    conf = s.get('confidence', 'N/A')
    print(f'{name:<20} {str(signal):<10} {str(conf):<10}')
  " 2>/dev/null
else
  echo "No master edge report found"
fi
```

## 3. Signal History

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== RECENT SIGNALS ==="

# Check for signal log
if [ -f "data/signal_history.db" ]; then
  sqlite3 -header -column data/signal_history.db "
  SELECT
    datetime(timestamp, 'unixepoch', 'localtime') as time,
    symbol,
    direction,
    strength
  FROM signals
  ORDER BY timestamp DESC
  LIMIT 10"
fi
```

## 4. Present Results

```
# Signal Aggregator

## Current Signal
- Direction: [LONG/SHORT/NEUTRAL]
- Strength: [0-100]
- Confidence: [0-100]

## Source Breakdown
| Source | Signal | Confidence | Weight |
|--------|--------|------------|--------|
| sentiment | LONG | 75% | 25% |
| technical | SHORT | 60% | 35% |
| l2_flow | LONG | 80% | 20% |

## Consensus
- Bullish sources: [N]
- Bearish sources: [N]
- Neutral: [N]

## Recommendation
- [based on aggregate signal]
```

</process>

<success_criteria>
- [ ] Aggregated signal retrieved
- [ ] Source breakdown shown
- [ ] History available
- [ ] Clear recommendation
</success_criteria>
