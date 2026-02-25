---
name: quant:kill-loser
description: Find worst performing pair/strategy, disable it, and commit with reason
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

<objective>
Identify the worst performing pair or strategy, disable it from trading, document the reason, and commit the change.
</objective>

<process>

## 1. Find Worst Performers

```bash
cd ~/Developer/quant_master/quant_v4/efg_paper_trading

echo "=== WORST PERFORMING PAIRS (Hybrid Trader) ==="
sqlite3 -header -column state/hybrid_trader.db "
SELECT
  symbol,
  COUNT(*) as trades,
  SUM(CASE WHEN net_pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(100.0 * SUM(CASE WHEN net_pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate,
  ROUND(SUM(net_pnl), 2) as total_pnl,
  ROUND(MIN(net_pnl), 2) as worst_trade
FROM trades
GROUP BY symbol
HAVING COUNT(*) >= 3
ORDER BY total_pnl ASC
LIMIT 5
"
```

## 2. Analyze Why It's Losing

For the worst pair, check:

```bash
# Exit reasons
sqlite3 state/hybrid_trader.db "
SELECT exit_reason, COUNT(*), ROUND(AVG(net_pnl), 4)
FROM trades
WHERE symbol = '[WORST_PAIR]'
GROUP BY exit_reason
"

# Hold times
sqlite3 state/hybrid_trader.db "
SELECT ROUND(AVG(hold_hours), 1) as avg_hold, ROUND(MAX(hold_hours), 1) as max_hold
FROM trades
WHERE symbol = '[WORST_PAIR]'
"
```

## 3. Decide: Disable or Adjust

Options:
1. **Disable completely** - Remove from PAIRS list
2. **Reduce capital** - Lower from $100 to $25
3. **Adjust parameters** - Wider BB, stricter RSI

## 4. Disable the Pair

Comment out in `hybrid_trader.py`:

```python
# DISABLED: [DATE] - [REASON]
# {'symbol': '[PAIR]', 'bb_std': X.X, 'capital': XXX},
```

Or add to disabled list:

```python
DISABLED_PAIRS = [
    {'symbol': '[PAIR]', 'reason': '[REASON]', 'date': '[DATE]', 'pnl': [PNL]},
]
```

## 5. Restart System

```bash
pkill -f "hybrid_trader" 2>/dev/null
sleep 2
pkill -f "supervisor.py" 2>/dev/null
sleep 2
nohup python3 supervisor.py > logs/supervisor.log 2>&1 &
sleep 10

# Verify pair is no longer tracked
grep "PAIRS" logs/HybridTrader.log | tail -1
```

## 6. Commit with Documentation

```bash
cd ~/Developer/quant_master/quant_v4
git add efg_paper_trading/hybrid_trader.py
git commit -m "chore: Disable [PAIR] - consistent losses

Performance:
- Trades: [N]
- Win rate: [X]%
- Total PnL: $[X]
- Worst trade: $[X]

Reason: [Why it failed - trend vs range, high vol, etc.]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

git push origin main
```

## 7. Update Obsidian

Add to "Disabled Pairs" section:
- Pair name
- Disable date
- Performance stats
- Reason for disabling
- Lesson learned

</process>

<success_criteria>
- [ ] Worst performer identified with data
- [ ] Root cause analyzed
- [ ] Pair disabled in config
- [ ] System restarted
- [ ] Committed with full documentation
- [ ] Obsidian updated with lesson learned
</success_criteria>
