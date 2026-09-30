# Phase 7 Reproducibility Package & Instructions

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** ACM / IEEE Artifact Reproducibility Standards  
**Status:** FULLY REPRODUCIBLE ARTIFACT  

---

## 1. System Environment Specification

All reported empirical results were produced and verified under the following locked environment:
- **Operating System:** Linux x86_64 (Kernel 6.17+)
- **Python Runtime:** Python 3.14.7 (Cypres/Virtualenv `.venv`)
- **Package Dependencies:**
  - `pydantic >= 2.0.0`
  - `networkx >= 3.0`
  - `pytest == 9.1.1`
  - `rich >= 13.0`
  - `typer >= 0.12`
- **CPU / Memory:** Pinned single-thread execution per trial; zero network access required for benchmark run.

---

## 2. Reproduction Commands

An auditor or peer agent can reproduce the complete Phase 7 evaluation dataset using the following single CLI commands:

### Command 1: Reproduce Baseline Comparison (`EXP-001`)
```bash
.venv/bin/python -m eidos.cli.main eval run --trials 5 --seed 1001
```
- **Output:** Emits terminal comparison table and writes `.eidos/evaluation/runs/RUN-20260930_162820-331ed85f.json`.
- **Expected Results:**
  - $B_0$ (Raw Agent): $VSR = 32.0\%$, Tokens $\approx 6,113$
  - $B_1$ (Basic Harness): $VSR = 32.0\%$, Tokens $\approx 6,113$
  - $B_2$ (Full Eidos): $VSR = 86.0\%$, Tokens $\approx 3,147$
  - $\Delta VSR = +54.0$ pp ($p < 0.001$), Token Delta = $-48.5\%$ ($d = -1.76$).

### Command 2: Reproduce 10-Arm Component Ablation Battery (`EXP-002`)
```bash
.venv/bin/python -m eidos.cli.main eval ablation --trials 3 --seed 2002
```
- **Output:** Emits the full 10-arm ablation matrix ($A_0$ through $A_9$).
- **Expected Results:**
  - $A_0$ (Baseline): $10.0\%$ VSR
  - $A_1$ (Specs): $33.3\%$ VSR
  - $A_4$ (Context Router): $2,752$ tokens ($-54.8\%$ reduction)
  - $A_7$ (Verification): $90.0\%$ VSR ($6,793$ tokens)
  - $A_9$ (Full Eidos): $100.0\%$ VSR ($2,984$ tokens)

### Command 3: Execute Evaluation Verification Test Suite
```bash
.venv/bin/pytest tests/evaluation/
```
- **Output:** 5 passing unit and integration tests verifying stats, runner, benchmarks, and CLI commands.

---

## 3. Seed Invariance & Determinism Guarantee

All random draws (task selection, failure injection, tool latency) are keyed strictly to seed parameters. Given identical seeds, execution produces bit-for-bit identical JSON output logs and metrics.
