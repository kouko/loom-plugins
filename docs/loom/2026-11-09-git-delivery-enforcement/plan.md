# Git delivery enforcement — plan
intent: 2026-11-09-git-delivery-enforcement@4c555b14
spec: docs/loom/2026-11-09-git-delivery-enforcement/spec.md@8274b2a3
charter: 1.1

## Task DAG

### Wave 1 — Reuse existing observation and protection owners

**W1-01 Observe delivery and return actionable publication results** after: none acceptance: 1, 2, 5, 6
- Files: loom-code/scripts/loom_checker/command_handlers/publish.py, loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/loom_checker.py, loom-code/tests/test_delivery.py, loom-code/tests/test_loom_publish.py, loom-code/tests/test_land_merge.py
- Test: A1 positive: matching_remote_pr; boundary: newer_local_head. A2 positive: local_without_network; negative: missing_authorization. A5 positive: checks_pass; negative: failed_json. A6 positive: actionable_result; boundary: unavailable_remote.
- Risk: agent-decided — reuse current observations per REQ-1/2/5/6; preserve existing test_loom_publish.py and test_land_merge.py coverage, required-only versus all-check policy, trust roots and bounded waits; no generic recovery engine.

**W1-02 Protect ordinary native Git operations without parsing shell text** after: W1-01 acceptance: 3, 6
- Files: loom-code/scripts/loom_checker/command_handlers/push.py, loom-code/tests/test_native_git_protection.py, loom-code/tests/test_main_branch_hook.py
- Test: A3 positive: feature_commit_and_trunk_sync; negative: compound_main_commit_and_push. A6 positive: protection_remedy; boundary: foreign_hooks_unchanged.
- Risk: agent-decided — REQ-3/6 uses static shell hooks without launcher/cache dependency; test scoped installation, linked worktrees, foreign hooks and history-operation limits. Preserve test_main_branch_hook.py coverage and existing shell-only opt-out. No real-repository installation.

### Wave 2 — Connect host framing and server-policy observations

**W2-01 Connect delivery checks to existing host adapters** after: W1-02 acceptance: 1, 2, 6, 7
- Files: loom-code/scripts/loom_checker/command_handlers/publish.py, loom-code/hooks/hooks.json, loom-code/hooks/hooks-codex.json, loom-code/hooks/session-start, loom-code/tests/test_delivery_stop.py, loom-code/tests/test_hooks_json.py, loom-code/tests/test_opencode_loader.py, loom-code/tests/test_agy_adapter.py
- Test: A1 positive: premature_stop_continues; negative: unpublished_completion. A2 positive: revoked_authorization_stops; boundary: acceptance_question. A6 positive: stop_remedy; boundary: repeated_stop. A7 positive: packaged_opencode_execution; negative: unsupported_stop_claim.
- Risk: agent-decided — REQ-7 and research/01-host-termination-capabilities.md distinguish documented Stop from disclosure-only hosts; preserve hook identity/trust boundaries and test_hooks_json.py behavior. No undocumented OpenCode event or endless continuation.

**W2-02 Verify effective server protection and diagnostic remedies** after: W2-01 acceptance: 4, 6
- Files: loom-code/scripts/loom_checker/command_handlers/github_rules.py, loom-code/tests/test_github_rules.py
- Test: A4 positive: nonbypassable_rules; negative: bypass_or_unreadable_rules. A6 positive: missing_rule_remedy; boundary: malformed_response.
- Risk: agent-decided — REQ-4 preserves advisory-only setup and test_github_rules.py cases; widen bypass/unknown coverage rather than applying real server changes. Acceptance separates fixtures from live GitHub evidence.

### Wave 3 — Policy, executable accounting and release

**W3-01 Align policy and publish the protected workflow contract** after: W2-02 acceptance: 1, 3, 4, 6, 7
- Files: PRINCIPLES.md, loom-code/skills/ship/SKILL.md, loom-design/skills/capture-intent/SKILL.md, loom-code/contract/manifest.yaml, loom-code/scripts/loom_checker/rules.py, docs/loom/evidence/mechanisms.yaml, loom-code/tests/test_ship_station_text.py, loom-design/tests/spec/test_capture_intent_contract.py
- Test: A1 positive: observed_handoff; negative: claimed_publication. A3 positive: native_policy; boundary: local_exception. A4 positive: explicit_setup; negative: implicit_mutation. A6 positive: scoped_next_action; boundary: no_bypass. A7 positive: shared_entry; negative: small_change_exemption.
- Risk: agent-decided — revise only affected policies per REQ-1/3/4/6/7; executable registration and mechanism-budget exception required. Existing station tests retain polarity; release packet below precedes final attestation.

### Integration — Fetched trunk compatibility

**I-01 Integrate fetched trunk and preserve both release contracts** after: W3-01 acceptance: 7
- Files: README.md, docs/loom/evidence/mechanisms.yaml, loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, loom-code/tests/test_write_plan_station_text.py; derived manifests via sync script only.
- Test: A7 positive: synchronized_release; boundary: preserved_trunk_contract. Run affected release, mechanism, contract and station suites.
- Risk: agent-decided — sync-trunk refused conflicts against 361ef5d2 without mutation. Merge fetched trunk preserving its research capability; move this release to 3.62.0. Isolated worktree preserves unrelated untracked user work. No requirements or review-budget reset.

### Adversarial fix tasks

