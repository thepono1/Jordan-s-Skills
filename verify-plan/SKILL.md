---
name: verify-plan
description: "Production-grade plan verification using parallel subagents. Guarantees zero objective flaws — any remaining issues are subjective judgment calls, not bugs."
user_invocable: true
---

# /verify-plan — Production-Grade Plan Verification

Verify a plan to the standard: **after this passes, any remaining issues are subjective design choices, not objective flaws.** No bugs, no race conditions, no contradictions, no missing error paths, no impossible states.

## Step 0: Locate the Plan

1. Check `.planning/` directory for the most recently modified `.md` file
2. If not found, check the current conversation for a plan written during this session
3. If no plan exists, stop and tell the user

Read the plan file. Also read any source files the plan references (imports, modifications, dependencies). You need the plan AND the code it touches.

## Step 1: Dispatch Parallel Verification Agents

Launch **4 subagents in parallel** using the Task tool. Each agent gets the full plan text and relevant source files. Each returns a structured findings list.

### Agent 1: Logic Auditor (subagent_type: "general-purpose")
Prompt the agent with:
```
You are a logic auditor. Your job: find every objective logical flaw in this plan.

PLAN:
[paste full plan]

REFERENCED FILES:
[paste relevant source code]

Check for:
- Contradictions: Does step N say X but step M assume NOT X?
- Impossible states: Can the system reach a state the plan doesn't handle?
- Race conditions: Are there concurrent operations on shared state without synchronization?
- Deadlocks: Can two operations block each other indefinitely?
- Circular dependencies: Does A depend on B which depends on A?
- Ordering violations: Does step N use output from step M, but M runs after N?
- Type/interface mismatches: Does the plan pass data of type X where type Y is expected?
- Off-by-one / boundary errors: Loops, indices, pagination, time ranges
- Silent failures: Operations that can fail but whose failure isn't checked

For each finding:
- Quote the exact plan text that contains the flaw
- Explain WHY it's objectively wrong (not a preference)
- Classify: BUG | RACE_CONDITION | CONTRADICTION | DEADLOCK | ORDERING | TYPE_MISMATCH | BOUNDARY | SILENT_FAILURE
- Severity: CRITICAL (will break) | HIGH (likely breaks under load/edge case)

Return ONLY objective flaws. If something is a subjective design choice, skip it.
If the logic is sound, say "NO_FINDINGS" — do NOT invent problems.
```

### Agent 2: Completeness Auditor (subagent_type: "general-purpose")
```
You are a completeness auditor. Your job: find every gap in this plan — things that SHOULD be specified but aren't.

PLAN:
[paste full plan]

REFERENCED FILES:
[paste relevant source code]

Check for:
- Missing error handling: What happens when [network call / DB query / file read / API call] fails?
- Missing rollback: If step 3 of 5 fails, what happens to steps 1-2's side effects?
- Unhandled edge cases: Empty inputs, null values, duplicate entries, concurrent requests
- Missing validation: User input, API responses, config values — are they validated before use?
- Missing cleanup: Temp files, connections, locks, timers — are they released on all paths (including error)?
- Undefined behavior: What does the plan say happens when [X]? If it says nothing, that's a gap.
- Missing verification: How do you know each step worked? If there's no check, it's a gap.
- State transitions: Are all valid state transitions defined? Are invalid ones blocked?

For each finding:
- Identify the specific gap
- Explain what could go wrong because of it
- Classify: MISSING_ERROR_HANDLING | MISSING_ROLLBACK | UNHANDLED_EDGE | MISSING_VALIDATION | MISSING_CLEANUP | UNDEFINED_BEHAVIOR | MISSING_VERIFICATION | STATE_GAP
- Severity: CRITICAL (will break in production) | HIGH (breaks on edge cases)

Return ONLY genuine gaps. If the plan handles something implicitly through the framework/language, that's fine — don't flag it.
If complete, say "NO_FINDINGS."
```

