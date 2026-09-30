# Eidos Architectural Principles (Phase 2)

**Status:** ARCHITECTED | Each principle ends with its honest epistemic tag.
Tags: `EVIDENCE_BACKED` / `PARTIALLY_SUPPORTED` / `DESIGN_CHOICE` /
`RESEARCH_HYPOTHESIS` / `OPEN_DECISION`.

## P1 — Model Agnosticism — DESIGN_CHOICE
Eidos must not depend architecturally on one model provider. All model interactions
go through pinned, versioned interfaces (`evaluation_run.json` records exact model
ID). Basis: EVD-015 (provider drift), EVD-001/002 (harness deltas replicate across
models). Assumption: provider APIs remain callable with deterministic settings.

## P2 — Harness Agnosticism — PARTIALLY_SUPPORTED
Eidos adapts to harnesses via `HarnessAdapter` (harness.md). Basis: EVD-001/002
(harness changes move outcomes), SRC-105 (MCP standard). Assumption: MCP/CLI
stability; breakage measured longitudinally (EXP-007).

## P3 — Evidence Traceability — DESIGN_CHOICE
Decisions and results trace to evidence (`SRC → EVD → CLM → ADR → EXP`).
Basis: Phase-1 methodology (EVD-015 reproducibility need). This is a governance
choice, not a scientific finding.

## P4 — Explicit State — DESIGN_CHOICE
Artefacts carry one of `Observed / Inferred / Proposed / Approved / Implemented /
Verified / Validated`. Maps to epistemic model (data-model.md). NoOrphanInference:
nothing labelled `Verified/Validated` without machine evidence + experiment.

## P5 — Verification First — EVIDENCE_BACKED (necessity) + DESIGN_CHOICE (form)
Task completion requires machine evidence, never bare agent assertion (CLM-009,
INV-003). The exact layers/thresholds are design choices calibrated in EXP-004/006.

## P6 — Controlled Autonomy — PARTIALLY_SUPPORTED
Autonomy bounded by contracts, permissions, sandboxing, verification gates.
Basis: EVD-007 (prompt bans fail), EVD-008 (supply-chain risk), EVD-009 (oracle
need). Sandbox efficacy vs SWE tasks remains OPEN (EXP-005).

## P7 — Repository Intelligence — PARTIALLY_SUPPORTED
Eidos builds a structured repo representation (graph.md). Basis: EVD-005 (+32.8%
line-graph gains). Granularity (line/entity/CPG) is RESEARCH_HYPOTHESIS (GAP-002).

## P8 — Context Efficiency — EVIDENCE_BACKED (phenomenon) + DESIGN_CHOICE (policy)
Select deliberately; never maximize (EVD-003, EVD-016). k≤2 / order-preservation /
Self-Route escalation are current policies, all recalibratable (EXP-002).

## P9 — Fresh Task-Bounded Agents — PARTIALLY_SUPPORTED
Prefer bounded-contract subagents over long singletons (EVD-004, non-code transfer;
cost conflict documented). Default parallelism and delegation policy are OPEN (EXP-002).

## P10 — Auditable Progress — DESIGN_CHOICE
Event-sourced, replayable, crypto-anchored progress (progress.md). Efficacy vs plain
git is unmeasured; kept as governance choice (ADR-008 lineage).

## P11 — Explicit Self-Improvement — RESEARCH_HYPOTHESIS + DESIGN_CHOICE (gating)
No silent self-modification (INV-004). Observation→Proposal→Experiment→Approval→
Versioned-Change only. Basis: EVD-018 (GEPA strong w/ metric; DGM sandboxed-only).
Open-ended evolution is forbidden by default until EXP-006.

## P12 — Security by Design — PARTIALLY_SUPPORTED
Skills/tools/MCP/agents/memory operate under explicit limits (security.md).
Basis: EVD-007/008, SRC-027/028/108. Thresholds (risk<25) and sandbox guarantees
are OPEN (EXP-005).
