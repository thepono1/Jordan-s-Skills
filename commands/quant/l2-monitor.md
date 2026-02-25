---
name: quant:l2-monitor
description: Monitor L2 order book health and depth
argument-hint: [status|depth|spread|history]
allowed-tools:
  - Bash
  - Read
---

<objective>
Monitor L2 order book data health, depth, and spread metrics. Essential for market microstructure analysis.
</objective>

<context>
L2 Database: efg_paper_trading/state/l2_data.db
L2 System: efg_paper_trading/l2_system/
</context>

<process>

## 1. Check L2 System Status

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== L2 SYSTEM STATUS ==="

# Check if L2 process running
if pgrep -f "l2_system\|l2_archiver" > /dev/null; then
  pid=$(pgrep -f "l2_system")
  echo "L2 System: RUNNING (PID: $pid)"
else
  echo "L2 System: STOPPED"
fi

# Check database
if [ -f "efg_paper_trading/state/l2_data.db" ]; then
  size=$(ls -lh efg_paper_trading/state/l2_data.db | awk '{print $5}')
  echo "L2 Database: $size"
else
  echo "L2 Database: NOT FOUND"
fi
```

## 2. Check Data Freshness

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== DATA FRESHNESS ==="
sqlite3 efg_paper_trading/state/l2_data.db "
SELECT
  symbol,
  datetime(MAX(timestamp), 'unixepoch', 'localtime') as last_update,
  ROUND((julianday('now') - julianday(datetime(MAX(timestamp), 'unixepoch'))) * 24 * 60, 1) as mins_ago,
  COUNT(*) as records_24h
FROM order_book
WHERE timestamp > strftime('%s', 'now', '-24 hours')
GROUP BY symbol
ORDER BY last_update DESC" 2>/dev/null || echo "No L2 data available"
```

## 3. Current Spread Analysis

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== CURRENT SPREAD ==="
sqlite3 efg_paper_trading/state/l2_data.db "
SELECT
  symbol,
  ROUND(best_ask - best_bid, 2) as spread,
  ROUND((best_ask - best_bid) / best_bid * 100, 4) as spread_pct,
  ROUND(best_bid, 2) as bid,
  ROUND(best_ask, 2) as ask
FROM (
  SELECT
    symbol,
    MAX(CASE WHEN side = 'bid' THEN price END) as best_bid,
    MIN(CASE WHEN side = 'ask' THEN price END) as best_ask
  FROM order_book
  WHERE timestamp = (SELECT MAX(timestamp) FROM order_book)
  GROUP BY symbol
)" 2>/dev/null || echo "Spread data not available"
```

## 4. Order Book Depth

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== ORDER BOOK DEPTH ==="
sqlite3 efg_paper_trading/state/l2_data.db "
SELECT
  symbol,
  side,
  COUNT(*) as levels,
  ROUND(SUM(quantity), 4) as total_qty,
  ROUND(SUM(quantity * price), 2) as total_value
FROM order_book
WHERE timestamp = (SELECT MAX(timestamp) FROM order_book)
GROUP BY symbol, side
ORDER BY symbol, side" 2>/dev/null || echo "Depth data not available"
```

## 5. Present Results

```
# L2 Order Book Monitor

## System Status
- L2 Feed: [RUNNING/STOPPED]
- Database: [size]
- Last Update: [time]

## Current Market
| Symbol | Bid | Ask | Spread | Spread% |
|--------|-----|-----|--------|---------|
| ETH/USD | 3200.50 | 3200.75 | 0.25 | 0.008% |

## Depth
| Symbol | Side | Levels | Volume |
|--------|------|--------|--------|
| ETH/USD | bid | 25 | 150.5 |
| ETH/USD | ask | 25 | 145.2 |

## Health
- Data Freshness: [OK/STALE]
- Spread: [NORMAL/WIDE]
```

</process>

<success_criteria>
- [ ] L2 system status verified
- [ ] Data freshness checked
- [ ] Spread calculated
- [ ] Depth analyzed
</success_criteria>
