# Eidos Data & Epistemic Model (Phase 2)

**Status:** ARCHITECTED | Combines knowledge-status (§8 epistemics) + Feature Passport (§9).

## 1. Knowledge status (every relevant artefact carries one)

```text
FACT — compiler/machine-verified (AST validity, exit codes, hashes)
EVIDENCE — peer-reviewed or reproduced benchmark result (EVD-XXX)
OBSERVATION — logged runtime trace (events, tool outputs)
INTERPRETATION — deduction explaining a phenomenon (CLM-XXX)
HYPOTHESIS — testable, unverified (H1, GAP-XXX)
DESIGN_DECISION — Eidos commitment, trade-off-based (P2-ADR-XXX)
EXPERIMENT — pre-registered protocol (EXP-XXX)
EXPERIMENTAL_RESULT — outcome of one EXP run
VALIDATED_RESULT — replicated, reviewed outcome
UNKNOWN — none of the above (default for new claims)
```

Forbidden promotions: `HYPOTHESIS→FACT`, `DESIGN_DECISION→EVIDENCE`,
`IMPLEMENTED→VALIDATED`, `CORRELATION→CAUSATION` (Constitution Honesty Axiom).

## 2. Provenance (every edge/claim carries one)

```text
EXTRACTED — deterministic parser/compiler output, confidence 1.0
INFERRED — LLM-derived, confidence ∈ [0.0, 0.99], never overrides EXTRACTED
USER_CONFIRMED — human-verified inference
AGENT_PROPOSED — working hypothesis pending verification
```

## 3. Artefact header (conceptual; Phase 3 schemas formalize)

```text
What / Where-from / Who / When / Why / Supporting evidence (EVD/SRC) /
Status (§1) / Provenance (§2) / Supersedes
```

## 4. Feature Passport — architectural model (§9, NOT an implemented system)

```text
Feature
├── Requirement (REQ-XXX, USER_CONFIRMED intent)
├── Spec (SPEC-XXX, Phase 4)
├── Architecture (nodes/edges touched, graph.md)
├── Dependencies (DDR, DEPENDENCY_DECISION_RECORDS.md)
├── Contracts (Phase 3 schemas)
├── Implementation (git diff, COMMIT)
├── Tests (TEST nodes, TESTED_BY edges)
├── Security (gateway verdict, sandbox policy)
├── Documentation (DOCUMENTED_BY edges; DOC-DRIFT flag)
├── Evidence (observation hashes, evaluation_run.json refs)
├── Git (SHAs, worktree, base)
└── Verification (VerificationResult; CONVERGED only if all layers pass)
```

- Created by: Orchestration on CONVERGE. Consumed by: Reporting, Evolution
  (as training/approval input), audit. Relation to graph: passport is a
  projection over `Feature → {Spec, Contract, Test, Finding, Evidence}` subgraphs.
- Status: CONCEPTUAL. Open: minimal viable passport fields (Phase 3).
