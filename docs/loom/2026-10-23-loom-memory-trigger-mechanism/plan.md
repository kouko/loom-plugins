# loom-memory fires on host memory saves — plan
intent: 2026-10-23-loom-memory-trigger-mechanism@d3bad1fe
spec: docs/loom/2026-10-23-loom-memory-trigger-mechanism/spec.md@d99e48a9
charter: 1.1

## Task DAG

Wave 1 — skill text, and the hook that replaces the orphan (independent modules).

**W1-01 loom-memory trigger and classification text**  after: none  acceptance: 1, 2, 4, 5, 6
- Files: loom-workflow/skills/loom-memory/SKILL.md, loom-workflow/skills/loom-memory/references/operations.md, loom-workflow/tests/loom-memory/test_skill_contract.py, loom-workflow/skills/loom-memory/evals/host-memory-trigger.md, loom-workflow/skills/loom-memory/evals/host-memory-trigger-cases.json
- Test: A1 positive: activation-names-host-memory-save; negative: activation-without-it-fails. A2 positive: machine-and-tool-notes-excluded; negative: repo-wide-lesson-kept. A4 positive: description-names-own-memory; boundary: description-within-133-chars. A5 positive: activation-lists-host-save; negative: no-other-condition-sentence-absent. A6 positive: post-finalize-deferral-kept; negative: deferral-removal-fails.
- Risk: preserves REQ-4 station-coupling pin in test_skill_contract.py; narrows nothing. Description wording agent-decided within 133 chars; recall phrasing kept. See spec Design decision.

**W1-02 loom-workflow host memory reminder hook replaces the orphan**  after: none  acceptance: 3, 4, 6, 7, 8
- Files: loom-workflow/hooks/memory-mirror-reminder, loom-workflow/hooks/hooks.json, loom-workflow/tests/loom-memory/test_memory_mirror_hook.py, .claude/hooks/remind-memory-mirror.sh, tests/hooks/test_remind_memory_mirror.py, tests/test_tests_folder_convention.py
- Test: A3 positive: any-note-type-reminds; negative: non-memory-or-malformed-silent. A4 positive: claude-hooks-wired; negative: codex-hooks-unwired. A6 positive: reminder-names-finalize-deferral; boundary: index-write-silent. A7 positive: orphan-files-absent; negative: fixture-neutral-name. A8 positive: package-suite-passes; boundary: removed-test-coverage-widened.
- Risk: deletes the orphan and its test; new test widens coverage to all note types. Path-only match, additionalContext exit 0 (spec Design decision). Fixture renamed; historical CHANGELOG/docs mentions kept, agent-decided.

Wave 2 — release.

**W2-02 loom-workflow release metadata**  after: W1-01, W1-02  acceptance: 8
- Files: loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json, loom-workflow/plugin.json, loom-workflow/package.json, loom-workflow/CHANGELOG.md, loom-workflow/README.md, loom-workflow/README.ja.md, loom-workflow/README.zh-TW.md
- Test: A8 positive: release-metadata-synchronized; boundary: derived-manifests-match-ssot.
- Risk: minor bump 5.14.0 to 5.15.0 (new hook); derive via sync_codex_manifests.py --all, never hand-edit derived files. Bump before finalize-review.

## Simplicity check
- merge orphan removal into the hook task (one task and one dependency fewer) — taken

## Questions asked
① — what — 這樣對嗎？PR 描述那一行要保留還是拿掉？
① — what — 要我把 intent 改成 B 嗎？這會改掉 intent 的主要方向：流程站不動，改成調整 loom-memory 的 description 和分類標準，所以需要你明確回答。
① — what — 要我照 B + C 改寫 intent 嗎？還有一件事要你決定：hook 要放在 loom-workflow plugin 裡（所有使用 loom 的 repo 都會生效），還是只放在這個 repo？
① — consequence — hook 放在 loom-workflow 裡，代表你所有裝了 loom-workflow 的 repo（例如 dbt 專案）都會生效。在那些 repo 裡每次存內建記憶，都會多一次提醒。這個影響可以收回。這樣對嗎？
① — what — 我建議用第一種：同樣長度內改寫，加上新舊對照實測……如果你想加中文和日文的觸發詞，就要選第二種，請告訴我。

## Risks
1. Description triggering is probabilistic; acceptance testing measures old against new on the eval cases and reports counts, it does not guarantee a rate.
2. The hook fires in every repo with loom-workflow installed; a repo without `docs/loom/memory/` gets one initialized when a repo lesson is recorded.
3. agent-decided — Acceptance 7 read as runtime and test files: historical CHANGELOG and migration records keep the old name; acceptance testing reports them plainly.
4. user-decided — hook in the loom-workflow plugin, all repos (2026-10-24); description same-length rewrite with measurement (2026-10-24).
