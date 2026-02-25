---
name: quant:model-registry
description: Track and manage ML models
argument-hint: [list|info|deploy]
allowed-tools:
  - Bash
  - Read
---

<objective>
Track trained ML models, versions, and deployment status.
</objective>

<process>

## 1. List Models

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== TRAINED MODELS ==="

# Check trained_models directories
for dir in trained_models_runpod trained_models models; do
  if [ -d "$dir" ]; then
    echo ""
    echo "[$dir]"
    ls -lt "$dir"/*.pkl "$dir"/*.pt "$dir"/*.h5 2>/dev/null | head -5 || echo "  (no models)"
  fi
done
```

## 2. Model Details

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== MODEL METADATA ==="

# Check for model registry
if [ -f "data/model_registry.json" ]; then
  cat data/model_registry.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for model in data.get('models', [])[:10]:
    print(f\"{model.get('name')}: v{model.get('version')} - {model.get('status')}\")
  " 2>/dev/null
else
  echo "No model registry found"

  # Try to infer from files
  echo ""
  echo "Detected model files:"
  find . -name "*.pkl" -o -name "*.pt" -o -name "*.h5" 2>/dev/null | head -10
fi
```

## 3. Currently Deployed

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== DEPLOYED MODELS ==="

# Check manifest for active models
cat efg_paper_trading/deployment_manifest.json 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
models = data.get('models', data.get('ml_models', []))
if models:
    for m in models:
        print(f\"  {m.get('name', m)}: {m.get('status', 'active')}\")
else:
    print('  No ML models in manifest')
" 2>/dev/null || echo "Could not read manifest"
```

## 4. Present Results

```
# Model Registry

## Available Models
| Model | Version | Trained | Size |
|-------|---------|---------|------|

## Deployed
- Active: [list]
- Staged: [list]

## Recent Training
- Last trained: [date]
- Next scheduled: [date]
```

</process>

<success_criteria>
- [ ] Models listed
- [ ] Versions tracked
- [ ] Deployment status clear
</success_criteria>
