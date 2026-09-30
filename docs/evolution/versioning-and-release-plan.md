# Eidos Versioning & Release Governance Plan

**Authority:** Eidos System Constitution & Phase 8 Evolution Governance  
**Standard:** Semantic Versioning 2.0.0 (SemVer)  
**Status:** RATIFIED RELEASE POLICY  

---

## 1. SemVer Governance Policy

Eidos adheres to strict Semantic Versioning (`MAJOR.MINOR.PATCH`) to guarantee backward compatibility and prevent silent contract drift:

- **MAJOR (`X.0.0`)**: Incompatible API or architectural changes, modifications to System Constitution articles, breaking changes to Draft 2020-12 contract schemas, or changes that alter event log fold semantics. Requires a formal Architectural Decision Record (ADR) and Quality Gate sign-off.
- **MINOR (`1.X.0`)**: Backward-compatible new capabilities, new harness adapters, new language grammar extractors, or opt-in subsystem features (e.g. `EVO-002`, `EVO-003`).
- **PATCH (`1.0.X`)**: Backward-compatible bug fixes, security patches, performance optimizations, and heuristic calibrations ratified through Phase 8 Evolution proposals (e.g. `EVO-001`).

---

## 2. Release Roadmap & Milestones

```text
┌────────────────────────────────────────────────────────────────────────┐
│ v1.0.0 — Canonical Eidos Release                      (2026-09-30)     │
│   • Complete 8-Phase Engineering Intelligence Pipeline                 │
│   • Heterogeneous Graph Engine (21 nodes, 11 edges)                    │
│   • Minimal Sufficient Context Router (k<=2 topological pruning)       │
│   • Non-bypassable Verification Gating & Oracle Repair Loop            │
│   • Policy-as-Physics Security Sandbox & Secret Scrubbing              │
│   • PROP-EVO-001: Adaptive Early-Stopping on Repair Loops              │
├────────────────────────────────────────────────────────────────────────┤
│ v1.1.0 — Multi-Session Episodic Memory                (Q4 2026)        │
│   • PROP-EVO-002: Project-isolated historical episode indexing         │
│   • Consistency-gated patch retrieval across multi-day sessions       │
├────────────────────────────────────────────────────────────────────────┤
│ v1.2.0 — Polyglot Graph Parsing & Tree-Sitter         (Q1 2027)        │
│   • PROP-EVO-003: Multi-language AST ingestion (TS, Rust, Go)          │
│   • Cross-language dependency analysis                                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Release Verification Checklist

Prior to tagging any production release:
1. `python -m eidos.cli.main doctor` must report 14/14 PASS.
2. `python -m eidos.cli.main invariant check` must report 0 violations.
3. Automated test suite must pass with 100% success rate.
4. Feature Passports for all 15 core capabilities must be in state `VERIFIED`.
5. All accepted evolution proposals must have explicit operator signatures.
