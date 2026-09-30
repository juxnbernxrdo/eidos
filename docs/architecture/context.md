# Context Architecture (Phase 2)

**Status:** ARCHITECTED (policy) | Basis: EVD-003 (U-curve), EVD-016 (Self-Route,
order-preservation, model/length/task conditionality). k/order/escalation values
are DESIGN_CHOICE, recalibrated by EXP-002.

## Pipeline

```text
Repository → Repository Intelligence (fingerprint + graph)
  → Task Understanding (contract: objective, scope, acceptance)
  → Context Retrieval (traverse k≤2 + lexical fallback)
  → Context Ranking (relevance × proximity × provenance weight; EXTRACTED > INFERRED)
  → Context Assembly (order-preserved source order, contracts pinned at boundaries)
  → Agent (MSC payload only)
```

## MSC assembly rules (policies, not laws)

1. Target nodes full; neighbors pruned to **signatures/types/contract comments**.
2. Source-order concatenation (OP-RAG lesson), never score-sorted dumps.
3. Critical contracts at prompt start/end (Lost-in-the-Middle mitigation).
4. Budget-aware: cheap retrieval first, escalate to wider context only on
   explicit `unanswerable` signal (Self-Route pattern).
5. Cache-friendly: frozen system+tools prefix, explicit breakpoints (prompt-caching).

## Context classes (every assembled unit tagged)

```text
Always Required — task contract, acceptance criteria, pinned interfaces
Task Relevant — k≤2 neighborhood, TESTED_BY traces
Optional — docs, history, similar-code examples
Retrieved — provenance-tagged graph/lexical hits
Generated — agent-produced summaries (INFERRED, expirable)
Historical — past events/findings (recency + ρ-risk tagged)
Potentially Contaminating — failed-trace dumps, unverified inferences,
  Adversarial surfaces (poisoned files); quarantined by default, admitted only
  with explicit justification logged (memory.md ConsistencyGate lineage)
```

## Explicit non-goal
More context is NOT better (P8). Context volume is a costed experimental variable
(tokens, latency, VSR) in EXP-002, not a virtue signal.
