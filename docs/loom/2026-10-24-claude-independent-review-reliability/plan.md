# Reliable Claude Code independent review — plan
intent: 2026-10-24-claude-independent-review-reliability@0743260432a8ecdfc4dd392b5bf236aeb050c1d0
spec: docs/loom/2026-10-24-claude-independent-review-reliability/spec.md@0d60f19069f9e7a0db64f778e5042f10f104f233
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

### Wave 5 — Recover presentation-only review output drift

**W5-01 Accept safe outside-review formatting**  after: W4-02  acceptance: 5
- Files: `loom-code/scripts/loom_checker/reviewers.py`, `loom-code/tests/test_loom_attestation.py`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/CHANGELOG.md`
- Test: A5 positive: whole_yaml_fence_and_unlabeled_text; boundary: raw_digest_preserved. A5 negative: trailing_prose, missing_or_blank_anchor, zero_line, absent_required_field, weak_dimension_score, contradictory_overall_verdict.
- Risk: agent-decided — use one bounded normalization at the owning receipt parser; leave semantic fields untouched and reject ambiguous repairs. Keep the already published 3.49.0 minor version, updating its pending changelog entry before renewed finalization.

**W5-02 Graduate the duplicate-key adversarial regression**  after: W5-01  acceptance: 5
- Files: `docs/loom/2026-10-24-claude-independent-review-reliability/evidence/probes/test_receipt_duplicate_verdict_rejected.py`, `loom-code/tests/test_adversarial_duplicate_outside_verdict.py`
- Test: A5 positive: duplicate_verdict_rejected; boundary: nested_duplicate_score_rejected.
- Risk: agent-decided — move the earned red probe into the normal package suite so future changes cannot silently restore last-key-wins parsing.

## Simplicity check

- Keep the Claude contract and runner in one task — taken
- Move live acceptance to Closing Review — taken
- Keep the existing YAML carrier — taken

## Questions asked

- none — the confirmed engineering intent arrived with the user's direct confirmation; no additional decision-point question was asked during spec or plan.

## Risks

1. The local private full-size fixture is temporary; the independent acceptance tester runs it during Closing Review and records only hashes, sizes, status, and model attribution.
2. A live Claude run transmits the authorized packet to Anthropic; use the already confirmed USD 6 cap and do not retry without fresh authorization.
3. Safe and restricted CLI flags are version-dependent; probe the installed CLI and keep synthetic tests separate from the live result.
4. Build ends with an independent adversary's committed executable cases, followed by the complete package suite before Closing Review.
5. The earlier review episode used its three digests. The newly confirmed intent starts a new episode. Retained Haiku/low output permits local parser testing, but not Opus/high live acceptance. No new external invocation is authorized.
