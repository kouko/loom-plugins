# 建立一致的機器可讀結果規範並分批導入
originator: kouko
kind: engineering
needs-design: yes — 涉及跨命令公開結果規範及新增唯讀命令的選用結構化輸出
intent_confirmed_sha: 7dd7da523efc2f41876729d2cf26bfd957c38b90
status: confirmed 2026-11-13
publication: automatic — authorized 2026-11-13 by kouko

## Problem
目前 Loom 命令的結果包含文字、整數、表格、CI 訊息及不同 JSON 介面。代理或程式需分別理解命令差異，尚無覆蓋全部主要命令的一致性規範與分批導入依據。

## Proposed outcome
主要命令具有明確的共同機器可讀結果規範及適用邊界，並由一批唯讀命令證明可落實且保持相容。

## Acceptance
1. 全部主要子命令的既有輸入、輸出、狀態、退出碼與副作用有可追溯盤點，共同規範對各命令的適用方式及例外可被獨立核對。
2. 本輪選定的唯讀命令可選擇輸出一致、可被程式解析且保留命令特有資料的結果，成功與失敗語意符合共同規範。
3. 既有文字呼叫、已發布 JSON 介面、退出狀態、檢查條件及授權行為保持相容；未導入命令的狀態明確揭露。
4. 全部主要公開子命令提供清楚且可安全探索的說明，操作者能了解功能、必要輸入、結果與操作後果，而不因查閱說明執行實際工作。

## Constraints
- 先盤點與定義共同規範，再分批導入；本輪實作限一批唯讀命令。
- 保留全部現有 worktree。
- 先整理全部主要子命令的 help 並確認與實作一致，再擴充 JSON。
- 不以 JSON 格式本身宣稱 LLM 表現或操作效率改善。

## Out of scope
- 本輪對發布、合併、清理等寫入命令新增 JSON。
- 啟動器命名、執行環境管理與無關重構。

## Open questions
- none
