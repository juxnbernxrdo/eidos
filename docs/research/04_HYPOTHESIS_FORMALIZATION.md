# EIDOS Central Hypothesis Formalization & Experimental Protocol

**Project:** Eidos — Engineering Intelligence for Deterministic, Orchestrated Software  
**Version:** 1.0.0  
**Research Unit:** Agentic Systems Empirical Validation Laboratory  

---

## 1. Central Hypothesis Formulation

### 1.1 Natural Language Statement
> **"El mejor modelo sin el harness adecuado no garantiza los mejores resultados."**  
> *(The frontier foundation model paired with an inadequate harness underperforms a smaller or standard model paired with an engineered, deterministic, context-aware harness.)*

### 1.2 Mathematical Formulation
We model the probability of successful, verified software task completion $S \in [0, 1]$ as a non-linear interaction tensor:

$$S = \Phi\Big(\mathcal{M} \otimes \mathcal{H} \otimes \mathcal{T} \otimes \mathcal{C}\Big)$$

Where:
- $\mathcal{M} \in \mathbb{R}^{d_m}$: **Model Vector** (parameter scale, reasoning depth, pre-training token distribution, context capacity).
- $\mathcal{H} \in \mathbb{R}^{d_h}$: **Harness Vector** (context engineering quality, Agent-Computer Interface (ACI), specification rigor, tool representation, graph navigation, verification feedback fidelity).
- $\mathcal{T} \in \mathbb{R}^{d_t}$: **Task Vector** (scope of modification, single-file vs. multi-file, ambiguity of requirements, bug localization complexity).
- $\mathcal{C} \in \mathbb{R}^{d_c}$: **Repository Complexity Vector** (lines of code, cyclomatic complexity, architectural coupling, dependency depth, documentation drift).
- $\Phi$: Sigmoidal task convergence function mapping the latent execution state to verified success.

---

## 2. Statistical Hypothesis Testing

### 2.1 Null Hypothesis ($H_0$)
$$\frac{\partial^2 S}{\partial \mathcal{M} \, \partial \mathcal{H}} = 0 \quad \text{and} \quad \mathbb{E}[S \mid \mathcal{M}_{\text{frontier}}, \mathcal{H}_{\text{baseline}}] \ge \mathbb{E}[S \mid \mathcal{M}_{\text{standard}}, \mathcal{H}_{\text{Eidos}}]$$
*The interaction effect between Model and Harness is additive or negligible. A frontier model operating within a rudimentary baseline harness (raw bash, unconstrained prompt) will achieve a task success rate equal to or higher than a standard model operating within the structured Eidos harness layer, regardless of task or repository complexity.*

### 2.2 Alternative Hypothesis ($H_1$)
$$\frac{\partial^2 S}{\partial \mathcal{M} \, \partial \mathcal{H}} > 0 \quad \text{and} \quad \exists \, \mathcal{C} > \mathcal{C}_{\text{threshold}} : \mathbb{E}[S \mid \mathcal{M}_{\text{standard}}, \mathcal{H}_{\text{Eidos}}] > \mathbb{E}[S \mid \mathcal{M}_{\text{frontier}}, \mathcal{H}_{\text{baseline}}]$$
*The interaction effect between Model and Harness is super-additive. Beyond a critical threshold of repository complexity ($\mathcal{C}_{\text{threshold}}$), a standard model operating within the Eidos harness layer statistically outperforms a frontier model in a rudimentary baseline harness in verified task completion, cost efficiency, and regression minimization.*

---

## 3. Experimental Variables

### 3.1 Independent Variables (IV)
1. **Model ($\mathcal{M}$)**:
   - $\mathcal{M}_1$: Baseline Standard Model (e.g., Claude 3.5 Haiku, GPT-4o-mini, Qwen 2.5 Coder 32B).
   - $\mathcal{M}_2$: Frontier Reasoning Model (e.g., Claude 3.5/3.7 Sonnet, OpenAI o1/o3, Gemini 1.5/2.0 Pro).
2. **Harness Architecture ($\mathcal{H}$)**:
   - $\mathcal{H}_{\text{Raw}}$: Raw bash shell execution with flat prompt (generic agent baseline).
   - $\mathcal{H}_{\text{Generic}}$: Standard tool-calling harness without graph or formal specs (e.g., vanilla ReAct/CodeAct).
   - $\mathcal{H}_{\text{Eidos}}$: Full Eidos Layer (Adaptive Interview $\rightarrow$ SDD Spec $\rightarrow$ Repo Graph $\rightarrow$ Context Router $\rightarrow$ Contract-Bounded Subagent $\rightarrow$ Verification-First Loop).

