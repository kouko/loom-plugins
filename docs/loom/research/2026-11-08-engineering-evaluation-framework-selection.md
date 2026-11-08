---
title: "Which engineering evaluation approach fits which research question?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
  - software-engineering
  - decision-analysis
---

# Which engineering evaluation approach fits which research question?

## Question and scope

How should the proposed `loom-workflow:engineering-research` choose an
engineering evaluation approach based on the actual question, project conditions
and decision risk, informed by published practitioner experience?

The baseline is the uninstalled [revision-4 prototype](../2026-11-07-engineering-research-trial/revision-4-structured-relations/candidate/engineering-research/SKILL.md)
and its [method catalog](../2026-11-07-engineering-research-trial/revision-4-structured-relations/candidate/engineering-research/references/research-methods.md).
This record proposes selection guidance. It does not change the prototype,
install a skill, create a Loom station, or certify compliance with any standard.

## Method and rationale

Read primary standards summaries, method-owner guidance, and first-party
engineering reports. Search in English and Japanese; retain only sources that
support a claim. Inspect actual article bodies and selected report sections,
not search snippets alone. Prioritize accounts explaining a failure, limitation
or decision consequence over lists of framework names.

The evidence ledger below distinguishes normative descriptions from reported
experience. No private project files were submitted to searches. No company
implementation was independently reproduced, no upstream repository behavior
was certified, and no experiment of this proposed selection policy was run.
Public guidance was inspected on 2026-11-08; historical reports do not establish
an organization's present-day internal practice.

## Findings

### Use approaches at the level where they answer the question

The selection proposal distinguishes four roles:

| Role | What it contributes | Examples |
|---|---|---|
| Evaluation dimensions | Which properties matter to this decision | Product quality model, project constraints and user outcomes |
| Analysis procedure | How to compare designs, identify risks or explain behavior | Trade study, architecture scenarios, threat modeling, hypothesis-driven diagnosis |
| Evidence acquisition | How to obtain a missing observation | Source tracing, feasibility experiment, profiling, representative benchmark, controlled experiment |
| Durable representation | How to preserve a supported conclusion | The existing research Markdown record, comparison table, optional Mermaid |

This is a Loom-oriented classification, not a published universal taxonomy.
A quality model does not supply runtime evidence; a diagram does not validate
an implementation; a successful prototype does not select the final design.
ISO's public summaries distinguish the product-quality reference model from
the evaluation framework, and explicitly state that ISO/IEC 25040 does not
provide specific test methods [S01, S02].

### Practitioner experience that changes the selection rule

| Source/context | What the inspected source actually reports | Selection consequence proposed for Loom | Limit |
|---|---|---|---|
| Microsoft software trade studies [S03] | Alternatives are compared against agreed criteria; clear choices should skip the full study. The team describes pairing on criteria and preserving results in the repository. | Compare only plausible alternatives; a known answer can use a short rationale. | Team practice, not a controlled productivity result. |
| Microsoft feasibility work [S04, S05] | Experiments are time-bounded learning activities. Its Graph authentication example investigates operations under minimal permissions. The separate technical-spike guidance distinguishes fact-finding from final selection. | Investigate the uncertain capability first; use the results in a later comparison if a choice still remains. | The permission example is illustrative guidance; no raw execution evidence is supplied. |
| SEI CAAS avionics architecture evaluation [S07] | Sections 5.1–5.2 report increased risk awareness and stakeholder communication. Several participants thought evaluation came too late to materially change design. Section 4 warns that counts of risks versus non-risks do not measure architecture quality. | Use architecture scenarios while a consequential decision can still change; do not score designs by the number of risks found. | Historical acquisition case and participant feedback, not general ROI evidence. |
| Google App Engine troubleshooting [S08] | An indexing hypothesis was contradicted when static content was also slow. Application instrumentation eventually identified an access-control cache problem. Mitigation preceded full diagnosis. | Seek observations that distinguish competing explanations; preserve mitigation and causal explanation as separate results. | The chapter says its case was compressed and simplified; not independently reproduced. |
| Microsoft/MSN experiment [S14] | A carousel experiment appeared negative because a bot filter excluded affected users. Investigating sample-allocation imbalance changed the interpretation. | Validate the experiment's data path before drawing an effect conclusion. | First-party retrospective; not proof that every imbalance has the same cause. |
| Monzo security design [S13] | The 2022 article describes collaborative STRIDE threat modeling for new infrastructure, periodic reassessment, and deriving controls/design principles from the models. | Route security-boundary changes to an adversarial design analysis and check concrete controls. | The article explicitly limits accuracy to publication time; effectiveness was not independently measured. |
| Stripe subscriptions migration [S17] | The team describes dual writes, backfill, comparison of old/new read results, incremental path changes and eventual removal of old data. | Evaluate migration stages, consistency and cutover evidence, rather than only the attractiveness of the target design. | A particular migration report; neither a universal dual-write recipe nor proof of atomicity. |
| AWS resilience analysis [S15, S16] | AWS attributes its failure categories to work with customers and advises selecting relevant questions rather than rigidly classifying every failure. | Examine failure propagation for the relevant user story; retain unknowns and iterate. | Practitioner guidance with examples, not a published comparative outcome study. |

