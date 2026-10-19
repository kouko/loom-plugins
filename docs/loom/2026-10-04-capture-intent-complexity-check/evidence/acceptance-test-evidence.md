# capture-intent checks whether the scope earns its cost — acceptance test evidence

Tried on 2026-10-04, in a clean copy of the project at ac13a98f
(`git worktree add .git/loom-scratch/at-wt HEAD`, detached; `git status --short` empty afterwards).

## Setup — the change loads in a clean copy
- How I tried it: the README's install path is `claude plugin marketplace add` + `claude plugin install`, which would change the user's installed plugins, so I validated the plugin from the clean copy instead: `claude plugin validate ./loom-design`.
- What came back: `✔ Validation passed with warnings`. The one warning, `Unknown field 'requires-contract'`, is already present at the branch base 2ccf92a7 (`git show 2ccf92a7:loom-design/.claude-plugin/plugin.json | grep -c requires-contract` → 1), so this change did not introduce it.
- Live trials: four fresh-context general-purpose subagents, each given only the clean copy's `loom-design/skills/capture-intent/SKILL.md` path, a stated plugin set, one user request in Traditional Chinese, and a dry-run instruction (no writes). Each returned its file-read trace, its Step 4 item-by-item decisions, and the verbatim decision point ① message. Each trace confirms the skill file was read first.

| Trial | Plugins | User request (summary) | Expected | Item 6 (complexity check) |
|---|---|---|---|---|
| A | loom-code, loom-design, loom-workflow | new required intent field `risk-level` + new checker rule | fires | applied — read `loom-workflow/skills/critique/SKILL.md` and mindset references; verdict RESHAPE |
| B | same as A | bug fix: checker crashes on empty Acceptance | quiet | not applied — "a bug fix and adds no mechanism, field, rule or step" |
| C | loom-code, loom-design only | same request as A | skipped, message unchanged | not applied — "trigger does apply … but loom-workflow is not installed"; nothing under `loom-workflow/` read |
| D | same as A | wording change: 「對嗎？」 → 「這樣理解對嗎？」 | quiet | not applied — "a wording change that adds no mechanism, field, rule or step" |

## 1. capture-intent 說明：當使用者的要求或討論中的選項會新增機制、欄位、規則或步驟時，確認前先執行一次複雜度檢驗（loom-workflow 的 critique，complexity 模式）。
- How I tried it: read Step 4 of the skill in the clean copy; ran trial A; ran the criterion's own tests.
- What came back: Step 4 item 6 (`loom-design/skills/capture-intent/SKILL.md:236-247`) says "When the user's request or an option under discussion would add a mechanism, field, rule or step, run `loom-workflow:critique` in complexity mode before you compose this message." Trial A read the critique skill before composing its ① message and reported "Complexity check: applied … verdict RESHAPE".
- Tests: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --no-project --python /opt/homebrew/bin/python3 --with pytest --with pyyaml python -m pytest loom-design/tests/spec/test_capture_intent_complexity_check.py loom-design/tests/spec/test_capture_intent_contract.py -q` → `20 passed in 0.02s` (includes `test_step_4_runs_complexity_check_in_the_one_message`, `test_critique_named_only_in_step_4`, `test_wording_change_that_adds_cost_still_runs_the_check`, `test_critique_questions_are_answered_from_the_draft_intent`).

## 2. 檢驗的判定與較小的替代做法，出現在決策點 ① 的同一則訊息裡；不新增停點，最後仍由使用者選擇。
- How I tried it: inspected trial A's verbatim ① message.
- What came back: the message carries a section 「簡化建議（我先做了一次「有沒有更小的做法」檢查）」 with the verdict in plain words (「方向可以，但做法建議縮小」) and the smaller alternative (「不用新增一條檢查規則」 — register the field as required in the existing schema check). It sits inside the one ① message, between the restatement and the one-way doors; no separate stop for the check. Critique's full response, mindset names and question-by-question shape do not appear. The user still chooses (the message asks for 「對」 and lists questions).
- Observed deviation (nit): the message also carries a second critique finding, 「更大的問題是，目前沒有任何東西會讀這個欄位」, and ties it to user question 2 (「所以想先請你回答下面第 2 題」). The skill says "Carry only its verdict and its smaller alternative" and "never put [critique's questions] to the user". Question 2 is also one Step 1's interview requires (what the field changes), so the question itself is legitimate; the extra finding is the drift.
- Trial A reported "at least 2" stops before confirmation; its stated cause is the interview's open questions (Problem, value, who picks), not the complexity check.

## 3. 修 bug、改措辭這類不增加成本的要求，不觸發檢驗。
- How I tried it: trials B (bug fix) and D (wording change).
- What came back: neither read anything under `loom-workflow/`; both reported item 6 not applied with the skill's own exemption as the reason; neither ① message contains a simplification section. Skill text: "A request that adds no such cost, such as a bug fix or a wording change, does not run it. A wording change that adds a mechanism, field, rule or step still runs it."
- Side note (not about this change): trial B, against its dry-run instruction, created and then removed a sample file in a system temp folder to try reproducing the bug; nothing in the repo was touched.

## 4. 沒有安裝 loom-workflow 時，capture-intent 的行為跟現在完全一樣。
- How I tried it: skill text, the plugin boundary check, and trial C.
- What came back: skill text "When loom-workflow is not installed, skip this item; the rest of this message is unchanged." `/opt/homebrew/bin/python3 scripts/check_plugin_boundaries.py loom-design` → `OK: loom-design is filesystem-boundary clean.` exit 0. The diff `git diff 2ccf92a7...HEAD -- loom-design/skills/capture-intent/SKILL.md` adds only item 6 (+13 lines), nothing else in the station changed. Trial C skipped item 6 for that reason and composed its message from items 1–5 only.
- Limit: "exactly as before" was judged from the text diff plus one trial; I did not run the base-version skill side by side.

## 5. 完整 package suite 全部通過，版號一致。
- How I tried it: version strings and the version tests; the full suite was not run here (finalize-review runs it).
- What came back: `"version": "2.12.0"` in all four loom-design manifests (`plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `package.json`); `## [2.12.0] — 2026-10-04` in `loom-design/CHANGELOG.md`; 2.12.0 in root `README.md:16` and the three loom-design READMEs.
- Tests: `... -m pytest loom-code/tests/test_adversarial_version_metadata_sync.py "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized" -q` → `14 passed in 0.12s`; `test_loom_design_version_2_2_0_consistent` passed within the 20 above.
- Suite check: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID /opt/homebrew/bin/python3 scripts/run_package_tests.py --loom-family`, executed by finalize-review on committed content, which refuses the attestation on failure.
