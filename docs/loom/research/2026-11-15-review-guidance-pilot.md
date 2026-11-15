---
title: "Can compact guidance preserve document-review behavior?"
type: loom-research
status: concluded
created: 2026-11-15
updated: 2026-11-15
tags: [loom/research]
---

# Can compact guidance preserve document-review behavior?

## Question and scope

The user authorized testing another Loom stage after the [method-guidance pilot](2026-11-15-method-guidance-pilot.md). This stage tests document-review instructions: can a shorter reviewer contract retain evidence-backed defect detection and avoid unfounded findings? It does not alter production, test code review, replace the whole closing-review station or publish a skill.

Source revision: `4d44cd3ce2889c552d46ca4687596bc4f5298a17`. Prior work remains intact: six research executions and two independent audits. This stage adds six document-review executions and two independent adjudications. Cumulative series count is **12 executor contexts and 4 auditor contexts**, across two different bounded experiments; these are not interchangeable samples for a single quality statistic. No counters, failures or previous conclusions were reset.

## Method and rationale

The [protocol](2026-11-15-review-guidance-pilot/protocol.md), [oracle](2026-11-15-review-guidance-pilot/oracle.json) and [audit rubric](2026-11-15-review-guidance-pilot/audit-rubric.md) were retained before execution. Baseline X is current `loom-code/agents/reviewer.md`. Candidate Y compresses reconciliation exposition and replaces the duplicated lens-dimension table and prescribed reading order with concise evidence obligations and freedom to choose inspection order. [Exact candidate diff](2026-11-15-review-guidance-pilot/candidate.diff).

Reviewer text decreases from 1,541 to 1,327 whitespace-delimited words: 214 fewer, about 14%. The shared 2,491-word lens reference remains unchanged, so this is not a 14% reduction of every instruction the reviewer reads. Severity thresholds, shared dimension definitions, no-edit responsibility, output schema, style caps and fix-round sections remain present. This does not prove whole-contract equivalence, particularly in untested lenses and handoffs.

Three real reports from the previous pilot were copied with relative links rebased. R1 changes one source-inspection statement into an unsupported successful-execution claim. R2 reverses a non-authorization clause into permission to remove a current shared interface. R3 is an unchanged clean control, meaning no defect was planted; auditors could still report a legitimate unplanted problem. These are controlled mutations, not organically discovered bugs or representative defect prevalence. Their explicit internal contradictions make detection easier than a subtle, internally consistent error.

Each case-condition ran once in a fresh context without parent conversation. Run order was R1-Y, R1-X, R2-X, R2-Y, R3-Y, R3-X, sequentially. Reviewers did not receive the oracle, condition mapping, other variant, or other outputs. Two fresh auditors then independently read every result, the shared rules, oracle and actual sources, without variant mapping or each other's judgments. They inherited the same host model configuration; exact model snapshots were not independently pinned, and same-family blind spots remain possible. There is no repeated/randomized causal effect estimate.

The offline adapter is identical for both conditions: `reviewed_sha` is an explicitly labeled real snapshot digest, not a Git commit; supplied base/delta files replace `git show` and a committed diff. Writing only the assigned review result/trajectory is authorized, while target and sources remain read-only. No branch-end target, attestation or production gate is claimed. This tests review reasoning through a snapshot harness, not native closing-review delivery end to end.

## Findings

### Defect detection and false-positive findings

| Case | Baseline X | Candidate Y | Both independent auditors confirm |
|---|---|---|---|
| R1: unsupported execution claim | One important inconsistency; PASS_WITH_NOTES | One important inconsistency; PASS_WITH_NOTES | Both identify the planted claim and give an anchored concrete repair |
| R2: unauthorized interface-removal instruction | One fatal inconsistency; NEEDS_REVISION | One fatal inconsistency; NEEDS_REVISION | Both identify the authorization reversal and supported consequence |
| R3: unchanged report | No findings; PASS | No findings; PASS | Neither invents a target defect; substantive source claims are supported |

