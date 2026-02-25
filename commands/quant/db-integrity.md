---
name: quant:db-integrity
description: Check database integrity and catch corruption early
allowed-tools:
  - Bash
---

<objective>
Verify database integrity across all trading databases. Catch corruption before it causes problems.
</objective>

<process>

## 1. Check All Databases

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== DATABASE INTEGRITY CHECK ==="

# List of databases to check
DBS=(
  "efg_paper_trading/trading.db"
  "data/unified_alpha_v4.db"
  "data/strategy_validation.db"
  "data/circuit_breaker.db"
  "data/social_sentiment.db"
  "efg_paper_trading/state/l2_data.db"
)

for db in "${DBS[@]}"; do
  if [ -f "$db" ]; then
    result=$(sqlite3 "$db" "PRAGMA integrity_check" 2>&1)
    if [ "$result" = "ok" ]; then
      size=$(ls -lh "$db" | awk '{print $5}')
      echo "$db: OK ($size)"
    else
      echo "$db: CORRUPTED - $result"
    fi
  else
    echo "$db: NOT FOUND"
  fi
done
```

## 2. Check Table Counts

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== TABLE STATISTICS ==="

# Trading DB tables
echo "trading.db:"
sqlite3 efg_paper_trading/trading.db "
SELECT 'trades' as tbl, COUNT(*) as rows FROM trades
UNION ALL SELECT 'positions', COUNT(*) FROM positions
UNION ALL SELECT 'open_positions', (SELECT COUNT(*) FROM positions WHERE status='OPEN')
" 2>/dev/null
```

## 3. Check for Orphaned Data

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== ORPHAN CHECK ==="
sqlite3 efg_paper_trading/trading.db "
SELECT 'Trades without position' as issue, COUNT(*) as count
FROM trades t
WHERE NOT EXISTS (SELECT 1 FROM positions p WHERE p.id = t.position_id)
AND t.position_id IS NOT NULL
" 2>/dev/null || echo "Check skipped"
```

## 4. Vacuum Recommendation

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== VACUUM STATUS ==="
for db in efg_paper_trading/trading.db data/unified_alpha_v4.db; do
  if [ -f "$db" ]; then
    page_count=$(sqlite3 "$db" "PRAGMA page_count")
    freelist=$(sqlite3 "$db" "PRAGMA freelist_count")
    if [ "$freelist" -gt 1000 ]; then
      echo "$db: VACUUM RECOMMENDED (freelist: $freelist pages)"
    else
      echo "$db: OK (freelist: $freelist pages)"
    fi
  fi
done 2>/dev/null
```

## 5. Present Results

```
# Database Integrity Report

## Integrity Status
| Database | Status | Size |
|----------|--------|------|
| trading.db | OK | 2.1M |
| alpha.db | OK | 5.3M |

## Table Counts
- Trades: [N]
- Positions: [N] (Open: [N])

## Issues Found
- [any corruption or orphans]

## Recommendations
- [vacuum if needed]
- [backup if issues found]
```

</process>

<success_criteria>
- [ ] All databases checked
- [ ] Integrity verified
- [ ] Issues identified
- [ ] Recommendations provided
</success_criteria>
