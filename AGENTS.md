# AGENTS.md — Eidos Agent Navigation & Operating System

Welcome, Agent. You are operating within **Eidos — Engineering Intelligence for Deterministic, Orchestrated Software**.

Do not load all repository rules at once. This repository utilizes **Progressive Disclosure**. Follow the navigation links below to retrieve the minimum sufficient context required for your active task.

---

## 1. Operating Axioms & Constitution
Before executing any action, read and obey the foundational project principles:
- **Core Principles**: [CONSTITUTION.md](file:///home/juxnbernxrdo/Documentos/eidos/CONSTITUTION.md)
- **Foundational Axiom**: Eidos must be built using its own principles. Never bypass specifications or verification.

---

## 2. Documentation & System Router
Navigate to specific sub-systems using the targeted links below:

| Dimension | Primary Documentation / Router Path | Purpose |
|:---|:---|:---|
| **Research & Evidence** | [docs/research/01_RESEARCH_REPORT.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/01_RESEARCH_REPORT.md)<br>[docs/research/02_EVIDENCE_MATRIX.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/02_EVIDENCE_MATRIX.md) | Primary literature review and verified empirical findings. |
| **System Architecture** | [docs/architecture/ARCHITECTURE_PROPOSAL.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/ARCHITECTURE_PROPOSAL.md) | Complete conceptual pipeline, state machines, and context router. |
| **CLI & Layout** | [docs/architecture/CLI_AND_REPOSITORY_SPEC.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/CLI_AND_REPOSITORY_SPEC.md) | Command-line interface definitions and source repository structure. |
| **Machine Schemas** | [docs/architecture/SCHEMAS_SPECIFICATION.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/SCHEMAS_SPECIFICATION.md) | JSON Schema Draft 2020-12 definitions for all 18 entities. |
| **Invariants & Drift** | [docs/architecture/INVARIANTS_AND_DRIFT_SPEC.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/INVARIANTS_AND_DRIFT_SPEC.md) | Machine-checkable invariants (`ARCH-001`) and drift detection. |
| **Dependencies (DDR)** | [docs/architecture/DEPENDENCY_DECISION_RECORDS.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/DEPENDENCY_DECISION_RECORDS.md) | Dependency vetting policy and accepted package records. |
| **Risk Register** | [docs/architecture/RISK_REGISTER_AND_RESEARCH_GAPS.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/RISK_REGISTER_AND_RESEARCH_GAPS.md) | Hazard analysis, mitigations, and open research questions. |
| **Decisions (ADRs)** | [docs/adr/](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/) | Canonical ADR location: ADR-001 through ADR-008 (historical) + P2-ADR-001 through P2-ADR-008 (Phase-2 baseline, binding). |

---

## 3. Subagent Operating Instructions (Contract-Bounded)
1. **Fresh Context**: Do not rely on conversational assumptions. Read your assigned `task_id` and `spec_id`.
2. **Read-First**: Query the relevant files and AST signatures before proposing any code edits.
3. **No Vibe Coding**: Never implement a change without verifying it satisfies an active specification.
4. **Verification-First**: After any edit, run the designated verification test suite:
   ```bash
   pytest tests/
   ```
5. **Report Truthfully**: If a test or invariant check fails, report the exact error trace. Never state "Done" until all verifications pass deterministically.
