# Eidos Bounded Domains (Phase 2)

**Status:** ARCHITECTED | Detail files linked. Template per domain:
Purpose / Responsibilities / Inputs / Outputs / Dependencies / Invariants /
Security Boundary / Future Contracts / Research Basis / Open Questions.

## Core — orchestration kernel (pure, deterministic, no I/O)
- Responsibilities: pipeline state machine, event fold `S_t = Fold(S_0, [e_1..e_t])`,
  invariant dispatch. Deps: none (inward only). Invariants: INV-001..006.
- Basis: EVD-002 (phased determinism). Open: formal FSM verification (Phase 3 contracts).
- Existing bootstrap: `src/eidos/core/state.py` (EXPERIMENTAL).

## CLI — operator interface
- Responsibilities: `init/doctor/analyze/graph/spec/verify/baseline/invariant`
  (see `CLI_AND_REPOSITORY_SPEC.md`, PROPOSED). Deps: Core outward.
- Basis: EVD-001 (ACI as interface). Open: command surface freeze (Phase 3).

## Orchestration — pipeline execution
- Responsibilities: phase gating (non-bypassable Discovery→…→Converge),
  REPAIR/ESCALATE transitions. Inputs: contracts; Outputs: events + passports.
- Basis: EVD-002, EVD-009. Open: K-bound + stopping (EXP-004).

## Harness — adapter abstraction → harness.md
## Context — selection/routing/assembly → context.md
## Repository Intelligence — fingerprint + AST extraction → graph.md
## Graph — store, provenance, queries → graph.md
## Specs — SDD artefacts (Phase 4 defines; Phase 2 only references)
- Basis: CLM-010 HYPOTHESIS. Open: efficacy + ceremony (EXP-003).
## Contracts — machine schemas (Phase 3 defines; Phase 2 lists needs → phase-2-status.md)
## Skills — lifecycle + gateway → skills.md
## Agents — subagent model + execution (CodeAct) → agents.md
## Execution — sandboxed tool runtime → agents.md + security.md
## Verification — layers + repair loop → verification.md
## Evidence — passports + anchoring → progress.md
## Progress — event log + state projection → progress.md
- Existing bootstrap: `src/eidos/progress/logger.py` (EXPERIMENTAL).
## Memory — working/project/institutional → memory.md (EXPERIMENTAL, gated)
## Security — permissions/sandbox/provenance → security.md
## Evaluation — ablation harness + benchmarks (Phase 7; pre-registered in EXP-001..007)
## Reporting — health scores from observed metrics only (no hallucinated scorecards)
## Evolution — gated improvement pipeline → evolution.md (forbidden-by-default autonomy)

## Dependency direction (CONSTITUTION Art. II, retained)

```text
Core ← Contracts ← {Intelligence, Graph, Context} ← Adapters ← CLI
Verification + Storage are sinks; Security + Memory are cross-cutting guards.
```
