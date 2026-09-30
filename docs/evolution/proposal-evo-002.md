# Learning Proposal `PROP-EVO-002`: Long-Horizon Multi-Session Memory Gating

**Proposal Identifier:** `PROP-EVO-002`  
**Target Subsystem:** [`src/eidos/memory/manager.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/memory/manager.py)  
**Category:** `MEMORY_INFRASTRUCTURE`  
**Governing Specification:** `SPEC-011-MEMORY-GATING`  
**Current Status:** **PLANNED (Target Release: v1.1.0)**  
**Date Authored:** 2026-09-30  

---

## 1. Problem Statement & Empirical Rationale

In Phase 7 Ablation `EXP-002`, the isolated memory arm ($A_8$) yielded $0.0$ pp improvement over baseline because single-task benchmark runs initialize with an empty memory store.

However, in multi-day developer workflows, agents encounter recurring defect patterns (e.g. repeated ORM migration idiosyncrasies, specific dependency quirks). Without long-horizon indexing, agents must rediscover repair strategies from scratch each session.

---

## 2. Proposed Architecture

1. **Episodic Repair Indexing**: When a task converges via `PhasedPipeline`, serialize the minimal diagnostic diff and successful patch into `.eidos/memory/episodes/{task_hash}.json`.
2. **Project-Gated Retrieval**: When assembling Minimal Sufficient Context for a new task, query historical episodes matching the AST subgraph ($k \le 2$).
3. **Consistency Gate**: Any retrieved memory item must pass a consistency check against active contracts; conflicting memories are quarantined automatically (`EVD-017`).

---

## 3. Governance Timeline
- Scheduled for implementation in Eidos v1.1.0 following creation of a multi-session benchmark evaluation suite.
