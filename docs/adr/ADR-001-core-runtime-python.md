# ADR-001: Selection of Core Runtime and Polyglot Distribution Model

**Status:** Accepted  
**Date:** 2024-09-30 (Updated 2026)  
**Deciders:** Juan Bernardo Ordóñez (Author), AI Agent Systems Architecture Team  
**Consulted:** Primary Literature & Reference System Benchmarks  

---

## Context
Eidos must operate as a high-performance, deterministic **Agentic Software Engineering Layer**. The runtime must support complex code parsing across multiple programming languages, execute graph algorithms (community detection, centrality, pathfinding), provide microsecond schema validation, integrate natively with AI research benchmarks (SWE-bench), and offer an instantaneous, frictionless developer experience (CLI).

We evaluated three potential execution runtime strategies:
1. **Pure Python 3.11+**
2. **Pure Node.js / TypeScript 20+**
3. **Python-Core Hybrid with Polyglot Distribution**

## Decision
We select **Option 3: Python-Core Hybrid with Polyglot Distribution**:
- The **Core Engine** (`eidos-core`) is implemented in **Python 3.11+**.
- Core AST parsing is handled natively by `tree-sitter` and Python `ast`.
- Graph analysis is powered by `networkx` with optional `rustworkx` acceleration.
- Schemas and serialization are powered by `pydantic` v2 (backed by Rust `pydantic-core`).
- The primary developer CLI is packaged with `typer`/`click` and distributed via PyPI (`uvx eidos` or `pipx run eidos`).
- Cross-runtime integration is achieved via standard JSON-RPC / **Model Context Protocol (MCP)** over `stdio`, allowing seamless invocation by Node.js harnesses (Claude Code), IDEs (Antigravity), or web dashboards.
- An optional thin npm wrapper (`@eidos/cli`) will be published to enable `npx eidos` execution where mandated by JavaScript-only environments.

## Consequences

### Positive
- **Native Research Ecosystem Compatibility**: 95% of state-of-the-art agent code (SWE-agent, Agentless, RepoGraph) can be imported, adapted, or benchmarked directly without IPC serialization overhead.
- **Deep Graph Algorithms**: Immediate access to mature community detection (Louvain/Leiden), betweenness centrality, and topological sorting algorithms that are absent or poorly maintained in the JavaScript ecosystem.
- **Microsecond Validation**: Pydantic v2 compiles data models to native machine code via Rust, outperforming standard JS/TS runtime validators on large AST graphs.
- **Zero-Install Friction**: Modern distribution via `uvx` provides sub-second startup without Python environment corruption.

### Negative
- Python must be available on the host machine (mitigated by `uv` automated Python fetching or standalone compiled binary distribution).
- Developers writing harness plugins in Node.js must communicate via stdio/CLI rather than in-process function calls.

### Compliance & Validation
- Validated via `docs/research/05_RUNTIME_EVALUATION_PYTHON_VS_NODE.md`.
- CI will run multi-platform testing on Linux, macOS, and Windows.
