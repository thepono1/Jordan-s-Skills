---
name: quant:integration-health
description: Check health of all 35 DIY data provider integrations
allowed-tools:
  - Bash
  - Read
  - Glob
---

<objective>
Check all 35 DIY data provider integrations in one command. Verify connections, data freshness, and error rates.
</objective>

<context>
Integration directory: integrations/
Saves: ~$9K/mo vs commercial alternatives
</context>

<process>

## 1. List All Integrations

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== DATA PROVIDER INTEGRATIONS ==="
ls -la integrations/*.py 2>/dev/null | wc -l | xargs -I {} echo "Found {} integration files"
echo ""
ls integrations/*.py 2>/dev/null | xargs -n1 basename | sed 's/.py$//'
```

## 2. Check Master Edge Aggregator

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== MASTER EDGE STATUS ==="
python3 -c "
import sys
sys.path.insert(0, 'integrations')
try:
    from master_edge import get_edge_summary
    summary = get_edge_summary()
    print(f'Status: {summary}')
except Exception as e:
    print(f'Error: {e}')
" 2>/dev/null || echo "Master edge not available"
```

## 3. Check Data Freshness

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== DATA FRESHNESS ==="

# Check cache files
for cache in rl_engine/*_cache.json; do
  if [ -f "$cache" ]; then
    age_mins=$(( ($(date +%s) - $(stat -f %m "$cache")) / 60 ))
    name=$(basename "$cache" _cache.json)
    if [ $age_mins -lt 60 ]; then
      echo "$name: ${age_mins}m ago (OK)"
    else
      echo "$name: ${age_mins}m ago (STALE)"
    fi
  fi
done 2>/dev/null
```

## 4. Check Integration Errors

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== RECENT INTEGRATION ERRORS ==="
grep -l "error\|exception\|failed" efg_paper_trading/logs/*.log 2>/dev/null | while read log; do
  count=$(grep -ci "error\|exception" "$log")
  echo "$(basename $log): $count errors"
done | head -10
```

## 5. Verify Critical Providers

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== CRITICAL PROVIDER STATUS ==="

# Kraken API
python3 -c "
import requests
try:
    r = requests.get('https://api.kraken.com/0/public/Time', timeout=5)
    if r.status_code == 200:
        print('Kraken API: OK')
    else:
        print(f'Kraken API: ERROR {r.status_code}')
except Exception as e:
    print(f'Kraken API: FAILED - {e}')
" 2>/dev/null

# Check local websocket status
pgrep -f "websocket\|ws_" > /dev/null && echo "WebSocket feeds: RUNNING" || echo "WebSocket feeds: NOT DETECTED"
```

## 6. Present Results

```
# Integration Health

## Summary
- Total Integrations: [N]
- Healthy: [N]
- Stale Data: [N]
- Errors: [N]

## Provider Status
| Provider | Status | Last Update | Errors |
|----------|--------|-------------|--------|
| kraken | OK | 2m ago | 0 |
| sentiment | OK | 15m ago | 0 |
| l2_feed | STALE | 2h ago | 3 |

## Action Needed
- [list any providers needing attention]

## Monthly Savings
~$9,000/mo vs commercial alternatives
```

</process>

<success_criteria>
- [ ] All integrations enumerated
- [ ] Data freshness checked
- [ ] Errors identified
- [ ] Critical providers verified
</success_criteria>