### Proposed question-to-approach selection

All rows below are proposed adaptations. Source links justify the underlying
method, not a claim that this exact router has already been behaviorally tested.

| Question being decided | Primary approach | Minimum useful evidence/output | When to simplify or escalate |
|---|---|---|---|
| **F0 — Is the premise/capability/completion claim true here?** | Direct inspection of applicable source, configuration, version and actual artifacts | Claim, relevant revision/conditions, inspected path or real execution result, remaining unknown | No named framework needed if direct evidence settles it. Historical success requires historical results, not a fresh source read. |
| **F1 — Can this integration work under our constraints?** | A time-bounded feasibility experiment [S04, S05] | Exact unknown, minimal test, success/failure observation, conditions, stopping point | Reuse adequate existing evidence. Escalate only when the unknown still changes the choice; do not grow a prototype into production work. |
| **F2 — Which library, design or implementation should we choose?** | A lightweight trade study [S03], with relevant quality dimensions [S01] | Mandatory constraints, credible alternatives, common criteria, evidence, tradeoffs and conditional recommendation | Include the current approach, a smaller change, postponement or a combination when viable. Use a short rationale when a clear choice remains. |
| **F3 — Will architecture choices conflict under important conditions?** | Quality-scenario analysis informed by ATAM [S06, S07] | Concrete condition/event, affected components, expected measurable response, approaches, risks and conflicting goals | A few decision-critical scenarios can inform a local design. Seek the full facilitated method for major cross-team/high-impact architecture decisions; do not label a small checklist a completed ATAM. |
| **F4 — Is this code/refactor appropriate, understandable and testable?** | Focused design/code-health inspection using applicable review criteria [S18] | Actual change/call paths, correctness and concurrency concerns, complexity, meaningful test coverage and change impact | Use existing project criteria. Do not turn a research question into another complete closing review or silently approve implementation. |
| **F5 — Why does actual behavior differ from expectations?** | Hypothesis-driven troubleshooting [S08] | Observations, plausible competing causes, discriminating tests, negative results and current explanation | Contain active harm within authorization before exhaustive diagnosis. Correlation or one successful retry does not establish a cause. |
| **F6 — Which resource limits this workload?** | Resource bottleneck analysis: utilization, saturation and errors (USE) [S09] | Resource inventory, load/time window, queueing/errors, profile or wait evidence where relevant | Missing metrics stay unknown. Application algorithms, remote waits and caches can require other analysis; do not treat USE as every performance method. |
| **F7 — Is A faster or cheaper for our workload?** | Representative controlled benchmarking plus analysis while the benchmark runs [S10] | Matched inputs/configuration, actual work performed, limiter, repetitions/variability, versions and relevant costs | A single unmatched number is inconclusive. Verify the benchmark target and correctness before interpreting statistical precision. |
| **F8 — Did this change cause an outcome improvement?** | A controlled comparison appropriate to the allocation unit; randomized A/B when justified [S14] | Prespecified effect/guardrail measures, baseline, exposure/data validity, sample uncertainty and confounders | Distinguish offline paired cases from population experiments. Apply sample-ratio checks to applicable allocated experiments, not arbitrary case counts. No unapproved live traffic experiments. |
| **F9 — Can an actor misuse trust, permissions or data flows?** | Threat modeling, with STRIDE prompts for technical security [S12, S13] | Assets/actors, data flow and trust boundaries, concrete threats, relevant controls and validation evidence | Use privacy- or business-abuse-specific approaches when STRIDE does not fit [S12]. A list of plausible threats is not verified vulnerability evidence or proof of completeness. |
| **F10 — What happens if dependencies fail, slow down or overload?** | Failure-mode/resilience analysis, using AWS's SEEMS prompts when applicable [S15, S16] | User story, failure trigger, local/downstream effects, detection, containment/recovery and unverified mitigation | A small component can use a compact table. High-impact failure paths warrant deeper tests, within authorization; drawing redundancy does not prove resilience. |
| **F11 — Can we migrate without losing data or breaking compatibility?** | Staged migration analysis and old/new comparison, informed by the Stripe case [S17] | Read/write paths, compatibility stages, data invariants, comparison/backfill evidence, cutover and point-of-no-return conditions | Dual writes add failure modes and cost; inspect partial writes, retry/idempotency, ordering and consistency under the actual architecture. Do not copy the case blindly or authorize deletion. |
| **F12 — Is this service/release reliable enough to proceed?** | User-facing service-level targets and bounded rollout analysis [S11] | Relevant indicator/target, baseline, representative exposure, observed regression signals, stop/recovery conditions | Existing service objectives should be reused. Without meaningful observations, retain an unresolved readiness claim; a tiny canary is not complete compatibility coverage. |

