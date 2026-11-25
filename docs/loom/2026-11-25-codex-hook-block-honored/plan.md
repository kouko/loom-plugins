# Codex honours loom's main-protection hook — plan
intent: 2026-11-25-codex-hook-block-honored@0772a66ba
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/hooks-codex.json` PreToolUse matcher `Bash` runs `loom-python --ready push --hook`; exit 2 plus stderr blocks, which Codex 0.172.0 honours.
- Reverse: `loom-code/.codex-plugin/plugin.json` `hooks` points Codex at `hooks-codex.json`; README `### Codex` section documents install and update.
- Error: after `codex plugin add`, changed hook content is untrusted until re-approved interactively; the 2026-11-25 probe commits landed within two minutes of install.
- Data: `~/.codex/config.toml` `[hooks.state."loom-code@loom:hooks/hooks-codex.json:pre_tool_use:0:0"]` keeps `trusted_hash` and `trusted_content_hash`.
- Boundary: orchestrator observation (unrecorded in evidence) 2026-11-25 on 3.90.1: plain and `cd ../repo &&` commits on main were blocked, feature commit allowed; no code defect found.

## Task DAG

### Wave 1

**W1-01 Document Codex hook re-approval after update**  after: none  acceptance: 1, 2, 3, 4, 5
- Files: loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md
- Test: A1 positive: live-codex-main-commit-blocked; negative: none-needed-docs. A2 positive: live-codex-cd-main-blocked; negative: live-codex-feature-commit-allowed. A3 positive: live-codex-feature-commit-allowed; boundary: live-codex-cd-main-blocked. A4 positive: package-suite-green; boundary: hooks-files-unchanged. A5 positive: readme-codex-update-note; boundary: three-readmes-consistent.
- Risk: no hook or checker code changes; AT re-run verified A1 (hook blocked main commit); A2 unsettled (Codex model refused); A3 carried over; delivery rests on A1, A3–A5; agent-decided.

**W1-02 Release metadata for loom-code 3.90.2**  after: W1-01  acceptance: 4
- Files: loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, README.md, loom-code/tests/test_write_plan_station_text.py
- Test: A4 positive: release_sync; boundary: release_stale_pin. Existing pin `test_current_release_metadata_is_synchronized` covers it.
- Risk: patch bump via SSOT then `sync_codex_manifests.py --all`; agent-decided.

## Simplicity check
- Docs-only fix; keep exit-2 blocking, which Codex 0.172.0 honours — taken
- Withdraw the change entirely — declined: user chose option A (document the limitation)

## Questions asked
① — what — 這樣是你要的嗎？ (restatement confirmation; user: yes)
① — what — 要選哪個？(A docs-only / B withdraw / C reproduce first; user: A)

## Risks
1. Root cause (untrusted hooks after update) is inferred from timing and the content-hash trust failure, not reproduced; the note is phrased as a safe precaution.
2. Early probes saw the hook event fire yet commits land; untrusted changed hook content may run without enforcement or be skipped — both explained by trust state, not reproduced.
