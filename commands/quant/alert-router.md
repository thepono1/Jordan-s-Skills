---
name: quant:alert-router
description: Route alerts to appropriate channels based on severity
argument-hint: [message] --level [critical|warning|info]
allowed-tools:
  - Bash
  - Read
---

<objective>
Route alerts to appropriate notification channels based on severity. Triage without context switching.
</objective>

<context>
Alert Channels:
- iMessage: Critical alerts (Singapore: +65 89456242)
- Slack: All alerts
- Console: Logged locally
</context>

<process>

## 1. Parse Alert

Extract from $ARGUMENTS:
- Message content
- Level: critical, warning, info (default: info)

## 2. Determine Routing

| Level | Channels |
|-------|----------|
| critical | iMessage + Slack + Console |
| warning | Slack + Console |
| info | Console only |

## 3. Send Alerts

### Console (always)
```bash
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$LEVEL] $MESSAGE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$LEVEL] $MESSAGE" >> ~/Developer/quant_master/quant_v4/data/alerts.log
```

### Slack (warning+)
```bash
cd ~/Developer/quant_master/quant_v4
python -c "
from notifications.slack_notifier import send_slack_message
send_slack_message('$MESSAGE', level='$LEVEL')
" 2>/dev/null || echo "Slack notification failed"
```

### iMessage (critical only)
```bash
osascript -e 'tell application "Messages" to send "$MESSAGE" to buddy "+65 89456242"' 2>/dev/null || echo "iMessage failed"
```

## 4. Log Alert

```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 data/alerts.db "
CREATE TABLE IF NOT EXISTS alerts (
  id INTEGER PRIMARY KEY,
  timestamp INTEGER,
  level TEXT,
  message TEXT,
  channels TEXT
);
INSERT INTO alerts (timestamp, level, message, channels)
VALUES (strftime('%s', 'now'), '$LEVEL', '$MESSAGE', '$CHANNELS');"
```

## 5. Confirm

```
Alert Sent:
- Level: [LEVEL]
- Message: [MESSAGE]
- Channels: [list of channels used]
- Time: [timestamp]
```

</process>

<success_criteria>
- [ ] Alert level determined
- [ ] Correct channels selected
- [ ] All channels notified
- [ ] Alert logged
</success_criteria>