SEEMS is AWS's grouping of single points of failure, excessive load, excessive
latency, misconfiguration/bugs, and shared fate (failure propagation). It is
used here as a set of prompts, not a required taxonomy or a reason to add AWS
infrastructure to a project [S15, S16].

STRIDE groups technical security threats concerning identity, integrity,
accountability, confidentiality, availability and authorization. It is a prompt
set; privacy harms and misuse of otherwise valid workflows can need additional
models [S12]. A migration check can therefore combine F11 with F9 or F10 when
the actual question includes those boundaries.

### Shared selection and stopping rules

The following proposed rules synthesize the sources and the existing prototype;
they are not ISO requirements or additional Loom gates.

- State the pending decision, actual object/revision and the uncertainty that
  could change the answer before choosing a framework. If the current evidence
  already answers it, reuse it and keep the record proportionate.
- Select one primary approach for each independently answerable question. Add
  a complementary approach only for an identified gap; split unrelated questions
  into their existing question-based record structure. Do not run the catalog.
- Separate mandatory constraints from preferences. A failed mandatory condition
  excludes an alternative; a favorable weighted total cannot compensate for it.
  NASA explicitly makes this distinction [S19].
- Select relevant quality dimensions from the project and quality model. Define
  an observable check or evidence target for each material criterion. A generic
  label such as "maintainable" is not an evaluation result [S01, S18].
- Record facts, measured outcomes, reported experience, source inference and
  preferences separately. Evidence quality and actual applicability are not
  encoded by a framework name or a numeric score.
- Use qualitative judgments or comparable measurements by default. If weighted
  scoring is useful, define the scales and weights, retain missing evidence as
  unknown, and examine whether plausible assumption/weight changes reverse the
  recommendation. Treat this as decision sensitivity, not measured certainty
  [S19].
- Stop when remaining uncertainty is unlikely to alter the bounded decision,
  or when resolving it is infeasible or not worth the cost. Report which missing
  observation could change the conclusion rather than searching indefinitely.
  NASA's decision guidance explicitly varies rigor with consequence and
  uncertainty; Microsoft's trade-study guidance permits omitting clear choices
  [S03, S19].
- Keep recommendations inside the owning task's authority. Analysis may show
  that a deployment, contact, installation, production test or irreversible data
  change is needed; it does not supply that authorization.

### Expected record content

Keep the existing file-per-question and flat-frontmatter contract. Reuse the
current template headings. In `Method and rationale`, state the selected
approach, relevant criteria, scope and why it fits. In `Evidence`, show the
actual source/measurement and applicable conditions. In `Decision impact`, give
the supported conclusion, material tradeoffs, and conditions that would change
it. An inconclusive result is valid. A separate ADR, index, scorecard or diagram
is not mandatory; Mermaid remains optional and cannot replace evidence.

## Decision impact for the current prototype

| Existing capability inspected | Result of this research |
|---|---|
| Premise checks, proportionate methods and sources, explicit limitations | Preserve. They already support selecting a method by the actual gap. |
| Feasibility, trade study, diagnosis, profiling/benchmarking and A/B methods | Preserve and clarify their different questions; avoid replacing them with one universal evaluation checklist. |
| General project-specific criteria | Add a clearer distinction between hard constraints, quality dimensions, observations and preferences if this proposal is adopted. |
| Architecture, security, resilience, migration and release readiness | Supply conditional reference guidance or examples for these question types; do not load all of it for every invocation. |
| Per-question records and optional relationships | Preserve. Add method-specific detail only when it helps the actual decision. |
| Prior dogfood evidence | Preserve its limited scope; it did not evaluate this new selection proposal, all these domains, or comparative understanding gains. |

The local baseline and its [dogfood report](../../skill-dogfood/2026-11-08-engineering-research/report.md)
were inspected as project context. No earlier trial or dogfood artifact was
rewritten. Adopting a routing rule would be a later prototype change requiring
behavioral checks for ambiguous, mixed and simple questions.

## Evidence ledger

Each entry below identifies content actually inspected. URLs were opened during
this investigation. "Reported" means the author's experience, not a new local
measurement. References are paraphrased, not reproduced in full.

