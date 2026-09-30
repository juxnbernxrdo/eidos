# EIDOS Machine-Readable Schemas Specification

**Project:** Eidos — Engineering Intelligence for Deterministic, Orchestrated Software  
**Version:** 1.0.0  
**Specification:** JSON Schema (Draft 2020-12 Compliant)  
**Scope:** Formal Definitions for the 18 Foundational System Entities  

---

## 1. Overview of Entity Schemas

Eidos maintains a dual-plane architecture:
- **Human-Readable Plane**: High-craftsmanship Markdown (`CONSTITUTION.md`, `spec.md`, `tasks.md`, `GRAPH_REPORT.md`).
- **Machine-Readable Plane**: Strictly typed JSON Schemas with microsecond validation (`pydantic` v2 in Python, standard JSON Schema validators across harnesses).

Below are the complete, production-grade schema specifications for all 18 core entities.

---

## 2. Governance & Project Schemas

### 2.1 `Project` Schema (`project.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/project.schema.json",
  "title": "EidosProject",
  "type": "object",
  "properties": {
    "project_id": { "type": "string" },
    "name": { "type": "string" },
    "version": { "type": "string" },
    "documentation_language": { "type": "string", "enum": ["es", "en", "pt", "fr", "de", "zh"] },
    "lifecycle_state": { "type": "string", "enum": ["greenfield", "existing", "maintenance"] },
    "primary_harness": { "type": "string", "enum": ["antigravity", "claude_code", "opencode", "codex", "hermes", "headless"] },
    "target_environments": { "type": "array", "items": { "type": "string" } },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" }
  },
  "required": ["project_id", "name", "documentation_language", "primary_harness", "lifecycle_state"]
}
```

### 2.2 `Constitution` Schema (`constitution.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/constitution.schema.json",
  "title": "EidosConstitution",
  "type": "object",
  "properties": {
    "version": { "type": "string" },
    "immutable_principles": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "category": { "type": "string", "enum": ["architecture", "security", "testing", "documentation", "dependency", "ai_governance"] },
          "statement": { "type": "string" },
          "enforcement_level": { "type": "string", "enum": ["mandatory", "advisory"] }
        },
        "required": ["id", "category", "statement", "enforcement_level"]
      }
    },
    "ratified_at": { "type": "string", "format": "date-time" },
    "ratified_by": { "type": "string" }
  },
  "required": ["version", "immutable_principles", "ratified_at"]
}
```

### 2.3 `Rule` Schema (`rule.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/rule.schema.json",
  "title": "EidosRule",
  "type": "object",
  "properties": {
    "rule_id": { "type": "string" },
    "name": { "type": "string" },
    "category": { "type": "string", "enum": ["architecture", "coding_standard", "security", "testing", "git"] },
    "trigger": { "type": "string", "enum": ["always_on", "on_file_pattern", "model_decision"] },
    "file_patterns": { "type": "array", "items": { "type": "string" } },
    "invariant_assertion": { "type": "string" },
    "check_command": { "type": "string" },
    "remediation": { "type": "string" }
  },
  "required": ["rule_id", "name", "category", "trigger"]
}
```

---

## 3. Specification & Planning Schemas

### 3.1 `Spec` Schema (`spec.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/spec.schema.json",
  "title": "EidosSpec",
  "type": "object",
  "properties": {
    "spec_id": { "type": "string" },
    "title": { "type": "string" },
    "status": { "type": "string", "enum": ["draft", "approved", "in_progress", "converged", "deprecated"] },
    "requirements": { "type": "array", "items": { "type": "string" } },
    "subspecs": { "type": "array", "items": { "type": "string" } },
    "acceptance_criteria": { "type": "array", "items": { "type": "string" } },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" }
  },
  "required": ["spec_id", "title", "status", "requirements", "acceptance_criteria"]
}
```

### 3.2 `SubSpec` Schema (`subspec.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/subspec.schema.json",
  "title": "EidosSubSpec",
  "type": "object",
  "properties": {
    "subspec_id": { "type": "string" },
    "parent_spec_id": { "type": "string" },
    "module": { "type": "string" },
    "component": { "type": "string" },
    "interface_contract": { "type": "string" },
    "tasks": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["subspec_id", "parent_spec_id", "module", "component", "tasks"]
}
```

### 3.3 `Task` Schema (`task.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/task.schema.json",
  "title": "EidosTask",
  "type": "object",
  "properties": {
    "task_id": { "type": "string" },
    "spec_id": { "type": "string" },
    "subspec_id": { "type": "string" },
    "title": { "type": "string" },
    "status": { "type": "string", "enum": ["pending", "in_progress", "verified", "converged", "failed"] },
    "target_files": { "type": "array", "items": { "type": "string" } },
    "allowed_tools": { "type": "array", "items": { "type": "string" } },
    "acceptance_criteria": { "type": "array", "items": { "type": "string" } },
    "assigned_agent_id": { "type": "string" },
    "convergence_attempts": { "type": "integer", "default": 0 }
  },
  "required": ["task_id", "spec_id", "title", "status", "target_files"]
}
```

---

## 4. Agent & Tool Schemas

### 4.1 `Agent` Schema (`agent.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/agent.schema.json",
  "title": "EidosAgent",
  "type": "object",
  "properties": {
    "agent_id": { "type": "string" },
    "role": { "type": "string" },
    "harness": { "type": "string" },
    "model_id": { "type": "string" },
    "context_budget": { "type": "integer" },
    "tools": { "type": "array", "items": { "type": "string" } },
    "skills": { "type": "array", "items": { "type": "string" } },
    "isolation_level": { "type": "string", "enum": ["in_process", "worktree", "container", "sandbox"] }
  },
  "required": ["agent_id", "role", "harness", "model_id", "isolation_level"]
}
```

### 4.2 `Skill` Schema (`skill.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/skill.schema.json",
  "title": "EidosSkill",
  "type": "object",
  "properties": {
    "skill_id": { "type": "string" },
    "name": { "type": "string" },
    "version": { "type": "string" },
    "description": { "type": "string" },
    "provenance": {
      "type": "object",
      "properties": {
        "source": { "type": "string" },
        "author": { "type": "string" },
        "license": { "type": "string" },
        "commit_hash": { "type": "string" },
        "security_score": { "type": "number", "minimum": 0, "maximum": 100 }
      },
      "required": ["source", "license", "security_score"]
    },
    "entrypoint": { "type": "string" },
    "permissions": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["skill_id", "name", "version", "description", "provenance"]
}
```

### 4.3 `Tool` Schema (`tool.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/tool.schema.json",
  "title": "EidosTool",
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "description": { "type": "string" },
    "parameters": { "type": "object" },
    "returns": { "type": "object" },
    "is_read_only": { "type": "boolean" },
    "is_sandboxed": { "type": "boolean" }
  },
  "required": ["name", "description", "parameters", "is_read_only"]
}
```

---

## 5. Repository Intelligence Graph Schemas

### 5.1 `GraphNode` Schema (`graph_node.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/graph_node.schema.json",
  "title": "EidosGraphNode",
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "type": {
      "type": "string",
      "enum": ["File", "Module", "Class", "Function", "API", "Database", "Dependency", "Test", "Spec", "SubSpec", "Task", "Agent", "Skill", "Rule", "Finding"]
    },
    "label": { "type": "string" },
    "file_path": { "type": "string" },
    "line_range": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 },
    "community_id": { "type": "integer" },
    "centrality": { "type": "number" },
    "metadata": { "type": "object" }
  },
  "required": ["id", "type", "label"]
}
```

### 5.2 `GraphEdge` Schema (`graph_edge.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/graph_edge.schema.json",
  "title": "EidosGraphEdge",
  "type": "object",
  "properties": {
    "source": { "type": "string" },
    "target": { "type": "string" },
    "relation": {
      "type": "string",
      "enum": ["IMPLEMENTS", "DEPENDS_ON", "TESTED_BY", "DOCUMENTED_BY", "DEFINED_BY", "MODIFIED_BY", "VIOLATES", "SATISFIES", "DERIVED_FROM", "CONFLICTS_WITH", "SUPERSEDES"]
    },
    "epistemic_type": {
      "type": "string",
      "enum": ["EXTRACTED", "INFERRED", "USER_CONFIRMED", "AGENT_PROPOSED"]
    },
    "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "evidence_ref": { "type": "string" }
  },
  "required": ["source", "target", "relation", "epistemic_type", "confidence"]
}
```

---

## 6. Execution, Verification & Progress Schemas

### 6.1 `Evidence` Schema (`evidence.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/evidence.schema.json",
  "title": "EidosEvidence",
  "type": "object",
  "properties": {
    "evidence_id": { "type": "string" },
    "claim": { "type": "string" },
    "type": { "type": "string", "enum": ["observed", "reproduced", "inferred", "human_confirmed"] },
    "source_file": { "type": "string" },
    "line_range": { "type": "array", "items": { "type": "integer" } },
    "graph_node_id": { "type": "string" },
    "verification_command": { "type": "string" },
    "stdout": { "type": "string" },
    "stderr": { "type": "string" },
    "exit_code": { "type": "integer" },
    "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "timestamp": { "type": "string", "format": "date-time" },
    "git_commit": { "type": "string" }
  },
  "required": ["evidence_id", "claim", "type", "confidence", "timestamp", "git_commit"]
}
```

### 6.2 `Session` Schema (`session.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/session.schema.json",
  "title": "EidosSession",
  "type": "object",
  "properties": {
    "session_id": { "type": "string" },
    "harness": { "type": "string" },
    "user_id": { "type": "string" },
    "started_at": { "type": "string", "format": "date-time" },
    "ended_at": { "type": "string", "format": "date-time" },
    "active_spec_id": { "type": "string" },
    "total_tokens": { "type": "integer" },
    "total_cost": { "type": "number" },
    "tasks_completed": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["session_id", "harness", "started_at"]
}
```

### 6.3 `ProgressEvent` Schema (`progress_event.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/progress_event.schema.json",
  "title": "EidosProgressEvent",
  "type": "object",
  "properties": {
    "event_id": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "session_id": { "type": "string" },
    "task_id": { "type": "string" },
    "agent_id": { "type": "string" },
    "event_type": {
      "type": "string",
      "enum": [
        "TASK_INITIALIZED", "TOOL_INVOKED", "TOOL_COMPLETED", "TOOL_FAILED",
        "VERIFICATION_STARTED", "VERIFICATION_PASSED", "VERIFICATION_FAILED",
        "REPAIR_ATTEMPTED", "PATCH_APPLIED", "TASK_CONVERGED", "DRIFT_DETECTED",
        "HUMAN_FEEDBACK_RECORDED"
      ]
    },
    "payload": { "type": "object" },
    "git_commit": { "type": "string" }
  },
  "required": ["event_id", "timestamp", "session_id", "event_type", "git_commit"]
}
```

### 6.4 `VerificationResult` Schema (`verification_result.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/verification_result.schema.json",
  "title": "EidosVerificationResult",
  "type": "object",
  "properties": {
    "verification_id": { "type": "string" },
    "task_id": { "type": "string" },
    "converged": { "type": "boolean" },
    "test_suite": {
      "type": "object",
      "properties": {
        "passed": { "type": "integer" },
        "failed": { "type": "integer" },
        "coverage": { "type": "number" },
        "failure_traces": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["passed", "failed"]
    },
    "type_check": {
      "type": "object",
      "properties": {
        "errors": { "type": "integer" },
        "messages": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["errors"]
    },
    "lint": {
      "type": "object",
      "properties": {
        "violations": { "type": "integer" },
        "details": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["violations"]
    },
    "invariant_violations": { "type": "array", "items": { "type": "string" } },
    "timestamp": { "type": "string", "format": "date-time" }
  },
  "required": ["verification_id", "task_id", "converged", "test_suite", "type_check", "lint", "timestamp"]
}
```

### 6.5 `Finding` Schema (`finding.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/finding.schema.json",
  "title": "EidosFinding",
  "type": "object",
  "properties": {
    "finding_id": { "type": "string" },
    "severity": { "type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"] },
    "category": { "type": "string", "enum": ["SECURITY", "ARCHITECTURE", "PERFORMANCE", "DEAD_CODE", "DRIFT", "BUG"] },
    "title": { "type": "string" },
    "description": { "type": "string" },
    "file_path": { "type": "string" },
    "line_range": { "type": "array", "items": { "type": "integer" } },
    "evidence_ref": { "type": "string" },
    "remediation": { "type": "string" }
  },
  "required": ["finding_id", "severity", "category", "title", "description", "file_path"]
}
```

---

## 7. Evaluation & Evolution Schemas

### 7.1 `EvaluationRun` Schema (`evaluation_run.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/evaluation_run.schema.json",
  "title": "EidosEvaluationRun",
  "type": "object",
  "properties": {
    "run_id": { "type": "string" },
    "benchmark": { "type": "string" },
    "harness": { "type": "string" },
    "model_id": { "type": "string" },
    "total_tasks": { "type": "integer" },
    "solved_tasks": { "type": "integer" },
    "verified_success_rate": { "type": "number" },
    "total_tokens": { "type": "integer" },
    "total_cost": { "type": "number" },
    "mean_turns": { "type": "number" },
    "started_at": { "type": "string", "format": "date-time" },
    "finished_at": { "type": "string", "format": "date-time" }
  },
  "required": ["run_id", "benchmark", "harness", "model_id", "verified_success_rate"]
}
```

### 7.2 `LearningProposal` Schema (`learning_proposal.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://eidos.dev/schemas/learning_proposal.schema.json",
  "title": "EidosLearningProposal",
  "type": "object",
  "properties": {
    "proposal_id": { "type": "string" },
    "category": { "type": "string", "enum": ["new_rule", "invariant_refinement", "skill_creation", "context_routing_optimization"] },
    "rationale": { "type": "string" },
    "observed_patterns": { "type": "array", "items": { "type": "string" } },
    "evidence_refs": { "type": "array", "items": { "type": "string" } },
    "proposed_changes": { "type": "object" },
    "status": { "type": "string", "enum": ["proposed", "testing", "accepted", "rejected"] },
    "reviewed_by": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" }
  },
  "required": ["proposal_id", "category", "rationale", "observed_patterns", "status"]
}
```
