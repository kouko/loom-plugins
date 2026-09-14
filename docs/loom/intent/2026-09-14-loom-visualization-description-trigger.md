# Trigger loom-visualization when Loom stations report to the user, by description only
originator: kouko
kind: engineering
needs-design: no — rewords one skill description; no user interface surface and no multi-state behaviour
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
When a Loom station talks to the user — restating an intent, laying out
choices that are expensive to undo, or reporting blind-run results — the agent
usually answers in prose or its own ad-hoc tables and seldom invokes
`loom-visualization`. The skill's description says what it can draw but names
no moment when it should be used, so nothing points the agent at it during
those station messages. The user wants those messages to use the skill as much
as possible without adding hooks, station rules, or other mechanisms.

## Proposed outcome
`loom-visualization`'s description alone names Loom station messages to the
user as a time to use the skill, and a before/after behavioural comparison
shows whether that wording actually makes the agent invoke it more often.

## Acceptance
1. The `loom-visualization` description names Loom stations reporting to the user as a use case, and the repository's description budget checks pass.
2. A before/after comparison runs the same fixed set of Loom station reporting prompts in fresh sessions with only the Loom plugins enabled, once with the current description and once with the new one, and reports how many sessions invoked `loom-visualization` in each.
3. The new description ships only if its sessions invoke `loom-visualization` more often than the current description's; otherwise the description stays unchanged and the report says so.
4. The shipped description is word-for-word the one that ran in the comparison.
5. The repository's package test suite passes.

## Constraints
- Only the `loom-visualization` description text changes; no hook, no Loom station skill text, and no trigger card changes.
- The accepted overlap between the loom-visualization and ascii-graph trigger cards stays as it is (user-decided 2026-09-14).
- Committed artifacts stay in English.

## Out of scope
- Loom station skill files, hooks, and the session-start trigger cards.
- The ascii-graph-toolkit plugin and its card.
- Diagram rules for committed specs, plans, and pull requests.

## Open questions
- none
