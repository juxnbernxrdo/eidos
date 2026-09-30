# Context Router Contract (`CTX-CONTRACT-001`)

**Contract ID:** `CTX-CONTRACT-001`  
**Version:** 1.0.0  
**Status:** ACCEPTED  
**Owner Domain:** Context  
**Machine Schema:** [`context-router.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/context/context-router.schema.json)  
**Architecture Basis:** [P2-ADR-002](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-002-graph-msc-router.md), [context.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/context.md), [EVD-003](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [EVD-016](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md)

---

## 1. Purpose & Core Architectural Axiom

The `ContextRouter` contract establishes the formal protocol for assembling **Minimal Sufficient Context (MSC)**.

### Architectural Axiom (Principle P8):
> **More context is NOT better.** Full repository dumps cause severe retrieval degradation (EVD-003 "Lost-in-the-Middle" U-curve) and inflate execution costs 8–13× (EVD-001). Context must be deliberately pruned, strictly budgeted, and posited in deterministic source order.

---

## 2. Context Sources & Epistemic Boundaries

The router draws upon bounded knowledge sources under strict epistemic ranking:

| Source Domain | Epistemic Status | Content Pruning Rule | Priority |
|---|---|---|---|
| **Graph Nodes (Target)** | `EXTRACTED` (1.0) | Complete implementation and AST bodies. | Highest |
| **Graph Nodes ($k \le 2$ Neighbors)** | `EXTRACTED` (1.0) | Pruned to **signatures, type annotations, and contract docstrings**. | High |
| **Pinned Contracts & Rules** | `EXTRACTED` (1.0) | Pinned at prompt boundary (start/end) to combat attention fade. | Critical |
| **Specifications & Acceptance Criteria** | `USER_CONFIRMED` | Complete criteria text for the assigned task. | High |
| **Evidence & Oracle Traces** | `EXTRACTED` / `OBSERVED` | Test failure stdout/stderr for targeted repair. | High |
| **Memory (Project Tier)** | `USER_CONFIRMED` | Admitted **only** if opt-in flag is enabled (ARR-01). | Low |
| **Agent Inferences** | `INFERRED` | Summaries tagged with confidence; excluded from blocking paths. | Low / Quarantined |

---

## 3. Auditable Selection Requirement

The contract enforces that **every assembled item must justify why it was selected**. 

In `assembled_items[].selection_audit`, the router must record:
- `selection_reason`: Machine-readable classification (e.g., `TARGET_SCOPE`, `K1_NEIGHBOR_DEPENDENCY`, `PINNED_BOUNDARY_INTERFACE`, `FAILED_VERIFICATION_ORACLE`).
- `proximity_hops`: Distance in the repository graph ($0$ for target, $1$ or $2$ for adjacent modules).
- `matched_query`: The specific symbol or contract dependency that triggered retrieval.

---

## 4. Pruning, Budgeting & Quarantine Semantics

1. **Hard Token Budgeting**: Total token count must strictly remain within `max_tokens - reserve_for_generation`.
2. **Deterministic Source-Order Assembly**: Items are emitted in topological source order (OP-RAG pattern, EVD-016), **never** score-sorted arbitrary dumps.
3. **Quarantine & Exclusions**: When candidates cannot be safely admitted, they are emitted in `quarantined_exclusions` with a formal reason:
   - `EXCEEDED_TOKEN_BUDGET`: Excluded to protect the generation window.
   - `POISONED_FILE_FLAG`: Quarantined due to adversarial or unverified surface.
   - `UNCONFIRMED_INFERENCE`: Quarantined because an unverified inference attempted to override an extracted fact.
   - `CROSS_PROJECT_ISOLATION`: Blocked by INV-002 cross-project boundary.
   - `UNAUTHORIZED_MEMORY`: Blocked because memory opt-in is disabled.
4. **Escalation Signal**: If critical target symbols cannot fit in the budget or context is provably unanswerable, `escalation_required = true` is emitted (Self-Route pattern).

---

## 5. Architectural Invariants Bound

- **INV-002 (Cross-Project Isolation)**: ContextRouter cannot query or inject nodes outside `isolated_project_id`.
- **INV-005 (Provenance Preservation)**: Every assembled item carries its explicit provenance tag and confidence value.
- **P8 (Minimal Sufficient Context)**: Full-repo dumping is contractually prohibited.

---

## 6. Open Constants & Phase 4 Handoff

The following constants remain open `DESIGN_CHOICE` values to be calibrated in Phase 7 (EXP-002):
- Default token budget ($k$-bound value: $k \le 2$).
- Specific ranking weight constants between semantic proximity and graph centrality.

Phase 4 will specify:
- Concrete tokenizer integrations.
- Serialization formatting for prompt template engines.
- Cache-breakpoint boundary specifications for prompt caching.
