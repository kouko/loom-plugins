# Record the lesson from an adversarial probe that could not see its own defect — plan
intent: 2026-09-20-adversarial-probe-self-referential-blind-spot@8452eb70
charter: 1.0

## Current State Evidence
- Forward: `docs/loom/memory/README.md` "Format — one fact per file" section states the required frontmatter (name/description/type/sources) and body shape (fact, Why, How to apply) the new entry must follow.
- Reverse: `loom-workflow/skills/loom-memory/scripts/loom_memory.py validate` checks frontmatter shape only; no test asserts the truth of an entry's content.
- Error: before this change, no entry in `docs/loom/memory/` names a probe dodging its own population or deselecting its refuting cases (checked by grep across the store for `deselect`, `vacuous`, `population`).
- Data: `docs/loom/2026-09-18-modular-adversary-recipes/evidence/probes/test_modular_recipes_abuse.py:30-47,120-127` — the fixed probe's own docstring describes each original defect while explaining its fix.
- Boundary: one new file under `docs/loom/memory/` plus a regenerated `index.md`; no probe, recipe, or checker script changes.

## Task DAG

**W1-01 Add the memory entry and regenerate the index**  after: none  acceptance: 1, 2, 3, 4, 5, 6
- Files: docs/loom/memory/an-adversarial-probe-can-go-green-by-excluding-what-would-refute-it.md, docs/loom/memory/index.md
- Test: A1 positive: loom-memory-validate-ok; negative: missing-required-frontmatter-field. A2 positive: description-is-tool-agnostic; negative: description-names-a-specific-function. A3 positive: body-names-both-manifestations-and-blind-run-catch; negative: body-omits-blind-run-catch-method. A4 positive: sources-cites-9bf87029-pr33; negative: sources-empty. A5 positive: loom_memory-validate-exit-0; boundary: index-drift-before-regeneration. A6 positive: full-package-suite-exit-0; negative: any-non-zero-exit-blocks-hand-off.
- Risk: This entry is documentation-only, drafted before Build by the orchestrator itself rather than dispatched to an implementer, since there is no code path to write a failing test against. agent-decided.

## Questions asked
① — what — 我把這件事寫成了一條 intent……這樣的理解對嗎？

## Risks
1. PR #33 squash-merged, so the two original defects are not independently re-derivable from history; both are corroborated by the shipped probe's own docstring describing its fix, and by the confirming user's first-hand blind-run account.
