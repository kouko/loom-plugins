---
title: Recommendation evidence and record drift in the dotfiles RAR-to-ZIP session
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags:
  - loom/research
---

# Recommendation evidence and record drift

## Question and scope

Why did the latest dotfiles discussion recommend Python ZIP creation, then
recommend all-7-Zip after a challenge, without a comparative assessment? Are the
dimensions and steps subsequently described already present in Loom?

Scope: local historical transcript, retained research, installed loom-code
3.66.0, installed loom-workflow 5.21.0, and this checkout at
248d5272ac71ff2926f1fc675db4884f1e589f4d. This is standalone research, not work
on the unrelated flaky-discovery change currently selected by the checkout.
No runtime skill, test, setting or original dotfiles record was changed.

## Method and rationale

Hypothesis-driven diagnosis using actual conversation/tool receipts, followed
by a contract-to-behavior and coverage comparison. This distinguishes missing
guidance, missing loading, incomplete application, stale records and checker
scope. Inspecting local artifacts answers the historical question; external
framework research or rerunning a compression benchmark would not explain this
trajectory. No new model runs or third-party requests were made for diagnosis.
Stop after locating the demonstrated failures and the limits of existing checks;
do not claim a proposed repair works without a controlled behavioral trial.

## Findings

### Historical observations

The session is `01a1cb50-9c99-7a22-8699-b91d49a79335`, started on November 11
at 23:53 Taipei time. Its final substantive answer was recorded by 00:04 on
November 12. JSONL line numbers below refer to the original transcript, not an
exported subset. Sources are identified in Evidence.

| Observation | Evidence | Interpretation |
|---|---|---|
| The skill was actually read | Transcript lines 18–20; historical command output equals the installed main SKILL.md | Not simply a failure to select the skill |
| The evaluation reference was requested and relevant rules reached the tool result | Lines 29, 31, 34 contain the common-criteria paragraph, supported-conclusion section and material-tradeoff requirement | Missing comparison cannot be explained solely by an absent reference |
| The initial study compared completion callback versus polling | Retained record, Method and rationale and Findings; transcript 54 | Legitimate comparison at one decision level |
| The same record selected 7-Zip extraction plus Python ZIP creation without comparing ZIP creation alternatives | Retained record, Findings; transcript 61 | Support for the integration trigger was not support for the nested tool choice |
| A challenge immediately reversed the recommendation | User line 68; answer line 72 | No intervening source/tool call or new comparative observation supports the reversal |
| Later explanation correctly limits all-7-Zip to a candidate | Answer line 100 | Conversational correction is real; it does not retroactively validate the earlier recommendation |
| The saved record still recommends Python ZIP creation | Current dotfiles record matches the substantive initial content; no later patch appears in the transcript | The durable recommendation did not follow the conversation |

The reference-loading tool result was truncated: the combined call exceeded its
output budgets. However the returned result still includes the common-criteria,
fact/inference separation and material-tradeoff paragraphs. Truncation is an
observed exposure risk, not an isolated cause. Neither command execution nor
visible returned text proves the model attended to every requirement.

### Competing explanations

| Hypothesis | Assessment | Reason |
|---|---|---|
| Loom has no method for comparing alternatives | Contradicted | The installed evaluation reference explicitly specifies it |
| The agent never loaded the method | Contradicted in that broad form | Actual calls and returned applicable text exist; attention is unobservable |
| Rules were added only after the incident | Contradicted for the relevant rules | They are in the historical main/reference outputs before the first answer |
| All choices were evaluated because one comparison table existed | Contradicted | Trigger selection and ZIP creation are independent choices with different evidence |
| Follow-up treated a preference as decisive evidence | Supported as a behavioral description | Tool count was used to reverse the recommendation without a new comparison |
| Model agreement pressure, overload or truncation caused the failure | Unresolved causal hypotheses | No controlled comparison isolates these explanations |
| Skipping capture-intent caused this failure | Unsupported | Standalone research is explicitly allowed; no implementation was requested |

### Are the eight dimensions present?

These ratings describe research-stage guidance, not guaranteed execution or an
exact eight-item checklist. The evaluation reference explicitly chooses relevant
dimensions by project and rejects mandatory application of every framework.

