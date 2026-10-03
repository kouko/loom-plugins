# Session start survives control characters in the repo defaults — plan
intent: 2026-10-03-session-start-control-characters@11dc4ac3
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/session-start` reads `docs/loom/KICKOFF-DEFAULTS.md` list lines into `defaults` (line ~101) and appends them to `body`.
- Reverse: `test_session_start_words.py::test_kickoff_defaults_lines_are_injected_when_the_file_exists` runs the hook against a temporary defaults file.
- Error: `escape_for_json` (line ~111) escapes only backslash, quote, newline, carriage return and tab; a form feed in a defaults line makes `json.tool` fail with "Invalid control character".
- Data: the rest of `body` is static text, so the defaults lines are the only source of other control characters.
- Boundary: `loom-code/CHANGELOG.md` 3.29.0 first bullet says options that run no tests are refused in any position, but `-o addopts=--collect-only` is accepted.

## Task DAG
Wave 1 fixes the hook; wave 2 rewords the 3.29.0 bullet and bumps the version.

**W1-01 Session start drops other control characters from the defaults lines**  after: none  acceptance: 1, 2
- Files: loom-code/hooks/session-start, loom-code/tests/test_session_start_words.py
- Test: A1 positive: form-feed-and-escape-defaults-yield-valid-json-with-station-order; negative: control-characters-absent-from-context. A2 positive: existing-kickoff-defaults-test-passes-unchanged; boundary: plain-line-beside-control-line-kept.
- Risk: agent-decided — delete control characters other than tab and newline from `defaults` where read, one line; adds one test to test_session_start_words.py, preserves its existing cases.

**W2-01 Release metadata: reword 3.29.0 bullet and bump to 3.29.1**  after: W1-01  acceptance: 3, 4
- Files: loom-code/CHANGELOG.md, loom-code/plugin.json, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/package.json, README.md, loom-code/README*.md, loom-code/tests/test_write_plan_station_text.py
- Test: A3 positive: changelog-names-config-override-gap; negative: no-always-refused-claim. A4 positive: release-metadata sync test passes at 3.29.1; negative: `sync_codex_manifests.py --check --all` exits 0.
- Risk: agent-decided — patch for loom-code (hook fix, no guidance, field or rule change); reword the 3.29.0 bullet in place, no allowlist code change; loom-design and loom-workflow untouched.

## Simplicity check
- One new test, reusing the existing defaults test as A2 evidence — taken
- Fold the CHANGELOG rewording into the release-metadata task — taken

## Questions asked
① — what — 覆述 intent（控制字元修正），含自動發布授權 → 「對」
① — what — CHANGELOG 3.29.0 過度宣稱要不要一起修 → 「一起修」

## Risks
1. A defaults line that relied on a control character loses it; none of the documented defaults use one.
