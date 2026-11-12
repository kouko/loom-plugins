# 延續整理代理操作 CLI 的一致性
originator: kouko
kind: engineering
needs-design: yes — 其餘命令的操作說明與錯誤回覆尚未由上一輪三命令規格涵蓋
intent_confirmed_sha: 9455be5ff8c81053bc88d3d0e6b531c05a0eb08c
status: confirmed 2026-11-12
publication: automatic — authorized 2026-11-12 by kouko

## Problem
上一輪只涵蓋三個命令；代理使用其他既有命令時，仍需面對不同的說明入口與錯誤回覆。整體 CLI 規範尚未完成整理。

## Proposed outcome
代理能以一致且足夠的操作資訊使用既有命令，辨識輸入錯誤與可行的下一步。

## Acceptance
1. 本輪選定命令的說明入口與必要操作資訊符合共同規範，獨立操作者能依說明完成既有任務。
2. 可由呼叫端修正的錯誤提供可執行的下一步，且不把被阻擋或無法確認誤認為完成。
3. 既有合法呼叫、結果讀取、退出狀態及授權與驗證條件保持相容。

## Constraints
- 完成已安裝新版的實際操作測試後才開始本輪整理。
- 保留既有 worktree；逐步整理，不一次全面重寫所有工具。

## Out of scope
- 新業務能力與與 CLI 操作一致性無關的重構。

## Open questions
- none
