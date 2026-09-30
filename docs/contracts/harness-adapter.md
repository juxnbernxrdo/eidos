# Harness Adapter Contract (`HARN-CONTRACT-001`)

**Contract ID:** `HARN-CONTRACT-001`  
**Version:** 1.0.0  
**Status:** ACCEPTED  
**Owner Domain:** Harness  
**Machine Schema:** [`harness-adapter.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/harness/harness-adapter.schema.json)  
**Architecture Basis:** [P2-ADR-005](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-005-harness-adapters.md), [harness.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/harness.md), [EVD-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [EVD-002](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), SRC-105

---

## 1. Purpose & System Boundary

The `HarnessAdapter` contract formalizes the boundary between Eidos Core and external agent execution hosts (Google Antigravity, Claude Code, OpenCode, Codex, Hermes, and Headless CI). 

Its purpose is to provide host harness portability **without leaking host-specific concepts into Eidos Core** (Principle P1, Constitution Art. II).

### Non-Goals:
- Eidos is **not** an agent host or IDE; it does not replace the harness runtime.
- The adapter does **not** evaluate model quality or perform verification certification.
- Host-internal prompts, proprietary weights, and unexposed routing mechanisms remain `UNKNOWN` by construction (Honesty Axiom).

---

## 2. Operation Analysis & Categorization

Each candidate operation identified in Phase 2 is categorized according to its architectural necessity:

| Operation | Category | Rationale & Architectural Rule |
|---|---|---|
| `detect()` | **REQUIRED** | Inspects workspace markers (e.g. `.gemini/`, `.claude/`) for zero-config harness discovery. |
| `capabilities()` | **REQUIRED** | Declares support for subagents, CodeAct, MCP stdio, worktree isolation, and trace fidelity. |
| `configure(config)` | **REQUIRED** | Mounts Eidos rule files (`AGENTS.md`), contracts, and MCP server bindings into host workspace. |
| `invoke(dispatch_req)` | **REQUIRED** | Dispatches a contract-bounded task with explicit MSC payload, permissions, and timeout. |
| `collect_output(exec_id)` | **REQUIRED** | Gathers structured results (summary, patch diffs, created/modified artifacts, errors). |
| `collect_trace(exec_id)` | **REQUIRED** | Ingests the complete raw observation stream for the append-only event log and benchmark runs. |
| `install()` | **OPTIONAL** | Permitted only for thin host bridge packages (`npx`/`uvx`). Core never installs full host software. |
| `verify()` | **DROPPED** | **Architectural Non-Goal**: Verification belongs strictly to the Verifier domain (P5). Adapters must not self-certify. |
| Keep-alive / Pipes | **ADAPTER-INTERNAL**| Transport-level IPC mechanics are encapsulated entirely within the adapter implementation. |

---

## 3. Formal Lifecycle State Machine

The adapter must progress through a deterministic state machine:

```text
               ┌─────────────┐
               │ UNDETECTED  │
               └──────┬──────┘
                      │ detect()
               ┌──────▼──────┐
        ┌──────┤  DETECTED   ├──────┐
        │      └──────┬──────┘      │
        │             │ check       │
        │      ┌──────▼──────┐      │
        │      │  AVAILABLE  │      │
        │      └──────┬──────┘      │
        │             │ configure() │
        │      ┌──────▼──────┐      │
        │      │ CONFIGURED  │      │
        │      └──────┬──────┘      │
        │             │ ready check │
        │      ┌──────▼──────┐      │
        │      │    READY    │◄─────┼────────────────┐
        │      └──────┬──────┘      │                │
        │             │ invoke()    │                │
        │      ┌──────▼──────┐      │                │
        │      │   RUNNING   │      │                │
        │      └──┬────────┬─┘      │                │
        │         │        │        │                │
        │ success │        │ error  │                │
        │  ┌──────▼──────┐ │ ┌──────▼──────┐         │
        │  │  COMPLETED  │ │ │   FAILED    │─────────┘ (reset)
        │  └──────┬──────┘ │ └─────────────┘
        │         └────────┼────────┐
        │                  │        │
        ▼                  ▼        ▼
  ┌───────────────────────────────────┐
  │            UNAVAILABLE            │
  └───────────────────────────────────┘
```

Valid transitions:
- `UNDETECTED → DETECTED`: Markers located in environment/workspace.
- `DETECTED → AVAILABLE`: Required binary/CLI/socket accessible.
- `AVAILABLE → CONFIGURED`: Configuration mounted; contracts and tools registered.
- `CONFIGURED → READY`: Handshake successful, ready for dispatch.
- `READY → RUNNING`: Task dispatched via `invoke()`.
- `RUNNING → COMPLETED`: Task finished within turn/time bounds; output collected.
- `RUNNING → FAILED`: Execution error, timeout, or uncaught host exception.
- `FAILED → READY`: Adapter state reset after recording failure event.
- `* → UNAVAILABLE`: Fatal process termination or lost connection.

---

## 4. Contract Schema Definition

The machine-readable schema is canonically located at [`schemas/contracts/harness/harness-adapter.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/harness/harness-adapter.schema.json).

### 4.1 Input Specification (`dispatch_request`)
- `execution_id`: Unique identifier for the dispatch run.
- `task`: Contract-bound task definition (id, objective, target files, allowed tools).
- `context_payload`: Minimal Sufficient Context (MSC) payload with token count.
- `permissions`: Declared security boundary:
  - `filesystem_scope`: `repo_read_only` | `worktree_write` | `repo_write` | `isolated_sandbox`
  - `network_scope`: `disabled` | `local_only` | `explicit_whitelist` | `unrestricted`
  - `max_turns`: Strictly bounded integer $[1, 100]$.
  - `timeout_seconds`: Strictly bounded integer $[1, 7200]$.
- `environment`: Key-value strings (zero secrets permitted).

### 4.2 Output Specification (`execution_response`)
- `execution_id`: Correlated run identifier.
- `status`: `COMPLETED` | `FAILED` | `TIMED_OUT` | `CANCELLED`.
- `result_summary`: High-level summary of action taken.
- `patch_diff`: Unified diff of modified code (if any).
- `artifacts`: Array of affected files with SHA-256 hashes and action (`created`, `modified`, `deleted`).
- `observation_trace`: Turn-by-turn trace items (action, input, output, exit code).
- `evidence_refs`: Array of generated evidence identifiers.
- `errors`: Typed errors conforming to the canonical error taxonomy.

---

## 5. Security & Isolation Boundaries

1. **No Implicit Grants**: The adapter cannot grant access beyond the contract's declared `permissions`.
2. **Cross-Project Isolation (INV-002)**: The adapter must restrict operations to the active repository root. Probing parent directories or sibling projects is rejected with `PERMISSION_DENIED`.
3. **Secret Redaction**: Any environment variables or outputs matching secret entropy signatures must be redacted before entering `collect_trace()`.

---

## 6. Architectural Invariants Bound

- **INV-001 (Model-Provider Agnosticism)**: The adapter presents a uniform interface regardless of whether the host uses Claude, GPT, Gemini, or local models.
- **INV-002 (Cross-Project Isolation)**: Zero leakage of state across distinct repository workspaces.
- **INV-003 (Claims Are Not Evidence)**: Adapter `COMPLETED` status indicates execution finish, **never** convergence or validation.

---

## 7. Phase 4 Handoff

Phase 4 will specify:
- Concrete adapter bridge protocols (e.g. MCP stdio transports, Antigravity brain artifact integration, Claude Code hook mappings).
- Timeout negotiation algorithms.
- Conformance test scenarios for host harnesses under test.