| Session dimension | Coverage in research guidance | Actual boundary |
|---|---|---|
| Function and compatibility | Explicit general coverage | Premise/version checks and compatibility analysis; multipart/Unicode/empty-directory checks must be derived for this archive task |
| Data integrity | Explicit general coverage | Invariants, loss and consistency appear in migration analysis; archive content/metadata equivalence is not a bundled archive checklist |
| Failure and recovery | Explicit | Failure propagation, detection, containment and recovery; disk-full/interruption/retry examples remain task-specific |
| Security | Explicit | Assets, actors, flows, trust boundaries and controls; archive traversal/link handling must be concretized |
| Performance and resources | Explicit | Profiling, resource saturation, representative workload and matched benchmarking |
| Integration and maintenance cost | General/partial | Common criteria and focused code-health/complexity/change-impact inspection; no universal total-cost formula or tool-count rule |
| Testability and diagnosis | General/partial | Correct/testable design and hypothesis-driven diagnosis; no requirement to enumerate logging/operational diagnosis as a separate dimension in every comparison |
| Deployment and replacement cost | General/partial | Version/environment, migration and release guidance; packaging/installation/vendor-replacement cost is not a universal required comparison row |

Later code review also examines architecture, security, correctness, tests and
simplification. That supports implementation review, not a claim that every
research answer already assessed all eight dimensions. A source supporting that
7-Zip can pack ZIP establishes capability, not superiority over Python zipfile.
No full ISO standard was inspected or compliance established in this diagnosis.

### Are the five steps present?

| Session step | Existing instruction | Coverage |
|---|---|---|
| Establish non-negotiable conditions | Evaluation reference, Frame the decision: distinguish mandatory constraints from preferences and exclude failures | Explicit |
| Keep credible alternatives | Research methods, Trade study; evaluation reference, lightweight trade study, including current/smaller/postponed/combined approaches | Explicit |
| Identify unknowns that could change the choice | Main skill steps 1–3 and evaluation framing | Explicit |
| Obtain the smallest useful verification | Main skill step 3 and methods experiment rules | Explicit but conditional; no mandatory runtime experiment if adequate source evidence answers the question |
| Retain the conclusion and change-of-choice conditions | Evaluation reference, Form a supported conclusion; template, Decision impact; retained-record continuation rule | Explicit |

The session's five-step explanation is a useful synthesis, not a fixed sequence
required by Loom. The missing behavior is applying existing guidance to each
material recommendation, and maintaining the answer when the question changes.

### What existing verification can and cannot establish

- The package test module identifies itself as portable package invariants,
  not proof of agent behavior. It checks resources, metadata, links, ownership
  and station references. It does not inspect a conversation's recommendations.
- The framework trial did test real alternative assessment (C02) and unsupported
  evidence (C04/C06). Its report says old and new versions achieved the same
  substantive outcomes; it does not establish an improvement from added prose.
  The inspected six-case execution corpus does not contain a follow-up challenge
  that reverses a recommendation and then checks saved-record consistency.
- Earlier code-owned dogfood already reported failures to follow explicit
  verification instructions. That is relevant counterevidence to assuming more
  prose necessarily fixes compliance, not proof of this incident's model cause.
- The contract registers engineering-research as a nonstation capability; research
  Markdown falls under the docs artifact mapping. The checker rule registry has
  no dedicated research recommendation/evidence or conversation-sync rule.
- The delivery observer resolves a committed change, confirmed intent and Git/PR
  state. It does not compare a research answer with its source evidence. A generic
  delivery result is neither an endorsement nor rejection of this research's
  conclusion. Later docs review could flag unsupported or inconsistent claims if
  such a document enters a reviewed change; it did not intervene here.

## Evidence

All sources below were inspected locally. Historical outputs were parsed as
JSON rather than inferring reads from assistant declarations. Line references
identify the relevant original spans; no private transcript was sent externally.

- Historical transcript: `/Users/kouko/.codex/sessions/2026/11/11/rollout-2026-11-11T23-53-40-01a1cb50-9c99-7a22-8699-b91d49a79335.jsonl`.
  Source class: conversation, command receipts and returned tool results.
  Main instruction read: 18–20; reference call/output: 29–34; record write/read:
  54 onward; recommendation: 61; challenge/reversal: 68/72; qualification: 100;
  Loom explanation: 125. Raw local session path is retained instead of copying
  unrelated private context into this report.
- Original retained record: `/Users/kouko/dotfiles/docs/loom/research/2026-11-11-rar-to-zip.md`.
  Read in full; Findings preserves the Python ZIP recommendation. Source class:
  actual artifact, not proof of compression execution.
