# Integrate the small bash guard into Loom hooks — plan
intent: 2026-11-01-integrate-bash-guard-into-loom-hooks@348e43b9
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/hooks.json:30` sends shell calls to `push --hook`; Codex and OpenCode use the same checker.
- Reverse: `loom-code/tests/test_publish_command_detection.py:109` verifies the publication reminder from that handler.
- Error: `loom-code/hooks/agy_adapter.py:80` maps checker exit 2 to an Antigravity denial.
- Data: `loom-code/scripts/loom_checker/command_handlers/push.py:54` reads the command and host working directory.
- Boundary: `loom-code/scripts/loom_checker/rule_checks/push.py:76` recognizes only a direct publication command.

## Task DAG

Wave 0: Add failing boundary cases, then place one guard in the existing checker.

**W0-01 Guard direct main-branch Git changes**  after: none  acceptance: 1, 2, 3, 5, 6
- Files: `loom-code/tests/test_main_branch_hook.py`, `loom-code/scripts/loom_checker/command_handlers/push.py`, `loom-code/tests/test_publish_command_detection.py`, `loom-code/tests/test_agy_adapter.py`
- Test: A1 positive: direct-main-denial; boundary: feature-and-wrapper; A2 positive: nongit-ls; boundary: detached; A3 positive: publication-reminder; boundary: pr-merge-allow; A5 positive: host-carriers; boundary: malformed-payload; A6 positive: local-optout; boundary: ordinary-repo.
- Risk: agent-decided — keep publication detection unchanged; add one direct Git verb check. Intentional refusal exits 2; non-Git, detached, and unexpected reminder errors allow.

Wave 1: Remove the duplicate user hook registration and verify host behavior.

**W1-01 Cut over dotfiles registration**  after: W0-01  acceptance: 4, 5, 6
- Files: `/Users/kouko/dotfiles/claude/settings.template.json`, `/Users/kouko/dotfiles/tests/claude_settings_sync_test.sh`, `/Users/kouko/dotfiles/claude/.claude/hooks/README.md`, `loom-code/tests/test_hooks_json.py`
- Test: A4 positive: one-registration; boundary: retained-dcg; A5 positive: all-host-definitions; boundary: stale-checker; A6 positive: personal-repos; boundary: other-user.
- Risk: agent-decided — use repo-local Git config opt-outs in dotfiles and vault; verify both after installation. Remove only duplicate registration and preserve unrelated changes.

Wave 2: Publish a distinct plugin version so installed hosts can receive the guard.

**W2-01 Bump Loom release metadata**  after: W1-01  acceptance: 4, 5
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/README.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`, `scripts/sync_codex_manifests.py`
- Test: A4 positive: distinct-installed-version; boundary: derived-manifests; A5 positive: release-sync; boundary: stale-version-pin.
- Risk: agent-decided — patch bump because no station guidance, field, rule id, or contract manifest changes; regenerate derived manifests from the single source.

## Simplicity check
- Keep publication recognition unchanged; add one exact Git verb check in the existing handler — taken
- Set and verify both personal repo opt-outs explicitly rather than assuming Loom files configure them — taken
- Exercise the Antigravity adapter's deny carrier alongside other hosts — taken

## Questions asked
- none

## Risks
user-decided — Implement the small direct-command guard first; accept that prefixed commands, wrappers, and scripts can bypass this host hook.
user-decided — Keep Loom's reminder policy for PR merge/close and preserve personal main-branch exceptions without hard-coded paths.
1. A direct-command check cannot stop shell wrappers or Git operations outside the host; the acceptance report must state this limit.
2. The dotfiles repository and both repos' local Git config are outside this worktree; cutover must preserve unrelated changes and cannot be called active before the new plugin is installed.
