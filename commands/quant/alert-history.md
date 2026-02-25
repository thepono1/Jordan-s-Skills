---
name: quant:alert-history
description: Search past alerts and notifications
argument-hint: [search-term|today|week]
allowed-tools:
  - Bash
  - Read
  - Grep
---

<objective>
Search historical alerts. Find past notifications, patterns, and alert frequency.
</objective>

<process>

## 1. Parse Query

Default: today's alerts

Options:
- `today` - Today's alerts
- `week` - Last 7 days
- `[term]` - Search for specific term
- `critical` - Critical alerts only

## 2. Query Alerts

### Today's Alerts
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== TODAY'S ALERTS ==="

# Check alert log
if [ -f "data/alerts.log" ]; then
  grep "$(date +%Y-%m-%d)" data/alerts.log | tail -50
else
  echo "No alerts.log found"
fi

# Check database if exists
sqlite3 data/alerts.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  level,
  substr(message, 1, 60) as message
FROM alerts
WHERE date(timestamp, 'unixepoch') = date('now')
ORDER BY timestamp DESC
LIMIT 50" 2>/dev/null || echo "No alerts database"
```

### Search Term
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== SEARCH: $TERM ==="
grep -i "$TERM" data/alerts.log 2>/dev/null | tail -30 || echo "No matches"

sqlite3 data/alerts.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  level,
  message
FROM alerts
WHERE message LIKE '%$TERM%'
ORDER BY timestamp DESC
LIMIT 30" 2>/dev/null
```

## 3. Alert Statistics

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== ALERT STATISTICS ==="

sqlite3 data/alerts.db "
SELECT
  level,
  COUNT(*) as count,
  MAX(datetime(timestamp, 'unixepoch', 'localtime')) as last_seen
FROM alerts
WHERE timestamp > strftime('%s', 'now', '-7 days')
GROUP BY level
ORDER BY count DESC" 2>/dev/null || echo "No statistics available"
```

## 4. Present Results

```
# Alert History

## Recent Alerts
| Time | Level | Message |
|------|-------|---------|

## Statistics (7d)
- Critical: [N]
- Warning: [N]
- Info: [N]

## Patterns
- Most common: [type]
- Peak time: [hour]
```

</process>

<success_criteria>
- [ ] Alerts retrieved
- [ ] Search executed
- [ ] Statistics calculated
- [ ] Patterns identified
</success_criteria>
