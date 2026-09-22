# Publication floor moves to GitHub — plan
intent: 2026-09-22-publication-floor-moves-to-github@71377548
spec: docs/loom/2026-09-22-publication-floor-moves-to-github/spec.md@cc6616a3
charter: 1.0

Current state evidence lives in the spec's `## Current state evidence`; each
Risk line points at the spec's Design decision by REQ id rather than restating it.

## Task DAG

**W0-01 Body validator names the offending heading**  after: —  acceptance: 5
- Files: `loom-code/scripts/loom_checker/rule_checks/publish.py`, `loom-code/scripts/test_loom_publish.py`
- Test: A5 positive: missing-heading-named; boundary: duplicated-out-of-order-and-empty-each-named.
- Risk: `test_loom_publish.py` pins the generic sentence; preserve every refused shape, only the message narrows to one heading. REQ-5 decision; agent-decided.

**W0-02 Identify the change and compute verification status**  after: —  acceptance: 3, 10
- Files: `loom-code/scripts/loom_checker/verification.py`, `loom-code/scripts/loom_checker/attestation.py`, `loom-code/scripts/test_verification_status.py`
- Test: A3 positive: skip-set-reports-valid-skipped; negative: two-attestations-and-bad-json-are-stale. A10 positive: absent-lists-missing-records; boundary: unidentified-branch-named.
- Risk: status never refuses; CI depth must not call selection-record comparison. REQ-3, REQ-10 decisions; agent-decided.

**W1-01 Publish discloses instead of refusing**  after: W0-01, W0-02  acceptance: 5, 10
- Files: `loom-code/scripts/loom_checker/command_handlers/publish.py`, `loom-code/scripts/loom_checker/rule_checks/publish.py`, `loom-code/scripts/test_loom_publish.py`, `loom-code/scripts/test_adversarial_blocked_publish_routes.py`
- Test: A5 positive: bad-body-refused-before-push; negative: good-body-no-attestation-publishes. A10 positive: status-and-skip-lines-in-body; boundary: skipped-by-instruction-without-attestation-accepted.
- Risk: `test_adversarial_blocked_publish_routes.py` encodes zero-attestation refusals; narrows them to body and unidentified-change refusals only. REQ-5, REQ-10; agent-decided.

**W1-02 Land checks the live body and discloses**  after: W0-01, W0-02  acceptance: 6
- Files: `loom-code/scripts/loom_checker/command_handlers/land.py`, `loom-code/scripts/loom_checker/rules.py`, `loom-code/scripts/test_land_merge.py`
- Test: A6 positive: no-attestation-good-body-merges-with-reminder; negative: missing-heading-refuses-names-it.
- Risk: `test_land_merge.py` pins attestation-at-HEAD refusal; narrowed to body, acceptance and unidentified refusals; PR, checks, mergeable preconditions preserved. REQ-6; agent-decided.

**W1-03 Hook allows and reminds, parser shrinks**  after: W0-02  acceptance: 4, 12
- Files: `loom-code/scripts/loom_checker/command_handlers/push.py`, `loom-code/scripts/loom_checker/rule_checks/push.py`, `loom-code/scripts/loom_checker/rules.py`, `loom-code/scripts/test_publish_command_detection.py`, `loom-code/scripts/test_adversarial_push_reason.py`
- Test: A4 positive: direct-push-reminds-exit-0; boundary: wrapped-push-silent-exit-0. A12 positive: grep-echo-commit-silent; negative: direct-merge-reminds.
- Risk: deletes refusal-only parsing; keep helpers imported by `selection_guard.py`, `publish.py`, `land.py`; `test_selection_guard.py` must stay green unchanged. REQ-4, REQ-12; agent-decided.

**W1-04 Host fallbacks allow except the selection store**  after: W1-03  acceptance: 4
- Files: `loom-code/hooks/hooks-codex.json`, `loom-code/hooks/agy_adapter.py`, `loom-code/scripts/test_agy_adapter.py`, `loom-code/scripts/test_adversarial_agy_adapter.py`, `loom-code/scripts/test_codex_hook_trust_contract.py`
- Test: A4 positive: missing-checker-allows-push-on-both-hosts; negative: missing-checker-denies-selection-store-write.
- Risk: fail-open fallback must not loosen `selection.guard`; existing deny tests narrowed to selection paths. REQ-4 host-fallback decision; agent-decided.

