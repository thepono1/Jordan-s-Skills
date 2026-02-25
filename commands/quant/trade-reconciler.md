---
name: quant:trade-reconciler
description: Reconcile local trades with exchange records
argument-hint: [check|sync|report]
allowed-tools:
  - Bash
  - Read
---

<objective>
Match local trade records with exchange data. Detect discrepancies and ensure accuracy.
</objective>

<process>

## 1. Get Local Trades

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== LOCAL TRADE RECORDS ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  id,
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  side,
  quantity,
  price,
  ROUND(pnl, 2) as pnl
FROM trades
WHERE timestamp > strftime('%s', 'now', '-24 hours')
ORDER BY timestamp DESC
LIMIT 20"
```

## 2. Get Exchange Trades (Paper Trading Mode)

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== RECONCILIATION STATUS ==="

# For paper trading, we reconcile against our own signals
python3 << 'EOF'
import sqlite3

conn = sqlite3.connect('efg_paper_trading/trading.db')

# Count trades by status
stats = conn.execute('''
    SELECT
        'Total trades (24h)' as metric,
        COUNT(*) as value
    FROM trades
    WHERE timestamp > strftime('%s', 'now', '-24 hours')
    UNION ALL
    SELECT
        'With position ID',
        COUNT(*)
    FROM trades
    WHERE timestamp > strftime('%s', 'now', '-24 hours')
    AND position_id IS NOT NULL
    UNION ALL
    SELECT
        'Without position ID (orphan)',
        COUNT(*)
    FROM trades
    WHERE timestamp > strftime('%s', 'now', '-24 hours')
    AND position_id IS NULL
''').fetchall()

for metric, value in stats:
    print(f"{metric}: {value}")

conn.close()
EOF
```

## 3. Check Position-Trade Consistency

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== POSITION-TRADE CONSISTENCY ==="

sqlite3 efg_paper_trading/trading.db "
SELECT
  'Open positions' as check_type,
  COUNT(*) as count
FROM positions
WHERE status = 'OPEN'
UNION ALL
SELECT
  'Positions with no entry trade',
  COUNT(*)
FROM positions p
WHERE NOT EXISTS (
  SELECT 1 FROM trades t
  WHERE t.position_id = p.id AND t.side = p.side
)
AND p.status = 'OPEN'
UNION ALL
SELECT
  'Closed positions with no exit trade',
  COUNT(*)
FROM positions p
WHERE p.status = 'CLOSED'
AND NOT EXISTS (
  SELECT 1 FROM trades t
  WHERE t.position_id = p.id AND t.side != p.side
)" 2>/dev/null
```

## 4. PnL Reconciliation

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== PNL RECONCILIATION ==="

python3 << 'EOF'
import sqlite3

conn = sqlite3.connect('efg_paper_trading/trading.db')

# Compare position PnL vs trade PnL
result = conn.execute('''
    SELECT
        ROUND(SUM(t.pnl), 2) as trade_pnl,
        ROUND(SUM(p.realized_pnl), 2) as position_pnl
    FROM trades t
    LEFT JOIN positions p ON t.position_id = p.id
    WHERE t.timestamp > strftime('%s', 'now', '-7 days')
''').fetchone()

trade_pnl = result[0] or 0
position_pnl = result[1] or 0
diff = abs(trade_pnl - position_pnl)

print(f"Trade PnL (7d): ${trade_pnl}")
print(f"Position PnL (7d): ${position_pnl}")
print(f"Difference: ${diff}")
print(f"Status: {'OK' if diff < 1 else 'DISCREPANCY DETECTED'}")

conn.close()
EOF
```

## 5. Present Results

```
# Trade Reconciliation

## Summary
- Local Trades (24h): [N]
- Exchange Trades (24h): [N] (paper mode)
- Matched: [N]
- Discrepancies: [N]

## Issues Found
- [list any discrepancies]

## PnL Check
- Calculated PnL: $[X]
- Recorded PnL: $[X]
- Difference: $[X]

## Recommendations
- [any fixes needed]
```

</process>

<success_criteria>
- [ ] Local records retrieved
- [ ] Consistency checked
- [ ] PnL reconciled
- [ ] Discrepancies reported
</success_criteria>
