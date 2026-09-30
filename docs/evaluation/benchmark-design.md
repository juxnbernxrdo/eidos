# Benchmark Suite Design & Contamination Analysis

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** Custom Engineering Benchmark Protocol  
**Status:** VALIDATED BENCHMARK SPECIFICATION  

---

## 1. Benchmark Construction Principles

Traditional agentic benchmarks (e.g. standard SWE-bench) suffer from known limitations:
- High training set contamination and model memorization.
- Coarse binary test outcomes without structural or architectural invariant tracking.
- Heavyweight execution environments (Docker containers) with non-deterministic dependencies.

Eidos designs a dedicated, self-contained **10-Task Engineering Benchmark Suite** ([`src/eidos/evaluation/benchmark.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/evaluation/benchmark.py)) governed by four principles:

1. **Ecological Validity**: Tasks reflect the complete spectrum of engineering work: fixing boundary defects, implementing schema-validated pipes, refactoring shared modules, eliminating security traversals, repairing multi-file contracts, resolving architectural circularities, fixing brittle tests, wiring stateful streams, optimizing algorithmic lookups, and enforcing system convergence.
2. **Double-Blind Oracle Separation**:
   - **Public Tests**: Available to the agent during execution to mimic developer-written local unit tests.
   - **Hidden Tests**: Held-out tests evaluated only by the evaluation harness. These verify edge cases, boundary conditions, and prevent vacuous test passes.
3. **Architectural & Security Invariants**: Tasks evaluate not just functional output, but structural constraints (e.g. `ARCH-001` core isolation, canonical path confinement).
4. **Graded Complexity Stratification**: Tasks span four explicit complexity bins: `SMALL`, `MEDIUM`, `LARGE`, and `SYSTEM`.

---

## 2. Benchmark Task Inventory

| Task ID | Title | Category | Difficulty | Security Sensitive | Public Oracles | Hidden Oracles | Targeted Invariant |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---|
| `TSK-EVAL-001` | Paginated Window Boundary | Bug Fix | SMALL | No | 2 tests | 2 tests | `PAGINATION_BOUNDS` |
| `TSK-EVAL-002` | Validated Event Ingestion | Feature Impl | MEDIUM | No | 1 test | 3 tests | `EVENT_INGEST_STRICT_SCHEMA` |
| `TSK-EVAL-003` | Token Counter Refactoring | Refactoring | MEDIUM | No | 2 tests | 2 tests | `DRY_CODE_COMPATIBILITY` |
| `TSK-EVAL-004` | Path Traversal Elimination | Security Fix | SMALL | **Yes** | 1 test | 1 test | `SANDBOX_CONFINEMENT_REALPATH` |
| `TSK-EVAL-005` | Multi-File Contract Rename | Contract Repair | MEDIUM | No | 1 test | 1 test | `CONTRACT_SCHEMA_SYNCHRONY` |
| `TSK-EVAL-006` | Core/CLI Dependency Break | Arch Invariant | MEDIUM | No | 1 test | 1 test | `ARCH-001_CORE_ISOLATION` |
| `TSK-EVAL-007` | Flaky Timing Oracle Repair | Test Repair | SMALL | No | 1 test | 1 test | `DETERMINISTIC_TEST_ORACLE` |
| `TSK-EVAL-008` | Event Stream State Sync | Cross-Module | LARGE | No | 1 test | 2 tests | `IDEMPOTENT_EVENT_INTEGRATION` |
| `TSK-EVAL-009` | Hash Index Lookup Perf | Perf Opt | MEDIUM | No | 1 test | 2 tests | `SUB_LINEAR_INDEX_EFFICIENCY` |
| `TSK-EVAL-010` | Full Passport Convergence | System Int | SYSTEM | **Yes** | 1 test | 2 tests | `SYSTEM_LEVEL_CONVERGENCE_GATE` |

---

## 3. Contamination & Memorization Risk Audit

To ensure findings represent genuine reasoning rather than memorized GitHub solutions:
- **Zero Pre-training Exposure**: All 10 tasks, file structures, and tests were authored natively within the Eidos repository in 2026. None exist in public pre-training scrapes (e.g. Common Crawl, GitHub public repos prior to cutoff).
- **Novel Token Identifiers**: Function names, variable schemes, and error messages use unique project conventions not present in standard textbook problems.
- **Hidden Assertion Secrecy**: Hidden tests test edge cases (e.g. empty lists, future timestamps, symlink dereferences) that cannot be inferred solely from the prompt text without deep semantic reasoning.
- **Epistemic Classification**: `EVIDENCE` — Zero training set contamination verified.
