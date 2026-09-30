# EIDOS Reference Systems Analysis

**Project:** Eidos — Engineering Intelligence for Deterministic, Orchestrated Software  
**Version:** 1.0.0  
**Scope:** Forensic Architectural Analysis of 13 State-of-the-Art Agentic Systems  

---

## 1. Taxonomic Classification of Reference Systems

Before analyzing individual systems, we categorize each system according to its dominant design paradigm:

1. **Autonomous Self-Hosted Agents**: Hermes Agent, OpenClaw
2. **Interactive Coding Harnesses & TUIs**: Claude Code, OpenCode
3. **Specification & Governance Frameworks**: GitHub Spec Kit
4. **Agent Security & Sandboxing Infrastructure**: NVIDIA OpenShell, NVIDIA SkillSpector
5. **Code Graph & Repository Intelligence Engines**: Graphify, RepoGraph
6. **Multi-Agent & Workflow Orchestrators**: Open Code Review (OCR), Worktrunk
7. **Agent Skill Standards & Repositories**: Anthropic Agent Skills, Emil Kowalski Skills / skills.sh

---

## 2. In-Depth System Evaluations

### 1. Hermes Agent (Nous Research)
- **Purpose**: Autonomous, self-hosted, persistent AI agent designed to live on local machines/servers and self-evolve across sessions.
- **Architecture**: Event-driven agent daemon connected to chat gateways (Telegram, Discord, Slack, CLI) with a DSPy/GEPA self-evolution optimization loop.
- **Runtime**: Python 3.10+.
- **Model Integration**: Open weights (Hermes series, Llama, Mistral) via vLLM/Ollama, plus API endpoints (OpenAI, Anthropic).
- **Harness**: Headless daemon with multi-channel messaging gateway.
- **Tools**: Dynamic tool execution via Python/bash and plugin registry (`hermes-example-plugins`).
- **Skills**: Skill scripts dynamically loaded from disk; self-improves skills via genetic prompt algorithms.
- **Memory**: Persistent cross-session user modeling and operational memory stored in SQLite/local vector store.
- **Context Management**: Rolling conversation memory with semantic retrieval of historical facts.
- **Subagents**: Limited multi-agent delegation; primarily operates as a long-running singleton.
- **Graph**: None natively; flat relational storage.
- **Security**: Local user execution privileges; lacks OS-level sandboxing by default.
- **Sandbox**: Relies on host environment or user-configured Docker containers.
- **Evaluation**: Evaluated on multi-turn dialogue, tool benchmarks, and DSPy optimization metrics.
- **Persistence**: SQLite database + markdown state files.
- **Git Integration**: Basic Git CLI commands via tool execution.
- **Documentation**: Markdown guides, setup scripts, Discord community.
- **Extensibility**: High (custom plugins and DSPy teleprompters).
- **Limitations**: High risk of context drift during long-horizon tasks; no formal architectural invariants or repository verification.
- **Eidos Status**: *Community-Driven / Experimental*.

### 2. OpenClaw (`openclaw/openclaw`)
- **Purpose**: Open-source gateway and agent harness transforming chat interfaces into autonomous software engineering control rooms.
- **Architecture**: Modular agent gateway orchestrating git worktrees, task dispatch, CI monitoring, and multi-user chat channels.
- **Runtime**: Node.js / TypeScript runtime with shell bridges.
- **Model Integration**: Multi-provider (Claude, GPT, Gemini, GitHub Copilot).
- **Harness**: Terminal & messaging gateway (Slack, Discord, Telegram) with background execution.
- **Tools**: CLI wrappers, GitHub API integrations, workspace file managers.
- **Skills**: Skill packages managed via `openclaw/agent-skills`.
- **Memory**: Session state persistence and chat context caching.
- **Context Management**: Channel-scoped context with auto-summarization.
- **Subagents**: Spawns isolated worker agents bound to dedicated Git worktrees.
- **Graph**: No formal AST code graph.
- **Security**: Role-based access within messaging channels; commands run with local runner permissions.
- **Sandbox**: Experimental container isolation; often executed directly on developer host.
- **Evaluation**: User task acceptance and CI/CD status reporting.
- **Persistence**: JSON session logs and git commit history.
- **Git Integration**: Native Git worktree automation (`git worktree add/remove`).
- **Documentation**: Official portal (`openclaw.ai`), API documentation, video tutorials.
- **Extensibility**: Plugin architecture via npm and TypeScript modules.
- **Limitations**: Lacks formal specification-driven constraints; prone to "vibe coding" regressions without verification gates.
- **Eidos Status**: *Community-Driven / Emerging*.

