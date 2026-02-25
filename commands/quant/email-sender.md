---
name: quant:email-sender
description: Email reports
argument-hint: [subject] [body]
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
python3 -c "
from notifications.email_sender import send_email
send_email('$SUBJECT', '$BODY')
print('Email sent')
" 2>/dev/null || echo "Email not configured"
```
</process>
