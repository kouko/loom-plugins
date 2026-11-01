# Standalone diagrams and explicit external-file editing — plan
intent: 2026-11-01-standalone-diagram-files@699f87dbd4bbe8582820e6aa281093930c565224
spec: docs/loom/2026-11-01-standalone-diagram-files/spec.md@291822476e4c81578259b6b1c625a7bbc50e550b
charter: 1.1

## Task DAG

Wave 1 — implement diagram operations at one command boundary.

**W1-01 Explicit standalone creation, copying, and guarded external projection**  after: none  acceptance: 1,3,4,5
- Files: loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py, loom-workflow/tests/loom-interactive-diagram/test_diagram_tool.py
- Test: A1 positive: standalone-create; boundary: missing-destination. A3 positive: copy-and-direct-project; negative: occupied-target. A4 positive: loom-copy-managed; boundary: symlinked-managed-store. A5 positive: managed-new-unchanged; negative: external-write-without-selection.
- Risk: agent-decided — REQ-1/3/4/5: require explicit external choices and no overwrite; preserve managed-path tests while rejecting symlinked external writes.

Wave 2 — teach the chosen user interaction and prepare the release.

**W2-01 Skill conversation and editor guidance**  after: W1-01  acceptance: 2,6
- Files: loom-workflow/skills/loom-interactive-diagram/SKILL.md, loom-workflow/skills/loom-interactive-diagram/references/editor-setup.md, loom-workflow/skills/loom-interactive-diagram/references/projection.md, loom-workflow/tests/loom-interactive-diagram/test_skill_guidance.py
- Test: A2 positive: ask-before-external-edit; negative: unanswered-no-write. A6 positive: both-contexts-explained; boundary: destination-named.
- Risk: agent-decided — REQ-2/6: ask on every external edit request, including clear direct-edit wording; state the actual destination without a second automatic-copy path.

**W2-02 Release metadata and version sync**  after: W2-01  acceptance: 6
- Files: loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json, loom-workflow/plugin.json, loom-workflow/package.json, loom-workflow/CHANGELOG.md, loom-workflow/README.md, README.md, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A6 positive: release-describes-standalone-use; boundary: manifest-versions-match; rewrite the pinned current-version test.
- Risk: agent-decided — REQ-6: minor release 5.19.0 is needed for changed skill guidance and CLI; generated manifests are synchronized from the plugin source.

Wave 3 — close two demonstrated write-boundary defects.

**W3-01 Protect every projection rewrite and graduate hardlink probe**  after: W2-02  acceptance: 3,5
- Files: loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py, loom-workflow/tests/loom-interactive-diagram/test_diagram_tool.py, docs/loom/2026-11-01-standalone-diagram-files/evidence/probes/test_projection_hardlink_preserves.py, loom-workflow/tests/loom-interactive-diagram/test_projection_hardlink_preserves.py
- Test: A3 positive: direct-project-safe-replace; boundary: hardlinked-projection. A5 positive: managed-project-safe-replace; boundary: managed-hardlinked-projection.
- Risk: agent-decided — projection rewrite alias class searched all changed diagram.py writes and related tests; both direct and managed project write sites must avoid changing unselected hard-linked files.

**W3-02 Reject redirecting standalone destinations and graduate symlink probe**  after: W3-01  acceptance: 1,3
- Files: loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py, loom-workflow/tests/loom-interactive-diagram/test_diagram_tool.py, docs/loom/2026-11-01-standalone-diagram-files/evidence/probes/test_destination_symlink_rejected.py, loom-workflow/tests/loom-interactive-diagram/test_destination_symlink_rejected.py
- Test: A1 positive: canonical-standalone-create; negative: symlinked-output-dir. A3 positive: canonical-standalone-copy; negative: symlinked-copy-output-dir.
- Risk: agent-decided — redirected destination class searched destination_args, create, copy, and related tests; reject symlinked standalone output directories before either operation writes.

**W3-03 Keep the skill description inside its routing budget**  after: W3-02  acceptance: 6
- Files: loom-workflow/skills/loom-interactive-diagram/SKILL.md, tests/test_loom_skill_description_catalog.py
- Test: A6 positive: standalone-create-readback-description; boundary: catalog-description-budget.
- Risk: agent-decided — description pin drift class searched the changed SKILL.md frontmatter and tests/test_loom_skill_description_catalog.py; retain the established 213-character budget and creation wording.

## Simplicity check
- One command-and-test task for the shared entrypoint — taken

## Questions asked
- ① — what — 這次要涵蓋哪些外部圖檔操作？我會保留 Loom 變更內的固定存放位置；獨立使用時則可明確指定外部位置。
- ① — what — 這項圖表工具工作會取代或延後哪項原定工作？若沒有，請直接回答「沒有」。
- ① — what — 你希望 Loom 流程也允許使用者明確選擇直接編輯外部原檔這項例外嗎？
- ① — what — 你指的是改用較自然的說法，還是希望 Loom 流程也能把副本放在專案內任意指定的位置？
- ① — what — 你要的是讓圖表工具也能獨立使用；每次要編輯既有外部圖檔時，先問你要不要複製到專案內，得到回答後才編輯副本或原檔。完成後，你也能指定新圖的保存位置；Loom 討論中新建的圖和經同意建立的副本，仍放在該次變更的圖表資料夾。這樣理解對嗎？
- ② — behaviour — 這就是你希望使用時看到的行為嗎？
- ② — behaviour — 這個區分和上一則列出的其他行為，符合你的預期嗎？
- ② — behaviour — 這些補充後的行為符合你的預期嗎？

## Risks
1. In-place editing can change an external original and adjacent projection; each edit requires the user's copy choice, and no automatic backup is promised.
2. Standalone destinations are selected by the user rather than inferred from the current working directory; missing destinations must stop before writing.
3. Existing parser and managed-path tests protect PR #125 behavior; the new options must not weaken those boundaries.
4. Two adversarial RED programs are graduated into the routine diagram suite through W3-01 and W3-02; Build re-runs them after each fix.
5. The complete suite found two description-contract failures; W3-03 restores the description budget without weakening the catalog checks.
