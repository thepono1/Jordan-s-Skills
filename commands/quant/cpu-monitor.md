---
name: quant:cpu-monitor
description: Monitor CPU usage of trading processes
allowed-tools:
  - Bash
---

<process>
```bash
echo "=== LOCAL CPU USAGE ==="
ps aux --sort=-%cpu | grep -E "python|node" | grep -v grep | head -10 | awk '{printf "PID:%-6s CPU:%5s%% MEM:%5s%% %s\n", $2, $3, $4, $11}'

echo ""
echo "=== VPS CPU USAGE ==="
ssh quantpod "uptime && echo '' && ps aux --sort=-%cpu | grep python | head -5" 2>/dev/null || echo "Cannot connect to VPS"
```
</process>
