# Skill Architecture (Phase 2)

**Status:** ARCHITECTED | Basis: Anthropic Agent Skills open standard (SRC-104:
`SKILL.md` + YAML `name/description`, progressive disclosure), NVIDIA T1–T3
evaluation (SRC-108), supply-chain risk EVD-008. Thresholds OPEN (EXP-005).

## Skill unit (conceptual)

```text
Skill
├── Identity — name (kebab, namespaced), version (semver), owner/signature pin
├── Purpose — description (≤1024 chars, trigger-gated disclosure)
├── Inputs / Outputs — Phase-3 schemas (typed, validated)
├── Tools — declared executables (scripts/), least-privilege
├── Dependencies — pinned (hash, not star-count)
├── Permissions — explicit grants (fs/net/exec scopes)
├── Provenance — origin repo, commit hash, author, audit trail
├── Version — semver + deprecation policy
├── Tests — evals incl. negative cases (evals/evals.json lineage)
└── Security — gateway verdict (risk score; threshold TBD by EXP-005)
```

## Lifecycle

```text
Discovery (local → registry; reuse-before-authoring policy)
→ Validation (static AST+YARA → provenance → semantic audit; repo-aware scan)
→ Installation (hash-pinned, manifest-locked, e.g. skills-lock.json lineage)
→ Invocation (progressive disclosure: metadata → SKILL.md → scripts on trigger)
→ Evaluation (T1 blocking, T2 dedup, T3 live A/B where affordable)
→ Deprecation (versioned, announced, reversible)
```

Reuse-before-author: search local + registry; inspect provenance/maintenance/license
(MIT/Apache-2.0/BSD per Constitution Art. V) before scaffolding new.

## Security boundary (§16 detail in security.md)

```text
Skill ──de déclared-tools──▶ Tools ──sandbox-policy──▶ External Systems
```

- Skill code is **untrusted input** until gateway passes (INV: zero unaudited skills).
- Repo-aware scanning (SRC-028 lesson: 99.5% naive flags vanish with context;
  hijacked-repo vector) + owner pinning.
- `risk<25`-style thresholds are DESIGN_CHOICE pending ROC calibration (ARR-03).
