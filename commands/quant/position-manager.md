---
name: quant:position-manager
description: View and manage open trading positions
argument-hint: [list|close|details|symbol]
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

<objective>
View open positions, get position details, and manage position lifecycle. Core visibility into current trading exposure.
</objective>

<process>

## 1. Parse Command

Default: list all open positions

Commands:
- `list` - Show all open positions
- `details [id]` - Show detailed position info
- `close [id]` - Mark position for closure
- `[symbol]` - Show positions for symbol

## 2. Execute Command

### list (default)
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== OPEN POSITIONS ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  id,
  symbol,
  strategy_name,
  side,
  quantity,
  entry_price,
  datetime(entry_time, 'unixepoch', 'localtime') as entry_time,
  ROUND((julianday('now') - julianday(datetime(entry_time, 'unixepoch'))) * 24, 1) as hours_held
FROM positions
WHERE status='OPEN'
ORDER BY entry_time DESC"
```

### details [id]
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT *
FROM positions
WHERE id = $ID"
```

### by symbol
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  id,
  strategy_name,
  side,
  quantity,
  entry_price,
  datetime(entry_time, 'unixepoch', 'localtime') as entry_time
FROM positions
WHERE status='OPEN' AND symbol LIKE '%$SYMBOL%'
ORDER BY entry_time DESC"
```

## 3. Position Metrics

Calculate for each position:
```bash
cd ~/Developer/quant_master/quant_v4
sqlite3 efg_paper_trading/trading.db "
SELECT
  symbol,
  SUM(CASE WHEN side='BUY' THEN quantity ELSE -quantity END) as net_exposure,
  COUNT(*) as position_count,
  SUM(quantity * entry_price) as total_notional
FROM positions
WHERE status='OPEN'
GROUP BY symbol"
```

## 4. Present Results

Format:

```
# Open Positions

## Summary
- Total Positions: [N]
- Symbols: [list]
- Net Exposure: [by symbol]

## Positions
| ID | Symbol | Strategy | Side | Qty | Entry | Held |
|----|--------|----------|------|-----|-------|------|
| 1 | ETH/USD | momentum_15m | BUY | 0.1 | 3200 | 2.5h |

## Exposure
| Symbol | Long | Short | Net |
|--------|------|-------|-----|
| ETH/USD | 0.5 | 0.2 | +0.3 |
```

</process>

<success_criteria>
- [ ] All open positions retrieved
- [ ] Exposure calculated correctly
- [ ] Position age displayed
- [ ] Clear summary provided
</success_criteria>
