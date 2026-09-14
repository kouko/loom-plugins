# Let the user choose which Loom steps a single change runs
originator: kouko
kind: engineering
needs-design: yes — multi-state selection flow (proposed step table, user-confirmed binding, mid-change reissue) with no spec
status: confirmed 2026-09-15
publication: automatic — authorized 2026-09-15 by kouko

## Problem
Every Loom change pays the full process regardless of size. A one-line
parameter change still carries an intent, a plan, fresh-context reviewers, an
adversarial program, a blind-run report and a nine-heading pull request. In
iCHEF-dbt-pipeline, Loom records made up 59–87% of the added lines in the
recent small changes (#550: 618 of 784 lines, for a 166-line workflow edit),
and historically most pull requests there bypassed Loom entirely, leaving no
record of what was skipped.

There is no sanctioned way to lighten one change. The `lane:` field and the
`default-lane` key still appear in the contract manifest, the templates and
this repository's `KICKOFF-DEFAULTS.md`, but no checker code reads them since
the reviewer floor became path-computed, so a declaration has no effect. The
station texts assume every earlier station ran, and the push gate requires
reviewer verdicts and an adversarial execution for every change. The only
lighter path is to leave Loom, which the push hook blocks and which records
nothing.

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
- New mechanisms arrive with regression evals (PRINCIPLES.md non-negotiable 4), including the case where the agent suggests a skip and the user replies with a plain "yes" instead of typing the confirmation.

## Out of scope
- A persistent expert mode, named presets, or a per-repository skip configuration.
- Protection against other people using the entry point in this public plugin.
- Automatically re-running skipped reviews later.
- Hosts other than Claude Code and Codex CLI.

## Open questions
- none
