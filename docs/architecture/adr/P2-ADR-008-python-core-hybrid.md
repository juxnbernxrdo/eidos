# P2-ADR-008 — Python-Core Hybrid Runtime

**Status:** ACCEPTED (DESIGN_CHOICE)
**Date:** 2026-09-30 | **Supersedes-format-of:** `docs/adr/ADR-001-*` (retained)

## Context
`05_RUNTIME_EVALUATION_PYTHON_VS_NODE.md` compared pure-Python / pure-Node / hybrid
across AST parsing, graph algorithms, CLI DX, research-ecosystem alignment, MCP/LSP,
packaging, interop, perf, sandboxing, typing.

## Problem
Which runtime maximizes graph/AST depth and research compatibility without
abandoning the Node-harness ecosystem?

## Decision
Python 3.11+ core (tree-sitter, NetworkX/rustworkx, Pydantic v2, Typer/Rich) with
JSON-schema + CLI/MCP-stdio boundaries and thin polyglot bridges (`uvx` primary,
`npx` wrapper where mandated).

## Alternatives
Pure Node (rejected: graph-algorithm depth + Wasm/native binding risk);
monolithic isolated Python ignoring Node ecosystem (rejected: harness reach).

## Research Evidence
Trade-off matrix (05_*, ecosystem argument) + EVD-005/006 ecosystem fit.
No head-to-head build exists — this is judgment, honestly labelled.

## Trade-offs
Scientific depth and native benchmark reuse vs CLI-startup/DX edge of Node
and bridge-maintenance cost.

## Consequences
All contracts JSON-shaped for runtime neutrality; bridge prototype + perf/DX
measurement recommended before Phase 5.

## Assumptions
`uv` distribution parity holds; Rust-backed libs cover perf-critical paths.

## Open Questions
Measured startup/memory/latency deltas? Bridge failure modes?

## Future Experiment
Bridge prototype benchmark (pre-Phase-5, lightweight).
