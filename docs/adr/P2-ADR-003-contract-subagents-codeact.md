# P2-ADR-003 — Contract-Bounded Subagents with CodeAct Execution

**Date:** 2026-09-30 | **Canonical location:** `docs/adr/`
**Re-expresses (new format):** `docs/adr/ADR-004-contract-bounded-subagents.md` (retained as historical record)

## Status

ACCEPTED

## Context

Long conversational singletons contaminate context (EVD-003, EVD-004);
orchestrator-workers beat singletons on research tasks at ~15× token cost
(SRC-102, non-code transfer); code-as-action beats JSON calling for programmatic
workflows (EVD-006: up to +20% across 17 LLMs); lateral agent chat loops are
fragile (AutoGen rewrite lineage). Prior `41%` subagent figure retired (U-004).

## Problem

How to parallelize agent work without context contamination, filesystem
collision, or runaway cost?

## Decision

Ephemeral contract-bound subagents (agents.md unit: task, scope, allowed context,
tools, permissions, expected output, verification, lifecycle), star topology
through the parent (no lateral chat), Git-worktree isolation, CodeAct execution
inside the sandbox, ≤30-turn budget, best-so-far rollback. Default 3–5 parallel
lanes; more than 5 requires logged justification.

## Alternatives Considered

- Long-lived conversational singleton — rejected: contamination (EVD-003/EVD-004).
- Free multi-agent chat — rejected: error loops and debugging cost.
- JSON-only tool calling — rejected: EVD-006.

## Research Evidence

EVD-004, EVD-003, EVD-006. Traceability: `research-traceability.md` rows 4–5.

## Evidence Status

PARTIALLY_SUPPORTED

## Trade-offs

Task focus and isolation vs token/time cost (up to ~15× lineage) and
orchestration complexity. Cost conflict recorded, not resolved.

## Consequences

Parents must assemble precise contracts; all coordination flows through contracts
plus events; per-dispatch cost accounting (tokens, turns, time) is mandatory.

## Assumptions

Non-code multi-agent transfer holds for code tasks; contract schema suffices;
worktree discipline prevents collisions.

## Open Questions

Singleton-vs-contract ΔVSR on code tasks? Optimal parallelism cap? (GAP-003)

## Future Experiment

EXP-002 (arm B).

## Phase Boundary

### Phase 2

Architectural decision: subagent unit fields, star topology, isolation and
budget policies, CodeAct action-space choice.

### Phase 3

Future contract implications: `agent_contract` schema, Finding/Patch/
VerificationResult shapes, dispatch/trace interfaces — to be defined, not
defined here.

### Phase 4+

Future specification/implementation/verification implications: orchestrator and
runner specs, sandbox wiring, code-task ablation; no agent is implemented by
this ADR.
