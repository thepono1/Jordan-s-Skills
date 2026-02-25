---
name: quant:execution-quality
description: Analyze trade execution quality and slippage
argument-hint: [summary|detailed|strategy]
allowed-tools:
  - Bash
  - Read
---

<objective>
Analyze execution quality: slippage, fill rates, timing. Identify execution improvements.
</objective>

<process>

## 1. Calculate Slippage

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== SLIPPAGE ANALYSIS ==="

sqlite3 efg_paper_trading/trading.db "
SELECT
  'All Trades' as period,
  COUNT(*) as trades,
  ROUND(AVG(slippage_pct), 4) as avg_slippage_pct,
  ROUND(MAX(slippage_pct), 4) as max_slippage_pct,
  ROUND(SUM(slippage_cost), 2) as total_slippage_cost
FROM trades
WHERE slippage_pct IS NOT NULL" 2>/dev/null || echo "Slippage data not tracked"

# Alternative calculation
sqlite3 efg_paper_trading/trading.db "
SELECT
  COUNT(*) as trades,
  ROUND(AVG(ABS(actual_price - signal_price) / signal_price * 100), 4) as avg_slippage_pct
FROM trades
WHERE actual_price IS NOT NULL AND signal_price IS NOT NULL" 2>/dev/null
```

## 2. Execution by Time of Day

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== EXECUTION BY HOUR ==="

sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strftime('%H', timestamp, 'unixepoch') as hour,
  COUNT(*) as trades,
  ROUND(AVG(pnl), 2) as avg_pnl,
  ROUND(100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate
FROM trades
GROUP BY hour
ORDER BY trades DESC
LIMIT 12"
```

## 3. Execution by Strategy

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== EXECUTION BY STRATEGY ==="

sqlite3 -header -column efg_paper_trading/trading.db "
SELECT
  strategy_name,
  COUNT(*) as trades,
  ROUND(AVG(ABS(pnl)), 2) as avg_move,
  ROUND(AVG(
    CASE
      WHEN pnl > 0 THEN pnl
      WHEN pnl < 0 THEN -pnl
    END
  ), 2) as avg_abs_pnl
FROM trades
GROUP BY strategy_name
HAVING trades >= 5
ORDER BY trades DESC
LIMIT 10"
```

## 4. Fill Time Analysis

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== FILL TIMING ==="

# Analyze time between signal and fill
sqlite3 efg_paper_trading/trading.db "
SELECT
  'Average fill delay' as metric,
  ROUND(AVG(fill_time - signal_time), 2) as seconds
FROM trades
WHERE fill_time IS NOT NULL AND signal_time IS NOT NULL" 2>/dev/null || echo "Fill timing not tracked"
```

## 5. Present Results

```
# Execution Quality

## Slippage
- Average: [X]%
- Total Cost: $[X]
- Max: [X]%

## Best Execution Hours
| Hour | Trades | Win% | Avg PnL |
|------|--------|------|---------|

## By Strategy
| Strategy | Trades | Avg Move |
|----------|--------|----------|

## Recommendations
- [optimal trading hours]
- [strategies with best execution]
- [areas for improvement]
```

</process>

<success_criteria>
- [ ] Slippage calculated
- [ ] Time analysis done
- [ ] Strategy comparison
- [ ] Recommendations provided
</success_criteria>
