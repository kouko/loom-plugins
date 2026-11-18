# Skill folder check and AGENTS.md cleanup — plan
intent: 2026-11-18-skill-folder-check-and-agents-cleanup@dc09e338
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/hooks/hooks.json:21` runs `loom-workflow/scripts/validate-skill-folder-structure.sh` after Write and Edit.
- Reverse: `loom-workflow/scripts/validate-skill-folder-structure.sh:31-34` exits 0 when `.claude/hooks/validate-skill-folder-structure.sh` is executable in the repository.
- Error: `.claude/settings.json` is absent, so `.claude/hooks/validate-skill-folder-structure.sh:4` names a registration that does not exist; nested folders pass silently.
- Data: `loom-code/scripts/repo_files.py:64` lists tracked plus untracked non-ignored files; `tests/test_tests_folder_convention.py:32-34` shows the import pattern.
- Boundary: `AGENTS.md:44-88` and `AGENTS.md:123` are pinned by tests; `AGENTS.md:111` has no check and keeps its MUST.

## Task DAG
Wave 1 restores the check, then aligns the guide with it.

**W1-01 Restore the flat skill-folder check**  after: none  acceptance: 1, 2
- Files: tests/test_skill_folder_flatness.py (entry), .claude/hooks/validate-skill-folder-structure.sh (delete)
- Test: A1 positive: nested-uncommitted-path-fails; boundary: flat-and-ignored-paths-pass. A2 positive: nested-write-reports-violation; negative: test_flat_skill_passes (existing).
- Risk: agent-decided: delete the unregistered copy, because registering it duplicates the plugin hook. Plugin deferral stays for other repositories; existing `loom-workflow/tests/scripts/test_validate_skill_folder_structure_hook.py` coverage is preserved.

**W1-02 Align AGENTS.md with the repository**  after: W1-01  acceptance: 3, 4, 5
- Files: AGENTS.md
- Test: A3 positive: named-paths-resolve; negative: absent-plugin-names-gone. A4 positive: rules-match-current-sources; negative: stale-review-claims-gone. A5 positive: pinned-guide-tests-pass; negative: both-must-rules-retained. No new test file.
- Risk: agent-decided: point review details to `lenses.md` and the checker instead of restating them. Keep test-pinned sections; correct version text per plugin without weakening its MUST.

## Simplicity check
- Reuse the existing flat-skill hook test instead of adding another A2 negative test — taken
- Verify AGENTS.md by lookups and existing tests instead of new prose-pin tests — taken

## Questions asked
① — what — 先修檢查和文件、只清 AGENTS.md、先補 main 防護、或先不動，要選哪一個？（answer: 先修檢查和文件）
① — consequence — 確認範圍、刪除未註冊的 repo hook、把跨 plugin 委派規則從本 repo 移除（monkey-skills/CLAUDE.md 仍保留），並授權審查與發布檢查通過後 non-force push 和 Ready PR；這樣可以嗎？（answer: ＯＫ）

## Risks
1. user-decided — delete the unregistered repository hook and remove the cross-plugin rule here, because it remains in the sibling repository's `CLAUDE.md`.
2. agent-decided — no plugin version bump: this change edits no plugin path, so installed plugin content is unchanged.
3. agent-decided — two test `conftest.py` comments naming the old hook were already outdated and stay untouched, keeping plugin paths out of this change.
