# 讓 Go 套件測試能作為找漏洞測試的審查證據
originator: kouko
kind: engineering
needs-design: no — 只調整審查工具對已記錄 Go 測試執行結果的內部判斷，以及對應的執行指引；沒有新的使用者介面或多狀態行為
status: confirmed 2026-10-23
publication: automatic — authorized 2026-10-23 by kouko

## Problem
在 Go 專案使用 Loom 的開發者，若找漏洞測試依賴同一套件的其他程式與測試工具，現有的單檔執行限制會使測試無法編譯。開發者能讓套件測試通過，卻無法讓 Loom 接受這次測試並產生最後的審查證明。

## Proposed outcome
Loom 能接受正常的 Go 套件測試作為找漏洞測試的證據，同時確認指定的測試確實執行並通過，讓審查證明可產生並通過驗證。

## Acceptance
1. 在乾淨的 Go 範例專案中，找漏洞測試需要同一套件的其他程式與測試工具時，已通過的套件測試可讓 Loom 產生審查證明，且證明通過 checker 驗證。
2. Go 套件測試沒有執行指定的找漏洞測試，或指定測試沒有通過時，Loom 不會把該執行認定為有效證據。
3. 現有可被接受的 Go 單檔測試仍可產生有效的審查證明；repo 的完整 package suite 通過。

## Constraints
- 審查工具仍須實際執行已記錄的測試指令，且該次執行必須成功。
- 不能只因套件裡有指定測試檔，就推定該檔的測試已執行並通過。

## Out of scope
- 修改 Go 專案的被測邏輯或測試內容。
- 改變其他語言測試指令的接受規則。

## Open questions
- none
