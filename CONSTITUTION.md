# CONSTITUTION.md — Eidos Core Principles & Governance

**Project:** Eidos — Engineering Intelligence for Deterministic, Orchestrated Software  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** Immutable Foundational Governance Document  

---

## Article I: The Self-Referential Axiom (Rule 0)
1. **Self-Demonstrating Methodology**: Eidos must be built strictly using the same principles, specifications, invariants, verification loops, and governance that Eidos enforces on other systems.
2. **First Harness**: Google Antigravity serves as the primary development and verification harness for Eidos.
3. **No Unenforced Rules**: Any architectural constraint declared for external projects must be applied and tested against the Eidos repository itself.

---

## Article II: Architectural Principles
1. **Separation of Concerns**: Core domain logic (`src/eidos/core/`) must remain pure, deterministic, and free of I/O, network, or harness-specific dependencies.
2. **Directional Dependency**: Core $\leftarrow$ Contracts $\leftarrow$ Subsystems (Intelligence, Graph, Context) $\leftarrow$ Adapters (Harnesses) $\leftarrow$ CLI. Inward dependencies only.
3. **Machine-Readable Truth**: All critical data structures must possess a validated JSON Schema. Markdown serves human readability; JSON/Pydantic serves machine verification.

---

## Article III: Security Principles
1. **Policy-as-Physics**: Security cannot rely on natural language model instructions. Process, filesystem, and network isolation must be enforced via OS primitives (Linux Landlock, namespaces, read-only mounts).
2. **Zero Unaudited Skills**: Every third-party skill must undergo static AST analysis, YARA scanning, and risk scoring ($< 25$) before installation.
3. **Data Isolation**: Zero implicit cross-project data leakage. Project memory remains locked within the local repository; institutional memory requires explicit sanitization and human approval.

---

## Article IV: Testing & Verification-First Mandate
1. **Deterministic Done**: No task or feature may transition to `DONE` without machine-verified evidence: passing unit/integration tests, 0 type errors, 0 linter violations, and 0 architectural invariant violations.
2. **Reflexion Bounding**: Automated repair loops are strictly capped at $K = 5$ iterations to prevent runaway token expenditure. Unconverged tasks escalate to a human engineer with full diagnostic diffs.
3. **Invariant Enforcement**: Every pull request and release must pass `eidos invariant check`.

---

## Article V: Dependency Engineering Policy
1. **Necessity First**: Dependencies are forbidden if the functionality can be implemented cleanly in $< 150$ lines of tested native code.
2. **License Purity**: Only OSI-approved permissive licenses (`MIT`, `Apache-2.0`, `BSD`) are permitted in core libraries. Copyleft licenses (`GPL`, `AGPL`) are strictly banned.
3. **Documented Rationale**: Any core dependency must have a corresponding Dependency Decision Record (DDR).

---

## Article VI: Coding & Error Handling Standards
1. **Modern Python**: Codebase targets Python 3.11+. Strict static typing (`mypy` / `pyright` strict mode) is mandatory across all modules.
2. **Explicit Errors**: No generic `except Exception: pass`. All exceptions must be explicitly typed domain exceptions derived from `EidosError`.
3. **Immutability Where Feasible**: Data contracts and events must be modeled as frozen Pydantic models or dataclasses.

---

## Article VII: Documentation & Language Policy
1. **Living Documentation**: Documentation must be kept in sync with code at all times. `DOC-DRIFT` is treated as a blocking CI failure.
2. **Progressive Disclosure**: Documentation must follow a hierarchical router pattern. No monolithic rule dumping.
3. **Language Policy**: Technical documentation for Eidos is maintained in English for international open-source contribution, while the interactive interview engine dynamically respects and confirms the developer's language preference.

---

## Article VIII: Git & Progress Standards
1. **Event-Sourced Traceability**: Every significant agent action, patch, and verification run must append an immutable event to `.eidos/progress/events.jsonl` anchored to the Git HEAD commit.
2. **Atomic Commits**: Git commits must correspond 1:1 with converged Feature Passports or validated subtasks.

---

## Article IX: AI Agent Operating Protocol
1. **Contract-Bounded Subagents**: Subagents must be spawned with fresh context and an explicit task contract. Subagents must never inherit messy conversational history.
2. **Honesty Axiom**: An agent must never classify an inference as a fact. The Repository Graph must strictly distinguish `EXTRACTED` compiler facts from `INFERRED` LLM hypotheses.
