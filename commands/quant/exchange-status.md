---
name: quant:exchange-status
description: Kraken health check
allowed-tools:
  - Bash
---

<process>
```bash
echo "=== KRAKEN STATUS ==="
start=$(date +%s%N)
curl -s -o /dev/null -w "HTTP: %{http_code}\n" https://api.kraken.com/0/public/Time
end=$(date +%s%N)
echo "Latency: $(( (end - start) / 1000000 ))ms"
```
</process>
