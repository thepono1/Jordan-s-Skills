---
name: quant:db-explorer
description: Explore database schema and structure
argument-hint: [database-name]
allowed-tools:
  - Bash
---

<objective>
Schema discovery - tables, columns, relationships.
</objective>

<process>

```bash
cd ~/Developer/quant_master/quant_v4
DB="${1:-efg_paper_trading/trading.db}"
echo "=== DATABASE: $DB ==="

echo "Tables:"
sqlite3 "$DB" ".tables"

echo ""
echo "Schema:"
sqlite3 "$DB" ".schema" | head -50

echo ""
echo "Row counts:"
for table in $(sqlite3 "$DB" ".tables"); do
  count=$(sqlite3 "$DB" "SELECT COUNT(*) FROM $table")
  echo "  $table: $count rows"
done
```

</process>
