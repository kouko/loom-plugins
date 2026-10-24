# Reliable Claude Code independent review — plan
intent: 2026-10-24-claude-independent-review-reliability@43470b27e359b7c87173a2cac28f8e302d76eb2d
spec: docs/loom/2026-10-24-claude-independent-review-reliability/spec.md@bf89ee1ce7d78e4835c390e626e2c01e672d8d24
charter: 1.1

## Task DAG

### Wave 1 — Claude execution boundary

**W1-01 Bound Claude execution and classify rapid refill**  after: none  acceptance: 1, 2, 3, 4
- Files: `loom-code/scripts/external_review.py`, `loom-code/skills/external-review/SKILL.md`, `loom-code/tests/test_external_review.py`, `loom-code/tests/test_external_failure_terminal_envelope.py`
- Test: A1 positive: full_profile; boundary: model_attribution. A2 positive: restricted_root; negative: outside_root_denied. A3 positive: rapid_refill_nonzero; boundary: rapid_refill_zero_exit. A4 positive: other_executors; negative: stale_consent.
- Risk: agent-decided — implement REQ-1–4 at the existing runner entry; align Claude disclosure, preserve covered test cases, and avoid global user settings.

### Wave 2 — Release metadata

**W2-01 Synchronize release metadata**  after: W1-01  acceptance: 1, 2, 3, 4
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/README*.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A1 positive: released_runner; boundary: version_sync. A2 positive: documented_boundary; negative: stale_disclosure. A3 positive: documented_failure; negative: raw_content. A4 positive: release_tests; negative: unsynced_manifest.
- Risk: agent-decided — apply a minor bump for the changed runtime contract after implementation so closing-review attests the final release content.

### Wave 3 — Preserve the adversarial regression

**W3-01 Graduate the failed-result privacy probe**  after: W1-01, W2-01  acceptance: 3
- Files: `docs/loom/2026-10-24-claude-independent-review-reliability/evidence/probes/test_adversarial_claude_probe_model_key_privacy.py`, `loom-code/tests/test_adversarial_claude_probe_model_key_privacy.py`
- Test: A3 positive: hostile_model_key_red_then_green; boundary: failed_review_contains_no_probe_text.
- Risk: agent-decided — move the proven adversarial program into the package suite unchanged so REQ-3 remains guarded on later changes.

### Wave 4 — Closing review findings

**W4-01 Align owner retry authorization**  after: W3-01  acceptance: 3, 4
- Files: `loom-code/skills/closing-review/SKILL.md`, `loom-code/tests/test_closing_review_recovery_rules.py`
- Test: A3 positive: rapid_refill_stops; negative: silent_retry. A4 positive: fresh_authorization; boundary: malformed_output_retry.
- Risk: agent-decided — close the reviewer-found retry contradiction in both owner clauses while preserving the existing bounded episode rule.

**W4-02 Ground the Claude CLI profile**  after: W4-01  acceptance: 1, 2
- Files: `loom-code/scripts/external_review.py`, `loom-code/tests/test_external_review.py`
- Test: A1 positive: documented_full_profile; boundary: model_attribution. A2 positive: documented_root_boundary; negative: outside_grant.
- Risk: agent-decided — cite the official CLI contract beside the existing flags without changing their behavior or adding a new profile.

## Simplicity check

- Keep the Claude contract and runner in one task — taken
- Move live acceptance to Closing Review — taken

## Questions asked

- none — the confirmed engineering intent arrived with the user's direct confirmation; no additional decision-point question was asked during spec or plan.

## Risks

1. The local private full-size fixture is temporary; the independent acceptance tester runs it during Closing Review and records only hashes, sizes, status, and model attribution.
2. A live Claude run transmits the authorized packet to Anthropic; use the already confirmed USD 6 cap and do not retry without fresh authorization.
3. Safe and restricted CLI flags are version-dependent; probe the installed CLI and keep synthetic tests separate from the live result.
4. Build ends with an independent adversary's committed executable cases, followed by the complete package suite before Closing Review.
