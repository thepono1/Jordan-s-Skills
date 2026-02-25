---
name: quant:bulk-scorecard
description: Generate scorecards for ALL strategies using recursive sub-agent pattern
---

<objective>
Score every strategy in the database using the @agentic.james recursive sub-agent pattern.
This demonstrates how to process large datasets without the main agent timing out.
</objective>

<architecture>
```
MAIN AGENT (orchestrator)
│
├── Step 1: Get list of all strategies
│
├── Step 2: Spawn BATCH sub-agents (5 strategies each)
│   ├── Batch 1: strategies 1-5
│   ├── Batch 2: strategies 6-10
│   └── Batch N: strategies ...
│
├── Step 3: Audit each batch result
│   └── If incomplete → reprompt that batch
│
├── Step 4: Continue until ALL strategies scored
│
└── Step 5: Synthesize final ranking
```
</architecture>

<process>

## Phase 1: Discovery

Get all unique strategies with sufficient trades:

```bash
sqlite3 ~/Developer/quant_master/quant_v4/efg_paper_trading/state/trading.db "
SELECT DISTINCT candidate_id, COUNT(*) as trades
FROM trades
WHERE candidate_id IS NOT NULL
GROUP BY candidate_id
HAVING COUNT(*) >= 3
ORDER BY trades DESC
"
```

Store the count: TOTAL_STRATEGIES = [N]

## Phase 2: Batch Processing

For every 5 strategies, spawn a sub-agent:

```
Task tool prompt:
"Score these 5 strategies from the trading database at
~/Developer/quant_master/quant_v4/efg_paper_trading/state/trading.db

Strategies to score:
1. [strategy_1]
2. [strategy_2]
3. [strategy_3]
4. [strategy_4]
5. [strategy_5]

For EACH strategy, calculate:
- Win rate
- Profit factor
- Total PnL
- Trade count
- Score (0-10 using standard scorecard criteria)

Return JSON format:
{
  'batch': [batch_number],
  'strategies': [
    {'id': '...', 'win_rate': X, 'pf': X, 'pnl': X, 'trades': X, 'score': X},
    ...
  ],
  'complete': true
}

You MUST score ALL 5 strategies. Do not return until complete."
```

## Phase 3: Audit Loop

After each batch returns:

```python
# Pseudocode for audit
if len(result['strategies']) < expected_count:
    # REPROMPT the same batch
    reprompt = f"""
    Your batch was incomplete. You only scored {len(result['strategies'])}
    but should have scored {expected_count}.

    Missing strategies: {missing_list}

    Complete the remaining strategies NOW.
    """
    # Spawn sub-agent again with reprompt
```

## Phase 4: Continue Until Complete

```
processed = 0
while processed < TOTAL_STRATEGIES:
    batch = get_next_batch(5)
    result = spawn_subagent(batch)

    # Audit
    if not result.complete:
        result = reprompt_subagent(batch, result)

    processed += len(result.strategies)
    all_results.append(result)

# Only exit loop when ALL strategies scored
```

## Phase 5: Final Synthesis

Combine all batch results into ranked list:

```
╔════════════════════════════════════════════════════════════════╗
║                  STRATEGY RANKINGS                             ║
║                  (All [N] strategies scored)                   ║
╠════════════════════════════════════════════════════════════════╣
║ RANK │ STRATEGY              │ SCORE │ WIN% │ PF   │ PNL      ║
╠══════╪═══════════════════════╪═══════╪══════╪══════╪══════════╣
║  1   │ [best_strategy]       │ 8/10  │ 55%  │ 2.1  │ +$XX.XX  ║
║  2   │ [second_strategy]     │ 7/10  │ 48%  │ 1.8  │ +$XX.XX  ║
║ ...  │ ...                   │ ...   │ ...  │ ...  │ ...      ║
╠════════════════════════════════════════════════════════════════╣
║ RECOMMENDATIONS:                                               ║
║ ✅ GO:      [list strategies with score >= 8]                  ║
║ ⚠️ CAUTION: [list strategies with score 5-7]                   ║
║ ❌ NO-GO:   [list strategies with score < 5]                   ║
╚════════════════════════════════════════════════════════════════╝
```

</process>

<the_key_pattern>
THE RECURSIVE CALLING PATTERN:

1. Know your total (TOTAL_STRATEGIES)
2. Process in batches
3. AUDIT every batch
4. REPROMPT if incomplete
5. Track progress: processed / total
6. ONLY finish when processed == total

This is how @agentic.james runs tasks for hours without timing out.
</the_key_pattern>

<success_criteria>
- [ ] All strategies discovered
- [ ] Batches processed in parallel where possible
- [ ] Each batch audited for completeness
- [ ] Incomplete batches reprompted
- [ ] Final ranking synthesized
- [ ] Clear GO/CAUTION/NO-GO categories
</success_criteria>