**W1-05 Read-only pr-floor subcommand**  after: W0-01, W0-02  acceptance: 1, 3
- Files: `loom-code/scripts/loom_checker/command_handlers/pr_floor.py`, `loom-code/scripts/loom_checker.py`, `loom-code/scripts/loom_checker/rules.py`, `loom-code/scripts/test_pr_floor.py`
- Test: A1 positive: bad-body-exit-1-names-heading; negative: good-body-exit-0. A3 positive: status-in-summary-and-notice; negative: body-status-text-ignored.
- Risk: runs in CI on untrusted PR content; reads files and event body only, never executes PR code. REQ-1, REQ-3; agent-decided.

**W1-06 github-rules probe and setup printer**  after: —  acceptance: 2, 7, 8
- Files: `loom-code/scripts/loom_checker/command_handlers/github_rules.py`, `loom-code/scripts/loom_checker.py`, `loom-code/scripts/test_github_rules.py`
- Test: A2 positive: setup-json-requires-pr-with-empty-bypass; boundary: classic-without-enforce-admins-reported-missing. A7 positive: missing-rules-listed-with-command; negative: template-absent-withholds-ruleset. A8 positive: unreadable-could-not-confirm; boundary: rulesets-empty-classic-unreadable-unconfirmed.
- Risk: `gh api` stubbed in tests; bypass_actors visibility and check context unverified live until the blind run. REQ-2, REQ-7, REQ-8; agent-decided.

**W2-01 CI template and reusable workflow**  after: W1-05  acceptance: 9
- Files: `loom-code/templates/loom-pr-floor.yml`, `.github/workflows/loom-pr-floor-reusable.yml`, `.github/workflows/loom-pr-floor.yml`, `loom-code/scripts/test_pr_floor_workflow.py`
- Test: A9 positive: template-uses-pull-request-target-and-context-constant; negative: template-grants-only-contents-read.
- Risk: live behaviour only provable on GitHub; blind run lands the template before its test PR. REQ-9 template-first; agent-decided.

**W2-02 Station prose: skip by words, probe, disclosure**  after: W1-01, W1-02, W1-06  acceptance: 7, 10
- Files: `loom-code/skills/ship/SKILL.md`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/skills/build/SKILL.md`, `loom-code/skills/using-loom-code/SKILL.md`, `loom-code/scripts/test_ship_station_text.py`, `loom-code/scripts/test_simplified_station_text.py`
- Test: A7 positive: ship-runs-github-rules-before-publish; negative: ship-never-runs-setup-unasked. A10 positive: skip-announced-in-one-line; negative: no-generated-code-requested.
- Risk: expert-mode left intact; prose must not say a code is required anywhere. REQ-7, REQ-10; agent-decided.

**W2-03 Amend non-negotiable 2**  after: —  acceptance: 11
- Files: `PRINCIPLES.md`, `loom-code/scripts/test_principles_amendment.py`
- Test: A11 positive: nn2-states-pr-disclosure-and-ratified-line-appended; negative: typed-confirmation-clause-gone.
- Risk: amendment text fixed by the spec; ratified-by line is appended, never rewritten. REQ-11; user-decided.

**W3-01 Rule inventory, release metadata, suite green**  after: W1-01, W1-02, W1-03, W1-04, W1-05, W1-06, W2-01, W2-02, W2-03  acceptance: 13
- Files: `docs/loom/evidence/mechanisms.yaml`, `loom-code/scripts/loom_checker/rules.py`, `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/README.md`, `README.md`
- Test: A13 positive: package-runner-exits-0; negative: net-mechanism-count-not-raised.
- Risk: minor bump 3.8.0 (rule ids change); localized READMEs bump too; check_mechanisms baseline origin/main. Mechanism ids decision; agent-decided.

## Questions asked
① — what — PR 內文要維持九個章節，還是放寬到只要求「做了什麼」和「為什麼」？ — 「PR 內文先維持九個章節」
① — consequence — PRINCIPLES.md 第 2 條：修改為只需 PR 揭露（A），或維持打字確認改用固定指令（B）？ — 「A」（經「A 方案只要用口語就可以跳過任何步驟？」確認：「對」）
① — what — 跳過步驟時的行為 — 「希望 agent 可以在跳過的時候給使用者提醒（但是不擋流程繼續執行）」
① — consequence — 回答「是」授權之後的非強制推送與 Ready PR，合併另為一個決定 — 「是」

## Risks
1. The change removes the only local refusal of zero-attestation publication; the floor then rests on GitHub rules the user must apply. Ship's probe makes their absence visible every run.
2. Three GitHub behaviours are unverified live: the check context string, read-only visibility of `bypass_actors`, and notice rendering. The blind run needs a rules-bearing repository, which requires the user's consent.
3. Applying the rule set to kouko/loom-plugins is outward-facing and not performed by Build; agent-decided — not authorised, took the conservative option.
4. Deleting refusal-only parsing touches many tests; each rewritten test must keep the non-refusal cases it pinned.
