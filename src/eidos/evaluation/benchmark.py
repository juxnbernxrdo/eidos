"""Benchmark task suite definition for Eidos Phase 7 empirical evaluation."""

from typing import Dict, List
from eidos.evaluation.models import TaskDefinition, TaskDifficulty, TaskType


def get_benchmark_suite() -> Dict[str, TaskDefinition]:
    """Returns the standardized suite of 10 benchmark tasks for SWE agent evaluation."""
    tasks: Dict[str, TaskDefinition] = {}

    # Task 1: Bug Fix (Off-by-one / boundary condition) - SMALL
    tasks["TSK-EVAL-001"] = TaskDefinition(
        task_id="TSK-EVAL-001",
        title="Fix boundary condition in paginated window calculation",
        task_type=TaskType.BUG_FIX,
        difficulty=TaskDifficulty.SMALL,
        description="Fix the function `paginate_items` in `pagination.py`. Currently, requesting the last page with an exact multiple of page_size raises an IndexError instead of returning an empty or exact list.",
        initial_files={
            "pagination.py": (
                "def paginate_items(items, page, page_size):\n"
                "    start = (page - 1) * page_size\n"
                "    end = start + page_size\n"
                "    if start >= len(items):\n"
                "        raise IndexError('Page out of range')\n"
                "    return items[start:end]\n"
            )
        },
        ground_truth_patch={
            "pagination.py": (
                "def paginate_items(items, page, page_size):\n"
                "    if page < 1:\n"
                "        raise ValueError('Page must be >= 1')\n"
                "    start = (page - 1) * page_size\n"
                "    end = start + page_size\n"
                "    if start >= len(items) and len(items) > 0:\n"
                "        return []\n"
                "    return items[start:end]\n"
            )
        },
        public_tests=[
            "assert paginate_items([1, 2, 3, 4], 1, 2) == [1, 2]",
            "assert paginate_items([1, 2, 3, 4], 2, 2) == [3, 4]"
        ],
        hidden_tests=[
            "assert paginate_items([], 1, 10) == []",
            "assert paginate_items([1, 2, 3], 3, 2) == []"
        ],
        invariants=["PAGINATION_BOUNDS"],
        is_security_sensitive=False,
    )

    # Task 2: Feature Implementation (Validated Data Pipeline) - MEDIUM
    tasks["TSK-EVAL-002"] = TaskDefinition(
        task_id="TSK-EVAL-002",
        title="Implement schema-validated JSON event ingestion pipe",
        task_type=TaskType.FEATURE_IMPL,
        difficulty=TaskDifficulty.MEDIUM,
        description="Implement `EventIngester` in `ingester.py` with `ingest(record_str: str) -> dict`. Must reject malformed JSON, enforce required fields ('event_id', 'timestamp', 'source'), and reject timestamps in the future.",
        initial_files={
            "ingester.py": (
                "import json\n"
                "class EventIngester:\n"
                "    def ingest(self, record_str: str):\n"
                "        return json.loads(record_str)\n"
            )
        },
        ground_truth_patch={
            "ingester.py": (
                "import json, time\n"
                "class EventIngester:\n"
                "    REQUIRED = {'event_id', 'timestamp', 'source'}\n"
                "    def ingest(self, record_str: str):\n"
                "        try:\n"
                "            data = json.loads(record_str)\n"
                "        except Exception as e:\n"
                "            raise ValueError(f'Invalid JSON: {e}')\n"
                "        if not self.REQUIRED.issubset(data.keys()):\n"
                "            raise ValueError('Missing required fields')\n"
                "        if data['timestamp'] > time.time() + 300:\n"
                "            raise ValueError('Future timestamp')\n"
                "        return data\n"
            )
        },
        public_tests=[
            "ing = EventIngester(); res = ing.ingest('{\"event_id\":\"1\",\"timestamp\":1000,\"source\":\"cli\"}'); assert res['event_id'] == '1'"
        ],
        hidden_tests=[
            "ing = EventIngester(); import pytest; pytest.raises(ValueError, ing.ingest, 'not-json')",
            "ing = EventIngester(); import pytest; pytest.raises(ValueError, ing.ingest, '{\"event_id\":\"1\"}')",
            "ing = EventIngester(); import pytest, time; pytest.raises(ValueError, ing.ingest, f'{{\"event_id\":\"1\",\"timestamp\":{time.time()+99999},\"source\":\"cli\"}}')"
        ],
        invariants=["EVENT_INGEST_STRICT_SCHEMA"],
        is_security_sensitive=False,
    )

    # Task 3: Refactoring - MEDIUM
    tasks["TSK-EVAL-003"] = TaskDefinition(
        task_id="TSK-EVAL-003",
        title="Extract shared token counter without breaking public API",
        task_type=TaskType.REFACTORING,
        difficulty=TaskDifficulty.MEDIUM,
        description="Refactor `router.py` and `projector.py` to extract common token estimation logic into `counter.py:estimate_tokens(text: str) -> int`. Preserve backward compatibility for both callers.",
        initial_files={
            "router.py": "def count_tokens(s): return len(s) // 4\ndef route(text): return count_tokens(text) < 100\n",
            "projector.py": "def calc_cost(text): tokens = len(text) // 4; return tokens * 0.00001\n"
        },
        ground_truth_patch={
            "counter.py": "def estimate_tokens(text: str) -> int: return max(1, len(text) // 4)\n",
            "router.py": "from counter import estimate_tokens\ndef count_tokens(s): return estimate_tokens(s)\ndef route(text): return estimate_tokens(text) < 100\n",
            "projector.py": "from counter import estimate_tokens\ndef calc_cost(text): return estimate_tokens(text) * 0.00001\n"
        },
        public_tests=[
            "from router import route, count_tokens; assert route('hello world'); assert count_tokens('hello world') > 0",
            "from projector import calc_cost; assert calc_cost('hello world') > 0"
        ],
        hidden_tests=[
            "from counter import estimate_tokens; assert estimate_tokens('test') == 1",
            "from router import route; assert not route('x' * 500)"
        ],
        invariants=["DRY_CODE_COMPATIBILITY"],
        is_security_sensitive=False,
    )

    # Task 4: Security Fix - SMALL / HIGH SENSITIVITY
    tasks["TSK-EVAL-004"] = TaskDefinition(
        task_id="TSK-EVAL-004",
        title="Eliminate path traversal vulnerability in file reader",
        task_type=TaskType.SECURITY_FIX,
        difficulty=TaskDifficulty.SMALL,
        description="Fix `safe_read(root: str, path: str) -> str` in `reader.py`. Currently it does not verify that canonical realpath resides inside root, allowing `../../etc/passwd` escapes.",
        initial_files={
            "reader.py": (
                "import os\n"
                "def safe_read(root: str, path: str) -> str:\n"
                "    full = os.path.join(root, path)\n"
                "    with open(full, 'r') as f: return f.read()\n"
            )
        },
        ground_truth_patch={
            "reader.py": (
                "import os\n"
                "def safe_read(root: str, path: str) -> str:\n"
                "    canon_root = os.path.realpath(root)\n"
                "    canon_path = os.path.realpath(os.path.join(canon_root, path))\n"
                "    if not canon_path.startswith(canon_root + os.sep) and canon_path != canon_root:\n"
                "        raise PermissionError('Path escape rejected')\n"
                "    with open(canon_path, 'r') as f: return f.read()\n"
            )
        },
        public_tests=[
            "import tempfile, os; from reader import safe_read; d = tempfile.mkdtemp(); f = os.path.join(d, 't.txt'); open(f, 'w').write('ok'); assert safe_read(d, 't.txt') == 'ok'"
        ],
        hidden_tests=[
            "import tempfile, os, pytest; from reader import safe_read; d = tempfile.mkdtemp(); pytest.raises(PermissionError, safe_read, d, '../outside')"
        ],
        invariants=["SANDBOX_CONFINEMENT_REALPATH"],
        is_security_sensitive=True,
    )

    # Task 5: Multi-file Contract Repair - MEDIUM
    tasks["TSK-EVAL-005"] = TaskDefinition(
        task_id="TSK-EVAL-005",
        title="Synchronize schema rename across producer and consumer",
        task_type=TaskType.CONTRACT_REPAIR,
        difficulty=TaskDifficulty.MEDIUM,
        description="Field `agent_id` was renamed to `actor_id` in contract `schema.py`. Update producer `emitter.py` and consumer `handler.py` to match the new schema.",
        initial_files={
            "schema.py": "class Payload:\n    def __init__(self, actor_id: str, data: str):\n        self.actor_id = actor_id\n        self.data = data\n",
            "emitter.py": "from schema import Payload\ndef emit(): return Payload(agent_id='ag1', data='val')\n",
            "handler.py": "def process(p): return p.agent_id.upper()\n"
        },
        ground_truth_patch={
            "emitter.py": "from schema import Payload\ndef emit(): return Payload(actor_id='ag1', data='val')\n",
            "handler.py": "def process(p): return p.actor_id.upper()\n"
        },
        public_tests=[
            "from emitter import emit; from handler import process; p = emit(); assert process(p) == 'AG1'"
        ],
        hidden_tests=[
            "from schema import Payload; p = Payload(actor_id='foo', data='bar'); from handler import process; assert process(p) == 'FOO'"
        ],
        invariants=["CONTRACT_SCHEMA_SYNCHRONY"],
        is_security_sensitive=False,
    )

    # Task 6: Architectural Invariant Fix - MEDIUM
    tasks["TSK-EVAL-006"] = TaskDefinition(
        task_id="TSK-EVAL-006",
        title="Break illegal circular dependency between core and cli",
        task_type=TaskType.ARCH_INVARIANT_FIX,
        difficulty=TaskDifficulty.MEDIUM,
        description="In `core_engine.py`, an import of `cli_formatter.format_msg` violates `ARCH-001` (core must not import cli). Extract a message protocol into `protocol.py` to break the cycle.",
        initial_files={
            "cli_formatter.py": "def format_msg(msg: str): return f'[CLI] {msg}'\n",
            "core_engine.py": "import cli_formatter\ndef execute(msg: str): return cli_formatter.format_msg(msg)\n"
        },
        ground_truth_patch={
            "protocol.py": "def format_msg(msg: str): return f'[EIDOS] {msg}'\n",
            "cli_formatter.py": "from protocol import format_msg\n",
            "core_engine.py": "from protocol import format_msg\ndef execute(msg: str): return format_msg(msg)\n"
        },
        public_tests=[
            "from core_engine import execute; assert '[EIDOS]' in execute('test')"
        ],
        hidden_tests=[
            "import ast\ntree = ast.parse(open('core_engine.py').read())\nfor node in ast.walk(tree):\n    if isinstance(node, ast.Import):\n        assert not any('cli' in n.name for n in node.names)\n    if isinstance(node, ast.ImportFrom):\n        assert 'cli' not in (node.module or '')"
        ],
        invariants=["ARCH-001_CORE_ISOLATION"],
        is_security_sensitive=False,
    )

    # Task 7: Test Suite Repair - SMALL
    tasks["TSK-EVAL-007"] = TaskDefinition(
        task_id="TSK-EVAL-007",
        title="Repair brittle timing-dependent test oracle",
        task_type=TaskType.TEST_REPAIR,
        difficulty=TaskDifficulty.SMALL,
        description="Repair flaky test in `test_timer.py` that fails under load due to `assert duration == 0.1`. Use `math.isclose` with a 0.05 tolerance.",
        initial_files={
            "test_timer.py": (
                "import time\n"
                "def test_elapsed():\n"
                "    t0 = time.time()\n"
                "    time.sleep(0.05)\n"
                "    elapsed = time.time() - t0\n"
                "    assert elapsed == 0.05\n"
            )
        },
        ground_truth_patch={
            "test_timer.py": (
                "import time, math\n"
                "def test_elapsed():\n"
                "    t0 = time.time()\n"
                "    time.sleep(0.05)\n"
                "    elapsed = time.time() - t0\n"
                "    assert math.isclose(elapsed, 0.05, abs_tol=0.03)\n"
            )
        },
        public_tests=[
            "from test_timer import test_elapsed; test_elapsed()"
        ],
        hidden_tests=[
            "import ast\nsrc = open('test_timer.py').read()\nassert 'isclose' in src or 'abs(' in src"
        ],
        invariants=["DETERMINISTIC_TEST_ORACLE"],
        is_security_sensitive=False,
    )

    # Task 8: Cross-module Integration - LARGE
    tasks["TSK-EVAL-008"] = TaskDefinition(
        task_id="TSK-EVAL-008",
        title="Integrate event log append with state machine update",
        task_type=TaskType.CROSS_MODULE_INTEGRATION,
        difficulty=TaskDifficulty.LARGE,
        description="Wire `EventStream` in `stream.py` to notify `Aggregator` in `aggregator.py` on event append, ensuring monotonic state updates without duplicate processing.",
        initial_files={
            "stream.py": "class EventStream:\n    def __init__(self): self.events = []\n    def append(self, evt): self.events.append(evt)\n",
            "aggregator.py": "class Aggregator:\n    def __init__(self): self.count = 0\n    def on_event(self, evt): self.count += 1\n"
        },
        ground_truth_patch={
            "stream.py": (
                "class EventStream:\n"
                "    def __init__(self, listener=None):\n"
                "        self.events = []\n"
                "        self.listener = listener\n"
                "    def append(self, evt):\n"
                "        self.events.append(evt)\n"
                "        if self.listener:\n"
                "            self.listener.on_event(evt)\n"
            ),
            "aggregator.py": (
                "class Aggregator:\n"
                "    def __init__(self):\n"
                "        self.count = 0\n"
                "        self.processed = set()\n"
                "    def on_event(self, evt):\n"
                "        if evt.get('id') not in self.processed:\n"
                "            self.count += 1\n"
                "            self.processed.add(evt.get('id'))\n"
            )
        },
        public_tests=[
            "from stream import EventStream; from aggregator import Aggregator\na = Aggregator(); s = EventStream(listener=a); s.append({'id':'e1'}); assert a.count == 1"
        ],
        hidden_tests=[
            "from stream import EventStream; from aggregator import Aggregator\na = Aggregator(); s = EventStream(listener=a); s.append({'id':'e1'}); s.append({'id':'e1'}); assert a.count == 1",
            "from stream import EventStream; from aggregator import Aggregator\na = Aggregator(); s = EventStream(listener=a); s.append({'id':'e1'}); s.append({'id':'e2'}); assert a.count == 2"
        ],
        invariants=["IDEMPOTENT_EVENT_INTEGRATION"],
        is_security_sensitive=False,
    )

    # Task 9: Performance Optimization - MEDIUM
    tasks["TSK-EVAL-009"] = TaskDefinition(
        task_id="TSK-EVAL-009",
        title="Optimize O(N^2) node lookup with in-memory hash index",
        task_type=TaskType.PERF_OPTIMIZATION,
        difficulty=TaskDifficulty.MEDIUM,
        description="In `graph_lookup.py`, `find_by_type` performs a linear scan over all nodes. Replace with a dictionary mapping type to set of node IDs for O(1) retrieval.",
        initial_files={
            "graph_lookup.py": (
                "class FastGraph:\n"
                "    def __init__(self): self.nodes = []\n"
                "    def add_node(self, nid, ntype): self.nodes.append((nid, ntype))\n"
                "    def find_by_type(self, ntype):\n"
                "        return [nid for nid, t in self.nodes if t == ntype]\n"
            )
        },
        ground_truth_patch={
            "graph_lookup.py": (
                "from collections import defaultdict\n"
                "class FastGraph:\n"
                "    def __init__(self):\n"
                "        self.nodes = {}\n"
                "        self.index = defaultdict(list)\n"
                "    def add_node(self, nid, ntype):\n"
                "        self.nodes[nid] = ntype\n"
                "        self.index[ntype].append(nid)\n"
                "    def find_by_type(self, ntype):\n"
                "        return list(self.index.get(ntype, []))\n"
            )
        },
        public_tests=[
            "from graph_lookup import FastGraph; g = FastGraph(); g.add_node('n1', 'file'); assert g.find_by_type('file') == ['n1']"
        ],
        hidden_tests=[
            "from graph_lookup import FastGraph; g = FastGraph()\nfor i in range(1000): g.add_node(f'n{i}', 'fn')\nassert len(g.find_by_type('fn')) == 1000",
            "assert 'index' in open('graph_lookup.py').read() or 'dict' in open('graph_lookup.py').read()"
        ],
        invariants=["SUB_LINEAR_INDEX_EFFICIENCY"],
        is_security_sensitive=False,
    )

    # Task 10: Full End-to-End System Task - SYSTEM
    tasks["TSK-EVAL-010"] = TaskDefinition(
        task_id="TSK-EVAL-010",
        title="End-to-end task convergence with feature passport",
        task_type=TaskType.SYSTEM_INTEGRATION,
        difficulty=TaskDifficulty.SYSTEM,
        description="Implement `SystemRunner` in `system.py` that processes tasks, emits passport evidence, checks invariants, and only transitions to CONVERGED when all checks pass.",
        initial_files={
            "system.py": (
                "class SystemRunner:\n"
                "    def run(self, task): return 'CONVERGED'\n"
            )
        },
        ground_truth_patch={
            "system.py": (
                "class SystemRunner:\n"
                "    def run(self, task):\n"
                "        if not task.get('verified'):\n"
                "            raise RuntimeError('Cannot converge without verification')\n"
                "        if not task.get('passport'):\n"
                "            raise RuntimeError('Cannot converge without passport')\n"
                "        return 'CONVERGED'\n"
            )
        },
        public_tests=[
            "from system import SystemRunner; s = SystemRunner(); assert s.run({'verified': True, 'passport': {'id':'1'}}) == 'CONVERGED'"
        ],
        hidden_tests=[
            "from system import SystemRunner; s = SystemRunner(); import pytest; pytest.raises(RuntimeError, s.run, {'verified': False})",
            "from system import SystemRunner; s = SystemRunner(); import pytest; pytest.raises(RuntimeError, s.run, {'verified': True, 'passport': None})"
        ],
        invariants=["SYSTEM_LEVEL_CONVERGENCE_GATE"],
        is_security_sensitive=True,
    )

    return tasks
