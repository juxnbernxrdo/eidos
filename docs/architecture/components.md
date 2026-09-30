# Eidos Components & Interfaces (Phase 2 — conceptual)

**Status:** ARCHITECTED (interfaces are sketches for Phase 3 contracts, NOT APIs).

> **Phase-2 corrective governance (binding):** the interfaces described in this
> document represent architectural boundaries and conceptual capabilities
> identified during Phase 2. They do NOT constitute public APIs or
> machine-readable contracts. No schema is frozen here, no field name is frozen
> here, no validator is created here. Method lists (including the `HarnessAdapter`
> sketch) record *candidate* operations for Phase-3 contract design — see
> `harness.md` for per-method verdicts (REQUIRED / OPTIONAL / DROPPED) and
> `interface-contract-readiness.md` for the Phase-3 readiness map.
>
> ```text
> PHASE 2 — Architectural Interface Sketch
>     ↓
> PHASE 3 — Machine Contract
>     ↓
> PHASE 4 — Specification
>     ↓
> PHASE 5 — Implementation
> ```

## Component map (domain → component → consumes/produces)

| Component | Domain | Consumes | Produces | Status |
|---|---|---|---|---|
| Pipeline Engine | Orchestration | Task contracts, phase gates | State transitions, events | PROPOSED |
| Context Router | Context | Task + graph + rules | MSC payload | PROPOSED (policy OPEN) |
| Graph Builder / Querier | Graph | Repo snapshot | `EXTRACTED` edges, traversals | EXPERIMENTAL (`src/eidos/graph/engine.py` exists, unvalidated) |
| Fingerprinter | Repo Intel | Filesystem (read-only) | Language/deps/test profile | EXPERIMENTAL (`intelligence/fingerprint.py`) |
| Invariant Checker | Verification | AST + rules | Violations | EXPERIMENTAL (`intelligence/invariants.py`) |
| Verify Runner | Verification | Tests/types/lint/invariants | `VerificationResult` | EXPERIMENTAL (`verification/runner.py`) |
| Skill Gateway | Skills/Security | Skill package | Risk verdict + install decision | PROPOSED |
| Sandbox Supervisor | Security | Policy + command | Isolated execution | PROPOSED |
| Event Log / Projector | Progress | Events | State, passports | EXPERIMENTAL (`progress/logger.py`) |
| Memory Stores (×3) | Memory | Writes (gated) | Reads (scoped) | CONCEPTUAL, gated |
| Evolution Pipeline | Evolution | Proposals + evidence | Accepted/Rejected versions | CONCEPTUAL, forbidden-by-default |
| Harness Adapters (×N) | Harness | Contracts | Traces | PROPOSED |

## Interface sketches (ARCHITECTURAL SKETCH — Phase 3 formalizes; nothing frozen)

| Interface | Phase 2 Purpose | Research Basis | Status | Phase 3 Contract |
|---|---|---|---|---|
| HarnessAdapter | Harness abstraction boundary (portability without Core coupling) | EVD-001 (SWE-agent ACI deltas), EVD-002 (Agentless cost) | ARCHITECTURAL SKETCH | FUTURE |
| ContextRouter | Deliberate context-selection boundary (MSC assembly) | EVD-003 (Lost-in-the-Middle U-curve), EVD-016 (Self-Route, order preservation) | ARCHITECTURAL SKETCH | FUTURE |
| GraphStore | Repository-knowledge abstraction (extract/traverse/query with provenance) | EVD-005 (RepoGraph +32.8% relative) | ARCHITECTURAL SKETCH | FUTURE |
| Verifier | Verification boundary (layers + bounded repair + escalation) | EVD-009 (oracle-gated repair), EVD-015 (test-suite weakness) | ARCHITECTURAL SKETCH | FUTURE |
| EventLog | Event-persistence boundary (append/replay/anchor for audit + ablation) | EVD-015 (reproducibility need) | ARCHITECTURAL SKETCH | FUTURE |

Candidate operations (NOT signatures — names, arities, and shapes are Phase-3 work):

- `HarnessAdapter`: `detect / capabilities / install / configure / invoke /
  collect_output / collect_trace / verify` — necessity evaluated per-method in harness.md.
- `ContextRouter`: `route(task, graph, rules, budget) → MSC` with positional pinning.
- `GraphStore`: `extract / traverse(k≤2) / query / provenance(edge)`.
- `Verifier`: `verify(task) → VerificationResult(tests, types, lint, invariants, drift)`.
- `EventLog`: `append(event) / replay(since) / anchor()`.
- All exchanges are JSON-schema-shaped in Phase 3; Markdown is human projection only.

## What Phase 2 does NOT define
Executable workflows, final schemas, productive agents, benchmarks, auto-evolution
(§27). Anything in `src/` predating this baseline is bootstrap, not contract.
