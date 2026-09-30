# P2-ADR-008 — Python-Core Hybrid Runtime

**Date:** 2026-09-30 | **Canonical location:** `docs/adr/`
**Re-expresses (new format):** `docs/adr/ADR-001-core-runtime-python.md` (retained as historical record)

## Status

ACCEPTED

## Context

`05_RUNTIME_EVALUATION_PYTHON_VS_NODE.md` compared pure-Python, pure-Node, and
hybrid across ten dimensions: AST parsing, graph algorithms, CLI DX, research
ecosystem alignment, MCP/LSP, packaging, interop, performance, sandboxing,
and typing.

## Problem

Which runtime maximizes graph/AST depth and research compatibility without
abandoning the Node-harness ecosystem?

## Decision

Python 3.11+ core (tree-sitter, NetworkX/rustworkx, Pydantic v2, Typer/Rich)
with JSON-schema plus CLI/MCP-stdio boundaries and thin polyglot bridges
(`uvx` primary, `npx` wrapper where mandated).

## Alternatives Considered

- Pure Node.js/TypeScript — rejected: graph-algorithm depth gap plus Wasm/native
  binding risk on developer machines.
- Monolithic isolated Python ignoring the Node ecosystem — rejected: harness
  reach (Claude Code, OpenCode, Cursor are Node-side).

## Research Evidence

Trade-off matrix (`05_RUNTIME_EVALUATION_PYTHON_VS_NODE.md`, ecosystem argument)
with EVD-005/EVD-006 ecosystem fit. No head-to-head build exists — this is
engineering judgment, honestly labelled as such.

## Evidence Status

DESIGN_CHOICE

## Trade-offs

Scientific depth and native benchmark reuse vs CLI-startup/DX edge of Node and
ongoing bridge-maintenance cost.

## Consequences

All cross-boundary exchanges are JSON-shaped for runtime neutrality; a bridge
prototype with perf/DX measurement is recommended before Phase 5.

## Assumptions

`uv` distribution parity holds; Rust-backed libraries cover perf-critical paths.

## Open Questions

Measured startup, memory, and dispatch-latency deltas? Bridge failure modes?

## Future Experiment

Lightweight bridge-prototype benchmark (pre-Phase-5, not a Phase-7 study).

## Phase Boundary

### Phase 2

Architectural decision: runtime selection and boundary technology (JSON/MCP-stdio).

### Phase 3

Future contract implications: runtime-neutral schema discipline (Draft 2020-12
lineage); no field names frozen by this ADR.

### Phase 4+

Future specification/implementation/verification implications: packaging specs,
bridge specs, perf measurement; no distribution artifact is produced by this ADR.
