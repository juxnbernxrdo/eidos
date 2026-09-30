# SPEC-010 — Contract-Bounded Subagents & CodeAct Execution

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavior of Eidos subagents: contract-bounded, fresh-context agent instances operating in a star topology using the CodeAct execution paradigm inside an isolated sandbox.

## 3. Scope
Subagent spawning, fresh context provisioning, star-topology coordination, tool execution via Python CodeAct, and termination upon task return.

## 4. Non-Goals
- Does not permit unconstrained multi-agent freeform peer chat (avoids AutoGen error loops).
- Does not preserve persistent conversational memory across subtasks.
- Does not allow subagents to self-assign tasks or alter their own permissions.

## 5. Source Requirements
- `REQ-AGENT-001`: Fresh Context per Subtask
- `REQ-AGENT-002`: CodeAct Programmatic Execution Space

## 6. Architectural Basis
- `docs/architecture/agents.md`: Subagent unit, isolation, and CodeAct lineage.
- `docs/adr/P2-ADR-003`: Contract subagents with CodeAct action space.
- `docs/research/evidence-registry.md`: EVD-004 (orchestrator-workers +90.2%), EVD-006 (CodeAct +20% success across 17 LLMs).

## 7. Contract Dependencies
- `CORE-CONTRACT-002`: Task Contract.
- `CORE-CONTRACT-003`: Agent Contract schema (`schemas/contracts/core/agent.schema.json`).
- `CORE-CONTRACT-008`: Capability & Permission Contract.

## 8. Behavioral Requirements
Subagents are strictly bounded:
```text
Parent Task Dispatch ──► Fresh Subagent Spawn ──► MSC Ingest ──► Sandboxed CodeAct ──► Output Return ──► Terminate
```
- A subagent is instantiated with a dedicated task contract and fresh MSC payload.
- It receives zero conversational history from parent or sibling agents.
- All coordination is strictly hierarchical through the parent (star topology); lateral peer chatter is forbidden.
- For programmatic code modification, subagents execute Python code blocks in a sandbox to inspect state and debug tracebacks directly.

## 9. Inputs
- Subagent definition conforming to `CORE-CONTRACT-003`.
- Bounded Task Contract (`CORE-CONTRACT-002`) and MSC payload (`CTX-CONTRACT-001`).

## 10. Outputs
- Structured execution outcome: `Finding`, `PatchDiff`, or `Artifact` collection.
- Local verification trace before returning control to parent.

## 11. State Model
Lifecycle: `SPAWN → INITIALIZE → EXECUTE (turn <= 30) → VERIFY_LOCAL → REPORT → TERMINATE`.
Subagents are ephemeral; their processes and working memory are destroyed immediately upon task termination.

## 12. Invariants
- `INV-001`: Subagent contract declarations are model-provider neutral.
- `INV-002`: Subagents running in parallel operate on isolated Git worktrees to prevent clobbering.
- Constitution Art. IX: Fresh context guarantee on every subagent dispatch.

## 13. Preconditions
- A valid Task Contract and Capability Grant must exist before spawning.

## 14. Postconditions
- All spawned subprocesses, temporary files, and working memory buffers are destroyed upon termination.

## 15. Failure Semantics
If a subagent exceeds its maximum turn limit ($\le 30$) without completing the task, the parent terminates the subagent, recovers the best-so-far diff, and initiates repair or escalation.

## 16. Security Requirements
- Sandboxed execution: Subagents cannot access the parent host process or read unauthorized directories.
- Tool capabilities are locked to the declared task scope.

## 17. Observability Requirements
- Emits turn metrics: total tokens consumed, turn duration, tool invocations, and traceback errors encountered.

## 18. Edge Cases
- Parallel subagent collision: Parallel lanes (3–5 lanes) must be isolated on dedicated Git worktrees. Merge conflicts are resolved by the parent orchestrator.
- Infinite execution loops: Enforced turn ceiling halts runaway loops deterministically.

## 19. Acceptance Criteria
### `AC-010-01` (Fresh Context Isolation)
```gherkin
Given a parent session with 25 prior conversation turns
When a subagent is spawned to execute TASK-002
Then the subagent prompt context must contain only the TASK-002 contract and MSC payload, with zero parent conversation turns.
```

### `AC-010-02` (CodeAct Sandboxed Execution)
```gherkin
Given a subagent tasked with computing AST metrics
When the subagent executes a Python script block
Then the script executes inside the sandbox and stdout/traceback is captured directly for self-debugging.
```

## 20. Verification Strategy
Integration tests in `tests/specs/test_subagents.py` validating context purity, parallel worktree isolation, and turn cap enforcement.

## 21. Traceability
- Research: EVD-004, EVD-006
- ADR: `P2-ADR-003`
- Contract: `CORE-CONTRACT-002`, `CORE-CONTRACT-003`
- Requirements: `REQ-AGENT-001`, `REQ-AGENT-002`

## 22. Open Questions & Phase 5 Notes
- Parallel subagent lane scaling (3 vs 5 lanes) to be measured under controlled evaluation in Phase 7 (`EXP-002`).
- Phase 5 note: CodeAct execution must run via isolated subprocess with timeout wrappers.
