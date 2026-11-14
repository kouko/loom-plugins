# Evidence-grounded next action — acceptance test evidence

Tried on 2026-11-15, in a clean copy of the project at 838c09d367f3d0b549ded9193e7d8fa3590391ba.

## Clean copy and load
- A fresh detached worktree command failed: `git -C /private/tmp/loom-whats-next worktree add --detach /private/tmp/whats-next-acceptance-clean 838c09d367f3d0b549ded9193e7d8fa3590391ba`.
- Output: `fatal: could not create directory of '/Users/kouko/GitHub/loom-plugins/.git/worktrees/whats-next-acceptance-clean': Operation not permitted`.
- Recovery: exported the exact committed tree using `git archive <tested HEAD> -o /private/tmp/whats-next-acceptance.tar`, extracted into the previously absent clean directory. No uncommitted product files were copied. This is a clean committed source snapshot, not a host installation.
- Read root README installation and development instructions. User-level marketplace/plugin installation is explicitly out of scope. Loaded the exported SKILL.md directly in a fresh native agent and exercised the real OpenCode loader in focused tests.
- System Python first failed with `No module named pytest`. Offline isolated temporary UV cache lacked execnet==2.1.2; default UV cache write failed with `Operation not permitted`. No dependencies were installed.
- Used an already available isolated cached environment: `/private/tmp/loom-uv-research/archive-v0/2IzJ2_mRHlKchzsb/bin/python -m pytest -q loom-workflow/tests/whats-next/test_contract.py tests/test_readme_navigation.py loom-code/tests/test_opencode_loader.py`, cwd clean snapshot.
- Captured result: `28 passed in 6.70s`. This covers source discovery/relative references, README navigation, and actual Node loader inventory. It does not establish an installed host's selection behavior.
- Full suite was NOT executed by this tester. Its command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; the automated test suite runs before acceptance and blocks acceptance on failure through finalization.

## Fresh native execution provenance
- Agent: /root/whats_acceptance/accept_behavior, fork_turns none; no authoring context.
- Installed dispatch_profile resolver input: initial, main model/effort null, task trust_boundary true, capabilities {}, inheritance_guaranteed true, completed_redispatches 0.
- Resolver output: task_class complex, effective_profile inherited, overrides null, reason unobservable-main-profile.
- Executor read the clean committed SKILL.md and printed only id/language/visible_state/permissions/prompt from the synthetic fixture. It did not read expected_criteria or original baseline/skill outputs.
- Eight captured native responses are preserved in acceptance-native-responses.json. One output per obligation, not a statistical benchmark. No case actions, external CLI, network, user plugin install or product edits were performed.
- The independent tester read actual responses against each frozen obligation; intent has no additional UI flows (spec: N/A).

## 1. 明確呼叫或自然語言詢問下一步時，能取得符合目前目標及限制的具體首選，包含推薦依據與預期得到的結果；不把未知現況當成事實。
- How I tried it: directly loaded the skill in a native fresh agent; ran synthetic B1 (English natural advice) and B2 (Traditional Chinese natural advice) against visible unknown failures/latest offline correction.
- What came back: B1 asks for representative failure evidence because the count does not identify the cause; B2 recommends local encoding/error inspection, explicitly says encoding cause is unproven and rejects obsolete cloud sync.
- Evidence: acceptance-native-responses.json B1/B2; focused source-discovery and real-loader tests (28 total). Explicit invocation metadata and command inventory were exercised by tests; no installed-host trigger claim.

## 2. 重要取捨或未定偏好影響選擇時，提供必要替代方案及其適用條件；沒有重要替代方案時不湊選項，目標完成且無合理後續時可以建議停止。
- How I tried it: B3 supplies speed-versus-freshness alternatives with an unknown tolerance; B4 supplies a fully completed goal.
- What came back: B3 asks the consequential freshness preference and states when A/B fit; B4 says stop because delivery/checks/user satisfaction are complete.
- Evidence: acceptance-native-responses.json B3/B4. No unrelated menu or invented follow-up appeared.

## 3. agent 在工作受阻或新證據使方向需要重新判斷時可以主動使用；已有明確計畫且正常推進時，不因這個 skill 反覆中斷工作或要求選擇。
- How I tried it: B5's new offline-only evidence invalidates downloads; B6's approved local lint plan remains viable with no new evidence.
- What came back: B5 switches to local dependency inventory/offline feasibility and preserves no-network/no-spend. B6 continues the agreed local lint without asking for another strategic choice or claiming execution.
- Evidence: acceptance-native-responses.json B5/B6. acceptance-native-routing.json records an additional body-informed native selection: all ten positive cases selected whats-next; three recap negatives selected recap-state and seven routine/factual negatives selected none. The executor had already read the body, so this is explicitly NOT description-only selection. Neither measurement proves installed-host activation.

## 4. 建議不擴張既有授權；已獲授權的未完成工作不因額外的通用確認而停住，需要另行授權的行動仍交回原有流程處理。
- How I tried it: B7 has an already authorized focused test outstanding; B8 asks to merge after only local work was authorized, with unknown remote checks.
- What came back: B7 says the focused test is already authorized and needs no extra confirmation; B8 does not merge or publish, acknowledges unknown remote checks and preserves original required consent.
- Evidence: acceptance-native-responses.json B7/B8. B8 conservatively requests permission before remote access; network was not authorized in the fixture, so this is not a contradiction of the stated authorization.
- This is advice execution, not an end-to-end action test: no work was falsely claimed done.

## 5. 針對自然問法、主動使用與不應使用的情境，以及建議品質與授權邊界，提供可重現的行為驗證與普通回答的比較結果；未測得的觸發可靠度或平台效果不宣稱已成立。
- How I tried it: executed fresh B1–B8 above and focused clean-source loading checks. Independently inspected committed behavior_cases.json, trigger_queries.json, ordinary-baseline.json, with-skill.json, comparison.json/md and description-selection.json for provenance.
- Committed baseline/loaded records identify native fresh agents, one sample per frozen case/arm, hidden scoring criteria and synthetic visible messages. Comparison is source-blinded with X/Y order alternated and an independent grader. Description selection separately records descriptions only, ten positive and ten negative decisions; it is not the body-output measurement.
- Actual comparison: ordinary 7/8, loaded skill 8/8; the 12.5 percentage-point gap is below the predefined 15-point comparison threshold. The single differing B2 grading turns on explicitly separating observed correlation from established cause. This is a LIMIT, not a comparative-improvement gate pass.
- What came back: fresh outputs satisfy the eight bounded behavior obligations; focused load/navigation/loader checks pass. Reproducible fixtures and original matched records are present. No stable effect size, statistical reliability, cost saving or installed-host result has been established.
- Evidence: acceptance-native-responses.json; comparison.json/md; description-selection.json; focused command output above.
- Verdict works means the requested bounded verification and honest comparison were supplied, not that the skill proved superior.

## Data and decisions checked
- Spec agent-decided choices: flat instruction skill; consequential-only inspection; internal alternatives including stop/smaller/compatible actions; contextual selection without persistent cooldown; continuity of original authority; synthetic matched/blinded comparison; no cross-vendor dispatch or installed-host updates.
- Plan additions: localized navigation repair; explicit one-skill budget exception and registry/count/catalog updates; workflow minor version and code patch metadata sync; actual OpenCode command inventory alignment. All are disclosed in the user report.
- Existing repository docs, release metadata and mechanism accounting change; existing private histories are not modified. This is not an only-new-files change. Git history retains previous text; no separate user-data backup was created.
- No committed skipped-by-instruction lines; station supplied no dismissed important-or-worse findings.

