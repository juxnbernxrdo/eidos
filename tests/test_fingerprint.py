"""Unit tests for repository fingerprinting and AST parser."""

from pathlib import Path
from eidos.intelligence.fingerprint import fingerprint_repository, get_git_info
from eidos.intelligence.parser import parse_python_file

def test_fingerprint_repository():
    root = Path(__file__).parent.parent
    fp = fingerprint_repository(root)
    
    assert "workspace_root" in fp
    assert "file_count" in fp
    assert fp["file_count"] > 0
    assert "Python" in fp["languages"]
    assert "Python (pyproject/setup)" in fp["manifests"]
    assert fp["lifecycle_state"] == "existing"

def test_get_git_info():
    root = Path(__file__).parent.parent
    git_info = get_git_info(root)
    assert isinstance(git_info, dict)
    assert "is_git" in git_info

def test_parse_python_file():
    root = Path(__file__).parent.parent
    sample_file = root / "src" / "eidos" / "contracts" / "models.py"
    parsed = parse_python_file(sample_file, root)
    
    assert parsed is not None
    assert parsed["file_path"] == "src/eidos/contracts/models.py"
    assert len(parsed["classes"]) > 0
    class_names = [c["name"] for c in parsed["classes"]]
    assert "ProjectContract" in class_names
    assert "SpecModel" in class_names
