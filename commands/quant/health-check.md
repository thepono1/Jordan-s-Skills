---
name: quant:health-check
description: Complete system health check across local, VPS, and RunPod
allowed-tools:
  - Bash
  - Read
---

<objective>
Run comprehensive health check across all quant infrastructure: local processes, VPS services, databases, and connections.
</objective>

<process>

## 1. Check Local Processes

```bash
echo "=== LOCAL PROCESSES ==="
ps aux | grep -E "adaptive_beast|ssh_mcp|l2_system|emotion" | grep -v grep || echo "No local trading processes running"
```

## 2. Check VPS Services

```bash
echo "=== VPS SERVICES ==="
ssh quantpod "systemctl list-units --state=running | grep -E 'alpha|trader|dashboard'" 2>/dev/null || echo "VPS connection failed"
```

## 3. Check Database Health

```bash
echo "=== DATABASE HEALTH ==="
cd ~/Developer/quant_master/quant_v4

# Check main trading db
sqlite3 efg_paper_trading/trading.db "SELECT COUNT(*) as open_positions FROM positions WHERE status='OPEN'" 2>/dev/null || echo "trading.db: ERROR"

# Check db sizes
ls -lh efg_paper_trading/trading.db data/unified_alpha_v4.db 2>/dev/null
```

## 4. Check Recent Trades

```bash
echo "=== LAST 3 TRADES ==="
cd ~/Developer/quant_master/quant_v4
sqlite3 efg_paper_trading/trading.db "SELECT datetime(timestamp, 'unixepoch'), symbol, side, quantity, price FROM trades ORDER BY timestamp DESC LIMIT 3" 2>/dev/null
```

## 5. Check Disk Space

```bash
echo "=== DISK SPACE ==="
df -h / | tail -1
```

## 6. Present Summary

Format output as:

```
# System Health Check

| Component | Status |
|-----------|--------|
| Paper Trader | [RUNNING/STOPPED] |
| SSH MCP | [RUNNING/STOPPED] |
| VPS Services | [X/7 running] |
| Open Positions | [N] |
| Disk Space | [X% used] |

Last 3 Trades:
- [trade 1]
- [trade 2]
- [trade 3]
```

</process>

<success_criteria>
- [ ] All local processes checked
- [ ] VPS connectivity verified
- [ ] Database health confirmed
- [ ] Recent activity displayed
- [ ] Clear status summary provided
</success_criteria>
