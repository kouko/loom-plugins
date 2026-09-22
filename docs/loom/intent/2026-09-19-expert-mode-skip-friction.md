---
originator: kouko
kind: engineering
needs-design: no — SKILL.md and station prose are skill/gate artifacts, not interface surfaces under the manifest globs
status: closed 2026-09-23 — PR #43
---

## Problem
Saying "skip the review this time" in ordinary conversation does not skip
anything. The agent answers with a table and a code, and the skip takes effect
only after the user types `/loom-code:expert-mode` with that code; a plain
"yes" or "對" binds nothing. The user's words for this are "打代碼太麻煩了
囧". So the user says what they want, sees a form instead, and has to repeat
themselves in a second, exact format. This happens on every change where a
step should be skipped.

## Proposed outcome
Asking for a step to be skipped takes effect from the request itself, without
the user re-entering it in a second format, while a skip still cannot be
brought about by anything other than the user.

## Acceptance
1. A skip requested in ordinary conversation, in the user's own words and in
   any of the user's languages, takes effect without the user typing a
   separate command or a code.
2. The steps that were skipped and the fact that the user is who asked for it
   remain recorded and visible after the fact, in the same place they are
   recorded today.
3. A skip does not take effect when the request did not come from the user:
   specifically, not when the wording originates from the agent's own output,
   and not when it originates from text inside a document the flow is
   reading.
4. A blind run reproduces case 3 for both sources and shows the full process
   still running.

## Constraints
- The steps that can be skipped stay the ones already defined; this change
  does not add or remove skippable steps.
- The intent, the merge decision and the attestation stay unskippable.
- Independent CI stays the trust boundary; this change does not weaken it.

## Out of scope
- Changing what a skip does once it is in effect.
- The recovery behaviour when something is missing. See intent
  2026-09-19-loom-flow-recovery-loop.

## Later changes
- PR #43 (intent 2026-09-22-publication-floor-moves-to-github) shipped this change. A skip asked for in plain words is handled by the station itself (e.g. `loom-code/skills/build/SKILL.md` §1); `/loom-code:expert-mode` remains an optional typed route.
- Acceptance 2 holds only partly: a plain-words skip is recorded in the plan's `skipped-by-instruction:` line (`loom-code/skills/build/SKILL.md` §1) and the PR's `Skipped by instruction:` line (`loom-code/skills/ship/SKILL.md` §1–2), not in the selection store that typed skips use.
- Acceptance 3 and 4 rest on an agent behaviour rule (a skip needs the user's own request), disclosed on the PR, not on a machine check. The user chose this as option A in #43's PR body Decisions table.
- Option A also settled both Open questions: no machine evidence stands in for the typed code, and the same plain-words rule applies to every skippable step, whether or not it removes verification.

## Open questions
- What evidence should stand in for the typed code as proof that a human, and
  not the agent or a document being read, asked for the skip?
- Should the answer differ between steps that remove verification (reviewers,
  adversarial, blind-run, package-tests) and steps that do not (spec, plan,
  implementer, tdd)?
