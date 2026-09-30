# SPEC-004 — Context Router & Minimal Sufficient Context (MSC)

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavior of the Context Router in selecting, pruning, budgeting, and assembling Minimal Sufficient Context (MSC) payloads for agent dispatch, combating attention degradation and prompt saturation.

## 3. Scope
Context candidate selection, topological pruning, token budgeting, positional pinning, selection auditing, and adversarial quarantine.

## 4. Non-Goals
- Does not implement proprietary vector embedding databases.
- Does not rank items using unvalidated black-box AI judges.
- Does not dump full repositories into prompt windows.

## 5. Source Requirements
- `REQ-CTX-001`: Minimal Sufficient Context Assembly
- `REQ-CTX-002`: Auditable Selection Rationale
- `REQ-CTX-003`: Strict Token Budgeting and Quarantine

## 6. Architectural Basis
- `docs/architecture/context.md`: Context pipeline and MSC assembly rules.
- `docs/adr/P2-ADR-002`: Repository Graph with $k \le 2$ MSC routing.
- `docs/research/evidence-registry.md`: EVD-003 (U-curve retrieval degradation), EVD-016 (Self-Route order-preservation).

## 7. Contract Dependencies
- `CTX-CONTRACT-001`: Context Router Contract (`schemas/contracts/context/context-router.schema.json`).
- `GRAPH-CONTRACT-001`: Graph Store Contract.
- `CORE-CONTRACT-002`: Task Contract.

## 8. Behavioral Requirements
The router takes a task and repository graph, retrieves candidates up to $k \le 2$ hops, prunes neighbor nodes to signatures/types, pins critical contracts at prompt boundaries, and emits an auditable payload strictly within the token budget.
$$\text{AssembleContext}(\text{Task}, G, \text{Budget}) \to \text{MSC Payload}$$
Every assembled item must record why it was selected. Contaminating or out-of-budget items must be explicitly quarantined.

## 9. Inputs
- `routing_request` conforming to `CTX-CONTRACT-001`:
  - `task`: Target files and seed symbols.
  - `context_sources`: Flags for graph, rules, specs, skills, memory, evidence.
  - `budget_constraints`: `max_tokens`, `reserve_for_generation`, `k_hop_limit`.
  - `security_constraints`: `quarantine_adversarial`, `isolated_project_id`.

## 10. Outputs
- `routing_response` conforming to `CTX-CONTRACT-001`:
  - `msc_id`, `total_tokens`, `budget_exhausted`, `escalation_required`.
  - `pinned_boundary_contracts`: Critical interfaces at start/end.
  - `assembled_items`: Ordered list with `selection_audit` metadata.
  - `quarantined_exclusions`: Excluded items with justification.

## 11. State Model
Stateless functional request-response pipeline:
`Ingest Request → Graph Neighborhood Query → Pruning & Filtering → Budget Allocation → Boundary Pinning → Emit MSC`.

## 12. Invariants
- `INV-002`: Zero context items from outside `isolated_project_id`.
- `INV-005`: All assembled items retain `epistemic_provenance` and confidence.
- Principle P8: Total context tokens must not exceed budget.

## 13. Preconditions
- Target files and seed symbols must exist in the repository graph.
- Budget constraints must satisfy: $\text{max\_tokens} > \text{reserve\_for\_generation} + 500$.

## 14. Postconditions
- $\text{total\_tokens} \le \text{max\_tokens} - \text{reserve\_for\_generation}$.
- All items in `assembled_items` have non-empty `selection_audit.selection_reason`.

## 15. Failure Semantics
If target files cannot fit within the available token budget, the router emits `budget_exhausted: true` and `escalation_required: true` (Self-Route unanswerable escalation).

## 16. Security Requirements
- Adversarial files flagged with suspicious entropy or prompt-injection markers must be quarantined in `quarantined_exclusions`.
- Untrusted memory writes are excluded unless opt-in flag is enabled.

## 17. Observability Requirements
- Emits telemetry logging total candidate nodes evaluated, pruned count, admitted tokens, and budget utilization percentage.

## 18. Edge Cases
- Disconnected Graph Component: If seed symbol has no neighbors, router includes target file and falls back to lexical keyword retrieval.
- Exact Budget Boundary: Items are prioritized by proximity (distance 0 before distance 1 before distance 2).

## 19. Acceptance Criteria
### `AC-004-01` (Topological Pruning & Boundary Pinning)
```gherkin
Given a task targeting auth.py with neighbor db.py at 1 hop
When the context router assembles the MSC payload
Then auth.py must be included in full, db.py must be pruned to signatures/types, and CORE-CONTRACT-002 must be pinned at the boundary.
```

### `AC-004-02` (Auditable Selection Reason)
```gherkin
Given an assembled MSC payload with 5 items
When the payload is inspected
Then every item must have a populated selection_audit.selection_reason explaining its inclusion.
```

### `AC-004-03` (Token Budget Enforcement)
```gherkin
Given a routing request with max_tokens=4000 and reserve_for_generation=1000
When context assembly completes
Then total_tokens must be <= 3000 and budget_exhausted must be false.
```

## 20. Verification Strategy
Automated tests in `tests/specs/test_context_router.py` evaluating pruning ratios, boundary order preservation, and budget compliance.

## 21. Traceability
- Research: EVD-003, EVD-016
- ADR: `P2-ADR-002`
- Contract: `CTX-CONTRACT-001`
- Requirements: `REQ-CTX-001`, `REQ-CTX-002`, `REQ-CTX-003`

## 22. Open Questions & Phase 5 Notes
- Ranking weight calibration between graph centrality and lexical match is an open empirical experiment (`EXP-002`).
- Phase 5 note: Use deterministic source-order concatenation to preserve syntax context.
