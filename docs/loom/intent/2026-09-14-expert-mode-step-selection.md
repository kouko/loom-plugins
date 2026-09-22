# Let the user choose which Loom steps a single change runs
originator: kouko
kind: product
needs-design: yes — multi-state selection flow (proposed step table, user-confirmed binding, mid-change reissue) with no spec
status: confirmed 2026-09-15
publication: automatic — authorized 2026-09-15 by kouko

## Problem
Every Loom change pays the full process regardless of size. A one-line
parameter change still carries a written intent, a plan, one or two fresh reviewers,
an adversarial test program, a blind-run report and a long pull-request
description. In one team repository, Loom records made up 59–87% of the added
lines in recent small changes (one change added 618 record lines around a
166-line edit), and historically most pull requests there bypassed Loom
entirely, leaving no record of what was skipped.

There is no sanctioned way to lighten one change. The old "lane" setting still
appears in the contract and the repository defaults, but nothing reads it any
more, so declaring it has no effect. The stations assume every earlier station
ran, and publication demands reviewer verdicts and an adversarial run for every
change. The only lighter path is to leave Loom, which publication blocks and
which records nothing.

## Proposed outcome
The user can, for one change, say in natural language which Loom steps to run
or skip. Loom shows its reading of that instruction, lets it take effect only
when the user deliberately types a confirmation that only the user can
produce, honours it through publication, keeps a small fixed floor that no
instruction removes, and discloses what was skipped and on what authority.

## Acceptance
1. After the user describes in natural language which steps to run or skip — either through the entry point or in ordinary conversation — the user sees a table of steps to run and steps to skip; after the user types the entry point's confirmation, the remaining steps of the change are only those marked to run; the user can withdraw a bound selection in their own words, and the full process resumes.
2. Until that typed confirmation exists, the change follows the full process; a plain reply such as "yes" is not a confirmation.
3. Whatever the instruction, the change is still published through a pull request and merged, and cannot be pushed if its content differs from the content its record describes; the package tests may be skipped like any other step, and when they run they must pass.
4. When the agent suggests skipping steps without the user having asked, the suggestion is shown at most once per change, the work continues on the full process without waiting for an answer, and no step is skipped unless the user later types the confirmation.
5. The pull request states which steps were skipped and whether the authority is the user's own recorded words or an agent-recorded instruction.
6. A selection applies only to the change it was given for; the next change follows the full process unless the user gives a new instruction.
7. An instruction given partway through a change affects only the steps after it; a failure the checker recorded before it still appears in the pull request.
8. The user can list the merged changes that skipped review.
9. The entry point works on both Claude Code and Codex CLI, each through its own way of invoking a skill, with the same results.
10. `KICKOFF-DEFAULTS.md`, the contract manifest and the templates no longer carry the unused lane settings, and the repository's existing Loom checks still pass.

## Constraints
- Single user for now (kouko); no qualification switch or persistent mode.
- Supported hosts are Claude Code and Codex CLI.
- Every rule that must block lives in the checker; station prose presents and asks, it does not decide (PRINCIPLES.md Won't do: prose-only gates).
- The agent may suggest skipping steps at most once per change and never waits on that suggestion; only the user's typed confirmation makes a skip take effect.
- The agent-recorded fallback applies only when the checker, not the agent, determines that the host cannot record the user's words.
- PRINCIPLES.md non-negotiable 2 is amended to state that steps the user explicitly skips fall outside its guarantee and must be disclosed; the amendment is re-ratified by kouko.
- Protection stops an agent that takes a shortcut, such as running a documented command or writing a record file; an agent that deliberately disguises its commands to evade the local guard is outside the local guarantee, the same boundary Loom's other local gates keep (user-decided 2026-09-14).
- A reviewer rejection is recorded only when the review station hands it to the checker; the pull request states that limit (user-decided 2026-09-14).
- The intent itself cannot be skipped: every change keeps a confirmed intent, because it carries the acceptance lines and the publication and landing authority the merge path requires (user-decided 2026-09-15).
- On hosts outside scope (such as Antigravity CLI) no confirmation is captured; the entry point says so and the full process applies (user-decided 2026-09-15).
- New mechanisms arrive with regression evals (PRINCIPLES.md non-negotiable 4), including the case where the agent suggests a skip and the user replies with a plain "yes" instead of typing the confirmation.

## Value case
- Beneficiary: kouko, working alone on Loom and adopting repositories.
- Urgency (from the Problem kouko confirmed at ①): small changes in an adopting repository already spend most of their added lines on Loom records, and the workaround is abandoning Loom with no record.
- Existing alternative (from the same confirmed Problem): skip Loom entirely, which publication blocks here and which leaves no disclosure elsewhere.
- Displaced work: nothing — kouko, 2026-09-15 (weak answer).
- GO — kouko chose to continue at every decision in this change; urgency and the alternative are concrete, displaced work is weak.

## Out of scope
- A persistent expert mode, named presets, or a per-repository skip configuration.
- Protection against other people using the entry point in this public plugin.
- Automatically re-running skipped reviews later.
- Hosts other than Claude Code and Codex CLI.

## Later changes
- PR #43 replaced Acceptance 1 and 2, and the typed-confirmation clause of Acceptance 4: a skip no longer waits for a typed confirmation; the user's plain words take effect and the skip is disclosed on the PR (`loom-code/skills/build/SKILL.md` §1, `loom-code/skills/ship/SKILL.md` §1). `/loom-code:expert-mode` remains an optional typed route.
- It also replaced the clause of Acceptance 3 that a change "cannot be pushed if its content differs from the content its record describes": `publish` now discloses an absent or stale verification status and publishes anyway (`loom-code/scripts/loom_checker/command_handlers/publish.py`).
- Acceptance 8 now holds only for the typed `/loom-code:expert-mode` route: a reviewer skip given in plain words leaves the change unattested (`loom-code/skills/closing-review/SKILL.md`), and `selection skipped-review` (`_skipped_review` in `loom-code/scripts/loom_checker/command_handlers/selection.py`) reads only attestations, so such a skip is never listed.
- #43 also replaced four Constraints bullets: "Every rule that must block lives in the checker…", "The agent may suggest skipping steps at most once per change…" (its typed-confirmation clause), "On hosts outside scope (such as Antigravity CLI)…", and the plain-"yes" case of "New mechanisms arrive with regression evals…". A plain-words skip now rests on station prose on every host. PRINCIPLES.md non-negotiable 2 was amended for plain-words skips on 2026-09-22.
- Acceptance 5 carries an authority source only on the typed route (`Skipped steps: <steps> — authority: <source> …`); a plain-words skip is disclosed as `Skipped by instruction: <steps>` with no authority source (`loom-code/skills/ship/SKILL.md` §2).
- Decision recorded in #43's PR body Decisions table (option A) and intent 2026-09-22-publication-floor-moves-to-github.

## Open questions
- none
