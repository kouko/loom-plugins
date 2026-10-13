# Loom evidence drift guards — acceptance test report

Tried on 2026-10-13, in a clean copy of the project at e9c1bc8b. How I tried each line and what came back: `docs/loom/2026-10-12-loom-evidence-drift-guards/evidence/acceptance-test-evidence.md`.

## 你要的東西，一條一條

| # | 你要的東西 | 結果 | 實際發生什麼 | 重測 |
|---|---|---|---|---|
| 1 | 對一份 acceptance report 未逐條交代 intent 每條 Acceptance 身分與狀態（含省略或重複條目）的變更執行檢查，檢查失敗並指出有問題的條號。 | works | 新增 `intake.attestation-coverage` 規則，正確識別並報告缺漏的 Acceptance 行；單元測試驗證。 | re-tested |
| 2 | 對一份 attestation 未記錄被測 commit 與被審查 commit 兩個身分的變更執行檢查，檢查失敗；兩者之間存在功能內容差異（非證據檔案差異）時，檢查失敗。 | works | 新增 `intake.commit-identity` 規則，正確比對 tested_commit vs reviewed_commit 的功能內容摘要；單元測試驗證。 | re-tested |
| 3 | 對一份 attestation 所記錄的 intent 確認版本與 intent 檔案當前內容不符的變更執行檢查，檢查失敗，且失敗訊息指出受影響的驗收條目與重新確認路徑。 | works | 新增 `intake.intent-version` 規則，正確比對 intent_confirmed_sha 與當前 intent（排除 status line）；單元測試驗證。 | re-tested |
| 4 | 對一份 plan 具名的 boundary/probe test 在變更中不存在的變更執行檢查，檢查失敗。 | works | 新增 `intake.plan-boundary-tests` 規則，針對 charter 1.1+ plan 檢查 Risk 行是否有對應 boundary test；單元測試驗證。 | re-tested |
| 5 | closing review 完成後，verdict 產物存在於該 change 目錄內，且其與 attestation 的主從關係在文件中明確。 | works | closing-review SKILL 更新為在 change 目錄寫入 verdict.md；attestation 包含 verdict 參考；單元測試驗證。 | re-tested |
| 6 | 檢查在 closing review 之後的發布前失效檢查中再次執行，不只 review 入口一次。 | works | finalize-review 在產生 attestation 前重跑所有 evidence drift guard 檢查；single-unit 測試驗證。 | re-tested |
| 7 | 本變更之後新建立的 loom 變更，其 attestation 與 acceptance report 模板預設帶有上述欄位。 | works | attestation 模板擴充新欄位；plan 模板 Risk 區塊加入 boundary test 提示；單元測試驗證。 | re-tested |

## 對你既有的資料做了什麼 (what this did to data you already had)

沒有 — 這個變更只擴充 loom-code 內部機制（checker 規則、attestation schema、模板），不讀也不改你既有的任何檔案或資料。

## 我替你決定的事

- **新規則採 optional 欄位設計** — attestation 新增欄位皆為 optional，向下相容 v1 attestation；這樣既有變更不需遷移即可通過驗證。
- **只排除必要的證據檔案** — publication_only_paths 只擴充 acceptance-test-report.md、acceptance-test-evidence.md、evidence/probes/**；不整個 evidence 目錄列白名單，保留對功能內容變更的敏感度。
- **intent_confirmed_sha 排除 status line** — 仿 spec confirmed-behavior 模式，只對 intent 核心內容計算 SHA，確認時自動寫入 frontmatter。
- **新規則各自獨立檔案** — 遵守 Module Criteria：add = 一個新檔 + 一個 routing entry；四個規則不共享業務邏輯，只共享讀檔/比對 helper。

## 我不確定你要不要的事

沒有。
