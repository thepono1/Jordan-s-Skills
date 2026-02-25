---
name: quant:strategy-enabler
description: Enable or disable strategies in manifest
argument-hint: [enable|disable] [strategy-name]
allowed-tools:
  - Bash
  - Read
  - Edit
---

<objective>
Toggle strategies on/off without manual JSON editing.
</objective>

<process>

## 1. List Current Status

```bash
cd ~/Developer/quant_master/quant_v4
cat efg_paper_trading/deployment_manifest.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for s in data.get('strategies', [])[:20]:
    status = 'ON' if s.get('enabled', True) else 'OFF'
    print(f'[{status}] {s.get(\"name\")}')"
```

## 2. Toggle Strategy

```bash
cd ~/Developer/quant_master/quant_v4
python3 << EOF
import json

with open('efg_paper_trading/deployment_manifest.json', 'r') as f:
    data = json.load(f)

for s in data.get('strategies', []):
    if '$STRATEGY' in s.get('name', ''):
        s['enabled'] = $ENABLED  # True or False
        print(f"Set {s['name']} to {'enabled' if $ENABLED else 'disabled'}")

with open('efg_paper_trading/deployment_manifest.json', 'w') as f:
    json.dump(data, f, indent=2)
EOF
```

</process>
