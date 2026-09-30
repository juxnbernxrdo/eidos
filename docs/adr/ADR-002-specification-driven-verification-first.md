# ADR-002: Specification-Driven Development (SDD) & Verification-First State Machine

**Status:** Accepted  
**Date:** 2024-09-30 (Updated 2026)  
**Deciders:** Juan Bernardo Ordóñez (Author), AI Agent Systems Architecture Team  

---

## Context
Traditional AI coding agents suffer from the "vibe coding" failure mode: models receive a loose natural language prompt and immediately begin generating code diffs. This results in:
1. Hallucinated APIs and unnecessary dependencies.
2. Silent regressions in unmonitored areas of the repository.
3. Premature declarations of task completion ("I have fixed the issue!") when tests fail or are omitted.
4. Severe architectural drift where documentation and implementation rapidly diverge.

## Decision
Eidos adopts a mandatory **Specification-Driven Development (SDD)** and **Verification-First** state machine:

1. **Phase Gating**:
   No code implementation step can commence without an approved, machine-validated **Specification** (`spec.json` / `spec.md`) and actionable **Tasks** (`tasks.json` / `tasks.md`).
2. **Deterministic State Machine**:
   Every engineering task must progress through a closed-loop finite state machine:
   $$\text{DISCOVERY} \longrightarrow \text{SPECIFY} \longrightarrow \text{PLAN} \longrightarrow \text{IMPLEMENT} \longrightarrow \text{VERIFY} \longrightarrow \text{CONVERGE}$$
3. **Automated Repair Loop**:
   If verification fails, the state transitions to `REPAIR`, ingesting compiler errors, lint violations, and test failure diffs (Reflexion model), bounded by a maximum of $K$ convergence attempts.
4. **Non-Negotiable Completion Criteria**:
   A task can **never** transition to state `DONE` based solely on model assertion. The state machine strictly mandates:
   $$\text{State} = \text{DONE} \iff \text{VerificationResult}(\text{tests}=\text{PASS}, \text{lint}=\text{PASS}, \text{types}=\text{PASS}, \text{invariants}=\text{PASS}) = \text{TRUE}$$

## Consequences

### Positive
- Completely eliminates "vibe coding" regressions.
- Guarantees 100% traceability between user requirements, specifications, code diffs, and verification logs.
- Prevents infinite spinning loops through explicit bounded convergence thresholds ($K \le 5$).

### Negative
- Increases initial task latency: small 1-line changes require passing through the specification and verification harness. (Mitigated by a "Fast-Path / Micro-Spec" profile for localized bug fixes).