- [Main research contract](../../../loom-code/skills/engineering-research/SKILL.md),
  steps 1–5, evaluation selection, retained records, return to owning task.
  At the inspected baseline, the local file matched installed 3.66.0; the
  historical main command output also matched those installed bytes. Later
  implementation changes are outside that historical comparison.
- [Evaluation selection](../../../loom-code/skills/engineering-research/references/evaluation-selection.md),
  Frame the decision, question table and Form a supported conclusion.
- [Research methods](../../../loom-code/skills/engineering-research/references/research-methods.md)
  and [record template](../../../loom-code/skills/engineering-research/templates/research.md).
- [Package invariants](../../../loom-code/tests/engineering-research/test_package.py)
  and [routing corpus](../../../loom-code/tests/engineering-research/routing-corpus.json).
  The latter explicitly labels expectations as inputs, `run_status: not-run`;
  it is not an observed activation result.
- [Framework trial report](../../skill-dogfood/2026-11-08-engineering-research-frameworks/report.md)
  and [actual case definitions](../../skill-dogfood/2026-11-08-engineering-research-frameworks/execution/cases.json).
  Results are attributed historical trial evidence; no new actors were run.
- [Code-owned dogfood report](../../skill-dogfood/2026-11-08-code-owned-engineering-research/report.md),
  especially saved-content verification findings and causal limitations.
- [Formal acceptance report](../2026-11-08-engineering-research-skill/acceptance-test-report.md),
  items 2–5 and 9: bounded tested behavior and explicit activation/host limits.
- [Contract manifest](../../../loom-code/contract/manifest.yaml), tools and
  artifact_types; [checker rules](../../../loom-code/scripts/loom_checker/rules.py);
  [delivery implementation](../../../loom-code/scripts/loom_checker/command_handlers/publish.py),
  observe_delivery; [session routing](../../../loom-code/hooks/session-start),
  research/notes direct-work boundary; [review lenses](../../../loom-code/skills/closing-review/references/lenses.md),
  code dimensions and docs incorrect-fact/inconsistency.

## Decision impact

The strongest diagnosis is a demonstrated application and record-maintenance
failure with a bounded verification gap, not a missing evaluation-method catalog.
The internal cognitive cause remains unknown. A defensible answer in the original
case would retain both ZIP implementations as candidates, give supported
tradeoffs, and identify which unknown warrants a small check. It need not run a
full benchmark or all eight dimensions before offering a conditional candidate.

| Improvement option | Expected benefit | Cost/limit |
|---|---|---|
| Leave rules unchanged and defer | No added workflow or instruction cost | Demonstrated failure remains unaddressed |
| Add another mandatory dimension checklist | Makes omissions easier to notice | Duplicates existing guidance; no evidence it fixes unsupported reversals |
| Test a minimal recommendation-and-update procedure (recommended first) | Directly targets nested decisions, justified reversals and saved-record consistency | Effectiveness still needs a bounded behavioral comparison |
| Add semantic review for every research recommendation | Potential independent detection before delivery | More latency/cost and orchestration; necessity not yet established |

The smaller version is one multi-turn case plus a simple-fact negative control.
Compare current instructions with a concise procedure: identify the material
choice, distinguish capability from comparative advantage, justify any reversal,
and update the matching record or explicitly retain the uncertainty. Use the
same initial task and follow-up, not an answer that tells the actor the expected
tool. Check actual evidence, final answer and saved file; measure added work as
well as correctness. A challenge must be allowed to produce either a justified
change or a reasoned non-change. Combining this procedure with independent review
is possible if residual failures justify the cost. These are research proposals,
not an implemented fix or a confirmed implementation plan.

## Limitations and open questions

One installed-session incident does not establish a failure rate or model ranking.
The prior trial reports cover different prompts/environments and do not substitute
for a current controlled multi-turn test. No new behavioral trial, full package
suite, archive conversion, upstream compression audit or external framework
verification was run. Installed reference behavior was checked against historical
returned text; attention and the counterfactual effect of truncation are unknown.
The original conversation's final mapping is directionally correct, but its
"Loom has the method" conclusion alone does not explain enforcement or upkeep.

Verification: the saved report was read back in full and its relative Markdown
file targets were resolved from this directory. External raw paths were checked
for existence. This report contains analysis only; delivery readiness for a
software change is reported separately and does not certify the research.
