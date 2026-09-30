# Learning Proposal `PROP-EVO-001`: Adaptive Early-Stopping on Repair Loops

**Proposal Identifier:** `PROP-EVO-001`  
**Target Subsystem:** [`src/eidos/orchestration/pipeline.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/orchestration/pipeline.py)  
**Category:** `ORCHESTRATION_EFFICIENCY`  
**Governing Specification:** `SPEC-002-PIPELINE` & `SPEC-014-EVOLUTION-PIPELINE`  
**Final Status:** **ACCEPTED & MERGED**  
**Approval Signature:** `HUMAN-OPERATOR-GOVERNANCE`  
**Date Ratified:** 2026-09-30  

---

## 1. Problem Statement & Empirical Rationale

In Phase 7 Experiment `EXP-003` (Repair Loop Bound Calibration), analysis revealed that when an agent generates an incorrect patch and receives an oracle error trace:
- If the agent makes a meaningful revision, convergence occurs in $k=1$ (58%) or $k=2$ (cumulative 82%).
- In $14\%$ of difficult trials, the agent enters an **unproductive error loop**: repeating the exact same defect or generating identical failing assertions across consecutive turns.
- In unassisted systems, continuing to attempt repair up to $K=5$ burns an additional $\sim 1,500$ completion tokens per task with a marginal resolution rate of $<5\%$.

**Evolution Objective**: Implement **Adaptive Cycle Detection** in [`PhasedPipeline.execute_bounded_repair_loop`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/orchestration/pipeline.py). If the oracle diagnostic trace emitted at iteration $k$ is identical to iteration $k-1$, execution terminates early, transitioning to `PipelineStage.ESCALATED` with reason `REPETITIVE_ERROR_CYCLE_DETECTED`.

---

## 2. Formal Proposed Code Modification

```python
--- a/src/eidos/orchestration/pipeline.py
+++ b/src/eidos/orchestration/pipeline.py
@@ -103,9 +103,11 @@ class PhasedPipeline:
         self,
         task: TaskRecord,
         verifier_fn: Callable[[int], Any],
         repair_fn: Callable[[str], None],
+        adaptive_early_stopping: bool = True,
     ) -> dict[str, Any]:
         """Executes bounded repair loop up to K iterations with adaptive early-stopping."""
         attempt = 1
+        previous_trace: str | None = None
 
         while attempt <= self.max_repair_k:
             # 1. Run verification
@@ -121,6 +123,24 @@ class PhasedPipeline:
                     "verification_result": verif_result,
                 }
 
+            oracle_trace = getattr(verif_result, "oracle_trace", "") or str(verif_result)
+
+            # EVO-001: Adaptive early-stopping on repetitive failure cycles
+            if adaptive_early_stopping and previous_trace is not None and oracle_trace == previous_trace:
+                self.current_stage = PipelineStage.ESCALATED
+                task.status = TaskStatus.ESCALATED
+                diff = self.capture_diagnostic_diff()
+                return {
+                    "verdict": "ESCALATED",
+                    "converged": False,
+                    "attempts": attempt,
+                    "escalation_payload": {
+                        "reason": "REPETITIVE_ERROR_CYCLE_DETECTED",
+                        "failure_summary": f"Task '{task.task_id}' aborted early at attempt {attempt} due to repetitive error cycle",
+                        "diagnostic_diff": diff,
+                        "oracle_trace": oracle_trace,
+                    },
+                }
+
+            previous_trace = oracle_trace
```

---

## 3. Sandboxed Evaluation Results

The candidate modification was tested in an isolated sandbox against 20 synthetic cyclic failure trials:
- **Baseline Behavior ($K=5$ fixed)**: Exhausted 5 iterations $\times$ 650 tokens = 3,250 tokens per failing task.
- **Adaptive Early-Stopping**: Terminated deterministically at attempt 2 = 1,300 tokens per failing task.
- **Observed Token Savings**: **$60.0\%$ reduction** in token waste on non-converging tasks.
- **Regression Audit**: All existing 108 verification and unit tests passed with **zero regressions**.

---

## 4. Operator Human Review & Approval Record

```json
{
  "proposal_id": "PROP-EVO-001",
  "title": "Adaptive Early-Stopping on Repair Loops",
  "status": "ACCEPTED",
  "benchmark_delta_vsr": 0.0,
  "token_savings_percent": 60.0,
  "regressions_detected": 0,
  "approved_by": "HUMAN-OPERATOR-GOVERNANCE",
  "approved_at": "2026-09-30T21:34:00Z"
}
```

**Verdict:** Ratified for merge into core orchestration codebase.
