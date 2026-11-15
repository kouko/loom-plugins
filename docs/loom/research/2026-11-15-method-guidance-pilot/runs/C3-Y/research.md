---
title: "Should planning intake add JSON to reduce orchestration overhead?"
type: loom-research
status: concluded
created: 2026-11-15
updated: 2026-11-15
tags:
  - loom/research
---

# Should planning intake add JSON to reduce orchestration overhead?

## Question and scope

Do not add a new JSON planning-intake interface on the strength of the recorded comparison. Guided text already met the bounded consumption need, and no incremental JSON benefit was observed. Current source also already exposes optional intake JSON; therefore the historical claim that the final interface is text-only does not describe this checkout.

Scope: offline reuse of project evidence and focused source inspection at HEAD `4d44cd3ce2889c552d46ca4687596bc4f5298a17`. Conditions set before substantive inspection: (1) require comparable consumption evidence to justify extra format/maintenance surface; (2) require actual model-turn/token/cost/end-to-end measurements for a general overhead claim; (3) inspect the current entry point and handler before assuming the historical capability still applies. No model, external service, installation or test execution is authorized or necessary here.

## Method and rationale

A lightweight comparison reusing the existing controlled trial answers the adoption question; connected source inspection checks applicability to this revision. Criteria are correct intake interpretation, preserved confirmation/downstream authority, incremental consumption benefit, maintenance surface and measured orchestration cost. Local records suffice; external search or rerunning consumers would not repair the original trial's design limits. Stop after locating the comparison, scoring, final historical acceptance and present entry/handler/output path.

## Findings

- **Supported within the historical trial:** guided text and JSON produced equivalent decisions across six controlled cases: five real CLI cases and one injected partial-output crash control. One fresh consumer saw text, guidance, then JSON sequentially; prior guidance could influence JSON. The [scoring](../../../../2026-11-11-intake-observation-pilot/evidence/consumer-scoring.json) records five of five real-case completeness resolutions for both guided text and JSON, versus three for text alone; the other two text answers were justified unknowns, not errors. All arms shared an overstatement about crash completion; safe recovery does not establish how many checks ran.
- **Supported historical cost, not token cost:** [comparison](../../../../2026-11-11-intake-observation-pilot/evidence/comparison.md#recorded-collection-results) records packets of 1,765 text, 2,236 guided-text and 2,681 JSON bytes. JSON minus guidance is 445 bytes. Bytes include serialization and question text. The historical repaired candidate added net 42 handler lines and 73 implementer-owned test lines, with additional help/adversary surface. These are historical maintenance costs, not the cost of the present implementation.
- **Historical adoption:** the [acceptance evidence](../../../../2026-11-11-intake-observation-pilot/evidence/acceptance-test-evidence.md#3-comparison-integrity-and-adopted-choice--re-tested) describes the guidance-only final repair and preservation of original answers, plus a later final-scope acceptance rerun. This supersedes the earlier candidate's partly finding for that historical tree; it does not validate today's checkout.
- **Current applicability correction:** [CLI main](../../../../../../loom-code/scripts/loom_checker.py#L576) recognizes final `--json` for intake, constructs a result, passes it to the handler, serializes it, and maps usage/internal failures to error results. [cmd_intake](../../../../../../loom-code/scripts/loom_checker/command_handlers/intake.py#L29) calls `check_confirmed` first and immediately reports/returns on failures; later checks are conditional on station, intent and skip records. [report_result](../../../../../../loom-code/scripts/loom_checker/preparation_output.py#L22) fills status/diagnostics and preserves exit 0/1 behavior. Thus optional JSON is already implemented in current source; this is a static capability observation, not a runtime pass. Its schema differs from the old pilot: current `new_result` has schema_version/command/status/diagnostics/notices/error/suggested_next, rather than the old candidate's state/checks_complete/failures contract. The old experiment is not a direct benchmark of this implementation.
- **Unresolved:** whether today's optional format reduces orchestration overhead for an actual caller. Neither present source nor the historical comparison supplies model-token use, parent turns, end-to-end latency or monetary savings. Single ordered local CLI durations cannot establish a causal format benefit.

## Evidence

The [initial architectural assessment](../../../2026-11-11-recursive-decision-models-for-loom.md) and [input-evidence research](../../../2026-11-11-mechanical-decision-input-evidence.md) supplied orientation and historical scope. Directly inspected comparison, semantic scoring and acceptance record corroborate the bounded no-benefit selection. Their measurements are reused reported historical observations, not freshly executed results. Current source citations above identify the implementation and connected path read at the stated HEAD. [Current planning guidance](../../../../../../loom-code/skills/write-plan/SKILL.md#L238) still explains text exits, early confirmation blockers, unknown crash completion, changed-input reruns and downstream authority boundaries.

Actual actions: read assigned skill/method/source/evaluation/template files and case; read the two starting research records, comparison, acceptance, scoring, handler and renderer; search/read CLI routing and planning guidance; obtain HEAD with `git rev-parse HEAD`. An initial search named two nonexistent CLI module paths; those errors were followed by reading the actual `loom-code/scripts/loom_checker.py`. No check execution, replay or performance measurement was performed.

## Decision impact

The smaller alternative, existing text plus guidance, already answered the trial's consumption questions without a new output contract. Keeping ordinary text requires no new interface work. Adding another format or claiming that JSON saves overhead is unsupported by these results; deterministic fields alone are not measured benefit. Existing optional JSON may serve an actual machine caller, but that caller and its need are not established here. Do not remove today's JSON merely because a different historical candidate failed its adoption condition: removal and current compatibility costs were not evaluated.

Reconsider an overhead-driven change only when a concrete caller/workload exposes a gap and comparable current-format evidence demonstrates useful benefit while retaining correctness, error/unknown handling and authority boundaries. This is a condition for revisiting the decision, not authorization for a new experiment or implementation.

## Limitations and open questions

The trial is one sequential consumer, not randomized independent samples, a general accuracy benchmark or representative cross-host workload. It supports the original no-benefit choice, not universal superiority of text. Current JSON was source-inspected only; runtime behavior, deployment, host consumption, introduction history and compatibility obligations remain unverified. No external links in historical research were followed and no external architectural claim is adopted here. UTC activity times and observable actions are retained in trajectory.json. No claim of efficiency savings or current acceptance is made.
