---
name: quant:vps-manager
description: Manage VPS services and check status
argument-hint: [status|restart|logs|service-name]
allowed-tools:
  - Bash
  - AskUserQuestion
---

<objective>
Manage VPS (quantpod) services: check status, restart services, view logs, and troubleshoot issues.
</objective>

<context>
VPS: quantpod (69.169.111.9)
Services:
- alpha-chat-api.service
- alpha-control-api.service
- alpha-dashboard-api.service
- alpha-dashboard.service
- enhanced-trader.service
- monday-trader.service
- unified-alpha-mm.service
</context>

<process>

## 1. Parse Command

If no $ARGUMENTS, show status of all services.

Commands:
- `status` - Show all service statuses
- `restart [service]` - Restart specific service
- `restart all` - Restart all trading services
- `logs [service]` - View recent logs
- `[service-name]` - Show specific service status

## 2. Execute Command

### status (default)
```bash
echo "=== VPS SERVICE STATUS ==="
ssh quantpod "
systemctl list-units --type=service --state=running | grep -E 'alpha|trader|dashboard' | while read line; do
  service=\$(echo \$line | awk '{print \$1}')
  echo \"\$service: RUNNING\"
done

systemctl list-units --type=service --state=failed | grep -E 'alpha|trader|dashboard' | while read line; do
  service=\$(echo \$line | awk '{print \$1}')
  echo \"\$service: FAILED\"
done
"
```

### restart [service]
```bash
ssh quantpod "systemctl restart $SERVICE && systemctl status $SERVICE --no-pager | head -10"
```

### restart all
```bash
ssh quantpod "
for svc in enhanced-trader alpha-dashboard alpha-dashboard-api alpha-control-api alpha-chat-api monday-trader unified-alpha-mm; do
  systemctl restart \$svc 2>/dev/null && echo \"\$svc: RESTARTED\" || echo \"\$svc: NOT FOUND\"
done
"
```

### logs [service]
```bash
ssh quantpod "journalctl -u $SERVICE -n 50 --no-pager"
```

## 3. Health Checks

After any restart, verify:
```bash
ssh quantpod "sleep 2 && systemctl is-active $SERVICE"
```

## 4. Present Results

Format:

```
# VPS Status

| Service | Status | Uptime |
|---------|--------|--------|
| enhanced-trader | RUNNING | 2d 5h |
| alpha-dashboard | RUNNING | 2d 5h |
...

[Any actions taken]
[Any issues found]
```

</process>

<success_criteria>
- [ ] VPS connection established
- [ ] Service status retrieved
- [ ] Any requested actions completed
- [ ] Results clearly presented
</success_criteria>
