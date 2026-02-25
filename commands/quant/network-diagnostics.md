---
name: quant:network-diagnostics
description: Network connectivity troubleshooting
allowed-tools:
  - Bash
---

<objective>
Diagnose network connectivity issues with exchanges, VPS, and data providers.
</objective>

<process>

## 1. Check Internet Connectivity

```bash
echo "=== INTERNET CONNECTIVITY ==="
ping -c 3 8.8.8.8 2>&1 | tail -3
```

## 2. Check Exchange Connectivity

```bash
echo ""
echo "=== EXCHANGE CONNECTIVITY ==="

# Kraken API
curl -s -o /dev/null -w "Kraken API: %{http_code} (%{time_total}s)\n" https://api.kraken.com/0/public/Time

# Kraken WebSocket
curl -s -o /dev/null -w "Kraken WS: %{http_code} (%{time_total}s)\n" https://ws.kraken.com/ 2>/dev/null || echo "Kraken WS: connection test skipped"
```

## 3. Check VPS Connectivity

```bash
echo ""
echo "=== VPS CONNECTIVITY ==="

# Ping VPS
ping -c 3 69.169.111.9 2>&1 | tail -3

# SSH test
timeout 5 ssh quantpod "echo 'SSH: OK'" 2>/dev/null || echo "SSH: FAILED or TIMEOUT"
```

## 4. DNS Resolution

```bash
echo ""
echo "=== DNS RESOLUTION ==="
nslookup api.kraken.com 2>/dev/null | grep -A1 "Name:" || echo "DNS lookup completed"
```

## 5. Port Connectivity

```bash
echo ""
echo "=== PORT CHECKS ==="

# Check common ports
nc -z -w5 api.kraken.com 443 && echo "Kraken 443: OPEN" || echo "Kraken 443: BLOCKED"
nc -z -w5 69.169.111.9 22 && echo "VPS SSH 22: OPEN" || echo "VPS SSH 22: BLOCKED"
```

## 6. Latency Check

```bash
echo ""
echo "=== LATENCY ==="

# Kraken latency
start=$(python3 -c "import time; print(time.time())")
curl -s https://api.kraken.com/0/public/Time > /dev/null
end=$(python3 -c "import time; print(time.time())")
latency=$(python3 -c "print(f'{($end - $start) * 1000:.0f}ms')")
echo "Kraken API latency: $latency"

# VPS latency
ssh_latency=$(ping -c 5 69.169.111.9 2>/dev/null | tail -1 | awk -F'/' '{print $5}')
echo "VPS ping latency: ${ssh_latency}ms"
```

## 7. Present Results

```
# Network Diagnostics

## Connectivity
| Endpoint | Status | Latency |
|----------|--------|---------|
| Internet | OK | - |
| Kraken API | OK | 150ms |
| Kraken WS | OK | - |
| VPS (quantpod) | OK | 45ms |

## DNS
- Resolution: OK

## Issues Found
- [any issues]

## Recommendations
- [if issues found]
```

</process>

<success_criteria>
- [ ] Internet tested
- [ ] Exchanges reachable
- [ ] VPS accessible
- [ ] Latency measured
</success_criteria>
