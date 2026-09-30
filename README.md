# Eidos — Engineering Intelligence for Deterministic, Orchestrated Software

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: SDD](https://img.shields.io/badge/Architecture-Specification--Driven-green.svg)](docs/architecture/ARCHITECTURE_PROPOSAL.md)

**Eidos** is an open-source, portable **Agentic Software Engineering Layer** developed by **Juan Bernardo Ordóñez**.

Eidos functions as the deterministic engineering harness that provides repository intelligence, specification governance, context routing, invariant verification, and cryptographic auditability across existing coding harnesses (Google Antigravity, Claude Code, OpenCode, Codex, Cursor, and Hermes Agent).

---

## Foundational Principle (Rule 0)
> **Eidos is the first system constructed using its own methodology.**  
> Google Antigravity serves as the primary development and verification harness.

---

## Core Capabilities

- **Project Discovery & Fingerprinting**: Non-destructive AST and dependency analysis.
- **Adaptive Requirements Interview**: Entropy-minimizing requirement discovery with explicit language policy confirmation.
- **Specification-Driven Development (SDD)**: Machine-validated specs, subspecs, and tasks.
- **Repository Intelligence Graph**: Heterogeneous code graph with community clustering (Louvain/Leiden) and God Node detection.
- **Context Routing**: Minimum Sufficient Context computation protecting models from context saturation.
- **Contract-Bounded Subagents**: Ephemeral, task-bounded agent execution with zero history contamination.
- **Verification-First Loop**: Deterministic test and invariant verification with bounded Reflexion repair.
- **Cryptographic Evidence & Feature Passports**: Tamper-evident commit traceability.
- **Architectural Invariants & Drift Detection**: Automated detection of `DOC-DRIFT`, `SPEC-DRIFT`, `ARCH-DRIFT`, and `CONTRACT-DRIFT`.

---

## Quickstart

```bash
# Initialize Eidos in your repository
eidos init

# Run system diagnostic
eidos doctor

# Non-destructive repository intelligence audit
eidos analyze

# Build and query the Repository Intelligence Graph
eidos graph build
eidos graph query "How does AuthMiddleware interact with TokenService?"

# Verify all architectural invariants and tests
eidos verify
```

---

## Documentation

- [Constitutional Principles](CONSTITUTION.md)
- [Agent Navigation Router](AGENTS.md)
- [System Architecture](docs/architecture/ARCHITECTURE_PROPOSAL.md)
- [Research Report](docs/research/01_RESEARCH_REPORT.md)
- [Architectural Decision Records (ADRs)](docs/adr/)
