"""Repository Intelligence Graph engine utilizing NetworkX.

Implements SPEC-005 (Storage-Agnostic Repository Graph Engine) and satisfies
REQ-GRAPH-001, REQ-GRAPH-002, REQ-GRAPH-003, AC-005-01, AC-005-02, AC-005-03.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import networkx as nx
from eidos.contracts.models import NodeType, EdgeRelation, EpistemicType
from eidos.intelligence.fingerprint import get_git_info
from eidos.intelligence.parser import parse_python_file


class RepositoryGraphEngine:
    """Storage-agnostic heterogeneous graph engine preserving epistemic provenance."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.graph = nx.DiGraph()
        self.freshness: str = "STALE"
        self.last_git_commit: str = "HEAD"

    def build(self) -> nx.DiGraph:
        """Parses all Python source files and builds the directed code intelligence graph."""
        self.graph.clear()
        git_info = get_git_info(self.workspace_root)
        self.last_git_commit = git_info.get("head") or "HEAD"

        py_files = [
            f for f in self.workspace_root.rglob("*.py")
            if not any(p.startswith((".", "venv", "__pycache__", ".venv")) for p in f.parts)
        ]

        for f in py_files:
            parsed = parse_python_file(f, self.workspace_root)
            if not parsed:
                continue

            file_node_id = f"file:{parsed['file_path']}"
            self.graph.add_node(
                file_node_id,
                type=NodeType.FILE.value,
                label=parsed["file_path"],
                file_path=parsed["file_path"],
                line_count=parsed["line_count"],
            )

            # Classes
            for cls in parsed["classes"]:
                cls_id = f"class:{parsed['file_path']}#{cls['name']}"
                self.graph.add_node(
                    cls_id,
                    type=NodeType.CLASS.value,
                    label=cls["name"],
                    file_path=parsed["file_path"],
                    line_range=cls["line_range"],
                )
                self.graph.add_edge(
                    file_node_id,
                    cls_id,
                    relation=EdgeRelation.DEFINED_BY.value,
                    epistemic_provenance=EpistemicType.EXTRACTED.value,
                    confidence=1.0,
                )

            # Functions
            for fn in parsed["functions"]:
                fn_id = f"fn:{parsed['file_path']}#{fn['name']}"
                self.graph.add_node(
                    fn_id,
                    type=NodeType.FUNCTION.value,
                    label=fn["name"],
                    file_path=parsed["file_path"],
                    line_range=fn["line_range"],
                )
                self.graph.add_edge(
                    file_node_id,
                    fn_id,
                    relation=EdgeRelation.DEFINED_BY.value,
                    epistemic_provenance=EpistemicType.EXTRACTED.value,
                    confidence=1.0,
                )

            # Imports / Dependencies
            for imp in parsed["imports"]:
                mod = imp["module"]
                imp_id = f"dep:{mod}"
                if not self.graph.has_node(imp_id):
                    self.graph.add_node(imp_id, type=NodeType.DEPENDENCY.value, label=mod)
                self.graph.add_edge(
                    file_node_id,
                    imp_id,
                    relation=EdgeRelation.DEPENDS_ON.value,
                    epistemic_provenance=EpistemicType.EXTRACTED.value,
                    confidence=1.0,
                )

        self.freshness = "FRESH"
        return self.graph

    def propose_edge(
        self,
        source: str,
        target: str,
        relation: str,
        epistemic_provenance: str = EpistemicType.INFERRED.value,
        confidence: float = 0.7,
        evidence_ref: str | None = None,
    ) -> dict[str, Any]:
        """Proposes an inferred edge. If it contradicts an EXTRACTED ground-truth fact,

        it is quarantined as CONFLICTS_WITH per AC-005-02 and INV-009.
        """
        # Ensure nodes exist
        if not self.graph.has_node(source):
            self.graph.add_node(source, type=NodeType.FINDING.value, label=source)
        if not self.graph.has_node(target):
            self.graph.add_node(target, type=NodeType.FINDING.value, label=target)

        # Check for conflict with existing EXTRACTED edges
        has_extracted_conflict = False
        if relation == EdgeRelation.DEFINED_BY.value:
            # Check if target already has an EXTRACTED DEFINED_BY from another source
            for u, v, d in self.graph.in_edges(target, data=True):
                if d.get("relation") == EdgeRelation.DEFINED_BY.value and d.get("epistemic_provenance") == EpistemicType.EXTRACTED.value and u != source:
                    has_extracted_conflict = True
                    break

        if has_extracted_conflict:
            # AC-005-02: Quarantine as CONFLICTS_WITH and preserve EXTRACTED ground truth
            self.graph.add_edge(
                source,
                target,
                relation=EdgeRelation.CONFLICTS_WITH.value,
                epistemic_provenance=epistemic_provenance,
                confidence=confidence,
                evidence_ref=evidence_ref or "conflicting-inference-quarantined",
            )
            return {
                "status": "QUARANTINED",
                "relation": EdgeRelation.CONFLICTS_WITH.value,
                "reason": "Conflicts with verified EXTRACTED ground truth edge",
            }

        # Otherwise add proposed edge normally
        self.graph.add_edge(
            source,
            target,
            relation=relation,
            epistemic_provenance=epistemic_provenance,
            confidence=confidence,
            evidence_ref=evidence_ref or "",
        )
        return {"status": "ACCEPTED", "relation": relation}

    def traverse_neighborhood(self, seed_node_id: str, k_hops: int = 2) -> nx.DiGraph:
        """Computes the directed ego-subgraph strictly bounded by k_hops (AC-005-03)."""
        if not self.graph.has_node(seed_node_id):
            return nx.DiGraph()

        # Perform BFS bounded by k_hops
        visited = {seed_node_id: 0}
        queue = [(seed_node_id, 0)]

        while queue:
            current, dist = queue.pop(0)
            if dist < k_hops:
                for successor in self.graph.successors(current):
                    if successor not in visited or visited[successor] > dist + 1:
                        visited[successor] = dist + 1
                        queue.append((successor, dist + 1))

        # Build induced subgraph strictly over reachable nodes
        return self.graph.subgraph(visited.keys()).copy()

    def analyze(self) -> dict[str, Any]:
        """Computes god nodes, centrality, and architectural metrics."""
        if len(self.graph) == 0:
            self.build()

        degrees = dict(self.graph.degree())
        sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        god_nodes = [
            {"node_id": node, "degree": deg, "label": self.graph.nodes[node].get("label", node)}
            for node, deg in sorted_degrees[:5]
        ]

        communities: dict[str, list[str]] = {}
        for node in self.graph.nodes():
            label = self.graph.nodes[node].get("label", "")
            root_domain = label.split("/")[0] if "/" in label else label.split(".")[0]
            communities.setdefault(root_domain, []).append(node)

        return {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "god_nodes": god_nodes,
            "community_count": len(communities),
            "density": nx.density(self.graph) if len(self.graph) > 1 else 0.0,
            "freshness": self.freshness,
        }

    def query_path(self, source_label: str, target_label: str) -> list[str]:
        """Finds the shortest directed path between two concepts."""
        src = next((n for n, d in self.graph.nodes(data=True) if source_label in d.get("label", "")), None)
        tgt = next((n for n, d in self.graph.nodes(data=True) if target_label in d.get("label", "")), None)
        if not src or not tgt:
            return []
        try:
            return nx.shortest_path(self.graph, source=src, target=tgt)
        except nx.NetworkXNoPath:
            return []

    def export_snapshot(self, target_path: Path | None = None) -> dict[str, Any]:
        """Exports graph snapshot conforming to GRAPH-CONTRACT-001 schema."""
        if len(self.graph) == 0:
            self.build()

        snapshot_doc = {
            "contract_id": "GRAPH-CONTRACT-001",
            "contract_version": "1.0.0",
            "snapshot": {
                "snapshot_id": f"SNAP-{uuid.uuid4().hex[:8].upper()}",
                "project_id": f"PROJ-{self.workspace_root.name.upper()}",
                "git_commit": self.last_git_commit,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "graph_freshness": self.freshness,
                "node_count": self.graph.number_of_nodes(),
                "edge_count": self.graph.number_of_edges(),
                "nodes": [
                    {
                        "id": n,
                        "type": d.get("type", NodeType.FILE.value),
                        "label": d.get("label", n),
                        "file_path": d.get("file_path"),
                        "line_range": d.get("line_range"),
                    }
                    for n, d in self.graph.nodes(data=True)
                ],
                "edges": [
                    {
                        "source": u,
                        "target": v,
                        "relation": d.get("relation", EdgeRelation.DEPENDS_ON.value),
                        "epistemic_provenance": d.get("epistemic_provenance", EpistemicType.EXTRACTED.value),
                        "confidence": float(d.get("confidence", 1.0)),
                        "evidence_ref": d.get("evidence_ref"),
                    }
                    for u, v, d in self.graph.edges(data=True)
                ],
            },
        }

        if target_path:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(json.dumps(snapshot_doc, indent=2), encoding="utf-8")

        return snapshot_doc

    def export_json(self, target_path: Path):
        """Backward-compatible JSON export."""
        self.export_snapshot(target_path)