### 3. GitHub Spec Kit (`github/spec-kit`)
- **Purpose**: Specification-Driven Development (SDD) toolkit eliminating "vibe coding" in AI-assisted repositories.
- **Architecture**: Staged pipeline tool implementing a formal sequence: Constitution -> Specify -> Plan -> Tasks -> Implement -> Converge.
- **Runtime**: Python (packaged and run via `uv` / `specify` CLI).
- **Model Integration**: Model-agnostic; generates structured markdown artifacts intended for consumption by any LLM.
- **Harness**: Agnostic (works seamlessly with GitHub Copilot, Claude Code, Gemini CLI, Cursor).
- **Tools**: Deterministic file generation, template rendering, and contract linting.
- **Skills**: Slash commands and agent skill definitions for each phase (`/specify`, `/plan`, `/tasks`).
- **Memory**: Artifact-based persistent memory (all project context resides in `spec.md`, `plan.md`, `tasks.md`).
- **Context Management**: High signal-to-noise ratio: context is restricted to structured phase markdown.
- **Subagents**: Workflow-oriented; delegates specific tasks sequentially to the host harness.
- **Graph**: Hierarchical task-to-spec tree; no AST code graph.
- **Security**: Passive documentation/template layer; carries zero execution vulnerability.
- **Sandbox**: N/A (operates on the local file system creating markdown artifacts).
- **Evaluation**: Convergence checks verifying task completion against acceptance criteria.
- **Persistence**: Git-versioned markdown files in repository root or `.spec/`.
- **Git Integration**: Changes tracked naturally through standard Git commits.
- **Documentation**: Official documentation, GitHub blog technical articles.
- **Extensibility**: Custom templates and user-defined constitutional guidelines.
- **Limitations**: Does not enforce automated code verification, test execution, or type checking; relies on human/agent honesty during "Converge".
- **Eidos Status**: *Established / Community-Driven Standard*.

### 4. OpenCode (`anomalyco/opencode`)
- **Purpose**: Open-source terminal-first (TUI) and desktop AI coding agent supporting 75+ model providers.
- **Architecture**: Split-engine architecture featuring a dedicated `Plan` agent (for read-only architectural analysis) and a `Build` agent (for active modifications), with native LSP integration.
- **Runtime**: Go / Rust native binary or Node.js TUI.
- **Model Integration**: Comprehensive (OpenAI, Anthropic, Gemini, DeepSeek, Ollama, Groq).
- **Harness**: Full-screen terminal user interface (TUI) with parallel session management.
- **Tools**: LSP-backed symbol search, file edit tools, bash command execution.
- **Skills**: Project-level customization via `AGENTS.md` and `/init` bootstrapping.
- **Memory**: Session history with conversational branch switching.
- **Context Management**: Progressive disclosure using LSP symbols to prune unnecessary file lines.
- **Subagents**: Explicit dual-agent model (`Plan` vs `Build`).
- **Graph**: LSP call-hierarchy and reference trees.
- **Security**: Interactive user prompt confirmation for destructive terminal commands.
- **Sandbox**: Local process execution without kernel-level sandboxing.
- **Evaluation**: Interactive developer feedback and diff review.
- **Persistence**: Local SQLite/JSON session cache.
- **Git Integration**: Built-in diff view and branch switching.
- **Documentation**: Official website (`opencode.ai`), interactive terminal tutorials.
- **Extensibility**: Custom model configuration, custom prompts, and LSP plugin mounts.
- **Limitations**: No automated verification loop; requires human manual verification of patches.
- **Eidos Status**: *Emerging / Rapidly Maturing*.

