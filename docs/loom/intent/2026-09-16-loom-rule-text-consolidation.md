# Consolidate loom rule text without changing what the flow does
originator: kouko
kind: engineering
needs-design: no — this edits skill, agent, and reference prose, one link checker, and their tests; no command, output format, or interface surface a user types into changes
evidence: [docs/loom/2026-09-16-loom-rule-text-consolidation/evidence/rule-audit.md]
status: confirmed 2026-09-16
publication: automatic — authorized 2026-09-16 by kouko

## Problem
The loom rule files that agents read on every change have grown by accretion.
An audit of main at dec4e927 found 19 places where one rule file contradicts
another or points at something that no longer exists, including a missing
attack catalogue the adversary is told to work from, a spec review handed to a
station that cannot run one, and a docs/loom README whose sequence still has
review dispatching the adversary. It also found 11 blocks copied between files,
the largest a 304-word station table held in five identical copies, with three
tests that require the copies to stay identical. write-plan's SKILL.md is 4,182
words, over the repository's 3,750-word soft cap. Agents following two
disagreeing copies can take the wrong step, every edit has to be made in several
places, and vendor guidance and measured studies agree that contradictory and
repeated instructions lower how reliably a model follows them.

## Proposed outcome
Each rule an agent needs is stated once, in the file that owns it, and every
other place points there. Rule files no longer contradict each other or the
enforced behaviour, stale pointers are gone, and a firm prohibition keeps its
force with a short reason instead of extra emphasis. An agent running any
station does the same things it does today, from noticeably less text.

## Acceptance
1. Every contradiction and stale reference the audit lists (its items C1–C19) is gone: re-checking each listed item against the new text finds it removed or consistent with what the scripts and stations actually do.
2. Each block duplicated within one plugin that the audit lists (D1 for the two loom-design tools, D2, D3, D4, D5, D9) exists in one file of that plugin, and every former copy is replaced by a pointer to it.
3. The loom-code and loom-design rule files, counted the same way as the audit baseline of 37,665 words, total at least 2,000 fewer words, and loom-code's write-plan SKILL.md is under 3,750 words.
4. The skill cross-reference checker reports a link to a missing file written inside a references file or as a backtick path, and passes on the consolidated tree.
5. Fresh-context agents given the same real task for each changed station on main and on the branch take the same steps, ask the user the same decision-point questions, and produce artifacts that pass the same checker commands.
6. The package test suite, the mechanism inventory check, and the contract citation check pass.

## Constraints
- What each station, agent, checker, and hook does stays the same, except where two rule files disagree; there the text follows the behaviour the scripts enforce today.
- No new rules, stations, decision points, or questions to the user.
- A prose pin moves to the single remaining copy with its check intact; a pin is removed only together with the duplicate text it guarded.
- A gate marker moves with its text; the registered prose-gate count stays at 17.
- Firm prohibitions stay firm: no plan without a confirmed intent, never confirming on the user's behalf, no raw merge outside land, no discard commands in adversary work, and never weakening a test to make it pass.

## Out of scope
- Removing copies shared across loom-code and loom-design (the station table beyond the two tools, second-vendor text, intake text for the loom-design-absent path, one-way-door classes); a later change.
- Rewording emphasis in loom-workflow tools; loom-workflow changes are limited to its stale skill names.
- Restoring the deleted attack catalogue.
- Changing checker, hook, or resolver behaviour, other than extending the skill cross-reference checker's scan.
- The host safety classifier, dcg, and the user's permission settings.

## Open questions
- none
