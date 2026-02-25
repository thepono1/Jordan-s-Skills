---
name: quant:runpod-monitor
description: Monitor RunPod GPU usage and costs
argument-hint: [status|cost|jobs]
allowed-tools:
  - Bash
  - Read
  - WebFetch
---

<objective>
Monitor RunPod GPU instances, training jobs, and costs.
</objective>

<process>

## 1. Check RunPod Status

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== RUNPOD STATUS ==="

# Check if runpodctl is installed
if command -v runpodctl &> /dev/null; then
  runpodctl get pods 2>/dev/null || echo "RunPod CLI not configured"
else
  echo "runpodctl not installed"
  echo "Install: pip install runpodctl"
fi
```

## 2. Check Local Training Results

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== RECENT TRAINING RESULTS ==="

if [ -d "trained_models_runpod" ]; then
  ls -lt trained_models_runpod/ | head -10
else
  echo "No trained models directory"
fi

if [ -d "runpod_results" ]; then
  echo ""
  echo "Latest results:"
  ls -lt runpod_results/ | head -5
fi
```

## 3. Training Job Status

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== TRAINING JOB STATUS ==="

# Check for running training processes
ps aux | grep -E "train_finrl|gpu_parameter|continuous_learning" | grep -v grep || echo "No local training processes"

# Check deployment scripts
if [ -f "runpod_deployment/continuous_learning_pipeline.py" ]; then
  echo "Continuous learning pipeline: Available"
fi
```

## 4. Cost Tracking

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== COST ESTIMATE ==="

# Check if we have cost tracking
if [ -f "data/runpod_costs.json" ]; then
  cat data/runpod_costs.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f\"This month: \${data.get('month_cost', 0):.2f}\")
print(f\"Total usage: {data.get('gpu_hours', 0):.1f} GPU hours\")
  " 2>/dev/null
else
  echo "Cost tracking not configured"
  echo "Typical costs:"
  echo "  - RTX 3090: ~$0.40/hr"
  echo "  - A100: ~$1.50/hr"
fi
```

## 5. Present Results

```
# RunPod Monitor

## Active Pods
| Pod ID | GPU | Status | Uptime |
|--------|-----|--------|--------|

## Recent Training
- Last job: [timestamp]
- Model: [name]
- Duration: [hours]

## Costs
- This Month: $[X]
- GPU Hours: [N]

## Recommendations
- [any idle pods to terminate]
- [training opportunities]
```

</process>

<success_criteria>
- [ ] Pod status checked
- [ ] Training results found
- [ ] Costs estimated
- [ ] Recommendations provided
</success_criteria>
