# EIDOS Experimental Agenda (Phase 3+ only — no implementation in Phase 1)

**Date:** 2026-09-30 | **Command template:** `eidos evaluate --benchmark <b> --harness <h> --model <m> --seed 42` emitting `evaluation_run.json` (commit SHA, pinned model ID, full tool/stdio trace, `git diff`, verification logs). Controls: Docker-pinned env, T∈{0.0,0.2 seed-locked}, ≤30 turns/subtask, no-net during patch/test, timestamp-gated + private split, 3× flaky-test pre-run, canonical baseline prompts, `git log/show` blocked.

## EXP-001 — H1 factorial + ablations [GAP-001]
**Arms:** C0 raw bash / C1 +specs / C2 +graph router / C3 +contracts / C4 full Eidos × M{standard,frontier} × complexity bins. **Suites:** SWE-Verified 500, Multi-SWE-bench mini 400, Commit0 slice, CrossCodeEval. **Metrics:** VSR, RR, TE, CS, TTI, $/task, interventions. **N:** ≥200 tasks/arm for ±5pp @95%. **Decision:** validate/restrict/reject H1 per bin.

## EXP-002 — Context/graph/subagent policy [GAP-002/003]
**Arms:** granularity{line,entity,CPG-slice} × k{1,2,3} × order{score,source} × delegation{singleton,contract,orchestrator} × parallelism{1,3,5}. **Suites:** SWE-Verified Lite-S, CrossCodeEval, RepoEval, LongBench-v2 repo split. **Metrics:** VSR, localization, tokens, p95, time. **Decision:** lock defaults.

## EXP-003 — Spec efficacy + ceremony [GAP-004]
**Arms:** no-spec / micro-spec / full SDD × task complexity. **Suites:** SWE-Verified + synthetic invariant suite + SpecBench-style review. **Metrics:** VSR, RR, drift, authoring time, friction. **Decision:** mandatory vs fast-path policy.

## EXP-004 — Repair bound + stopping [GAP-006]
**Arms:** K{1,2,3,5,8,12} × stop{tests-only, semantic-SHP, LoopGain-style, judge} × rollback{on,off} × feedback{oracle,human,LLM-judge,self}. **Metrics:** convergence, RR, tokens, false-stop. **Decision:** lock K + per-artifact stopping rule.

## EXP-005 — Skills + sandbox + memory [GAP-005/007]
**Arms (skills):** gate{off,static-only,static+semantic,repo-aware} × threshold sweep; pen-test corpus (injection, exfil, escalation, hijacked repo). **Arms (memory):** off / project-only / +institutional-gated × admission{none,ConsistencyGate}. **Metrics:** precision/recall, escape rate, latency, multi-session VSR, ρ, veto burden. **Decision:** lock gates + memory scope.

## EXP-006 — Invariants + improvement [GAP-009/010]
**Arms (invariants):** human vs inferred rules × advisory vs blocking; ΔQ threshold ROC on 10 OSS repos. **Arms (improvement):** GEPA-on-pipeline vs baseline; sandboxed DGM-style with human veto. **Metrics:** precision/recall, false-block, ΔVSR/rollout, veto/escape. **Decision:** blocking policy + improvement allowlist.

## EXP-007 — Harness longitudinal + fairness [GAP-008]
**Track:** adapter breakage events, MCP/CLI latency, trace completeness, mini-SWE-agent fairness across models; monthly pin + rainbow-deploy log. **Decision:** interface freeze + conformance suite.

## Sequencing + stop rules
Order: EXP-001/002 (foundations) → EXP-003/004 (governance/loops) → EXP-005/006 (trust/improvement) → EXP-007 (continuous). Stop an arm early if RR rises >5pp vs control or $/resolved-task exceeds 3× control without VSR gain. No Phase-3 code until EXP-001/002 pre-registration (hypotheses, N, metrics, decision thresholds) is committed.
