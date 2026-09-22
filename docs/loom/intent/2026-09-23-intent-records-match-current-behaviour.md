# Make intent records match what the code does after the publication-floor change
originator: kouko
kind: engineering
needs-design: no — status lines and notes in internal intent records only
status: confirmed 2026-09-23
publication: automatic — authorized 2026-09-23 by kouko

## Problem
After PR #43 moved the publication floor to GitHub, several intent records in
`docs/loom/intent/` no longer describe what the code does. One intent still
reads `status: open` although #43 shipped it, and five confirmed intents
promise blocking or typed-code behaviour that #43 deliberately removed, with
nothing in them saying so. Anyone asking "what is still left to build in
loom" is misled — on 2026-09-23 an audit reported the shipped intent as the
only open work item. One more intent's Constraints describe a branch delta
that the shipped mechanism deliberately does not use.

## Proposed outcome
Every intent record either still holds as written, or says plainly which of
its lines a later change replaced and where that decision is recorded, so the
intent store can be read as an accurate list of open and done work.

## Acceptance
1. `docs/loom/intent/2026-09-19-expert-mode-skip-friction.md` no longer reads `status: open`; it reads closed with PR #43, and notes that its Acceptance 3 and 4 rest on an agent behaviour rule rather than a machine check, as #43 recorded.
2. Each of these five intents carries a note naming PR #43, the Acceptance lines it replaced, and what the behaviour is now: `2026-09-14-expert-mode-step-selection`, `2026-09-14-land-merged-changes`, `2026-09-14-antigravity-cli-compatibility`, `2026-09-18-blocked-publish-names-the-legal-routes`, `2026-09-19-publication-hook-false-positives`.
3. `docs/loom/intent/2026-09-20-mechanical-calculations.md` carries a note that the shipped branch delta counts committed paths only, and why.
4. No intent file in `docs/loom/intent/` reads `status: open`.
5. The loom checker's `intent` command passes on every edited intent file.

## Constraints
- Existing wording of each intent stays as it was confirmed; changes are added notes plus the one status line in Acceptance 1.
- Exception, user-decided 2026-09-23: `2026-09-19-publication-hook-false-positives` never carried the required schema fields, so it also gains an `originator:` line and an `## Out of scope` section, and its `needs-design: no` line gains a reason, so that Acceptance 5 can hold.
- This PR bumps the plugin version per the repository's versioning rule.

## Out of scope
- Changing any code, skill text, or behaviour.
- Applying GitHub rules to this repository.
- Other open items (PR #35, contract-citation debt, the two skill-structure checkers).

## Open questions
- none