### 5. Claude Code (Anthropic)
- **Purpose**: Production-grade terminal-native agentic coding tool developed by Anthropic.
- **Architecture**: Client-side CLI orchestrating a tool-use execution loop with auto-compaction of context, subagent dispatch, and progressive project guidelines (`CLAUDE.md`).
- **Runtime**: Node.js executable distributed via npm (`@anthropic-ai/claude-code`).
- **Model Integration**: Claude 3.5 Sonnet / Claude 3.7 Sonnet via Anthropic Messages API.
- **Harness**: Interactive CLI with rich terminal formatting, command approval gates, and multi-file diffing.
- **Tools**: Bash execution, Grep, Glob, View, Edit, Replace, Agent dispatch.
- **Skills**: Discovers skills dynamically from `.claude/skills/` and project `CLAUDE.md`.
- **Memory**: Context window auto-compaction and project-level memory files (`.claude/memory/`).
- **Context Management**: Dynamic context pruning, progressive disclosure of project rules, and subagent isolation.
- **Subagents**: Dispatches general-purpose and read-only subagents for isolated research tasks.
- **Graph**: Relies on Grep/Glob search; lacks persistent semantic or AST code graph.
- **Security**: Permission prompt tiering (read, write, bash) with configurable allowlists.
- **Sandbox**: Runs directly on user's machine; relies on OS user permissions.
- **Evaluation**: Internal SWE-bench validation and human-in-the-loop task completion.
- **Persistence**: Local conversation cache and Git working tree.
- **Git Integration**: Automatic Git status awareness, commit drafting, and PR creation.
- **Documentation**: Extensive official technical guides and best practice documentation.
- **Extensibility**: MCP server configuration and customizable skill directories.
- **Limitations**: Proprietary model lock-in; lacks automated invariant verification and architectural drift detection.
- **Eidos Status**: *Established / Commercial Benchmark*.

### 6. NVIDIA OpenShell
- **Purpose**: Kernel-enforced policy runtime sandbox for autonomous AI agents.
- **Architecture**: Layered security shim intercepting agent syscalls and network requests using Linux kernel primitives and declarative policies.
- **Runtime**: Rust / C++ kernel integration with Python/CLI management.
- **Model Integration**: Model-agnostic; wraps the agent execution runtime.
- **Harness**: Universal container/process sandbox wrapper.
- **Tools**: Intercepts all standard OS tools (bash, curl, file read/write).
- **Skills**: N/A (operates below the skill layer).
- **Memory**: Stateless security enforcement; audits telemetry streams.
- **Context Management**: Transparent to context.
- **Subagents**: Can spawn isolated child namespaces for subagent processes.
- **Graph**: N/A.
- **Security**: "Policy-as-Physics": Linux Landlock (filesystem restriction), seccomp-bpf (syscall restriction), Open Policy Agent (OPA network filtering), and credential scoping.
- **Sandbox**: Kernel-level native sandbox with near-zero overhead.
- **Evaluation**: Security penetration testing, prompt injection resistance benchmarks.
- **Persistence**: Append-only security audit log (`telemetry.jsonl`).
- **Git Integration**: Transparent.
- **Documentation**: Technical whitepaper, GitHub repository, security advisories.
- **Extensibility**: Custom OPA Rego policies and Landlock access rules.
- **Limitations**: Linux-specific kernel dependencies (limited macOS/Windows parity without virtualization).
- **Eidos Status**: *Experimental / Frontier Security Standard*.

### 7. Open Code Review (OCR - Alibaba)
- **Purpose**: Multi-agent automated code review CLI tool simulating an elite peer review team.
- **Architecture**: Multi-agent discourse pipeline: independent reviewer personas analyze diffs -> engage in structured cross-agent debate -> synthesize a deduplicated, prioritized finding report.
- **Runtime**: Python 3.10+.
- **Model Integration**: Multi-model (Qwen, GPT-4o, Claude).
- **Harness**: CLI tool and CI/CD GitHub Action runner.
- **Tools**: Git diff parser, AST analyzer, linter wrapper.
- **Skills**: Domain-specific review personas (Security, Performance, Clean Architecture).
- **Memory**: Repository review history cache.
- **Context Management**: Diff-targeted context pruning with relevant file slicing.
- **Subagents**: Native persona-based multi-agent architecture with structured discourse protocols.
- **Graph**: Basic syntax dependency analysis.
- **Security**: Read-only repository access; runs in CI without write permissions.
- **Sandbox**: Standard CI container environment.
- **Evaluation**: Precision and recall of bug/vulnerability detection on historical PR datasets.
- **Persistence**: Review reports stored in markdown/JSON format.
- **Git Integration**: Deep integration with Git diffs, PR comments, and GitHub Actions.
- **Documentation**: GitHub repository, research documentation.
- **Extensibility**: Customizable reviewer prompts and severity thresholds.
- **Limitations**: Focused strictly on review/auditing; cannot iteratively modify or repair code.
- **Eidos Status**: *Emerging / Academic & Enterprise Proven*.

