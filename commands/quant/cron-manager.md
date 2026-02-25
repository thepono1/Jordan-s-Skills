---
name: quant:cron-manager
description: View and manage scheduled cron jobs
allowed-tools:
  - Bash
---

<process>
```bash
echo "=== LOCAL CRON JOBS ==="
crontab -l 2>/dev/null || echo "No local cron jobs"

echo ""
echo "=== VPS CRON JOBS ==="
ssh quantpod "crontab -l" 2>/dev/null || echo "Cannot connect to VPS"

echo ""
echo "=== SYSTEMD TIMERS (VPS) ==="
ssh quantpod "systemctl list-timers --no-pager" 2>/dev/null | head -15 || echo "Cannot list timers"
```
</process>
