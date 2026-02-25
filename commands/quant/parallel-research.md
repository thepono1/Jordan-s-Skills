---
name: quant:parallel-research
description: Research multiple topics simultaneously using parallel Explore agents
allowed-tools:
  - Task
  - Read
---

<objective>
Demonstrate parallel sub-agent research pattern. Spawn multiple Explore agents to research different aspects of a topic simultaneously, then synthesize results.
</objective>

<arguments>
- topic: What to research (e.g., "trailing stop implementations", "regime detection algorithms")
</arguments>

<architecture>
```
MAIN AGENT (orchestrator)
├── Spawns: Explore Agent 1 (codebase search)
├── Spawns: Explore Agent 2 (documentation search)
├── Spawns: Explore Agent 3 (test/example search)
│   [All run in PARALLEL - single message, multiple Task calls]
├── Waits for all results
├── Synthesizes findings
└── Returns comprehensive answer
```
</architecture>

<process>

## Phase 1: Spawn Parallel Explore Agents

In a SINGLE message, spawn THREE explore agents:

```
Task 1 (Explore agent):
"Search the quant_v4 codebase for implementations of {topic}.
Focus on:
- Core implementation files
- Function signatures and parameters
- Current usage patterns
Return: file paths, key functions, how it works"

Task 2 (Explore agent):
"Search for documentation about {topic} in:
- /docs folder
- README files
- Code comments
- Obsidian notes
Return: existing docs, explanations, rationale"

Task 3 (Explore agent):
"Search for tests and examples of {topic}:
- Test files
- Example scripts
- Backtests using this feature
Return: test coverage, example usage, edge cases"
```

## Phase 2: Synthesize Results

Combine findings into structured output:

```markdown
# Research: {topic}

## Implementation
- Location: [files]
- Key functions: [list]
- How it works: [explanation]

## Documentation
- Existing docs: [yes/no/partial]
- Key points: [summary]

## Tests & Examples
- Test coverage: [good/partial/none]
- Examples found: [list]

## Gaps Identified
- [missing documentation]
- [untested edge cases]
- [unclear implementations]

## Recommendations
1. [next step]
2. [improvement]
```

</process>

<key_pattern>
PARALLEL SPAWNING:
- Put ALL Task tool calls in a SINGLE message
- They run simultaneously, not sequentially
- Much faster than running one at a time
- Use for independent research tasks
</key_pattern>

<success_criteria>
- [ ] All 3 agents spawned in single message
- [ ] Results from all 3 collected
- [ ] Findings synthesized coherently
- [ ] Gaps and next steps identified
</success_criteria>
