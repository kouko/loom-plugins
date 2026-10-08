# 統一外部 coding agent 的獨立審查
originator: kouko
kind: engineering
needs-design: yes — 獨立意見與正式審查跨越多種任務、執行器及失敗狀態，目前沒有共同規格描述它們的關係
status: confirmed 2026-10-08
publication: automatic — authorized 2026-10-08 by kouko
amendment: confirmed 2026-10-08 by kouko — an explicit named outside-review request needs no second consent confirmation

## Problem
要求另一個 coding agent 獨立審查時，Loom 的意見諮詢與正式審查各走不同接點。使用者無法確定要求獨立 code review、plan review 或決策意見時，原本的審查標準會不會保留，也無法依賴一致的外部 agent 選擇方式。外部 CLI 的預設模型或帳號環境若失效，審查可能在開始前失敗，或無法證明實際使用了要求的模型。

## Proposed outcome
使用者明確要求或同意外部 coding agent 後，Loom 能透過統一的獨立審查接點執行不同種類的審查，同時保留原本任務的審查標準，並清楚報告所選執行器、實際可驗證的模型能力及失敗原因。

## Acceptance
1. 使用者要求另一個 coding agent 獨立審查程式碼、計畫或決策時，Loom 會啟動相應的外部審查；原本 agent 的審查仍存在，外部結果可與它分別辨認。
2. 外部 agent 執行 Loom 的既有審查任務時，結果仍符合該任務原有的審查標準與交付格式，不因改由其他 agent 執行而改用另一套評判方式。
3. 沒有使用者明確要求或同意時，現有的第二廠商提示仍不強制啟動外部審查。
4. 在已安裝且已登入的 Codex、Claude Code 或 Antigravity CLI 中，Loom 能取得或選定候選模型，明確指定模型與 effort 執行，並在正式審查前確認可觀察到的執行結果；同一套選擇與失敗規則適用於各種獨立審查任務。
5. 候選清單過期、模型無法使用、實際模型廠商不符要求或無法核對必要能力時，Loom 會停止或明確標示限制，不會悄悄換模型或把未驗證的審查算成通過。
6. 使用者已明確指定外部 coding agent，而審查目標也可由目前任務明確判定時，Loom 告知資料傳送、費用與本機執行限制後直接執行，不再要求使用者重複確認；只有必要選擇仍不明確或資料範圍擴大時才詢問。

## Constraints
- 保留使用者對外部審查的選擇權；現有的資料傳送、成本與本機執行告知要求仍適用。
- 原本 Loom 審查 skill 擁有評判標準及結果格式；independent-advisor 統一外部 agent 的執行接點，不另造 code review 專屬例外。
- 保留目前支援的 Loom 主機及既有未選擇外部審查的流程。
- 外部審查明確指定模型與 effort，不依賴執行器的預設值。
- 使用者明確要求外部審查本身就是該次審查的授權；單純的第二廠商提示仍不是授權。

## Out of scope
- 定期維護一份宣稱完整且保證可用的固定模型清單。
- 自動操作互動式模型選單。
- 安裝新的外部 CLI 或替使用者建立登入憑證。

## Open questions
- none
