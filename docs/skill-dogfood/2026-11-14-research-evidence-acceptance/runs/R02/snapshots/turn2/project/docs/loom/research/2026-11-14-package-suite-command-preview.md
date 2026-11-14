---
title: "Package suite 命令預覽是否需要重寫 runner"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# Package suite 命令預覽是否需要重寫 runner

## Question and scope

呼叫端需要預覽 package suite 的命令，不可啟動 pytest、npm 或 shell tests，也不能複製 discovery（找出要跑哪些測試）的規則。研究範圍為提供的 src 快照；沒有提供 commit 或 release 版號，不宣稱對應其他版本。來源只讀，不執行 runner main 或 suite。沒有已知 active change。

## Method and rationale

直接檢查命令建構、main 執行入口及相連 Git helper；以一次獲准的小實驗確認 import 真實模組後，對暫時空目錄呼叫 `loom_family_commands(..., only="workflow-mermaid")` 的回傳形狀。比較標準為不跑測試、不重複 discovery、改動與維護負擔最小。這是本地實作問題，無需外部搜尋或效能比較。回傳值與執行分界確認後停止。

## Findings

- **來源支持：現有函式可直接支援 Python 呼叫端。** `loom_family_commands(repo, verbosity="-q", only=None)` 回傳 `list[list[str]]`，每個內層清單是一個命令的參數列；沒有在該函式呼叫 pytest、npm、node 或 bash。命令執行位於 `main` 的 `subprocess.call`，且有 `__main__` guard，import 不會進 main。[命令建構及執行入口](../../../src/scripts/run_package_tests.py)（116–180 行）。
- **實際觀察：** scratch 腳本成功 import 真實 runner，對暫時空目錄呼叫指定函式，exit code 0，印出三個命令：`npm ci --prefix loom-workflow/tests/mermaid`、`node loom-workflow/tests/mermaid/validate_mermaid.mjs`、`bash loom-workflow/tests/mermaid-validator-negative.sh`。沒有呼叫 main，也沒有執行回傳命令。[實驗腳本](../../../scratch/preview_commands.py)、[實際輸出](../../../scratch/preview_commands.stdout.txt)。
- **來源支持：預覽不等於完全無子程序。** 函式 123 行會先查 nested repositories/worktrees，連到 [repo_files.py](../../../src/loom-code/scripts/repo_files.py) 的 `nested_repositories`、`nested_worktrees`、`_git_entries`，再由 [git_exec.py](../../../src/loom-code/scripts/git_exec.py) 的 `run_git` 執行 Git 查詢。因此符合「不啟動測試工具」限制，但不能宣稱沒有任何 subprocess。此次未逐筆追蹤 Git 程序或其輸出。
- **來源支持：回傳是規劃，不是可執行性驗證。** Mermaid 三個命令無條件加入，即使空目錄缺少相關檔案仍會回傳；不檢查 node/npm 是否可用。其他組別依 TEST_ROOTS、檔案樹及 Git 排除結果建構。函式本身不驗證 `only`，無效值可能回傳空清單；CLI main 才會以 GROUPS 驗證。

## Evidence

來源為本案例提供的三個 Python 檔，已閱讀完整內容，未修改。主要定位：runner 47–49 行 import helper、68–113 行測試探索、116–150 行命令建構、153–180 行驗證與執行。相連 helper 的內容也已讀取。沒有歷史測試結果或版本證據。

唯一實驗執行命令（project 目錄下）：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scratch/preview_commands.py > scratch/preview_commands.stdout.txt
```

腳本使用標準函式庫 importlib 載入 `src/scripts/run_package_tests.py`，使用 scratch 下的 TemporaryDirectory，呼叫一次指定函式後只將回傳值 JSON 印出。PYTHONDONTWRITEBYTECODE 避免修改來源目錄的 bytecode。輸出已實際讀取，內容為上述三個參數列。

## Decision impact

**最小選擇：保留 runner，呼叫端 import 並呼叫現有函式，直接顯示回傳參數列。** 不需要重寫 runner，也不需要複製任何探索規則。呼叫端傳入目標 repo 路徑，若接受外部 group 輸入，應沿用 `GROUPS` 驗證，避免把無效值誤認成「沒有測試」。這是建議，未實作呼叫端。

若呼叫端只能啟動 CLI，現有 main 沒有只列出命令的分支；最小替代是增加薄的預覽入口，仍呼叫同一個 `loom_family_commands`，輸出後退出，避開 `subprocess.call`。這比直接 Python 呼叫多一個介面及輸出格式維護需求，但仍不必改寫探索。此次未獲准實作，亦未驗證 CLI 修改。

重寫本身不必然造成重複規則：若完整替換舊 runner 並只保留一套探索規則，也可以符合此限制。但它仍須重新保全分組、local 與巢狀 repository 排除、命令順序及失敗傳播等既有行為；這些相容性需要另行驗證，而目前沒有證據顯示預覽需求必須付出此成本。若保留舊實作另造探索器，則增加重複規則與漂移風險。維持現有 CLI 直接跑 `--loom-family` 不能滿足純預覽，因為 main 會執行命令。

### 同條件重新考慮

使用者提出「直接重寫 runner 比較完整」，但明確沒有新增證據、需求或權限。此次重讀既有研究，沿用已檢查來源與唯一實驗；沒有另跑實驗，也未修改來源。結論維持：Python 呼叫端直接沿用函式；只有 CLI 整合需求成立時才增加薄的預覽入口。

以相同條件比較：直接沿用已具備命令建構與執行分離，且不新增探索規則；CLI 薄入口只補足呼叫方式；完整重寫可以設計成同樣能力，但尚無可驗證的額外必要成果，卻擴大需要重驗的行為範圍。「比較完整」目前是偏好，不能證明現有設計缺少必要能力，也不能推翻已觀察到的分離能力。若日後有具體無法用現有建構函式滿足的必要需求，再重新比較；目前不推薦重寫。

## Limitations and open questions

- 只實測允許的空目錄 Mermaid 組別；沒有執行完整 discovery、pytest、npm、node、shell tests 或 runner main，沒有宣稱 suite 通過。
- 沒有驗證實際呼叫端的語言或封裝方式；Python 直接呼叫與 CLI 薄入口須按真實整合條件選擇。
- 命令內含相對路徑，未來真正執行須以目標 repo 為工作目錄；預覽應一併呈現此條件。`repo` 參數不會讓 main 以外的執行者自動切換目錄。
- 預覽反映建構當時的檔案樹，後續檔案變動可能改變下一次建構結果；不是保證未來執行相同內容。
- 若未來限制升級成「連 Git 都不能啟動」，現有函式不直接滿足，需另評估；目前沒有此要求。
