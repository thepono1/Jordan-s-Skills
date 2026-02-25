---
name: quant:recent-errors
description: Show recent errors from trading logs
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== RECENT ERRORS (Local) ==="
find efg_paper_trading/logs -name "*.log" -mtime -1 2>/dev/null | while read f; do
  errors=$(grep -c -i "error\|exception\|fail" "$f" 2>/dev/null || echo 0)
  if [ "$errors" -gt 0 ]; then
    echo "--- $f ($errors errors) ---"
    grep -i "error\|exception\|fail" "$f" | tail -5
  fi
done

echo ""
echo "=== L2 System Errors ==="
grep -i "error" /tmp/l2_system.log 2>/dev/null | tail -5 || echo "No recent errors"
```
</process>