### 3.2 Dependent Variables (DV - Metrics)
1. **Verified Success Rate ($\text{VSR}$)**: Percentage of tasks where all unit, integration, and regression test suites pass without human intervention ($\% \in [0, 100]$).
2. **Regression Rate ($\text{RR}$)**: Percentage of tasks where the patch breaks previously passing test suites ($\% \in [0, 100]$).
3. **Token Efficiency ($\text{TE}$)**: Total input + output tokens consumed per resolved task ($\text{Tokens} / \text{Task}$).
4. **Context Saturation ($\text{CS}$)**: Average context window utilization percentage across agent steps ($\% \in [0, 100]$).
5. **Tool Thrashing Index ($\text{TTI}$)**: Count of redundant or failing tool calls before first productive edit ($\text{Calls} / \text{Task}$).
6. **Convergence Steps ($\text{CS}$)**: Total agent-environment interaction turns required to reach state `DONE`.
7. **Monetary Cost ($\text{Cost}$)**: Dollar cost per resolved task based on standard API pricing ($\$ / \text{Task}$).

### 3.3 Control Variables
- **Compute Environment**: Identical Docker containers (Debian Linux, 8 vCPUs, 32GB RAM, pinned Python/Node runtimes).
- **Sampling Temperature**: Locked at $T = 0.0$ for deterministic greedy decoding (or $T = 0.2$, seed-locked for reasoning models).
- **Max Interaction Limit**: Bounded at 30 turns per subtask to prevent infinite loops.
- **Network Egress**: Sandboxed; zero internet access during patch generation and test execution.

### 3.4 Confounders & Mitigation Strategies
| Confounder | Threat to Validity | Mitigation Protocol |
|:---|:---|:---|
| **Data Contamination in Pre-training** | Models may have memorized public GitHub issues/fixes. | Evaluate on recent, timestamp-gated commits and private/synthetic benchmark suites (e.g., SWE-bench Verified post-cutoff split). |
| **Flaky Tests** | Non-deterministic test suites produce false negative verifications. | Run test suites 3 times before task assignment to isolate non-deterministic tests; discard flaky tests from scoring. |
| **Model API Provider Drift** | Undisclosed backend model weights updates by API providers. | Pin exact snapshot model IDs (e.g., `claude-3-5-sonnet-20241022`, `gpt-4o-2024-08-06`) and record token logprobs where available. |
| **Prompt Sensitivity** | Minor phrasing differences in baseline prompts distort harness comparisons. | Use canonical, peer-reviewed baseline prompts directly from SWE-agent and Agentless official repositories. |

---

## 4. Benchmark Suites & Empirical Testbed

1. **SWE-bench / SWE-bench Lite / SWE-bench Verified** (*Princeton / OpenAI*):
   - 500 (Lite) and 500 (Verified) real-world Python GitHub issues across high-complexity repositories (Django, SymPy, scikit-learn, astropy, matplotlib).
2. **CrossCodeEval** (*Microsoft Research*):
   - Multi-file code completion benchmark testing cross-file context retrieval and dependency awareness.
3. **RepoEval** (*Zhang et al.*):
   - Repository-level unit test generation and completion benchmark measuring architectural comprehension.
4. **Synthetic Invariant Suite (Eidos Internal)**:
   - 100 multi-layer architectural refactoring tasks designed to test cyclic dependency detection, interface compliance, and documentation drift.

---

## 5. Existing Empirical Evidence Analysis

### 5.1 Evidence Supporting $H_1$
1. **SWE-agent Empirical Findings** (*Yang et al., NeurIPS 2024*):
   - When GPT-4 was evaluated in a raw bash environment, its SWE-bench solve rate was $< 4.0\%$.
   - When the exact same GPT-4 model was placed into the SWE-agent ACI harness (with bounded file viewers, lint feedback, and custom search), its solve rate jumped to **$12.5\%$** (a **$3.1\times$ improvement** purely from harness engineering).
2. **Agentless Benchmark** (*Xia et al., 2024*):
   - Open-source models (DeepSeek-Coder-33B) within the structured Agentless harness solved more SWE-bench issues ($27.3\%$) than unguided GPT-4 in complex multi-agent frameworks ($18.0\%$).
3. **RepoGraph Integration** (*Ouyang et al., ICLR 2025*):
   - Adding RepoGraph's AST context navigation to SWE-agent boosted resolution rates across every tested model by $3.4$ to $5.8$ percentage points while reducing token consumption by up to $28\%$.

### 5.2 Evidence Challenging / Qualifying $H_1$
1. **Reasoning Model Scaling (OpenAI o1/o3, DeepSeek-R1)**:
   - Models trained with reinforcement learning for test-time compute can self-correct basic syntactic and logical mistakes even in raw shells, narrowing the gap on *single-file, isolated tasks*.
   - *Qualification for Eidos*: On high-complexity, multi-file repositories ($\mathcal{C} > \mathcal{C}_{\text{threshold}}$), test-time compute alone cannot overcome lack of cross-file visibility, context truncation, or absence of project-level architectural invariants.

---

## 6. Reproducibility Protocol

To ensure 100% scientific reproducibility:
1. Every experimental run must emit an immutable `evaluation_run.json` containing:
   - Commit SHA of Eidos and benchmark repository.
   - Pinned model ID and provider completion headers.
   - Full event stream of all tool calls, arguments, stdout, and stderr.
   - Final Git patch (`git diff`).
   - Exact verification logs and test execution output.
2. The benchmark harness will be distributed with a single deterministic command:
   ```bash
   eidos evaluate --benchmark swe-bench-lite --harness eidos --model claude-3-5-sonnet-20241022 --seed 42
   ```
