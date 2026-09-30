# Learning Proposal `PROP-EVO-003`: Polyglot Graph Parsing & Tree-Sitter Extension

**Proposal Identifier:** `PROP-EVO-003`  
**Target Subsystem:** [`src/eidos/intelligence/parser.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/intelligence/parser.py) & [`src/eidos/graph/engine.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/graph/engine.py)  
**Category:** `GRAPH_INTELLIGENCE`  
**Governing Specification:** `SPEC-005-GRAPH-STORE`  
**Current Status:** **PLANNED (Target Release: v1.2.0)**  
**Date Authored:** 2026-09-30  

---

## 1. Problem Statement & Empirical Rationale

Phase 7 Threats to Validity analysis noted that Eidos's AST extractor is currently limited to Python's standard `ast` module. Expanding external validity across enterprise polyglot repositories requires parsing languages like TypeScript, Rust, and Go without altering the canonical 21 node types and 11 edge relations.

---

## 2. Proposed Architecture

1. **Tree-Sitter Grammar Bindings**: Integrate pre-compiled Tree-Sitter parsers for TypeScript, Rust, and Go into a dedicated adapter package `eidos-polyglot`.
2. **Canonical Mapping**: Map foreign AST constructs to standard Eidos entities:
   - TypeScript `interface` / `type` $\to$ `NodeType.CONTRACT`
   - Rust `fn` / Go `func` $\to$ `NodeType.FUNCTION`
   - `import` / `use` $\to$ `EdgeRelation.IMPORTS` / `DEPENDS_ON`
3. **Zero Core Disruption**: The Heterogeneous Graph Engine data model and context router remain completely untouched; only the parser ingestion frontend is generalized.

---

## 3. Governance Timeline
- Scheduled for Eidos v1.2.0 following Dependency Decision Record vetting for Tree-Sitter native wheels.
