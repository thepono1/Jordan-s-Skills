---
name: quant:price-feed
description: Real-time price alerts
argument-hint: [symbol]
allowed-tools:
  - Bash
---

<process>
```bash
curl -s "https://api.kraken.com/0/public/Ticker?pair=ETHUSD,XBTUSD" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for pair, info in data.get('result', {}).items():
    price = info.get('c', ['N/A'])[0]
    print(f'{pair}: \${float(price):,.2f}')"
```
</process>
