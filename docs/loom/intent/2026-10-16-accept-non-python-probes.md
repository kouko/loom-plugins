# 審查證明接受 Go 等語言寫的找漏洞測試
originator: kouko
kind: engineering
needs-design: no — 只改 checker 內部的接受判斷，沒有使用者輸入的介面或檔案格式變更，行為是每支已記錄測試的單一接受／拒收決定
status: confirmed 2026-10-16
publication: automatic — authorized 2026-10-16 by kouko

## Problem
在 Go 專案裡跑 loom 時，build 站的 adversary 依專案語言寫了 Go 測試當找漏洞測試（adversarial probe）。到 closing-review 產生審查證明（attestation）時，`finalize-review` 以「command must execute the artifact directly」拒收，因為 `loom-code/scripts/loom_checker/probes.py` 的 `command_executes_artifact` 只認得 Python／pytest 與 bash／sh 指令；attestation validator 用同一個判斷，所以也會拒收。

卡住後沒有好的退路：
- 不放找漏洞測試 → 被「至少要有一個 adversarial execution」擋下。
- 另寫一支 shell 包裝去跑 Go 測試 → 新檔案改變功能內容摘要，先前的 reviewer verdict 失效，要再審一輪，超過三輪上限會被判成無法收斂。

受影響的是所有用 Go、JavaScript／TypeScript、Rust 寫程式的 repo：loom 在這些 repo 裡走不完 closing-review。

## Proposed outcome
審查證明工具接受用 Go、JavaScript／TypeScript、Rust 寫的找漏洞測試，只要記錄的指令是該語言平常的測試指令、而且真的跑到那個測試檔；仍然拒收沒有真的跑到該檔案的指令。

## Acceptance
1. 在一個乾淨的 Go 範例 repo 裡，一支 Go 寫的找漏洞測試用 `go test` 執行並記錄後，`finalize-review` 產生審查證明，而且該證明通過 checker 的驗證。
2. 同樣的結果在 JavaScript／TypeScript（npm 專案）與 Rust（cargo 專案）範例 repo 各成立一次。
3. 對上述三種語言，指令裡雖然寫了測試檔路徑、但實際上不會執行它的情況（例如把路徑當成其他選項的值，或用不跑測試的子指令），仍被拒收。
4. 現有用 Python 或 shell 寫的找漏洞測試照舊被接受，repo 的完整 package suite 通過。

## Constraints
- 功能內容摘要的計算方式與三輪審查上限不變。
- 「至少要有一個找漏洞測試」的規定不變。

## Out of scope
- 上述三種以外的語言（例如 Java、Kotlin、Ruby）。
- 解開那個 Go repo 目前卡住的變更本身；它在更新 plugin 後自行重跑 closing-review。
- 接受任意指令（只要寫了檔案路徑就算）。

## Open questions
- none
