# Baseline Architecture & Fair Comparison Specifications

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** Comparative Methodology Guidelines  
**Status:** VALIDATED BASELINES  

---

## 1. Baseline Design Principles

To establish whether observed improvements are genuinely caused by Eidos rather than general model capabilities or trivial prompting differences, Phase 7 defines three primary comparative baselines:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ B0 — Raw Agent                                                         │
│   • Model + Bash / Filesystem                                          │
│   • Full unpruned context dumping                                      │
│   • Self-reporting completion (Zero automated verification gating)     │
├────────────────────────────────────────────────────────────────────────┤
│ B1 — Agent + Basic Scaffolding                                         │
│   • Model + Standard File Tools + Grep Search                          │
│   • Discretionary test running (Agent decides if/when to verify)       │
│   • No graph engine, no contract schemas, unguided retries             │
├────────────────────────────────────────────────────────────────────────┤
│ B2 — Agent + Full Eidos Stack                                          │
│   • Phased pipeline (INIT -> SPECIFY -> IMPLEMENT -> VERIFY)           │
│   • Context Router (Heterogeneous graph k<=2 + boundary pinning)       │
│   • Non-bypassable verification gate + oracle bounded repair (K<=5)    │
│   • Policy-as-Physics sandbox & secret redaction                       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Granular Baseline Specification

### Baseline `B0`: Raw Agent (Unassisted Execution)
- **Component Stack**: Direct model prompt + standard shell commands (`cat`, `echo`, `python`).
- **Context Mechanism**: The agent is provided the raw task description and entire unpruned source files.
- **Verification Loop**: None. The agent self-reports completion (`"Done"`, `"Fixed"`). No verification tests are executed unless the model explicitly writes and runs a bash command.
- **Error Recovery**: None. If the agent issues a flawed patch, execution terminates immediately.
- **Justification**: Represents the bare-bones baseline common in early autonomous agent benchmarks.

### Baseline `B1`: Agent + Basic Harness (Scaffolding Tooling)
- **Component Stack**: Model wrapped in standard tool-dispatch harness (structured `read_file`, `write_file`, `run_command`).
- **Context Mechanism**: Keyword matching / Grep-based search. No graph topology or dependency closures.
- **Verification Loop**: Discretionary. The harness provides a `test` tool, but does not enforce a gate: the agent may declare completion even if tests fail or were never run.
- **Error Recovery**: Unguided retry loop without formal oracle diagnostic localization.
- **Justification**: Represents commercial IDE coding assistants and standard coding harness wrappers.

### Baseline `B2`: Agent + Full Eidos Harness
- **Component Stack**: Complete Eidos Architecture ([`PhasedPipeline`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/orchestration/pipeline.py), [`ContextRouter`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/context/router.py), [`RepositoryGraphEngine`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/graph/engine.py), [`run_verification`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/verification/runner.py), [`SandboxSupervisor`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/security/supervisor.py)).
- **Context Mechanism**: Minimal Sufficient Context (MSC) dynamically extracted from the AST dependency graph ($k \le 2$ neighborhood) with boundary-pinned invariants and strict token budget enforcement.
- **Verification Loop**: Hard non-bypassable verification gating. When tests fail, oracle diagnostic traces are fed into a bounded repair loop ($K \le 5$). If $K > 5$, execution escalates deterministically.
- **Security & Integrity**: Canonical `os.path.realpath` confinement, multi-provider secret scrubbing, POSIX-locked append-only event logging.
- **Justification**: Realizes the full engineering intelligence harness hypothesis.

---

## 3. Strict Fair Comparison Controls

To prevent confounding variables:
1. **Model Invariance**: $B_0$, $B_1$, and $B_2$ evaluate the identical model checkpoint (`claude-3-5-sonnet-20241022`) under identical temperature ($T=0.0$).
2. **Resource Parity**: Identical maximum token ceiling ($8,000$ tokens/task) and timeout limits ($60$ seconds).
3. **Problem Statement Parity**: All three arms receive the identical task description and initial file contents.
4. **Oracle Secrecy**: Neither $B_0$, $B_1$, nor $B_2$ is provided with the hidden held-out tests or ground-truth reference patches.
