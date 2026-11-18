# Skill folder check and AGENTS.md cleanup — plan
intent: 2026-11-18-skill-folder-check-and-agents-cleanup@0c3bd97b
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/hooks/hooks.json:21` runs `loom-workflow/scripts/validate-skill-folder-structure.sh` after Write and Edit.
- Reverse: `loom-workflow/scripts/validate-skill-folder-structure.sh:31-34` exits 0 when `.claude/hooks/validate-skill-folder-structure.sh` is executable in the repository.
- Error: `.claude/settings.json` is absent, so `.claude/hooks/validate-skill-folder-structure.sh:4` names a registration that does not exist; nested folders pass silently.
- Data: `loom-code/scripts/repo_files.py:64` lists tracked plus untracked non-ignored files; `tests/test_tests_folder_convention.py:32-34` shows the import pattern.
- Boundary: `AGENTS.md:44-88` and `AGENTS.md:123` are pinned by tests; `AGENTS.md:111` has no check and keeps its MUST.

## Task DAG
Wave 1 restores the check, then aligns the guide with it.

**W1-01 Restore the flat skill-folder check**  after: none  acceptance: 1
- Files: tests/test_skill_folder_flatness.py (entry)
- Test: A1 positive: nested-uncommitted-path-fails; boundary: flat-and-ignored-paths-pass.
- Risk: user-decided: the package suite is the check here; the unregistered copy stays, so the plugin hook keeps deferring. Existing `loom-workflow/tests/scripts/test_validate_skill_folder_structure_hook.py` coverage is preserved.

**W1-02 Align AGENTS.md with the repository**  after: W1-01  acceptance: 2, 3, 4
- Files: AGENTS.md
- Test: A2 positive: named-paths-resolve; negative: absent-plugin-names-gone. A3 positive: rules-match-current-sources; negative: stale-review-claims-gone. A4 positive: pinned-guide-tests-pass; negative: both-must-rules-retained. No new test file.
- Risk: agent-decided: point review details to `lenses.md` and the checker instead of restating them. Keep test-pinned sections; correct version text per plugin without weakening its MUST.

**W1-03 Graduate the adversarial flatness programs**  after: W1-01  acceptance: 1
- Files: tests/test_adversarial_flatness_committed_nested_missed.py, tests/test_adversarial_flatness_nested_repository_missed.py, tests/test_adversarial_flatness_non_plugin_false_alarm.py, tests/test_adversarial_flatness_removed_still_fails.py
- Test: A1 positive: committed-nested-path-fails; boundary: removed-path-passes.
- Risk: agent-decided: move each program that caught a defect into root `tests/` unchanged except for path resolution, so the package suite keeps them.

## Simplicity check
- Leave the write-time hook out of this change and rely on the package suite — taken
- Verify AGENTS.md by lookups and existing tests instead of new prose-pin tests — taken

## Questions asked
① — what — 先修檢查和文件、只清 AGENTS.md、先補 main 防護、或先不動，要選哪一個？（answer: 先修檢查和文件）
① — consequence — 確認範圍、刪除未註冊的 repo hook、把跨 plugin 委派規則從本 repo 移除（monkey-skills/CLAUDE.md 仍保留），並授權審查與發布檢查通過後 non-force push 和 Ready PR；這樣可以嗎？（answer: ＯＫ）
① — consequence — 要照建議退回 hook 這部分、取消寫檔當下提示的驗收條件，並保留未註冊的 repo hook 嗎？（answer: 退回吧）

## Risks
1. user-decided — remove the cross-plugin rule here, because it remains in the sibling repository's `CLAUDE.md`.
2. agent-decided — no plugin version bump: this change edits no plugin path, so installed plugin content is unchanged.
3. user-decided — Build requirement change: activating the plugin hook exposed false alarms and misses whose fix would affect other repositories. Former Acceptance 2 is removed and later lines renumber; W1-01 continues because its package-suite obligation is unchanged.
4. agent-decided — evidence: package-suite flatness and AGENTS.md lookups still apply; hook-write evidence and hook adversarial programs no longer apply and are replaced.
