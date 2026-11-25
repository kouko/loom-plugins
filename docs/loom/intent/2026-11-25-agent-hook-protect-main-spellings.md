# Agent hook blocks common spellings that commit, merge or push to main
originator: kouko
kind: engineering
needs-design: no — internal gate behaviour; the hook's refusal message and exit code stay as they are, no user-facing surface changes
evidence: [loom-code/scripts/loom_checker/command_handlers/push.py]
status: confirmed 2026-11-25
intent_confirmed_sha: 18d07977f374536f90000a09827b05c7f84ac674
publication: automatic — authorized 2026-11-25 by kouko

## Problem
loom's agent hook is meant to stop an agent from committing, merging or pushing directly on main/master. On 2026-11-25 (loom-code 3.89.0) three common spellings got past it:

| Command an agent ran | Result |
|---|---|
| `cd <main checkout> && git commit -m x` | allowed (exit 0) |
| `git -C <main checkout> commit -m x` | allowed (exit 0) |
| `git push origin HEAD:main` while on a feature branch | allowed (exit 0) |

GitHub's rules still reject a push to main, so the damage is local: an agent can commit or merge onto the local main checkout, and the maintainer later cleans it up by hand (for example `land` reporting that trunk was not updated). Native git hooks close this, but they are opt-in and not installed in most repositories that use loom.

## Proposed outcome
Without native git hooks installed, the agent hook refuses these three spellings the same way it already refuses a plain `git commit` on main, and still lets ordinary feature-branch work through.

## Acceptance
1. An agent command `cd <main checkout> && git commit …` (and the same with `git merge`) is refused with the existing "direct git merge, commit, or push on main/master is blocked" message, and nothing is committed.
2. An agent command `git -C <main checkout> commit …` or `git -C <main checkout> merge …` is refused the same way.
3. An agent command run on a feature branch that pushes to `main` or `master` on a remote (for example `git push origin HEAD:main`) is refused the same way.
4. The commands refused today are still refused, and these still pass: commit, merge and push on a feature branch; a push from a feature branch to a feature branch; any command in a repository with `loom.protectMain` set to `false`.
5. All of the above hold in a repository with no native git hooks installed.
6. The three commands from items 1–3, sent through the OpenCode hook loader and through the Antigravity hook adapter, are refused there too. Codex is reported as not verified when its CLI is unavailable in the test environment.

## Constraints
- The refusal message and exit code stay as they are today.
- The `loom.protectMain false` opt-out keeps working.

## Out of scope
- Commands hidden inside `sh -c`, `eval`, scripts, shell functions or git aliases (native git hooks cover those).
- Commands a person types in their own terminal.
- A trunk named something other than main or master.
- GitHub-side branch rules.

## Open questions
- none
