# Subagent & Execution Architecture (Phase 2)

**Status:** ARCHITECTED | Basis: EVD-004 (PARTIALLY, non-code transfer + cost
conflict), EVD-003 (contamination), EVD-006 (CodeAct). Delegation/parallelism
policy OPEN (EXP-002).

## Subagent unit (conceptual; Phase 3 schemas formalize)

```text
Task — objective + acceptance criteria (contract-bound, immutable)
Scope — target files/symbols + explicit non-goals
Allowed Context — MSC payload only (context.md); zero parent history
Tools — minimal surface for the objective (bounded agency)
Permissions — sandbox policy + capability grants (security.md)
Expected Output — Finding / Patch / VerificationResult (structured)
Verification — local verify before return; parent re-verifies (never trusts)
Lifecycle — spawn → execute (≤30 turns) → report → terminate → event-logged
```

## Policies (defaults, all falsifiable in EXP-002)

- **Isolation:** fresh context per subtask; parallel subtasks on isolated Git
  worktrees (worktrunk lineage) to prevent clobbering.
- **Parallelization:** default 3–5 independent lanes (Anthropic lineage); fan-out
  beyond 5 requires justification (cost/latency blowup documented).
- **Communication:** no lateral agent chat; all coordination via parent through
  contracts + events (star topology; avoids AutoGen-style error loops).
- **Failure recovery:** bounded retry → best-so-far rollback → parent re-plans or
  ESCALATEs with diffs; silent self-retry loops forbidden (EVD-009).

## Execution action space — CodeAct lineage (EVD-006)

Python/tool execution as primary action inside sandbox; JSON/schema calling at
harness boundary (MCP). Rationale: dynamic composition + traceback self-debug
with 60%-fewer-rounds lineage; sandbox mandatory (security.md).

## Cost/latency/contamination accounting

Every dispatch logs tokens, turns (TTI), wall-time, and MSC provenance; these are
first-class ablation variables (EXP-001/002), reported per resolved task.
