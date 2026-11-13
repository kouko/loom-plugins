# 先獨立交付與實作一致的 CLI help
originator: kouko
kind: engineering
needs-design: yes — 涉及全部主要命令的公開說明與安全探索介面
intent_confirmed_sha: 66583a51db46
status: confirmed 2026-11-13
publication: automatic — authorized 2026-11-13 by kouko

## Problem
目前 Loom 主要命令的說明覆蓋不完整；命令的輸入、退出語意、副作用與完成限制不同，操作者難以安全探索並正確理解實際行為。

## Proposed outcome
先獨立交付全部主要命令清楚、可安全探索且與實作一致的 help；JSON 擴充留到下一輪，這次不新增。

## Acceptance
1. 全部主要子命令的既有輸入、輸出、狀態、退出碼與副作用有可追溯盤點，各命令的適用方式及例外可被獨立核對。
2. 全部主要命令的 help 與實際參數、模式、前置條件、結果、錯誤路徑及操作後果一致，並經獨立逐一核對。
3. 既有文字呼叫、已發布 JSON 介面、退出狀態、檢查條件及授權行為保持相容；現有 JSON 支援範圍明確揭露，本輪不新增 JSON 介面。
4. 全部主要公開子命令提供清楚且可安全探索的說明，操作者能了解功能、必要輸入、結果與操作後果，而不因查閱說明執行實際工作。

## Constraints
- user-decided — 2026-11-13 使用者同意「先把 help 整理獨立交付，JSON 留下一輪」；此確認取代本變更先前的 JSON 實作範圍。
- 保留全部現有 worktree。
- 本輪範圍限全部主要子命令的 help、相容性與驗證；保留先前失敗及修正通過的證據。
- 不以 JSON 格式本身宣稱 LLM 表現或操作效率改善。

## Out of scope
- 任何命令新增 JSON、共同機器可讀結果格式與資料轉換工具；未確認下一輪的具體設計或實作承諾。
- 啟動器命名、執行環境管理與無關重構。

## Open questions
- none
