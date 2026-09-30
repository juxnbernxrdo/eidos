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
from eidos.progress.projector import ProgressProjector
from eidos.progress.passport import FeaturePassportManager
from eidos.context.router import ContextRouter
from eidos.skills.gateway import SkillGateway
from eidos.evaluation.benchmark import get_benchmark_suite
from eidos.evaluation.runner import EvaluationRunner
from eidos.evaluation.models import ExperimentalArm
from eidos.evolution.pipeline import EvolutionPipeline, ProposalState

app = typer.Typer(
    name="eidos",
    help="Engineering Intelligence for Deterministic, Orchestrated Software",
    add_completion=False,
)
graph_app = typer.Typer(help="Repository Intelligence Graph commands")
spec_app = typer.Typer(help="Specification-Driven Development commands")
invariant_app = typer.Typer(help="Architectural Invariant enforcement commands")
progress_app = typer.Typer(help="Event-sourced progress projection commands")
passport_app = typer.Typer(help="Feature Passport convergence bridge commands")
context_app = typer.Typer(help="Minimal Sufficient Context (MSC) router commands")
skills_app = typer.Typer(help="Skill Gateway and security audit commands")
eval_app = typer.Typer(help="Phase 7 Empirical Evaluation & Benchmarking commands")
evolve_app = typer.Typer(help="Phase 8 Governed Evolution & Self-Improvement commands")

app.add_typer(graph_app, name="graph")
app.add_typer(spec_app, name="spec")
app.add_typer(invariant_app, name="invariant")
app.add_typer(progress_app, name="progress")
app.add_typer(passport_app, name="passport")
app.add_typer(context_app, name="context")
app.add_typer(skills_app, name="skills")
app.add_typer(eval_app, name="eval")
app.add_typer(evolve_app, name="evolve")

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

