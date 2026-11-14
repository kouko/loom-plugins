# Recap progress clarity — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at be34122e8106f595d6b01a0dae033b2fa2162c9a.

## Environment, setup and provenance

- Independent acceptance tester; no product, test or plan edits. First acceptance run; no carried-over verdicts. No spec because this is an engineering change. No dismissed important findings were supplied.
- Clean detached copy: `/tmp/recap-acceptance-be34122e`. Ran `git status --porcelain` (empty) and `git rev-parse HEAD` (exact commit above) before testing.
- Read root README, plugin README Install section, committed intent and plan. README installation uses marketplace commands that change the local host. Local plugin installation is explicitly out of scope; therefore installation and installed-host loading were not run or claimed. The bounded setup exercised here is loading the source entry plus its required reference into fresh native agents. No additional dependency is required for reading that skill. This does not establish marketplace delivery, host hook trust or actual installed runtime behavior.
- Reviewed all seven actual outputs against the six committed cases' withheld checks plus the longer synthetic case. Executors were separate fresh native agents, not installed-host sessions. The parent supplied final-response snapshots and confirmed each execution ended at its final question without continuation. No subsequent user turn was simulated. The tester independently assessed response content, while execution termination provenance is supplied by the orchestrator rather than inferred from a promise in prose.
- Direct evidence: `acceptance-behavior-snapshots.json` retains seven synthetic inputs and actual final outputs, including executor source revisions. No real histories, credentials or private user documents are included. No A/B superiority claim is made.
- Independently recomputed source identity with `git show <revision>:<path>` and Python `hashlib.sha256`, comparing revisions `2b1cdcd57bedc4545aa591ae00609e7f3fd50636`, `94be76fda82fb8eaeec948a1f26f4e6868a9e6e5`, and clean `HEAD`; all three blobs for each file were byte-identical. Did not rely on the supplied convenience identity file.
  - `loom-workflow/skills/recap-state/SKILL.md`: `59f742e7daf9097ac1e809f86ee048b546f426056346e1067d1567755a8cb1ce`.
  - `loom-workflow/skills/recap-state/references/seven-block-schema.md`: `4f30550f8130b4595ab357d5d4f08f4164af82fc2d39d24aff621304435142a7`.
- Full package suite was deliberately left to closing-review: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. The station said package-tests are not skipped and finalize-review will run. A prior Build log was supplied, but it is not treated as this tester's suite result.

## 1. 在實作、驗證與合併或發佈狀態不同的情況，回顧清楚區分相關工作的完成狀態；未知狀態不被宣稱為完成。

- How I tried it: evaluated implemented-unmerged, unknown-delivery and long-session actual responses against their full synthetic histories.
- What came back: implemented-unmerged says `本機實作已完成並提交為 abc1234`, `最終審查尚未開始，也沒有合併或發佈`. Unknown-delivery says `測試、合併與發佈狀態仍未知` and separates the old sorting merge. Long-session explicitly separates another team's sorting PR from export work.
- Evidence: snapshot output keys above. No invented delivery fact or mandatory repository inspection. Result: works.

## 2. 回顧使用目前對話語言，並在目的已知時保留目的、只確認具體下一步，不要求使用者重新說明需求。

- How I tried it: evaluated known-purpose-language with English skill-loading context and Traditional Chinese conversation; cross-checked other known-purpose outputs.
- What came back: `我們在做「讓搜尋結果依更新時間排序」` followed by `我建議先檢查特殊情況下排序是否正確，再整理說明，這樣繼續可以嗎？` Entire response is Traditional Chinese. No purpose re-interview. Unknown-delivery asks purpose only because its history lacks the actual search problem, which is consistent with the unknown-purpose boundary.
- Evidence: known-purpose-language snapshot; implemented-unmerged, scoped-tests and resumed-date snapshots. Result: works.

## 3. 與驗收或發佈判斷相關的測試結果具有可辨識的驗證範圍及對應內容；局部成功不被描述為整體目標完成。

- How I tried it: evaluated scoped-tests and long-session outputs, including older successful tests followed by newer untested implementation.
- What came back: `提交 def5678 的匯出單元測試 8 項通過` and `尚不能據此判定發佈後可正常使用`; full suite, installed environment and post-release flow remain unverified. Long-session associates nine collision tests with cde1234, newer work with efg5678, and says `9 項通過只支持先前提交的碰撞處理`.
- Evidence: scoped-tests and long-session snapshots. Result: works; no full-suite or release-readiness overclaim.

## 4. 跨日恢復對話時，回顧不把較早發生的工作誤稱為今天或剛剛完成；無可靠日期時不捏造相對時間。

- How I tried it: evaluated resumed-date with current date November 14, known event November 7 and an undated update.
- What came back: `依 2026-11-07 的對話，修正已合併` and `那則訊息沒有可靠日期`. Preserves remaining sample-file verification, does not label the merge today or just now, and does not invent update timing.
- Evidence: resumed-date snapshot. Result: works.

## 5. 既有依對話長度調整內容、保留重要使用者原話，以及確認方向後等待回覆的行為維持有效。

- How I tried it: compared short unknown-purpose and unknown-delivery outputs with long-session; checked exact constraints and final-question termination across all seven outputs.
- What came back: short unknown-purpose asks only `你原本想完成什麼？` without invented work. Long-session uses four relevant sections and a table, retains `先不要合併`, `不同資料夾撞名時，在檔名加上來源資料夾，不能覆寫。`, and `檔名中的日文要保留，不要轉羅馬字。輸出也保留原副檔名。`. It proposes the grounded next step and ends `照這個方向接續嗎？`. Implemented-unmerged retains the no-merge constraint.
- Evidence: all seven final snapshots, particularly unknown-purpose and long-session. All executions ended after the final question according to their supplied execution records; later-turn behavior is untested. Result: works within the observed single-turn boundary.

## Focused automated checks

- Initial attempt: `python3 -m pytest -q loom-workflow/tests/recap-state loom-workflow/tests/scripts/test_release_metadata.py` failed before collection because default Python 3.15 has no pytest. This is a runner-environment issue, not a failed product assertion.
- README-based isolated runner attempt with `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-workflow/tests/recap-state loom-workflow/tests/scripts/test_release_metadata.py` failed before collection because the sandbox denied creating a lock temporary file in the user uv cache. No host or dependency changes were made.
- Successful bounded check in the clean copy: `PYTHONDONTWRITEBYTECODE=1 /Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest -p no:cacheprovider -q loom-workflow/tests/recap-state loom-workflow/tests/scripts/test_release_metadata.py` → `37 passed in 0.22s`. Used an existing read-only Python 3.12 environment (pytest 9.1.1); no packages installed. This differs from Build's lock-isolated Python 3.13.5 environment, so the complete lock-based suite remains the station's required check before acceptance. These tests cover recap contract, cases, existing presentation rules/readmes and release metadata; they supplement actual-output evaluation rather than replace it.
