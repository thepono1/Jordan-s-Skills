---
name: quant:api-rate-limiter
description: Check API rate limit status
argument-hint: [status|reset|history]
allowed-tools:
  - Bash
  - Read
---

<objective>
Monitor API rate limits to prevent throttling. Track usage across exchanges and data providers.
</objective>

<process>

## 1. Check Kraken Rate Limits

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== KRAKEN API STATUS ==="

# Kraken has call rate limits based on API tier
# Basic: 15 calls / 3 seconds
# Intermediate: 20 calls / 2 seconds

# Check recent API calls from logs
if [ -f "efg_paper_trading/logs/beast.log" ]; then
  api_calls_1m=$(grep -c "kraken.*api\|API.*call" efg_paper_trading/logs/beast.log 2>/dev/null | tail -1 || echo "0")
  echo "Recent API activity detected in logs"
fi

# Test current limit status
python3 << 'EOF'
import requests
import time

start = time.time()
try:
    r = requests.get('https://api.kraken.com/0/public/Time', timeout=5)
    if r.status_code == 200:
        print(f"Kraken API: OK ({(time.time()-start)*1000:.0f}ms)")
    elif r.status_code == 429:
        print("Kraken API: RATE LIMITED")
    else:
        print(f"Kraken API: {r.status_code}")
except Exception as e:
    print(f"Kraken API: Error - {e}")
EOF
```

## 2. Check Other Providers

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== OTHER API STATUS ==="

# Check for rate limit tracking
if [ -f "data/rate_limits.json" ]; then
  cat data/rate_limits.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for provider, info in data.items():
    used = info.get('used', 0)
    limit = info.get('limit', 'N/A')
    print(f'{provider}: {used}/{limit}')
  " 2>/dev/null
else
  echo "Rate limit tracking not configured"
fi
```

## 3. API Call History

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== API CALL HISTORY (1h) ==="

# Count API-related log entries
if [ -f "efg_paper_trading/logs/beast.log" ]; then
  echo "Log entries with API/request mentions:"
  grep -c -i "api\|request\|fetch" efg_paper_trading/logs/beast.log 2>/dev/null | tail -1 || echo "0"
fi
```

## 4. Present Results

```
# API Rate Limiter

## Current Status
| Provider | Used | Limit | Status |
|----------|------|-------|--------|
| Kraken | OK | 15/3s | GOOD |

## Recommendations
- [any throttling risks]
- [optimization suggestions]
```

</process>

<success_criteria>
- [ ] Rate limits checked
- [ ] Usage tracked
- [ ] Throttling risks identified
</success_criteria>