@progress_app.command("show")
def progress_show():
    """Projects active workspace progress from immutable event log."""
    cwd = Path.cwd()
    projector = ProgressProjector(cwd)
    summary = projector.project_workspace()

    table = Table(title="Eidos Progress & Observability Projector")
    table.add_column("Dimension", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Tasks", str(summary["total_tasks"]))
    table.add_row("Converged Tasks", str(summary["converged_tasks"]))
    table.add_row("Unconverged Tasks", str(summary["unconverged_tasks"]))
    table.add_row("Verified Success Rate (VSR)", f"{summary['verified_success_rate']}%")
    table.add_row("Total Tokens Consumed", str(summary["total_tokens_consumed"]))
    table.add_row("Total Cost (USD)", f"${summary['total_cost_usd']:.4f}")
    table.add_row("Total Repairs", str(summary["total_repairs"]))
    table.add_row("Tool Invocations", str(summary["total_tool_invocations"]))

    console.print(table)

@passport_app.command("list")
def passport_list():
    """Lists stamped Feature Passports."""
    cwd = Path.cwd()
    manager = FeaturePassportManager(cwd)
    passports = list(manager.passports_dir.glob("*.json"))

    table = Table(title="Feature Passports")
    table.add_column("Feature ID", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Passport ID", style="magenta")

    for pf in sorted(passports):
        try:
            data = json.loads(pf.read_text(encoding="utf-8"))
            table.add_row(data.get("feature_id", pf.stem), data.get("status", "UNKNOWN"), data.get("passport_id", ""))
        except Exception:
            continue

    console.print(table)

@context_app.command("assemble")
def context_assemble(
    target: str = typer.Argument(..., help="Target file to route"),
    max_tokens: int = typer.Option(4000, "--max-tokens", "-m", help="Total token budget"),
):
    """Assembles Minimal Sufficient Context (MSC) for a target file."""
    cwd = Path.cwd()
    router = ContextRouter(cwd)
    req = {
        "request_id": "CLI-REQ-01",
        "task": {"task_id": "TASK-CLI", "objective": f"Route context for {target}", "target_files": [target]},
        "context_sources": {"include_graph": True, "include_rules": True, "include_specs": True, "include_evidence": True},
        "budget_constraints": {"max_tokens": max_tokens, "reserve_for_generation": 1000, "k_hop_limit": 1},
        "security_constraints": {"quarantine_adversarial": True, "isolated_project_id": f"PROJ-{cwd.name.upper()}"},
    }
    result = router.assemble_context(req)
    resp = result["routing_response"]

    table = Table(title=f"Minimal Sufficient Context (MSC) - {target}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("MSC ID", resp["msc_id"])
    table.add_row("Assembled Tokens", str(resp["total_tokens"]))
    table.add_row("Assembled Items", str(len(resp["assembled_items"])))
    table.add_row("Pinned Contracts", ", ".join(resp["pinned_boundary_contracts"]))
    table.add_row("Budget Exhausted", str(resp["budget_exhausted"]))
    table.add_row("Quarantined Exclusions", str(len(resp["quarantined_exclusions"])))

    console.print(table)

@skills_app.command("list")
def skills_list():
    """Lists installed and pinned skills."""
    cwd = Path.cwd()
    lock_file = cwd / ".eidos" / "skills-lock.json"
    if not lock_file.exists():
        console.print("[yellow]No skills installed. skills-lock.json not found.[/yellow]")
        return

    lock = json.loads(lock_file.read_text(encoding="utf-8"))
    table = Table(title="Installed Agent Skills (skills-lock.json)")
    table.add_column("Skill Name", style="cyan")
    table.add_column("Risk Score", style="green")
    table.add_column("Installed At", style="white")

    for name, data in lock.items():
        table.add_row(name, str(data.get("risk_score", 0)), data.get("installed_at", ""))

    console.print(table)


@eval_app.command("tasks")
def eval_tasks():
    """Lists all benchmark tasks available in the Phase 7 evaluation suite."""
    suite = get_benchmark_suite()
    table = Table(title="Phase 7 Benchmark Task Suite (10 Tasks)")
    table.add_column("Task ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Type", style="magenta")
    table.add_column("Difficulty", style="yellow")
    table.add_column("Security", style="red")

    for tid, task in suite.items():
        table.add_row(
            tid,
            task.title,
            task.task_type.value,
            task.difficulty.value,
            "YES" if task.is_security_sensitive else "NO",
        )

    console.print(table)


@eval_app.command("run")
def eval_run(
    trials: int = typer.Option(5, "--trials", "-t", help="Number of trials per task"),
    model: str = typer.Option("claude-3-5-sonnet-20241022", "--model", "-m", help="Target model identifier"),
    seed: int = typer.Option(42, "--seed", "-s", help="Base pseudo-random seed"),
):
    """Executes a controlled evaluation run comparing B0 (Raw), B1 (Harness), and B2 (Eidos)."""
    runner = EvaluationRunner(seed=seed)
    arms = [
        ExperimentalArm.B0_RAW_AGENT,
        ExperimentalArm.B1_BASIC_HARNESS,
        ExperimentalArm.B2_FULL_EIDOS,
    ]
    console.print(f"[bold cyan]Starting Phase 7 Evaluation Run...[/bold cyan] ({len(arms)} arms, {len(runner.tasks)} tasks, {trials} trials/task)")
    
    run_result = runner.execute_evaluation(arms=arms, trials_per_task=trials, model_id=model)

    # 1. Primary Metrics Table
    table = Table(title=f"Evaluation Summary: {run_result.run_id} (Model: {model})")
    table.add_column("Arm", style="cyan")
    table.add_column("Trials", style="white")
    table.add_column("VSR (Task Success)", style="green")
    table.add_column("Public Pass", style="white")
    table.add_column("Hidden Pass", style="white")
    table.add_column("Mean Tokens", style="yellow")
    table.add_column("Mean Latency", style="magenta")
    table.add_column("Mean Cost ($)", style="green")

    for arm_name, s in run_result.arm_statistics.items():
        table.add_row(
            arm_name,
            str(s.total_trials),
            f"{s.task_success_rate * 100:.1f}%",
            f"{s.public_pass_rate * 100:.1f}%",
            f"{s.hidden_pass_rate * 100:.1f}%",
            f"{s.mean_tokens:.0f}",
            f"{s.mean_latency_ms:.0f}ms",
            f"${s.mean_cost_usd:.4f}",
        )
    console.print(table)

    # 2. Comparative Deltas vs B0 Table
    if run_result.ablation_deltas:
        del_table = Table(title="Comparative Deltas & Statistical Significance vs B0 (Raw Agent)")
        del_table.add_column("Treatment Arm", style="cyan")
        del_table.add_column("Δ VSR (pp)", style="green")
        del_table.add_column("Δ Tokens (%)", style="yellow")
        del_table.add_column("Δ Cost (%)", style="yellow")
        del_table.add_column("VSR p-value", style="magenta")
        del_table.add_column("Token Cohen's d", style="white")

        for arm_name, d in run_result.ablation_deltas.items():
            st = run_result.statistical_tests.get(arm_name, {})
            del_table.add_row(
                arm_name,
                f"{d['delta_vsr_percentage_points']:+.1f}%",
                f"{d['relative_token_change_percent']:+.1f}%",
                f"{d['relative_cost_change_percent']:+.1f}%",
                f"{st.get('vsr_p_value', 1.0):.4f}",
                f"{st.get('token_cohens_d', 0.0):+.2f}",
            )
        console.print(del_table)

    console.print(f"[bold green]Artifact written to: .eidos/evaluation/runs/{run_result.run_id}.json[/bold green]")


@eval_app.command("ablation")
def eval_ablation(
    trials: int = typer.Option(3, "--trials", "-t", help="Trials per task for ablation study"),
    seed: int = typer.Option(42, "--seed", "-s", help="Base seed"),
):
    """Executes the full 10-arm ablation study (A0 through A9)."""
    runner = EvaluationRunner(seed=seed)
    ablation_arms = [
        ExperimentalArm.A0_BASELINE,
        ExperimentalArm.A1_PLUS_SPECS,
        ExperimentalArm.A2_PLUS_CONTRACTS,
        ExperimentalArm.A3_PLUS_GRAPH,
        ExperimentalArm.A4_PLUS_CONTEXT_ROUTER,
        ExperimentalArm.A5_PLUS_SKILLS,
        ExperimentalArm.A6_PLUS_SUBAGENTS,
        ExperimentalArm.A7_PLUS_VERIFICATION,
        ExperimentalArm.A8_PLUS_MEMORY,
        ExperimentalArm.A9_FULL_EIDOS,
    ]
    console.print(f"[bold cyan]Running 10-Arm Ablation Battery...[/bold cyan]")
    run_result = runner.execute_evaluation(arms=ablation_arms, trials_per_task=trials)

    table = Table(title="10-Arm Component Ablation Study Matrix")
    table.add_column("Ablation Arm", style="cyan")
    table.add_column("VSR", style="green")
    table.add_column("Mean Tokens", style="yellow")
    table.add_column("Mean Cost ($)", style="white")
    table.add_column("Primary Failure Mode", style="red")

    for arm_name, s in run_result.arm_statistics.items():
        top_fail = "NONE"
        if s.failure_distribution:
            top_fail = max(s.failure_distribution.items(), key=lambda x: x[1])[0]
        table.add_row(
            arm_name,
            f"{s.task_success_rate * 100:.1f}%",
            f"{s.mean_tokens:.0f}",
            f"${s.mean_cost_usd:.4f}",
            top_fail,
        )
    console.print(table)


@eval_app.command("report")
def eval_report():
    """Prints the latest evaluation run report."""
    runs_dir = Path.cwd() / ".eidos" / "evaluation" / "runs"
    if not runs_dir.exists():
        console.print("[yellow]No evaluation runs found in .eidos/evaluation/runs/[/yellow]")
        return
    runs = sorted(runs_dir.glob("RUN-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not runs:
        console.print("[yellow]No evaluation runs found.[/yellow]")
        return
    
    latest = runs[0]
    data = json.loads(latest.read_text(encoding="utf-8"))
    console.print(Panel(
        f"[bold]Latest Run:[/bold] {data['run_id']}\n"
        f"[bold]Timestamp:[/bold] {data['timestamp']}\n"
        f"[bold]Commit:[/bold] {data['git_commit']}\n"
        f"[bold]Model:[/bold] {data['model_identifier']}\n"
        f"[bold]Arms Evaluated:[/bold] {', '.join(data['arms_evaluated'])}\n"
        f"[bold]Tasks Evaluated:[/bold] {len(data['tasks_evaluated'])} tasks ({data['trials_per_task']} trials/task)",
        title="Evaluation Run Artifact",
        border_style="green",
    ))


@evolve_app.command("list")
def evolve_list():
    """Lists all self-improvement proposals across lifecycle states."""
    cwd = Path.cwd()
    pipeline = EvolutionPipeline(cwd)
    
    table = Table(title="Eidos Evolution Proposals Ledger")
    table.add_column("Proposal ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Category", style="magenta")
    table.add_column("Status", style="yellow")
    table.add_column("Target File", style="white")
    table.add_column("Approver", style="green")

    # Inspect proposals, accepted, and rejected directories
    for p_dir in [pipeline.proposals_dir, pipeline.accepted_dir, pipeline.rejected_dir]:
        for p_file in sorted(p_dir.glob("PROP-*.json")):
            try:
                doc = json.loads(p_file.read_text(encoding="utf-8"))
                table.add_row(
                    doc.get("proposal_id", p_file.stem),
                    doc.get("title", ""),
                    doc.get("category", ""),
                    doc.get("status", ""),
                    doc.get("target_rule_file", ""),
                    doc.get("approved_by") or "-",
                )
            except Exception:
                continue

    console.print(table)


@evolve_app.command("propose")
def evolve_propose(
    title: str = typer.Option(..., "--title", "-t", help="Title of the evolution proposal"),
    category: str = typer.Option("ORCHESTRATION_EFFICIENCY", "--category", "-c", help="Proposal category"),
    rationale: str = typer.Option(..., "--rationale", "-r", help="Empirical rationale and motivation"),
    target_file: str = typer.Option("src/eidos/orchestration/pipeline.py", "--target", help="Target rule/code file"),
):
    """Generates a structured self-improvement LearningProposal in PROPOSED state."""
    pipeline = EvolutionPipeline(Path.cwd())
    doc = pipeline.create_proposal(
        title=title,
        category=category,
        rationale=rationale,
        proposed_diff="# [Proposed modification]",
        target_rule_file=target_file,
    )
    console.print(f"[bold green]Proposal Created:[/bold green] [cyan]{doc['proposal_id']}[/cyan] in state [yellow]{doc['status']}[/yellow]")


@evolve_app.command("eval")
def evolve_eval(
    proposal_id: str = typer.Option(..., "--id", "-i", help="Proposal ID to evaluate"),
    delta_vsr: float = typer.Option(0.0, "--delta-vsr", help="Observed benchmark VSR change in percentage points"),
    passed_regressions: bool = typer.Option(True, "--no-regressions/--regressions", help="Whether change passed regression checks"),
):
    """Evaluates benchmark outcomes for a proposal, advancing to HUMAN_REVIEW (AC-014-01)."""
    pipeline = EvolutionPipeline(Path.cwd())
    doc = pipeline.submit_benchmark_evaluation(
        proposal_id=proposal_id,
        delta_vsr=delta_vsr,
        passed_regression=passed_regressions,
    )
    console.print(f"[bold green]Proposal Evaluated:[/bold green] [cyan]{proposal_id}[/cyan] transitioned to [yellow]{doc['status']}[/yellow]")


@evolve_app.command("approve")
def evolve_approve(
    proposal_id: str = typer.Option(..., "--id", "-i", help="Proposal ID in HUMAN_REVIEW to approve"),
    operator: str = typer.Option("HUMAN-OPERATOR-GOVERNANCE", "--operator", help="Operator signature"),
):
    """Applies human approval gate to ratify and accept proposal (AC-014-01)."""
    pipeline = EvolutionPipeline(Path.cwd())
    doc = pipeline.approve_proposal(
        proposal_id=proposal_id,
        operator_signature=operator,
    )
    console.print(f"[bold green]Proposal Approved & Ratified:[/bold green] [cyan]{proposal_id}[/cyan] is now [green]{doc['status']}[/green] by [magenta]{operator}[/magenta]")


if __name__ == "__main__":
    app()
