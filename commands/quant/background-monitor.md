---
name: quant:background-monitor
description: Run background agents to monitor logs and alert on issues
allowed-tools:
  - Task
  - Bash
  - Read
---

<objective>
Spawn background monitoring agents that watch logs and alert on important events. Demonstrates the run_in_background pattern for long-running tasks.
</objective>

<architecture>
```
MAIN AGENT (you - continues working)
├── Spawns: Background Agent 1 (error watcher)
├── Spawns: Background Agent 2 (trade watcher)
├── Returns immediately (doesn't wait)
├── Background agents write to output files
└── Check output files periodically or when needed
```
</architecture>

<process>

## Phase 1: Spawn Background Monitors

```python
# Error Monitor (runs in background)
Task(
    subagent_type="Bash",
    run_in_background=True,
    prompt="""
    Monitor trading logs for errors and alert conditions.

    Run this loop:
    while true; do
      # Check for errors in last 5 minutes
      ERRORS=$(tail -100 ~/Developer/quant_master/quant_v4/efg_paper_trading/logs/*.log | grep -i "error\|exception\|failed" | tail -5)

      if [ -n "$ERRORS" ]; then
        echo "[ALERT] $(date): Errors detected:"
        echo "$ERRORS"
      fi

      sleep 300  # Check every 5 minutes
    done

    Continue running until killed.
    """
)
```

```python
# Trade Monitor (runs in background)
Task(
    subagent_type="Bash",
    run_in_background=True,
    prompt="""
    Monitor for new trades and report them.

    LAST_COUNT=$(sqlite3 ~/Developer/quant_master/quant_v4/efg_paper_trading/state/hybrid_trader.db "SELECT COUNT(*) FROM trades")

    while true; do
      NEW_COUNT=$(sqlite3 ~/Developer/quant_master/quant_v4/efg_paper_trading/state/hybrid_trader.db "SELECT COUNT(*) FROM trades")

      if [ "$NEW_COUNT" -gt "$LAST_COUNT" ]; then
        echo "[TRADE] $(date): New trade detected!"
        sqlite3 -header ~/Developer/quant_master/quant_v4/efg_paper_trading/state/hybrid_trader.db "SELECT symbol, side, entry_price, net_pnl FROM trades ORDER BY id DESC LIMIT 1"
        LAST_COUNT=$NEW_COUNT
      fi

      sleep 60  # Check every minute
    done
    """
)
```

## Phase 2: Continue With Other Work

After spawning background agents, you can:
- Continue with other tasks
- The agents run independently
- Check their output files when needed

## Phase 3: Check Background Agent Output

```bash
# Get output file path from Task result
cat /path/to/background/output.txt

# Or tail for live updates
tail -f /path/to/background/output.txt
```

## Phase 4: Kill Background Agents When Done

```bash
# Find the process
ps aux | grep "background-agent-id"

# Or use the KillShell tool
KillShell(shell_id="background-agent-id")
```

</process>

<key_pattern>
BACKGROUND AGENTS:
- Use run_in_background=True in Task call
- Agent continues running after you move on
- Output written to a file (path returned in tool result)
- Use Read or Bash tail to check output
- Kill with KillShell when done

WHEN TO USE:
- Long-running monitoring tasks
- Tasks that shouldn't block your workflow
- Continuous log watching
- Periodic health checks
</key_pattern>

<success_criteria>
- [ ] Background agents spawned successfully
- [ ] Main workflow continues without blocking
- [ ] Can check agent output when needed
- [ ] Can kill agents when done
</success_criteria>
