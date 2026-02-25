---
name: quant:refactor-strategy
description: Analyze a strategy, suggest improvements, implement, test, and commit
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
---

<objective>
Full refactoring workflow for a trading strategy. Analyze current implementation, identify improvements, implement changes, test, and commit with documentation.
</objective>

<arguments>
- strategy_name: Name of strategy file (e.g., "hybrid_trader", "proven_trader_v2")
</arguments>

<process>

## 1. Analyze Current Strategy

Use an Explore agent to understand the strategy:

```
Task(subagent_type="Explore", prompt="
Analyze the {strategy_name}.py strategy in efg_paper_trading/:
1. Entry logic - what triggers a trade?
2. Exit logic - stops, targets, trailing?
3. Position sizing - how is size calculated?
4. Risk management - what protections exist?
5. Known issues or TODOs in comments
")
```

## 2. Query Performance Data

```bash
cd ~/Developer/quant_master/quant_v4/efg_paper_trading

# Get strategy performance
sqlite3 -header -column state/{strategy_db}.db "
SELECT
  exit_reason,
  COUNT(*) as count,
  ROUND(AVG(net_pnl), 4) as avg_pnl,
  ROUND(SUM(net_pnl), 2) as total_pnl
FROM trades
GROUP BY exit_reason
ORDER BY count DESC
"
```

## 3. Identify Improvement Areas

Based on data, identify:
- **Entry timing**: Are we entering too early/late?
- **Exit efficiency**: Are stops too tight/loose?
- **Position sizing**: Is risk appropriate?
- **Filters**: Should we add regime/volatility filters?

## 4. Plan Refactor

Use Plan agent if changes are significant:

```
Task(subagent_type="Plan", prompt="
Plan a refactor of {strategy_name}.py to:
1. [Specific improvement 1]
2. [Specific improvement 2]
Consider: backward compatibility, testing, rollback plan
")
```

## 5. Implement Changes

Make focused, atomic changes:
- One logical change per edit
- Preserve existing behavior where not intentionally changing
- Add comments explaining why, not what

## 6. Test Changes

```bash
# Syntax check
python3 -c "import {strategy_name}; print('✅ Syntax OK')"

# Quick backtest if available
python3 {strategy_name}.py --backtest --period 7d

# Dry run
python3 {strategy_name}.py --dry-run
```

## 7. Commit and Document

```bash
git add efg_paper_trading/{strategy_name}.py
git commit -m "refactor({strategy_name}): [description]

Changes:
- [Change 1]
- [Change 2]

Expected impact:
- [Impact 1]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

git push origin main
```

## 8. Update Obsidian

Document the refactor in Obsidian:
- What was changed and why
- Expected vs actual results
- Lessons learned

</process>

<success_criteria>
- [ ] Strategy analyzed thoroughly
- [ ] Performance data reviewed
- [ ] Improvements identified with rationale
- [ ] Changes implemented cleanly
- [ ] Tests pass
- [ ] Committed with descriptive message
- [ ] Documentation updated
</success_criteria>
