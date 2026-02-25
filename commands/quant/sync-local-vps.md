---
name: quant:sync-local-vps
description: Sync files between local and VPS
argument-hint: [to-vps|from-vps|status]
allowed-tools:
  - Bash
---

<objective>
Keep local and VPS environments aligned.
</objective>

<process>

## Check Diff

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== FILES DIFFERENT FROM VPS ==="
rsync -avzn --exclude '.git' --exclude '__pycache__' --exclude '*.db' \
  ./ quantpod:/root/quant_v4/ 2>&1 | grep -E "^[<>]|sending"
```

## To VPS

```bash
cd ~/Developer/quant_master/quant_v4
rsync -avz --exclude '.git' --exclude '__pycache__' --exclude '*.db' \
  ./ quantpod:/root/quant_v4/
```

## From VPS

```bash
cd ~/Developer/quant_master/quant_v4
rsync -avz --exclude '.git' --exclude '__pycache__' --exclude '*.db' \
  quantpod:/root/quant_v4/ ./
```

</process>
