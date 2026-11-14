# Post-merge delivery guidance — plan
intent: 2026-11-14-post-merge-delivery-guidance@dbec38f57
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/session-start:94` requires branch-dependent delivery before completion without a post-cleanup exception.
- Reverse: `loom-code/skills/ship/SKILL.md:Handoff` requires observation before reporting, then allows land evidence after cleanup.
- Error: `loom-code/scripts/loom_checker/command_handlers/publish.py:observe_delivery` always recommends branch naming when identification fails.
- Data: `loom-code/scripts/loom_checker/verification.py:identify_change` resolves current branch identity before validating an optional intent path.
- Boundary: `loom-code/scripts/loom_checker/command_handlers/land.py:_land_accepted` prints merge before verification; `execute_cleanup` may print next-directory guidance after failure.

## Task DAG

### Wave 1 — Guidance and diagnostic

**W1-01 Align completion guidance and unidentified-change diagnostics** after: none acceptance: 1, 2, 3, 4, 5
- Files: `loom-code/hooks/session-start`, `loom-code/skills/ship/SKILL.md`, `loom-code/scripts/loom_checker/command_handlers/publish.py` (entry: cmd_delivery), `loom-code/tests/test_delivery.py`, `loom-code/tests/test_delivery_stop.py`, `loom-code/tests/test_ship_station_text.py`
- Test: A1 positive: cleaned-completion; negative: incomplete-work. A2 positive: unidentified-guidance; negative: no-evidence. A3 positive: retained-branch; boundary: silent-stop. A4 positive: partial-cleanup; negative: merge-line-only. A5 positive: same-change; negative: unrelated-success.
- Risk: agent-decided — replace guidance only, preserving observer state and authorization. Existing test_delivery.py and test_delivery_stop.py coverage remains unchanged; added cases cover main, missing evidence, and conditional completion guidance without inventing historical lookup.

### Wave 2 — Release synchronization

**W2-01 Synchronize release metadata** after: W1-01 acceptance: 3
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README.md`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A3 positive: synchronized-release; negative: stale-version.
- Risk: agent-decided — minor bump for station guidance; generate derived manifests with scripts/sync_codex_manifests.py, and preserve unrelated metadata.

### Wave 3 — Build integration

**W3-01 Integrate upstream CLI release without losing completion guidance** after: W2-01 acceptance: 1, 2, 3, 4, 5
- Files: `README.md`, `loom-code/README*.md`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/package.json`, `loom-code/plugin.json`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A1 positive: cleaned-completion; negative: incomplete-work. A2 positive: unidentified-guidance; negative: no-evidence. A3 positive: synchronized-release; boundary: retained-advice. A4 positive: partial-cleanup; negative: merge-line-only. A5 positive: same-change; negative: unrelated-success.
- Risk: agent-decided — sync-trunk fetched upstream 3bf50711f after W2 and refused overlapping release updates without changing work. Preserve upstream CLI advice and all prior acceptance obligations; existing test_delivery.py covers the retained observer entry and tests remain unchanged.

### Wave 4 — Confirmation bookkeeping repair

**W4-01 Correct confirmation bookkeeping identity** after: W3-01 acceptance: 3
- Files: `docs/loom/intent/2026-11-14-post-merge-delivery-guidance.md`, `docs/loom/2026-11-14-post-merge-delivery-guidance/plan.md`
- Test: A3 positive: unchanged-canonical-identity; negative: invalid-confirmation-pin. Direct check_intent_version reproduces the recorded refusal, then accepts the repaired pin; canonical bytes match the original confirmation.
- Risk: agent-decided — correct only the pin and this plan reference; preserve all Acceptance surfaces, original user confirmation and historical evidence.

## Simplicity check
- none found

## Questions asked
① — what — 確認照這個範圍進行嗎？
① — what — 確認照此範圍進行嗎？

## Risks
1. agent-decided — same-change complete land execution is required for successful cleanup; merged-only output and next-directory output are insufficient. Partial cleanup retains explicit failure and existing cleanup recovery, without blanket success.
2. agent-decided — preserve unconfirmed exit 1 on unidentified delivery, even with an intent argument. No new status, selector, persistent receipt, or remote lookup is introduced.
3. user-decided — the confirmed minimal scope excludes historical PR lookup, merging changes, installed plugin edits, and Obsidian project edits.
4. agent-decided — guidance semantics require independent acceptance testing; text guards alone cannot prove agent behavior. Use fresh clean-environment scenarios at closing review, including partial failures and unrelated prior success.
5. agent-decided — preserve existing required full package suite and native independent review. second-vendor remains suggest; no outside executor has been authorized.
6. agent-decided — W3 is upstream integration, not changed requirements or a retry-budget reset. Upstream 3.79.0 adds advisory fields; keep them and release this station-guidance change as 3.80.0, including translated README versions.
7. agent-decided — W4 corrects a status-inclusive confirmation hash. Canonical content, requirements, scope and authorization remain unchanged. Preserve the failed finalization evidence; refresh acceptance and the same reviewers without resetting the episode.
