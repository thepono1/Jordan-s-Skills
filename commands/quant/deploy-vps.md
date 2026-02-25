---
name: quant:deploy-vps
description: Deploy code updates to VPS
argument-hint: [sync|restart|full]
allowed-tools:
  - Bash
  - AskUserQuestion
---

<objective>
Push code and config updates to VPS (quantpod).
</objective>

<process>

## 1. Sync Code

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== SYNCING TO VPS ==="
rsync -avz --exclude '.git' --exclude '__pycache__' --exclude '*.db' \
  ./ quantpod:/root/quant_v4/ 2>&1 | tail -20
echo "Sync complete"
```

## 2. Restart Services

```bash
ssh quantpod "systemctl restart enhanced-trader && systemctl status enhanced-trader --no-pager | head -5"
```

## 3. Verify

```bash
ssh quantpod "systemctl is-active enhanced-trader"
```

</process>
