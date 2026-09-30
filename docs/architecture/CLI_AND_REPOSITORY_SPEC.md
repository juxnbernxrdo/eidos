# EIDOS CLI & Repository Structure Specification

**Project:** Eidos — Engineering Intelligence for Deterministic, Orchestrated Software  
**Version:** 1.0.0  
**Domain:** Command-Line Interface Definition & Source Code Tree Organization  

---

## 1. CLI Architecture & Interface Specification

The Eidos CLI (`eidos`) is implemented in Python using `typer` and `rich`, providing an intuitive, interactive, and machine-readable command suite.

```text
eidos
├── init         <-- Detects repo state, runs adaptive interview, bootstraps .eidos/
├── doctor       <-- Runs 14-point diagnostic check across harness, graph, rules, tests
├── analyze      <-- Performs non-destructive audit (AST, dependencies, dead code)
├── graph        <-- Builds, clusters, queries, and visualizes Repository Graph
│   ├── build    <-- Extracts AST & semantic nodes, computes communities & god nodes
│   ├── query    <-- Performs BFS/DFS path traversal within token budget
│   ├── export   <-- Exports graph to HTML visualizer, JSON, or Obsidian
│   └── health   <-- Checks for dangling edges, collapsed endpoints, or corruption
├── spec         <-- Manages Specification-Driven Development workflow
│   ├── new      <-- Scaffolds new spec matching JSON schema
│   ├── plan     <-- Generates technical plan from specification
│   ├── tasks    <-- Decomposes plan into atomic, contract-bounded tasks
│   └── check    <-- Validates spec schema and checks for specification drift
├── verify       <-- Deterministic verification-first test & invariant execution
├── baseline     <-- Manages versioned repository health snapshots
│   ├── create   <-- Captures current metrics, graph cohesion, and test coverage
│   └── compare  <-- Computes objective delta between two baselines
├── invariant    <-- Manages machine-checkable architectural invariants
│   ├── list     <-- Lists active invariant rules
│   ├── check    <-- Validates invariants against the live AST graph
│   └── add      <-- Registers a new architectural invariant rule
├── skill        <-- Manages agent skills with pre-install security scanning
│   ├── find     <-- Searches open skill ecosystem (find-skills / skills.sh)
│   ├── audit    <-- Runs static AST & semantic audit (SkillSpector model)
│   └── install  <-- Verifies provenance, risk score, and installs skill
└── evaluate     <-- Runs empirical SWE-bench / ablation evaluation suites
```

---

## 2. Detailed CLI Command Specifications

### 2.1 `eidos init`
```bash
eidos init [--harness <name>] [--lang <es|en>] [--non-interactive]
```
- **Behavior**:
  1. Inspects current working directory.
  2. If empty $\rightarrow$ triggers **Greenfield Wizard** (Adaptive Interview $\rightarrow$ Language Confirmation $\rightarrow$ Constitution $\rightarrow$ Initial Spec).
  3. If code detected $\rightarrow$ triggers **Existing Repository Discovery** (Fingerprint $\rightarrow$ Non-Destructive AST Scan $\rightarrow$ Graph Build $\rightarrow$ Baseline).
  4. Generates `.eidos/` directory and root `AGENTS.md` router.

### 2.2 `eidos doctor`
```bash
eidos doctor [--fix] [--json]
```
- **Behavior**:
  Executes the 14-point diagnostic battery:
  - `[PASS]` Harness detected: Google Antigravity (Capabilities: subagents, tasks, mcp).
  - `[PASS]` `AGENTS.md` and `CONSTITUTION.md` present and valid.
  - `[PASS]` Repository Intelligence Graph up-to-date (482 nodes, 1,120 edges).
  - `[PASS]` Active skills audited (0 high-risk skills).
  - `[PASS]` Architectural invariants engine online (3 active rules).
  - `[PASS]` Test runner detected: `pytest` (24 test suites discovered).
  - `[PASS]` Git working tree clean.
  - **Overall Health**: `READY (14/14 checks passed)`.

### 2.3 `eidos graph`
```bash
# Build complete repository graph with community detection
eidos graph build [--mode <fast|deep>] [--directed]

# Query relational path between two architectural concepts
eidos graph query "How does AuthMiddleware communicate with TokenService?" --budget 1000

# Export interactive visualization
eidos graph export --format html --open
```

### 2.4 `eidos verify`
```bash
eidos verify [--task <task_id>] [--strict] [--fix]
```
- **Behavior**:
  1. Runs unit, integration, and contract tests.
  2. Executes static type checking (`mypy`/`pyright`/`tsc`).
  3. Executes linter and formatting rules (`ruff`/`eslint`).
  4. Evaluates all architectural invariants (`eidos invariant check`).
  5. Computes documentation and specification drift.
  6. Emits `VerificationResult` JSON and Feature Passport update.
  7. If verification fails and `--fix` is passed, triggers the bounded Reflexion repair loop ($K \le 5$).

---

## 3. Proposed Eidos Source Repository Tree

