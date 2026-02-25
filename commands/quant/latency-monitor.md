---
name: quant:latency-monitor
description: Monitor API and WebSocket latency
allowed-tools:
  - Bash
---

<process>
```bash
echo "=== LATENCY MONITORING ==="
echo "Kraken API ping:"
time curl -s "https://api.kraken.com/0/public/Time" > /dev/null

echo ""
echo "VPS latency:"
ping -c 3 69.169.111.9 2>/dev/null | tail -1 || echo "VPS unreachable"

echo ""
echo "=== WebSocket Status ==="
ps aux | grep -E "websocket|l2_system" | grep -v grep | head -5
```
</process>
