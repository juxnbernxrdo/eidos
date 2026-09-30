# SPEC-011 — Tripartite Memory Boundaries & Opt-in Admission Gates

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavioral boundaries and admission gates for the Tripartite Memory subsystem: ensuring working, project, and institutional memory tiers remain isolated and that persistent memory is strictly opt-in to prevent contamination cascades.

## 3. Scope
Memory tier boundaries, write-time admission filtering, sanitization rules, and cross-project isolation.

## 4. Non-Goals
- Does not implement vector databases or semantic retrieval engines.
- Does not permit autonomous un-audited memory writes across project boundaries.
- Does not enable memory by default (`opt-in only` rule).

## 5. Source Requirements
- `REQ-MEM-001`: Tripartite Memory Scoping
- `REQ-MEM-002`: Opt-In Gating for Persistent Memory

## 6. Architectural Basis
- `docs/architecture/memory.md`: Tiers, rules, and contamination prevention.
- `docs/adr/P2-ADR-004`: Tripartite memory isolation and opt-in policy (`ARR-01`).
- `docs/research/evidence-registry.md`: EVD-017 (dialogue memory gains vs $\rho$-contamination cascades).

## 7. Contract Dependencies
- `CORE-CONTRACT-001`: Project Contract.
- `CORE-CONTRACT-008`: Capability & Permission Contract.

## 8. Behavioral Requirements
The memory subsystem enforces three strictly bounded tiers:
1. **Working Memory**: Subtask lifetime, in-memory, destroyed upon subtask termination.
2. **Project Memory**: Repository lifetime, git-tracked in `.eidos/memory/`, strictly scoped to the local repo.
3. **Institutional Memory**: Cross-project lifetime, stored in `~/.eidos/institutional/`, human-approved only.
Persistent memory is **disabled by default**. When enabled via project configuration, writes must pass a consistency admission gate to prevent hallucinated facts from entering long-term stores.

## 9. Inputs
- Memory write candidate: Key, content, epistemic status, source task ID.
- Memory query: Keyword / symbol filter, project ID.

## 10. Outputs
- On Write: Admission decision (`ACCEPTED` or `REJECTED_CONTAMINATION`) and write hash.
- On Query: Filtered snippets tagged with provenance.

## 11. State Model
```text
[CANDIDATE WRITE] ──► [OPT-IN CHECK] ──► [CONSISTENCY GATE] ──► [ADMITTED]
                            │                     │
                            ▼                     ▼
                        [REJECTED]           [QUARANTINED]
```

## 12. Invariants
- `INV-002`: Zero cross-project memory leakage without explicit human authorization.
- `INV-005`: All admitted memory items must retain their origin provenance and confidence score.

## 13. Preconditions
- Persistent memory writes require explicit `opt_in_memory: true` in `.eidos/project.json`.

## 14. Postconditions
- Admitted project memories are committed as versioned JSON records in `.eidos/memory/`.

## 15. Failure Semantics
Attempting to write to institutional memory without human cryptographic signing triggers an immediate `PERMISSION_DENIED` violation.

## 16. Security Requirements
- Project memory is strictly confined to the local repository filesystem.
- Secrets, passwords, or personal credentials must be rejected by sanitization regex filters prior to admission.

## 17. Observability Requirements
- Emits telemetry on memory queries, cache hits, rejected write candidates, and cascade risk metrics ($\rho$).

## 18. Edge Cases
- Contradictory memory writes: If a new candidate contradicts an existing memory entry, the gate records a conflict and requires operator resolution.
- Institutional export: Exporting project heuristics to institutional tier strips all repo-specific paths and symbol names.

## 19. Acceptance Criteria
### `AC-011-01` (Default Opt-In Gating)
```gherkin
Given a project initialized with default configuration (opt_in_memory=false)
When a subagent attempts to persist an insight to project memory
Then the memory subsystem ignores the write and emits an advisory notice.
```

### `AC-011-02` (Cross-Project Isolation)
```gherkin
Given two distinct repositories Repo-A and Repo-B
When a memory query is executed in Repo-A
Then the query result contains only memories created within Repo-A and zero records from Repo-B.
```

## 20. Verification Strategy
Automated tests in `tests/specs/test_memory_gating.py` verifying opt-in enforcement, cross-project data boundaries, and ephemeral working memory destruction.

## 21. Traceability
- Research: EVD-017
- ADR: `P2-ADR-004`
- Contract: `CORE-CONTRACT-001`, `CORE-CONTRACT-008`
- Requirements: `REQ-MEM-001`, `REQ-MEM-002`

## 22. Open Questions & Phase 5 Notes
- Admission confidence threshold $\tau$ remains an open calibration constant (`ARR-03`, `EXP-005`).
- Phase 5 note: Project memory should be implemented as human-readable Markdown/JSON files tracked in git.
