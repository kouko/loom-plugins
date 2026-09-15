# Probe — does `--plugin-dir` reach a subagent's role contract?

Date: 2026-09-15. Question: an ordinary in-session dispatch of
`loom-code:reviewer` loads the installed plugin's contract (3.4.0), not this
branch's edited `loom-code/agents/reviewer.md`. Does a headless session started
with `--plugin-dir <branch>/loom-code` dispatch that subagent with the branch
contract instead?

## Method

Two headless Claude Code sessions, each started from its own new empty
directory (no repository files reachable by relative path), model `sonnet`,
only the Agent tool allowed, prompt passed on stdin:

> Use the Agent tool exactly once with subagent_type "loom-code:reviewer" and
> this prompt: 'Do not use any tools. Quote verbatim the sentence in your own
> system instructions that says whether you may run the complete package suite
> or adversarial programs, and the sentence that says what you must do with
> test files the change added or changed. If no such sentence exists, reply
> NONE for it.' Then print the subagent reply verbatim and nothing else.

- Branch arm: `claude -p --plugin-dir <worktree>/loom-code --model sonnet --allowedTools=Agent`
- Control arm: `claude -p --model sonnet --allowedTools=Agent` (installed loom-code 3.4.0)

Discriminator: the sentences below exist only in this branch's reviewer
contract (commit a8552878); the installed 3.4.0 contract has neither.

## Result

Branch arm (exit 0) quoted:

> "In every round, you never run the complete package suite or the adversarial
> programs: both run mechanically at the end of Build, and `finalize-review`
> executes them again and records the result."

> "The `tests` dimension reads the committed tests and adversarial artifacts,
> and you run the test files the change added or changed — a test in one of
> those files that is skipped, or that never actually executes, is a `tests`
> finding, since a green exit code does not show that it ran."

Control arm (exit 0) quoted the installed text instead — "Do not re-run
adversarial programs; closing finalization owns their single execution." — and
answered NONE for changed test files.

## Conclusion

`--plugin-dir` does reach subagent role contracts: a reviewer dispatched from a
session started with the branch plugin runs under the branch's reviewer
contract, and the control arm confirms the ordinary path runs the installed one.
This change's closing reviewers are therefore dispatched through a
`--plugin-dir` headless session so Acceptance 9 observes the new contract.
