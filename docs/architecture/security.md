# Security Architecture (Phase 2)

**Status:** ARCHITECTED | Basis: EVD-007 (prompt bans fail; OS enforcement),
EVD-008 + SRC-027/028 (supply-chain base rates), SRC-108 (T1–T3). Guarantees
OPEN until pen-test (EXP-005). Security is architecture, not a later stage (P12).

## Trust-boundary stack

```text
Agent → Skill → Tool → Filesystem → Repository → Network → External Service
```

Each `→` is a policy-enforced boundary (declared permissions + sandbox + audit),
never a prompt instruction.

## Boundaries & mechanisms (concepts; Phase 3+ contracts)

- **Permissions/capabilities:** contract-scoped grants per subagent/skill
  (agents.md, skills.md); default-deny; destructive ops need explicit scope.
- **Sandboxing:** kernel-level lineage (Landlock/seccomp/userns/netns + OPA +
  policy proxy; OpenShell model, alpha — efficacy OPEN). Workspace-confinement;
  only protects in-sandbox runs (Linux-first; other OS via containers — OPEN).
- **Secrets:** injected providers, never filesystem; redaction in traces/logs.
- **Provenance:** hash-pinned skills/deps/owners; hijacked-repo watch (SRC-028);
  repo-aware scanning (naive flags over-block 99.5% — calibrate, don't naively gate).
- **Prompt injection:** untrusted-content marking (retrieved code/docs/skills);
  tool-description distrust (MCP lesson); no security-by-instruction (EVD-007).
- **Tool injection:** schema-validated I/O; TOCTOU-aware; MCP enforcement outside
  the reasoning loop (SRC-104/105 orthogonality: skills=knowledge, MCP=connection).
- **Repository poisoning:** poisoned-file quarantine class in context.md;
  eval sandboxes block `git log/show` (leakage lineage EVD-015/U-002).
- **Cross-project leakage:** INV-002; memory.md gating; adapter boundary blindness
  to other projects (harness.md).

## Threat-model inputs (carried from RISK_REGISTER_AND_RESEARCH_GAPS.md, PROPOSED)

RSK-01 runaway loops → bounded repair; RSK-02 supply chain → gateway;
RSK-03 context saturation → MSC; RSK-04 harness drift → adapters + EXP-007;
RSK-05 destructive FS → sandbox; RSK-06 hallucinated edges → epistemics;
RSK-07 spec friction → micro-spec; RSK-08 provider drift → pinning.
Quantification of base rates and residual risk is EXP-005/007 work.
