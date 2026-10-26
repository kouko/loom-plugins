# Resolve five confirmed skill/checker consistency defects
change_id: 2026-10-26-five-skill-consistency-defects
originator: kouko
kind: engineering
needs-design: no — skill and checker contract repairs; no user interface surface
evidence: [
  docs/loom/2026-10-26-five-skill-consistency-defects/evidence/first-review-packet.md,
  docs/loom/2026-10-26-five-skill-consistency-defects/evidence/first-review-result.json,
  docs/loom/2026-10-26-five-skill-consistency-defects/evidence/second-review-result.md
]
status: confirmed 2026-10-26
publication: automatic — authorized 2026-10-26 by kouko

## Problem

Five places in the Loom skills contradict their own enforcing code or procedures. An agent that follows the skill literally can be refused by the closing-review finalization step, left with no adversarial program to record and no compliant way forward, routed to a memory operation whose trigger does not apply to its case, or shown template examples that the page verifier would reject. In one further place the documented command spelling is narrower than the checker actually accepts. Each of the five was surfaced by an independent external review and confirmed by a second fresh-context reviewer; all five are verified against the current source.

## Proposed outcome

The five skill/checker disagreements are resolved so the prose and the enforcing code accept the same behavior: an agent can complete finalization for every outcome the adversarial protocol permits, reuse and ceiling counting agree, every recorded memory lesson has one defined outcome, templates match the separator shape the verifier requires, and the documented probe command spelling matches what the checker accepts.

## Acceptance

1. A change that survives every adversarial attack and has no covering repository test can complete finalize-review without the user skipping the adversarial step, and the recorded adversarial evidence names the no-program outcome and its reason.
2. The adversarial ceiling stated in the skill prose and the ceiling enforced by finalize-review count the same set of programs, so reusing an existing program never overflows the five-program ceiling and never produces a refusal the prose says cannot happen.
3. Recording a lesson that an existing memory entry already states produces exactly one defined outcome and never a second entry for the same subject, and the skill and its operations reference name that outcome identically.
4. Every loom-visualization chat template that draws a node-label separator uses exactly six U+2501 characters, and the page verifier accepts a page built from each changed template.
5. A pytest-style adversarial probe recorded with any supported Python invocation (for example `python3 -m pytest`) is accepted by finalize-review, and one recorded as a direct `python3 <artifact>` run is still refused; the adversarial protocol states that acceptance instead of one literal spelling.
6. The complete package suite passes, and both affected plugins land synchronized minor version bumps with CHANGELOG entries.

## Constraints

- No rule is weakened to make a contradiction disappear: where the checker is the authority (the probe command form and the ceiling count), the prose follows the code; where the prose is the authority (the adversarial minimum and the memory reconcile trigger), the enforcement follows the intended behavior.
- The repair to the adversarial minimum adds no subcommand and no configuration surface — at most one optional field on the finalize-review adversarial input record.
- Repo policy applies: minor version bump (station guidance and contract changes) for each affected plugin, with CHANGELOG entry, README version strings, and pinned release tests updated in the same change; `scripts/run_package_tests.py --loom-family` must pass.
- Skill folders stay flat; runtime prose must not cite this repo's `docs/` records.
- Template edits change only the separator and heading shape, nothing else.

## Out of scope

- The sixteen findings that two independent reviews rejected as scope errors from the earlier consistency pass.
- The local Claude gateway environment (`ANTHROPIC_BASE_URL`) that blocked one external-review leg — unrelated to this change.
- Any redesign of the closing-review adversarial protocol beyond the two named conflicts.
- Any widening of which templates must follow page-mode rules; this change only normalizes what the templates already present as node labels.

## Open questions

- none
