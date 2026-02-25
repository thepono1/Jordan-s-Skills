---
name: quant:log-parser
description: Parse and analyze trading system logs for errors and patterns
argument-hint: [log-type|search-term]
allowed-tools:
  - Bash
  - Read
  - Grep
  - AskUserQuestion
---

<objective>
Parse trading system logs to find errors, warnings, patterns, and recent activity. Provides instant diagnosis of issues.
</objective>

<context>
Log locations:
- Local: `efg_paper_trading/logs/beast.log`
- VPS: `/var/log/enhanced-trader/` or journalctl
</context>

<process>

## 1. Determine Log Source

If no $ARGUMENTS:
- Check local logs by default
- Offer: errors, warnings, recent, trades, [custom search]

Options:
- `errors` - Show recent errors
- `warnings` - Show warnings
- `recent` - Last 100 lines
- `trades` - Trade execution logs
- `vps` - VPS logs
- `[term]` - Search for specific term

## 2. Execute Log Query

### errors
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== RECENT ERRORS ==="
grep -i "error\|exception\|failed\|traceback" efg_paper_trading/logs/beast.log 2>/dev/null | tail -30
```

### warnings
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== RECENT WARNINGS ==="
grep -i "warning\|warn\|caution" efg_paper_trading/logs/beast.log 2>/dev/null | tail -30
```

### recent
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== LAST 100 LINES ==="
tail -100 efg_paper_trading/logs/beast.log 2>/dev/null
```

### trades
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== TRADE ACTIVITY ==="
grep -i "trade\|order\|position\|entry\|exit" efg_paper_trading/logs/beast.log 2>/dev/null | tail -50
```

### vps
```bash
echo "=== VPS LOGS (enhanced-trader) ==="
ssh quantpod "journalctl -u enhanced-trader -n 100 --no-pager" 2>/dev/null
```

### custom search
```bash
cd ~/Developer/quant_master/quant_v4
grep -i "$SEARCH_TERM" efg_paper_trading/logs/beast.log 2>/dev/null | tail -50
```

## 3. Error Analysis

If errors found:
1. Group by error type
2. Count occurrences
3. Show most recent timestamp
4. Suggest possible causes

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== ERROR SUMMARY ==="
grep -i "error\|exception" efg_paper_trading/logs/beast.log 2>/dev/null | \
  sed 's/.*\(Error\|Exception\)/\1/' | \
  sort | uniq -c | sort -rn | head -10
```

## 4. Present Results

Format:

```
# Log Analysis

## Summary
- Time Range: [first to last log entry]
- Errors Found: [N]
- Warnings Found: [N]

## Error Types
| Error | Count | Last Seen |
|-------|-------|-----------|
| [type] | [N] | [time] |

## Recent Issues
[List of recent errors with context]

## Recommendations
- [Suggested fixes]
```

</process>

<success_criteria>
- [ ] Correct log source identified
- [ ] Errors/warnings extracted
- [ ] Patterns identified
- [ ] Clear recommendations provided
</success_criteria>
