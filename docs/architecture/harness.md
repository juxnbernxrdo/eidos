# Harness Adapter Architecture (Phase 2)

**Status:** ARCHITECTED | Basis: EVD-001/002 (harness moves outcomes),
SRC-105 (MCP), OSS snapshots (SRC-200..203). Breakage/overhead OPEN (EXP-007).

## Concept

```text
Harness → Harness Adapter → Capabilities → Execution → Trace → Evidence
```

Eidos observes only what the adapter can capture; unobservable host internals
(model weights, proprietary routing) are UNKNOWN by construction and must never
be inferred-into-existence (Honesty Axiom).

## Method evaluation (§6 — the sketch is NOT frozen)

| Method | Verdict | Rationale |
|---|---|---|
| `detect` | REQUIRED | Workspace fingerprint → harness selection; zero-config init |
| `capabilities` | REQUIRED | Common capability matrix (exec, LSP, subagents, MCP, worktrees, sandbox) |
| `configure` | REQUIRED | Mount contracts/skills/rules (`AGENTS.md`/`CLAUDE.md`/MCP stdio) |
| `invoke` | REQUIRED | Dispatch bounded task (contract in, execution id out) |
| `collect_output` | REQUIRED | Structured result payload (Finding/Patch/VerificationResult) |
| `collect_trace` | REQUIRED | Full observation stream for events + `evaluation_run.json` |
| `install` | OPTIONAL | Thin bridge packages only (`npx`/`uvx` wrappers); core never auto-installs host |
| `verify` | DROPPED as adapter duty | Verification belongs to Verification domain (P5); adapters must not self-certify |

## Common vs specific

- Common: task dispatch, output/trace collection, capability declaration, MCP stdio.
- Specific (isolated per adapter): Antigravity brain-artifacts, Claude Code hooks/
  compaction, OpenCode LSP+TUI sessions, Codex/Cursor cloud boundaries, Hermes
  daemon/gateway. Specifics never leak into Core (P1/P2, INV-001).

## Observability / permissions

- Observable: tool calls + args, stdout/stderr, file diffs, test logs, token/time
  accounting where host exposes it.
- NOT observable: host-internal prompts, weight versions beyond declared IDs,
  other-project data (INV-002 enforced at adapter boundary).
- Permissions: least-privilege; destructive ops require explicit contract scope +
  sandbox (security.md).

## First-class adapters (priorities, not promises)

Antigravity (primary dev harness, Axiom 0) → Claude Code → OpenCode →
Codex/Cursor → Hermes → Headless (benchmark/CI reference harness for EXP-001,
mini-SWE-agent lineage for fair model comparison).