### 8. Worktrunk
- **Purpose**: High-performance Git worktree manager designed specifically for concurrent AI coding agents.
- **Architecture**: CLI utility automating the creation, synchronization, isolation, and teardown of Git worktrees to prevent agent collision.
- **Runtime**: Rust.
- **Model Integration**: Agnostic (manages developer filesystem state).
- **Harness**: CLI utility invoked before/during agent launch.
- **Tools**: Automated Git worktree and branch manipulation.
- **Skills**: N/A.
- **Memory**: Local Git branch tracking.
- **Context Management**: Filesystem isolation ensures agents do not see uncommitted changes from parallel workers.
- **Subagents**: Prerequisite infrastructure for running parallel subagents on a single repository.
- **Graph**: Git commit DAG.
- **Security**: Prevents cross-agent filesystem race conditions and file clobbering.
- **Sandbox**: Filesystem folder segregation.
- **Evaluation**: Zero merge collisions during parallel agent benchmarks.
- **Persistence**: Git working trees.
- **Git Integration**: Core domain: native wrapper around `git worktree`.
- **Documentation**: GitHub repository, Rust crate docs.
- **Extensibility**: Standard CLI scripting.
- **Limitations**: Pure infrastructure tool; contains no AI or code analysis logic.
- **Eidos Status**: *Community-Driven / High-Utility Utility*.

### 9. NVIDIA SkillSpector
- **Purpose**: Pre-installation static and semantic security scanner for AI agent skills and tool packages.
- **Architecture**: Two-phase inspection engine: (Phase 1) Fast static analysis utilizing YARA malware signatures and AST pattern matching; (Phase 2) Semantic LLM auditing comparing stated intent against actual code implementation.
- **Runtime**: Python.
- **Model Integration**: Fast embedding/LLM classifier for semantic intent matching.
- **Harness**: CLI scanner and pre-install verification hook.
- **Tools**: AST parser, YARA engine, static taint analyzer.
- **Skills**: Specializes in auditing `SKILL.md`, Python scripts, and JSON schemas.
- **Memory**: Vulnerability signature database.
- **Context Management**: N/A.
- **Subagents**: N/A.
- **Graph**: Call graph and taint analysis within audited skill packages.
- **Security**: Detects prompt injection, data exfiltration, privilege escalation, and excessive agency. Provides 0–100 risk score.
- **Sandbox**: Executes within safe read-only analysis process.
- **Evaluation**: Validated against synthetic and real-world malicious agent skills.
- **Persistence**: Scan reports in JSON format.
- **Git Integration**: Can run as a pre-commit or pre-merge hook.
- **Documentation**: NVIDIA developer portal, research reports.
- **Extensibility**: Custom YARA rules and policy definitions.
- **Limitations**: Semantic pass incurs API latency and token cost; zero-day prompt injection can occasionally evade heuristics.
- **Eidos Status**: *Experimental / Best-in-Class Security Model*.

### 10. Anthropic Agent Skills Standard
- **Purpose**: Open, standardized specification for packaging reusable instructions, workflows, and tools for AI agents.
- **Architecture**: Directory-based specification centered around `SKILL.md` with YAML frontmatter, progressive disclosure triggers, and associated scripts/references.
- **Runtime**: Agnostic (markdown + standard scripts in bash/Python/Node).
- **Model Integration**: Claude Code, Antigravity, and compatible open harnesses.
- **Harness**: Adopted by Anthropic CLI, Google Antigravity, and community runners.
- **Tools**: Defines executable scripts within a `scripts/` directory.
- **Skills**: The canonical definition of the modern "Agent Skill".
- **Memory**: Static procedural instructions loaded into model context on activation.
- **Context Management**: **Progressive Disclosure**: Only name and description are initially visible; full instructions load only when activated.
- **Subagents**: Can specify subagent execution requirements within skill workflows.
- **Graph**: N/A.
- **Security**: Relies on host harness verification; lacks built-in cryptographic provenance.
- **Sandbox**: Dependent on host harness.
- **Evaluation**: Task completion fidelity when skill is active vs. baseline.
- **Persistence**: Checked directly into repository under `.agents/skills/` or `.claude/skills/`.
- **Git Integration**: First-class citizen in repository version control.
- **Documentation**: Official Anthropic documentation and examples.
- **Extensibility**: Fully open and customizable.
- **Limitations**: Lacks formal parameter validation schemas and execution sandboxing out of the box.
- **Eidos Status**: *Established Industry Standard*.

