---
name: quant:process-manager
description: Start, stop, and restart local trading processes
argument-hint: [status|start|stop|restart] [process-name]
allowed-tools:
  - Bash
  - AskUserQuestion
---

<objective>
Manage local trading processes: paper trader, SSH MCP server, L2 system, emotion engine. Start/stop without SSH fumbling.
</objective>

<context>
Processes:
- adaptive_beast: Main paper trading daemon
- ssh_mcp_server: SSH integration for Claude
- l2_system: L2 order book processor
- emotion_engine: Market sentiment analyzer
</context>

<process>

## 1. Parse Command

Default: status

Commands:
- `status` - Show all process statuses
- `start [process]` - Start a process
- `stop [process]` - Stop a process
- `restart [process]` - Restart a process

## 2. Execute Command

### status (default)
```bash
echo "=== LOCAL TRADING PROCESSES ==="
echo ""

# Paper Trader
if pgrep -f "adaptive_beast" > /dev/null; then
  pid=$(pgrep -f "adaptive_beast")
  echo "adaptive_beast: RUNNING (PID: $pid)"
else
  echo "adaptive_beast: STOPPED"
fi

# SSH MCP
if pgrep -f "ssh_mcp_server" > /dev/null; then
  pid=$(pgrep -f "ssh_mcp_server")
  echo "ssh_mcp_server: RUNNING (PID: $pid)"
else
  echo "ssh_mcp_server: STOPPED"
fi

# L2 System
if pgrep -f "l2_system" > /dev/null; then
  pid=$(pgrep -f "l2_system")
  echo "l2_system: RUNNING (PID: $pid)"
else
  echo "l2_system: STOPPED"
fi
```

### start [process]

#### adaptive_beast
```bash
cd ~/Developer/quant_master/quant_v4/efg_paper_trading
mkdir -p logs
nohup python -u adaptive_beast.py > logs/beast.log 2>&1 &
sleep 2
pgrep -f "adaptive_beast" && echo "Started successfully" || echo "Failed to start"
```

#### ssh_mcp_server
```bash
cd ~/Developer/quant_master/quant_v4
nohup python ssh_mcp_server.py > logs/ssh_mcp.log 2>&1 &
sleep 2
pgrep -f "ssh_mcp_server" && echo "Started successfully" || echo "Failed to start"
```

### stop [process]
```bash
pkill -f "$PROCESS_NAME"
sleep 1
pgrep -f "$PROCESS_NAME" && echo "Failed to stop" || echo "Stopped successfully"
```

### restart [process]
```bash
pkill -f "$PROCESS_NAME"
sleep 2
# Then start based on process type
```

## 3. Present Results

```
# Process Manager

## Status
| Process | Status | PID |
|---------|--------|-----|
| adaptive_beast | RUNNING | 12345 |
| ssh_mcp_server | STOPPED | - |

## Actions Taken
- [any start/stop/restart actions]

## Logs
- adaptive_beast: efg_paper_trading/logs/beast.log
- ssh_mcp_server: logs/ssh_mcp.log
```

</process>

<success_criteria>
- [ ] Process status accurately detected
- [ ] Start/stop executed cleanly
- [ ] Process verification after action
- [ ] Log locations provided
</success_criteria>
