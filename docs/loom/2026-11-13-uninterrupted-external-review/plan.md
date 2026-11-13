# Uninterrupted explicit external review — plan
intent: 2026-11-13-uninterrupted-external-review@ab99fe978
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/skills/independent-advisor/SKILL.md` “Authorization and the single checkpoint” accepts a named request but does not explicitly forbid ending the turn after disclosure.
- Reverse: `loom-code/skills/closing-review/SKILL.md` “Before any network-backed discovery” already accepts the direct request; execution evidence alone is not an accepted verdict.
- Error: `loom-code/scripts/external_review.py` `_consent_valid` rejects missing records; historical Codex host approval refused three fully named review requests before execution.
- Data: `loom-code/scripts/external_review.py` `_authorization_valid` binds quoted request, executor and target; disclosures record shown facts, not another user answer.
- Boundary: `loom-code/scripts/external_review.py` executor choices are codex/claude/agy; host approval is outside that runner and must never be bypassed.

## Task DAG
### Wave 1 — Correct the existing execution contract
**W1-01 Remove confirmation-shaped pauses from explicit review requests** acceptance: 1, 2, 4
- Files: loom-code/skills/external-review/, loom-code/skills/closing-review/SKILL.md, loom-workflow/skills/independent-advisor/ (including references/dispatch-protocol.md and references/report-contract.md), loom-workflow/tests/independent-advisor/, loom-code/tests/test_external_review.py
- Test: A1 positive: direct-request-continues and unowned-artifact-review-with-unavailable-design-history; boundary: cancelled-request-stops and open-ended-consultation-retains-packet-completeness. A2 positive: disclosure-continues; negative: disclosure-question. A4 positive: refusal-reported-incomplete; negative: refusal-bypassed.
- Risk: agent-decided — preserve runner authorization schema and host approval; tighten the caller's continuation contract, not permissions. Preserve existing external-review and advisor tests; add targeted behavioral cases.

### Wave 2 — Validate the actual interruption boundary
**W2-01 Probe test for uninterrupted host execution** after: W1-01 acceptance: 1, 2, 3, 4
- Files: docs/loom/2026-11-13-uninterrupted-external-review/evidence/, loom-code/tests/local/
- Test: A1 positive: one-request-valid-review; negative: second-answer-required. A2 positive: disclosure-only; negative: disclosure-blocks. A3 positive: live-claude-result; negative: simulated-result. A4 positive: real-failure-retained; negative: false-completion.
- Risk: agent-decided — one Claude Sonnet/medium preflight and review with scoped project files; no conversation histories, secrets, retries or provider substitution. Host refusal fails acceptance rather than inviting a workaround.

### Wave 3 — Release and integration
**W3-01 Synchronize release metadata** after: W2-01 acceptance: 1
- Files: loom-code/.claude-plugin/plugin.json, loom-workflow/.claude-plugin/plugin.json, CHANGELOG.md, README.md, loom-code/, loom-workflow/, .claude-plugin/marketplace.json
- Test: A1 positive: release-metadata-synchronized; negative: old-version-left-behind.
- Risk: agent-decided — minor bumps for changed station guidance; use manifest sync script and existing release checks. No unrelated versions or installed-cache edits.

## Simplicity check
- none found

## Questions asked
① — consequence — 是否確認這個範圍？ 確認也授權檢查通過後推送分支、建立 PR；合併仍需另外同意，你可在發布前取消。

## Risks
1. Host automatic approval is independent of Loom consent. If it still requires another user answer, Acceptance 3 fails; never publish a semantic pass based only on unit tests.
2. Private session evidence remains local: use the already-inspected research record for local diagnosis only; omit it from the external packet and publication commits.
3. agent-decided — GO: repeated verified interruptions warrant a bounded correction. No new consent mechanism, schema, executor, global approval setting or promise to suppress platform policy.
4. user-decided — The confirmed intent permits a bounded live Claude Code review of this repair's code/tests to Anthropic, cost unknown, and later publication after checks; merge remains separate.
