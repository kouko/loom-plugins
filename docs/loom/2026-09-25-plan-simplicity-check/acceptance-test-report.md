# 每份 plan 在 Build 前都先檢查有沒有更簡單的做法 — 我試了什麼、結果如何

2026-09-25 先在專案的乾淨副本（611c2182）上試過一次；closing review 發現「簡化檢查」寫在兩個檢查通過之後、但那兩個檢查會擋下還沒做簡化檢查的 plan，所以照字面永遠跑不到。修正後在新的乾淨副本（fc4dbf30）上重試受影響的條目。每一條怎麼試、回來什麼：`docs/loom/2026-09-25-plan-simplicity-check/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | Before Build starts on a change, a fresh-context reviewer that did not write the plan checks it for a simpler way to reach the same Acceptance lines, and returns either no simpler shape or a concrete smaller shape. | works | 我照規劃步驟的順序，從範本寫出一份刻意做太多的小 plan，再照說明派一個全新的 reviewer；它拿到的輸入就是說明規定的那幾行，沒有因為缺東西而停下，回了三個具體的縮小方案（三個 task 縮成一個、拿掉 registry 和 YAML 設定）。 | 重試 |
| 2 | The plan records the outcome of that check — the simpler shapes considered and whether each was taken or why not — and a plan without that record cannot enter Build. | works | 還沒記錄的草稿，兩個檢查都擋下；把三個方案記成「taken」後，兩個檢查都通過。現在的順序（先做簡化檢查、再跑檢查）照著做就走得通。 | 重試 |
| 3 | The check needs only loom-code installed. | works | 用到的 reviewer、說明和檢查全部都在 loom-code 裡，沒有任何地方要求 loom-workflow。 | carried over — 修正沒有加入任何對其他 plugin 的依賴，重查仍然沒有 |
| 4 | A change the checker judges narrow skips the check, and says so. | works | 只改文件的 plan 寫「skipped — narrow change」可以通過；同一句話寫在會改程式的 plan 上會被擋，並說明「不夠窄，必須做檢查」。 | 重試 |
| 5 | The check never asks the user a question; adopting or declining a simpler shape is recorded as agent-decided. | works | 說明仍寫「採用或拒絕都由 agent 決定、不問使用者、只跑一輪」，也新寫明 reviewer 這一輪之後沒有修正回合；實際試跑的 reviewer 沒有問任何問題。 | 重試 |
| 6 | When the adversary names an existing test as this change's adversarial program, it marks that test with its `concern:` line in the same dispatch, so finalize-review does not refuse the change for a missing line. | works | 在一個丟棄用的小專案裡，沿用的既有 test 沒標 concern 時最後檢查會拒絕；照新說明補上一行 concern 後就不再拒絕。 | carried over — 修正沒有動到 adversary 的說明，也沒有動到檢查程式 |

涵蓋這些條目的 targeted tests 在新的乾淨副本上全部通過（69 個）；完整的自動測試套件會在 change 被接受前再跑一次，失敗就擋下。

## 對你既有的資料做了什麼

Nothing — it only touched files this change created。舊版（charter 1.0）的 plan 不受新規則影響，照舊通過。

## 我替你決定的事

- **沒有用 marketplace 安裝這個 branch 來試** — 我直接在乾淨副本上跑檢查和 reviewer，因為照 README 安裝會抓已發佈的 main，而且會改動你這台電腦上已安裝的 plugin。以後要補，就是推上去之後再裝一次試。

## 我不確定你要不要的事

- 檢查只看 plan 裡的紀錄格式對不對，看不出 reviewer 是否真的有被派出去：手寫一行「none found」也會通過。這樣可以接受嗎？還是你希望紀錄能證明 reviewer 真的跑過？
