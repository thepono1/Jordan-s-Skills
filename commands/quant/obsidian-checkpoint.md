---
name: quant:obsidian-checkpoint
description: Save current project state to Obsidian vault as checkpoint
allowed-tools:
  - Bash
  - Read
  - Write
  - Task
---

<objective>
Create a checkpoint in the Obsidian vault capturing current quant system state for future context restoration.
</objective>

<process>
1. Gather current system state:
   - VPS service status
   - Local process status
   - Recent trade counts
   - Open positions
   - L2 system health
   - Any recent changes or fixes

2. Create a new session checkpoint file at:
   `~/Obsidian/ClaudeContext/sessions/YYYY-MM-DD-checkpoint.md`

3. Update the project README at:
   `~/Obsidian/ClaudeContext/projects/quant-v4/README.md`

4. Format includes:
   - Timestamp
   - Infrastructure status table
   - Performance metrics (if available)
   - Recent changes summary
   - Current focus/issues

5. Use this template for session checkpoint:
```markdown
---
date: YYYY-MM-DD
type: checkpoint
project: quant-v4
---

# Checkpoint: [Brief Description]

## System State

### Infrastructure
| Component | Status |
|-----------|--------|
| VPS (quantpod) | ... |
| Local processes | ... |
| RunPod | ... |

### Key Metrics
- Open positions: X
- Trades today: X
- L2 health: X checksum mismatches

## Recent Changes
- [List recent work]

## Current Focus
- [Active work items]

## Notes
[Any important context for future sessions]
```
</process>

<success_criteria>
- [ ] Session checkpoint file created
- [ ] Project README updated with current state
- [ ] All status data is current (not stale)
</success_criteria>
