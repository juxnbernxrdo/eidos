# Architectural Invariants (Phase 2 — model + future contract relation)

**Status:** ARCHITECTED (models only; NOT implemented gates — §22).
Each invariant lists its Phase-3 contract target and validating experiment.
Pre-existing `INVARIANTS_AND_DRIFT_SPEC.md` (ARCH-001 layer isolation, 4-drift
engine) is PROPOSED detail design, reclassified below.

## Invariants

- **INV-001 — Model-provider agnosticism.** No Core/contract dependency on one
  provider. → Contract: provider-neutral interfaces + pinned IDs. Basis: P1.
- **INV-002 — No cross-project leakage without explicit authorization.**
  → Contracts: adapter blindness, memory gating, sandbox confinement. Basis: EVD-008.
- **INV-003 — Agent completion claims are insufficient evidence.** DONE ⟺ machine
  VerificationResult. → Contract: CONVERGED predicate (verification.md). Basis: EVD-009.
- **INV-004 — Self-improvement is auditable.** All changes via evolution pipeline.
  → Contract: `.eidos/evolution/` schemas + approval gates. Basis: EVD-018.
- **INV-005 — Research claims retain provenance.** Every claim carries status +
  provenance (data-model.md). → Contract: artefact headers. Basis: Phase-1 method.
- **INV-006 — Decisions trace to evidence or are marked design choices.**
  → Contract: ADR required fields (Research Evidence / Assumptions / Experiment).
  Basis: P3.

## Relation to ARCH-001 & drift (existing spec, PROPOSED)

ARCH-001 (layer isolation) becomes the first *instance* of the invariant engine
model above; DOC/SPEC/ARCH/CONTRACT-drift detectors become *instances* of
Verification layer 7. Thresholds (ΔQ<−0.05 etc.) are DESIGN_CHOICE pending EXP-006
(ARR-02/03). Blocking enforcement before calibration is forbidden.