### Agent 3: Integration Auditor (subagent_type: "general-purpose")
```
You are an integration auditor. Your job: find every place where components connect incorrectly.

PLAN:
[paste full plan]

REFERENCED FILES:
[paste relevant source code]

Check for:
- API contract violations: Does the caller match what the callee expects? (params, return types, error types)
- Shared state conflicts: Do multiple components read/write the same state without coordination?
- Import/dependency errors: Does the plan import things that don't exist or have changed?
- Config mismatches: Does the plan assume config values that aren't set or have different names?
- Environment assumptions: Does the plan assume env vars, paths, services, ports that may not exist?
- Version incompatibilities: Does the plan use features from library version X but the project has version Y?
- Data format mismatches: JSON vs dict, string vs int, UTC vs local time, 0-indexed vs 1-indexed
- Cross-file consistency: If the plan changes file A's interface, are all callers in files B, C, D updated?

For each finding:
- Quote both sides of the mismatch
- Explain the specific incompatibility
- Classify: CONTRACT_VIOLATION | STATE_CONFLICT | IMPORT_ERROR | CONFIG_MISMATCH | ENV_ASSUMPTION | VERSION_ISSUE | FORMAT_MISMATCH | CALLER_UPDATE_MISSING
- Severity: CRITICAL (won't work at all) | HIGH (works sometimes, breaks under conditions)

If integrations are clean, say "NO_FINDINGS."
```

### Agent 4: Adversarial Tester (subagent_type: "general-purpose")
```
You are an adversarial tester. Your job: actively try to break this plan. Think like a chaos engineer.

PLAN:
[paste full plan]

REFERENCED FILES:
[paste relevant source code]

Attack vectors:
- What if a dependency is down? (DB, API, file system, network)
- What if load is 100x expected? (rate limits, memory, connection pools, queue depth)
- What if data is malformed? (missing fields, wrong types, extra fields, unicode, huge payloads)
- What if timing is wrong? (request arrives before init completes, timeout during critical section, clock skew)
- What if it runs twice? (idempotency — duplicate events, double-submit, retry storms)
- What if partial failure? (3 of 5 records written, then crash — is state consistent?)
- What if permissions change? (file not writable, API key expired, DB user revoked)
- What if the plan is deployed mid-operation? (in-flight requests during deploy, schema migration with active queries)

For each attack that succeeds (plan doesn't handle it):
- Describe the attack scenario in one sentence
- Explain the consequence (data loss, crash, wrong results, security issue)
- Classify: DEPENDENCY_FAILURE | LOAD | MALFORMED_INPUT | TIMING | IDEMPOTENCY | PARTIAL_FAILURE | PERMISSIONS | DEPLOYMENT
- Severity: CRITICAL (data loss/security) | HIGH (crash/wrong results)

Only report attacks the plan is genuinely vulnerable to. Don't flag things the framework/runtime handles.
If robust, say "NO_FINDINGS."
```

## Step 2: Synthesize Results

After all 4 agents return, merge their findings:

1. **Deduplicate**: If two agents found the same issue, keep the more detailed one
2. **Cross-validate**: If Agent 1 says "race condition on X" and Agent 3 says "shared state conflict on X" — that's the same finding, merge them
3. **Discard false positives**: If an agent flagged something the code/framework already handles, remove it
4. **Rank**: Sort by severity (CRITICAL first), then by frequency (found by multiple agents = higher confidence)

## Step 3: Output Report

```
## Plan Verification Report
**Plan**: [filename]
**Agents dispatched**: 4 | **Total findings**: [N]

### CRITICAL (must fix before implementation)
| # | Finding | Type | Agents | Detail |
|---|---------|------|--------|--------|
[findings or "None"]

### HIGH (should fix — breaks under real conditions)
| # | Finding | Type | Agents | Detail |
|---|---------|------|--------|--------|
[findings or "None"]

### Verdict
- **Objective flaws**: [count] CRITICAL, [count] HIGH
- **Production ready**: [YES/NO]
- **Confidence**: [After fixing the above, remaining issues would be subjective design choices only: YES/NO]
```

If CRITICAL = 0 and HIGH = 0:
> **VERIFIED.** This plan has no objective flaws found by 4 independent auditors. Any remaining concerns are subjective design preferences.

If CRITICAL > 0:
> **BLOCKED.** [N] critical flaws must be resolved. These are not style preferences — they are bugs that will manifest in production.

If CRITICAL = 0 but HIGH > 0:
> **CONDITIONAL PASS.** No critical flaws, but [N] high-severity issues exist. These will likely cause problems under real-world conditions. Recommended: fix before implementation.

## Rules

- **Zero tolerance for objective flaws.** The whole point is that after this passes, you can trust the plan.
- **Don't invent problems.** If the plan is solid, say so. False findings erode trust in the process.
- **Read the actual code.** Don't verify the plan in isolation — check it against what exists in the codebase.
- **Each agent works independently.** No agent sees another's output. This prevents groupthink.
- **Severity is binary judgment, not sliding scale.** CRITICAL = will break. HIGH = breaks under real conditions. Nothing else gets reported — medium/low noise dilutes the signal.
