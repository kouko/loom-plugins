# Claude Code external-review recovery — plan
intent: 2026-10-22-claude-review-diagnostics@13a12c32fb0a868faf87f9519464397f65405e48
spec: docs/loom/2026-10-22-claude-review-diagnostics/spec.md@bd2140c28775bfc12e9f5295368a030610e9aa26
charter: 1.1

## Task DAG

**W0-01 Classify Claude execution failures safely**  after: none  acceptance: 1, 2, 3
- Files: loom-code/scripts/external_review.py, loom-code/tests/test_external_review.py
- Test: A1 positive: completed_claude_review; boundary: preflight_only. A2 positive: known_failure_action; negative: unknown_output_no_leak. A3 positive: consented_other_executor; negative: failed_review_no_verdict.
- Risk: agent-decided — preserve exercised cases in `test_external_review.py`; widen only Claude diagnosis under REQ-2, leaving authorization and completion semantics under REQ-1/3 intact.

**W1-01 Explain failure and recovery to review owners**  after: W0-01  acceptance: 2, 3
- Files: loom-code/skills/external-review/SKILL.md, loom-code/tests/test_external_review.py
- Test: A2 positive: known_failure_guidance; boundary: unknown_failure_guidance. A3 positive: consent_guidance_retained; negative: no_failed_verdict.
- Risk: agent-decided — document only the safe result and next action under REQ-2/3; no raw error relay, silent retry, or provider fallback.

**W2-01 Synchronize the plugin release**  after: W1-01  acceptance: 2
- Files: loom-code/plugin.json, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/package.json, loom-code/CHANGELOG.md, loom-code/README*.md, README.md, loom-code/tests/test_write_plan_station_text.py
- Test: A2 positive: release_metadata_synchronized; boundary: stale_version_pin.
- Risk: agent-decided — use a minor bump for changed review guidance and result contract; complete it before final attestation so the published version identifies the fix.

**W3-01 Keep the caught zero-exit error case in the suite**  after: W0-01, W2-01  acceptance: 2, 3
- Files: docs/loom/2026-10-22-claude-review-diagnostics/evidence/probes/test_claude_error_result.py, loom-code/tests/test_adversarial_claude_error_result.py
- Test: A2 negative: zero_exit_error_keeps_private_text_out; A3 negative: zero_exit_error_has_no_review_verdict; the graduated program passes both as a standalone unittest and in the package suite.
- Risk: agent-decided — move the adversary's already RED-then-GREEN case into the package suite before finalization, preserving its `concern:` and adapting only its repository-root lookup.

## Simplicity check
- Reuse the existing external-review test module for skill guidance; it already reads this skill — taken

## Questions asked
① — what — 這是你要修的範圍嗎？

## Risks
1. The prior Claude failure's raw output was discarded, so its exact cause is unproven; use public synthetic material for any live CLI trial and report external-service limits separately.
2. Unknown failures remain unknown until the local diagnostic action identifies them; never infer a provider outage, account issue, or code defect from exit code alone.
