---
name: quant:discord-poster
description: Discord updates
argument-hint: [message]
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
source .env 2>/dev/null
curl -s -H "Content-Type: application/json" \
  -d "{\"content\": \"$1\"}" \
  "$DISCORD_WEBHOOK" && echo "Discord sent"
```
</process>
