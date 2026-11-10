# 以實際 Git／PR 狀態確認交付，並在阻擋時提供下一步
originator: kouko
kind: engineering
needs-design: yes — 交付狀態、本地 Git 保護與發布／合併失敗處理形成新的跨本機及遠端多狀態契約，既有 spec 未共同涵蓋。
evidence: [loom-code/skills/ship/SKILL.md, loom-design/skills/capture-intent/SKILL.md, loom-code/scripts/loom_checker/command_handlers/publish.py, loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/loom_checker/command_handlers/push.py, loom-code/scripts/loom_checker/command_handlers/github_rules.py, PRINCIPLES.md]
status: confirmed 2026-11-09
intent_confirmed_sha: c089c6af658d6659c48d33e441a7172bae6f6d28
publication: automatic — authorized 2026-11-09 by kouko

## Problem
使用者在本機多個專案遇到 agent 已宣稱實作完成，卻沒有推送或開 PR，必須追問才繼續交付；也遇到 agent 以改動小或測試通過為由直接在 main 提交，以及發布／合併受阻後改用其他指令操作 main。現有錯誤回報未必能讓 agent 判斷下一步，使用者必須再次介入解釋、補流程或同步分歧的主分支。

## Proposed outcome
Loom 依本次授權的交付目標，以可重新查驗的本機與遠端事實判定完成；Git 分支與 PR 政策不因變更大小或 Loom 步驟簡化而被自行省略。本地與遠端主分支具有對應的操作限制，發布／合併失敗能區分具體原因，並連同適用且安全的下一步建議回傳，使已授權的工作能接續處理或明確回報阻擋。

## Acceptance
1. 交付檢查能以實際提交、遠端分支與 PR 的對應關係，區分尚未提交、尚未推送、尚未開 PR、檢查未完成、已發布與已合併；未達本次授權目標或證據不可取得時，不回報交付完成。
2. 已明確限定只在本機交付的變更，不會被要求推送、建立 PR 或合併；未取得發布或合併授權的變更不會因完成檢查而自行執行外部操作。
3. 在啟用保護的專案，一般 Git 提交與會建立合併提交的操作在主分支被拒絕，在功能分支可正常進行；保護不依賴 shell 指令必須以 git 開頭，既有 Git hooks 與未提交工作受到保留，已經由 PR 合併的遠端主分支仍可正常同步。
4. 遠端主分支的 PR 要求與必要檢查能被查驗並提供設定方式；在已啟用相應規則的驗證環境，直接更新主分支及未通過必要檢查的 PR 合併均被拒絕，讀不到規則時不宣稱已受保護。
5. 發布與合併對檢查失敗、等待中、診斷或權限不可取得及成功回傳可區分的結果；失敗或無法確認不會被當成成功，也不會使流程自動轉往直接更新主分支或跳過必要檢查的路徑。
6. 本次交付、主分支保護及發布／合併檢查發現問題時，同時回傳具體原因與對應的下一步建議；建議不要求繞過保護、丟棄既有工作或擅自執行未授權的操作，無安全自動修復方式時明確說明缺少的條件。
7. 小改動與工程性變更適用相同的專案分支及 PR 政策；現有受支援宿主能使用這組交付檢查與回報，不以 agent 自述或只比對文件措辭作為驗證證據。

## Constraints
- 使用者選定 1B＋2A/B＋3B：機械核對交付、將分支／PR 政策與步驟簡化分開、在 Git 與 GitHub 執行限制，以及回傳明確發布／合併結果。
- 使用者要求機械檢查除了具體錯誤，也直接回傳建議做法。
- 本地 Git 保護會影響啟用專案中使用者與 agent 的一般 Git 操作；現有「只用宿主 hooks、不用 Git hooks」原則需隨本變更明確修訂，不暗中保留矛盾政策。
- 既有本機專案、歷史、未提交修改、Git hook 與遠端保護設定均不擅自覆寫；本變更提供可驗證的保護與設定方式，實際啟用依專案授權進行。
- 維持本機交付例外，以及發布與合併各自的授權邊界；完成檢查不授權額外網路寫入。
- 沿用既有 checker 與發布／合併入口，加入可執行的回歸驗證；新增機制依 PRINCIPLES.md 記錄數量與必要的預算例外。

## Out of scope
- 修復其他專案既有的未提交功能、重寫歷史或自動清理分支與工作目錄。
- 批次替所有本機專案安裝保護或修改 GitHub 規則。
- 新增常駐監控服務、排程或獨立的交付工作流框架。
- 宣稱本地 Git hooks 能阻止所有刻意繞過或所有低階 Git 操作。
- 將本次無關的 checker 錯誤全面改寫。

## Open questions
- none
