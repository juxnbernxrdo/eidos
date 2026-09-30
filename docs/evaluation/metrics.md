# Metric Definitions & Mathematical Formalism

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** Quantitative Software Engineering Analytics  
**Status:** FROZEN NORMATIVE DEFINITIONS  

---

## 1. Primary Effectiveness & Reliability Metrics

### Metric `MTR-001`: Task Success Rate (Verification Success Rate — VSR)
- **Definition:** The proportion of experimental trials where the agent's proposed patch passes all public tests, all hidden held-out tests, and satisfies all specified system invariants.
- **Mathematical Formula:**
  $$\text{VSR} = \frac{1}{N} \sum_{i=1}^{N} \left( \mathbb{I}_{\text{public}}^{(i)} \land \mathbb{I}_{\text{hidden}}^{(i)} \land \mathbb{I}_{\text{invariant}}^{(i)} \right)$$
- **Unit:** Proportion / Percentage ($[0.0, 1.0]$ or $[0\%, 100\%]$).
- **Interpretation:** The definitive measure of end-to-end task completion. A trial that passes public tests but fails hidden tests or breaks security invariants is marked as a failure ($0$).
- **Limitations:** Binary metric per trial; does not reflect partial code progress if final assertions fail.

### Metric `MTR-002`: Public Test Pass Rate
- **Definition:** Proportion of trials where the public test suite passed.
- **Formula:** $\text{PPR} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}_{\text{public}}^{(i)}$
- **Interpretation:** Measures local developer-visible conformance. Discrepancy between PPR and VSR measures "false confidence".

### Metric `MTR-003`: Hidden Test Pass Rate
- **Definition:** Proportion of trials where held-out validation tests passed.
- **Formula:** $\text{HPR} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}_{\text{hidden}}^{(i)}$
- **Interpretation:** Measures generalizability and robustness against edge cases not explicitly stated in the public test files.

### Metric `MTR-004`: Mean Regressions per Trial
- **Definition:** Average number of previously working tests or functions broken by the agent's modification.
- **Formula:** $\text{MR} = \frac{1}{N} \sum_{i=1}^{N} R_i$ where $R_i \ge 0$ is the count of broken existing assertions.
- **Interpretation:** Lower is superior; measures code safety and localized isolation.

---

## 2. Resource Efficiency & Cost Metrics

### Metric `MTR-005`: Mean Total Tokens Consumed
- **Definition:** Sum of input prompt tokens and output completion tokens consumed across all agent turns and repair cycles for a trial.
- **Formula:**
  $$\text{Tokens}_{\text{total}} = \text{Tokens}_{\text{prompt}} + \text{Tokens}_{\text{completion}}$$
- **Aggregation:** Arithmetic Mean, Median, and 95% Confidence Interval across trials.
- **Interpretation:** Primary measure of token overhead.

### Metric `MTR-006`: Context Size (MSC Efficiency)
- **Definition:** Number of tokens allocated to repository context per prompt invocation.
- **Interpretation:** Directly isolates the efficiency of the Minimal Sufficient Context router against raw file dumping.

### Metric `MTR-007`: Wall-Clock Latency (ms)
- **Definition:** Total elapsed execution time from task initialization to final patch emission.
- **Unit:** Milliseconds (ms).

### Metric `MTR-008`: Mean Financial Cost per Task ($USD)
- **Definition:** Estimated monetary expense per trial based on standard frontier model pricing:
  $$\text{Cost} = \left( \frac{\text{Tokens}_{\text{prompt}}}{1,000,000} \times \$3.00 \right) + \left( \frac{\text{Tokens}_{\text{completion}}}{1,000,000} \times \$15.00 \right)$$
- **Unit:** USD ($).

### Metric `MTR-009`: Net Cost per Resolved Task
- **Definition:** Total monetary expenditure divided by the number of successful tasks:
  $$\text{Cost}_{\text{resolved}} = \frac{\sum_{i=1}^{N} \text{Cost}_i}{\sum_{i=1}^{N} \text{Success}_i}$$
- **Interpretation:** Crucial economic metric. If an unassisted baseline is cheap per trial but has a 10% VSR, its net cost per resolved task may be vastly higher than an orchestrated harness with an 85% VSR.
