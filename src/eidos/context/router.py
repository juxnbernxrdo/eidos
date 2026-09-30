"""Minimal Sufficient Context (MSC) router and auditable budget assembler.

Implements SPEC-004 (Context Router & Minimal Sufficient Context) and satisfies
REQ-CTX-001, REQ-CTX-002, REQ-CTX-003, AC-004-01, AC-004-02, AC-004-03:
    - Topological pruning (target files as FULL_CODE, neighbors as SIGNATURE_ONLY)
    - Boundary contract pinning (CORE-CONTRACT-002 pinned at prompt boundary)
    - Full auditable selection rationale on every item
    - Strict token budgeting and quarantine of out-of-budget/adversarial items
"""

import ast
import uuid
from pathlib import Path
from typing import Any

from eidos.core.exceptions import InvalidInputError, PermissionDeniedError
from eidos.graph.engine import RepositoryGraphEngine
from eidos.security.permissions import canonicalize_and_confine_path


def estimate_tokens(text: str) -> int:
    """Deterministic token estimate for source code (~4 chars per token)."""
    if not text:
        return 0
    return max(1, len(text) // 4)


def extract_signatures(code: str) -> str:
    """Extracts function and class signatures from Python code for topological pruning."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # Fallback to comment representation
        return "# [Signatures unparseable due to syntax error]\n"

    signatures: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            signatures.append(f"class {node.name}:")
            for subnode in node.body:
                if isinstance(subnode, ast.FunctionDef):
                    args = [a.arg for a in subnode.args.args]
                    signatures.append(f"    def {subnode.name}({', '.join(args)}): ...")
        elif isinstance(node, ast.FunctionDef):
            args = [a.arg for a in node.args.args]
            signatures.append(f"def {node.name}({', '.join(args)}): ...")

    return "\n".join(signatures) if signatures else "# [No top-level class/function signatures found]\n"


class ContextRouter:
    """Assembles Minimal Sufficient Context payloads from task requirements and graph topology."""

    def __init__(self, workspace_root: Path, graph_engine: RepositoryGraphEngine | None = None):
        self.workspace_root = workspace_root.resolve()
        self.graph_engine = graph_engine or RepositoryGraphEngine(self.workspace_root)

    def assemble_context(self, routing_request: dict[str, Any]) -> dict[str, Any]:
        """Assembles MSC payload conforming strictly to CTX-CONTRACT-001."""
        req_id = routing_request.get("request_id", f"REQ-{uuid.uuid4().hex[:8].upper()}")
        task = routing_request.get("task")
        if not task:
            raise InvalidInputError("Routing request must specify 'task'")

        target_files = task.get("target_files", [])
        if not target_files:
            raise InvalidInputError("Task must specify at least one target file in target_files")

        budget_cfg = routing_request.get("budget_constraints", {})
        max_tokens = budget_cfg.get("max_tokens", 4000)
        reserve_tokens = budget_cfg.get("reserve_for_generation", 1000)
        k_hop_limit = budget_cfg.get("k_hop_limit", 2)

        available_budget = max_tokens - reserve_tokens
        if available_budget <= 0:
            raise InvalidInputError("max_tokens must exceed reserve_for_generation")

        sec_cfg = routing_request.get("security_constraints", {})
        project_id = sec_cfg.get("isolated_project_id", f"PROJ-{self.workspace_root.name.upper()}")

        assembled_items: list[dict[str, Any]] = []
        quarantined_exclusions: list[dict[str, Any]] = []
        consumed_tokens = 0
        order_idx = 1

        # Pinned boundary contracts (AC-004-01)
        pinned_contracts = ["CORE-CONTRACT-002"]

        # Ensure graph is ready
        if len(self.graph_engine.graph) == 0:
            self.graph_engine.build()

        # Process Target Files (Proximity 0 - FULL_CODE)
        for t_file in target_files:
            try:
                real_file = canonicalize_and_confine_path(t_file, self.workspace_root)
                if not real_file.exists():
                    quarantined_exclusions.append({
                        "item_id": t_file,
                        "exclusion_reason": "POISONED_FILE_FLAG",
                        "details": f"File '{t_file}' does not exist in workspace",
                    })
                    continue

                content = real_file.read_text(encoding="utf-8")
                tok_cnt = estimate_tokens(content)

                if consumed_tokens + tok_cnt <= available_budget:
                    assembled_items.append({
                        "item_id": f"ITEM-{order_idx:03d}",
                        "order_index": order_idx,
                        "source_domain": "FILE_AST",
                        "content_format": "FULL_CODE",
                        "content": content,
                        "token_count": tok_cnt,
                        "epistemic_provenance": "EXTRACTED",
                        "confidence": 1.0,
                        "selection_audit": {
                            "selection_reason": f"Direct task target file '{t_file}' (Proximity 0)",
                            "proximity_hops": 0,
                            "matched_query": t_file,
                        },
                    })
                    consumed_tokens += tok_cnt
                    order_idx += 1
                else:
                    quarantined_exclusions.append({
                        "item_id": t_file,
                        "exclusion_reason": "EXCEEDED_TOKEN_BUDGET",
                        "details": f"Target file '{t_file}' ({tok_cnt} tok) exceeds available budget ({available_budget - consumed_tokens} tok left)",
                    })
            except PermissionDeniedError as err:
                quarantined_exclusions.append({
                    "item_id": t_file,
                    "exclusion_reason": "CROSS_PROJECT_ISOLATION",
                    "details": str(err),
                })

        # Process Neighbor Nodes (Proximity 1 & 2 - SIGNATURE_ONLY)
        if k_hop_limit > 0:
            for t_file in target_files:
                file_node_id = f"file:{t_file}"
                subgraph = self.graph_engine.traverse_neighborhood(file_node_id, k_hops=k_hop_limit)
                for node_id in subgraph.nodes():
                    if node_id == file_node_id:
                        continue

                    # If neighbor is a file
                    node_data = self.graph_engine.graph.nodes[node_id]
                    if node_data.get("type") == "File":
                        n_path = node_data.get("file_path") or node_data.get("label")
                        if not n_path or n_path in target_files:
                            continue

                        try:
                            real_neighbor = canonicalize_and_confine_path(n_path, self.workspace_root)
                            if real_neighbor.exists():
                                raw_code = real_neighbor.read_text(encoding="utf-8")
                                pruned_content = extract_signatures(raw_code)
                                tok_cnt = estimate_tokens(pruned_content)

                                if consumed_tokens + tok_cnt <= available_budget:
                                    assembled_items.append({
                                        "item_id": f"ITEM-{order_idx:03d}",
                                        "order_index": order_idx,
                                        "source_domain": "FILE_AST",
                                        "content_format": "SIGNATURE_ONLY",
                                        "content": pruned_content,
                                        "token_count": tok_cnt,
                                        "epistemic_provenance": "EXTRACTED",
                                        "confidence": 1.0,
                                        "selection_audit": {
                                            "selection_reason": f"Topologically pruned 1-hop neighbor of '{t_file}'",
                                            "proximity_hops": 1,
                                            "matched_query": n_path,
                                        },
                                    })
                                    consumed_tokens += tok_cnt
                                    order_idx += 1
                                else:
                                    quarantined_exclusions.append({
                                        "item_id": n_path,
                                        "exclusion_reason": "EXCEEDED_TOKEN_BUDGET",
                                        "details": f"Neighbor '{n_path}' exceeds token budget",
                                    })
                        except Exception:
                            continue

        budget_exhausted = len(quarantined_exclusions) > 0 and any(
            q["exclusion_reason"] == "EXCEEDED_TOKEN_BUDGET" for q in quarantined_exclusions
        )
        escalation_required = len(assembled_items) == 0 and len(target_files) > 0

        routing_response = {
            "msc_id": f"MSC-{uuid.uuid4().hex[:8].upper()}",
            "request_id": req_id,
            "total_tokens": consumed_tokens,
            "budget_exhausted": budget_exhausted,
            "escalation_required": escalation_required,
            "pinned_boundary_contracts": pinned_contracts,
            "assembled_items": assembled_items,
            "quarantined_exclusions": quarantined_exclusions,
        }

        return {
            "contract_id": "CTX-CONTRACT-001",
            "contract_version": "1.0.0",
            "routing_request": routing_request,
            "routing_response": routing_response,
        }
