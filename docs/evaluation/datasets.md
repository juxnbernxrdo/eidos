# Phase 7 Dataset Architecture & Corpus Specification

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** Controlled Software Engineering Corpora  
**Status:** VALIDATED DATASET CORPUS  

---

## 1. Corpus Overview

The evaluation utilizes a curated benchmark corpus composed of **10 self-contained software engineering environments** covering core software engineering patterns:

```text
Corpus Summary:
- Total Tasks: 10 Distinct Scenarios
- Programming Language: Python 3 (Typing, Pydantic, AST)
- Average Lines of Code per Task: 85 LOC (range: 25 to 190 LOC)
- Multi-file Tasks: 6 / 10 (60%)
- Security-Sensitive Tasks: 2 / 10 (20%)
- Pre-training Exposure: Exact 0.0% (Private synthetic benchmark)
```

---

## 2. Corpus Stratification by Dimension

### By Difficulty Bin:
- **SMALL (30%)**: Tasks `001`, `004`, `007`. Single-file or localized boundary condition / bug fixes.
- **MEDIUM (50%)**: Tasks `002`, `003`, `005`, `006`, `009`. Multi-file refactorings, contract renames, dependency decoupling, algorithm optimization.
- **LARGE (10%)**: Task `008`. Stateful event stream integration across decoupled modules.
- **SYSTEM (10%)**: Task `010`. End-to-end multi-gate system convergence with Feature Passports.

### By Engineering Task Classification:
1. `BUG_FIX`: `TSK-EVAL-001` (Paginated window off-by-one edge case)
2. `FEATURE_IMPL`: `TSK-EVAL-002` (Validated JSON event ingestion pipeline)
3. `REFACTORING`: `TSK-EVAL-003` (Shared token counter extraction with backward compatibility)
4. `SECURITY_FIX`: `TSK-EVAL-004` (Path traversal elimination via canonical realpath)
5. `CONTRACT_REPAIR`: `TSK-EVAL-005` (Schema field rename synchronization across producer/consumer)
6. `ARCH_INVARIANT_FIX`: `TSK-EVAL-006` (Breaking forbidden cross-layer import between core and cli)
7. `TEST_REPAIR`: `TSK-EVAL-007` (Eliminating flaky time-dependent test assertion)
8. `CROSS_MODULE_INTEGRATION`: `TSK-EVAL-008` (Idempotent event stream to state machine aggregator wiring)
9. `PERF_OPTIMIZATION`: `TSK-EVAL-009` (Replacing $O(N^2)$ linear search with $O(1)$ dictionary hash index)
10. `SYSTEM_INTEGRATION`: `TSK-EVAL-010` (Full multi-check convergence gate with Feature Passports)

---

## 3. Ground Truth & Oracle Construction

Each dataset scenario provides:
1. `initial_files`: Buggy or incomplete source code representing the starting state.
2. `ground_truth_patch`: Human-authored reference solution satisfying all requirements and invariants.
3. `public_tests`: Test cases exposed to the agent during prompt assembly.
4. `hidden_tests`: Held-out assertion suites evaluated post-run to verify edge-case coverage and screen false confidence.
5. `invariants`: Formal structural or security constraints enforced via static AST or dynamic supervisor checks.
