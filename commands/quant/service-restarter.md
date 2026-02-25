---
name: quant:service-restarter
description: Restart trading services on VPS
argument-hint: [service-name]
allowed-tools:
  - Bash
---

<process>
```bash
echo "=== VPS SERVICE RESTARTER ==="
echo "Available services:"
ssh quantpod "systemctl list-units --type=service --state=running | grep -E 'alpha|trader|unified'" 2>/dev/null

echo ""
echo "To restart a service, run:"
echo "  ssh quantpod 'systemctl restart <service-name>'"
```
</process>
