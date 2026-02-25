---
name: quant:parameter-tuner
description: Adjust strategy parameters without editing JSON directly
argument-hint: [strategy] [param] [value]
allowed-tools:
  - Bash
  - Read
  - Edit
  - AskUserQuestion
---

<objective>
Tune strategy parameters interactively. Adjust without directly editing JSON files.
</objective>

<process>

## 1. List Strategies

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== AVAILABLE STRATEGIES ==="
cat efg_paper_trading/deployment_manifest.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
strategies = data.get('strategies', [])
for i, s in enumerate(strategies[:20], 1):
    name = s.get('name', 'unnamed')
    enabled = 'ON' if s.get('enabled', True) else 'OFF'
    print(f'{i}. [{enabled}] {name}')
"
```

## 2. Show Strategy Parameters

If strategy selected:
```bash
cd ~/Developer/quant_master/quant_v4
cat efg_paper_trading/deployment_manifest.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
strategies = data.get('strategies', [])
for s in strategies:
    if '$STRATEGY' in s.get('name', ''):
        print(f\"Strategy: {s.get('name')}\")
        print(f\"Enabled: {s.get('enabled', True)}\")
        params = s.get('params', s.get('parameters', {}))
        print('Parameters:')
        for k, v in params.items():
            print(f'  {k}: {v}')
        break
"
```

## 3. Interactive Parameter Edit

Use AskUserQuestion to get:
- Which parameter to change
- New value

## 4. Apply Change

```bash
cd ~/Developer/quant_master/quant_v4

# Backup first
cp efg_paper_trading/deployment_manifest.json efg_paper_trading/deployment_manifest.json.bak

# Apply change
python3 << EOF
import json

with open('efg_paper_trading/deployment_manifest.json', 'r') as f:
    data = json.load(f)

for s in data.get('strategies', []):
    if '$STRATEGY' in s.get('name', ''):
        params = s.get('params', s.get('parameters', {}))
        params['$PARAM'] = $VALUE
        s['params'] = params
        print(f"Updated {s['name']}: $PARAM = $VALUE")
        break

with open('efg_paper_trading/deployment_manifest.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Saved successfully")
EOF
```

## 5. Validate & Confirm

```bash
cd ~/Developer/quant_master/quant_v4
python3 -c "import json; json.load(open('efg_paper_trading/deployment_manifest.json'))" && echo "Validation: OK" || echo "Validation: FAILED"
```

## 6. Present Results

```
# Parameter Tuner

## Change Applied
- Strategy: [name]
- Parameter: [param]
- Old Value: [old]
- New Value: [new]

## Validation
- JSON: OK
- Backup: [path]

## Next Steps
- Restart paper trader to apply
- Monitor performance after change
```

</process>

<success_criteria>
- [ ] Strategy identified
- [ ] Parameter located
- [ ] Backup created
- [ ] Change validated
</success_criteria>
