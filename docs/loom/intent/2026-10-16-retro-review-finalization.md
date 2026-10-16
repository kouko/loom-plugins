# Finish verification of recovered retrospectives
originator: kouko
kind: engineering
needs-design: no — this repairs review evidence and test metadata without changing the retrospective behavior or a user-facing interface
status: confirmed 2026-10-16
publication: automatic — authorized 2026-10-16 by kouko

## Problem

The confirmed retrospective rename has been restored from local edit records, but its review cannot finish. The previous review episode reached its limit, and finalization rejects a graduated test whose concern is not declared where the checker expects it. The two new skills therefore remain unavailable through a verified pull request.

## Proposed outcome

The recovered retrospective change is independently verified on its actual committed content and available as a Ready pull request for acceptance.

## Acceptance

1. The recovered project and skill retrospectives retain their confirmed names, scopes, and proposal-only behavior.
2. The complete declared package suite and finalization checks pass on the committed change, producing review evidence bound to that content.
3. A Ready pull request presents the acceptance results and verification status without merging the change.

## Constraints

- Keep the confirmed `project-retro` and `skill-retro` behavior and migration contract.
- Do not treat reviews of the lost temporary Git object as reviews of the recovered commit.
- Do not merge without a separate user decision.

## Out of scope

- New retrospective features or changes to the two skills' improvement targets.
- Direct modification of projects, skills, plugins, or connectors by either retrospective.

## Open questions

- none
