# System Boundaries — What Eidos Is NOT (Phase 2)

**Status:** ARCHITECTED | Purpose: prevent scope explosion (§20).

```text
Eidos ≠ Foundation Model — it orchestrates models, never trains/serves one
Eidos ≠ Coding Agent — it is the intelligence layer inside harnesses, not a harness
Eidos ≠ IDE — no editor UI; integrates via adapters and MCP
Eidos ≠ LLM Provider — provider-neutral by INV-001
Eidos ≠ Git replacement — Git is the ground-truth substrate (events anchor to HEAD)
Eidos ≠ Test framework — it invokes pytest/jest/etc., never replaces them
Eidos ≠ Universal autonomous software engineer — bounded autonomy only (P6);
  open-ended autonomy is explicitly out of scope until EXP-006 says otherwise
Eidos ≠ Benchmark — it runs pre-registered experiments; it is not itself a leaderboard
Eidos ≠ Production self-evolving system — evolution.md pipeline is gated research
  infrastructure, not an autonomous capability
```

Positive scope (one line): deterministic, portable engineering-intelligence
services — repo understanding, context routing, contracts, bounded execution,
verification, evidence — consumable by any compatible harness.
