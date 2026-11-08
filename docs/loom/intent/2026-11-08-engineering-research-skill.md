# 將軟體工程研究能力納入 Loom
originator: kouko
kind: engineering
needs-design: yes — 新增可持續保存的研究文件及跨任務收尾的知識保存行為，涉及多個文件與條件分支，現有試驗稿尚非正式規格。
evidence: [docs/loom/2026-11-07-engineering-research-trial/revision-5-framework-selection/decisions.md, docs/skill-dogfood/2026-11-08-engineering-research-frameworks/report.md, docs/loom/research/2026-11-08-engineering-evaluation-framework-selection.md]
intent_confirmed_sha: bd80f2c5840966f36ef1df243e79d8c482215828
status: confirmed 2026-11-08
publication: automatic — authorized 2026-11-08 by kouko

## Problem

kouko 希望一般工程討論中會影響決策的前提、功能與完成聲明能得到適時查證，
並留下可回查、可延續的研究紀錄。目前研究方法、來源判斷與文件保存規則仍在
試驗稿，尚未成為正式 Loom 能力；具有長期或跨專案價值的研究，也缺少與變更
完成後保存至 Obsidian 的銜接。

## Proposed outcome

在 loom-workflow 提供按需使用的軟體工程研究 skill，供 Loom 任務與獨立工程
討論使用。它能依待決問題核對前提、取得適用證據、選擇適當研究或評估方法，
留下可追溯紀錄，再將有根據的結論或尚未解決的不確定性帶回原任務。適合長期
保存的研究，能在變更完成後提出保存提議，經使用者當次授權才寫入 Obsidian。

## Acceptance

1. 正式 loom-workflow 可發現並使用 engineering-research；既有 Loom 任務仍可在未使用此能力時正常進行。
2. 在代表性工程證據缺口與一般查詢中，研究能力能按問題的重要性適當使用，保留原任務的目標與授權範圍。
3. 研究能核對前提及適用條件，對結論提供可回查的證據，並區分來源推論、實際執行與尚未驗證的聲明；所聲稱的研究產物可實際核對。
4. 工程評估能按問題選用合適方法；單純問題可直接查證，混合問題可使用必要的互補方法，不強制套用全部框架、工具或來源。
5. 每個獨立研究問題有可追溯的 Markdown 紀錄，具備 frontmatter 並可供 Obsidian 與一般 Markdown 工具閱讀；延續研究與條件改變後的重新驗證能保留原有依據。
6. 禁止寫入或無法保存時，提供明確標示的未儲存研究內容，不誤稱已產生保存文件。
7. GitHub／GitLab 實作行為的研究會檢查相關原始碼與相連條件；結構圖按需使用，其關係與不確定性不會取代證據或被誤稱為已驗證因果。
8. 在變更合併至 main 後，具有長期或跨專案價值的研究可獲得 Obsidian 保存提議；依賴釋出成立的內容須有相應釋出證據，未經當次明確授權不寫入 Vault，保存內容可回溯專案原始紀錄與版本。
9. 正式技能的載入、與原任務的銜接及上述研究行為有實際驗收證據；試驗稿、正式安裝及未驗證宿主的結果不混為同一項完成聲明。

## Constraints

- 以第 5 版試驗稿的已討論行為為實作基礎，研究是按需能力，不新增 Loom 站點或強制品質閘。
- 研究按問題分檔並採用 frontmatter；相同問題與條件延續原紀錄，重大條件變化保留原決策依據。
- 研究方法、框架、來源及 Mermaid 均按問題需要選用，不設固定數量或一律執行的完整清單。
- 研究原始紀錄保留於專案；Obsidian 保存由使用者當次確認目的地與範圍，不因偵測到 Vault 便自動寫入。
- 保留既有試驗稿、研究與 dogfood 原始紀錄及其限制，不以正式化為由改寫先前結果。
- 延續現有研究工具與 Loom 流程的授權界線；研究建議本身不構成安裝、對外聯繫、正式環境操作或不可逆資料變更的授權。

## Out of scope

- 用程式保證每次研究必然啟用，或宣稱框架指引已證明提升所有模型的研究品質。
- 對既有 Obsidian 筆記的自動同步、批次重整、刪除或未授權覆寫。
- 新的背景研究服務、排程服務或常駐 Vault 監控。
- 自動合併本次變更，以及更新使用者既有 plugin 安裝與個人設定。

## Open questions
- none
