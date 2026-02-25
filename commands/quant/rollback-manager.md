---
name: quant:rollback-manager
description: Quick config revert to previous state
argument-hint: [list|restore|diff]
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

<objective>
Quickly restore previous configuration when changes cause issues.
</objective>

<process>

## 1. List Available Backups

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== AVAILABLE BACKUPS ==="

# Manifest backups
echo "Manifest backups:"
ls -lt efg_paper_trading/deployment_manifest.json.bak* 2>/dev/null | head -5

# Full backups
echo ""
echo "Full backups:"
ls -ltd backups/*/ 2>/dev/null | head -5
```

## 2. Show Diff (if requested)

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CHANGES FROM BACKUP ==="

if [ -f "efg_paper_trading/deployment_manifest.json.bak" ]; then
  diff efg_paper_trading/deployment_manifest.json.bak efg_paper_trading/deployment_manifest.json | head -30
else
  echo "No backup to compare"
fi
```

## 3. Restore from Backup

If restore confirmed:
```bash
cd ~/Developer/quant_master/quant_v4

# Create safety backup of current
cp efg_paper_trading/deployment_manifest.json efg_paper_trading/deployment_manifest.json.pre_rollback

# Restore
cp "$BACKUP_FILE" efg_paper_trading/deployment_manifest.json

echo "Restored from: $BACKUP_FILE"
echo "Previous saved to: deployment_manifest.json.pre_rollback"
```

## 4. Validate Restored Config

```bash
cd ~/Developer/quant_master/quant_v4
python3 -c "
import json
with open('efg_paper_trading/deployment_manifest.json', 'r') as f:
    data = json.load(f)
print(f'Strategies: {len(data.get(\"strategies\", []))}')
print('Validation: OK')
" || echo "Validation: FAILED"
```

## 5. Present Results

```
# Rollback Manager

## Available Backups
| File | Date | Size |
|------|------|------|
| manifest.json.bak.20260122_100000 | Jan 22 | 5.2KB |

## Action
- [Restored from X / Listed backups / Showed diff]

## Current State
- Config valid: OK
- Strategies: [N]

## Next Steps
- Restart paper trader if restored
- Verify behavior after restart
```

</process>

<success_criteria>
- [ ] Backups listed
- [ ] Diff shown if requested
- [ ] Restore executed safely
- [ ] Validation passed
</success_criteria>
