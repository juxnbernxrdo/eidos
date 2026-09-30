# Verification Architecture (Phase 2 — conceptual ONLY)

**Status:** ARCHITECTED (model, not a complete system — §15). Basis: EVD-009
(oracle necessity), EVD-012 (formal path, function-scale), EVD-015 (test weakness).
K value + thresholds OPEN (EXP-004/006).

## Loop model

```text
IMPLEMENT → VERIFY → PASS ──→ CONVERGED (Feature Passport stamped)
               │ FAIL
               ├── attempts left? → REPAIR (oracle trace ingested) → VERIFY
               └── exhausted → ESCALATE (human + full diagnostic diffs)
```

Repair without external oracle is forbidden (EVD-009/012: verbal-only ≈ sampling).

## Verification layers (all must pass for CONVERGED; weights/thresholds Phase 3+)

1. **Tests** — targeted + regression suites (3× flaky pre-screen; timestamp-gated,
   private-split aware per EVD-015; `git log/show` blocked in eval sandboxes).
2. **Static types** — `mypy/pyright/tsc`, 0 errors.
3. **Lint/standards** — `ruff/eslint`, 0 violations.
4. **Contracts** — Phase-3 schema conformance (spec/task/contract/event shapes).
5. **Invariants** — `invariant check` (invariants.md; advisory-before-blocking, ARR-02).
6. **Security** — gateway verdict + sandbox policy conformance (security.md).
7. **Drift** — DOC/SPEC/ARCH/CONTRACT-drift vs baseline (thresholds TBD, EXP-006).

## Verification vs Validation (§15 distinction, retained)

- **Verification:** did we build the thing right? (layers above, machine-checkable).
- **Validation:** did we build the right thing? (acceptance criteria, human/spec
  confirmation, SpecBench-style review EVD-011). Eidos needs both; only the first
  gates CONVERGED automatically.
