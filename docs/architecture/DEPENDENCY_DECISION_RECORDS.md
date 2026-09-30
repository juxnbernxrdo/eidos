# EIDOS Dependency Decision Records (DDR)

**Project:** Eidos — Engineering Intelligence for Deterministic, Orchestrated Software  
**Version:** 1.0.0  
**Policy:** Zero-Bloat, Security-Vetted Dependency Engineering  

---

## 1. Dependency Engineering Policy

Eidos adheres to a strict dependency vetting protocol:
1. **Necessity Test**: Can this functionality be implemented deterministically in $< 150$ lines of tested native code? If yes, reject external dependency.
2. **Maintenance Health**: Must have active maintenance, $>90\%$ test coverage, and responsive CVE patching ($< 30$ days).
3. **License Purity**: Only OSI-approved permissive licenses permitted (`MIT`, `Apache-2.0`, `BSD-3-Clause`). No copyleft (`GPL`, `AGPL`) or non-commercial licenses in core libraries.
4. **Transitive Footprint**: Minimize deep dependency trees. Every transitive dependency increases supply-chain attack surface.
5. **Runtime Overhead**: Native C/Rust extensions must supply pre-built wheels for Linux (glibc/musl x86_64, aarch64), macOS (Apple Silicon / Intel), and Windows.

---

## 2. Architectural Dependency Decisions

### DDR-001: Schema Validation and Serialization Engine
- **Selected**: `pydantic >= 2.8.0` (with `pydantic-core`)
- **Alternatives Considered**: `marshmallow`, `attrs`, native `dataclasses`, `jsonschema` (pure Python).
- **Rationale**:
  - `pydantic-core` is implemented in Rust, providing up to $20\times$ faster serialization and validation speeds over pure Python libraries.
  - Automatically exports Draft 2020-12 compliant JSON Schemas directly from Python classes, serving as the single source of truth for both Python and external harnesses.
  - Battle-tested in FastAPI and the official Model Context Protocol (MCP) Python SDK.
- **License**: MIT
- **Transitive Dependencies**: `annotated-types`, `pydantic-core`, `typing-extensions`.

---

### DDR-002: Multi-Language AST Parsing
- **Selected**: `tree-sitter >= 0.22.0` with `tree-sitter-languages` / pinned grammars.
- **Alternatives Considered**: Python standard `ast`, `libcst`, `ANTLR`, Language Server Protocol (LSP) daemons.
- **Rationale**:
  - Universal parsing engine capable of parsing Python, TypeScript, Go, Rust, Java, and C++ into consistent concrete syntax trees.
  - Extremely high speed (implemented in ANSI C).
  - Robust against syntax errors: can parse partially broken or in-progress code files during agent editing without throwing fatal exceptions.
- **License**: MIT
- **Transitive Dependencies**: Zero (self-contained C-extensions).

---

### DDR-003: Graph Computation and Community Clustering
- **Selected**: `networkx >= 3.3` + optional `rustworkx >= 0.15.0`
- **Alternatives Considered**: `graph-tool`, `igraph`, pure custom adjacency matrices.
- **Rationale**:
  - `NetworkX` is the universal reference implementation for network algorithms, centrality calculations, and topological sorting in Python.
  - High interoperability with GraphML, JSON, and Neo4j exporters.
  - For large repositories ($> 10,000$ nodes), `rustworkx` provides Rust-accelerated graph traversals with an API compatible with NetworkX.
- **License**: BSD-3-Clause (NetworkX) / Apache-2.0 (rustworkx).
- **Transitive Dependencies**: Minimal.

---

### DDR-004: Terminal Interface and CLI Framework
- **Selected**: `typer >= 0.12.0` / `click >= 8.1.0` + `rich >= 13.7.0`
- **Alternatives Considered**: `argparse` (stdlib), `prompt_toolkit`, `blessed`, `textual`.
- **Rationale**:
  - `Typer` leverages Python type hints for clean, self-documenting CLI commands.
  - `Rich` renders elite terminal tables, diff views, progress bars, and markdown reports with zero terminal glitching across Linux, macOS, and Windows.
  - Sub-millisecond startup overhead when combined with `uv`.
- **License**: MIT
- **Transitive Dependencies**: `click`, `markdown-it-py`, `pygments`.

---

### DDR-005: Model Context Protocol (MCP) Integration
- **Selected**: `mcp >= 1.0.0` (Official Anthropic / Model Context Protocol Python SDK)
- **Alternatives Considered**: Custom JSON-RPC 2.0 stdio server.
- **Rationale**:
  - First-party, standardized protocol layer supported natively by Claude Code, Google Antigravity, and Cursor.
  - Built-in lifecycle management, prompt templates, tool exposure, and resource reading over standard `stdio`.
- **License**: MIT
- **Transitive Dependencies**: `anyio`, `httpx`, `pydantic`.

---

## 3. Dependency Manifest Summary (Proposed `pyproject.toml`)

```toml
[project]
name = "eidos"
version = "0.1.0"
description = "Engineering Intelligence for Deterministic, Orchestrated Software"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [{ name = "Juan Bernardo Ordóñez" }]

dependencies = [
    "pydantic>=2.8.0",
    "tree-sitter>=0.22.0",
    "networkx>=3.3",
    "typer>=0.12.0",
    "rich>=13.7.0",
    "mcp>=1.0.0",
]

[project.optional-dependencies]
fast-graph = [
    "rustworkx>=0.15.0",
]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.5.0",
    "mypy>=1.10.0",
]

[project.scripts]
eidos = "eidos.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```
