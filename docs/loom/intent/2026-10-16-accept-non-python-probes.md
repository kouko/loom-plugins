# 審查證明接受各種語言與測試框架寫的找漏洞測試
originator: kouko
kind: engineering
needs-design: no — 只改 checker 內部的接受判斷與 loom 自己產生、只由 loom checker 讀取的審查證明欄位，沒有使用者輸入的介面，行為是每支已記錄測試的單一接受／拒收決定
status: confirmed 2026-10-17
publication: automatic — authorized 2026-10-17 by kouko

## Problem
在 Go 專案裡跑 loom 時，build 站的 adversary 依專案語言寫了 Go 測試當找漏洞測試（adversarial probe）。到 closing-review 產生審查證明（attestation）時，`finalize-review` 以「command must execute the artifact directly」拒收，因為 `loom-code/scripts/loom_checker/probes.py` 的 `command_executes_artifact` 只認得 Python／pytest 與 bash／sh 指令；attestation validator 用同一個判斷，所以也會拒收。

卡住後沒有好的退路：
- 不放找漏洞測試 → 被「至少要有一個 adversarial execution」擋下。
- 另寫一支 shell 包裝去跑 Go 測試 → 新檔案改變功能內容摘要，先前的 reviewer verdict 失效，要再審一輪，超過三輪上限會被判成無法收斂。

受影響的是所有不用 pytest 或 shell 寫測試的 repo；同一語言也常有多種測試框架（連 Python 標準庫的 unittest 都會被拒收），逐一支援永遠追不完，loom 在這些 repo 裡走不完 closing-review。

## Proposed outcome
審查證明工具照業界做法，先自己判斷找漏洞測試是否真的跑了，判斷不了才交給 LLM reviewer：
- 常用的語言與測試框架組合：工具先確認指令只跑這支測試檔，再讀該次執行的測試結果；至少有一支測試真的通過（不算跳過）才接受，零支或全部跳過就拒收。
- 不在清單上的組合，或結果讀不懂（例如框架改了輸出格式）：由 closing-review 的 LLM reviewer 看這次執行的輸出確認該測試檔的測試有跑，工具只確認這份確認存在、屬於這次執行。

Python（pytest）與 shell 照現在的方式由工具直接判斷。

## Acceptance
1. 在一個乾淨的 Go 範例 repo 裡，一支 Go 寫的找漏洞測試用 `go test` 執行並記錄後，不需要 reviewer 確認，`finalize-review` 就產生審查證明，而且該證明通過 checker 的驗證。
2. 同樣的結果，對下列每個組合在對應的範例 repo 各成立一次：Python unittest；JavaScript／TypeScript 的 Node 內建測試、vitest、jest、mocha、Bun、Deno；Rust 的 cargo test 與 cargo nextest；Ruby 的 rspec 與 minitest；PHP 的 phpunit。
3. 對清單上的組合，下列情況被拒收：指令雖然寫了測試檔路徑、但不會只執行它（例如把路徑當成其他選項的值、用不跑測試的子指令、同時跑其他測試檔）；執行成功但該測試檔沒有任何測試真的通過（零支，或全部被跳過）。
4. 清單外的組合（例如 Java 的 Maven），以及清單上但結果讀不懂的執行，只有在 reviewer 確認後才產生審查證明，證明裡看得出是哪個 reviewer、依據哪一段輸出確認的；沒有確認，或確認不屬於這次執行（例如沿用別的執行或舊內容的確認）就被拒收。
5. 現有用 Python（pytest）或 shell 寫的找漏洞測試照舊被接受，repo 的完整 package suite 通過。

## Constraints
- 功能內容摘要的計算方式與三輪審查上限不變。
- 「至少要有一個找漏洞測試」的規定不變。
- 不論哪種組合，工具仍會實際執行記錄的指令，結果必須成功。

## Out of scope
- 為 Java、Kotlin、C#、Swift 等寫專屬的指令判斷（它們走 reviewer 確認）。
- 修補現有 pytest 指令可用過濾條件排除該測試檔、卻仍被接受的問題（另案處理）。
- 防止測試程式蓄意印出假結果，或有權限改寫審查證明的人蓄意偽造 reviewer 確認。
- 要求使用者的專案另外安裝測試報告外掛。
- 解開那個 Go repo 目前卡住的變更本身；它在更新 plugin 後自行重跑 closing-review。
- 不經任何確認、只要寫了檔案路徑就接受的做法。
- 要求找漏洞測試加入 loom 專用的程式碼（例如寫入標記檔）。

## Open questions
- none
