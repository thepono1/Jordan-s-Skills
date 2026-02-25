---
name: quant:pushover-sender
description: Mobile push alerts
argument-hint: [message]
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
source .env 2>/dev/null
curl -s -X POST https://api.pushover.net/1/messages.json \
  -d "token=$PUSHOVER_TOKEN" \
  -d "user=$PUSHOVER_USER" \
  -d "message=$1" && echo "Push sent"
```
</process>
