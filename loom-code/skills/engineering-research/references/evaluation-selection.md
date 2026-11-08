# Select an engineering evaluation approach

Read this for a design/alternative assessment, a claim about a change's effect,
or an operational-risk question. Select an approach that answers the actual
question; these are optional tools, not a mandatory sequence or new Loom gates.
Equivalent methods are valid when their fit and evidence are explained.

## Frame the decision

Identify the object, applicable version/environment, pending decision, and
uncertainty that could change it. Preserve the user's established constraints.
A fact or completion claim can be settled by direct applicable evidence without
a named framework. Reuse adequate evidence; do not turn every lookup into a
trade study or force a method label, matrix, diagram or new experiment.

For comparisons, distinguish mandatory constraints from preferences. Exclude a
candidate that fails a mandatory condition; a weighted total cannot compensate
for it. Choose relevant quality dimensions from the project rather than checking
every possible attribute. Define an observable check or evidence target for
material criteria, such as which modules/tests a change affects, under what load
a response target holds, or whether a permission boundary is enforced.

Quality models organize criteria; analysis methods structure reasoning;
experiments/source inspection obtain evidence; notes and diagrams represent it.
None substitutes for another. ISO/IEC 25010 can inform the quality dimensions;
do not claim ISO compliance from using a few labels or an adapted procedure.

## Match the question to the approach

Choose a primary approach per independently answerable question. Add a
complementary method only for a distinct consequential gap. A mixed question
may need more than one method; unrelated questions retain separate records.

| Question | Appropriate starting approach | Evidence and limits |
|---|---|---|
| Is a premise, capability or completion claim true here? | Direct source/configuration/artifact inspection | Match version and conditions; historical success needs actual historical results. No named framework is required. |
| Can an integration work under the constraints? | Time-bounded feasibility experiment | Define the exact unknown, minimal permitted test, observation and stopping point. Success answers that bounded question, not production readiness. |
| Which design, library or implementation fits best? | Lightweight trade study | Compare credible alternatives against common relevant criteria and actual evidence. Consider the current approach, a smaller change, postponement or combination when viable; use a short rationale for a clear choice. |
| Do architecture decisions conflict under important conditions? | Concrete quality scenarios informed by ATAM | State the condition/event, affected parts, expected measurable response and tradeoffs. A few scenarios are not a completed ATAM; major cross-team decisions may need the full facilitated process. |
| Is this code/change understandable, correct and testable? | Focused design/code-health inspection | Inspect actual call paths, edge/concurrency behavior, complexity, tests and change impact. Respect existing project criteria; this research does not replace the owning review station. |
| Why does observed behavior differ from expectations? | Hypothesis-driven troubleshooting | Use competing explanations, distinguishing observations and negative results. Separate symptom mitigation from causal explanation; one successful retry is not proof of cause. |
| Which resource limits a workload? | Utilization, saturation and errors (USE), with relevant profiling/wait analysis | Inspect resource use, queues/errors and the actual workload/time window. Missing metrics stay unknown; USE does not explain every application or cache problem. |
| Is A faster or cheaper for our workload? | Representative controlled benchmark plus analysis while it runs | Match work/configuration, verify correctness and the true limiting factor, retain versions and variation. Unmatched timings or statistically precise measurements of the wrong work are inconclusive. |
| Did a change cause an improvement? | Appropriate controlled comparison; randomized A/B where justified | Define baseline, effect and guardrail measures, allocation unit, exposure/data validity and uncertainty. Offline repeated cases are not independent population evidence. Sample-ratio checks apply to suitable allocated experiments, not arbitrary case counts. |
| Can actors misuse trust, permissions or data flows? | Threat modeling; STRIDE prompts for technical security | Model assets, actors, flows and trust boundaries; identify concrete threats, controls and validation. STRIDE addresses identity, integrity, accountability, confidentiality, availability and authorization; privacy harms or valid-workflow abuse can need different prompts. Plausible threats are not verified vulnerabilities. |
| What if dependencies fail, slow down or overload? | Failure-mode/resilience analysis | Trace user impact, propagation, detection, containment and recovery. AWS's SEEMS prompts cover single points of failure, excessive load/latency, misconfiguration/bugs and shared fate; use relevant questions rather than rigid categories. An untested mitigation stays unverified. |
| Can we migrate without loss or compatibility breaks? | Staged migration analysis and old/new comparison | Inspect affected read/write paths, invariants, compatibility stages, comparison evidence, cutover and irreversible steps. Adapt to the actual artifact: a Markdown move needs link/provenance checks, not a copied database procedure. Dual writes, when relevant, introduce partial-write/retry/ordering risks. |
| Is a service/release reliable enough to proceed? | Relevant user-facing service targets and bounded rollout analysis | Reuse actual indicators/targets, baseline, representative exposure, stop and recovery conditions. Service-level objectives are not mandatory for a local artifact question. Missing CI/deployment evidence cannot be replaced with a tiny canary, source definitions or a successful subprocess exit. |

## Form a supported conclusion

Keep measured outcomes, source-supported facts, reported experience, inference
and preference distinct. Use comparable measurements or clear qualitative
judgments; do not invent numeric scores. If weighted scoring helps, define its
scales/weights, preserve unknown inputs, and check whether plausible assumptions
or weight changes reverse the recommendation. A framework name is not evidence
quality or certainty.

Explain material tradeoffs and what new evidence or changed conditions would
alter the recommendation. Stop once the bounded decision is sufficiently
supported; if access, cost or uncertainty prevents resolution, retain an
inconclusive result and identify the missing observation. Do not search or run
experiments merely to fill all cells.

Keep the existing question-based record, metadata, source policy and optional
diagram contract. A new index, ADR, scorecard or named framework section is not
required. Record fit/criteria in `Method and rationale`, actual support in
`Evidence`, and implications/conditions in `Decision impact`.

Selecting a method does not authorize implementation, installation, contacting
others, a production experiment, deployment, or irreversible data changes.
Return evidence and the bounded recommendation to the owning task.

## Primary method references

- [ISO/IEC 25010 product quality model](https://www.iso.org/standard/78176.html) — public abstract; paid standard not reproduced here.
- [Microsoft trade studies](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/trade-studies/) and [feasibility spikes](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/recipes/engineering-feasibility-spikes/).
- [SEI ATAM](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/).
- [Google code review criteria](https://google.github.io/eng-practices/review/reviewer/looking-for.html) and [SRE troubleshooting](https://sre.google/sre-book/effective-troubleshooting/).
- [USE](https://www.brendangregg.com/usemethod.html) and [active benchmarking](https://www.brendangregg.com/activebenchmarking.html).
- [Microsoft experimental data validity](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/).
- [OWASP threat modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html).
- [AWS resilience analysis](https://docs.aws.amazon.com/prescriptive-guidance/latest/resilience-analysis-framework/applying-framework.html).
- [Stripe migration experience](https://stripe.com/blog/online-migrations) — reported case, not a universal recipe.
- [Google bounded release evaluation](https://sre.google/workbook/canarying-releases/).
- [NASA decision analysis](https://www.nasa.gov/reference/6-8-decision-analysis/) — proportional rigor, constraints and uncertainty.

This selection guidance adapts those approaches to engineering research. It is
not a claim of industry-wide adoption, complete domain coverage, certification
or proof that a particular framework will improve an agent's output.
