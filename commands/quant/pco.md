---
name: quant:pco
description: Push, Commit, Obsidian, sync to all VPSs (unified workflow)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
---

<objective>
PCO = Push + Commit + Obsidian + VPS Sync. Unified workflow that:
1. Commits changes to git
2. Pushes to remote
3. Syncs SHARED_STATE.md to both VPSs (quantpod + contabo)
4. Updates Codex memory status snapshot for searchable context
5. Updates Obsidian notes
6. Runs code analysis on modified files
</objective>

<process>

## 1. Pre-flight Checks

```bash
cd ~/Developer/quant_master/quant_v4

# Check daemon status
python3 tools/unified_sync_daemon.py status

# Check VPS connectivity
ssh -o ConnectTimeout=5 quantpod 'echo quantpod:ok' 2>/dev/null || echo "quantpod:unreachable"
ssh -o ConnectTimeout=5 contabo 'echo contabo:ok' 2>/dev/null || echo "contabo:unreachable"

# Show changes
git status --short
```

## 2. Run Code Analysis (if Python files changed)

```bash
# Check for efficiency issues in modified files
python3 -c "
from ralph_daemon.optimization import CodeAnalyzer
import subprocess
result = subprocess.run(['git', 'diff', '--name-only'], capture_output=True, text=True)
files = [f for f in result.stdout.strip().split() if f.endswith('.py')]
if files:
    analyzer = CodeAnalyzer()
    for f in files[:5]:
        issues = analyzer.analyze_file(f)
        if issues:
            print(f'{f}: {len(issues)} issues')
            for i in issues[:3]:
                print(f'  L{i.line_number}: [{i.severity}] {i.description}')
else:
    print('No Python files modified')
" 2>/dev/null || echo "Analyzer not available"
```

## 3. Commit and Push

```bash
git add -A
git status --short
```

Create commit with conventional format:
- `feat:` new features
- `fix:` bug fixes
- `chore:` maintenance
- `refactor:` code improvements

```bash
git commit -m "$(cat <<'EOF'
<type>: <description>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

git push origin main
```

## 4. Sync to VPSs

```bash
# Update shared state timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
sed -i '' "s/^Last Updated:.*/Last Updated: ${TIMESTAMP}/" .kaleo/SHARED_STATE.md
sed -i '' "s/^Updated By:.*/Updated By: claude-code/" .kaleo/SHARED_STATE.md

# Sync to quantpod (trading VPS)
scp .kaleo/SHARED_STATE.md quantpod:~/quant_v4/.kaleo/

# Sync to contabo (email VPS) - state only, not code
ssh contabo 'mkdir -p ~/shared_state' 2>/dev/null
scp .kaleo/SHARED_STATE.md contabo:~/shared_state/

echo "✅ Synced to both VPSs"
```

## 5. Update Codex Memory Snapshot

```bash
cd ~/Developer/quant_master/quant_v4
python3 tools/codex_memory_bridge.py snapshot

# Optional query check after snapshot
python3 tools/codex_memory_bridge.py query pco --local
```

This keeps `docs/CODEX_MEMORY_STATUS.md` current and makes Claude-imported
history + local docs discoverable from one command.

## 6. Update Obsidian (if relevant)

Only update Obsidian if session involved significant changes:
- Trading system modifications
- Strategy updates
- Architecture changes

```bash
# Check if Obsidian update needed
ls ~/Obsidian/ClaudeContext/knowledge/ | head -5
```

## 7. Verify

```bash
# Recent commits
git log --oneline -3

# VPS state verification
ssh quantpod 'head -3 ~/quant_v4/.kaleo/SHARED_STATE.md' 2>/dev/null

echo ""
echo "✅ PCO Complete - All systems synced"
```

</process>

<automation>
The unified_sync_daemon handles background sync every 60s:
- Auto-commits when Claude Code is active
- Syncs state to both VPSs
- Runs code analysis on modified files
- Checks IntentRegistry for conflicts

Start daemon: `python3 tools/unified_sync_daemon.py start`
</automation>

<success_criteria>
- [ ] Changes committed with conventional message
- [ ] Pushed to origin/main
- [ ] State synced to quantpod VPS
- [ ] State synced to contabo VPS
- [ ] Codex memory snapshot updated
- [ ] Code analysis run (if Python changes)
</success_criteria>
