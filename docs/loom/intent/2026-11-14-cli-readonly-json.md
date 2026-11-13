# 兩個唯讀工具的 JSON 試作與實際流程驗證
originator: kouko
kind: engineering
needs-design: yes — 新增兩個公開 CLI 的 JSON 模式與結果契約，現有規格未涵蓋
status: confirmed 2026-11-14
intent_confirmed_sha: 496b642094663a227fabe0d864e1ae7f7b2ef446
publication: automatic — authorized 2026-11-14 by kouko

## Problem
目前讀取規範版本與計算所需審查人數的工具沒有可選 JSON 輸出，與已有 JSON 模式的工具不一致；自動化消費者難以用同一套明確的結果語意判讀成功、阻擋與輸入錯誤。

## Proposed outcome
先讓 contract 與 reviewer-count 兩個唯讀工具提供可選、可完整解析的 JSON 結果，維持既有呼叫相容，並由實際消費結果的流程驗證其用途與限制。

## Acceptance
1. 兩個工具的可選 JSON 模式均能完整解析，成功、阻擋與錯誤結果的含義及工具資料可被消費者明確辨識。
2. 原有文字呼叫、退出碼、既有 JSON 介面、檢查條件與授權行為保持相容。
3. 新模式維持原有副作用及啟動界線，不因輸入錯誤執行無關工作；輸出不以成功退出冒稱領域結果已完成。
4. help 與相關說明準確揭露兩個工具的 JSON 支援、必要輸入、結果範圍及錯誤限制。
5. 乾淨環境中的 dogfood 流程實際讀取 JSON 欄位並做判斷，涵蓋正常及失敗情況；結果、相容性與未驗證界線有可核對證據。

## Constraints
- 範圍限 contract 與 reviewer-count 的 JSON 試作及必要相容性、說明與驗證。
- 保留全部現有 worktree 與既有驗證紀錄。
- 不以 JSON 格式本身宣稱 agent 更快、成本更低或 token 更少。
- 使用者指示：「dogfood testing 沒問題就直接走標準流程合併吧」；僅在 dogfood、獨立審查、完整測試與 CI 均通過且沒有未解重要問題時自動合併。

## Out of scope
- 其餘工具新增 JSON、JSONL、欄位篩選、通用輸出框架或新依賴。
- 啟動器更名、執行環境重設、授權政策或既有 JSON 格式重設。
- 已安裝 plugin 更新及真實使用者資料遷移。

## Open questions
- none
