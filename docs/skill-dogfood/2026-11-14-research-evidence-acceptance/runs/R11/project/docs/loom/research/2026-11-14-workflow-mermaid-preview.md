---
title: "同程序預覽 workflow-mermaid 命令的最小方案"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# 同程序預覽 workflow-mermaid 命令的最小方案

## Question and scope

在同一個受信任的本機 Python 程序中，只取得 workflow-mermaid 的命令陣列，是否需要 HTTP 服務、常駐索引及另一份測試發現設定？充分證據是既有介面能回傳該組陣列、建立與執行路徑分離，並查清產生陣列時的副作用。硬性條件是不實作、不啟動服務、不執行 suite、不安裝、不連網。

## Method and rationale

採來源呼叫路徑檢查與簡短方案比較，以需求符合度、重複設定及運作負擔為判準。只讀本次提供的來源快照；讀完相關產生、執行與 Git 輔助函式即停止。未執行任何實驗，亦不需要外部資料或效能數字。

## Findings

- 已支持：`loom_family_commands(repo, only="workflow-mermaid")` 回傳 `list[list[str]]`；139–145 行直接加入三個命令，不依賴測試發現結果。既有介面已滿足取得陣列的需求。
- 已支持：產生命令與執行分離。`main` 於163–166行才迭代命令並呼叫 `subprocess.call`；模組末尾有 `__name__` 保護。預覽者應載入模組並呼叫函式，不呼叫 `main`，也不執行回傳的命令。
- 邊界：這不是完全無副作用的純函式。即使指定 Mermaid，123行仍先查巢狀 repository/worktree；`repo_files` 經 `git_exec.run_git` 執行唯讀 Git 查詢。模組載入亦會修改 `sys.path`。本次僅讀來源，沒有實際載入或呼叫。
- 來源所定義的陣列依序為 `['npm', 'ci', '--prefix', 'loom-workflow/tests/mermaid']`、`['node', 'loom-workflow/tests/mermaid/validate_mermaid.mjs']`、`['bash', 'loom-workflow/tests/mermaid-validator-negative.sh']`。這是靜態來源結果，並非實測輸出；尤其不得因預覽而執行 `npm ci`。

## Evidence

本次版本為提供的本機來源快照，未提供 commit/version，未以其他 checkout 代替。

- [run_package_tests.py](../../../src/scripts/run_package_tests.py)：47–49行載入依賴；116–150行產生陣列；139–145行定義 Mermaid 命令；153–180行顯示執行邊界。已讀完整內容。
- [repo_files.py](../../../src/loom-code/scripts/repo_files.py)：`nested_repositories`、`_git_entries`、`nested_worktrees` 的實作顯示 Git 查詢及無 Git 時的空集合行為。已讀完整內容。
- [git_exec.py](../../../src/loom-code/scripts/git_exec.py)：`run_git` 呼叫 `subprocess.run`，一般失敗回傳 `None`。已讀完整內容。沒有執行成功的證據，也不以定義當作執行紀錄。

## Decision impact

建議最小方案為同程序直接載入既有 Python 模組，以真正的 repository root 作 `Path` 參數呼叫 `loom_family_commands(repo, only="workflow-mermaid")`，在記憶體中顯示回傳陣列。來源快照位於 `src/`；真正部署時應傳入含 `loom-workflow/` 的根目錄，而非假設本次研究 project 目錄就是實際 suite 根目錄。

HTTP 服務同樣可以轉送這份陣列，但目前沒有跨程序或遠端呼叫需求可支持它；會另增服務生命週期、協定與錯誤處理。常駐索引沒有可支持的查詢或效能需求，而本組陣列是固定定義；會新增更新與過期問題。另一份測試發現設定也沒有必要，因本組直接由現有來源定義；複製規則會新增同步負擔。這些是新增設計的負擔推論，非量測成本或已證實漏洞。

若日後需要跨程序存取、不能接受現有 Git 查詢副作用、或有實測效能問題，再另行評估；目前條件不支持為「比較完整」加入這三項。

## Limitations and open questions

未執行 suite、未匯入模組、未實測函式或效能，也未驗證目標命令所指檔案是否可執行；這些不影響此處來源層級的設計判斷，但不能宣稱 runtime 驗證通過。既有函式對未知 `only` 不自行報錯，驗證在 CLI 的 `main`；本案使用已知常數，無須新增通用驗證架構。
