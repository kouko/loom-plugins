# Research 方法選用、方案簡化與案例驗證
originator: kouko
kind: engineering
needs-design: yes — 研究範圍、方法選用、重要方案簡化及證據不足的處理涉及多種行為，既有 spec 尚未涵蓋新增的簡化責任
evidence: [docs/loom/research/2026-11-12-design-research-framework-selection.md, loom-code/skills/engineering-research/SKILL.md, loom-code/skills/engineering-research/references/evaluation-selection.md]
status: confirmed 2026-11-13
intent_confirmed_sha: fa54053c310ef34fe2844af90e9857d8e1d9526d

## Problem
原有 Design Research 容許的研究活動超出使用者希望的網路搜尋與對談範圍，也缺少依問題選擇適用框架、流程或方法的明確引導。目前兩種研究雖可比較方案與沿用證據，仍未明確要求主動檢查重要方案是否能簡化；使用者無法確定代理會避免不必要的設計與工程負擔。

## Proposed outcome
Design Research 能依當前問題選擇適量的研究方式，在限定範圍內提供有根據且清楚標示限制的結論。Design Research 與 Engineering Research 各自能主動檢查重要方案的簡化可能，維持既有需求、限制與責任分界；透過實際案例確認其行為符合預期。

## Acceptance
1. Design Research 的研究執行限於網路研究及與當前使用者對談；不執行招募、團體訪談、工作坊、現場觀察、產品操作檢查、原型測試或實驗。
2. 方法選用符合待解問題與證據缺口；既有證據足夠時，不額外啟動研究或重問已回答的問題。
3. 研究結論可區分來源主張、使用者陳述與偏好、推論及未知；不把文獻、對談或方法名稱當成已完成的使用者研究或技術驗證。
4. 混合設計與技術問題能維持責任分界，將實作能力、相容性、可行性及安全控制實證的未解問題明確交回工程研究。
5. 延續或修正同一問題時，保留的研究紀錄與交付結論一致，並保留改變理由及限制。
6. 有可檢視的實際案例執行結果，能判定本次驗收要求的研究行為是否成立。
7. 對新增或重整的重要設計或工程方案，所屬研究技能能主動檢查是否有滿足同一需求與限制的更小方案，並清楚說明採用簡化或保留必要複雜度的理由。

## Constraints
- 複雜度留在 research skill；原有 Loom 流程盡量維持簡單。
- 可依不同場合或議題選用不同框架、流程或方法，不要求全部執行。
- Design Research 與 Engineering Research 各自負責自己的研究範疇。
- 本次採最小實作與案例驗證。
- 方案簡化的複雜度留在各自研究技能內；主流程維持不變，不新增站點或使用者確認點。

## Out of scope
- Design Research 執行招募或聯絡其他研究參與者，以及群體、現場、產品操作、原型或實驗活動。
- 各設計能力的完整專業研究手冊。
- 新增 Loom 流程站點或全面重設工程研究。

## Open questions
- none
