"""Non-destructive repository fingerprinting and state detection."""

from pathlib import Path
import subprocess
from typing import Any

def get_git_info(workspace_root: Path) -> dict[str, Any]:
    """Extracts Git HEAD, branch, and status non-destructively."""
    git_dir = workspace_root / ".git"
    if not git_dir.exists():
        return {"is_git": False, "head": None, "branch": None, "clean": True}
    
    try:
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=workspace_root, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        head = "UNCOMMITTED"
        
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=workspace_root, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        branch = "unknown"
        
    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=workspace_root, stderr=subprocess.DEVNULL
        ).decode().strip()
        is_clean = len(status) == 0
    except Exception:
        is_clean = False
        
    return {"is_git": True, "head": head, "branch": branch, "clean": is_clean}

def fingerprint_repository(workspace_root: Path) -> dict[str, Any]:
    """Analyzes workspace non-destructively to identify languages, tools, and lifecycle state."""
    files = list(workspace_root.rglob("*"))
    file_count = len([f for f in files if f.is_file() and not any(p.startswith(".") for p in f.parts)])
    
    languages: dict[str, int] = {}
    ext_map = {
        ".py": "Python",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".rs": "Rust",
        ".go": "Go",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".md": "Markdown",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
    }
    
    for f in files:
        if f.is_file() and not any(part.startswith((".", "node_modules", "venv", "__pycache__")) for part in f.parts):
            suffix = f.suffix.lower()
            if suffix in ext_map:
                lang = ext_map[suffix]
                languages[lang] = languages.get(lang, 0) + 1
                
    # Detect build manifests
    manifests = []
    if (workspace_root / "pyproject.toml").exists() or (workspace_root / "setup.py").exists():
        manifests.append("Python (pyproject/setup)")
    if (workspace_root / "package.json").exists():
        manifests.append("Node.js (package.json)")
    if (workspace_root / "Cargo.toml").exists():
        manifests.append("Rust (Cargo.toml)")
    if (workspace_root / "go.mod").exists():
        manifests.append("Go (go.mod)")
        
    # Detect test runners
    test_frameworks = []
    if (workspace_root / "pytest.ini").exists() or any("test_" in f.name for f in files):
        test_frameworks.append("pytest")
    if (workspace_root / "jest.config.js").exists() or (workspace_root / "vitest.config.ts").exists():
        test_frameworks.append("jest/vitest")
        
    git_info = get_git_info(workspace_root)
    
    # Greenfield determination: <= 3 non-hidden files and no src/lib
    is_greenfield = file_count <= 3 and not (workspace_root / "src").exists()
    
    return {
        "workspace_root": str(workspace_root.resolve()),
        "lifecycle_state": "greenfield" if is_greenfield else "existing",
        "file_count": file_count,
        "languages": languages,
        "manifests": manifests,
        "test_frameworks": test_frameworks,
        "git": git_info,
    }
