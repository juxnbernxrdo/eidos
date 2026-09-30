# Progress Architecture (Phase 2)

**Status:** ARCHITECTED | Basis: ADR-008 lineage; reproducibility need EVD-015;
OpenHands EventStream precedent. Efficacy-vs-git claim: none (DESIGN_CHOICE).

## Event (conceptual; Phase 3 schemas formalize)

```text
Event
├── ID (monotonic, hash-chained) / Timestamp / Actor (human/agent/harness)
├── Task (contract ref) / Action (tool + args) / Input / Output
├── Evidence (content hashes, log refs) / Result (status + metrics)
└── Git State (HEAD SHA, worktree, diff hash)
```

## Hierarchy

```text
Session → Task → Actions → Events → Evidence → State
S_t = Fold(S_0, [e_1 … e_t])   (state.json is a projection, events.jsonl is truth)
```

## Rules

- Append-only; no mutation/deletion (corrections are new events with SUPERSEDES).
- Every agent action, patch, and verification run emits an event anchored to Git HEAD
  (Constitution Art. VIII lineage; existing bootstrap `progress/logger.py` is
  EXPERIMENTAL, not the contract).
- `evaluation_run.json` (EXP-001 template: SHAs, model ID, full trace, diff,
  verification logs) is the benchmark-grade projection of this log.
- Feature Passports (data-model.md §4) are convergence projections over the log.
