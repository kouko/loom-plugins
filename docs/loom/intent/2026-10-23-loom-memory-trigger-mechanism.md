---
originator: kouko
kind: engineering
needs-design: no — internal documentation/rules change; no user-visible surface
status: open
---

# Record loom-memory automatic triggering mechanism

## Problem

loom-memory has only two passive triggers: (1) the user explicitly says ``remember this`` or similar, and (2) the agent independently judges a discovery is worth retaining. The user's analysis showed that two PRs involving loom-memory never triggered because ``walking to a workflow step`` is explicitly not a trigger condition — there are no automatic trigger points in the flow. The user wants a mechanism to actively decide when a durable lesson is worth recording during loom flow execution, without manual user prompting each time.

## Proposed outcome

A mechanism exists in the loom flow that actively decides whether a durable lesson is worth recording at defined boundaries (e.g., after finalize-review, or after ship). Lessons that qualify are recorded to ``docs/loom/memory/`` with ``Decision:``/``Learning:``/``Gotcha:`` trailers and a regenerated index, so future contributors can recall them by default. Lessons that do not qualify are silently omitted. The mechanism records why a lesson was or was not recorded.

## Acceptance

1. The loom flow contains at least one new checkpoint where a ``Decision:``/``Learning:``/``Gotcha:`` trailer may be earned and recorded to ``docs/loom/memory/``.
2. The index.md of ``docs/loom/memory/`` is regenerated to include any newly recorded entries.
3. The mechanism does not break any existing flow: existing behaviour is unchanged when the mechanism decides not to record.
4. The mechanism records the rationale (``Decision:``) for both recording and non-recording.

## Constraints

- The mechanism must not require manual user prompting each time a lesson is earned.
- The mechanism must not alter any existing functional content or test results.
- The mechanism must only activate at defined flow boundaries already present in the loom 1.0 stations.
- The mechanism may not cite any internal ``file:line`` paths from sibling plugins (repo contract citations rule).

## Out of scope

- The mechanism does not change how loom-memory is invoked outside the defined flow boundaries (it still only activates on explicit user request or independent agent judgement outside the flow).
- No new product user-visible behaviour is added.
- No DESIGN.md or PRINCIPLES.md is required for this engineering change.

## Open questions

1. Which loom station boundary should host the checkpoint (e.g., after finalize-review, after ship, or another point)?
2. What precise criteria should the checkpoint use to decide whether a lesson is worth recording (Decision:, Learning:, Gotcha:)?
3. How should the checklist of criteria be phrased so an agent can evaluate it without reading the full change history?