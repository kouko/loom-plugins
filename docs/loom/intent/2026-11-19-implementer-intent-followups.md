# Implementer intent hand-off: close the review follow-ups
originator: kouko
kind: engineering
needs-design: no — internal agent dispatch contract, station guidance and their tests; no interface surface (cli/api/commands/tsx/templates) is touched
evidence: [docs/loom/intent/2026-11-19-implementer-reads-intent.md]
status: confirmed 2026-11-19
publication: automatic — authorized 2026-11-19 by kouko
intent_confirmed_sha: 67165e8

## Problem
PR #169 told the implementer to read the confirmed intent, but its reviews left gaps. Build, the station that dispatches implementers, names the intent path only when the plan is skipped; on the ordinary planned path it says only "retained artifact paths", so whether the intent arrives depends on the dispatcher reading the implementer's own input template. The implementer is told to report beyond-task work under `DONE_WITH_CONCERNS` but not where to write it, its read-only input list omits the intent, its scope sentence forbids committing extra work rather than doing it, and its existing outside-file exception can be read as permission for intent-suggested work. One test's built-in counter-example deletes the sentence it guards, so it shows nothing a weakened rewrite would do. These were raised by two Claude reviewers and an independent Codex audit of PR #169.

## Proposed outcome
On both dispatch paths Build explicitly hands every implementer the confirmed intent path, and the implementer's instructions say unambiguously that intent-suggested work beyond its task is left undone and described in its report, without loosening any existing scope rule.

## Acceptance
1. Build's instructions name the confirmed intent path as an input of every implementer dispatch, on the planned path as well as the skipped-plan path, and a repository test fails when either path's mention is removed.
2. The implementer's instructions say beyond-task work the intent suggests is not done and is described in `self_review` under status `DONE_WITH_CONCERNS`.
3. The implementer's read-only input list includes the intent.
4. The implementer's outside-file exception states that it covers only edits the assigned task itself requires.
5. The scope-sentence test rejects a weakened rewrite of that sentence, not only its deletion, and the complete package suite passes with the change.

## Constraints
- Task scope stays bounded by the task's own files and Acceptance lines (arXiv 2605.18583), as in the parent intent.
- loom-code's version is bumped and its CHANGELOG updated per the repository's release rule.

## Out of scope
- Matching the implementer's whole input block line by line in tests (the Codex audit's remaining suggestion): it would break on every ordinary rewording.
- Capturing and checking a real dispatched packet at runtime.
- Any change to what the adversary, reviewers or acceptance tester receive.

## Open questions
- none
