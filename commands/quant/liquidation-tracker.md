---
name: quant:liquidation-tracker
description: Track large liquidations in the market
allowed-tools:
  - Bash
  - Read
---

<objective>
Monitor liquidation events for market sentiment signals.
</objective>

<process>

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== LIQUIDATION DATA ==="
if [ -f "rl_engine/liquidation_cache.json" ]; then
  cat rl_engine/liquidation_cache.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
liqs = data.get('liquidations', data.get('data', []))
print(f'Total events: {len(liqs)}')
for l in liqs[:10]:
    print(f\"{l.get('symbol')}: \${l.get('value', l.get('amount', 0)):,.0f} {l.get('side', '')}\")"
else
  echo "No liquidation cache found"
fi
```

</process>
