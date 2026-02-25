---
name: quant:exposure-monitor
description: Monitor net exposure across positions
argument-hint: [current|history|limits]
allowed-tools:
  - Bash
  - Read
---

<objective>
Check net exposure by symbol and overall. Essential for risk management.
</objective>

<process>

## 1. Calculate Current Exposure

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CURRENT EXPOSURE ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  symbol,
  SUM(CASE WHEN side='BUY' THEN quantity ELSE 0 END) as long_qty,
  SUM(CASE WHEN side='SELL' THEN quantity ELSE 0 END) as short_qty,
  SUM(CASE WHEN side='BUY' THEN quantity ELSE -quantity END) as net_qty,
  SUM(CASE WHEN side='BUY' THEN quantity * entry_price ELSE 0 END) as long_notional,
  SUM(CASE WHEN side='SELL' THEN quantity * entry_price ELSE 0 END) as short_notional
FROM positions
WHERE status='OPEN'
GROUP BY symbol"
```

## 2. Portfolio Exposure Summary

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== PORTFOLIO SUMMARY ==="
sqlite3 efg_paper_trading/trading.db "
SELECT
  'Total' as type,
  ROUND(SUM(CASE WHEN side='BUY' THEN quantity * entry_price ELSE 0 END), 2) as long_exposure,
  ROUND(SUM(CASE WHEN side='SELL' THEN quantity * entry_price ELSE 0 END), 2) as short_exposure,
  ROUND(SUM(CASE WHEN side='BUY' THEN quantity * entry_price ELSE -quantity * entry_price END), 2) as net_exposure,
  COUNT(*) as positions
FROM positions
WHERE status='OPEN'"
```

## 3. Exposure by Strategy

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== EXPOSURE BY STRATEGY ==="
sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as positions,
  SUM(CASE WHEN side='BUY' THEN 1 ELSE 0 END) as longs,
  SUM(CASE WHEN side='SELL' THEN 1 ELSE 0 END) as shorts,
  ROUND(SUM(quantity * entry_price), 2) as total_notional
FROM positions
WHERE status='OPEN'
GROUP BY strategy_name
ORDER BY total_notional DESC"
```

## 4. Exposure vs Limits

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== EXPOSURE VS LIMITS ==="

# Get capital from manifest
CAPITAL=$(cat efg_paper_trading/deployment_manifest.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('capital', d.get('portfolio',{}).get('capital', 500)))" 2>/dev/null || echo "500")

sqlite3 efg_paper_trading/trading.db "
SELECT
  ROUND(SUM(quantity * entry_price), 2) as total_exposure,
  $CAPITAL as capital,
  ROUND(SUM(quantity * entry_price) / $CAPITAL * 100, 1) as exposure_pct
FROM positions
WHERE status='OPEN'"
```

## 5. Present Results

```
# Exposure Monitor

## Current Positions
| Symbol | Long | Short | Net | Notional |
|--------|------|-------|-----|----------|
| ETH/USD | 0.5 | 0.2 | +0.3 | $960 |

## Portfolio
- Long Exposure: $[X]
- Short Exposure: $[X]
- Net Exposure: $[X]
- Capital Utilization: [X]%

## Limits
- Max Exposure: [configured limit]
- Current: [X]% of limit
- Status: [OK/WARNING/BREACH]
```

</process>

<success_criteria>
- [ ] Net exposure calculated
- [ ] Symbol breakdown provided
- [ ] Limits checked
- [ ] Clear status indication
</success_criteria>
