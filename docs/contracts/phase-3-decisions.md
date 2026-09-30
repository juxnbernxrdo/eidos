# Phase 3 Contract Decisions Log

**Status:** ACCEPTED  
**Authority:** Canonical Phase 3 Contract Decision Record  
**Rule:** No decision may alter Phase 2 architecture silently. Any decision requiring new architecture requires `ARCHITECTURAL ESCALATION REQUIRED`.

---

## Decision Record Index

- `P3-DEC-001`: Adopt JSON Schema Draft 2020-12 as Canonical Machine Contract Standard
- `P3-DEC-002`: Explicit HarnessAdapter Method Categorization (Drop `verify` from Adapter Duties)
- `P3-DEC-003`: Mandatory Auditable Selection Rationale in ContextRouter MSC Payloads
- `P3-DEC-004`: Minimal 12-Dimensional Contractual Feature Passport Schema
- `P3-DEC-005`: Advisory-First Invariant Classification Pre-Calibration (Preserving ARR-02)

---

## Detailed Records

### `P3-DEC-001`: Adopt JSON Schema Draft 2020-12 as Canonical Machine Contract Standard
- **Decision:** All machine-readable contracts are formalized as JSON Schema Draft 2020-12 specifications under `schemas/contracts/`.
- **Reason:** Universally parseable across diverse host harness environments (TypeScript, Python, Go, Rust), compatible with Pydantic v2 in Python Core and standard JSON Schema validators across CLI tools.
- **Architecture Basis:** `docs/architecture/SCHEMAS_SPECIFICATION.md`, Constitution Art. II.
- **Research Basis:** EVD-001, EVD-006 (strict schemas prevent agent hallucinations and tool calling drift).
- **Alternatives:** Protocol Buffers (rejected: requires compilation step), Python-only dataclasses (rejected: violates language-neutral contract requirement).
- **Trade-offs:** Verbose schema declarations vs cross-harness interoperability.
- **Status:** `ACCEPTED`
- **Future Impact:** Phase 4 specifications and Phase 5 implementations must use these schemas as validation gates.

---

### `P3-DEC-002`: Explicit HarnessAdapter Method Categorization
- **Decision:** Formally categorize adapter operations: `detect`, `capabilities`, `configure`, `invoke`, `collect_output`, `collect_trace` as `REQUIRED`; `install` as `OPTIONAL`; `verify` is `DROPPED` from the adapter domain.
- **Reason:** Verification belongs strictly to the Verifier domain (Principle P5). Allowing adapters to self-certify introduces false convergence risk and provider bias.
- **Architecture Basis:** `docs/architecture/harness.md`, `P2-ADR-005`.
- **Research Basis:** EVD-009 (oracle necessity), EVD-015 (test suite inflation).
- **Alternatives:** Allowing adapters to run their own internal test suites and return certified status.
- **Trade-offs:** Clear separation of concerns; prevents host cheating.
- **Status:** `ACCEPTED`
- **Future Impact:** Phase 4 harness bridge specifications will strictly implement trace collection; verification will be performed externally by Verifier.

---

### `P3-DEC-003`: Mandatory Auditable Selection Rationale in ContextRouter MSC Payloads
- **Decision:** Mandate that every item assembled in a Minimal Sufficient Context payload (`assembled_items[]`) contain a structured `selection_audit` object detailing `selection_reason` and `proximity_hops`.
- **Reason:** To combat the "Lost-in-the-Middle" phenomenon (EVD-003) and allow rigorous ablation of context utility, every item's inclusion must be accountable.
- **Architecture Basis:** `docs/architecture/context.md`, `P2-ADR-002`.
- **Research Basis:** EVD-003, EVD-016 (Self-Route and source-order assembly).
- **Alternatives:** Opaque vector relevance floats without semantic rationale.
- **Trade-offs:** Modest schema metadata overhead vs complete auditability and reproducible ablation.
- **Status:** `ACCEPTED`
- **Future Impact:** Context routing algorithms in Phase 4 must output explicit audit rationales.

---

### `P3-DEC-004`: Minimal 12-Dimensional Contractual Feature Passport Schema
- **Decision:** Define the Feature Passport as a minimal 12-dimensional contractual schema (`CORE-CONTRACT-010`) linking Requirement, Spec, Architecture, Dependencies, Contracts, Implementation, Tests, Security, Documentation, Evidence, Git, and Verification.
- **Reason:** To enable inter-phase traceability without premature implementation of the full runtime passport projection engine.
- **Architecture Basis:** `docs/architecture/data-model.md §4`, `P2-ADR-007`.
- **Research Basis:** EVD-015 (reproducibility need), EVD-018 (gated evolution).
- **Alternatives:** Delaying the passport schema to Phase 5 or building a heavy database model in Phase 3.
- **Trade-offs:** Provides unambiguous contract boundary now without violating the Phase 3 no-implementation rule.
- **Status:** `ACCEPTED`
- **Future Impact:** Provides the formal input structure for Phase 4 specification.

---

### `P3-DEC-005`: Advisory-First Invariant Classification Pre-Calibration (ARR-02)
- **Decision:** Formalize invariants INV-001 through INV-010 as `CONTRACT_BOUND`, but maintain their enforcement level as `ADVISORY` by default until empirical calibration in Phase 6/7.
- **Reason:** Hard blocking enforcement of uncalibrated invariant heuristics risks false-block regressions and developmental deadlocks.
- **Architecture Basis:** `docs/architecture/invariants.md`, Constitution Art. IV.
- **Research Basis:** ARR-02, EVD-012.
- **Alternatives:** Making all invariants immediately blocking.
- **Trade-offs:** Safe developmental progression vs requiring human vigilance during Phase 3-5.
- **Status:** `ACCEPTED`
- **Future Impact:** Blocking thresholds will be activated only after EXP-006 calibration.
