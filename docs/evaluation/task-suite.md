# Phase 7 Task Suite Specification (TSK-EVAL-001 – 010)

**Authority:** Phase 7 Experimental Evaluation Program  
**Source Module:** [`src/eidos/evaluation/benchmark.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/evaluation/benchmark.py)  
**Status:** CANONICAL TASK SPECIFICATIONS  

---

## Task Details

### `TSK-EVAL-001`: Fix Boundary Condition in Paginated Window Calculation
- **Task Type:** `BUG_FIX` | **Difficulty:** `SMALL` | **Security Sensitive:** No
- **Description:** Fix `paginate_items(items, page, page_size)` in `pagination.py`. Currently, requesting the last page with an exact multiple of `page_size` raises `IndexError` instead of returning an empty or exact list.
- **Initial Files:** `pagination.py`
- **Public Tests:**
  ```python
  assert paginate_items([1, 2, 3, 4], 1, 2) == [1, 2]
  assert paginate_items([1, 2, 3, 4], 2, 2) == [3, 4]
  ```
- **Hidden Tests:**
  ```python
  assert paginate_items([], 1, 10) == []
  assert paginate_items([1, 2, 3], 3, 2) == []
  ```
- **Invariant:** `PAGINATION_BOUNDS`

---

### `TSK-EVAL-002`: Implement Schema-Validated JSON Event Ingestion Pipe
- **Task Type:** `FEATURE_IMPL` | **Difficulty:** `MEDIUM` | **Security Sensitive:** No
- **Description:** Implement `EventIngester.ingest(record_str: str) -> dict` in `ingester.py`. Reject malformed JSON, enforce required fields (`event_id`, `timestamp`, `source`), and reject timestamps > current time + 300s.
- **Initial Files:** `ingester.py`
- **Public Tests:** Valid JSON record ingestion returns parsed dictionary.
- **Hidden Tests:** Malformed JSON raises `ValueError`; missing required fields raises `ValueError`; future timestamps raise `ValueError`.
- **Invariant:** `EVENT_INGEST_STRICT_SCHEMA`

---

### `TSK-EVAL-003`: Extract Shared Token Counter Without Breaking Public API
- **Task Type:** `REFACTORING` | **Difficulty:** `MEDIUM` | **Security Sensitive:** No
- **Description:** Extract duplicated token estimation logic from `router.py` and `projector.py` into `counter.py:estimate_tokens(text: str) -> int`. Preserve backward compatibility for existing callers.
- **Initial Files:** `router.py`, `projector.py`
- **Public Tests:** Existing `route()` and `calc_cost()` functions continue to return correct values.
- **Hidden Tests:** `estimate_tokens` correctly calculates tokens; large strings routed accurately.
- **Invariant:** `DRY_CODE_COMPATIBILITY`

---

### `TSK-EVAL-004`: Eliminate Path Traversal Vulnerability in File Reader
- **Task Type:** `SECURITY_FIX` | **Difficulty:** `SMALL` | **Security Sensitive:** **YES**
- **Description:** In `reader.py`, fix `safe_read(root: str, path: str) -> str`. Prevent path traversal attacks (`../../etc/passwd`) using canonical `os.path.realpath` containment check.
- **Initial Files:** `reader.py`
- **Public Tests:** Normal file inside directory reads successfully.
- **Hidden Tests:** Traversal escapes (`../outside`) raise `PermissionError`.
- **Invariant:** `SANDBOX_CONFINEMENT_REALPATH`

---

### `TSK-EVAL-005`: Synchronize Schema Rename Across Producer and Consumer
- **Task Type:** `CONTRACT_REPAIR` | **Difficulty:** `MEDIUM` | **Security Sensitive:** No
- **Description:** Field `agent_id` was renamed to `actor_id` in contract `schema.py`. Update producer `emitter.py` and consumer `handler.py` to match the new schema.
- **Initial Files:** `schema.py`, `emitter.py`, `handler.py`
- **Public Tests:** `emitter.emit()` output processed successfully by `handler.process()`.
- **Hidden Tests:** Directly created `Payload(actor_id=...)` instances handled without error.
- **Invariant:** `CONTRACT_SCHEMA_SYNCHRONY`

---

### `TSK-EVAL-006`: Break Illegal Circular Dependency Between Core and CLI
- **Task Type:** `ARCH_INVARIANT_FIX` | **Difficulty:** `MEDIUM` | **Security Sensitive:** No
- **Description:** In `core_engine.py`, an import of `cli_formatter` violates `ARCH-001`. Extract a shared interface into `protocol.py` to decouple core from CLI.
- **Initial Files:** `cli_formatter.py`, `core_engine.py`
- **Public Tests:** Message execution output preserved.
- **Hidden Tests:** AST audit confirms zero imports of `cli` in `core_engine.py`.
- **Invariant:** `ARCH-001_CORE_ISOLATION`

---

### `TSK-EVAL-007`: Repair Brittle Timing-Dependent Test Oracle
- **Task Type:** `TEST_REPAIR` | **Difficulty:** `SMALL` | **Security Sensitive:** No
- **Description:** Repair flaky test in `test_timer.py` that fails under varying system load due to exact float comparison `assert elapsed == 0.05`. Use `math.isclose` with tolerance.
- **Initial Files:** `test_timer.py`
- **Public Tests:** `test_elapsed()` executes without exception.
- **Hidden Tests:** AST audit verifies `math.isclose` or `abs()` tolerance in source.
- **Invariant:** `DETERMINISTIC_TEST_ORACLE`

---

### `TSK-EVAL-008`: Integrate Event Log Append with State Machine Update
- **Task Type:** `CROSS_MODULE_INTEGRATION` | **Difficulty:** `LARGE` | **Security Sensitive:** No
- **Description:** Wire `EventStream` in `stream.py` to notify `Aggregator` in `aggregator.py` on event append, ensuring monotonic updates without duplicate processing.
- **Initial Files:** `stream.py`, `aggregator.py`
- **Public Tests:** Single event notification increments aggregator count to 1.
- **Hidden Tests:** Duplicate event IDs are deduplicated; distinct events increment count monotonically.
- **Invariant:** `IDEMPOTENT_EVENT_INTEGRATION`

---

### `TSK-EVAL-009`: Optimize O(N^2) Node Lookup with In-Memory Hash Index
- **Task Type:** `PERF_OPTIMIZATION` | **Difficulty:** `MEDIUM` | **Security Sensitive:** No
- **Description:** In `graph_lookup.py`, `find_by_type` performs an $O(N)$ linear scan. Replace with a dictionary mapping type to a list of node IDs for $O(1)$ amortized retrieval.
- **Initial Files:** `graph_lookup.py`
- **Public Tests:** `find_by_type` returns correct node IDs.
- **Hidden Tests:** Performance check with 1,000 nodes; dictionary indexing confirmed in source.
- **Invariant:** `SUB_LINEAR_INDEX_EFFICIENCY`

---

### `TSK-EVAL-010`: End-to-End Task Convergence with Feature Passport
- **Task Type:** `SYSTEM_INTEGRATION` | **Difficulty:** `SYSTEM` | **Security Sensitive:** **YES**
- **Description:** Implement `SystemRunner.run(task: dict)` in `system.py`. Must reject convergence if `verified` is false or `passport` is missing, and transition to `CONVERGED` only when both gates pass.
- **Initial Files:** `system.py`
- **Public Tests:** Valid task with verification and passport returns `'CONVERGED'`.
- **Hidden Tests:** Missing verification raises `RuntimeError`; missing passport raises `RuntimeError`.
- **Invariant:** `SYSTEM_LEVEL_CONVERGENCE_GATE`
