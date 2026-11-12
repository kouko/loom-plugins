# 讓代理直接讀取準備檢查結果的小範圍試點
originator: kouko
kind: engineering
needs-design: yes — 新增命令結果格式，既有規格未涵蓋選用 JSON 輸出與相容性
intent_confirmed_sha: dd4c59806261556d67cdf4d750e63d0ddfc4922d
status: confirmed 2026-11-13
publication: automatic — authorized 2026-11-13 by kouko

## Problem
目前 plan 與 intake 的結果主要由退出碼、固定前綴與文字診斷組成。代理仍需讀取文字判斷檢查結果及原因，尚未驗證結構化結果是否能改善操作。

## Proposed outcome
代理可直接讀取這兩個命令的結構化結果，並以實際比較評估其操作價值。

## Acceptance
1. plan 與 intake 可選擇輸出可被程式穩定解析的結果，能辨識通過、規則阻擋與呼叫錯誤，以及對應的診斷資訊。
2. 既有文字呼叫的輸出、退出狀態、檢查範圍及授權與驗證條件保持相容。
3. 同一組真實任務的文字與結構化操作有可追溯比較，列出判讀錯誤、修正次數、操作步數及輸出量，明列限制與未改善項目。

## Constraints
- 小範圍試點限於 plan 與 intake，使用選用的 --json。
- 保留既有文字輸出與退出碼。
- 保留目前與上一輪 worktree。

## Out of scope
- 其餘命令的格式遷移、資料轉換工具與無關重構。

## Open questions
- none
