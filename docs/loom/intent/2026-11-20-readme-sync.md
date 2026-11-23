# Bring the plugin READMEs back in sync
originator: kouko
kind: engineering
needs-design: no — documentation and skill wording only; no interface surface (cli/api/commands/tsx/templates) is touched
evidence: []
status: confirmed 2026-11-21
publication: automatic — authorized 2026-11-21 by kouko
intent_confirmed_sha: d568cf5

## Problem
The 2026-11-20 terminology audit found loom-code's Japanese and Traditional Chinese READMEs far shorter than the English one: they lack the checker section's suggested-next-step, delivery and JSON result material. loom-workflow's three READMEs say "Old maps remain readable" without saying a map is the decision map that roadmap replaced. Readers of the translations get less, and all readers meet an undefined word.

## Proposed outcome
Each plugin's three READMEs carry the same sections and facts, and no README uses an undefined term for a retired feature.

## Acceptance
1. loom-code's README.ja.md and README.zh-TW.md carry every section and fact of README.md, translated.
2. loom-workflow's three READMEs say what an "old map" is (a decision map from before roadmap replaced it) on first use.
3. The complete package suite passes.

## Constraints
- Version strings stay synchronized with each plugin.json; changed plugins get a version bump and CHANGELOG entry per the repository's release rule.

## Out of scope
- Per-skill README translations that do not exist yet.
- Wording changes inside skills (separate change).

## Open questions
- none
