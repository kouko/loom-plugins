# 讓 loom 做出邊界明確、入口少的模組，降低測試複雜度
originator: kouko
kind: engineering
needs-design: no — station prose and reviewer lens rows under loom-code/skills/ and loom-code/references/, which the manifest classifies as the `skill` artifact type, not an interface surface (`**/cli/**`, `**/api/**`, `**/commands/**`, `**/*.tsx`, `**/templates/**`)
evidence: [docs/loom/memory/an-engineering-change-without-a-spec-leaves-interface-detail-with-no-persistent-home.md, docs/loom/memory/fixtures-mirror-producer-shape.md, docs/loom/intent/2026-10-05-pr-bottleneck-review-brakes.md, loom-code/skills/closing-review/references/lenses.md, loom-code/references/engineering-baseline.md]
status: confirmed 2026-10-05
publication: automatic — authorized 2026-10-05 by kouko

## Problem
loom 帶 agent 寫 code 時，從計畫、實作到審查，都沒有說明一個模組對外的入口在哪裡：

| 環節 | 今天的情況 | 後果 |
|---|---|---|
| 計畫 | 每個 task 只寫要改哪些檔案、對應哪幾條驗收 | 寫 code 的 agent 和審查的 agent 對「哪些是模組內部」沒有共同依據 |
| 實作與測試 | 測試可以從任何函式切進去 | 測試綁住內部結構，重構內部時要跟著改；入口一多，要測的切入點也跟著變多 |
| 審查 | 沒有檢查模組是否只是轉手、沒藏住任何邏輯 | 入口變多卻沒換到簡化，測試複雜度上升 |
| 審查 | 函式長度與「重複三次」兩條規則只憑數字就判定要拆分或抽出 | 為了湊數字拆出只轉手的函式，或抽出之後三處各自要改的錯誤抽象 |

影響每個用 loom 寫 code 的 repo。

## Proposed outcome
loom 的計畫寫明每個模組對外的入口；測試只需要涵蓋入口的介面；審查把「從入口能測卻直接測內部的測試」和「只轉手、沒藏住邏輯的模組」當成問題回報，並且不再單憑長度或重複次數要求拆分。模組邊界因此明確，入口變少，要測的切入點跟著變少。

## Acceptance
1. write-plan 產生的 plan 裡，每個會改程式碼的 task 都寫明它碰到的模組對外入口，而且它的測試案例以入口的行為命名。
2. 測試只需要涵蓋模組對外入口的介面：plan 裡每個測試案例都從入口測（必須測內部函式的案例不符合本條），不為內部函式另寫測試；closing review 把「直接測內部、而該行為從入口能觸及」的新增或修改測試當成問題回報，要求改從入口測。用刻意寫壞的範例改動試，這種測試會被抓到（不論入口是否已有測試涵蓋同樣行為），只從入口測的測試不會被要求補內部測試，而入口觸及不到、成為有自己入口的獨立模組並從該入口測的測試不會被抓。
3. closing review 的審查會把「只把呼叫轉給另一處、沒藏住任何邏輯」的新增模組或函式當成問題回報——只轉手指的是不做分支、轉換、驗證、錯誤處理、資源邊界處理或政策選擇，只呼叫另一處並回傳結果；用刻意寫壞的範例改動試，會被抓到，而真正藏住邏輯的模組不會被抓。
4. closing review 不單憑長度或重複次數要求拆分或抽出：長度只提示審查者去看，要求拆分時必須指出具體毛病（例如一個函式做了幾件不相干的事）；重複三次只在三處會因同一個理由一起改時才要求抽出。要求拆分或抽出時，修法預設是模組內部、不對外的函式；只有其他模組也需要呼叫它，或它的行為無法從既有模組的入口觸及時，才成為有自己入口的獨立模組；「想單獨測」本身不構成新增入口的理由。用刻意寫壞的範例改動試，只是長而沒有其他毛病的函式不會被要求拆分，三處碰巧相似但會各自改的程式不會被要求抽出，審查不會要求為拆分或抽出新增對外入口，而跨模組共用的抽出仍被接受。
5. 完整 package suite 全部通過；三份 manifest、README 的版號字串與 CHANGELOG 新區段一致。

## Constraints
- 不新增使用者決策點。
- 不新增 plan 欄位：入口寫在 task 既有的欄位裡。
- 審查者仍然只下判定、不改它審的東西（writer ≠ judge）。
- 對話用繁體中文；plan、spec、verdict、commit body 等 loom 機器面 artifacts 用英文；PR 說明與驗收報告用使用者的語言。

## Out of scope
- 改動兩條規則的門檻數字本身（20／50 行、三次）：量測 loom 本身 79 份審查證明與本機 6 個採用 loom 的專案，只找到一筆 loom 1.0 之前的弱證據（三處重複抽出後留下只轉手的函式），不足以支持換成別的數字；本次只把數字從判定改為提示。重新考慮的條件是，出現一筆紀錄顯示數字改為提示後，仍有人為了符合它而拆出只轉手的函式。
- 重構 loom 自己的程式碼成較深的模組（使用者選擇只改流程）。
- 另做一個專門處理模組邊界的獨立 skill。
- 由機器檢查擋下沒寫入口的 plan task：沒有紀錄顯示需要它，成本約為文字規則的五倍；重新考慮的條件是，closing review 記錄到一個改程式碼的 task 沒寫入口就交付。

## Open questions
- none
