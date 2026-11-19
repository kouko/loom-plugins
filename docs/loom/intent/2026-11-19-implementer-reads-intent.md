# Implementer reads the confirmed intent
originator: kouko
kind: engineering
needs-design: no — internal agent dispatch contract and its test; no interface surface (cli/api/commands/tsx/templates) is touched
status: confirmed 2026-11-19
intent_confirmed_sha: 8974e66
publication: automatic — authorized 2026-11-19 by kouko

## Problem
During Build, the agent that writes the code for each task receives the plan, the spec when one exists, and its own task, but is never pointed at the confirmed intent, which holds the change's problem and wanted outcome. Every agent that judges the work (the adversary, the closing reviewers, the acceptance tester) does read the intent. The writer therefore works from a narrow task statement while its judges work from the goal. No recorded incident in this repository shows harm from this yet; the gap was found by comparing what each agent receives, and outside evidence reports that adding the desired behaviour and its motivation to an agent's task statement raises resolution rates (arXiv 2608.27831).

## Proposed outcome
Every implementer dispatched during Build knows where the confirmed intent is and is told to read it for the change's goal, while its own task still bounds what it changes.

## Acceptance
1. When Build dispatches an implementer for a plan task, the implementer's input names the confirmed intent's path alongside the plan path, and the implementer's instructions tell it to read the intent to understand the change's goal.
2. The implementer's instructions state that the intent does not widen its task: it changes only what its own task covers, and reports work the intent suggests beyond its task instead of doing it.
3. When the plan is skipped, the implementer still receives the intent and a bounded task exactly as it does today.
4. A repository test fails when the intent path is removed from the implementer's input or the scope sentence is removed, and the complete package suite passes with the change.

## Constraints
- Task scope stays bounded by the task's own files and Acceptance lines; outside evidence shows agents overstep more when explicit scope text is removed (arXiv 2605.18583).
- loom-code's version is bumped and its CHANGELOG updated per the repository's release rule.

## Out of scope
- Measuring the effect on implementer output quality with a with/without trial.
- Any change to what the adversary, reviewers, or acceptance tester receive.
- Recording the user's literal request, asking what a request is ultimately for, or recording a practitioner's method (options B and C of the same review).

## Open questions
- none