```text
eidos/
├── pyproject.toml                     <-- Hatchling / uv build configuration
├── README.md                          <-- Project overview, quickstart, philosophy
├── AGENTS.md                          <-- Root navigation router for AI harnesses
├── CONSTITUTION.md                    <-- Core immutable principles and governance
├── LICENSE                            <-- MIT License
│
├── src/
│   └── eidos/
│       ├── __init__.py                <-- Package version and public API exports
│       ├── core/                      <-- Foundational abstractions and state machines
│       │   ├── pipeline.py            <-- End-to-end SDD execution pipeline
│       │   ├── state.py               <-- Finite state machine (Discovery -> Converged)
│       │   └── exceptions.py          <-- Typed domain exceptions
│       │
│       ├── cli/                       <-- Typer / Rich CLI commands
│       │   ├── __init__.py
│       │   ├── main.py                <-- CLI entrypoint
│       │   ├── commands/              <-- Subcommands: init, doctor, graph, spec, verify
│       │   └── ui.py                  <-- Rich terminal tables, spinners, and formatters
│       │
│       ├── contracts/                 <-- Pydantic v2 data models and JSON Schemas
│       │   ├── project.py             <-- Project and Constitution models
│       │   ├── spec.py                <-- Spec, SubSpec, and Task schemas
│       │   ├── graph.py               <-- GraphNode and GraphEdge models
│       │   ├── evidence.py            <-- Evidence and FeaturePassport models
│       │   └── progress.py            <-- ProgressEvent and Session models
│       │
│       ├── interview/                 <-- Adaptive interview engine
│       │   ├── engine.py              <-- Requirement & Uncertainty entropy minimizer
│       │   ├── questions.py           <-- Domain question bank
│       │   └── language.py            <-- Language detection and policy confirmation
│       │
│       ├── intelligence/              <-- Non-destructive repository intelligence
│       │   ├── fingerprint.py         <-- Language, framework, and tool detector
│       │   ├── parser.py              <-- Tree-sitter multi-language AST extractor
│       │   ├── drift.py               <-- DOC, SPEC, ARCH, CONTRACT drift detector
│       │   └── invariants.py          <-- Machine-checkable invariant rule checker
│       │
│       ├── graph/                     <-- Repository Intelligence Graph
│       │   ├── builder.py             <-- Graph construction (AST + semantic nodes)
│       │   ├── cluster.py             <-- Louvain / Leiden community clustering
│       │   ├── analyzer.py            <-- Centrality, God Node, and cohesion scoring
│       │   ├── query.py               <-- BFS/DFS path traversal and token budgeting
│       │   └── visualizer.py          <-- HTML and Obsidian export generators
│       │
│       ├── context/                   <-- Context engineering & routing
│       │   ├── router.py              <-- Minimum Sufficient Context (MSC) algorithm
│       │   ├── pruner.py              <-- AST signature extractor and body stripper
│       │   └── builder.py             <-- Prompt assembler (Lost-in-the-Middle guarded)
│       │
│       ├── harness/                   <-- Portable harness adapters
│       │   ├── base.py                <-- Abstract HarnessAdapter class
│       │   ├── antigravity.py         <-- Google Antigravity adapter
│       │   ├── claude_code.py         <-- Anthropic Claude Code adapter
│       │   ├── opencode.py            <-- OpenCode adapter
│       │   └── headless.py            <-- Docker/CLI runner for SWE-bench & CI
│       │
│       ├── agents/                    <-- Subagent orchestration
│       │   ├── contract.py            <-- Contract-bounded subagent builder
│       │   └── isolation.py           <-- Git worktree and process isolation
│       │
│       ├── skills/                    <-- Skill management & security
│       │   ├── registry.py            <-- find-skills / skills.sh package manager
│       │   ├── auditor.py             <-- SkillSpector static AST & YARA auditor
│       │   └── sandboxing.py          <-- OpenShell Landlock / namespace sandbox
│       │
│       ├── verification/              <-- Verification-first execution & repair
│       │   ├── runner.py              <-- Test, type, lint, and invariant runner
│       │   ├── reflexion.py           <-- Error trace analyzer and repair prompt generator
│       │   └── passport.py            <-- Feature Passport builder and signer
│       │
│       ├── progress/                  <-- Event sourcing & progress tracking
│       │   ├── logger.py              <-- Append-only events.jsonl writer
│       │   ├── state_projector.py     <-- State folding from events
│       │   └── baseline.py            <-- Baseline snapshot creation and comparison
│       │
│       ├── memory/                    <-- Tripartite memory management
│       │   ├── working.py             <-- Ephemeral task scratchpad
│       │   ├── project.py             <-- Repository-scoped persistent memory
│       │   └── institutional.py       <-- Sanitized cross-project heuristic scrubber
│       │
│       └── evaluation/                <-- Benchmark testbed & ablations
│           ├── swe_bench.py           <-- SWE-bench / Lite runner
│           └── ablation.py            <-- Modular ablation study orchestrator
│
├── schemas/                           <-- Standalone JSON Schema Draft 2020-12 files
│   ├── project.schema.json
│   ├── constitution.schema.json
│   ├── spec.schema.json
│   ├── task.schema.json
│   ├── graph_node.schema.json
│   ├── evidence.schema.json
│   └── progress_event.schema.json
│
├── docs/                              <-- Research, Architecture, and ADR documentation
│   ├── research/
│   ├── architecture/
│   └── adr/
│
├── tests/                             <-- Comprehensive test suite
│   ├── unit/
│   ├── integration/
│   └── invariants/
│
└── .eidos/                            <-- Self-referential governance metadata
    ├── project.json
    ├── rules/
    ├── specs/
    ├── progress/
    └── graph/
```
