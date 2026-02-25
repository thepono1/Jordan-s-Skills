---
name: quant:imessage-sender
description: Send critical alerts via iMessage
argument-hint: [message] --to [phone]
allowed-tools:
  - Bash
---

<objective>
Send critical mobile alerts via iMessage for immediate attention.
</objective>

<context>
Default recipients:
- Singapore: +65 89456242
- UK: +447532722082
</context>

<process>

## 1. Parse Message

Extract from $ARGUMENTS:
- Message content
- Recipient (optional, default: Singapore number)

## 2. Send iMessage

```bash
MESSAGE="$ARGUMENTS"
PHONE="${PHONE:-+65 89456242}"
TIMESTAMP=$(date '+%H:%M')

# Send via AppleScript
osascript << EOF
tell application "Messages"
    set targetBuddy to "$PHONE"
    set targetService to id of 1st account whose service type = iMessage
    set targetMessage to "[$TIMESTAMP] $MESSAGE"
    send targetMessage to participant targetBuddy of account id targetService
end tell
EOF

if [ $? -eq 0 ]; then
  echo "iMessage sent to $PHONE"
else
  echo "Failed to send iMessage"
fi
```

## 3. Log Alert

```bash
cd ~/Developer/quant_master/quant_v4
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [iMessage] [$PHONE] $MESSAGE" >> data/alerts.log
```

## 4. Confirm

```
iMessage Alert Sent:
- To: [phone]
- Message: [preview]
- Time: [timestamp]
```

</process>

<success_criteria>
- [ ] Message parsed
- [ ] iMessage sent
- [ ] Logged locally
- [ ] Confirmation displayed
</success_criteria>
