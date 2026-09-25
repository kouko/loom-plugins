# 讓變更新增的測試保持精簡 — 我試了什麼、結果如何

2026-09-25 在專案的乾淨副本（1b056075）上試。每一條怎麼試、回來了什麼：`docs/loom/2026-09-25-keep-mechanical-tests-small/evidence/acceptance-test-evidence.md`。

## 你要的東西，逐條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | The implementer contract states a test budget: at most one positive and one negative or boundary case per Acceptance line or finding, reuse of the existing test helpers, no new test harness, no tests of tests, and the net test lines added in its report. | works | 寫測試的 agent 現在讀得到這份預算，回報裡也多了「淨增測試行數」一欄；我另外只給一個全新的 agent 看這份規則加一個小題目，它規劃出一個正向、一個反向，review 意見用擴充既有測試來修，也沒有另寫 helper，完全在預算內（review 意見那一項比你寫的更嚴：只准加一個測試）。 | — |
| 2 | The adversary contract states that each probe program stays small and reuses existing test helpers. | works | 對抗測試的規則現在寫明每支 probe 保持精簡、沿用專案既有的測試 helper、不為單一案例蓋 harness；原本「最多五支」的上限沒動。 | — |
| 3 | Closing review's tests dimension makes over-built tests a finding with the smaller shape named, and says the fix for a finding adds at most one test, extending an existing test first. | works | Reviewer 的 tests 檢查現在把「這次變更新增、超出需要的測試」列為 finding，並要求指出更小的寫法；修 finding 最多加一個測試、先擴充既有的。舊有的重複測試不算，因為條文只針對這次新增的。 | — |
| 4 | No checker rule, flow step or agent dispatch is added. | works | 規則數前後都是 26；整體機制計數前後都是 142、沒有差；沒有新增任何閘門標記、流程步驟或新派出的 agent。完整自動測試套件會在變更被接受前另外執行，失敗就擋下。 | — |

## 對你既有的資料做了什麼

沒有 — 這次只改了規則文字與這次新增的測試檔，沒有讀寫你既有的任何資料。

## 我替你決定的

- **修 review 意見時的上限比你寫的更緊** — 你的第 1 條寫「每條 Acceptance 或每個 finding 最多一正一反」，實作對 finding 改成「最多一個測試、先擴充既有的」，和第 3 條一致。這是實作者的選擇，我只記錄；如果你要的是 finding 也能一正一反，之後改一句話即可。

## 我不確定你要不要的

沒有。
