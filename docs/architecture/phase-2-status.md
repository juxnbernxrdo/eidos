# Phase 2 Status & Roadmap (Phase 2)

**Status:** LIVING (updated at phase gates) | Date: 2026-09-30

## 1. Component state matrix (§26)

Allowed: `CONCEPTUAL / PROPOSED / ARCHITECTED / IMPLEMENTED / VERIFIED / VALIDATED`.
Nothing below may read VALIDATED (no experiments run — honesty rule).

| Component | State | Note |
|---|---|---|
| Principles (P1–P12) | ARCHITECTED | Tags per principle (principles.md) |
| Pipeline + state machine | ARCHITECTED | |
| Context router + MSC | ARCHITECTED (policy OPEN) | EXP-002 |
| Graph model/queries | ARCHITECTED | EXP-002 |
| Harness adapters | ARCHITECTED | EXP-007 |
| Subagents + CodeAct exec | ARCHITECTED | EXP-002 |
| Skills lifecycle + gateway | ARCHITECTED | EXP-005 |
| Memory (×3 tiers) | CONCEPTUAL / EXPERIMENTAL-gated | Opt-in only (ARR-01); EXP-005 |
| Progress events + passports | ARCHITECTED | Passport model CONCEPTUAL |
| Verification layers + loop | ARCHITECTED (model only) | K/thresholds OPEN; EXP-004/006 |
| Security boundaries | ARCHITECTED | Guarantees OPEN; EXP-005 |
| Evolution pipeline | CONCEPTUAL (forbidden-by-default) | EXP-006 |
| Invariants (INV-001..006) | ARCHITECTED (models) | Blocking forbidden pre-calibration |
| Contracts/Schemas | PROPOSED (needs list §2) | Phase 3 defines |
| Specs/Tasks | PROPOSED (referenced) | Phase 4 defines |
| Bootstrap code (`src/`, tests, `.eidos/`) | IMPLEMENTED / EXPERIMENTAL | Existence documented; not architecture |
| Evaluation harness | PROPOSED (pre-registered EXP-001..007) | Phase 7 runs |

## 2. Future contracts needed (input to Phase 3 — listed, NOT defined)

`project, agent_contract, spec/subspec/task, graph_snapshot, msc_payload,
verification_result, finding/patch, event, feature_passport, skill_manifest,
sandbox_policy, memory_write, evolution_proposal, evaluation_run`.
(Emerges from components.md + data-model.md + harness/agents/verification needs.)

## 3. Roadmap with gates (§23)

```text
PHASE 1 Research — DONE (reinforced) → output: EVD/CLM/GAP/EXP registries
PHASE 2 Architecture — THIS BASELINE → exit: all §28 questions answerable + ARR-01..05 recorded
PHASE 3 Contracts — entry: §2 list + traceability; exit: schemas frozen + validators; dep: Phase 2 baseline
PHASE 4 Specs — entry: contracts frozen; exit: SDD artefacts for Eidos itself; dep: EXP-003 design
PHASE 5 Implementation — entry: specs approved; exit: components pass contracts; dep: sandbox available
PHASE 6 Verification — entry: implementation; exit: layers 1-7 green, K calibrated; dep: EXP-004/006
PHASE 7 Evaluation — entry: pre-registered EXPs; exit: EXP-001..007 results; dep: pinned harness
PHASE 8 Evolution — entry: evaluation + human approval infra; exit: first gated improvement; dep: EXP-006
```

## 4. ARR-01..05 watchlist (from Phase-1 traceability — unchanged, carried)

ARR-01 memory opt-in · ARR-02 invariants advisory-first · ARR-03 constants
(K/risk/ΔQ/k) as DESIGN_CHOICE · ARR-04 evolution prohibited-by-default ·
ARR-05 no 2026-aggregator citations. Clearing any item requires its EXP + ADR update.
