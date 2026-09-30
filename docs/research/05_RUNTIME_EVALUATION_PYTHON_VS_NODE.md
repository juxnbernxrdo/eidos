# EIDOS Runtime Evaluation: Python vs. Node.js vs. Hybrid

**Project:** Eidos — Engineering Intelligence for Deterministic, Orchestrated Software  
**Version:** 1.0.0  
**Scope:** Architectural Trade-off Analysis Across Core Engine Runtime Options  

---

## 1. Executive Summary & Evaluation Context

A critical early decision for Eidos is the selection of its foundational execution runtime. The options under rigorous evaluation are:
- **Option A (Pure Python)**: Python 3.11+ ecosystem.
- **Option B (Pure Node.js / TypeScript)**: Node.js 20+ / Bun / TypeScript ecosystem.
- **Option C (Hybrid Architecture)**: Python core engine with thin, polyglot adapters (CLI bridges / Node wrappers / MCP stdio).

We evaluate each option across ten rigorous technical dimensions.

---

## 2. Multi-Dimensional Trade-off Matrix

| Evaluation Dimension | Option A: Pure Python | Option B: Pure Node.js / TypeScript | Option C: Hybrid Architecture | Winner / Highest Fitness |
|:---|:---|:---|:---|:---|
| **1. AST Parsing & Multi-Language Analysis** | Outstanding. Native access to Python `ast`, libcst, plus official high-performance Python bindings for `tree-sitter` (supporting 40+ languages). | Good. `web-tree-sitter` (Wasm) and native `tree-sitter` bindings exist, but Wasm incurs ~2-3x overhead and native bindings frequently hit build/gyp issues on developer machines. | **Python Core**: Runs native `tree-sitter` and Python AST without Wasm penalty. | **Python** |
| **2. Graph Computation & Network Algorithms** | Elite. Direct integration with `NetworkX` (reference graph algorithms), `rustworkx` (C/Rust performance), `graph-tool`, and scientific computing libraries (SciPy, NumPy). | Weak to Moderate. Graph libraries (`graphology`, `ngraph`) exist but lack algorithmic depth, community detection implementations (Louvain/Leiden), and centrality metrics required for Repo Intelligence. | **Python Core**: Direct execution of Louvain/Leiden modularity and NetworkX graph analysis. | **Python** |
| **3. CLI Startup Time & Developer Experience** | Moderate (standard Python ~80-120ms startup). Can be mitigated via `uv` tool isolation or standalone binaries (`PyInstaller` / `Mojo` / `Nuitka`). | Excellent. Node.js startup is ~30-50ms; Bun is <10ms. Rich terminal libraries (`ink`, `clack`, `commander`). | **Python Core with Optimized CLI**: Using modern Python CLI frameworks (`Typer` / `Click` + `Rich`) launched via `uv` yields fast startup (~40ms) and zero environment pollution. | **Node.js (slight edge)** |
| **4. Agent & AI Research Ecosystem Alignment** | Unmatched. 95% of state-of-the-art agent research (SWE-agent, Agentless, RepoGraph, LangGraph, DSPy, OpenAI Eval) is native Python. Zero translation layer required. | Moderate. Emerging frontend agent wrappers, but lagging behind academic code intelligence and evaluation frameworks. | **Python Core**: 100% native compatibility with existing AI research artifacts and benchmarks. | **Python** |
| **5. Model Context Protocol (MCP) & LSP Support** | Excellent. Official Python MCP SDK (`mcp`), native Language Server Protocol libraries (`pygls`, `lsprotocol`). | Excellent. Official TypeScript MCP SDK (`@modelcontextprotocol/sdk`). | **Equal**: Both runtimes have first-party, production-grade MCP SDKs. | **Tie** |
| **6. Packaging & Distribution** | Transformed by modern tooling. `uv` (`uvx eidos`) and `pipx` provide instant, isolated execution without virtual environment friction, rivaling `npx`. | Traditional strength. `npx eidos` provides universal zero-install execution for JS/TS developers. | **Dual Distribution**: Core distributed via PyPI (`uvx eidos`), with optional thin npm bridge (`npx @eidos/cli`) invoking the core daemon. | **Tie** |
| **7. Cross-Harness Interoperability** | Native integration with Antigravity (Python SDK), Hermes (Python), and SWE-bench environments. Node harness (Claude Code) requires stdio/CLI bridge. | Native integration with Claude Code (Node) and Cursor/VSCode plugins. Python harnesses require child process spawning. | **Hybrid**: The Eidos core exposes a clean CLI and stdio JSON-RPC/MCP protocol, making harness consumption completely runtime-agnostic. | **Hybrid** |
| **8. Performance & Memory Footprint** | Excellent for data/graph structures with C-extensions (`rustworkx`, `pydantic-core`). Python 3.11/3.12 has reduced runtime overhead significantly. | Excellent event-loop performance for I/O; higher memory overhead for large graph object representations compared to Rust/C-backed structures. | **Python Core**: Heavy graph traversal offloaded to Rust-backed `rustworkx`. | **Python** |
| **9. Security & Sandboxing Tooling** | Direct native support for Linux Landlock, seccomp, and container APIs via Python system bindings. | Sandboxing requires C++ native addons or external Docker CLI invocations. | **Python Core**: Directly invokes OS-level security primitives without bridging. | **Python** |
| **10. Typing & Schema Validation** | Elite. `Pydantic v2` (Rust-backed core) provides instantaneous JSON Schema generation and microsecond validation speeds. | Excellent. `zod` and `TypeScript` provide outstanding compile-time and runtime typing. | **Pydantic + JSON Schema**: Single source of truth generating standard JSON Schemas consumed across both runtimes. | **Tie** |

