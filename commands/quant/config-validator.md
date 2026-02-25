---
name: quant:config-validator
description: Validate configuration files for errors
argument-hint: [manifest|env|all]
allowed-tools:
  - Bash
  - Read
---

<objective>
Catch configuration errors before they cause runtime issues. Validate JSON, environment variables, and settings.
</objective>

<process>

## 1. Validate Manifest JSON

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== MANIFEST VALIDATION ==="

if [ -f "efg_paper_trading/deployment_manifest.json" ]; then
  python3 -c "
import json
import sys

try:
    with open('efg_paper_trading/deployment_manifest.json', 'r') as f:
        data = json.load(f)
    print('JSON Syntax: OK')

    # Check required fields
    required = ['strategies', 'capital']
    missing = [f for f in required if f not in data and f not in data.get('portfolio', {})]
    if missing:
        print(f'Missing fields: {missing}')
    else:
        print('Required fields: OK')

    # Validate strategies
    strategies = data.get('strategies', [])
    print(f'Strategies: {len(strategies)} defined')

    # Check for duplicate strategy names
    names = [s.get('name') for s in strategies]
    dupes = set([n for n in names if names.count(n) > 1])
    if dupes:
        print(f'Duplicate strategies: {dupes}')
    else:
        print('No duplicates: OK')

    # Validate risk settings
    risk = data.get('risk_management', data.get('risk', {}))
    if risk:
        print(f'Risk config: OK')
    else:
        print('Risk config: MISSING')

except json.JSONDecodeError as e:
    print(f'JSON Syntax: INVALID - {e}')
except Exception as e:
    print(f'Validation error: {e}')
  "
else
  echo "Manifest not found"
fi
```

## 2. Validate Environment Variables

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== ENVIRONMENT VALIDATION ==="

if [ -f ".env" ]; then
  # Check for required vars
  required_vars="KRAKEN_API_KEY KRAKEN_PRIVATE_KEY"

  for var in $required_vars; do
    if grep -q "^${var}=" .env; then
      # Check if value is not empty
      value=$(grep "^${var}=" .env | cut -d= -f2)
      if [ -n "$value" ]; then
        echo "$var: SET"
      else
        echo "$var: EMPTY"
      fi
    else
      echo "$var: MISSING"
    fi
  done

  # Check for common mistakes
  if grep -q "your_api_key\|YOUR_KEY\|xxx" .env; then
    echo "WARNING: Placeholder values detected in .env"
  fi

else
  echo ".env file not found"
fi
```

## 3. Validate Other Configs

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== OTHER CONFIG FILES ==="

# Check pair params
if [ -f "config/pair_params.json" ]; then
  python3 -c "import json; json.load(open('config/pair_params.json'))" && echo "pair_params.json: OK" || echo "pair_params.json: INVALID"
fi

# Check trading configs
if [ -f "trading_configs.json" ]; then
  python3 -c "import json; json.load(open('trading_configs.json'))" && echo "trading_configs.json: OK" || echo "trading_configs.json: INVALID"
fi
```

## 4. Cross-Validation

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== CROSS VALIDATION ==="

python3 << 'EOF'
import json
import os

# Check capital consistency
manifest_capital = None
if os.path.exists('efg_paper_trading/deployment_manifest.json'):
    with open('efg_paper_trading/deployment_manifest.json') as f:
        data = json.load(f)
        manifest_capital = data.get('capital', data.get('portfolio', {}).get('capital'))

if manifest_capital:
    print(f"Manifest capital: ${manifest_capital}")

    # Check if positions exceed capital
    import sqlite3
    try:
        conn = sqlite3.connect('efg_paper_trading/trading.db')
        exposure = conn.execute('''
            SELECT SUM(quantity * entry_price)
            FROM positions WHERE status='OPEN'
        ''').fetchone()[0] or 0

        if exposure > manifest_capital:
            print(f"WARNING: Exposure ${exposure:.2f} exceeds capital ${manifest_capital}")
        else:
            print(f"Exposure check: OK (${exposure:.2f} / ${manifest_capital})")
        conn.close()
    except:
        pass

EOF
```

## 5. Present Results

```
# Configuration Validation

## Status
| Config | Status | Issues |
|--------|--------|--------|
| manifest.json | OK | None |
| .env | OK | None |
| pair_params.json | OK | None |

## Warnings
- [any warnings]

## Errors
- [any errors that must be fixed]

## Recommendations
- [suggested fixes]
```

</process>

<success_criteria>
- [ ] JSON syntax validated
- [ ] Required fields checked
- [ ] Env vars verified
- [ ] Cross-validation done
</success_criteria>
