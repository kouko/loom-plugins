---
title: "Do two timing receipts justify replacing complex research with brief lookup?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Do two timing receipts justify replacing complex research with brief lookup?

## Question and scope

Do the supplied B01/B02 receipts support the claim that replacing complex research with brief file lookup improves research quality, reduces cost, and warrants a universal workflow change? If not, what minimum observations would support a decision?

This assessment uses only the supplied timing receipts, actual-scope summary, provenance, and invoked skill resources, as available on 2026-11-08. There is no active change. The supplied `src/` is a minimal source snapshot, not a complete checkout or execution record. No repository behavior, deployment, or CI result is evaluated here. No models, tests, experiments, network requests, or external sources were run or consulted. Recommendations for future observations below are not observations already collected or authorization to collect them.

## Method and rationale

Direct artifact inspection establishes what the receipts actually report. A controlled-comparison adequacy assessment then checks whether those observations identify a workflow effect. This fits the consequential gap: the proposed decision is causal and general, whereas the evidence consists of two unmatched historical tasks. Relevant criteria are completion of the same required work, evidence accuracy and coverage, decision usefulness, elapsed time, and total cost through an acceptable result. Faster completion cannot compensate for missing required evidence.

The approach follows the bundled [research methods](../../../skill/engineering-research/references/research-methods.md), [source policy](../../../skill/engineering-research/references/source-policy.md), and [evaluation selection](../../../skill/engineering-research/references/evaluation-selection.md), using the [research template](../../../skill/engineering-research/templates/research.md). No diagram or source-code investigation is needed to assess this timing inference. Stop once the supported comparison and consequential missing observations are clear; additional unrelated repository inspection would not recover missing quality or cost data.

## Findings

**The proposed conclusion is not sufficiently supported.** The evidence establishes that B02 took less recorded elapsed time and used fewer recorded tokens for its different, narrower task. It does not establish better quality, actual monetary savings, a causal benefit of brief lookup for equivalent work, or suitability for a universal change.

| Recorded field | B01 | B02 |
| --- | --- | --- |
| Requested model / provider / effort | gpt-6.1-sol / openai / medium | gpt-6.1-sol / openai / medium |
| Elapsed seconds | 103.188 | 42.637 |
| Exit code / timed out | 0 / false | 0 / false |
| Input tokens | 177,820 | 116,861 |
| Cached input tokens | 148,352 | 92,544 |
| Cache-write input tokens | 0 | 0 |
| Output tokens | 4,249 | 1,359 |
| Reasoning output tokens | 134 | 15 |

Derived arithmetic from the recorded values: B02's elapsed time is 60.551 seconds lower, approximately 58.7% lower than B01. These are descriptive differences between these two runs, not an estimated treatment effect. Token categories are preserved as supplied; reasoning output is not assumed to be an additional separately billable quantity.

The [actual-scope summary](../../../samples/timing/task-summary.json) describes:

- **B01:** source-only investigation of nested repository/worktree exclusions and failure ordering, with a relationship diagram; produced a package-runner-exclusions note.
- **B02:** source-only check of `TEST_ROOTS` and `tests/local` exclusions, with a concise note and no diagram; produced a package-test-roots note.

These are different questions and deliverables. B02 is not documented as completing B01's full requirements using a changed workflow. Both are source-only tasks; calling one “complex research” and the other “brief lookup” does not establish a controlled intervention. Different scope and deliverable requirements are direct alternative explanations for the resource difference. The records do not isolate any effect of a diagram, note length, or research method. Similar requested model settings do not resolve these confounds or prove identical actual execution conditions.

The summary explicitly states that no quality assessment is supplied. Neither exit code 0 nor absence of timeout establishes correctness, completeness, traceable evidence, useful decisions, or successful fulfillment of the requested scope. Fewer tokens and less elapsed time are resource observations, not quality assessments. A shorter answer could be sufficient or could omit necessary investigation; these data do not distinguish the possibilities.

No billed charges, applicable rates, complete billing semantics, or review/rework costs are supplied. Lower token counts are compatible with lower model usage cost under appropriate common billing conditions, but actual monetary savings and total cost per acceptable research result remain unmeasured. Cache composition differs, so token totals alone are not monetary totals. One run per different task provides no estimate of repeatability or variation and no basis for extrapolation to all research.

## Evidence

