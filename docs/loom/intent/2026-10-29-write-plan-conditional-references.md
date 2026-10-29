# write-plan keeps conditional paths out of its always-read body
originator: kouko
kind: engineering
needs-design: no — station prose moves between files; no CLI, API or template surface changes
status: confirmed 2026-10-29
publication: automatic — authorized 2026-10-29 by kouko

## Problem
`loom-code/skills/write-plan/SKILL.md` has 3749 body words against the 3750-word cap that the 2026-09-16 rule-text consolidation set (long rule text makes agents miss rules). Every change that has to add a sentence to write-plan must first cut one elsewhere; PR #118 had to drop two restated sentences to fit. About 1300 of those words, Step 1's no-intent interview (~600) and Step 4's self-written spec path (~716), only apply when loom-design is not installed, yet every write-plan run reads them.

## Proposed outcome
write-plan's always-read body carries only what every run needs; the two loom-design-absent paths live in `references/` and are read only when that condition holds, with every rule they state unchanged.

## Acceptance
1. write-plan's SKILL.md body is at most 2800 words, under an unchanged 3750-word cap.
2. A run without loom-design still reaches the no-intent interview and the self-written minimal spec path, and each rule those paths state today is still stated, with the same meaning, in the file the run is sent to.
3. A run with loom-design installed is not told to read either moved file.
4. Every existing check that pins those rules still runs and passes against the file that now holds them.

## Constraints
- The 3750-word cap is not raised.
- Rule wording moves, it is not compressed or rephrased; a sentence changes only where a cross-reference has to.

## Out of scope
- Word counts of other stations.
- Rewording or adding any rule.

## Open questions
- none
