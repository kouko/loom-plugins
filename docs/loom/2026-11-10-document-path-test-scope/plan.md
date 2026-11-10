# Scope document-path validation — plan
intent: 2026-11-10-document-path-test-scope@c1a4cb23
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/session-start:94` emits the installed launcher's absolute path.
- Reverse: `loom-code/tests/test_conversation_document_paths.py:43` checks emitted context and both visualization guidance sources together.
- Error: `loom-code/tests/test_conversation_document_paths.py:49` rejects the current checkout's user-directory prefix; the isolated test reproduces the failure.
- Data: `loom-workflow/tests/mermaid/package.json` declares test-only Mermaid and jsdom dependencies; npm reported three vulnerabilities during installation.
- Boundary: `loom-code/tests/test_conversation_document_paths.py:54` retains negative checks for missing and negated document-delivery obligations.

## Task DAG

### Wave 1
**W1-01 Scope path assertions and boundary tests** after: none acceptance: 1, 2, 3
- Files: `loom-code/tests/test_conversation_document_paths.py`
- Test: A1 positive: emitted-current-launcher; negative: wrong-launcher. A2 positive: portable-guidance; negative: hardcoded-guidance. A3 positive: complete-suite; boundary: unchanged-runtime.
- Risk: agent-decided — preserve existing cases and narrow the personal-path ban to guidance; separately validate the exact dynamic command. Defect class: overbroad output assertion; search the entire named test and session-start output for instances.

**W1-02 Assess test dependency advisories** after: W1-01 acceptance: 4
- Files: `docs/loom/2026-11-10-document-path-test-scope/research/01-test-dependency-advisories.md`, `docs/loom/2026-11-10-document-path-test-scope/evidence/npm-audit.json`
- Test: A4 positive: lockfile-advisory-attribution; boundary: applicability-limitations.
- Risk: agent-decided — inspect the locked dependency graph and primary advisories; preserve unavailable evidence and uncertainty. No dependency edits or automatic remediation are authorized.

### Wave 2
**W2-01 Patch release metadata** after: W1-02 acceptance: 3
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README*.md`, `loom-code/tests/test_write_plan_station_text.py`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`
- Test: A3 positive: synchronized-3.62.2; boundary: unchanged-contract.
- Risk: agent-decided — patch bump because only tests change; add the 3.62.2 CHANGELOG entry, update README versions and pin test, derive manifests through scripts/sync_codex_manifests.py --all before finalization.

## Simplicity check
- none found

## Questions asked
① — what — 確認後會實作、測試與獨立審查；通過後自動推送並建立 Ready PR，不自動合併，發布前可撤回授權。這就是你要的範圍嗎？

## Risks
1. user-decided — retain runtime behavior, reject hardcoded guidance and incorrect launcher paths, assess vulnerabilities without changing dependencies, and publish a Ready PR after checks; merge is not authorized.
2. agent-decided — no spec: internal validation only, no consumed interface changes and no command/screen behavior details carried from intake.
3. agent-decided — full package tests run in the repository's locked isolated environment; retain skips and environmental limitations in evidence.
