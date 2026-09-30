# EIDOS Source Registry — Phase 1 Reinforcement (Second Pass)

**Project:** Eidos — Engineering Intelligence for Deterministic, Orchestrated Software
**Date:** 2026-09-30
**Scope:** All primary and secondary sources consulted in Phase 1 (original + reinforcement pass).
**ID scheme:** `SRC-XXX` stable. Status: `VERIFIED_PRIMARY | VERIFIED_SECONDARY | VENDOR | UNVERIFIED`.

---

## Tier 1 — Primary Research (papers, official engineering reports)

| ID | Title | Authors / Institution | Year | Type | URL | Benchmark | Code/Data | Quality |
|---|---|---|---|---|---|---|---|---|
| SRC-001 | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | Jimenez et al., Princeton / ICLR 2024 Oral | 2024 | PRIMARY_STRONG (peer-reviewed) | arxiv.org/abs/2310.06770, swebench.com | SWE-bench 2294 / Lite 300 | Yes (SWE-bench/SWE-bench) | PRIMARY_STRONG |
| SRC-002 | SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering | Yang et al., Princeton / NeurIPS 2024 | 2024 | PRIMARY_STRONG | arxiv.org/abs/2405.15793 | SWE-bench Full 12.47% GPT-4 Turbo, Lite 18.00%; +10.7pp vs shell-only | Yes | PRIMARY_STRONG |
| SRC-003 | Agentless: Demystifying LLM-based Software Engineering Agents | Xia et al., UIUC / FSE 2025 | 2024-25 | PRIMARY_STRONG | arxiv.org/abs/2407.01489 | Lite 27.33% ($0.34) → 32.00% ($0.70); Verified 38.8%, >50% w/ Claude-3.5-Sonnet | Yes | PRIMARY_STRONG |
| SRC-004 | Executable Code Actions Elicit Better LLM Agents (CodeAct) | Wang et al., UIUC+Apple / ICML 2024 | 2024 | PRIMARY_STRONG | arxiv.org/abs/2402.01030 | API-Bank, M3 ToolEval, MiniWob++; hasta +20% vs JSON | Yes (CodeActInstruct 7k) | PRIMARY_STRONG |
| SRC-005 | OpenHands: An Open Platform for AI Software Developers | Wang, Li et al., Stanford/CMU/UIUC | 2024-25 | PRIMARY_STRONG | arxiv.org/abs/2407.16741 | Lite 26% (Claude-3.5); HumanEvalFix 79.3%; ML-Bench 76.47% GPT-4o | Yes | PRIMARY_STRONG |
| SRC-006 | Introducing SWE-bench Verified | OpenAI + Princeton | 2024-08 | PRIMARY_MODERATE (tech report, human annotation 93 devs) | openai.com/index/introducing-swe-bench-verified/ | Verified 500 (68.3% filtered); GPT-4o 33.2% | Yes (new Docker harness) | PRIMARY_MODERATE |
| SRC-007 | SWE-Bench+: Enhanced Coding Benchmark | Aleithan et al., York/Calgary | 2024 | PRIMARY_MODERATE | arxiv.org/abs/2410.06992 | Leakage 32.67%, weak tests 31.08%; Verified 22.4%→10.0% after filter | Yes | PRIMARY_MODERATE |
| SRC-008 | Lost in the Middle: How Language Models Use Long Contexts | Liu et al., Stanford / TACL 2024 | 2023-24 | PRIMARY_STRONG | arxiv.org/abs/2307.03172 | Multi-doc QA; >20% drop mid-context; 20→50 docs only +1.5% | Yes | PRIMARY_STRONG |
| SRC-009 | Reflexion: Language Agents with Verbal Reinforcement Learning | Shinn et al., Northeastern/Princeton / NeurIPS 2023 | 2023 | PRIMARY_STRONG | arxiv.org/abs/2303.11366 | HumanEval 91% vs 80%; AlfWorld +22pp / 12 iters | Yes | PRIMARY_STRONG |
| SRC-010 | Teaching LLMs to Self-Debug | Chen et al., CMU/Microsoft | 2023 | PRIMARY_STRONG | arxiv.org/abs/2304.05128 | Spider +2-3% (+9% hardest); TransCoder/MBPP hasta +12% | Yes | PRIMARY_STRONG |
| SRC-011 | Self-Refine: Iterative Refinement with Self-Feedback | Madaan et al., CMU/Google/AllenAI / NeurIPS 2023 | 2023 | PRIMARY_STRONG | arxiv.org/abs/2303.17651 | ~+20pp avg vs one-shot; max ~4 iters | Yes | PRIMARY_STRONG |
| SRC-012 | Is Self-Repair a Silver Bullet? | Olausson et al., MIT / ICLR 2024 | 2024 | PRIMARY_STRONG | arxiv.org/abs/2306.09896 | Self-repair ≈/peor que i.i.d. sampling a igual coste; human feedback 33.3%→52.6% | Yes | PRIMARY_STRONG |
| SRC-013 | RepoGraph: Enhancing AI SWE with Repository-level Code Graph | Ouyang et al., UIUC/Tencent / ICLR 2025 | 2025 | PRIMARY_STRONG | arxiv.org/abs/2410.14684 | +32.8% relative avg on SWE-bench; gains on CrossCodeEval | Yes (ozyyshr/RepoGraph) | PRIMARY_STRONG |
| SRC-014 | CodexGraph: Bridging LLMs and Code Repositories via Code Graph DBs | Liu et al., NUS/XJTU/Alibaba / NAACL 2025 | 2024-25 | PRIMARY_STRONG | arxiv.org/abs/2408.03910 | CrossCodeEval Lite Python + EvoCodeBench; ≈AutoCodeRover on Lite | Yes | PRIMARY_STRONG |
| SRC-015 | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | Wu et al., Microsoft Research / COLM 2024 | 2023-24 | PRIMARY_STRONG | arxiv.org/abs/2308.08155 | MATH 69.48% vs 55.18%; ALFWorld +15%; GAIA #1 Mar-2024 | Yes | PRIMARY_STRONG |
| SRC-016 | RAG or Long-Context LLMs? + Self-Route | Li et al., Google DeepMind + Michigan / EMNLP Industry 2024 | 2024 | PRIMARY_STRONG | aclanthology.org/2024.emnlp-industry.66/ | Self-Route +5% over RAG, 61%/38.6% tokens; −65%/−39% cost | Yes | PRIMARY_STRONG |
| SRC-017 | LongBench v2 | Bai et al., THUDM Tsinghua / ACL 2025 | 2024-25 | PRIMARY_STRONG | arxiv.org/abs/2412.15204 | 503 MCQ incl. code-repo; o1-preview 57.7% vs human 53.7% | Yes | PRIMARY_STRONG |
| SRC-018 | BABILong (NeurIPS 2024 D&B) | Track Datasets & Benchmarks | 2024 | PRIMARY_STRONG | NeurIPS 2024 proceedings | LLMs use only 10-20% of context; RAG-chunk fails multi-hop | Yes | PRIMARY_STRONG |
| SRC-019 | OP-RAG: Order-Preserve RAG | Yu et al. | 2024 | PRIMARY_MODERATE | arxiv.org/pdf/2409.01666 | En.QA 44.43 F1 @16k vs LC 34.26 @117k | Yes | PRIMARY_MODERATE |
| SRC-020 | CoALA: Cognitive Architectures for Language Agents | Sumers, Yao et al., Princeton / TMLR 2024 | 2023-24 | PRIMARY_STRONG (framework) | arxiv.org/abs/2309.02427 | Framework, no benchmark | — | PRIMARY_MODERATE |
| SRC-021 | MemGPT: Towards LLMs as Operating Systems | Packer et al., Letta/MIT/UCB | 2023 | PRIMARY_STRONG | arxiv.org/abs/2310.08560 | Baseline for later memory work | Yes | PRIMARY_MODERATE |
| SRC-022 | A-MEM: Agentic Memory for LLM Agents | Xu et al. | 2025 | PRIMARY_MODERATE | arxiv.org/abs/2502.12110 | DialSim F1 3.45 (+35% LoCoMo, +192% MemGPT) | Yes | PRIMARY_MODERATE |
| SRC-023 | Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory | Chhikara et al. | 2025 | PRIMARY_MODERATE | arxiv.org/abs/2504.19413 | LOCOMO +26% vs OpenAI; −91% p95, >90% tokens | Yes | PRIMARY_MODERATE |
| SRC-024 | DSPy / GEPA: Reflective Prompt Evolution Can Outperform RL | Khattab et al. Stanford 2023; Agrawal et al. Berkeley/Stanford 2025-26 ICLR Oral | 2023-26 | PRIMARY_STRONG | arxiv.org/abs/2310.03714, arxiv.org/abs/2507.19457 | GEPA +6pp avg vs GRPO (hasta +19pp), 35× fewer rollouts | Yes | PRIMARY_STRONG |
| SRC-025 | Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents | Zhang et al., UBC/Oxford / ICLR 2026 | 2025 | PRIMARY_MODERATE | arxiv.org/abs/2505.22954 | SWE-bench 20%→50%, Polyglot 14.2%→30.7% | Yes | PRIMARY_MODERATE |
| SRC-026 | SWE-smith: Scaling Data for Software Engineering Agents | Yang et al., Stanford/Princeton / NeurIPS 2025 Spotlight | 2025 | PRIMARY_STRONG | arxiv.org/abs/2504.21798 | 50k synthetic instances/128 repos; Qwen2.5-32B 40.2% Verified SOTA open | Yes | PRIMARY_STRONG |
| SRC-027 | Agent Skills in the Wild (SkillScan) | Liu et al. | 2026-01 | PRIMARY_MODERATE | arxiv.org/pdf/2601.10338 | 42,447 skills, 31,132 analyzed; Cato CTRL MedusaLocker case | Data released | PRIMARY_MODERATE |
| SRC-028 | Context Matters: Repository-Aware Security Analysis of the Agent Skill Ecosystem | — | 2026-03 | PRIMARY_MODERATE | arxiv.org/html/2603.16572v2 | 238,180 skills; malicious 46.8% ClawHub / 23.0% Skills.sh / 6.0% SkillsDir; only 0.52% persist w/ context | Yes | PRIMARY_MODERATE |
| SRC-029 | ConsistencyGate: Preventing Memory Contamination | Zhang & Li, Florida State | 2026 | PRIMARY_MODERATE | arxiv.org/html/2607.22962v1 | LoCoMo-Contam/MSC-Contam; admission gate p̂≥τ | Yes | PRIMARY_MODERATE |
| SRC-030 | CYCLE (training self-debug) / Revisit Self-Debugging | Ding et al. 2024; Chen et al. ACL 2025 | 2024-25 | PRIMARY_MODERATE | arxiv.org/abs/2403.18746, arxiv.org/abs/2501.12793 | CYCLE +63.5% relative small models; self-tests w/o oracle degrade | Yes | PRIMARY_MODERATE |
| SRC-031 | FormalBench / vericoding benchmark | Le et al., Bursuc et al. / ACL 2025 | 2025 | PRIMARY_MODERATE | arxiv.org/abs/2509.22908 | 12,504 specs; Dafny 82.2%, Verus 44.2%, Lean 26.8% | Yes | PRIMARY_MODERATE |
| SRC-032 | SpecBench (spec-reasoning) / SpecBench (reward hacking) | Hamblin et al. Toronto 2026; WecoAI 2026 | 2026 | PRIMARY_MODERATE | arxiv.org/abs/2605.30314, arxiv.org/abs/2605.21384 | Best GPT-5.4 44.4% (<45%); Δ val-test grows w/ horizon | Yes | PRIMARY_MODERATE |
| SRC-033 | Found in the Middle (positional bias calibration) | Univ. Washington | 2024 | PRIMARY_MODERATE | arxiv.org/html/2406.16008 | +6-15pp mid-context on 7B | Yes | PRIMARY_MODERATE |
| SRC-034 | Long Context RAG Performance of LLMs (20 LLMs) | — | 2024-11 | PRIMARY_MODERATE | arxiv.org/abs/2411.03538 | Only SOTA monotonic >64k; open-source peak 16-32k | Yes | PRIMARY_MODERATE |
| SRC-035 | Multi-SWE-bench (ByteDance Seed, NeurIPS 2025 D&B) | ByteDance Seed | 2025 | PRIMARY_STRONG | arxiv.org/abs/2504.02605 | 1,632 instances, 7 langs, human-validated | Yes (multi-swe-bench) | PRIMARY_STRONG |
| SRC-036 | Commit0 (ICLR 2025) | — | 2024-25 | PRIMARY_STRONG | arxiv.org/abs/2412.01769 | 54-57 libs from scratch; no agent fully solves | Yes (commit-0/commit0) | PRIMARY_STRONG |
| SRC-037 | CrossCodeEval (NeurIPS 2023 D&B) | Amazon Science | 2023 | PRIMARY_STRONG | github.com/amazon-science/cceval | 10k examples/1k repos, cross-file EM/ES | Yes | PRIMARY_STRONG |
| SRC-038 | RepoEval / RepoCoder (EMNLP 2023) | Zhang et al., Microsoft | 2023 | PRIMARY_STRONG | arxiv.org/abs/2303.12570 | Repo-level completion, post-2022 repos | Yes | PRIMARY_STRONG |
| SRC-039 | SWE-bench Multimodal (ICLR 2025) | — | 2024-25 | PRIMARY_MODERATE | arxiv.org/abs/2410.03859 | 517 JS visual instances | Yes (sb-cli) | PRIMARY_MODERATE |
| SRC-040 | Gödel Agent | Yin et al. / ACL 2025 | 2025 | PRIMARY_MODERATE | aclanthology.org/2025.acl-long.1354/ | Self-modifying agent line | Yes | PRIMARY_MODERATE |

