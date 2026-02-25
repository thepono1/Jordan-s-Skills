---
name: quant:alert-test
description: Test alert channels (Slack, Pushover, etc)
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== ALERT CHANNEL TEST ==="

echo "Testing Slack webhook..."
if [ -n "$SLACK_WEBHOOK_URL" ]; then
  curl -s -X POST "$SLACK_WEBHOOK_URL" -H 'Content-type: application/json' \
    --data '{"text":"🧪 Test alert from quant system"}' && echo " Slack: OK"
else
  echo "SLACK_WEBHOOK_URL not set"
fi

echo ""
echo "Alert endpoints configured in .env:"
grep -E "SLACK|PUSHOVER|DISCORD" .env 2>/dev/null | cut -d= -f1 || echo "No alert config found"
```
</process>