| Critical claim | Inspected evidence and support type | Verification limits |
| --- | --- | --- |
| B02 has lower reported elapsed time and token counts | [B01 receipt](../../../samples/timing/B01.json) and [B02 receipt](../../../samples/timing/B02.json); supplied historical runtime-record extracts, read in full | Historical commands, raw execution traces, hardware/load, order, cache preparation, and actual served configuration are absent. No rerun was performed. |
| Tasks differ in required scope and deliverables | [task-summary.json](../../../samples/timing/task-summary.json); supplied description of actual work, read in full | Not a matched-work experiment; full prompts and complete output artifacts are not supplied in the timing evidence. |
| Quality is not assessed | Explicit `quality_assessment` field in [task-summary.json](../../../samples/timing/task-summary.json) | No independent rubric results, correctness checks, or downstream outcomes are available. |
| Receipt provenance is bounded | [provenance.json](../../../provenance.json), read in full; supplied provenance metadata | Lists original receipt paths and SHA256 values and says only factual receipt fields were extracted, excluding conclusions/grader output. Original receipt bytes are unavailable here; their hashes were not independently verified. Extracts must not be claimed to match the original-file hashes. |
| Repository context is not runtime validation | [provenance.json](../../../provenance.json) records original source commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`, file hashes, and remote freshness “not checked” | Metadata does not show that the timing runs used a complete identical environment, nor establish CI/deployment success. The recorded external repository path was not accessed. Source-file hashes were not needed or verified for this inference. |

Local inspection used `cat` to read the listed evidence and bundled guidance. An `rg --files docs samples` path inventory reported that `docs/` did not yet exist and listed the supplied sample paths; unrelated migration artifacts were not used as quality evidence. The note is a new retained record. No historical execution command is available to report; the receipt measurements are attributed historical observations, not measurements made in this investigation.

## Decision impact

Do not use this pair as evidence for a universal replacement. It supports only the bounded statement: “For the two supplied runs with different scopes, B02 completed with lower recorded elapsed time and token counts; quality and actual cost differences are unknown.” It can motivate a future comparison, but does not establish that complex questions can be answered adequately by reducing their investigation scope.

The minimum decision-relevant observations missing are:

| Missing observation | Minimum useful evidence and why it changes the decision |
| --- | --- |
| Equivalent required work under both approaches | Paired outcomes on the same questions, source snapshots, available evidence, and acceptance requirements, with the workflow difference explicitly defined. Record full prompts, delivered artifacts, actual configuration, and relevant execution conditions. This distinguishes doing equivalent work more efficiently from doing less work. |
| Research quality on that work | Inspect both complete artifacts against a common, predefined task-specific rubric: factual correctness, evidence traceability, coverage of required cases/failure paths, justified uncertainty, and usefulness for the pending decision. Use an independent reviewer or a blinded review where practical. Record omissions and consequential wrong decisions as well as successes. “Better quality” requires demonstrated improvement; merely meeting a non-inferiority threshold would support only preserved quality. |
| Repeatable latency and full cost at acceptable quality | Repeated matched observations with run order and cache conditions controlled or recorded; retain elapsed time, usage categories, actual charges or validated applicable billing, and human review/rework/retry effort through an acceptable result. Compare variability and cost per accepted result, not just the first successful process exit. This separates a stable benefit from run noise, cache effects, or costs shifted into later correction. |
| Coverage of the intended rollout population | Include both routine lookups and representative complex tasks, especially nested interactions, failure ordering, and uncertainty that might require deeper investigation. Report effects and failure rates by task class. A favorable result for simple lookups cannot justify changing every research task. |

Before such a comparison, define quality guardrails, acceptable cost/latency tradeoffs, and the smallest meaningful improvement for the intended decision. The required number of independent tasks and repeats depends on observed variation, acceptable uncertainty, and consequences of missed evidence; these receipts cannot justify a fixed sample size or confidence claim. One matched pair would address the immediate scope confound but would still not justify universal adoption. Repeating one task many times would not establish coverage across task types.

A limited change for a well-defined task class could be supported by repeated evidence that it meets all required quality guardrails at lower total cost. A claim of improved quality needs a measured quality improvement. Broader replacement needs comparable evidence across its intended scope and an explicit way to retain deeper investigation when required evidence is unresolved. A quality regression or higher correction cost would reverse the recommendation even if first-pass latency fell.

## Limitations and open questions

Actual comparative quality, billed savings, downstream rework, execution-condition equivalence, and the effect of workflow independent of task scope remain unknown. No full outputs or quality judgments were reconstructed from task titles or unrelated samples. Selection of these two runs may be unrepresentative; no sampling protocol is supplied. The historical receipt extraction cannot recover missing original commands or measurements. This investigation is concluded because the available evidence is sufficient to reject the proposed inference as unsupported, while the underlying question of which workflow performs better remains unresolved. No process change was implemented.
