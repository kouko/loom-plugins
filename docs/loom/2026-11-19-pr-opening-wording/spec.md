# The PR-opening step is no longer called publish — spec
intent: 2026-11-19-pr-opening-wording@114d02af7
pre-build-review: required — renames a public CLI command and removes the old name with no alias (public contract change)

## Requirements
REQ-1 — open-pr command
  The loom checker shall accept `open-pr` with exactly the arguments `publish` accepts today (`--intent <path> --title <text> --body-file <path>`, and the legacy `--confirm-authorized` form), and shall push, open or reuse the PR, and observe CI as `publish` does today → Acceptance #1
REQ-2 — Old name removed
  WHEN a caller runs the `publish` sub-command, the loom checker shall report `unknown sub-command 'publish'` exactly as for any non-existent sub-command, push nothing, open no PR, and exit non-zero; the same holds for `publish --help` and `loom-python --repair publish ...`; no alias and no rename hint is kept (carried: 「直接移除 │ 只回 unknown sub-command，不推送」) → Acceptance #2
REQ-3 — CLI output wording
  The loom checker shall describe the PR-opening step in its printed lines, its usage and `open-pr --help` text, and its error advice as opening or reusing a PR awaiting merge, with no occurrence of publish/published/publication in that text except the machine identifiers listed as out of scope; this includes any checker advice elsewhere that tells the user to rerun the step (e.g. `land` advice, which shall say `run open-pr again`) (carried: 「移除 publish 這個字」) → Acceptance #3
REQ-4 — Push reminder wording
  The push reminder hook messages that today end in `publishing anyway.` and the PreToolUse hook message `...and publish its PR.` (`command_handlers/push.py:188`) shall use the same wording without the word publish; only `NATIVE_HOOK` (`push.py:39-54`) stays byte-identical → Acceptance #4
REQ-5 — Station wording
  The Ship station's skill description, headings, guidance prose, user reports, acceptance prompt and the commands it tells the agent to run (`open-pr`), the using-loom-code routing row, and capture-intent's/write-plan's disclosure that a yes authorizes a later push and Ready PR shall use the same wording and the new command name, and shall keep that merge is a separate decision → Acceptance #5
REQ-6 — README wording
  Every non-history document that describes this step or names the sub-command — the repository and plugin READMEs, `loom-code/skills/ship/README.md`, and `loom-code/references/cli-results.md` — shall use the same wording and the new command name → Acceptance #6
REQ-7 — Native hook unchanged
  The native git hook script bytes shall stay identical, so a repository with the hook already installed still installs and uninstalls it normally after the update → Acceptance #7
REQ-8 — End-to-end
  An agent following the Ship instructions shall still be able to open the PR, observe CI and merge, and the complete package suite shall pass → Acceptance #8

## Design decision
- Rename the dispatch key `publish` → `open-pr` in `COMMANDS`, `COMMAND_HELP`, the usage block, the hint set and `cli_advice`; do not add any entry for `publish`, so it falls through to the existing unknown-sub-command error (user-decided 2026-11-19).
- Keep machine identifiers unchanged: rule id `publish.preconditions`, delivery state and `--goal published`, intent field `publication:`, `publication_only_paths`, the GitHub ruleset name, Python module/function names (`command_handlers/publish.py`, `cmd_publish`). Renaming them invalidates existing intents, attestations and agent JSON consumers (agent-decided; disclosed at ①, intent Out of scope).
- `delivery --goal published` keeps its value name; only its help prose is reworded where it describes the step (agent-decided: the value is a machine identifier).
- The native hook's "publish its PR" sentence stays because installed hooks are byte-compared (intent Constraint).
- Historical records under `docs/loom/` are not edited (intent Out of scope).
- Version bump: loom-code and loom-design minor (station guidance and CLI surface change), per AGENTS.md versioning (agent-decided).

## Alternatives considered
- Keep `publish` as an alias — rejected by the user; it keeps the misleading word usable.
- Tombstone that prints the new name — rejected by the user in favour of plain removal.
- Rename identifiers too — rejected: 154 intents carry `publication:`; attestations and JSON consumers read the state values.
- Wording-only change, rename later — superseded by the user's request to remove the word now.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker.py:561` dispatches `"publish": cmd_publish`; `loom-code/skills/ship/SKILL.md:225,231` instruct the call.
- Reverse: `loom-code/scripts/loom_checker.py:443` (`COMMAND_HELP`), `:583` (hint set), `loom-code/scripts/loom_checker/cli_advice.py:8,26`, usage lines `loom_checker.py:19-20,43,215,279`.
- Error: `loom-code/scripts/loom_checker/command_handlers/land.py:1021,1027` advise `publish again`; `loom-code/scripts/loom_checker.py:606` raises `unknown sub-command` for unmatched names.
- Data: printed lines in `loom-code/scripts/loom_checker/command_handlers/publish.py:691,872,886,1102`; hook messages `command_handlers/push.py:188,223,226`; docs `loom-code/references/cli-results.md:27`, `README.md:261,302`, `loom-code/skills/ship/SKILL.md:4,98,100,165,181`, `loom-code/skills/ship/README.md:5,21,28`, `loom-code/skills/using-loom-code/SKILL.md:18`. Tests pinning `publish`: `test_loom_checker_cli.py`, `test_loom_checker_modules.py`, `test_loom_python_runtime.py`, `test_adversarial_blocked_publish_routes.py`.
- Boundary: `NATIVE_HOOK` at `command_handlers/push.py:39` stays byte-identical; `docs/loom/**` history and recorded dogfood artifacts under `docs/skill-dogfood/` untouched.

## UI flows
| case | what the user/agent does | what they see |
|---|---|---|
| new command | runs `open-pr --intent … --title … --body-file …` | branch pushed, PR opened or reused, CI observed; lines say the PR was opened and awaits merge |
| old command | runs `publish …` | `unknown sub-command 'publish'.` plus usage; nothing pushed; non-zero exit |
| help | runs `open-pr --help` | describes opening a PR and waiting for merge, no publish wording |
| push reminder | pushes with unverified state | reminder says the push proceeds, without "publishing" |
