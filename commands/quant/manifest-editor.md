---
name: quant:manifest-editor
description: View and edit deployment manifest configuration
argument-hint: [show|edit|strategies|risk|backup]
allowed-tools:
  - Bash
  - Read
  - Edit
  - AskUserQuestion
---

<objective>
Safe configuration changes to deployment_manifest.json. View and modify strategy settings, risk parameters, and system config.
</objective>

<context>
Manifest: efg_paper_trading/deployment_manifest.json
Contains: Active strategies, risk limits, position sizing, pairs config
</context>

<process>

## 1. Parse Command

Default: show

Commands:
- `show` - Display current manifest
- `strategies` - List active strategies
- `risk` - Show risk parameters
- `edit` - Guided edit mode
- `backup` - Backup before changes

## 2. Execute Command

### show
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== DEPLOYMENT MANIFEST ==="
cat efg_paper_trading/deployment_manifest.json | python3 -m json.tool
```

### strategies
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== ACTIVE STRATEGIES ==="
cat efg_paper_trading/deployment_manifest.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
strategies = data.get('strategies', [])
print(f'Total: {len(strategies)} strategies')
print()
for i, s in enumerate(strategies[:20], 1):
    name = s.get('name', 'unnamed')
    enabled = s.get('enabled', True)
    status = 'ON' if enabled else 'OFF'
    print(f'{i}. [{status}] {name}')
if len(strategies) > 20:
    print(f'... and {len(strategies) - 20} more')
"
```

### risk
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== RISK PARAMETERS ==="
cat efg_paper_trading/deployment_manifest.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
risk = data.get('risk_management', data.get('risk', {}))
print(f\"Max Daily Loss: \${risk.get('max_daily_loss', 'N/A')}\")
print(f\"Max Drawdown: {risk.get('max_drawdown_pct', 'N/A')}%\")
print(f\"Max Position Size: \${risk.get('max_position_size', 'N/A')}\")
print(f\"Stop Loss: {risk.get('stop_loss_pct', 'N/A')}%\")
print(f\"Position Size (% of capital): {risk.get('position_size_pct', 'N/A')}%\")

capital = data.get('capital', data.get('portfolio', {}).get('capital', 'N/A'))
print(f\"Capital: \${capital}\")
"
```

### backup
```bash
cd ~/Developer/quant_master/quant_v4
BACKUP="efg_paper_trading/deployment_manifest.json.bak.$(date +%Y%m%d_%H%M%S)"
cp efg_paper_trading/deployment_manifest.json "$BACKUP"
echo "Backed up to: $BACKUP"
```

### edit
First backup, then use AskUserQuestion to determine what to change:
- Enable/disable strategy
- Update risk parameter
- Change capital
- Modify position sizing

After user input, read the manifest file and use Edit tool to make changes.

## 3. Validate Changes

After any edit:
```bash
cd ~/Developer/quant_master/quant_v4
python3 -c "
import json
with open('efg_paper_trading/deployment_manifest.json', 'r') as f:
    data = json.load(f)
print('Manifest valid JSON: OK')
print(f'Strategies: {len(data.get(\"strategies\", []))}')
" && echo "Validation: PASSED" || echo "Validation: FAILED - restore backup!"
```

## 4. Present Results

```
# Manifest Editor

## Current Config
- Strategies: [N] active, [M] disabled
- Capital: $[X]
- Max Daily Loss: $[X]
- Position Size: [X]%

## Changes Made
- [list of changes]

## Backup
- [backup location if created]

## Next Steps
- Restart paper trader to apply changes
```

</process>

<success_criteria>
- [ ] Current config displayed
- [ ] Backup created before changes
- [ ] Edits validated
- [ ] Restart reminder provided
</success_criteria>
