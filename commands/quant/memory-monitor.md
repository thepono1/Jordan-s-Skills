---
name: quant:memory-monitor
description: Monitor memory usage of trading processes
allowed-tools:
  - Bash
---

<process>
```bash
echo "=== LOCAL MEMORY USAGE ==="
ps aux --sort=-%mem | grep -E "python|node" | grep -v grep | head -10 | awk '{printf "%-8s %5s%% %5s%% %s\n", $2, $3, $4, $11}'

echo ""
echo "=== VPS MEMORY USAGE ==="
ssh quantpod "free -h && echo '' && ps aux --sort=-%mem | head -10" 2>/dev/null || echo "Cannot connect to VPS"
```
</process>
