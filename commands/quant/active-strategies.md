---
name: quant:active-strategies
description: List currently active trading strategies
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== ACTIVE STRATEGIES ==="
if [ -f "efg_paper_trading/deployment_manifest.json" ]; then
  cat efg_paper_trading/deployment_manifest.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
strategies = data.get('strategies', [])
enabled = [s for s in strategies if s.get('enabled', False)]
print(f'Total: {len(strategies)} | Enabled: {len(enabled)}')
print()
for s in enabled[:15]:
    print(f\"  {s.get('name', 'unknown')}: {s.get('symbol', '?')} {s.get('side', '?')}\")
"
else
  echo "No deployment_manifest.json found"
fi
```
</process>