| ID | Primary source | Inspected content and evidence class |
|---|---|---|
| S01 | [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | Official public abstract/status: product-quality reference model and evaluation uses. Full paid standard not read. |
| S02 | [ISO/IEC 25040:2024](https://www.iso.org/standard/83467.html) | Official public abstract/status: quality-evaluation framework; specific test methods excluded. Full paid standard not read. |
| S03 | [Microsoft — Trade Studies](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/trade-studies/) | When to Use, Why, Flow and Template descriptions; practitioner process guidance. |
| S04 | [Microsoft — Engineering Feasibility Spikes](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/recipes/engineering-feasibility-spikes/) | Introduction, feedback/pivoting, code samples and Graph permissions example; practitioner guidance and illustrative example. |
| S05 | [Microsoft — Technical Spike](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/recipes/technical-spike/) | Deliverable section on repeatability, fact-finding and evidence; method guidance. |
| S06 | [SEI — ATAM collection/method](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) | Method description and steps; source for architecture scenarios, quality interactions and facilitated evaluation scope. |
| S07 | [SEI — CAAS ATAM case, 2003](https://www.sei.cmu.edu/documents/2021/2003_004_001_14150.pdf) | Report context and selected results, printed pp. 16–18 (PDF pp. 26–28); risk-count caveat, participant feedback and timing limitations. Historical case report, not all 31 PDF pages inspected. |
| S08 | [Google SRE — Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) | Theory, testing limitations and App Engine case; first-party method and simplified retrospective. |
| S09 | [Brendan Gregg — USE Method](https://www.brendangregg.com/usemethod.html) | Resource/metric definitions, short saturation hidden by averages, strategy and limits; method author's experience and guidance. Claimed general success percentages not used. |
| S10 | [Brendan Gregg — Active Benchmarking](https://www.brendangregg.com/activebenchmarking.html) | Summary, active/passive distinction and benchmark validity cautions; practitioner guidance, no local benchmark. |
| S11 | [Google SRE Workbook — Canarying Releases](https://sre.google/workbook/canarying-releases/) | Risk-model assumptions, representative population/duration, metric selection and model-complexity caveat; guidance with an illustrative model. |
| S12 | [OWASP — Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) | Overview, system model/trust boundaries and technique-selection guidance; community-maintained method reference. |
| S13 | [Monzo — How we secure the banking platform](https://monzo.com/blog/2022/03/31/how-we-secure-monzos-banking-platform) | Threat modelling and Design principles sections; published 30 March 2022, with explicit historical-accuracy notice. First-party reported practice. |
| S14 | [Microsoft Research — Diagnosing Sample Ratio Mismatch](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/) | SRM explanation and MSN carousel case, published September 2020; first-party reported experimental failure and correction. |
| S15 | [AWS — Resilience analysis overview](https://docs.aws.amazon.com/prescriptive-guidance/latest/resilience-analysis-framework/overview.html) | Desired properties and SEEMS failure categories; practitioner guidance attributed to customer experience. |
| S16 | [AWS — Applying resilience analysis](https://docs.aws.amazon.com/prescriptive-guidance/latest/resilience-analysis-framework/applying-framework.html) | User-story/component questions and non-rigid, iterative application advice; practitioner guidance. |
| S17 | [Stripe — Online migrations at scale](https://stripe.com/blog/online-migrations) | Subscriptions example, four stages, backfill, comparison of read paths and incremental write-path changes; historical first-party migration account. |
| S18 | [Google — What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Design, functionality/concurrency, complexity and meaningful tests; published engineering policy, not runtime proof. |
| S19 | [NASA — Decision Analysis, section 6.8](https://www.nasa.gov/reference/6-8-decision-analysis/) | Decision context, proportional rigor, mandatory criteria, methods, uncertainty and recommendation; systems-engineering guidance adapted here, not exclusively a software framework. |

## Limitations and open questions

This is a purposive primary-source review, not a systematic literature review,
industry adoption survey or proof of causal benefits. It favors organizations
that publish their practices and has publication/survivorship bias. Historical
cases and stakeholder feedback cannot establish present-day effectiveness for
Loom. Japanese searches provided contextual leads; no Japanese source was needed
to support the selected claims. Search leads not relied upon are not evidence.

The source diversity supports choosing different approaches for different
questions, not a mandatory industry-wide taxonomy. Specialist domains such as
regulated safety engineering, privacy analysis, formal verification, detailed
experiment statistics and economic modeling can require domain expertise and
additional sources. No claim of compliance or complete coverage is made.

The proposed selection policy remains unimplemented and untested. Its next
evaluation would need mixed questions, facts requiring no framework, explicit
constraints, invalid experimental evidence and framework-overuse negatives.
New wording must preserve the prototype's existing triggers and general method
behavior; the earlier dogfood cannot establish improved triggering for an edit
that has not occurred.
