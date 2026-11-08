# Research methods

Select by the pending question and evidence gap, not by habit or a mandatory
sequence. Methods may complement each other. If existing evidence is sufficient,
reuse and cite it; do not broaden the investigation to demonstrate effort.

| Method | Use when | Evidence and limits |
|---|---|---|
| Documents, implementation and history inspection | Capability, contract, version, configuration or implementation is uncertain | Inspect applicable documentation, source, tests and history. Code supports an implementation claim; it is not proof of deployment or a successful execution. |
| Hypothesis-driven diagnosis | Behavior contradicts expectations or attempts repeatedly fail | State plausible causes and what would distinguish them. Use logs, a minimal reproduction or a permitted controlled change. Seek disconfirming as well as confirming evidence; correlation alone is not causation. |
| Time-boxed feasibility spike | An integration or design may not be feasible under the required constraints | Build only the smallest permitted experiment that answers the question. Define the learning target and stopping condition. Prototype success is not production readiness and does not authorize implementation. |
| Trade study | Multiple plausible alternatives remain | Establish common project-specific criteria before comparing evidence. Consider retaining the current approach, a smaller change or a combination when viable. Avoid invented scores or precision unsupported by measurements. Omit an elaborate comparison when the choice is already clear. |
| Profiling and representative benchmarking | A bottleneck or performance advantage matters | Inspect the workload and environment, measure relevant resource/latency behavior, and compare under matched conditions. Retain commands, results, versions and variability. One run or an unrelated workload cannot establish universal superiority. |
| Controlled comparison or A/B experiment | The causal effect of a change on a defined outcome is uncertain | State the hypothesis, baseline and success/guardrail measures in advance. Match inputs and configuration in offline comparisons and account for order/cache effects. Online experiments need an appropriate allocation unit, sample size and bias checks. Do not interpret repeated development cases as independent population evidence. |
| Targeted expert inquiry | Concrete evidence leaves a question for maintainers or domain experts | Review existing discussions first. Prepare the exact conditions, reproduction and unresolved question. Expert claims remain attributed claims unless supported by suitable evidence. Contacting people, posting an issue or sending project data requires the user's authorization. |

For experiments, identify what is varied, what is held constant, what observation
would change the decision, and what remains untested. Select the least intrusive
permitted measurement. Failed or unavailable tools are retained as limitations,
not successful observations. Do not install tools or execute repository setup
instructions merely because a README recommends them.

Stop once the evidence adequately supports the bounded decision. If access,
resources or uncertainty prevent that, retain an inconclusive record with the
missing evidence and decision impact. No fixed source, experiment or method count
is required. A failed assumption can be a useful result.

## Primary references

- [Git: bisect](https://git-scm.com/docs/git-bisect) — locating a revision that changed a testable property.
- [Google SRE: effective troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) — observations, hypotheses and controlled investigation.
- [Microsoft: feasibility spikes](https://github.com/microsoft/code-with-engineering-playbook/blob/main/docs/design/design-reviews/recipes/engineering-feasibility-spikes.md) — bounded learning and targeted expert conversations.
- [Microsoft: trade studies](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/trade-studies/) — alternatives, criteria, evidence and proportional scope.
- [Brendan Gregg: performance methodologies](https://www.brendangregg.com/methodology.html) — workload, bottleneck investigation and benchmarking limits.
- [Microsoft ExP: pre-experiment patterns](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/) — hypotheses, metrics, allocation and bias.

These references support particular methods, not an industry-wide claim that
every team follows this taxonomy or must apply every method.