---

## 3. In-Depth Analysis of Critical Factors

### 3.1 AST Parsing and Multi-Language Representation
Eidos must parse and index repositories written in Python, TypeScript, Go, Rust, Java, C++, and SQL.
- Python offers official wheels for `tree-sitter` and language grammars (`tree-sitter-languages`, `tree-sitter-python`, `tree-sitter-typescript`). These compile to native C libraries and run directly in-process with zero IPC overhead.
- In Node.js, `tree-sitter` bindings often trigger native node-gyp compilation failures on non-standard developer environments (especially Windows and Alpine Linux), while `web-tree-sitter` incurs a significant Wasm memory and garbage collection penalty during full-repository scanning.

### 3.2 Graph Algorithms & Community Detection
Repository Intelligence requires computing:
1. Shortest dependency paths (Dijkstra/BFS).
2. Centrality metrics (Betweenness, PageRank) to detect "God Nodes".
3. Modularity maximization (Louvain / Leiden clustering) to cluster files into architectural communities.
- **Python**: `NetworkX` provides complete reference implementations. When scale demands acceleration, `rustworkx` drops in with sub-millisecond execution times written in Rust.
- **Node.js**: The JavaScript ecosystem lacks verified community detection algorithms at scale. Re-implementing Louvain or Leiden in TypeScript would introduce significant implementation risk, maintenance burden, and performance deficits.

### 3.3 Modern Distribution Parity: `uv` vs. `npx`
Historically, Python CLI distribution was plagued by `pip`, `venv`, and PATH configuration issues, giving Node.js (`npx`) a distinct advantage.
- The advent of **`uv`** (Astral) has fundamentally changed this landscape. `uvx` enables instantaneous, isolated execution of Python CLIs from PyPI with sub-second resolution and zero system environment pollution:
  ```bash
  uvx eidos init
  ```
- Developers do not need to manage virtual environments. For environments that mandate Node.js, a lightweight npm package (`@eidos/cli`) can download or wrap the platform binary.

---

## 4. Architectural Decision: The Justified Hybrid Architecture

Based on rigorous empirical evaluation, Eidos rejects a pure Node.js architecture because Node lacks the necessary graph intelligence and AST processing capabilities. Eidos also rejects a monolithic, isolated Python design that ignores the broad Node/TypeScript agent ecosystem.

### Architectural Decision
**Eidos adopts a Python-Core Hybrid Architecture:**
1. **Core Engine**: Implemented in **Python 3.11+** utilizing:
   - `pydantic` (v2) for schema contracts and validation.
   - `tree-sitter` for deterministic AST extraction.
   - `networkx` + `rustworkx` for repository intelligence and community clustering.
   - `click` / `typer` + `rich` for the high-craftsmanship terminal CLI.
2. **Interface Contracts**: All data exchange (specs, graph nodes, progress events, evidence) is defined via **strict JSON Schemas**.
3. **Harness Integration Layer**:
   - Exposes standard **CLI commands** (`eidos init`, `eidos doctor`, `eidos graph`, `eidos verify`).
   - Exposes an official **MCP Server** (`stdio` / SSE) consumable by Google Antigravity, Claude Code, Cursor, and any MCP-compliant client.
   - Optional thin **npm bridge wrapper** for developers preferring `npx`.

This guarantees maximum scientific depth, native research integration, and zero compromise on developer distribution.
