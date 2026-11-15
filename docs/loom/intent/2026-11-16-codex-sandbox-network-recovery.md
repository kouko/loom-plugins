# 修正 Loom 對沙箱網路限制的處理
originator: kouko
kind: engineering
needs-design: no — internal skill and diagnostic guidance repair; no new interface or multi-object behavior
evidence: [docs/loom/research/2026-11-15-codex-sandbox-gh-connectivity.md]
status: confirmed 2026-11-16
intent_confirmed_sha: 7b9555dab7aeefecb50d1aae13d3de0d239d8e31
publication: automatic — authorized 2026-11-16 by kouko

## Problem
使用者透過 Loom 發布變更時，agent 可能把受限執行環境中的 GitHub 連線失敗誤判為登入、權限或服務故障，導致流程提前停止；目前需要人工指出執行環境差異才能繼續。

## Proposed outcome
Loom 能引導 agent 辨別執行環境造成的連線失敗，在政策允許且操作已授權時恢復原有流程，並如實保留拒絕與尚未確認的狀態。

## Acceptance
1. 連線不可用與登入／權限問題得到不同且與證據相符的處理，不將一般連線失敗直接斷定為 DNS 問題。
2. 執行環境限制可在政策允許且既有授權足夠時，透過適當權限重試同一個 Loom 命令；原有發布檢查仍然有效。
3. 平台拒絕、權限不可取得或重試仍失敗時，流程保留失敗證據並準確報告未完成，不改用繞過檢查的發布方式。
4. 修正具備測試與獨立驗證證據；驗收報告逐條呈現實際結果及限制。

## Constraints
- 保留預設沙箱限制，不全面開放網路，不自動授予額外權限。
- 不變更憑證，不繞過平台拒絕，不跳過既有發布與合併檢查。
- 修改限於上述問題及其必要測試、版本與發行文件。

## Out of scope
- Codex 本身的沙箱實作與全域設定變更。
- GitHub 登入修復、憑證遷移與 DNS 系統修復。
- 新增通用網路探測服務。

## Open questions
- none
