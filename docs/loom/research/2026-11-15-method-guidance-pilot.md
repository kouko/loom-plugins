---
title: "Does compact method guidance preserve Loom research quality?"
type: loom-research
status: concluded
created: 2026-11-15
updated: 2026-11-15
tags: [loom/research]
---

# Does compact method guidance preserve Loom research quality?

## Question and scope

The user authorized the proposed bounded comparison: preserve outcomes, authorization, source quality, independent verification and required output contracts, while relaxing research-method guidance. This pilot tests one reference in `engineering-research`, not the whole Loom station workflow or all skill instructions. Production skill files were not edited. This is research, not a feature delivery, release, installation or merge.

Source revision: `4d44cd3ce2889c552d46ca4687596bc4f5298a17`. Executions took place on 2026-11-15 Asia/Taipei (2026-11-14 UTC). Six fresh execution agents ran sequentially without parent conversation, followed by two fresh blinded source-checking auditors sequentially. All inherited the host's default model configuration; exact model snapshot/weights and provider telemetry were unavailable, so this is not a verified exact-version-pinned model experiment. The agents are separate contexts, not independent model families.

## Method and rationale

A one-factor offline comparison is the smallest useful investigation. Baseline X is a copy of the current source skill bundle. Candidate Y changes only `references/research-methods.md`: its descriptive method table and reference list become brief outcome/evidence-selection guidance. Experimental source validation confirmed all other bundle files, including SKILL.md, trigger description, source policy, evaluation selection and template, are byte-identical. Thus the experiment does not test new triggers, a new tool, a different model, fewer reviewers or unrestricted autonomy.

The methods reference contains 575 whitespace-delimited words in X and 132 in Y: 443 fewer, about 77%. These are word counts, not tokens. The entire Markdown bundle is 6,324 versus 5,881 words; not every bundled file is necessarily loaded on each task. Shorter instruction text is a directly observed artifact property, not demonstrated runtime savings.

The [protocol](2026-11-15-method-guidance-pilot/protocol.md), case questions and adoption conditions were saved before execution. The [audit rubric](2026-11-15-method-guidance-pilot/audit-rubric.md) was saved before judging outputs. Run order was C1-X, C1-Y, C2-Y, C2-X, C3-X, C3-Y. There was one fresh execution per case-condition. Both auditors received case requirements, outputs, self-reported action trajectories and access to cited sources, but not variant instructions, mapping or each other's audit. This is a condition-blinded audit, not an independently reproduced experiment or a blinding-effectiveness test.

Primary guardrails were evidence-backed answers, no consequential unsupported conclusions or omissions, explicit source/runtime distinctions, retained limitations and authorization boundaries. Adoption required no guardrail regression and a consistent useful benefit. Original instructions already permit proportionate methods and stopping with adequate evidence; the candidate mainly removes explanatory material, rather than removing a genuinely mandatory method sequence.

## Findings

| Case | Question | Auditor one | Auditor two | Interpretation |
|---|---|---|---|---|
| C1 | What does package-suite success actually cover? | X acceptable; Y acceptable; tie | X acceptable; Y acceptable; tie | Both retained configured-root/local-exclusion and source-versus-execution distinctions |
| C2 | Does dispatch validate real risk or supplied flags? | X acceptable; Y acceptable; tie | X acceptable; Y acceptable; tie | Both traced caller assertions and mechanical precedence, without claiming tests or host behavior were verified |
| C3 | Does prior comparison justify adding JSON intake? | X acceptable; Y acceptable; Y modestly preferred | X acceptable; Y acceptable; Y modestly preferred | Both caught current-source drift; Y also inspected raw scoring and explicitly contrasted old/current schemas |

Both auditors found zero material and zero critical issues under the bounded rubric. These are two judgments of the same six outputs, not twelve independent executions. A single preferred candidate output cannot establish a stable treatment effect. No observed failure in three narrow cases is not proof of semantic equivalence or general safety.

C3 is a concrete counterexample to blindly reusing history: the old record reports a guidance-only decision, while current source already exposes optional intake JSON with a different schema. Both variants qualified the old conclusion rather than treating it as current inventory. This pilot records that discrepancy; it does not repair historical records or alter the interface.

No network, installations, production edits or tests were reported by the executors. Auditors checked source-backed outputs and trajectory consistency, not a complete independently captured action log. Absence of an authorization breach in inspected artifacts is weaker than verified universal enforcement.

### Efficiency evidence

[Metrics](2026-11-15-method-guidance-pilot/metrics.json) retain word/byte counts and executor-reported time intervals. Start boundaries differ, including two starts after orientation; do not compare those intervals as full-task latency. Tool counts use heterogeneous wrapper/nested-call conventions and are self-reported, so no reliable call-saving comparison follows. Provider tokens, fees, exact model snapshots and complete execution transcripts were unavailable.

