# P2-ADR-003 — Contract-Bounded Subagents with CodeAct Execution

**Status:** ACCEPTED (model) + EXPERIMENTAL (delegation policy, parallelism)
**Date:** 2026-09-30 | **Supersedes-format-of:** `docs/adr/ADR-004-*` (retained)

## Context
Long singletons contaminate context (EVD-003/004); orchestrator-workers beat
singletons on research tasks at ~15× tokens (SRC-102); code-as-action beats JSON
calling (EVD-006); lateral agent chat loops fragile (AutoGen rewrite lineage).

## Problem
How to parallelize agent work without contamination, collision, or runaway cost?

## Decision
Ephemeral contract-bound subagents (agents.md unit: task/scope/context/tools/
permissions/output/verification/lifecycle), star topology via parent, worktree
isolation, CodeAct execution inside sandbox, ≤30-turn budget, best-so-far
rollback. Defaults 3–5 lanes; `>5` needs justification.

## Alternatives
Long-lived singleton (rejected: contamination); free multi-agent chat
(rejected: error loops, debugging cost); JSON-only tools (rejected: EVD-006).

## Research Evidence
EVD-004, EVD-003, EVD-006 — traceability row 4–5. Prior `41%` figure retired (U-004).

## Trade-offs
Quality/focus vs token/time cost and orchestration complexity.

## Consequences
Parent must assemble precise contracts; all coordination flows through events;
cost accounting per dispatch is mandatory.

## Assumptions
Non-code transfer holds for code; contract schema suffices; worktree discipline.

## Open Questions
Singleton-vs-contract ΔVSR on code? Optimal parallelism? (GAP-003)

## Future Experiment
EXP-002 (arm B).
