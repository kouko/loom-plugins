# Rename the blind run to independent acceptance testing
originator: kouko
kind: engineering
needs-design: no — step id, agent name, report file name and prose in skill/gate artifacts and the contract manifest, none of them interface surfaces under the manifest globs
status: confirmed 2026-09-23
publication: automatic — authorized 2026-09-23 by kouko

## Problem
The step loom calls "blind run" has no industry meaning, and in the user's own
environment "blind" already means two other things: the independent-advisor
skill's blind judging and the dogfood-skill-testing skill's "blind behavioral
test". The user reads the internal step id directly, because pull requests
disclose skipped steps by id. "UAT" was considered and rejected: it collides
with the common "UAT environment" meaning, and it implies the user performed
the acceptance, while in loom the user accepts separately, afterwards, by
reading the report. The ISTQB definition of acceptance testing separates the
two the same way loom does — testing that lets an authorised person decide
whether to accept — and adding "independent" corrects its default that the
intended users perform it.

## Proposed outcome
The step is called independent acceptance testing everywhere a person or an
agent reads about it, its identifiers carry the same name, and the old name
survives only in records of changes that are already merged.

## Acceptance
1. The step id is `acceptance-test`, the agent is dispatched as `loom-code:acceptance-tester`, and the report is written at `docs/loom/<change-id>/acceptance-test-report.md` from a template of the same name.
2. No runtime file, identifier, test fixture or current-version documentation names `blind-run`, `blind-runner`, `blind run` or `blind runner`; only frozen records of merged changes and past CHANGELOG entries keep the old name.
3. Text the user reads — the three READMEs, PRINCIPLES.md, station prose and the pull-request lines that list skipped steps — names the step "independent acceptance testing" on first use and never "UAT".
4. A plain-words request to skip "acceptance testing", or the old "blind run", maps onto the renamed step.
5. Attestations and reports of merged changes are left as they are, and nothing that runs afterwards fails on them.
6. A check fails the repository if one of the old names reappears in a runtime file.

## Constraints
- No behaviour changes: the step runs when and as it runs today.
- The checker's rule list does not change.
- This is a minor version bump, because identifiers change.
- Changing PRINCIPLES.md wording is an amendment the user ratifies.

## Out of scope
- Making acceptance testing faster or its report shorter (a separate change).
- Rewriting records of merged changes.
- Other repositories' in-flight changes, beyond noting the rename in the release notes.

## Open questions
- none
