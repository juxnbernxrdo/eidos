# ADR-003: Repository Intelligence Graph Architecture and Epistemic Classification

**Status:** Accepted  
**Date:** 2024-09-30 (Updated 2026)  
**Deciders:** Juan Bernardo Ordóñez (Author), AI Agent Systems Architecture Team  

---

## Context
Standard RAG (Retrieval-Augmented Generation) based on naive vector embeddings performs poorly on software repositories. Code has precise syntax, call hierarchies, inheritance trees, and dependency constraints that cosine similarity on unstructured text chunks fails to capture. Conversely, pure AST analysis misses cross-document concepts, architectural intent, and implicit design patterns.

## Decision
Eidos implements a hybrid **Repository Intelligence Graph** combining deterministic syntactic parsing with semantic community detection:

1. **Dual-Tier Graph Construction**:
   - **Tier 1 (Syntactic & Deterministic)**: Extracted via `tree-sitter` (and native Python `ast`) directly from source code. Generates nodes for `File`, `Module`, `Class`, `Function`, `API`, and `Dependency`.
   - **Tier 2 (Semantic & Topological)**: Clusters the graph using Louvain/Leiden community detection, computes God Node centrality (betweenness/degree), and links specifications, architectural rules, and documentation.
2. **Epistemic Classification of Edges**:
   To prevent hallucinated relationships from corrupting the graph, every edge in the Eidos graph must carry an explicit epistemic classification:
   - `EXTRACTED`: Deterministically parsed from source code or compiler artifacts (Confidence = 1.0).
   - `INFERRED`: Hypothesized by an LLM based on semantic analysis or documentation (Confidence $\in [0.0, 0.99]$).
   - `USER_CONFIRMED`: An inferred relationship explicitly validated by a human engineer.
   - `AGENT_PROPOSED`: Proposed during task execution, pending verification.
3. **Graph Persistence**:
   Serialized in `graphify-out/graph.json` or `.eidos/graph/repository_graph.json` with an immutable schema, supported by an interactive visualization and markdown summary.

## Consequences

### Positive
- Enables the `Context Router` to traverse exact relational paths (e.g., "retrieve all classes implementing Interface X and tested by Suite Y") without loading irrelevant source files.
- Protects the system against LLM hallucination: the model can never claim an unverified import exists as a `FACT`.
- Surfaces high-risk refactoring targets (God Nodes and bridge edges across architectural communities).

### Negative
- Incremental graph rebuilding incurs computation time upon major Git branch switching or大規模 file modifications. (Mitigated by content-hash-based incremental updates).
