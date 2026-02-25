---
name: quant:fear-greed-tracker
description: Track Fear & Greed index
allowed-tools:
  - Bash
  - WebFetch
---

<objective>
Market sentiment via Fear & Greed index.
</objective>

<process>

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== FEAR & GREED INDEX ==="

# Check cache
if [ -f "data/fear_greed_cache.json" ]; then
  cat data/fear_greed_cache.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f\"Value: {data.get('value', 'N/A')}\")
print(f\"Classification: {data.get('classification', 'N/A')}\")
print(f\"Updated: {data.get('timestamp', 'N/A')}\")"
else
  echo "No Fear & Greed data cached"
  echo "Fetch from alternative.me/crypto/fear-and-greed-index/"
fi
```

</process>