## Tier 1.5 — Official engineering doctrine (vendor primary, non-peer-reviewed)

| ID | Title | Institution | Year | URL | Quality |
|---|---|---|---|---|---|
| SRC-100 | Building Effective Agents | Anthropic Engineering | 2024-12 | anthropic.com/engineering/building-effective-agents | SECONDARY_STRONG (doctrine, no metrics) |
| SRC-101 | Effective Context Engineering for AI Agents | Anthropic Engineering | 2025-09 | anthropic.com/engineering/effective-context-engineering-for-ai-agents | SECONDARY_STRONG |
| SRC-102 | How We Built Our Multi-Agent Research System | Anthropic (Hadfield et al.) | 2025-06 | anthropic.com/engineering/multi-agent-research-system | SECONDARY_STRONG (internal eval +90.2%, 15× tokens) |
| SRC-103 | Prompt Caching | Anthropic | 2024-12 | anthropic.com/news/prompt-caching | VENDOR (claim −90% cost/−85% latency) |
| SRC-104 | Equipping agents for the real world with Agent Skills + open spec | Anthropic | 2025-10/12 | agentskills.io/specification, github.com/anthropics/skills | PRIMARY_MODERATE (standard) |
| SRC-105 | Introducing MCP / Donating MCP to Agentic AI Foundation | Anthropic / Linux Foundation | 2024-11/2025-12 | anthropic.com/news/model-context-protocol | PRIMARY_MODERATE (standard) |
| SRC-106 | Introducing SWE-bench Verified (blog) | OpenAI | 2024-08 | openai.com/index/introducing-swe-bench-verified/ | PRIMARY_MODERATE |
| SRC-107 | Memory for teams / Memory tool API | Anthropic | 2025-09/10 | claude.com/blog/memory, platform.claude.com/docs/.../memory-tool | SECONDARY_STRONG |
| SRC-108 | Evaluate Agent Skills Before Publication (SkillEvaluator) | NVIDIA Docs | 2025-26 | docs.nvidia.com/skills/evaluating-agent-skills.md | SECONDARY_STRONG |
| SRC-109 | Claude Code: How Claude Code Works | Anthropic | 2025-26 | code.claude.com/docs/en/how-claude-code-works | SECONDARY_MODERATE |