### 11. Emil Kowalski Skills & `skills.sh`
- **Purpose**: Curated ecosystem and package manager (`npx skills`) for high-craftsmanship agent skills (UI/UX, animation, design engineering).
- **Architecture**: Central registry (`skills.sh`) indexing GitHub repositories, paired with a CLI tool (`npx skills add/find`) for automated discovery and installation.
- **Runtime**: Node.js CLI (`npx skills`) distributing markdown/code skills.
- **Model Integration**: Claude Code, Cursor, Windsurf, Antigravity.
- **Harness**: Integrates with any agent harness supporting the `.agents/` or `.claude/` directory convention.
- **Tools**: Focuses on design review, animation calculation, and component auditing scripts.
- **Skills**: High-polish engineering heuristics (e.g., `apple-design`, `animate`, `review-animations`).
- **Memory**: Embedded architectural and design rules loaded into agent context.
- **Context Management**: Modular activation prevents clogging the main system prompt with design minutiae.
- **Subagents**: Compatible with subagent workflows.
- **Graph**: N/A.
- **Security**: Package manager relies on GitHub repository reputation, install counts, and star metrics; lacks kernel-level sandboxing.
- **Sandbox**: Dependent on host harness.
- **Evaluation**: Visual polish and automated test suite adherence.
- **Persistence**: `skills-lock.json` dependency manifest in project root.
- **Git Integration**: Committed directly to VCS.
- **Documentation**: Official portal (`skills.sh`), personal engineering essays.
- **Extensibility**: Any developer can publish a skill via a public GitHub repo.
- **Limitations**: No automated behavioral verification; community skills may vary in instruction adherence.
- **Eidos Status**: *Community-Driven Standard / Premier Registry*.

### 12. Graphify (`graphifyy`)
- **Purpose**: Transforms any repository of code, documents, and media into a persistent, queryable knowledge graph with community detection and visual audit trails.
- **Architecture**: Dual-tier pipeline: deterministic AST extraction for code (Python `ast`), semantic LLM extraction for unstructured documents, clustered using Louvain/Leiden community detection into NetworkX graphs.
- **Runtime**: Python 3.10+.
- **Model Integration**: Gemini 1.5/2.0/3.0 for semantic document extraction; zero-LLM local AST extraction for code.
- **Harness**: Standalone CLI (`graphify`), Python library, and agent skill integration.
- **Tools**: Built-in CLI commands: `query`, `path`, `explain`, `export` (HTML, Obsidian, Neo4j, FalkorDB).
- **Skills**: Packaged as an Antigravity/Claude Code agent skill.
- **Memory**: Graph persistence in `graphify-out/graph.json` and sidecar caches.
- **Context Management**: BFS/DFS graph traversals allow agents to retrieve multi-hop context within a strict token budget.
- **Subagents**: Dispatches parallel subagents for chunked semantic document extraction.
- **Graph**: Rich NetworkX graph with node types (`File`, `Function`, `Class`, `Community`) and epistemic edges (`EXTRACTED`, `INFERRED`, `AMBIGUOUS`).
- **Security**: Read-only codebase analysis; protects against graph corruption via node-shrink guards.
- **Sandbox**: Standard local execution.
- **Evaluation**: Graph cohesion scoring ($Q \in [0, 1]$), God Node centrality detection, and token reduction benchmarks.
- **Persistence**: Versioned JSON graph, HTML interactive visualizer, and Markdown audit report (`GRAPH_REPORT.md`).
- **Git Integration**: Can be triggered via post-commit hooks for incremental graph updates.
- **Documentation**: Comprehensive `SKILL.md` and detailed offline reference guides.
- **Extensibility**: Modular export targets (Neo4j, FalkorDB, Gephi GraphML, Obsidian).
- **Limitations**: Currently requires separate LLM pass for rich semantic inferences across documentation; AST parsing primarily optimized for Python/JS/TS.
- **Eidos Status**: *Established / High-Precision Knowledge Graph*.

