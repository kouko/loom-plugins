---
title: "Do two timing receipts justify simplifying the research workflow?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Do two timing receipts justify simplifying the research workflow?

## Question and scope

Do the supplied B01 and B02 receipts support replacing complex research with brief file checks to improve quality and reduce cost across the workflow? What minimum additional observations would support a decision?

This is an isolated, offline assessment dated 2026-11-08, with no active change. It examines only the supplied timing receipts and their actual task scopes. No models, tests, network services, or experiments were run. The repository snapshot is not a checkout, deployment, or CI result; implementation behavior is outside this question.

## Method and rationale

Inspect and compare existing execution records, then assess competing explanations for the observed difference. This is a descriptive comparison, not a controlled benchmark. The supplied records are enough to determine whether the proposed conclusion follows; additional source-code investigation would not recover absent quality evaluations, billing, or matched workloads. Stop at the evidence boundary and specify missing observations instead of creating measurements.

## Findings

### Recorded observations

| Receipt field | B01 | B02 |
| --- | ---: | ---: |
| Elapsed seconds | 103.188 | 42.637 |
| Input tokens | 177,820 | 116,861 |
| Cached input tokens | 148,352 | 92,544 |
| Cache-write input tokens | 0 | 0 |
| Output tokens | 4,249 | 1,359 |
| Reasoning output tokens | 134 | 15 |
| Exit code | 0 | 0 |
| Timed out | false | false |

Both receipts record the same requested provider (`openai`), model (`gpt-6.1-sol`), and effort (`medium`). These are requested settings, not independent confirmation of the actual served configuration or identical execution conditions.

B02 took 60.551 fewer seconds, approximately 59% less elapsed time than B01. It also recorded approximately 34% fewer input tokens and 68% fewer output tokens. These are arithmetic comparisons of the supplied receipts, not new runtime measurements. Cached input is reported separately within input usage; it must not be added to input tokens as extra usage. The receipts do not establish whether reasoning output is an additional billable category, so it is not summed with output here.

### Scope and causal interpretation

The task summary describes B01 as a source-only investigation of nested repository/worktree exclusions and failure ordering, including a relationship diagram. B02 was a source-only check of `TEST_ROOTS` and `tests/local` exclusions, with a concise note and no diagram. Both inspected source; the records do not compare research against a method that avoided source inspection.

The tasks therefore differ in substantive questions and requested deliverables. A narrower task is a plausible explanation for less time and fewer tokens. Diagram requirements, output length, input context, cache behavior, and unrecorded runtime conditions also differ or remain uncontrolled. The observations cannot isolate the effect of a simplified research method on the same complex task. They also cannot isolate a diagram's effect or establish that diagrams are wasteful.

The task summary explicitly states: "No quality assessment supplied; summaries only describe actual requested scopes." There is no evidence that B02 was more accurate, more complete, better supported, or more useful for a decision. Successful process exits and absence of timeouts do not establish research quality. Neither output length nor reasoning-token count is a quality measure. The summary reports that notes were produced; their full contents and independent assessments are not supplied in this timing evidence.

### Cost and generalization

Lower recorded token use is a resource-use observation. It is consistent with lower token charges under common positive, identical per-category rates, but actual monetary savings are unmeasured. No applicable rate card, billing breakdown, or treatment of cached and reasoning tokens is supplied. Different cache mixes further prevent treating the input-token percentage as the cost-saving percentage. Human review, corrections, follow-up work, and consequences of missed findings are also absent.

One observation per different task gives no estimate of run-to-run variability and no representative evidence across research workloads. Even a reliable latency advantage would not establish a quality advantage or justify a universal workflow change.

## Evidence

