# Remove expert-mode and its typed skip confirmation
originator: kouko
kind: engineering
needs-design: no — removes one skill, its typed confirmation and the checker, hook and prose that serve it; the remaining plain-words skip route and its record line already exist; the existing acceptance report gains one section, with no new state or refusal
evidence: [loom-code/skills/expert-mode/SKILL.md]
status: confirmed 2026-10-01
publication: automatic — authorized 2026-10-01 by kouko

## Problem
Loom offers two ways to skip a step: saying so in plain words, or the expert-mode command, which asks the user to type a generated four-character code. Since plain-words skipping arrived, the command's only remaining effect is a label: a skip of reviewers, the package suite or the adversarial step shows `valid (skipped: …)` instead of `absent`, and neither label blocks CI or merging. It was used in 3 of 67 changes, all within five days of its release, and it works fully only in an attended Claude Code session, partly on Codex and not at all on Antigravity CLI. Maintainers carry it in about 300 references across 50 files, about 2,000 lines of dedicated tests, hooks on four hosts and a checker module, and users meet a second, longer route that behaves differently per host. Once it is gone, the plain-words route keeps the only record of a skip, and the user does not see those skips when accepting the change.

## Proposed outcome
Plain words are the only way to skip a loom step, on every host. expert-mode and everything that exists only to serve its typed confirmation are gone. Each plain-words skip stays recorded as the user's instruction, and the user sees every skip before accepting the change.

## Acceptance
1. expert-mode is no longer offered on Claude Code, Codex, Antigravity CLI or OpenCode, as a skill or as a command.
2. A user can still skip any of the eight steps in plain words with the same outcome as before: reviewers, package suite and adversarial skips leave the change unattested and disclosed as `absent`; the other five lose nothing.
3. No loom skill, hook, checker command or rule, README, CHANGELOG-current section or standing loom doc still offers expert-mode or a typed skip confirmation code.
4. Pull requests and merges of changes made after the removal show the same verification statuses as today for runs without a typed confirmation.
5. Every step skipped in plain words before Ship is recorded on the change's branch as skipped by the user's instruction, with its date, and a spec or plan skip recorded that way still waives the spec or plan.
6. When the user is asked to accept a change, the acceptance test report lists every step skipped by the user's instruction; when acceptance testing itself was skipped, the user is told the skipped steps in the conversation instead.
7. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.

## Constraints
- Skip records already stored on users' machines are left in place, not deleted.
- The automatic narrow-change simplification stays as it is.

## Out of scope
- Making a plain-words skip of reviewers, the package suite or the adversarial step produce an attestation.
- Refusing publication when the pull request body omits or misstates a skip record.
- Rewriting dated change folders under docs/loom that mention expert-mode.

## Open questions
- none
