# Evaluation Governance Framework

**Authority:** Eidos System Constitution Article IV & Phase 7 Mandate  
**Scope:** Epistemic Standards, Scientific Method, Experimental Ethics, and Quality Controls  
**Status:** BINDING  

---

## 1. Foundational Axioms of Evaluation

Eidos Phase 7 operates under strict scientific standards designed to prevent confirmation bias, methodological circularity, and inflated performance claims:

1. **Anti-Confirmation Bias**: Do not design experiments to "prove that Eidos works". Design experiments to systematically interrogate:
   - *Does it work?*
   - *How much does it work?*
   - *When does it work?*
   - *When does it NOT work?*
   - *Which specific components cause the effect?*
   - *What costs and latencies does it introduce?*
   - *What threats to validity remain?*
2. **Negative Results are First-Class Knowledge**: A negative result showing that a component adds overhead without improving outcomes is as valuable as a positive result. Such findings are never hidden, softened, or discarded.
3. **No Metric or Task Modification Post-Hoc**: Benchmark tasks, success criteria, and metric definitions must be locked prior to trial execution. Modifying a test or threshold after seeing data is strictly prohibited.
4. **Epistemic Classification**: Every claim and observation must be categorized into standard epistemic classes:
   - `FACT`: Reproducible raw trace or measurement (e.g. exit code 0, 3,147 tokens).
   - `EXPERIMENTAL_RESULT`: Aggregated statistical finding under controlled trials (e.g. $\Delta VSR = +54.0$ pp).
   - `OBSERVATION`: Direct qualitative or quantitative trace phenomenon.
   - `INTERPRETATION`: Explanatory conjecture linking observation to cause.
   - `HYPOTHESIS`: Unverified empirical assertion.
   - `UNKNOWN`: Unmeasured or confounding variable.

---

## 2. Definitional Separation: Verification vs Evaluation vs Validation

| Dimension | Core Question | Governing Phase | Primary Output | Epistemic Nature |
|:---|:---|:---:|:---|:---|
| **Verification** | *"Does the implementation satisfy its written contracts and specifications?"* | **Phase 6** | `PASS` / `FAIL` | Deterministic, non-probabilistic |
| **Evaluation** | *"How does the system perform empirically against controlled baselines and ablations?"* | **Phase 7** | Empirical Metrics, Effect Sizes, p-values | Statistical, probabilistic, empirical |
| **Validation** | *"Does the system solve the real-world software engineering problem for human developers?"* | **Phase 7+ / 8** | Field Case Studies, Longitudinal Studies | User-centric, ecological |

**Crucial Mandate:** Demonstrating a high Verification Success Rate in Phase 6 does not imply empirical superiority in Phase 7. Superiority must be demonstrated statistically against fair baselines holding the base model constant.

---

## 3. Scientific Integrity & Prohibited Practices

The following actions constitute scientific malpractice within Eidos:
- **P-Hacking**: Running trials until a desired p-value is achieved and dropping non-significant seeds.
- **Cherry-Picking**: Removing difficult tasks or failed trials from the reported dataset.
- **Confounder Presentation**: Presenting a multi-variable comparison (e.g. changing model AND harness simultaneously) as a causal proof of harness efficacy.
- **Harmonization**: Changing the definition of a metric (e.g. redefining "success" to mean "public tests passed" instead of all tests) to inflate numbers.
- **Silent Mutation**: Editing the underlying code or prompt templates during an experiment without recording a new arm.

---

## 4. Instrumentation & Observer Effect Minimization

All measurement probes, token counters, and trace loggers implemented in [`src/eidos/evaluation/`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/evaluation/) must:
1. Not alter the runtime environment of the agent under evaluation.
2. Not inject privileged context or test assertions into the agent prompt.
3. Separate the Eidos system being evaluated (the experimental subject) from the evaluation infrastructure (the test harness).

---

## 5. Phase 8 Evolution Guard

Phase 7 may identify defects, inefficiencies, or optimization opportunities. However:
> **Phase 7 is strictly prohibited from modifying the core Eidos architecture or source code in response to evaluation findings.**

All proposed optimizations must be recorded as recommendations in [`docs/evaluation/phase-8-handoff.md`](file:///home/juxnbernxrdo/Documentos/eidos/docs/evaluation/phase-8-handoff.md) for deliberation and governed mutation in Phase 8.
