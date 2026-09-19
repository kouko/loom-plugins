# Bump loom-code to 3.7.2 — plan
intent: 2026-09-19-bump-loom-code-3-7-2@b6a69a14
charter: 1.0

## Current State Evidence

- Forward: `loom-code/plugin.json:3`, `.claude-plugin/plugin.json:3`,
  `.codex-plugin/plugin.json:3` all read `3.7.1`, unmoved since 2026-09-16 while
  #30 and #31 merged after it.
- Reverse: `loom-code/scripts/test_write_plan_station_text.py:467`
  `test_current_release_metadata_is_synchronized` reads all three manifests and
  the changelog; it is the only check tying them together.
- Error: `claude plugin update` compares the version string only; an unmoved
  string reads as "already at the latest version" and refreshes nothing, per
  3.7.1's own changelog entry describing the identical prior failure.
- Data: five README locations (`loom-code/README.md`, `.ja.md`, `.zh-TW.md`,
  root `README.md` twice) also carry the version string and are not covered by
  the manifest-sync test; commit d1deffe0 found and fixed all five.
- Boundary: contract manifest version (`loom-code/contract/manifest.yaml:5`,
  `2.3.1`) is untouched, so this is a patch bump per the versioning convention
  3.7.1's entry states.

## Task DAG

**W0-01 Bump three manifests, changelog, and the pinned test**  after: —  acceptance: 1, 2, 4
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/scripts/test_write_plan_station_text.py`
- Test: A1 positive: manifests read `3.7.2`; boundary: `3.7.1` fails `test_current_release_metadata_is_synchronized`. A2 positive: changelog carries `## [3.7.2]`; negative: a missing heading fails it. A4 positive: full suite passes; negative: `3.7.1` fails the assertion.
- Risk: a manifest missed reopens the same failure; the pinned test catches all three by construction. agent-decided.

**W0-02 Bump five README version locations**  after: —  acceptance: 3, 4
- Files: `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `README.md`
- Test: A3 positive: all five locations read `3.7.2`; negative: a location left at `3.7.1` fails `test_readme_version_matches_manifest` or the root-README tests. A4 positive: full suite passes; negative: an unbumped location fails its own test.
- Risk: not covered by the manifest-sync test; caught only by grep, already done. agent-decided.

Already implemented and committed at d1deffe0, ahead of this plan (the fix was
built before the intent/plan formality this station requires); this plan
records it for the closing-review gate rather than redoing the work.

## Questions asked

① — consequence — 這個版本升級要推送並合併嗎? — 使用者稍早已看過完整內容並回答「好」,隨後再次確認「推吧 合併吧」;capture-intent 站沿用這兩次回答作為決策點①的確認,未重複提問。

## Risks

1. Release metadata only; no rule id or contract change. Full suite (3425 passed, 11 skipped pytest; 145 PASS, 0 FAIL shell) already covers the only regression risk.
