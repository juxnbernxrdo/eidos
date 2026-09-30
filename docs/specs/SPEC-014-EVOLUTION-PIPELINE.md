# SPEC-014 — Gated Evolution & Self-Improvement Pipeline

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavior of the gated Evolution and self-improvement pipeline: enforcing that any optimization to system rules, prompts, skills, or pipeline parameters follows an audited, sandboxed, human-approved path, prohibiting unconstrained autonomous self-modification.

## 3. Scope
Proposal generation, sandboxed experiment execution, benchmark evaluation, human review gating, and versioned configuration updates.

## 4. Non-Goals
- Does not permit unconstrained, autonomous self-evolution or un-supervised prompt rewrites (`ARR-04`).
- Does not modify Core architecture without explicit ADR ratification.
- Does not train new foundation model weights.

## 5. Source Requirements
- `REQ-EVO-001`: Gated Evolution Pipeline
- `REQ-EVO-002`: Prohibition of Autonomous Self-Evolution

## 6. Architectural Basis
- `docs/architecture/evolution.md`: Gated pipeline model and terminology distinctions.
- `docs/adr/P2-ADR-007`: Passports and evolution gating.
- `docs/research/evidence-registry.md`: EVD-018 (GEPA metric-driven optimization vs DGM sandbox requirement).

## 7. Contract Dependencies
- `CORE-CONTRACT-009`: Invariant Contract.
- `EVENT-CONTRACT-001`: Event Log Contract.

## 8. Behavioral Requirements
The evolution pipeline enforces a strict 7-stage gated progression:
$$\text{Observation} \to \text{Proposal} \to \text{Evidence} \to \text{Experiment} \to \text{Evaluation} \to \text{Human Approval} \to \text{Versioned Change}$$
1. **Observation**: A recurrent failure or performance bottleneck is captured in the event log.
2. **Proposal**: A structured `LearningProposal` is generated under `.eidos/evolution/proposals/`.
3. **Evidence**: Historical benchmark traces or failure instances are attached.
4. **Experiment**: The candidate modification is evaluated in an isolated, sandboxed environment.
5. **Evaluation**: Benchmark metrics are compared against baseline.
6. **Approval**: An authorized human engineer signs off on the proposal.
7. **Versioned Change**: The change is committed to version control.
Unapproved or silent runtime self-modification attempts are blocked and logged as security violations.

## 9. Inputs
- `LearningProposal` specifying category, rationale, observed patterns, and proposed diff.
- Benchmark test suite and evaluation budget.

## 10. Outputs
- On Human Approval: Accepted change committed to `.eidos/evolution/accepted/`.
- On Rejection: Rejection reason and diagnostic trace committed to `.eidos/evolution/rejected/`.

## 11. State Model
Lifecycle: `PROPOSED → TESTING → EVALUATED → HUMAN_REVIEW → ACCEPTED | REJECTED`.

## 12. Invariants
- `INV-004`: Self-improvement must be auditable, sandboxed, and human-approved.
- Principle P11: Autonomous self-evolution is prohibited-by-default (`ARR-04`).

## 13. Preconditions
- The proposed change must be isolated in a dedicated branch or worktree.
- The evaluation benchmark must have a pinned baseline score.

## 14. Postconditions
- Any accepted change produces a new SemVer release or versioned rule update.

## 15. Failure Semantics
Any detected attempt by an agent or script to alter `.eidos/` configurations directly without an approved proposal triggers a `SECURITY_BREACH` escalation.

## 16. Security Requirements
- Sandboxed experimentation: Proposed modifications run inside a restricted sandbox with zero production write access.
- Human-in-the-loop gate: The transition from `HUMAN_REVIEW` to `ACCEPTED` requires explicit operator confirmation.

## 17. Observability Requirements
- Emits structured telemetry on proposal creation, benchmark delta ($\Delta VSR$), and human approval events.

## 18. Edge Cases
- Regression detected during evaluation: If candidate modification improves one metric but causes regressions on other suites, proposal is automatically rejected.

## 19. Acceptance Criteria
### `AC-014-01` (Human Approval Gate Enforcement)
```gherkin
Given a proposed rule change that improves benchmark performance
When the automated evaluation completes successfully
Then the change remains unapplied in state HUMAN_REVIEW until an explicit operator approval event is received.
```

### `AC-014-02` (Blocking Unapproved Self-Modification)
```gherkin
Given a running subagent attempting to directly edit AGENTS.md or project rules
When the action is intercepted
Then the write is blocked with PERMISSION_DENIED and an INV-004 violation event is logged.
```

## 20. Verification Strategy
Integration tests in `tests/specs/test_evolution_pipeline.py` verifying proposal workflow states, sandbox isolation, and rejection of unauthorized modifications.

## 21. Traceability
- Research: EVD-018
- ADR: `P2-ADR-007`
- Contract: `CORE-CONTRACT-009`, `EVENT-CONTRACT-001`
- Requirements: `REQ-EVO-001`, `REQ-EVO-002`

## 22. Open Questions & Phase 5 Notes
- Validation set construction and metric calibration to be explored in Phase 7 (`EXP-006`).
- Phase 5 note: Evolution features should be scaffolded as command-line proposals (`eidos evolve propose`).