### 13. RepoGraph (Ouyang et al., ICLR 2025)
- **Purpose**: Repository-level line-level and entity-level code graph designed to boost AI coding agents on SWE-bench tasks.
- **Architecture**: Tree-sitter AST parsing generating fine-grained reference and dependency graphs, queried dynamically during agent issue localization.
- **Runtime**: Python 3.9+.
- **Model Integration**: Plugs into SWE-agent, Agentless, and generic LLM backends.
- **Harness**: Research framework evaluated in headless Docker containers.
- **Tools**: Tree-sitter AST query engine, symbol reference resolver.
- **Skills**: N/A (academic evaluation harness).
- **Memory**: Static in-memory code graph generated per evaluation run.
- **Context Management**: Multi-hop path retrieval providing the exact call/reference chain for a reported bug without loading extraneous files.
- **Subagents**: Compatible with hierarchical localization subagents.
- **Graph**: Directed graph of entities (Files, Functions, Classes, Variables) connected by `CALLS`, `DEFINES`, `REFERENCES`, `IMPORTS`.
- **Security**: Runs in isolated Docker containers for SWE-bench execution.
- **Sandbox**: Docker containerization.
- **Evaluation**: Rigorously benchmarked on SWE-bench and SWE-bench Lite, demonstrating consistent percentage-point gains over un-graphed baselines.
- **Persistence**: Serialized graph structures (pickle/JSON).
- **Git Integration**: Analyzes repository commits and PR diffs.
- **Documentation**: Academic paper (`arXiv:2410.14684`), GitHub repository README.
- **Extensibility**: Extensible to any programming language supported by Tree-sitter.
- **Limitations**: Research prototype; lacks interactive CLI, progressive documentation routing, and security scanning.
- **Eidos Status**: *Academic Benchmark / State-of-the-Art Formulation*.

---

## 3. Cross-System Synthesis & Epistemic Status

| Dimension | Established Principles | Emerging Principles | Experimental / Frontier | Vendor-Specific | Community-Driven |
|:---|:---|:---|:---|:---|:---|
| **Specifications & Planning** | Phased SDD (`spec.md` -> `plan.md` -> `tasks.md`) | Living specs linked to automated tests | Auto-generated specs from runtime traces | Copilot-specific prompts | GitHub Spec Kit templates |
| **Context Management** | Progressive disclosure of rules (`AGENTS.md`) | Dynamic context pruning & auto-compaction | Subagent contract-bounded fresh context | Claude context caching | `skills.sh` package manifests |
| **Code Representation** | Grep / Glob file searching | AST symbol extraction via Tree-sitter | Epistemic knowledge graphs (`EXTRACTED` vs `INFERRED`) | Google Antigravity Code Lens | Graphify interactive HTML visualizer |
| **Security & Isolation** | User-prompt confirmation for shell commands | Static AST & YARA scanning of agent tools | Kernel-level "Policy-as-Physics" (Landlock, OPA) | Anthropic permission tiering | Worktrunk git worktree isolation |
| **Execution & Repair** | Interactive human-in-the-loop terminal diff review | Test failure feedback into prompt (Reflexion) | Deterministic invariant checking before `DONE` transition | Claude Code auto-fix loop | Open Code Review multi-agent discourse |

---

## 4. Architectural Lessons for Eidos

1. **Adopt Anthropic & Spec Kit's Progressive Disclosure**: Never overwhelm context with exhaustive rules; use `AGENTS.md` and `CONSTITUTION.md` as lightweight entry points routing to specialized sub-documents.
2. **Incorporate Graphify & RepoGraph's Relational Architecture**: Combine Tree-sitter multi-language AST extraction with NetworkX community clustering and epistemic edge tagging (`EXTRACTED` vs `INFERRED`).
3. **Embed NVIDIA's Security Philosophy**: Integrate static scanning (SkillSpector model) for skills and kernel-level process isolation (OpenShell model) for untrusted tool execution.
4. **Enforce Agentless & SWE-agent Determinism**: Replace unpredictable, wandering agent loops with rigid, contract-bounded execution phases backed by rich verification traces.
