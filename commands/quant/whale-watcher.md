---
name: quant:whale-watcher
description: Monitor large order flow and whale movements
argument-hint: [current|alerts|history]
allowed-tools:
  - Bash
  - Read
---

<objective>
Track large transactions and whale movements from L2 data.
</objective>

<process>

## 1. Check Recent Large Orders

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== RECENT LARGE ORDERS ==="

sqlite3 -header -column efg_paper_trading/state/l2_data.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  side,
  quantity,
  price,
  ROUND(quantity * price, 2) as value
FROM order_book
WHERE quantity * price > 10000
AND timestamp > strftime('%s', 'now', '-24 hours')
ORDER BY quantity * price DESC
LIMIT 20" 2>/dev/null || echo "No L2 data available"
```

## 2. Whale Activity Summary

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== WHALE ACTIVITY (24h) ==="

sqlite3 efg_paper_trading/state/l2_data.db "
SELECT
  side,
  COUNT(*) as large_orders,
  ROUND(SUM(quantity), 4) as total_qty,
  ROUND(SUM(quantity * price), 2) as total_value
FROM order_book
WHERE quantity * price > 10000
AND timestamp > strftime('%s', 'now', '-24 hours')
GROUP BY side" 2>/dev/null || echo "No whale data"
```

## 3. Net Flow

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== NET WHALE FLOW ==="

sqlite3 efg_paper_trading/state/l2_data.db "
SELECT
  symbol,
  ROUND(SUM(CASE WHEN side = 'bid' THEN quantity * price ELSE 0 END), 2) as buy_flow,
  ROUND(SUM(CASE WHEN side = 'ask' THEN quantity * price ELSE 0 END), 2) as sell_flow,
  ROUND(
    SUM(CASE WHEN side = 'bid' THEN quantity * price ELSE -quantity * price END),
    2
  ) as net_flow
FROM order_book
WHERE quantity * price > 10000
AND timestamp > strftime('%s', 'now', '-24 hours')
GROUP BY symbol" 2>/dev/null
```

## 4. Whale Alerts

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== WHALE ALERTS ==="

# Check for very large orders (>$50k)
sqlite3 efg_paper_trading/state/l2_data.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  symbol,
  side,
  ROUND(quantity * price, 0) as value_usd
FROM order_book
WHERE quantity * price > 50000
AND timestamp > strftime('%s', 'now', '-1 hour')
ORDER BY timestamp DESC" 2>/dev/null || echo "No recent whale alerts"
```

## 5. Present Results

```
# Whale Watcher

## Recent Large Orders (>$10k)
| Time | Symbol | Side | Value |
|------|--------|------|-------|

## Net Flow (24h)
- Buy Flow: $[X]
- Sell Flow: $[X]
- Net: $[X] ([bullish/bearish])

## Whale Activity
- Large buys: [N] ($[X])
- Large sells: [N] ($[X])

## Signal
- [interpretation based on flow]
```

</process>

<success_criteria>
- [ ] Large orders detected
- [ ] Net flow calculated
- [ ] Alerts surfaced
- [ ] Signal interpretation
</success_criteria>
