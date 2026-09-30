# Evolution Governance Framework

**Authority:** Eidos System Constitution Article IV & SPEC-014  
**Scope:** Gated Self-Improvement Protocol, Sandboxed Experimentation, and Human Approval Gates  
**Status:** BINDING GOVERNANCE STANDARD  

---

## 1. Foundational Axiom & Non-Goals

> **"Eidos implements Policy-as-Physics: autonomous, unconstrained runtime self-modification is prohibited-by-default (ARR-04, INV-004)."**

Software systems that modify their own prompts, code, or routing weights in an unconstrained autonomous loop inevitably suffer from catastrophic drift, regression cascades, and reward hacking. Eidos strictly separates **experimental self-optimization** from **production ratification**.

### Non-Goals of Evolution:
- Eidos does NOT permit autonomous, unsupervised prompt rewriting in production.
- Eidos does NOT allow subagents or pipelines to bypass human review gates.
- Eidos does NOT train foundation model weights.
- Eidos does NOT weaken invariants or contract schemas to satisfy failing tasks.

---

## 2. The 7-Stage Gated Evolution Lifecycle

Every evolution candidate must traverse seven immutable stages before any line of production code or rule configuration is altered:

```text
┌────────────────────────────────────────────────────────┐
│ Stage 1: Observation      (Event Log / Benchmark Trace)│
├────────────────────────────────────────────────────────┤
│ Stage 2: Proposal         (Formal LearningProposal)    │
├────────────────────────────────────────────────────────┤
│ Stage 3: Evidence Binding (Attached Failure Traces)    │
├────────────────────────────────────────────────────────┤
│ Stage 4: Sandboxed Run    (Isolated Execution Sandbox) │
├────────────────────────────────────────────────────────┤
│ Stage 5: Eval & Regression(Automated ΔVSR Verification)│
├────────────────────────────────────────────────────────┤
│ Stage 6: Human Approval   (Cryptographic Operator Sign)│
├────────────────────────────────────────────────────────┤
│ Stage 7: Versioned Release(SemVer Git Ratification)    │
└────────────────────────────────────────────────────────┘
```

### Stage Transitions:
- `PROPOSED → TESTING`: Candidate diff isolated in ephemeral worktree.
- `TESTING → EVALUATED`: Evaluation battery runs. If regressions occur, immediately transition to `REJECTED`.
- `EVALUATED → HUMAN_REVIEW`: Automated pass; proposal remains **strictly unapplied** pending human decision.
- `HUMAN_REVIEW → ACCEPTED`: Operator reviews diff and signs with operator credentials.
- `HUMAN_REVIEW → REJECTED`: Operator vetoes proposal with diagnostic rationale.

---

## 3. Direct Modification Interception (`INV-004`)

Any attempt by a running agent, subagent, or external script to modify protected governance files directly is intercepted and blocked:
- **Protected Files**: `AGENTS.md`, `CONSTITUTION.md`, `pyproject.toml`, `.eidos/project.json`, `.eidos/skills-lock.json`, `src/eidos/core/`.
- **Enforcement Mechanism**: [`EvolutionPipeline.intercept_direct_modification`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/evolution/pipeline.py) raises `PermissionDeniedError` with error code `INV-004` and logs an immutable security event.

---

## 4. Allowable vs Prohibited System Modifications

| Modification Type | Classification | Governing Procedure |
|:---|:---:|:---|
| **Pipeline Parameter Calibration** (e.g. $K_{max}$, early-stopping threshold) | **Permitted** | 7-Stage Pipeline with Benchmark Delta |
| **Context Routing Heuristics** (e.g. hop radius $k=2$, token allocation) | **Permitted** | 7-Stage Pipeline with Token Compression Evidence |
| **New Skill Tool Admission** | **Permitted** | Skill Gateway Security Audit + SHA-256 Lockfile Pinning |
| **Relaxing Invariants or Contracts** | **PROHIBITED** | Hard Blocked (Requires Formal ADR Ratification) |
| **Bypassing Verification Gating** | **PROHIBITED** | Hard Blocked (Constitutional Violation) |
| **Direct Unaudited File Overwrites** | **PROHIBITED** | Intercepted via `INV-004` |
