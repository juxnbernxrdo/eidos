# ADR-005: Tripartite Memory Architecture and Cross-Project Data Isolation

**Status:** Accepted  
**Date:** 2024-09-30 (Updated 2026)  
**Deciders:** Juan Bernardo Ordóñez (Author), AI Agent Systems Architecture Team  

---

## Context
AI agents often blur the lines between temporary task scratchpads, persistent project knowledge, and generalizable engineering heuristics. Naively pooling memory across projects creates grave security risks (leaking proprietary API keys, internal architecture, or customer data between codebases) and pollutes local project context with irrelevant patterns.

## Decision
Eidos partitions agent memory into three strictly separated tiers:

```text
+---------------------------------------------------------------+
| 1. WORKING MEMORY (Ephemeral)                                 |
|    - Active subtask execution state, tool returns, diffs      |
|    - Lifespan: Single task or verification turn               |
|    - Location: In-memory runtime / temporary scratch directory|
+---------------------------------------------------------------+
                             |
                             v
+---------------------------------------------------------------+
| 2. PROJECT MEMORY (Persistent, Local to Repository)           |
|    - Project Contract, Constitution, ADRs, Specs, Graph       |
|    - Event log, verification baselines, test coverage history |
|    - Lifespan: Project lifecycle                              |
|    - Location: Git-tracked `.eidos/` directory in repo root   |
+---------------------------------------------------------------+
                             |
                             v (Explicit Sanitization & Human Approval)
+---------------------------------------------------------------+
| 3. INSTITUTIONAL MEMORY (Global, Abstracted, Sanitized)       |
|    - Generic architectural heuristics, reusable skills        |
|    - Anti-pattern detection rules, performance patterns       |
|    - Lifespan: Machine/Organization lifecycle                 |
|    - Location: `~/.eidos/institutional/`                      |
+---------------------------------------------------------------+
```

### Isolation Rules
1. **Zero Implicit Cross-Project Transfer**: Working or Project memory is strictly forbidden from transferring to another repository automatically.
2. **Sanitization Gateway**: Any pattern promoted from Project Memory to Institutional Memory must undergo an automated scrubbing pass (stripping credentials, URLs, domain-specific names, and proprietary logic) and require explicit human engineering sign-off.

## Consequences

### Positive
- Guarantees enterprise-grade IP protection and privacy compliance (GDPR, SOC2).
- Keeps local project context focused strictly on the active codebase.
- Allows organization-wide learning of generic engineering skills without accidental data leakage.

### Negative
- Requires explicit user interaction when exporting a novel, high-value skill or rule for cross-project reuse.