| Source | Kind and inspected content | Supports and limits |
| --- | --- | --- |
| [B01 receipt](../../../samples/timing/B01.json) | Supplied extracted execution record; all fields read | Recorded elapsed time, usage, requested configuration, exit status. No quality or billing observation. |
| [B02 receipt](../../../samples/timing/B02.json) | Supplied extracted execution record; all fields read | Same categories for the second, differently scoped task. |
| [Task summary](../../../samples/timing/task-summary.json) | Supplied scope descriptions and explicit absence of quality assessment; all fields read | Establishes scope mismatch and the quality-evidence gap; does not independently validate the produced notes. |
| [Provenance](../../../provenance.json) | Supplied provenance metadata; read locally | Records source snapshot HEAD `d5a7f0da247214bdb9c61fe90c550256432e5f76`, original receipt paths and original SHA256 values, and that receipt extraction retained factual fields without conclusions or grader output. Original receipt hashes are not hashes of these extracted JSON files. Original files and locations were not accessed or independently authenticated. |

The source snapshot revision is context, not proof that both executions used identical environments. No historical launch commands, full prompts/contexts, actual model-resolution records, or repeated execution traces are present in the timing records. A fresh execution would not recover those missing historical observations and was not attempted. No implementation claim is made that would require following repository execution paths.

## Decision impact

The proposed conclusion is not sufficiently supported. Retain the bounded observation: **B02 completed its narrower recorded assignment faster and with fewer recorded tokens than B01 completed its broader assignment.** Quality improvement, actual monetary savings, causation by workflow simplification, and suitability for broad rollout remain unresolved. These receipts may motivate a comparison; they do not justify replacing the workflow.

The minimum additional observation categories for a defensible workflow decision are:

1. **Comparable work and a defined change.** Observe both the existing and proposed methods answering the same research question with the same required coverage, source snapshot, available evidence, and acceptance criteria. Include complex tasks whose exclusions, failure paths, or interactions could be missed by a brief check. Specify what changes in the method; do not silently reduce the required outcome. Hold model/configuration and other material conditions constant, record actual execution settings and context/cache conditions, and balance or randomize order where relevant. Existing records satisfying these conditions could be used; collecting them is future work, not authorized execution here.
2. **Independent quality outcomes.** Inspect the actual outputs against a predefined rubric or reference evidence, preferably with reviewers unaware of the method. Record factual correctness, completeness of required coverage, evidence support, appropriate uncertainty, consequential omissions, and usefulness for the engineering decision. Check both methods; do not presume B01 is a gold standard. Define the acceptable quality threshold or non-inferiority margin before deciding. A claim of *better* quality needs observed superiority; acceptable quality at lower cost supports a different, narrower claim.
3. **Comparable total cost and latency.** Observe elapsed time, per-category usage, applicable billed rates or actual charges, and review/rework/follow-up effort for the same accepted outcome. Report cache conditions and corrections needed to reach acceptance. Define whether “cost” means API spend, human effort, or both. Faster initial completion alone cannot establish lower cost per correct decision.
4. **Repeatability and coverage of the rollout population.** Obtain repeated matched comparisons across representative routine and complex research tasks, recording paired differences, variability, and important failures. Choose the amount of evidence to resolve the agreed quality and cost thresholds with useful uncertainty; no defensible fixed sample size follows from these two receipts. Broad rollout needs evidence across the task classes it would affect. If benefits appear only for routine lookups, limit the change to that class and retain escalation for consequential gaps.

Together these observations distinguish “less work was requested” from “the method achieves the same required result more efficiently.” A decision rule should be set before evaluating the comparison: acceptable quality and consequential-omission rates, meaningful total-cost savings, and uncertainty small enough for the intended scope. No such comparison or decision threshold is supplied here.

## Limitations and open questions

The observed latency difference is real within the supplied records; its cause, repeatability, quality consequences, monetary value, and applicability to other work are unknown. The full outputs, quality rubric, billing, historical execution details, and representative matched observations remain missing. Provenance metadata was read, but no external originals or credentials were accessed. No assertion is made about deployment, CI, test passage, or source behavior. This investigation is concluded because the available evidence settles the support question, while the proposed workflow's effectiveness remains untested.
