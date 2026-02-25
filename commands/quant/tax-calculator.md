---
name: quant:tax-calculator
description: Calculate tax obligations from trading activity
argument-hint: [ytd|year|export]
allowed-tools:
  - Bash
  - Read
---

<objective>
Tax preparation automation. Calculate gains/losses for tax reporting.
</objective>

<context>
Note: Paper trading does not create tax obligations.
This is for when transitioning to live trading.
</context>

<process>

## 1. Calculate YTD Summary

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== YTD TRADING SUMMARY ==="

sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strftime('%Y', timestamp, 'unixepoch') as year,
  COUNT(*) as total_trades,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as winning_trades,
  SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losing_trades,
  ROUND(SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END), 2) as gross_gains,
  ROUND(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END), 2) as gross_losses,
  ROUND(SUM(pnl), 2) as net_pnl
FROM trades
WHERE strftime('%Y', timestamp, 'unixepoch') = strftime('%Y', 'now')
GROUP BY year"
```

## 2. Monthly Breakdown

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== MONTHLY BREAKDOWN ==="

sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strftime('%Y-%m', timestamp, 'unixepoch') as month,
  COUNT(*) as trades,
  ROUND(SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END), 2) as gains,
  ROUND(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END), 2) as losses,
  ROUND(SUM(pnl), 2) as net
FROM trades
WHERE strftime('%Y', timestamp, 'unixepoch') = strftime('%Y', 'now')
GROUP BY month
ORDER BY month"
```

## 3. Short vs Long Term

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== HOLDING PERIOD ANALYSIS ==="

# For crypto: typically all short-term (< 1 year)
sqlite3 efg_paper_trading/trading.db "
SELECT
  'Short-term (< 1 year)' as category,
  COUNT(*) as trades,
  ROUND(SUM(pnl), 2) as pnl
FROM trades
WHERE strftime('%Y', timestamp, 'unixepoch') = strftime('%Y', 'now')"
```

## 4. Export for Tax Software

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== EXPORT ==="

# Create tax export
sqlite3 -header -csv efg_paper_trading/trading.db "
SELECT
  datetime(timestamp, 'unixepoch') as date,
  symbol as asset,
  side as type,
  quantity,
  price,
  quantity * price as proceeds,
  pnl as gain_loss,
  strategy_name as description
FROM trades
WHERE strftime('%Y', timestamp, 'unixepoch') = strftime('%Y', 'now')
ORDER BY timestamp" > data/tax_export_$(date +%Y).csv 2>/dev/null && echo "Exported to: data/tax_export_$(date +%Y).csv" || echo "Export failed"
```

## 5. Present Results

```
# Tax Calculator

## YTD Summary
- Gross Gains: $[X]
- Gross Losses: $[X]
- Net P&L: $[X]

## Classification
- Short-term gains: $[X]
- Long-term gains: $[X]

## Monthly Breakdown
| Month | Gains | Losses | Net |
|-------|-------|--------|-----|

## Export
- CSV: data/tax_export_2026.csv

## Notes
- Paper trading: No tax obligation
- Consult tax professional for live trading
```

</process>

<success_criteria>
- [ ] YTD calculated
- [ ] Monthly breakdown
- [ ] Export generated
- [ ] Proper disclaimers
</success_criteria>