Both conditions detected the two unique planted issues. No independently established important/fatal false-positive target finding was identified in either control output. This is two positive cases and one control per condition, not a general recall/precision estimate. Four detection events are the same two seeded defects seen under two conditions, not four independent defects.

All outputs contain six docs dimensions, echo the correct supplied snapshot identity, and have parseable YAML. The four findings have exact anchors, concrete fixes and permitted opening labels. Finding-count severity arithmetic matches the returned verdicts. These mechanical checks do **not** establish whether a dimension's PASS is semantically warranted.

### Material disagreement about qualification scores

The auditors agree on all substantive target findings but disagree on review-output compliance:

| Question | Auditor one | Auditor two | Retained conclusion |
|---|---|---|---|
| R1-Y and both R3 reviews pass incorrect-fact while disclosing unchecked historical identity/provenance | Material issue: the express rejection rule forbids bare PASS on an unchecked dimension | Acceptable calibration: substantive source conclusions do not depend on authenticating that historical Git identity | Applicability of the qualification rule remains disputed; do not call these outputs unconditionally compliant |
| Pair preference | R1 X; R2 tie; R3 tie (both R3 outputs share the issue) | R1 tie; R2 tie; R3 tie | No demonstrated candidate advantage under either interpretation |

Auditor one's proposed correction is to qualify `incorrect-fact` as PASS_WITH_NOTES and, in R3, qualify the overall result without inventing a target defect. Auditor two argues that disclosure is sufficient because the checked source-behavior conclusions do not rest on historical identity authentication. Neither argues the historical identifier is demonstrated false or that the reviewers fabricated an execution.

This is a disagreement about whether the pass actually rests on an unchecked claim, not a YAML parsing failure or a missed seed. It is preserved rather than averaged away. Under the stricter interpretation the candidate has one additional noncompliant output in R1; under the other interpretation all pairs tie. Both interpretations support retaining production. No extra reviewer was recruited merely to force agreement; resolving this rule-boundary question is not necessary for that conservative decision. Raw results and both audits remain unedited.

### Efficiency and authorization evidence

No token, cost, complete tool-event or comparable full-task timing instrumentation was available. No efficiency claim is made. Output lengths and self-reported call lists do not establish savings. Executors and auditors report no tests, network, installation, production edits or commits; their trajectories are self-reports, not universal technical enforcement or independent complete action logs. Fixture digests and tracked production diffs provide narrower checks that target snapshots and the two tested production files remained unchanged.

## Evidence

