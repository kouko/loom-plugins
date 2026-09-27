# goal-create 產生提示詞並使用可用的原生 Goal
originator: kouko
kind: product
needs-design: yes — SESSION 的可見提示詞與啟用結果改變，需明定不同 host 的呈現與備援行為
status: confirmed 2026-09-27
publication: automatic — authorized 2026-09-27 by kouko

## Problem
使用者在建立長時間工作的目標時，需要可直接使用且可核對的提示詞。原有輸入來源與不同 host 的啟用能力未完整涵蓋已確認的工作文件；若提示詞工具把後續工作也直接執行，使用者無法分辨目標產生與工作執行的邊界。

## Proposed outcome
使用者指名呼叫 goal-create 後，取得完整可複製的目標提示詞；當前 host 若提供原生啟用工具，可由 agent 嘗試啟用，否則明確交付手動使用方式。skill 本身止於提示詞及啟用結果。

## Acceptance
1. SESSION 可依對話證據或已有的已確認文件產生完整提示詞，保留使用者限制；此操作不執行目標內容或推進 Loom 流程。
2. Codex 在原生工具可用時提交完整提示詞，只在主機確認成功後回報啟用；工具不可用或拒絕時，使用者仍取得完整提示詞與正確狀態。
3. Claude Code 只在當前工作階段暴露原生提議工具時嘗試啟用；未暴露時，使用者取得完整可複製的手動指令與取代現有目標的提醒，不需修改內部設定。
4. 既有 ARC 模式與目標的四欄格式、檢查及拒絕規則仍可用；發版資訊同步至新版本。

## Constraints
- skill 僅產生提示詞並嘗試可用的原生 Goal 啟用，不接管 Loom 站點或改動其機制。
- 不透過子行程、鍵盤注入或自訂 hook 模擬原生 Goal 啟用。
- 不把模擬測試稱為真實主機啟用成功。

## Out of scope
- 替使用者執行所產生的目標、改變 Loom 流程，以及開放 Claude Code 的內部功能旗標。

## Open questions
- none
