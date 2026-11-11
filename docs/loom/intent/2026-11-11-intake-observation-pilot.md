# 小範圍整合規劃進站檢查，並查明輸入證據的限制
originator: kouko
kind: engineering
needs-design: yes — 試作涉及通過、阻擋與無法判定等內部觀察結果，目前沒有涵蓋此整合的規格
evidence: [docs/loom/research/2026-11-11-recursive-decision-models-for-loom.md, docs/loom/research/2026-11-11-mechanical-decision-input-evidence.md]
intent_confirmed_sha: 27df9050ee80824e9b8f0ad7e4ae06bc20a2689e
status: confirmed 2026-11-11
publication: automatic — authorized 2026-11-11 by kouko

## Problem
Loom 已有進站檢查與模型分派規則，但尚未確認把既有檢查結果直接提供給代理，能否減少重複判讀而不漏掉必要檢查。部分機械判定的輸入仍由代理提供，輸入缺漏、判斷失準與證據過期的影響尚需分清，否則容易把規則執行正確誤認為判斷可靠。

## Proposed outcome
在規劃進站這一個有限範圍試用既有檢查結果，讓代理能直接依據可追溯的結果處理進站條件，並得到對整合效果與輸入可信程度有實證支持的評估。

## Acceptance
1. 規劃進站的試作整合能提供與既有檢查一致的通過或阻擋結果及其原因；無法取得必要資訊時不會被報為通過。
2. 試作的觀察操作不修改被觀察的專案內容、不自動推進流程，且不放寬既有確認、審查與驗收條件。
3. 提供可重現的前後比較，呈現代理實際使用整合結果的情形、判定一致性與額外成本；無法證明節省時明確記錄，而不宣稱已改善效率。
4. 輸入研究列出會影響本次判定及模型分派的主要輸入來源、可由程式驗證的範圍、仍須語意判斷的部分與缺漏或矛盾案例，並區分實測、推論及尚未驗證的事項。

## Constraints
- 以既有檢查結果的小範圍整合為試作範圍。
- 保留現有使用者決策點，以及 writer 與 judge 分離的驗證要求。
- 本次研究不得以機械測試通過替代實際語意正確性或效益證明。

## Out of scope
- 全站自動排程器、遞迴決策框架與新分類模型服務。
- 自動取代使用者授權、獨立審查或驗收。
- 因研究發現而全面改寫分派政策。

## Open questions
- none
