# Eidos Components & Interfaces (Phase 2 — conceptual)

**Status:** ARCHITECTED (interfaces are sketches for Phase 3 contracts, NOT APIs).

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

## Interface sketches (Phase 3 will formalize; §6 reference shape retained, NOT frozen)

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
