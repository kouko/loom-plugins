---
title: "不執行測試且不重複 discovery 的 JSON 命令介面"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# 不執行測試且不重複 discovery 的 JSON 命令介面

## Question and scope

不能 import Python 的獨立呼叫程序，需要透過命令取得 JSON suite 命令陣列；不得執行測試或重寫／重複 discovery。只評估提供的 project/src 快照，不實作、不執行 runner/main/suite、不連網。未提供 commit 或部署版本。

## Method and rationale

只讀入口、命令建構函式及其 git discovery 相依路徑，以必要條件淘汰方案，再比較最小替代方案。此問題可由控制流程判斷，無需執行測試、基準或外部來源。

## Findings

- **直接執行 runner 不成立。** `--loom-family --only workflow-mermaid` 會建構三個命令：npm ci、node validator、bash negative check。`main` 隨後逐一 `subprocess.call`，不是輸出 JSON；第一個成功後還會執行驗證測試。npm ci 也會安裝依賴。
- **叫外部程序 import 函式，描述本身不夠。** 原函式回傳 Python list，沒有 JSON CLI；若指要求呼叫端 import，直接違反呼叫端限制。若意指另建 Python 子程序負責 import、呼叫一次並 JSON 序列化，那已是新增 adapter，不能聲稱現成函式本身滿足命令協定。獨立呼叫端不能 import 不代表 Python adapter 內部也不能 import。
- **最小可行形狀（設計推論，未實作）：** 在現有 CLI 加明確的僅列出 JSON 模式。保留既有 group 驗證，呼叫 `loom_family_commands` 一次，將整個 `list[list[str]]` 用 JSON 輸出後立即 return，絕不進入執行迴圈；一般 runner 行為保持原樣。這重用唯一命令建構與 discovery，無需新增另一份掃描器、硬編碼 Mermaid 命令或先 discovery 再跑一次取得結果。
- 若原檔必須永久不改，薄 Python adapter 也是條件可行替代：內部 import 同一函式、傳入明確 repo、只呼叫一次並序列化；外部 caller 只啟動命令並解析 JSON。它增加入口與維護檔案；不能 import 的限制若涵蓋 adapter 也不能用，需先釐清。對本次「不修改來源」限制，兩者都僅是後續設計，沒有既成可執行介面。

## Evidence

來源均為本地靜態程式碼，未測量執行結果：

- [runner](../../../src/scripts/run_package_tests.py)：L116–150 `loom_family_commands` 回傳命令陣列；L139–145 定義 Mermaid 的 npm/node/bash 三命令。L153–167 解析 group 後直接執行，無 JSON 輸出分支；L179–180 腳本入口呼叫 main。L123 即使 only Mermaid 也呼叫兩個 foreign-repository discovery 函式，因此不要另複製或再呼叫一遍 discovery。
- [repository discovery](../../../src/loom-code/scripts/repo_files.py)：`nested_repositories` 使用 `_git_entries`，`nested_worktrees` 使用 git worktree list；需保留原有外部 subtree 語意，不能以硬編碼替代一般 suite discovery。
- [git execution helper](../../../src/loom-code/scripts/git_exec.py)：`run_git` 執行 git 並處理輸出／錯誤；這是命令建構所依賴的 metadata 查詢，不是 suite 執行。

實際執行的調查操作僅有 `rg --files`、`nl -ba`、`cat` 讀取來源與技能，以及建立／讀回本記錄。未執行上述 runner、其函式或測試。

## Decision impact

拒絕直接 runner 與「只有 import 就夠」兩案。建議後續採同檔 JSON-only CLI 分支，以最少新增維護面提供真正的程序邊界；若不允許修改 runner，才用薄 adapter。必要驗收應包含合法 JSON 陣列、一次命令建構、零測試／安裝子程序呼叫、錯誤參數不混入 JSON stdout；本次未執行這些驗收。

## Limitations and open questions

這是完整提供來源範圍內的控制流程判讀，非已實作功能或成功執行證明。呼叫端實際工作目錄、Python 路徑、stdout 編碼及 adapter 是否受禁 import 約束未提供；後續需明確 repo 參數或工作目錄，避免 main 的 Path.cwd 指錯目標。本次禁止 source 修改，故尚不能交付可用 JSON 命令；沒有假稱取得實際 suite JSON 或完成 runtime 驗證。
