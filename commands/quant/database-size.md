---
name: quant:database-size
description: Check sizes of all trading databases
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== DATABASE SIZES ==="
find . -name "*.db" -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $9}' | sort -hr | head -20

echo ""
echo "=== TABLE COUNTS ==="
for db in efg_paper_trading/trading.db efg_paper_trading/state/l2_data.db data/unified_alpha_v4.db; do
  if [ -f "$db" ]; then
    echo "--- $db ---"
    sqlite3 "$db" "SELECT name, (SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=m.name) FROM sqlite_master m WHERE type='table'" 2>/dev/null | head -10
  fi
done
```
</process>
