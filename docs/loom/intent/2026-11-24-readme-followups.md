# Resolve README follow-ups from PR #176
originator: kouko
kind: engineering
needs-design: no — documentation wording and release metadata only
evidence: []
status: confirmed 2026-11-24

## Problem
PR #176 left five non-blocking follow-ups: repeated sentences in loom-code's Japanese and Traditional Chinese READMEs, a loom-code CHANGELOG entry that omits the English README correction, an escaped em-dash in loom-workflow's manifest description, and translation sentences the English README lacks.

## Proposed outcome
loom-code's three READMEs state the same checker facts without repeats; changelogs and manifests are accurate.

## Acceptance
1. The three loom-code READMEs carry the same checker facts and no repeated paragraph.
2. loom-workflow's manifest description uses a literal em-dash.
3. The complete package suite passes.

## Constraints
- skipped-by-instruction: spec, plan, implementer, tdd, acceptance-test, reviewers, adversarial 2026-11-24 — the user asked to fix the follow-ups and open the PR once one independent review passed.

## Out of scope
Any code or skill behaviour.

## Open questions
None
