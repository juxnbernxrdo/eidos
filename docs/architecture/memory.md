# Memory Architecture (Phase 2)

**Status:** CONCEPTUAL / EXPERIMENTAL-gated | Basis: dialogue-only gains
(A-MEM +35%, Mem0 +26%/-91% p95) vs contamination cascade (SRC-029 ρ-formalism,
MemoryGraft, MINJA) — SWE transfer HYPOTHESIS (GAP-007/EXP-005). Ships OPT-IN
only (ARR-01). Vocabulary: CoALA (working/episodic/semantic/procedural).

## Tiers

| Tier | Lifetime | Scope | Ownership | Retrieval | Persistence | Deletion | Privacy | Contamination risk |
|---|---|---|---|---|---|---|---|---|
| Working | subtask | agent | orchestrator | direct | none (destroyed at termination) | automatic | n/a (ephemeral) | low (bounded) |
| Project | repo lifetime | repo | repo (git-tracked `.eidos/memory/`) | scoped queries | versioned | explicit commit | repo-confidential | medium → gated writes |
| Institutional | cross-project | org | human-approved `~/.eidos/institutional/` | sanitized heuristics | versioned, signed | human-only | sanitized, approved | HIGH → human gate mandatory |

## Rules (architectural, pre-contract)

1. **Write-time admission gate** (ConsistencyGate lineage: multi-sample verify,
   admit iff `p̂ ≥ τ`; track cascade rate `ρ = |false|/|M|` as invariant signal).
2. **Cross-project memory is Explicit, Configurable, Sanitized, Auditable,
   Optional** — never default-on (INV-002).
3. Procedural memory (prompts/code) is versioned; writes never auto-execute.
4. Anthropic project-memory precedent (SRC-107) adopted for scoping; MEMORY.md vs
   config confusion (issue #23341 lineage) avoided by single canonical path.

## Open (EXP-005)
Memory on/off ΔVSR on multi-session SWE tasks; τ calibration; sanitization-utility
trade-off; approval-burden budget.
