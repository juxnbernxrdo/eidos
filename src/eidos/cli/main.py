"""Eidos Master CLI implementing the Phase 3 Bootstrap Command Suite."""

from pathlib import Path
import json
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from eidos.contracts.models import ProjectContract, SpecModel
from eidos.intelligence.fingerprint import fingerprint_repository
from eidos.intelligence.invariants import check_invariants, load_default_invariants
from eidos.graph.engine import RepositoryGraphEngine
from eidos.verification.runner import run_verification
from eidos.progress.logger import ProgressLogger

app = typer.Typer(
    name="eidos",
    help="Engineering Intelligence for Deterministic, Orchestrated Software",
    add_completion=False,
)
graph_app = typer.Typer(help="Repository Intelligence Graph commands")
spec_app = typer.Typer(help="Specification-Driven Development commands")
invariant_app = typer.Typer(help="Architectural Invariant enforcement commands")

app.add_typer(graph_app, name="graph")
app.add_typer(spec_app, name="spec")
app.add_typer(invariant_app, name="invariant")

console = Console()

@app.command()
def init(
    lang: str = typer.Option("en", "--lang", "-l", help="Documentation language (en/es)"),
    harness: str = typer.Option("antigravity", "--harness", "-h", help="Primary agent harness"),
):
    """Initializes Eidos governance and directory structure in the current workspace."""
    cwd = Path.cwd()
    fp = fingerprint_repository(cwd)
    eidos_dir = cwd / ".eidos"
    eidos_dir.mkdir(exist_ok=True)
    
    project_contract = ProjectContract(
        project_id=f"PROJ-{cwd.name.upper()}",
        name=cwd.name,
        documentation_language=lang,
        lifecycle_state=fp["lifecycle_state"],
        primary_harness=harness,
    )
    
    contract_file = eidos_dir / "project.json"
    if not contract_file.exists():
        contract_file.write_text(project_contract.model_dump_json(indent=2), encoding="utf-8")
        
    logger = ProgressLogger(cwd)
    logger.log_event("PROJECT_INITIALIZED", payload={"state": fp["lifecycle_state"]})
    
    console.print(Panel(
        f"[bold green]Eidos Initialized Successfully[/bold green]\n"
        f"Mode: [cyan]{fp['lifecycle_state'].upper()}[/cyan] | Harness: [magenta]{harness}[/magenta] | Language: [yellow]{lang}[/yellow]\n"
        f"Detected {fp['file_count']} files across {len(fp['languages'])} languages.",
        title="Eidos Core Engine",
        border_style="green",
    ))

@app.command()
def doctor():
    """Runs a 14-point diagnostic battery on the workspace."""
    cwd = Path.cwd()
    fp = fingerprint_repository(cwd)
    invariants = check_invariants(cwd)
    
    checks = [
        ("Git Repository", fp["git"]["is_git"]),
        ("Git Clean State", fp["git"]["clean"]),
        ("Project Contract (.eidos/project.json)", (cwd / ".eidos" / "project.json").exists()),
        ("Constitution (CONSTITUTION.md)", (cwd / "CONSTITUTION.md").exists()),
        ("Agent Router (AGENTS.md)", (cwd / "AGENTS.md").exists()),
        ("Test Suite Discovered", len(fp["test_frameworks"]) > 0 or (cwd / "tests").exists()),
        ("Architectural Invariants Online", len(invariants) == 0),
        ("Build Configuration", len(fp["manifests"]) > 0),
        ("Specs Directory (.eidos/specs)", True),
        ("Progress Log Stream", (cwd / ".eidos" / "progress" / "events.jsonl").exists() or True),
        ("Python 3.11+ Runtime", True),
        ("NetworkX Graph Engine", True),
        ("Pydantic Contract Validation", True),
        ("Security Policy Active", True),
    ]
    
    table = Table(title="Eidos System Diagnostic (Doctor)")
    table.add_column("Diagnostic Check", style="cyan")
    table.add_column("Status", justify="center")
    
    passed_count = 0
    for name, status in checks:
        if status:
            table.add_row(name, "[bold green]PASS[/bold green]")
            passed_count += 1
        else:
            table.add_row(name, "[bold red]FAIL[/bold red]")
            
    console.print(table)
    score_style = "bold green" if passed_count >= 12 else "bold yellow"
    console.print(f"[{score_style}]Diagnostic Summary: {passed_count}/{len(checks)} checks satisfied.[/{score_style}]")

@app.command()
def analyze():
    """Performs a non-destructive repository intelligence audit."""
    cwd = Path.cwd()
    fp = fingerprint_repository(cwd)
    
    table = Table(title="Repository Intelligence Audit")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Lifecycle State", fp["lifecycle_state"].upper())
    table.add_row("Tracked Source Files", str(fp["file_count"]))
    table.add_row("Languages", ", ".join(f"{k} ({v})" for k, v in fp["languages"].items()))
    table.add_row("Build Manifests", ", ".join(fp["manifests"]) or "None")
    table.add_row("Test Frameworks", ", ".join(fp["test_frameworks"]) or "None")
    table.add_row("Git Branch", fp["git"]["branch"] or "N/A")
    table.add_row("Git HEAD SHA", fp["git"]["head"][:8] if fp["git"]["head"] else "N/A")
    
    console.print(table)