## Tier 2 — Open source systems (verified repo/docs snapshot 2026-09)

| ID | System | URL | License/Runtime | Quality |
|---|---|---|---|---|
| SRC-200 | Hermes Agent (NousResearch) | github.com/NousResearch/hermes-agent | MIT / Python | SECONDARY_STRONG (arch verified, no SWE-bench) |
| SRC-201 | OpenClaw | github.com/openclaw/openclaw, docs.openclaw.ai | MIT / Node-TS | SECONDARY_MODERATE |
| SRC-202 | OpenCode (sst/opencode → opencode-ai) | github.com/sst/opencode, opencode.ai/docs | MIT / Go+TUI | SECONDARY_MODERATE |
| SRC-203 | GitHub Spec Kit | github.com/github/spec-kit | MIT / Python (uv) | SECONDARY_STRONG (process, no controlled benchmark) |
| SRC-204 | NVIDIA OpenShell | github.com/NVIDIA/OpenShell, docs.nvidia.com/openshell | Apache-2.0 / Rust+C++ | SECONDARY_MODERATE (alpha, no prod) |
| SRC-205 | NVIDIA SkillSpector | github.com/NVIDIA/SkillSpector | — / Python+LangGraph | SECONDARY_MODERATE |
| SRC-206 | Alibaba open-code-review (`ocr`) | github.com/alibaba/open-code-review | Apache-2.0 / Python | SECONDARY_MODERATE (self-reported precision claims UNVERIFIED) |
| SRC-207 | worktrunk (`wt`) | github.com/max-sixty/worktrunk, worktrunk.dev | MIT/Apache / Rust | SECONDARY_MODERATE |
| SRC-208 | skills.sh + emilkowalski/skills | skills.sh, github.com/emilkowalski/skills | MIT / Node | SECONDARY_MODERATE |
| SRC-209 | Graphify (Graphify-Labs) | github.com/Graphify-Labs/graphify | — / Python (tree-sitter+NetworkX) | WEAK (own BENCHMARKS.md only) |
| SRC-210 | Joern / Code Property Graph + codebadger MCP | github.com/joernio/joern, docs.joern.io | — / Scala | SECONDARY_STRONG (CPG mature; codebadger claims UNVERIFIED) |
| SRC-211 | CrewAI / LangGraph+CrewAI study | github.com/crewaiinc/crewai, arxiv.org/html/2411.18241v1 | Apache-2.0 | WEAK (no peer-reviewed numbers) |

