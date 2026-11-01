# Fix Loom hook exit-code handling across hosts — plan
intent: 2026-10-25-loom-hook-exit-code@9dbb740e
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/hooks-codex.json:19` runs the checker before deciding whether to allow the command.
- Reverse: `loom-code/tests/test_hooks_json.py:261` exercises all four host hook definitions.
- Error: `loom-code/hooks/hooks.json:30` handles checker runtime exit 86 as an allowed hook failure.
- Data: `loom-code/hooks/hooks-opencode.json:20` stores the prior command's exit code in `status`.
- Boundary: `loom-code/tests/test_codex_stale_hook.py:36` invokes the command through the default shell, missing zsh behavior.

## Task DAG

Wave 0: Test the shell collision, then repair the shared command pattern.

**W0-01 Preserve hook exit codes in every host**  after: none  acceptance: 1, 2, 3
- Files: `loom-code/tests/test_hooks_json.py`, `loom-code/hooks/hooks.json`, `loom-code/hooks/hooks-codex.json`, `loom-code/hooks/hooks-opencode.json`, `loom-code/hooks.json`
- Test: A1 positive: codex-zsh; boundary: reserved-name; A2 positive: configured-shells; boundary: runtime-unavailable; A3 positive: all-zsh; boundary: reserved-name.
- Risk: agent-decided — rename only the local exit-code variable to preserve all checker and fallback paths; existing host tests retain their cases.

## Simplicity check
- One shared variable name in the existing commands — taken

## Questions asked
- ① — what — 所以所有 host 的 hook 都要統一變更 對嗎？
- ① — behaviour — 那就統一改名吧

## Risks
1. Some CI runners may lack zsh; a portable read-only variable probe must cover the collision alongside local zsh execution.
