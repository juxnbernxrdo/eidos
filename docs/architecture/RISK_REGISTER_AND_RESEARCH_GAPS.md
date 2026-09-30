# EIDOS Risk Register & Research Gaps

**Project:** Eidos — Engineering Intelligence for Deterministic, Orchestrated Software  
**Version:** 1.0.0  
**Scope:** Systematic Hazard Analysis, Mitigation Protocols, and Open Scientific Questions  

---

## 1. Risk Register

| Risk ID | Category | Risk Description | Probability | Impact | Severity Score | Mitigation Strategy in Eidos Architecture |
|:---|:---|:---|:---|:---|:---|:---|
| **RSK-01** | Agentic / Autonomy | **Runaway Infinite Repair Loops**: Agent fails a test, attempts a blind fix, breaks another test, and loops indefinitely consuming excessive API credits. | High (0.75) | High (0.80) | **Critical (0.60)** | Enforce strict convergence bounding: max $K = 5$ repair attempts. If verification does not converge, halt execution, snapshot state, and escalate to human. |
| **RSK-02** | Security | **Supply-Chain Compromise via Third-Party Skills**: Malicious or vulnerable skill package installed from an untrusted registry exfiltrates repository secrets. | Med (0.40) | Critical (0.95) | **Critical (0.38)** | Mandate **Skill Security Gateway** (SkillSpector model): YARA scanning, static AST analysis, author provenance check, and risk score $< 25$ gate. |
| **RSK-03** | Performance / Context | **Context Window Saturation & Cost Explosion**: Repository Intelligence Graph or AST parsing dumps excessive tokens into subagent context. | Med (0.50) | Med (0.60) | **High (0.30)** | Enforce **Minimum Sufficient Context (MSC)** algorithm: only $k \le 2$ graph neighborhood and pruned type signatures are injected. |
| **RSK-04** | Harness Portability | **Host Harness API Breakage**: External harness vendors (Anthropic Claude Code, Google Antigravity) update proprietary CLI flags or tool formats. | High (0.70) | Med (0.50) | **High (0.35)** | Isolate all harness communication behind the `HarnessAdapter` abstract base class and adhere to standardized open protocols (MCP over stdio). |
| **RSK-05** | Integrity / Data Loss | **Destructive File System Operations**: Subagent running bash tool executes accidental deletion (`rm -rf`) or corrupts Git history during refactoring. | Low (0.20) | Critical (1.00) | **High (0.20)** | Implement **Policy-as-Physics** runtime sandboxing (Linux Landlock / process namespaces) restricting writes strictly to the active workspace. |
| **RSK-06** | Epistemic | **Hallucinated Architectural Relationships**: Model treats an unverified semantic guess as an empirical dependency, skewing the graph. | High (0.65) | Med (0.45) | **High (0.29)** | Epistemic classification tagging: all edges are explicitly labeled `EXTRACTED` vs `INFERRED`. Inferred edges carry confidence scores and cannot override compiler facts. |
| **RSK-07** | Developer Adoption | **Specification Overhead Friction**: Developers perceive SDD specification writing as too slow for simple 1-line bugfixes. | High (0.60) | Med (0.40) | **Moderate (0.24)** | Provide a "Micro-Spec / Fast-Path" profile that auto-generates localized specs for single-file, low-complexity tasks while preserving full verification. |
| **RSK-08** | Reproducibility | **Model Weights / Provider Drift**: Undisclosed updates to backend LLM weights alter agentic behavior between benchmark runs. | High (0.80) | Med (0.40) | **High (0.32)** | Pin exact snapshot model IDs, record token logprobs where supported, and publish reproducible seed-locked evaluation manifests (`evaluation_run.json`). |

---

## 2. Research Gaps & Open Empirical Questions

While Eidos is grounded in the latest 2024–2026 literature, several fundamental theoretical and empirical questions remain open:

### 2.1 Optimal Graph Abstraction Granularity
- **Open Question**: *What is the optimal node granularity for repository intelligence graphs—file-level, class/function-level, or line/AST-statement level?*
- **Trade-off**: Line-level graphs (as in RepoGraph) provide pinpoint bug localization but incur massive in-memory graph sizes and token overhead on 100k+ LOC repositories. File/class-level graphs are fast and lightweight but require the agent to search within files.
- **Empirical Plan**: Run ablation experiments comparing AST Entity-level vs. Line-level nodes on SWE-bench Lite within Eidos.

### 2.2 Semantic Invariant Synthesis
- **Open Question**: *Can an AI agent reliably synthesize high-level architectural invariants (e.g., domain isolation, idempotency rules) purely from observing historical Git commits and PR reviews on an existing legacy repository?*
- **Trade-off**: Human-defined invariants are precise but tedious to write. LLM-inferred invariants may capture real patterns or hallucinate non-existent conventions.
- **Empirical Plan**: Evaluate the precision and recall of `eidos invariant infer` against ground-truth architectural rules across 10 popular open-source projects (Django, FastAPI, Flask, etc.).

### 2.3 The Limits of Test-Time Compute in Complex Repositories
- **Open Question**: *To what extent can reinforcement-learned reasoning models (e.g., o1/o3, DeepSeek-R1) compensate for poor harness tooling on multi-file, cross-repository tasks?*
- **Trade-off**: Test-time compute enables models to self-reflect and generate test cases mentally, but cannot inspect files it has not retrieved or execute tests it cannot run.
- **Empirical Plan**: Test $H_1$ by comparing reasoning models in raw bash vs. standard models in Eidos across varying repository complexity levels ($\mathcal{C}$).