- [Protocol](2026-11-15-review-guidance-pilot/protocol.md), [frozen seed oracle](2026-11-15-review-guidance-pilot/oracle.json), [mapping/source manifest](2026-11-15-review-guidance-pilot/manifest.json), [audit rubric](2026-11-15-review-guidance-pilot/audit-rubric.md).
- [Baseline reviewer](2026-11-15-review-guidance-pilot/variants/X.md), [candidate reviewer](2026-11-15-review-guidance-pilot/variants/Y.md), [shared lenses](../../../loom-code/skills/closing-review/references/lenses.md).
- R1: [packet](2026-11-15-review-guidance-pilot/fixtures/R1/packet.json), [base](2026-11-15-review-guidance-pilot/fixtures/R1/base.md), [target](2026-11-15-review-guidance-pilot/fixtures/R1/target.md), [delta](2026-11-15-review-guidance-pilot/fixtures/R1/delta.diff), [requirements](2026-11-15-review-guidance-pilot/fixtures/R1/requirements.json), [X review](2026-11-15-review-guidance-pilot/runs/R1-X/review.md), [X actions](2026-11-15-review-guidance-pilot/runs/R1-X/trajectory.json), [Y review](2026-11-15-review-guidance-pilot/runs/R1-Y/review.md), [Y actions](2026-11-15-review-guidance-pilot/runs/R1-Y/trajectory.json).
- R2: [packet](2026-11-15-review-guidance-pilot/fixtures/R2/packet.json), [base](2026-11-15-review-guidance-pilot/fixtures/R2/base.md), [target](2026-11-15-review-guidance-pilot/fixtures/R2/target.md), [delta](2026-11-15-review-guidance-pilot/fixtures/R2/delta.diff), [requirements](2026-11-15-review-guidance-pilot/fixtures/R2/requirements.json), [X review](2026-11-15-review-guidance-pilot/runs/R2-X/review.md), [X actions](2026-11-15-review-guidance-pilot/runs/R2-X/trajectory.json), [Y review](2026-11-15-review-guidance-pilot/runs/R2-Y/review.md), [Y actions](2026-11-15-review-guidance-pilot/runs/R2-Y/trajectory.json).
- R3: [packet](2026-11-15-review-guidance-pilot/fixtures/R3/packet.json), [base](2026-11-15-review-guidance-pilot/fixtures/R3/base.md), [target](2026-11-15-review-guidance-pilot/fixtures/R3/target.md), [delta](2026-11-15-review-guidance-pilot/fixtures/R3/delta.diff), [requirements](2026-11-15-review-guidance-pilot/fixtures/R3/requirements.json), [X review](2026-11-15-review-guidance-pilot/runs/R3-X/review.md), [X actions](2026-11-15-review-guidance-pilot/runs/R3-X/trajectory.json), [Y review](2026-11-15-review-guidance-pilot/runs/R3-Y/review.md), [Y actions](2026-11-15-review-guidance-pilot/runs/R3-Y/trajectory.json).
- [Audit one](2026-11-15-review-guidance-pilot/audit-one.md), [audit two](2026-11-15-review-guidance-pilot/audit-two.md), [mechanical observations](2026-11-15-review-guidance-pilot/observations.json). Actual target/code anchors supporting each semantic judgment are retained in the reviews and audits.

## Decision impact

Agent-decided: keep the official reviewer and shared lenses unchanged; retain the compact candidate and all outputs as research evidence. Shorter text did not improve substantive detection in these cases. Qualification-score compliance is contested, so a claim of complete non-regression is unsupported. No useful repeatable candidate benefit or cost improvement was established.

The smaller approach tested here remains preferable to a wholesale review redesign as an investigation scope, but not yet as a production replacement. Keeping production incurs no release/integration work. Combining this candidate with fewer reviewers, different models or changed score rules would create new untested variables; it is not undertaken. The existing pilot remains concluded on its own terms rather than being rewritten to imply this stage validated it.

This stage answers the authorized request to try another part of Loom. It does not authorize changing the disputed rule, repairing source history, adopting the candidate, installing plugins, merging or expanding the experiment automatically.

## Verification and limitations

Orchestrator checks: 68 fixture links resolved before execution; snapshot digests matched packets. All six YAML results and trajectories parse, the six dimension sets and echoed identities match, and findings have anchors/fixes. The finding-count threshold calculation is correct but deliberately does not settle the qualification dispute. Final checks verify fixture target hashes against the saved oracle, candidate diff stability, local report links and tracked production-file parity. No suite was run because production code/contracts did not change. Source-backed adjudication is in two independent audits; the investigator did not substitute structural green checks for their disputed judgments.

[Delivery observation](2026-11-15-review-guidance-pilot/delivery-observation.json): installed `loom-python --ready delivery --json` returned exit 1, state unconfirmed, reason `cannot identify a committed change`, complete false. This stage has no committed confirmed software intent. The local research is complete; software delivery/publication/installation remains unperformed and unconfirmed.

Limits: one run per condition/case; three related prose reports from the previous investigator-authored pilot; two intentionally conspicuous mutations and one clean control; no code/spec/skill/plan lens, fix-round, native branch identity, attestation, trigger, runtime-host or end-to-end station test; no verified exact model snapshot or cross-vendor independence; self-reported action lists and no efficiency telemetry. The auditors share a model family and disagree on one contract boundary. No general claim that fewer instructions improve Loom or that these variants are semantically equivalent follows.
