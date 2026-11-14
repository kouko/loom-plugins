---
title: "同程序預覽 workflow-mermaid 是否需要服務與索引"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# 同程序預覽 workflow-mermaid 是否需要服務與索引

## Question and scope

只在同一個受信任的本機 Python 程序預覽 workflow-mermaid 命令陣列。判斷 HTTP 服務、常駐索引與另一份測試發現設定是否必要。不實作、不啟動服務、不執行 suite 或 main、不連網。適用於本次提供的 src 快照；未提供可辨識 commit 或版本。

## Method and rationale

只讀實作與相連呼叫路徑，做輕量方案比較。共同判準是能否取得相同命令陣列、是否維持現有命令來源、是否增加維護及執行負擔。來源已直接回答能力問題，無需實驗、效能測量或外部搜尋。

## Findings

- **來源事實：** `loom_family_commands(repo: Path, verbosity="-q", only=None)` 回傳 `list[list[str]]`；指定 `only="workflow-mermaid"` 時加入以下三筆陣列：
  ```python
  ["npm", "ci", "--prefix", "loom-workflow/tests/mermaid"]
  ["node", "loom-workflow/tests/mermaid/validate_mermaid.mjs"]
  ["bash", "loom-workflow/tests/mermaid-validator-negative.sh"]
  ```
- **來源事實：** 命令建構與執行分離；`main` 才遍歷回傳值並呼叫 `subprocess.call`。匯入模組不會通過 `__main__` 條件執行 main。預覽不可呼叫 main。
- **邊界：** 建構函式仍會先呼叫 `nested_repositories` 與 `nested_worktrees`，它們透過 `run_git` 啟動唯讀 Git 查詢。因此這不是完全無子程序的純函式，但不會執行陣列中的 npm/node/bash 命令。
- **推論／建議：** 最小方案是由同程序載入既有模組，呼叫 `loom_family_commands(repo, only="workflow-mermaid")`，直接顯示回傳陣列；`repo` 應是實際目標專案根目錄，勿因本次來源放在 src 下而混淆。模組不在 import 路徑時可用標準庫 `importlib` 載入既有檔案，無需新增套件或服務。

## Evidence

本次實際使用 `rg --files` 列出提供的來源，並以 `nl -ba` / `cat` 讀取以下實作；沒有執行它們。

- [run_package_tests.py](../../../src/scripts/run_package_tests.py)：116–150 行定義回傳陣列與群組篩選；139–145 行提供三筆 Mermaid 命令；153–180 行顯示 main 的執行邊界；47–49 行顯示相鄰 helper 的匯入路徑；53–55 行為既有 roots/groups 設定。
- [repo_files.py](../../../src/loom-code/scripts/repo_files.py)：`nested_repositories` → `_git_entries` 查詢 Git 的 bare/root/listing；`nested_worktrees` 查詢 `git worktree list`，失敗時回傳空清單。
- [git_exec.py](../../../src/loom-code/scripts/git_exec.py)：`run_git` 的 `subprocess.run` 實作，說明建構階段仍存在唯讀 Git 子程序。

以上是來源檢查證據，並非成功執行、測試通過或效能量測紀錄。

## Decision impact

保留既有程式介面即可滿足需求。HTTP 服務同樣能包裝結果，但此處沒有跨程序或遠端呼叫需求，會增加協定、服務生命週期與錯誤處理；常駐索引增加更新與失效處理，且這個群組的命令直接由固定陣列建立；第二份發現設定增加同步與漂移負擔，無法為這三筆陣列帶來必要能力。三項新增均無本次需求所需的理由。

若日後確實需要跨程序呼叫，才重新評估傳輸介面；若有代表性測量證明查詢負擔不可接受，再評估快取。此處沒有性能證據，不宣稱索引一定較慢。若新增「不得啟動任何子程序」要求，既有介面因 Git 查詢而不完全符合，須另行研究最小調整。

## Limitations and open questions

未執行匯入、函式、main、suite 或服務；未驗證實際環境 import 是否成功、Git 可用性、命令目標檔是否存在、npm/node/bash 是否可用或命令能否成功。僅憑提供快照判斷設計必要性，不宣稱部署狀態、歷史成功或完整效能。來源未修改。
