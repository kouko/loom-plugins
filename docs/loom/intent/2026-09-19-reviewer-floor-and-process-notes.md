# 修正版本同步誤判、補兩則流程紀律、清理兩個死模組

originator: kouko
kind: engineering
needs-design: no — 全部改動落在 checker 程式碼、skill 說明文字與死程式碼清理,不是宣告的介面表面(`**/cli/**`、`**/api/**`、`**/commands/**`、`**/*.tsx`、`**/templates/**`)
evidence: [loom-code/scripts/loom_checker/reviewers.py, loom-code/scripts/test_loom_attestation.py, loom-code/skills/write-plan/SKILL.md, loom-workflow/skills/git-memory/SKILL.md]
status: confirmed 2026-09-19
publication: automatic — authorized 2026-09-19 by kouko

## Problem

同一個 session 裡發生了三件事,各自代表一種會在任何用 loom 做開發的專案裡重演的問題:

1. 把 `loom-code/plugin.json` 的版本字串從 `3.7.1` 升到 `3.7.2`,是一次單欄位改動,但 `reviewer_floor_for_paths` 的低風險判斷式只認得 `.md/.mdx/.rst/.txt` 四種副檔名,任何 `.json` 檔案一律落到高風險,審查人數因此算成 2 而非 1。這不是這個 repo 特有的——任何團隊在 `package.json`、`pyproject.toml`、`Cargo.toml` 裡改版本號都會撞上同一道牆。
2. 移除一個既有的文字辨識規則時,沒有先盤點它原本涵蓋的既有測試案例數,導致刪除後漏放了多個真實情況,要靠事後三波(套件、reviewer、對抗測試)才抓完。
3. 在 closing-review 的 `finalize-review` 產生驗證紀錄之後,又提交了一則 memory 教訓,導致驗證紀錄的內容指紋對不上,得撤銷重推。

## Proposed outcome

改一個 JSON 設定檔案裡的單一版本欄位,能被機械判定為低風險。write-plan 的計畫在移除或大改一個已有測試的函式時,要求先寫明現有覆蓋範圍。git-memory 的說明文字明講教訓必須搭上還在跑的修正輪,不能等驗證紀錄產生後才補。另外清掉兩個查證後確認沒有任何呼叫路徑的死模組。

## Acceptance

1. `.json` 檔案只有 `version` 欄位不同時,`reviewer_floor_for_paths` 判定為低風險(floor 1);同一個檔案若有任何其他欄位也不同、或是新增檔案、或內容不是合法 JSON,判定維持高風險(floor 2)。
2. `write-plan` 的 SKILL.md 明文要求:任務若移除或大改一個已有測試的函式,計畫必須寫明現有測試覆蓋範圍是否不變、擴大或縮小。
3. `git-memory` 的 SKILL.md 明文警告:Loom 的 memory 教訓必須在 `finalize-review` 產生驗證紀錄之前提交,不能事後補。
4. `heading_window.py`、`sibling_import.py` 兩個模組與其專屬測試已移除,完整套件通過。
5. 既有測試全部通過。

## Constraints

- 不新增機制、不改契約 manifest 版本、不改任何規則 id。
- 機器面輸出(commit、測試、skill 文字)維持英文。

## Out of scope

- 「共用識別字改動前要先機械列舉命中點」這條(當時討論的第 3 項)——那是要走預算宣告流程的新機制,不在這次範圍。
- 這次 session 稍早討論、後來放棄的閘門降級與 heredoc 誤攔修正。

## Open questions

- none