Output word counts X/Y were C1 723/681, C2 789/848, C3 781/913; total 2,293/2,442. They are descriptive, not quality or cost scores. Shorter input guidance did not consistently yield shorter research outputs. There is no substantiated speed, cost or user-intervention improvement. Executions requested no clarification, but this small offline exercise does not measure actual user workload or downstream rework.

## Evidence

- [Protocol](2026-11-15-method-guidance-pilot/protocol.md), [manifest and condition mapping](2026-11-15-method-guidance-pilot/manifest.json), [audit rubric](2026-11-15-method-guidance-pilot/audit-rubric.md).
- [Baseline skill](2026-11-15-method-guidance-pilot/variants/X/SKILL.md), [baseline methods](2026-11-15-method-guidance-pilot/variants/X/references/research-methods.md), [candidate methods](2026-11-15-method-guidance-pilot/variants/Y/references/research-methods.md).
- C1: [question](2026-11-15-method-guidance-pilot/cases/C1.json), [X output](2026-11-15-method-guidance-pilot/runs/C1-X/research.md), [X actions](2026-11-15-method-guidance-pilot/runs/C1-X/trajectory.json), [Y output](2026-11-15-method-guidance-pilot/runs/C1-Y/research.md), [Y actions](2026-11-15-method-guidance-pilot/runs/C1-Y/trajectory.json).
- C2: [question](2026-11-15-method-guidance-pilot/cases/C2.json), [X output](2026-11-15-method-guidance-pilot/runs/C2-X/research.md), [X actions](2026-11-15-method-guidance-pilot/runs/C2-X/trajectory.json), [Y output](2026-11-15-method-guidance-pilot/runs/C2-Y/research.md), [Y actions](2026-11-15-method-guidance-pilot/runs/C2-Y/trajectory.json).
- C3: [question](2026-11-15-method-guidance-pilot/cases/C3.json), [X output](2026-11-15-method-guidance-pilot/runs/C3-X/research.md), [X actions](2026-11-15-method-guidance-pilot/runs/C3-X/trajectory.json), [Y output](2026-11-15-method-guidance-pilot/runs/C3-Y/research.md), [Y actions](2026-11-15-method-guidance-pilot/runs/C3-Y/trajectory.json).
- [Independent audit one](2026-11-15-method-guidance-pilot/audit-one.md), [independent audit two](2026-11-15-method-guidance-pilot/audit-two.md). Both inspect actual implementation and historical records rather than relying solely on output format.

## Decision impact

Agent-decided: retain production unchanged and preserve the candidate as experimental evidence. The pilot supports a narrower statement: this one reference could be much shorter without a material quality issue observed in these three source-inspection cases. It does not meet the predeclared requirement of a consistent useful benefit sufficient for adoption.

Keeping the current version incurs no integration or publication work and is supported by the inconclusive improvement result. The smaller candidate remains available for later validation if there is a demonstrated burden. Combining this change with better data access or broader station simplification now would confound the one-factor comparison and introduce untested changes. No automatic expansion, skill installation or publishing is authorized by these findings.

The previous suggestion to test compact guidance remains useful, but no recommendation to replace the skill is supported. A later decision would require repeated fresh runs and broader tasks where methods may matter (diagnosis, feasibility, quantitative comparisons and failure/uncertainty), with comparable external timing and cost telemetry if efficiency is claimed. These are limits on inference, not a proposed automatic next project.

## Verification, delivery status and limitations

The orchestrator validated the single-file bundle difference, recomputed word counts and totals, parsed all trajectory JSON, read substantive audit reports and sampled research results, and checked local link targets. Both auditors independently source-checked all six results; audit two reports 64 resolvable output links. Findings are bounded to these retained artifacts and source revision. No package suite was run because production behavior did not change; no test passing claim follows.

Required installed-host delivery observation was run after the experiment with `/Users/kouko/.codex/plugins/cache/loom/loom-code/3.81.0/scripts/loom-python --ready delivery --json`: exit 1, state `unconfirmed`, reason `cannot identify a committed change`, complete false. This research has no committed confirmed implementation intent. The observation is retained as unconfirmed software delivery, not converted into a research failure or a release claim. The local research experiment is complete; publication, installation and software delivery have not been performed or confirmed.

Limitations: three related source-inspection tasks, one execution per condition, no randomized/repeated representative workload, inherited rather than verified pinned model version, same-family auditors with correlated blind spots, no trigger or live-host test, self-reported trajectories rather than complete independent transcripts, unequal timing boundaries and missing cost telemetry. The candidate was authored by the investigator; independent judging reduces but does not eliminate author/task-selection bias. The audits did not read variant instructions, so their verdicts establish output quality under the shared rubric, not exhaustive instruction equivalence. No general claim about fewer skills, more autonomous agents or all Loom stations is established.
