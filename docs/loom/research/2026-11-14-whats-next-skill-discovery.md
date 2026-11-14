---
title: "Bounded next-action advice: portable research summary"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-15
tags: [loom/research]
---

# Bounded next-action advice: portable research summary

## Question and scope

Does recurring next-action advice justify an independent skill, and how should
it differ from orientation, continuation and predictive prompt suggestions?
This is a sanitized summary of a consented local requirements study of one
user's retained coding conversations. Private source records remain outside
the repository; this document carries no transcript excerpts or private
locators. Its aggregate historical observations cannot be independently
recomputed from the public repository and are not current runtime test results.

## Method and bounded counts

The retained-message cutoff was 2026-11-14T15:09:18Z. The study considered
observable user and assistant messages from Codex, Claude Code and OpenCode,
excluding hidden reasoning, tool outputs, generated/subagent sessions, the
study itself and long pasted candidates. A lexical pass found 73 candidates;
seven quoted voice-delta matches and one irrelevant linked title were removed,
leaving 65 requests across 31 host/session pairs. Three fresh-context analysis
batches covered 9, 11 and 11 sessions; each selected request was adjudicated
once. A separate reader checked the synthesis. Finite phrase families and
unavailable/deleted records limit recall; this is no exhaustive census.

| Host | Clear advice requests | Other selected requests |
|---|---:|---:|
| Codex | 48 | 11 |
| Claude Code | 2 | 2 |
| OpenCode | 0 | 2 |

The 50 clear advice requests span 26 sessions from 2026-08-23 through
2026-11-14 UTC. The selected set begins on 2026-01-12 because older continuation
cases are included. The other 15 comprise three continuations, two orientation
requests, three execution instructions, four CLI-advice discussions, one
ambiguous advice/execution request, one advice/orientation mixture and one
superseded advice request. OpenCode's two selected cases concern continuation,
not a request for a recommendation menu.

## Findings and boundaries

Recurring advice supports a real job: select a small action that advances the
current goal and explain the uncertainty it resolves. Historical observations
also motivate checking premises against recent corrections, preserving the
actual project over incidental tooling work, retaining existing authorization,
and allowing a completed goal to stop. Frequency and positive uptake establish
neither effectiveness nor satisfaction. Historical execution, installation and
test claims were not independently verified by message-only analysis.

`recap-state` retains orientation and its confirmation pause; `critique`
evaluates an existing proposal; `decision-map` owns an explicitly selected
persistent map; `handoff` owns cross-session state. Advice adds no execution
authority and requires no recurring global history scan. An authorized action
continues through its existing owner; new scope, cost, disclosure and merge
remain subject to that owner's consent boundaries.

## Public reference inspected

The community next-steps plugin was inspected statically at revision
`163301d1904c0a994539f5226ce0fcd65b8652bf`, metadata version 1.0.0:

- [README](https://github.com/anthropics/claude-plugins-community/blob/163301d1904c0a994539f5226ce0fcd65b8652bf/next-steps/README.md)
  describes predictive terminal suggestions that fill a draft rather than
  submitting it.
- [Hook implementation](https://github.com/anthropics/claude-plugins-community/blob/163301d1904c0a994539f5226ce0fcd65b8652bf/next-steps/hooks/register.tsx)
  shows turn gating, a background fork, up to three predictions, stale-result
  handling and conditional command validation. Command-list failure does not
  establish that suggested commands exist. No SDK or terminal UI was exercised.
- [Plugin metadata](https://github.com/anthropics/claude-plugins-community/blob/163301d1904c0a994539f5226ce0fcd65b8652bf/next-steps/.claude-plugin/plugin.json)
  declares MIT while the [root license](https://github.com/anthropics/claude-plugins-community/blob/163301d1904c0a994539f5226ce0fcd65b8652bf/LICENSE)
  is Apache-2.0. No implementation was copied; applicable reuse licensing was
  not determined.

Transferable ideas include concrete context-specific actions, verified command
availability, optional editable prompts and permission to suggest nothing.
Predicting likely prompts differs from recommending valuable work. Background
calls, terminal controls and author-reported cost benefits do not establish
compatibility, measured cost or effectiveness for Loom.

Choice-count research also gives no universal menu size:
[Scheibehenne et al. (2010)](https://doi.org/10.1086/651235) reports a near-zero
mean choice-overload effect with substantial variation;
[Chernev et al. (2015)](https://doi.org/10.1016/j.jcps.2014.08.002) identifies
moderating conditions. These consumer-choice studies do not validate a coding
skill's output policy.

## Confirmed design and present validation

On 2026-11-15 the user confirmed an independent skill named `whats-next`, one
recommendation plus necessary alternatives, natural-language use and bounded
proactive reconsideration when blockers or new evidence invalidate direction.
Viable authorized plans should proceed without repeated advice interruptions.
The confirmed [intent](../intent/2026-11-15-whats-next.md) and
[specification](../2026-11-15-whats-next/spec.md) own the implementation scope.
This later confirmation supersedes the original research-stage pending decision;
the study alone supplied no implementation or publication authorization.

Alternatives included ordinary answering, extending recap-state and predictive
terminal integration. Ordinary answering remains the comparison baseline;
orientation's unconditional pause and terminal integration's host/call costs
make them materially different. The first implementation adds instructions and
discovery, without a hook, persistent queue, dispatcher or command wrapper.

Current synthetic [behavior cases](../../../loom-workflow/tests/whats-next/behavior_cases.json)
and [selection queries](../../../loom-workflow/tests/whats-next/trigger_queries.json)
are separate from the historical study. The matched
[comparison](../2026-11-15-whats-next/evidence/comparison.json) reports one native
sample per arm in eight frozen scenarios, graded with source labels withheld:
loaded skill 8/8, ordinary answer 7/8. The 12.5 percentage-point difference falls
below the 15-point comparison threshold. One strict judgment about explicit
observation-versus-cause separation accounts for the difference. This small
pilot establishes no stable superiority or installed-host triggering reliability;
cases and negative results remain unchanged. Description-only selection is a
separate test from loaded output quality.
