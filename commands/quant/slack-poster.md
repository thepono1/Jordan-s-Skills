---
name: quant:slack-poster
description: Post quick alerts and messages to Slack
argument-hint: [message] --channel [channel]
allowed-tools:
  - Bash
  - Read
---

<objective>
Quick Slack message posting for alerts and updates. No context switching needed.
</objective>

<context>
Default channel: #trading-alerts
Slack integration: notifications/slack_notifier.py
</context>

<process>

## 1. Parse Message

Extract from $ARGUMENTS:
- Message content
- Channel (optional, default: #trading-alerts)
- Priority (optional: normal, urgent)

## 2. Format Message

```bash
cd ~/Developer/quant_master/quant_v4
# Prepare message with timestamp
MESSAGE="$ARGUMENTS"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
```

## 3. Send to Slack

```bash
cd ~/Developer/quant_master/quant_v4

# Method 1: Use existing notifier
python3 -c "
import sys
sys.path.insert(0, 'notifications')
try:
    from slack_notifier import send_slack_message
    send_slack_message('$MESSAGE')
    print('Message sent via notifier')
except Exception as e:
    print(f'Notifier failed: {e}')
" 2>/dev/null || (

# Method 2: Direct webhook if notifier fails
WEBHOOK_URL=\$(grep SLACK_WEBHOOK .env 2>/dev/null | cut -d= -f2)
if [ -n \"\$WEBHOOK_URL\" ]; then
  curl -s -X POST -H 'Content-type: application/json' \
    --data \"{\\\"text\\\": \\\"[\$TIMESTAMP] \$MESSAGE\\\"}\" \
    \"\$WEBHOOK_URL\" && echo "Message sent via webhook"
else
  echo "No Slack webhook configured"
fi
)
```

## 4. Log Message

```bash
cd ~/Developer/quant_master/quant_v4
echo "[$TIMESTAMP] $MESSAGE" >> data/slack_log.txt
```

## 5. Confirm

```
Message Posted:
- Channel: [channel]
- Time: [timestamp]
- Content: [message preview]
```

</process>

<success_criteria>
- [ ] Message parsed
- [ ] Sent to correct channel
- [ ] Logged locally
- [ ] Confirmation provided
</success_criteria>
