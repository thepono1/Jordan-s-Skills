---
name: quant:circuit-breaker
description: Check and manage circuit breaker status for risk control
argument-hint: [status|reset|trigger|history]
allowed-tools:
  - Bash
  - Read
---

<objective>
Check circuit breaker status, view triggers, and manage risk controls. Critical safety check for trading operations.
</objective>

<context>
Circuit Breaker Database: data/circuit_breaker.db
Triggers:
- Max daily loss
- Max drawdown
- Max position size
- Rapid loss detection
</context>

<process>

## 1. Parse Command

Default: status

Commands:
- `status` - Current circuit breaker state
- `history` - Recent trigger history
- `reset` - Reset tripped breakers (requires confirmation)
- `config` - Show current thresholds

## 2. Execute Command

### status
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CIRCUIT BREAKER STATUS ==="

# Check if circuit breaker table exists
sqlite3 data/circuit_breaker.db "SELECT name FROM sqlite_master WHERE type='table' AND name='circuit_state'" 2>/dev/null | grep -q circuit_state && \
sqlite3 -header -column data/circuit_breaker.db "
SELECT
  breaker_name,
  status,
  CASE WHEN tripped_at IS NOT NULL THEN datetime(tripped_at, 'unixepoch', 'localtime') ELSE 'Never' END as last_tripped,
  threshold,
  current_value
FROM circuit_state
ORDER BY status DESC, breaker_name" || echo "Circuit breaker database not initialized"

# Calculate today's metrics for manual check
echo ""
echo "=== TODAY'S RISK METRICS ==="
sqlite3 efg_paper_trading/trading.db "
SELECT
  ROUND(SUM(pnl), 2) as daily_pnl,
  ROUND(MIN(
    (SELECT SUM(p2.pnl) FROM trades p2 WHERE p2.timestamp <= trades.timestamp AND date(p2.timestamp, 'unixepoch') = date('now'))
  ), 2) as max_intraday_drawdown,
  COUNT(*) as trades_today
FROM trades
WHERE date(timestamp, 'unixepoch') = date('now')" 2>/dev/null || echo "No trades today"
```

### history
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CIRCUIT BREAKER HISTORY (Last 7 days) ==="
sqlite3 -header -column data/circuit_breaker.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  breaker_name,
  action,
  reason,
  value_at_trigger
FROM circuit_history
WHERE timestamp > strftime('%s', 'now', '-7 days')
ORDER BY timestamp DESC
LIMIT 20" 2>/dev/null || echo "No history found"
```

### config
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CIRCUIT BREAKER THRESHOLDS ==="
cat efg_paper_trading/deployment_manifest.json 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
risk = data.get('risk_management', {})
print(f\"Max Daily Loss: \${risk.get('max_daily_loss', 'N/A')}\")
print(f\"Max Drawdown: {risk.get('max_drawdown_pct', 'N/A')}%\")
print(f\"Max Position Size: \${risk.get('max_position_size', 'N/A')}\")
print(f\"Stop Loss: {risk.get('stop_loss_pct', 'N/A')}%\")
" || echo "Could not read config"
```

## 3. Present Results

```
# Circuit Breaker Status

## Current State
| Breaker | Status | Threshold | Current |
|---------|--------|-----------|---------|
| daily_loss | OK | $50 | $12 |
| drawdown | OK | 10% | 3% |
| position | OK | $100 | $45 |

## Today's Metrics
- Daily PnL: $[X]
- Max Drawdown: $[X]
- Trades: [N]

## Status: [ALL CLEAR / BREAKER TRIPPED]
```

</process>

<success_criteria>
- [ ] All breaker states checked
- [ ] Current risk metrics calculated
- [ ] Thresholds displayed
- [ ] Clear status indication
</success_criteria>
