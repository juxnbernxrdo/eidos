"""Deterministic AST parser extracting entities, imports, and references."""

import ast
from pathlib import Path
from typing import Any

class EntityExtractor(ast.NodeVisitor):
    def __init__(self, relative_path: str):
        self.relative_path = relative_path
        self.classes: list[dict[str, Any]] = []
        self.functions: list[dict[str, Any]] = []
        self.imports: list[dict[str, Any]] = []
        self.calls: list[dict[str, Any]] = []

    def visit_ClassDef(self, node: ast.ClassDef):
        methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        docstring = ast.get_docstring(node) or ""
        self.classes.append({
            "name": node.name,
            "line_range": (node.lineno, getattr(node, "end_lineno", node.lineno)),
            "methods": methods,
            "docstring": docstring[:100],
        })
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        docstring = ast.get_docstring(node) or ""
        self.functions.append({
            "name": node.name,
            "line_range": (node.lineno, getattr(node, "end_lineno", node.lineno)),
            "args": [arg.arg for arg in node.args.args],
            "docstring": docstring[:100],
        })
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)  # type: ignore

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append({
                "module": alias.name,
                "alias": alias.asname,
                "line": node.lineno,
            })
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""
        for alias in node.names:
            self.imports.append({
                "module": f"{module}.{alias.name}" if module else alias.name,
                "alias": alias.asname,
                "line": node.lineno,
            })
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            self.calls.append({"target": node.func.id, "line": node.lineno})
        elif isinstance(node.func, ast.Attribute):
            self.calls.append({"target": node.func.attr, "line": node.lineno})
        self.generic_visit(node)

def parse_python_file(file_path: Path, workspace_root: Path) -> dict[str, Any] | None:
    """Parses a single Python file and returns its structural entities."""
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
        rel_path = str(file_path.relative_to(workspace_root))
        extractor = EntityExtractor(rel_path)
        extractor.visit(tree)
        
        return {
            "file_path": rel_path,
            "classes": extractor.classes,
            "functions": extractor.functions,
            "imports": extractor.imports,
            "calls": extractor.calls,
            "line_count": len(content.splitlines()),
        }
    except Exception:
        return None
