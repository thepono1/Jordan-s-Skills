---
name: quant:git-manager
description: Quick git operations for quant codebase
argument-hint: [status|commit|push|diff]
allowed-tools:
  - Bash
---

<objective>
Quick git operations without leaving context. Status, commits, and sync.
</objective>

<process>

## 1. Parse Command

Default: status

Commands:
- `status` - Show git status
- `diff` - Show changes
- `commit [msg]` - Commit with message
- `push` - Push to remote
- `log` - Recent commits

## 2. Execute Command

### status
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== GIT STATUS ==="
git status -s
echo ""
echo "Branch: $(git branch --show-current)"
echo "Last commit: $(git log -1 --format='%h %s' 2>/dev/null)"
```

### diff
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CHANGES ==="
git diff --stat
echo ""
echo "Files changed:"
git diff --name-only
```

### commit
```bash
cd ~/Developer/quant_master/quant_v4
git add -A
git commit -m "$MESSAGE"
echo "Committed: $MESSAGE"
```

### push
```bash
cd ~/Developer/quant_master/quant_v4
git push origin $(git branch --show-current)
echo "Pushed to remote"
```

### log
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== RECENT COMMITS ==="
git log --oneline -10
```

## 3. Present Results

```
# Git Manager

## Status
- Branch: [branch]
- Clean: [yes/no]
- Ahead/Behind: [N/N]

## Recent Activity
[last 5 commits]

## Uncommitted Changes
[list of changed files]
```

</process>

<success_criteria>
- [ ] Command executed
- [ ] Status clear
- [ ] No unintended changes
</success_criteria>
