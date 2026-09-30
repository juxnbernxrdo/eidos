# ADR-004: Contract-Bounded Fresh Subagents and Context Isolation

**Status:** Accepted  
**Date:** 2024-09-30 (Updated 2026)  
**Deciders:** Juan Bernardo Ordóñez (Author), AI Agent Systems Architecture Team  

---

## Context
When an AI agent engages in an extended coding session (20+ conversational turns), historical errors, irrelevant debugging output, and speculative explanations accumulate in the context window. Research from Stanford (*Lost in the Middle*) and Anthropic confirms that this leads to severe context pollution, high token costs, and a drop in task completion accuracy of over 40%.

## Decision
Eidos mandates **Contract-Bounded Fresh Subagents**:

1. **Zero Session History Inheritance**:
   Subagents spawned to execute an engineering task or subtask **must not inherit the parent conversation history**.
2. **Strict Task Contract Injection**:
   Every subagent is initialized with a freshly minted, schema-validated execution contract:
   ```json
   {
     "task_id": "TASK-042",
     "spec_id": "SPEC-007",
     "objective": "Implement deterministic JWT validation",
     "constraints": ["Zero third-party crypto libraries", "Must pass test_jwt.py"],
     "allowed_tools": ["view_file", "replace_file_content", "run_pytest"],
     "relevant_graph": ["auth/jwt.py", "auth/keys.py"],
     "evidence_anchor": "SEC-POL-003",
     "acceptance_criteria": ["All unit tests pass", "Type checker reports 0 errors"]
   }
   ```
3. **Bounded Tool Surface**:
   Subagents are only equipped with the minimum set of tools required for their declared objective, preventing unintended side effects or excessive agency.
4. **Structured Return Schema**:
   Upon completion or failure, the subagent terminates and returns a structured payload (`Finding`, `Patch`, `VerificationResult`), which the parent orchestrator records in the append-only event log.

## Consequences

### Positive
- Guarantees maximum attention capacity on the specific coding task.
- Eliminates context contamination and multi-turn error compounding.
- Dramatically lowers token consumption per task execution.
- Enables safe, parallel execution of disjoint subtasks across isolated Git worktrees.

### Negative
- The parent orchestrator must be precise in assembling the task contract; if a necessary dependency is omitted from `relevant_graph`, the subagent may lack critical context. (Mitigated by the `Context Router` graph traversal algorithm).
