# 明確指定外部 agent 後不中斷完成 review
originator: kouko
kind: engineering
needs-design: no — 修正既有 skill 授權與執行契約的遵循問題；不新增使用者介面或未覆蓋的 review 行為
evidence: [docs/loom/research/2026-11-13-explicit-external-review-authorization.md]
status: confirmed 2026-11-13
publication: automatic — authorized 2026-11-13 by kouko
intent_confirmed_sha: 7f3bf253b686281a11f62553a0cd89fe859fd115

## Problem
使用者明確指示用外部 agent 做獨立 review 後，agent 仍會追加詢問是否同意傳送資料並停下來等待回答，導致 review 無法靠一次指示完成，使用者必須反覆回來接續工作。

## Proposed outcome
使用者明確指定外部 agent 與可辨識的 review 對象後，既有外部 review 能在原授權範圍內持續執行並交回有效結果，不需要第二次回答；必要告知不造成等待。

## Acceptance
1. 對已支援的外部 reviewer，明確指定 agent 與 review 對象的一次指示，足以使流程持續至有效 review 結果，中間不追加資料傳送確認或等待使用者回答。
2. 必要的費用、目的地與資料存取告知不形成新的問答或接續條件。
3. 在本機曾出現阻擋的 Codex 執行環境，以已支援的外部 reviewer 完成一次真實 review，且沒有第二次使用者回答；僅有文字規則、模擬呼叫或本機測試通過不足以判定此條通過。
4. 遇到登入、額度、服務或平台拒絕等執行失敗時，如實回報未完成，不把告知、啟動成功或測試通過當成 review 結果。

## Constraints
- 授權僅涵蓋使用者明確指定的 review 與完成它所需的相關資料；不得推及無關私人文件、秘密、其他專案或其他用途。
- 不繞過平台拒絕或以間接方式重送被拒絕的操作。
- 保留獨立 review 的要求與結果驗證；不中斷不等於降低審查品質或改用未獲授權的 reviewer。

## Out of scope
- 新增目前不支援的外部 reviewer 執行器。
- 無關本次 review 的資料傳送、發布、合併或全域安全設定變更。

## Open questions
- none
