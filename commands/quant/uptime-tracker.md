---
name: quant:uptime-tracker
description: Service availability history
allowed-tools:
  - Bash
---

<process>
```bash
echo "=== UPTIME STATUS ==="
uptime
echo ""
ssh quantpod "uptime" 2>/dev/null || echo "VPS: unreachable"
```
</process>
