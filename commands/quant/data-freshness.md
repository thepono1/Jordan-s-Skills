---
name: quant:data-freshness
description: Detect stale data across all sources
allowed-tools:
  - Bash
  - Read
---

<objective>
Verify data freshness across all feeds and caches. Detect stale data before it affects trading.
</objective>

<process>

## 1. Check Cache Files

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CACHE FRESHNESS ==="

for cache in rl_engine/*_cache.json data/*_cache.json; do
  if [ -f "$cache" ]; then
    age_mins=$(( ($(date +%s) - $(stat -f %m "$cache")) / 60 ))
    name=$(basename "$cache")
    if [ $age_mins -lt 60 ]; then
      status="OK"
    elif [ $age_mins -lt 360 ]; then
      status="STALE"
    else
      status="OLD"
    fi
    printf "%-30s %5dm ago  [%s]\n" "$name" "$age_mins" "$status"
  fi
done 2>/dev/null
```

## 2. Check Database Records

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== DATABASE FRESHNESS ==="

# Trading DB
echo "Trading data:"
sqlite3 efg_paper_trading/trading.db "
SELECT
  'Last trade' as metric,
  datetime(MAX(timestamp), 'unixepoch', 'localtime') as value,
  ROUND((julianday('now') - julianday(datetime(MAX(timestamp), 'unixepoch'))) * 24 * 60, 0) as mins_ago
FROM trades" 2>/dev/null

# L2 DB
echo ""
echo "L2 data:"
sqlite3 efg_paper_trading/state/l2_data.db "
SELECT
  symbol,
  datetime(MAX(timestamp), 'unixepoch', 'localtime') as last_update,
  ROUND((julianday('now') - julianday(datetime(MAX(timestamp), 'unixepoch'))) * 24 * 60, 0) as mins_ago
FROM order_book
GROUP BY symbol" 2>/dev/null || echo "L2 data not available"
```

## 3. Check Sentiment Data

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== SENTIMENT FRESHNESS ==="

sqlite3 data/social_sentiment.db "
SELECT
  'Regime' as source,
  datetime(MAX(timestamp), 'unixepoch', 'localtime') as last_update,
  ROUND((julianday('now') - julianday(datetime(MAX(timestamp), 'unixepoch'))) * 24 * 60, 0) as mins_ago
FROM regime_state" 2>/dev/null || echo "Sentiment data not available"
```

## 4. Integration Data

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== INTEGRATION DATA ==="

# Check master edge report
if [ -f "rl_engine/master_edge_report.json" ]; then
  age_mins=$(( ($(date +%s) - $(stat -f %m "rl_engine/master_edge_report.json")) / 60 ))
  echo "Master Edge Report: ${age_mins}m ago"
fi
```

## 5. Freshness Summary

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== FRESHNESS SUMMARY ==="

python3 << 'EOF'
import os
import json
from datetime import datetime

issues = []

# Check cache files
for cache in ['rl_engine/market_intel_cache.json', 'rl_engine/liquidation_cache.json']:
    if os.path.exists(cache):
        age_mins = (datetime.now().timestamp() - os.path.getmtime(cache)) / 60
        if age_mins > 60:
            issues.append(f"{os.path.basename(cache)}: {age_mins:.0f}m old")

if issues:
    print("Issues found:")
    for i in issues:
        print(f"  - {i}")
else:
    print("All data sources fresh")

EOF
```

## 6. Present Results

```
# Data Freshness

## Status: [ALL FRESH / ISSUES FOUND]

## By Source
| Source | Last Update | Status |
|--------|-------------|--------|
| Trading DB | 5m ago | OK |
| L2 Feed | 30s ago | OK |
| Sentiment | 15m ago | OK |
| Caches | varies | OK |

## Issues
- [any stale sources]

## Recommendations
- [restart feeds if stale]
- [check integration health]
```

</process>

<success_criteria>
- [ ] All sources checked
- [ ] Stale data identified
- [ ] Clear status
- [ ] Actions suggested
</success_criteria>
