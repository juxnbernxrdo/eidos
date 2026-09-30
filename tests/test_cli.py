"""Integration tests for the Eidos Typer CLI."""

from typer.testing import CliRunner
from eidos.cli.main import app

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Engineering Intelligence for Deterministic, Orchestrated Software" in result.stdout

def test_cli_doctor():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Eidos System Diagnostic (Doctor)" in result.stdout
    assert "PASS" in result.stdout

def test_cli_analyze():
    result = runner.invoke(app, ["analyze"])
    assert result.exit_code == 0
    assert "Repository Intelligence Audit" in result.stdout
    assert "EXISTING" in result.stdout

def test_cli_invariants():
    result = runner.invoke(app, ["invariant", "list"])
    assert result.exit_code == 0
    assert "ARCH-001" in result.stdout

    result_check = runner.invoke(app, ["invariant", "check"])
    assert result_check.exit_code == 0
    assert "PASS: Zero architectural invariant violations detected" in result_check.stdout

def test_cli_graph_build():
    result = runner.invoke(app, ["graph", "build"])
    assert result.exit_code == 0
    assert "Repository Graph Summary" in result.stdout
    assert "Nodes" in result.stdout
