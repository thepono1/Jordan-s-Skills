---
name: quant:websocket-manager
description: Manage WebSocket and L2 feed connections
argument-hint: [status|restart|logs]
allowed-tools:
  - Bash
  - Read
---

<objective>
Monitor and manage WebSocket feed connections for L2 data and real-time prices.
</objective>

<process>

## 1. Check WebSocket Status

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== WEBSOCKET CONNECTION STATUS ==="

# Check for WS processes
ps aux | grep -E "websocket|ws_|l2_" | grep -v grep | while read line; do
  pid=$(echo "$line" | awk '{print $2}')
  cmd=$(echo "$line" | awk '{for(i=11;i<=NF;i++) printf "%s ", $i}')
  echo "PID $pid: $cmd"
done

if ! ps aux | grep -E "websocket|ws_|l2_" | grep -v grep > /dev/null; then
  echo "No WebSocket processes detected"
fi
```

## 2. Check Connection Health

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== CONNECTION HEALTH ==="

# Check last L2 update time
sqlite3 efg_paper_trading/state/l2_data.db "
SELECT
  'L2 Feed' as feed,
  CASE
    WHEN (julianday('now') - julianday(datetime(MAX(timestamp), 'unixepoch'))) * 24 * 60 < 5 THEN 'HEALTHY'
    WHEN (julianday('now') - julianday(datetime(MAX(timestamp), 'unixepoch'))) * 24 * 60 < 30 THEN 'STALE'
    ELSE 'DISCONNECTED'
  END as status,
  ROUND((julianday('now') - julianday(datetime(MAX(timestamp), 'unixepoch'))) * 24 * 60, 1) as mins_since_update
FROM order_book" 2>/dev/null || echo "L2 database not available"

# Check trade feed
sqlite3 efg_paper_trading/trading.db "
SELECT
  'Trade Feed' as feed,
  CASE
    WHEN (julianday('now') - julianday(datetime(MAX(timestamp), 'unixepoch'))) * 24 < 24 THEN 'ACTIVE'
    ELSE 'INACTIVE'
  END as status
FROM trades" 2>/dev/null
```

## 3. View Connection Logs

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== RECENT CONNECTION EVENTS ==="
grep -i "connect\|disconnect\|reconnect\|error\|websocket" efg_paper_trading/logs/beast.log 2>/dev/null | tail -20 || echo "No connection logs found"
```

## 4. Restart WebSocket (if needed)

If `restart` command:
```bash
cd ~/Developer/quant_master/quant_v4
echo "Restarting WebSocket feeds..."

# Kill existing
pkill -f "l2_system\|ws_feed" 2>/dev/null
sleep 2

# Restart L2 system if exists
if [ -f "efg_paper_trading/l2_system/main.py" ]; then
  cd efg_paper_trading/l2_system
  nohup python main.py > ../logs/l2.log 2>&1 &
  echo "L2 system restarted"
fi

sleep 3
# Verify
pgrep -f "l2_system" && echo "L2 feed: RUNNING" || echo "L2 feed: FAILED TO START"
```

## 5. Present Results

```
# WebSocket Manager

## Connection Status
| Feed | Status | Last Update |
|------|--------|-------------|
| L2 Order Book | HEALTHY | 30s ago |
| Price Feed | ACTIVE | - |

## Processes
- [list of WS processes with PIDs]

## Recent Events
- [connection/disconnection log]

## Actions
- `restart` to restart feeds
- Check logs at efg_paper_trading/logs/
```

</process>

<success_criteria>
- [ ] Connection status verified
- [ ] Data freshness checked
- [ ] Processes enumerated
- [ ] Restart capability available
</success_criteria>
