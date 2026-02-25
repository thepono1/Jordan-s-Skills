---
name: quant:funding-monitor
description: Monitor cryptocurrency funding rates
argument-hint: [current|history|alert]
allowed-tools:
  - Bash
  - Read
  - WebFetch
---

<objective>
Monitor funding rates for funding rate alpha. Extreme funding can signal reversal opportunities.
</objective>

<process>

## 1. Fetch Current Funding Rates

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CURRENT FUNDING RATES ==="

# Check if we have cached data
python3 << 'EOF'
import json
import os
from datetime import datetime

cache_file = 'data/funding_cache.json'

# Try to read from cache first
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        data = json.load(f)
    cache_time = datetime.fromisoformat(data.get('timestamp', '2000-01-01'))
    age_minutes = (datetime.now() - cache_time).total_seconds() / 60

    if age_minutes < 60:  # Cache valid for 1 hour
        print(f"Funding Rates (cached {age_minutes:.0f}m ago):")
        for symbol, rate in data.get('rates', {}).items():
            annual = rate * 3 * 365 * 100  # 8-hour funding to annual %
            print(f"  {symbol}: {rate*100:.4f}% ({annual:.1f}% annualized)")
    else:
        print("Cache expired, fetch fresh data")
else:
    print("No cache found, fetch fresh data")
EOF
```

## 2. Analyze Funding Extremes

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== FUNDING ANALYSIS ==="

python3 << 'EOF'
# Funding thresholds for signals
EXTREME_HIGH = 0.001  # 0.1% per 8h = very bullish crowd
EXTREME_LOW = -0.001  # -0.1% per 8h = very bearish crowd

# These extreme readings often precede reversals
print("Funding Rate Signals:")
print("  > 0.1%: Crowded long - consider short bias")
print("  < -0.1%: Crowded short - consider long bias")
print("  Near 0%: Neutral - no funding edge")
EOF
```

## 3. Historical Funding

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== FUNDING HISTORY (7d) ==="
sqlite3 -header -column data/funding_history.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  ROUND(rate * 100, 4) as rate_pct,
  ROUND(rate * 3 * 365 * 100, 1) as annual_pct
FROM funding_rates
WHERE timestamp > strftime('%s', 'now', '-7 days')
ORDER BY timestamp DESC
LIMIT 20" 2>/dev/null || echo "No funding history database"
```

## 4. Funding Alerts

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== FUNDING ALERTS ==="

python3 << 'EOF'
# Check for extreme funding conditions
import json
import os

cache_file = 'data/funding_cache.json'
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        data = json.load(f)

    alerts = []
    for symbol, rate in data.get('rates', {}).items():
        if rate > 0.001:
            alerts.append(f"HIGH: {symbol} funding {rate*100:.3f}% - shorts get paid")
        elif rate < -0.001:
            alerts.append(f"LOW: {symbol} funding {rate*100:.3f}% - longs get paid")

    if alerts:
        for a in alerts:
            print(a)
    else:
        print("No extreme funding conditions")
else:
    print("Funding data not available")
EOF
```

## 5. Present Results

```
# Funding Monitor

## Current Rates
| Symbol | Rate (8h) | Annualized | Signal |
|--------|-----------|------------|--------|
| ETH/USD | 0.01% | 10.95% | Neutral |
| BTC/USD | 0.03% | 32.85% | Bullish crowd |

## Analysis
- [interpretation of current funding]

## Alerts
- [any extreme conditions]

## Trading Implication
- [how this affects strategy selection]
```

</process>

<success_criteria>
- [ ] Current funding rates displayed
- [ ] Extreme conditions flagged
- [ ] Trading implications noted
- [ ] Historical context provided
</success_criteria>
