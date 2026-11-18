# Skill-folder check also rejects symlinks — plan
intent: 2026-11-18-skill-folder-symlink-check@5c8c698
spec: docs/loom/2026-11-18-skill-folder-symlink-check/spec.md
charter: 1.1

## Task DAG
One wave: the check, its tests, and its docstring are one module in one file; boundary coverage follows the core rule change on the same file, so the two tasks run sequentially.

**W1-01 Reject in-scope symlinks in the flatness check**  acceptance: 1, 2
- Files: tests/test_skill_folder_flatness.py
- Test: A1 positive: in-scope-symlink-fails; boundary: staged-dangling-link-fails. A2 positive: committed-link-fails-from-index; boundary: dangling-committed-link-fails.
- Risk: widen `assert_skill_folders_flat` and message; keep gitlink/nested behavior byte-identical (existing tests unchanged). agent-decided.

**W1-02 Boundary tests and docstring**  after: W1-01  acceptance: 3, 4
- Files: tests/test_skill_folder_flatness.py
- Test: A3 positive: symlink-outside-scope-passes; boundary: plugin-root-link-fails. A4 positive: repository-suite-passes; boundary: scope-link-flips-suite-red.
- Risk: this materially rewrites the docstring's exception list; preserve every other documented exception (ignored paths, deleted files, marketplace scope). agent-decided.

## Simplicity check
- One task instead of two — declined: Test-pair caps force A1/A2 and A3/A4 apart; same-file sequence costs nothing.
- A separate symlink-checker module — declined: one more module for ~10 lines; the existing file is the module boundary.

## Questions asked
① — what — 要把 symlink 也納入扁平檢查嗎（我提出選項，你回覆「ＯＫ go」）
① — consequence — skill 範圍內從此不能用 symlink 共用檔案（含指向單一檔案），你以「ＯＫ go」接受
① — what — 確認意圖：追加的檢查是避免 plugin/skills 範圍出現 symlink，你回覆「是，這就是我要的」

## Risks
1. A developer using a symlink for local convenience gets a red suite; the failure message must name the link path and the removal (`delete the link`) plainly.
2. Symlink detection must read `git ls-files` output the same way on fresh clones as in working trees; W1-01's A2 case pins the clone-like path.
