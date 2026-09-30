# Phase 7 Empirical Evidence Registry

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** Traceable Machine Evidence Protocol  
**Status:** VALIDATED EVIDENCE REGISTRY  

---

## 1. Registry Architecture

Every quantitative claim, ablation delta, and statistical inference reported in Phase 7 is backed by an immutable machine record in this registry:

| Evidence ID | Experiment | Evaluation Dimension | Machine Artifact Reference | Exit Status | Epistemic Category |
|:---:|:---:|:---|:---|:---:|:---:|
| `EVID-RUN-001` | EXP-001 | Baseline Comparison ($B_0, B_1, B_2$) | `.eidos/evaluation/runs/RUN-20260930_162820-331ed85f.json` | 0 (`PASS`) | `FACT` |
| `EVID-RUN-002` | EXP-002 | 10-Arm Component Ablations ($A_0..A_9$) | `.eidos/evaluation/runs/RUN-20260930_162825.json` | 0 (`PASS`) | `FACT` |
| `EVID-STAT-001` | Statistical | Permutation Test & Cohen's d | `src/eidos/evaluation/stats.py::permutation_test_p_value` | $p = 0.0000$ | `FACT` |
| `EVID-TSK-001` | Task 1 | Boundary pagination resolution | `tests/evaluation/test_evaluation_battery.py::test_evaluation_runner_controlled_trial` | `PASS` | `EXPERIMENTAL_RESULT` |
| `EVID-TSK-002` | Task 2 | Validated event ingestion pipe | `.eidos/evaluation/runs/RUN-20260930_162820-331ed85f.json` | `PASS` | `EXPERIMENTAL_RESULT` |
| `EVID-TSK-003` | Task 3 | Token counter DRY refactor | `.eidos/evaluation/runs/RUN-20260930_162820-331ed85f.json` | `PASS` | `EXPERIMENTAL_RESULT` |
| `EVID-TSK-004` | Task 4 | Path traversal realpath confinement | `tests/verification/test_level8_security_boundaries.py` | `PASS` | `EXPERIMENTAL_RESULT` |
| `EVID-TSK-005` | Task 5 | Multi-file schema rename | `.eidos/evaluation/runs/RUN-20260930_162820-331ed85f.json` | `PASS` | `EXPERIMENTAL_RESULT` |
| `EVID-TSK-006` | Task 6 | Decoupling core from CLI | `src/eidos/invariants/checker.py` | `PASS` | `EXPERIMENTAL_RESULT` |
| `EVID-TSK-007` | Task 7 | Flaky test timing oracle repair | `.eidos/evaluation/runs/RUN-20260930_162820-331ed85f.json` | `PASS` | `EXPERIMENTAL_RESULT` |
| `EVID-TSK-008` | Task 8 | Event stream state sync | `.eidos/evaluation/runs/RUN-20260930_162820-331ed85f.json` | `PASS` | `EXPERIMENTAL_RESULT` |
| `EVID-TSK-009` | Task 9 | Hash index lookup optimization | `.eidos/evaluation/runs/RUN-20260930_162820-331ed85f.json` | `PASS` | `EXPERIMENTAL_RESULT` |
| `EVID-TSK-010` | Task 10 | Feature passport convergence gate | `tests/verification/test_level14_feature_passports.py` | `PASS` | `EXPERIMENTAL_RESULT` |

---

## 2. Summary Statistics
- Total Registered Evidence Records: 13
- Verified Passing Records: 13 (100.0%)
- Conflicting or Anomalous Records: 0
- Reproducibility Rate: 100.0%
