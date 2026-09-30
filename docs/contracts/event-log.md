# Event Log Contract (`EVENT-CONTRACT-001`)

**Contract ID:** `EVENT-CONTRACT-001`  
**Version:** 1.0.0  
**Status:** ACCEPTED  
**Owner Domain:** Progress  
**Machine Schema:** [`event-log.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/events/event-log.schema.json)  
**Architecture Basis:** [P2-ADR-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-007-progress-passports-evolution.md), [progress.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/progress.md), [data-model.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/data-model.md), [EVD-015](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md)

---

## 1. Purpose & State Fold Axiom

The `EventLog` contract establishes the append-only persistence layer that guarantees complete reproducibility, auditability, and ablation tracking for all Eidos operations.

### Foundational State Fold Axiom:
> Current system state is never stored as an unanchored mutable blob. State is formally defined as the deterministic left-fold of historical events over the initial state:
> $$S_t = \text{Fold}(S_0, [e_1, e_2, \dots, e_t])$$
> `.eidos/progress/events.jsonl` is the sole ground truth. Any `state.json` or progress dashboard is strictly an ephemeral projection.

---

## 2. Event Envelope & Field Necessity Justification

Every event emitted in Eidos contains exactly the minimum fields required for auditable reconstruction:

| Field | Necessity Justification | Epistemic Rule |
|---|---|---|
| `event_id` | Monotonic ordering and hash-chaining; prevents reordering or deletion attacks. | System generated. |
| `timestamp` | Standard UTC ISO-8601 timestamp for temporal latency and timeout accounting. | Machine clock. |
| `event_type` | Strict closed enum defining the exact architectural transition occurring. | Categorical. |
| `actor` | Attributes action to `HUMAN`, `AGENT` (with ID), `HARNESS`, or `SYSTEM`. | Attribution. |
| `session_id` | Binds operations within an active interactive or autonomous session. | Boundary. |
| `project_id` | Enforces `INV-002`; prevents mixing events across distinct repositories. | Boundary. |
| `git_commit` | Anchors event to the physical Git HEAD commit SHA (Constitution Art. VIII). | Cryptographic anchor. |
| `payload` | Typed payload containing specific parameters, diffs, or verification traces. | Event-specific. |
| `provenance` | Epistemic tag (`EXTRACTED`, `OBSERVED`, `USER_CONFIRMED`, `AGENT_PROPOSED`). | Honesty axiom. |
| `schema_version` | Enables backward-compatible replay across contract version upgrades. | SemVer. |
| `supersedes_event_id` | (Optional) Explicitly points to an earlier event corrected by this event. | Supercession pointer. |

---

## 3. Log Operations & Semantics

The contract defines five core operations:

1. **`append(event)`**: Appends a validated event to the active log. Fails closed if the event does not conform to `event-log.schema.json`.
2. **`read(since_event_id, limit)`**: Sequentially streams events for audit, reporting, or subagent briefing.
3. **`replay(from_event_id, to_event_id)`**: Evaluates the state fold function over an event range to reconstruct historical state at any point in time.
4. **`query(filters)`**: Retrieves targeted events filtered by `session_id`, `actor`, `event_type`, or `git_commit`.
5. **`snapshot()`**: Checkpoints the projected state together with the highest folded `event_id`, enabling fast resume without scanning from $e_0$.

---

## 4. Immutability & Supercession Rules

1. **Zero Deletion / Zero In-Place Mutation**: Modifying or removing past lines in `events.jsonl` is a catastrophic contractual violation.
2. **Corrections via New Events**: If an error, flawed patch, or invalid finding was recorded in event $e_k$, the correction must be appended as a new event $e_{k+n}$ of type `SUPERSEDING_CORRECTION` specifying `supersedes_event_id = e_k`.
3. **Audit Trails**: Forensic diffs between $e_k$ and $e_{k+n}$ preserve why the correction was made.

---

## 5. Architectural Invariants Bound

- **INV-002 (Cross-Project Isolation)**: `project_id` must match workspace configuration; cross-repo event injection is rejected.
- **INV-004 (Auditable Self-Improvement)**: All modifications to prompt rules, skills, or pipeline parameters must emit auditable events.
- **INV-005 (Provenance Preservation)**: Every event records explicit provenance; ungrounded assertions are flagged.

---

## 6. Phase 4 Handoff

Phase 4 will specify:
- Concrete JSONL serialization and file locking semantics for multi-process safety.
- Projection reducers for `TaskPassport` and `EvaluationRun` generation.
- Log compaction and snapshot retention policies.
