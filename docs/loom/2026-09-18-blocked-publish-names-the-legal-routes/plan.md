# Blocked publication names the legal routes — plan
intent: 2026-09-18-blocked-publish-names-the-legal-routes@3bdaa258
spec: docs/loom/2026-09-18-blocked-publish-names-the-legal-routes/spec.md@fe52c3a4
charter: 1.0

## Task DAG

**W0-01 Extend the publication refusal with both legal routes**  after: none  acceptance: 1, 6
- Files: loom-code/scripts/loom_checker/command_handlers/push.py, loom-code/scripts/test_loom_publish.py, loom-code/scripts/test_adversarial_push_reason.py
- Test: A1 positive: test_missing_attestation_names_both_routes; negative: test_missing_attestation_reason_stays_one_line. A6 positive: test_hostile_unattested_pushes_stay_block_prefixed; boundary: test_unattested_unconfirmed_push_still_refused.
- Risk: a wrapped reason breaks the BLOCK-prefix assertion; spec Design decision pins one line and leaves report() untouched. agent-decided.

**W0-02 Extend the merge refusal with the same routes**  after: W0-01  acceptance: 2
- Files: loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/test_ship_worktree_merge.py
- Test: A2 positive: test_merge_refusal_names_both_routes; negative: test_merge_without_attestation_still_refused.
- Risk: land refuses before the shared check, so the earlier site carries the text; spec Design decision names the site. agent-decided.

**W1-01 Record the no-handover rule in the ship station**  after: W0-01  acceptance: 3
- Files: loom-code/skills/ship/SKILL.md, loom-code/scripts/test_ship_station_text.py
- Test: A3 positive: test_ship_prose_forbids_handing_the_command_over; negative: test_ship_prose_rule_is_not_marked_as_a_gate.
- Risk: prose is advisory and never the primary carrier; spec Design decision pins the refusal string as the carrier. agent-decided.

**W1-02 Cover the confirmed-skip publication path**  after: W0-01  acceptance: 4
- Files: loom-code/scripts/test_loom_publish.py
- Test: A4 positive: test_confirmed_skip_publishes_with_disclosure; negative: test_body_without_disclosure_refused_when_selection_bound.
- Risk: exercised through the existing external-command seams, never a live GitHub call; spec Current state evidence names the seam. agent-decided.

**W2-01 Publish and merge this change without a user-typed git command**  after: W0-02, W1-01, W1-02  acceptance: 5, 7, 8
- Files: docs/loom/2026-09-18-blocked-publish-names-the-legal-routes/blind-run-report.md
- Test: A5 positive: probe-publish-executed-by-agent; negative: probe-no-user-typed-git-command. A7 positive: probe-actor-named-per-action; boundary: probe-merge-actor-named. A8 positive: probe-package-suite-green; negative: probe-no-assertion-removed.
- Risk: the report is produced by the blind runner at closing review, not by an implementer; the merge line is observed at ship after acceptance. agent-decided.

## Questions asked
① — what — 要動哪幾層：改 dotfiles 的 CLAUDE.md 規則、改 dotfiles 的拒絕清單、改 loom 的攔截訊息，還是只做其中一項？
① — consequence — 推送閘門要改成哪一種：降級為警告、整個移除攔截、或只在跳站時降級？
① — what — 重述確認：沒有驗證紀錄時閘門印警告後放行，PR 內文與 GitHub 狀態兩道保留擋，對嗎？
① — consequence — 審查揭露的後果變了，這個變更要走哪一條：讓合法跳站變好用、照原訂降級為警告、還是先做前者把後者留成待辦？
① — what — 重述確認：發佈被擋的當下，agent 手上就有能自己接續的資訊，不准把指令丟回給使用者，對嗎？

## Risks
1. The refusal text is read by agents in every adopting repository; a wording change that drops the existing reason would silently weaken the gate, so the existing text is extended rather than replaced.
2. The ship station rule cannot be recomputed, so it must never be cited as a gate; the refusal string is the enforceable carrier and the prose only covers a pre-emptive decline.
3. W2-01's merge line is observed after the user accepts, so the blind-run report records the publication evidence and names the merge as the remaining action.