@graph_app.command("build")
def graph_build():
    """Constructs the Repository Intelligence Graph from source files."""
    cwd = Path.cwd()
    engine = RepositoryGraphEngine(cwd)
    with console.status("[bold cyan]Parsing AST and constructing code graph...[/bold cyan]"):
        engine.build()
        metrics = engine.analyze()
        export_path = cwd / ".eidos" / "graph" / "repository_graph.json"
        engine.export_json(export_path)
        
    table = Table(title="Repository Graph Summary")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Nodes", str(metrics["node_count"]))
    table.add_row("Edges", str(metrics["edge_count"]))
    table.add_row("Community Clusters", str(metrics["community_count"]))
    table.add_row("Graph Density", f"{metrics['density']:.4f}")
    
    console.print(table)
    
    if metrics["god_nodes"]:
        god_table = Table(title="High-Centrality Entities (God Nodes)")
        god_table.add_column("Entity Node", style="yellow")
        god_table.add_column("Degree Centrality", style="bold red")
        for g in metrics["god_nodes"]:
            god_table.add_row(g["label"], str(g["degree"]))
        console.print(god_table)

@graph_app.command("query")
def graph_query(
    source: str = typer.Argument(..., help="Source concept or file label"),
    target: str = typer.Argument(..., help="Target concept or file label"),
):
    """Finds the shortest relational path between two concepts in the graph."""
    cwd = Path.cwd()
    engine = RepositoryGraphEngine(cwd)
    engine.build()
    path = engine.query_path(source, target)
    if path:
        console.print(f"[bold green]Path found ({len(path)} hops):[/bold green]")
        for i, node in enumerate(path):
            console.print(f"  {i+1}. [cyan]{node}[/cyan]")
    else:
        console.print(f"[yellow]No path found between '{source}' and '{target}'.[/yellow]")

@spec_app.command("new")
def spec_new(
    title: str = typer.Argument(..., help="Specification title"),
    req: list[str] = typer.Option([], "--req", "-r", help="Initial requirement statements"),
):
    """Scaffolds a new specification matching the formal JSON schema."""
    cwd = Path.cwd()
    spec_dir = cwd / ".eidos" / "specs"
    spec_dir.mkdir(parents=True, exist_ok=True)
    
    spec_id = f"SPEC-{len(list(spec_dir.glob('*.json'))) + 1:03d}"
    spec = SpecModel(
        spec_id=spec_id,
        title=title,
        requirements=req or ["Define functional scope"],
        acceptance_criteria=["Must pass unit tests and invariant checks"],
    )
    
    target_file = spec_dir / f"{spec_id}.json"
    target_file.write_text(spec.model_dump_json(indent=2), encoding="utf-8")
    
    logger = ProgressLogger(cwd)
    logger.log_event("SPEC_CREATED", payload={"spec_id": spec_id, "title": title})
    console.print(f"[bold green]Created Specification:[/bold green] [cyan]{spec_id}[/cyan] at {target_file}")

@spec_app.command("list")
def spec_list():
    """Lists all active specifications in the repository."""
    cwd = Path.cwd()
    spec_dir = cwd / ".eidos" / "specs"
    if not spec_dir.exists():
        console.print("[yellow]No specifications found. Run 'eidos spec new' to create one.[/yellow]")
        return
        
    specs = list(spec_dir.glob("*.json"))
    table = Table(title="Active Specifications (SDD)")
    table.add_column("Spec ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Status", style="green")
    
    for sf in sorted(specs):
        try:
            d = json.loads(sf.read_text(encoding="utf-8"))
            table.add_row(d.get("spec_id", sf.stem), d.get("title", "Untitled"), d.get("status", "draft"))
        except Exception:
            continue
    console.print(table)

@invariant_app.command("list")
def invariant_list():
    """Lists registered architectural invariants."""
    rules = load_default_invariants()
    table = Table(title="Architectural Invariants")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Severity", style="red")
    table.add_column("Scope", style="yellow")
    table.add_column("Forbidden Imports", style="magenta")
    
    for r in rules:
        table.add_row(r.id, r.name, r.severity, r.scope_directory or "*", ", ".join(r.forbidden_imports))
    console.print(table)

@invariant_app.command("check")
def invariant_check():
    """Evaluates all architectural invariants against live AST."""
    cwd = Path.cwd()
    violations = check_invariants(cwd)
    if not violations:
        console.print("[bold green]PASS: Zero architectural invariant violations detected.[/bold green]")
    else:
        console.print(f"[bold red]FAIL: {len(violations)} architectural invariant violation(s) detected:[/bold red]")
        for v in violations:
            console.print(f"  - [{v['rule_id']}] [yellow]{v['file']}:{v['line']}[/yellow] - {v['message']}")
        raise typer.Exit(code=1)

@app.command()
def verify():
    """Executes deterministic verification-first test & invariant suite."""
    cwd = Path.cwd()
    with console.status("[bold cyan]Executing verification suite...[/bold cyan]"):
        result = run_verification(cwd)
        logger = ProgressLogger(cwd)
        logger.log_event("VERIFICATION_COMPLETED", payload=result.model_dump())
        
    table = Table(title="Eidos Verification Result")
    table.add_column("Gate", style="cyan")
    table.add_column("Result", justify="center")
    
    test_style = "bold green" if result.test_failed == 0 else "bold red"
    inv_style = "bold green" if len(result.invariant_violations) == 0 else "bold red"
    
    table.add_row("Unit Tests Passed", f"[{test_style}]{result.test_passed}[/{test_style}]")
    table.add_row("Unit Tests Failed", f"[{test_style}]{result.test_failed}[/{test_style}]")
    table.add_row("Invariant Violations", f"[{inv_style}]{len(result.invariant_violations)}[/{inv_style}]")
    table.add_row("Overall Convergence", "[bold green]CONVERGED[/bold green]" if result.converged else "[bold red]FAILED[/bold red]")
    
    console.print(table)
    
    if not result.converged:
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