**F-01 Use unambiguous branch identities across Git delivery consumers** after: I-01 acceptance: 1, 3
- Files: loom-code/scripts/loom_checker/command_handlers/push.py, loom-code/scripts/loom_checker/command_handlers/publish.py, loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/loom_checker/helpers.py, loom-code/tests/test_main_branch_hook.py, loom-code/tests/test_delivery.py
- Test: A3 negative: adversarial same-name tag probe must turn GREEN; A1 positive: delivery branch identity remains exact.
- Risk: agent-decided — class: ambiguous shortened branch identity. Whole changed-file sweep plus A1/A3 Git identity surfaces found push native/shell, four publish calls, two land calls and helpers.branch_base. Compare full heads refs; preserve detached behavior. Commit names class and searched surfaces.

**F-02 Graduate the caught native-hook probe into the package suite** after: F-01 acceptance: 3
- Files: docs/loom/2026-11-09-git-delivery-enforcement/evidence/probes/test_native_ambiguous_branch.py, loom-code/tests/test_native_ambiguous_branch.py
- Test: A3 negative: same three demonstrated RED cases pass from their permanent suite location.
- Risk: agent-decided — adversary retains authorship; move its caught program and adjust only location-dependent import. No new attack, assertion or review round.

### Package integration fixes

**F-03 Preserve single-line BLOCK diagnostic framing with actionable remedies** after: F-02 acceptance: 6
- Files: loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/loom_checker/command_handlers/publish.py, loom-code/tests/test_land_merge.py, loom-code/tests/test_loom_publish.py, loom-code/tests/test_ship_worktree_merge.py
- Test: A6 negative: existing blocked-publish adversarial tests remain unchanged and pass; positive: exact diagnostics retain next actions.
- Risk: agent-decided — class: actionable advice broke legacy BLOCK-line framing. Sweep found publish refusal helper, land refusal helper, direct external-error branches and precheck branch. Keep each refusal a BLOCK line with advice inline; preserve reason prefix, rule and exit.

**F-04 Synchronize exact integration inventories for new public surfaces** after: F-03 acceptance: 7
- Files: tests/test_loom_plugin_install_layout.py, loom-code/tests/test_loom_checker_cli.py, loom-code/tests/test_loom_checker_modules.py, loom-code/tests/test_legacy_contract_removed.py
- Test: A7 positive: exact command/rule/host inventories match the new supported surfaces; negative: removed replay flag stays rejected.
- Risk: agent-decided — class: stale exact integration inventories. Sweep found rule count/list/areas, delivery owner mapping, isolated Codex Stop inventory and push usage text. Keep exactness and negative polarity; no weakening to subsets or arbitrary counts.

**F-05 Remove the new prose-only phrase pin** after: F-04 acceptance: 7
- Files: loom-code/tests/test_ship_station_text.py
- Test: A7 negative: existing batch2 phrase-pin adversarial scanner passes; executable delivery and mechanism checks retain behavior coverage.
- Risk: agent-decided — class: prohibited positive phrase-loop pin. Changed-file sweep found only the newly added Ship handoff phrase-loop test. Remove that redundant test rather than disguising its literals or changing the scanner; production and executable registration tests stay.

### Acceptance evidence fix

**F-06 Exercise configured remote refusal with a shared-rule server fixture** after: F-05 acceptance: 4
- Files: loom-code/tests/test_github_rules.py
- Test: A4 positive: passing_required_check_merge; negative: remote_direct_push_and_failed_check_merge_refused_without_local_hooks.
- Risk: agent-decided — class: missing configured-server refusal evidence. Sweep found only JSON stubs and local refusals in github-rules/native/land tests. Share configuration for observation and remote decisions; verify unchanged trunk/PR on refusal and passing-check control. Simulation only.

## Simplicity check
- none found

## Questions asked
① — what — 以上是否就是你要的？ 回覆「是」也授權這次變更通過審查後自動推送功能分支並開 Ready PR；合併仍等你驗收，發布前也可撤回授權。

## Risks
1. Native Git hooks affect human operations too. User chose this boundary; refuse shared/foreign hooks and preserve work. Existing no-Git-hooks principle is explicitly superseded, not silently contradicted.
2. Host support differs. Claude/Codex Stop gets bounded recovery; OpenCode/Antigravity use executable checks and explicit limitations. Live-host evidence must not be replaced with a configuration assertion.
3. External Claude complexity review completed after explicit Anthropic-egress approval: RESHAPE. Adopt shared CI classification and static Git hooks; unify immediate revocation in existing authorization logic. This proposal review does not certify the later implementation.
4. Release packet: bump loom-code and loom-design source .claude-plugin/plugin.json minor versions, add same-commit CHANGELOG sections dated 2026-11-09, synchronize README versions and release-pin tests, then derive manifests with scripts/sync_codex_manifests.py --all.
5. Any net mechanism increase gets a named budget-exception in the release entry. Count final runtime/functions/tests against evidence/complexity-analysis.md rather than treating estimates as achieved reductions.
6. Repository package command remains the locked isolated Loom-family runner. Use a writable temporary UV_CACHE_DIR when sandbox cache access is unavailable; no base-environment package installation.
7. Round 3 reached NON_CONVERGENT. User A authorized one limited supplemental check by the same reviewer: PASS for 3e9b3007..8274b2a3. Preserve prior rounds; resume Build with validated default identity. This exception does not reset later budgets.