## Unverified / do-not-cite-as-evidence (2026 aggregators, vendor marketing)

- U-001: 2026 leaderboard claims (Opus 5 96%, GPT-5.5 88.7%, Gemini 3.1 80.6%, DeepSeek V4 80.6%, Sonnet 4.6 79.6% …): aggregators `benchmarks.company/llmreference/benchlm`, inconsistent across harnesses → **UNVERIFIED**. Never cite as EVIDENCE.
- U-002: DeepSWE/Datacurve audit (VentureBeat 2026-05: `CHEATED 12% git log`, `SWE-Pro 8.5% FP/24% FN`): relevant threat model for Eidos sandbox design, but single vendor audit → **UNVERIFIED**, use only as HYPOTHESIS driver.
- U-003: OpenCode `160-195k stars/7-16M devs`, OCR `precision >Claude Code @1/9 tokens`, Graphify `BENCHMARKS.md`, codebadger `90% slice / CVE-2025-6021 first-try`, LoopGain `false-stop ≤4.5%`: **UNVERIFIED** until reproduced.
- U-004: Anthropic subagent `41% higher success` as cited in Phase-1 v1 (EV-04): exact figure not recovered in primary 2024-25 doctrine pages → downgraded to **UNVERIFIED**, replaced by SRC-102 (+90.2% internal research-eval, non-code task).

---

## Practitioner sources on Loop Engineering (emerging term, non-academic)

| ID | Source | URL | Quality |
|---|---|---|---|
| SRC-300 | Loop Engineering knowledge base (2026) | loop-engineering.net | WEAK (blog, glossary usable) |
| SRC-301 | Santander Harness/Loop Engineering (observe-decide-act-check) | santander.com/en/stories/engineering-the-loop... | SECONDARY_MODERATE |
| SRC-302 | LoopGain — Barkhausen trajectory monitor | github.com/loopgain-ai/loopgain | WEAK (repo claim) |
| SRC-303 | Semantic Early-Stopping SHP (embeddings+Info Score) | arxiv.org/pdf/2606.27009 | PRIMARY_MODERATE |
| SRC-304 | Convergence detection (agentpatterns) / VS Code Autopilot max-3 | github.com/agentpatterns-ai/website/.../convergence-detection.md | WEAK |
