# Close the small follow-ups left by the expert-mode change
originator: kouko
kind: engineering
needs-design: no — documentation, a principles signature and removal of an unused contract field; no surface a user reads or types into changes behaviour
status: confirmed 2026-09-15
publication: automatic — authorized 2026-09-15 by kouko

## Problem
The expert-mode change (PR #13) shipped with four small loose ends:

- `PRINCIPLES.md` non-negotiable 2 carries an amendment that is still marked
  `pending-ratification:`; the principles the checker enforces are therefore
  partly unsigned.
- The expert-mode skill and `loom-code/CHANGELOG.md` say that a confirmation
  and finalization must happen in the same Claude Code session, but
  publication is bound to that session too, and a new session must re-run
  `selection propose` before the user confirms again. A user who publishes
  from a new session hits an unexplained refusal.
- The loom-code READMEs (English, Japanese, Traditional Chinese) still show
  version 3.1.4 while the release is 3.4.0.
- `step_selection` in the contract manifest keeps a `requires:` field on every
  step, and `validate_selection` keeps a dependency loop, but after the intent
  was removed no step depends on another; the mechanism has no real user.

## Proposed outcome
The amendment is signed, the session limit is documented completely, the
READMEs show the current version, and the unused dependency mechanism is gone,
with expert-mode behaving exactly as it does today.

## Acceptance
1. `PRINCIPLES.md` records kouko's dated signature for the non-negotiable 2 amendment, and no `pending-ratification:` line remains.
2. The expert-mode skill and the loom-code CHANGELOG state that confirmation, finalization and publication must happen in the same Claude Code session, and that a new session re-runs the proposal before the user confirms again.
3. The English, Japanese and Traditional Chinese loom-code READMEs show the current release version.
4. The step selection contract carries no dependency field, and `selection propose` still refuses an unknown step name and the intent.
5. The repository's package tests and mechanism checks pass.

## Constraints
- The amendment text is signed as merged in PR #13; its wording does not change.
- Expert-mode's observable behaviour does not change.

## Out of scope
- Generating a short intent from the user's words when they ask to skip it.
- Verifying or hardening nested Codex sessions.
- Expert-mode support on Antigravity CLI.

## Open questions
- none
