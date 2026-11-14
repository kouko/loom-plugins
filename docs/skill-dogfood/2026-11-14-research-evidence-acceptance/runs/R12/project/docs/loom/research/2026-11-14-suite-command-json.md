---
title: "不執行測試的 suite 命令 JSON 介面"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# 不執行測試的 suite 命令 JSON 介面

## Question and scope

不能匯入 Python 的獨立呼叫程序，如何透過命令取得 JSON 格式的 suite 命令陣列，同時絕不執行測試、也不另寫一套 discovery？充分證據是沿現有入口追到命令生成、輸出與執行分支，確認兩個提案是否全數符合必要條件，再找出最小修改。範圍僅本 project 提供的來源快照，無已知 commit；本次不實作、不執行 runner 或 suite。

## Method and rationale

只讀程式呼叫路徑，作必要條件逐項比較。這是介面可行性問題，現有完整入口與生成函式已足以判斷，無需量測、網路或新實驗。最少程式碼是偏好；不可執行測試、不可重複 discovery、外部程序只透過命令取得 JSON 是不能犧牲的條件。

## Findings

- **直接執行現有 `--loom-family --only workflow-mermaid` 不符合。** `main()` 取得命令後直接呼叫 `subprocess.call()`，沒有 JSON 輸出或僅列命令的分支（L153–167）。該群組的第一項是 `npm ci`，其後是 Node validator 和負向 shell 測試（L139–145）；不但不能取得要求的 JSON，還會進入安裝與測試執行路徑。
- **讓外部呼叫程序只 import 函式不符合。** `loom_family_commands()` 確實回傳 `list[list[str]]`，生成命令而不執行 suite（L116–150）；但 Python 物件並非命令介面的 JSON，而且要求中的呼叫程序不能 import Python。即使將 import 放在 `python -c` 子程序並序列化，也只是增加另一個 Python 包裝入口，並非現有 CLI 的能力；本次未實作或驗證此包裝。
- **最小可行替代是替既有 CLI 增加明確的 JSON 列印模式。** 沿用既有群組驗證與 `loom_family_commands()`，僅呼叫生成函式一次，將完整命令陣列序列化至 stdout 後立即 return，務必在任何 `subprocess.call()` 之前。正常執行分支仍使用同一生成結果；不要複製 roots、群組或掃描規則。這是來源支持的設計推論，尚非現有能力。
- 生成函式仍會查詢 Git 以取得排除項（L123），故「不執行測試」不等於「完全不啟動子程序」。這不違反已給條件，但新模式須保留此區別，不能宣稱完全無子程序。禁止重複 discovery 應由只呼叫既有生成函式一次落實，不能額外預掃或重建其邏輯。

## Evidence

以下皆為來源閱讀，沒有執行結果或測試通過聲稱：

- [runner 入口與命令生成](../../../src/scripts/run_package_tests.py)：L68–113 是既有 discovery；L116–150 是生成函式；L139–145 是 Mermaid 命令；L153–180 是 CLI 與執行入口。通讀全檔確認目前無 JSON／dry-run 分支。
- [Git 排除項查詢](../../../src/loom-code/scripts/repo_files.py)：L73–94、L97–120、L123–146 分別處理 worktree、巢狀 repo 與 Git 檔案查詢。
- [Git subprocess 包裝](../../../src/loom-code/scripts/git_exec.py)：L50–88 使用 capture_output 的 Git 呼叫及失敗回傳，支持生成階段會啟動 Git 而非 suite 的區別。

## Decision impact

排除直接執行原命令及要求非 Python 呼叫者 import 這兩案。建議在原入口加入單一列印模式（例如 `--list-commands-json`，名稱尚未決定），共用既有驗證與 discovery，輸出 JSON 後退出。相比另建包裝腳本，此方案少一個入口與參數同步責任；相比硬寫 Mermaid 三條命令，避免複製 inventory 與未來漂移。代價是增加一個需維護的 CLI 選項及 JSON 輸出契約；必要驗證包括 JSON 可解析、與同條件生成結果一致、生成只呼叫一次，以及列印路徑絕不進入 suite 執行。上述是後續實作驗證需求，本次沒有執行。

## Limitations and open questions

來源快照未附版本識別；未驗證任何實際 JSON 輸出、Git 環境或新選項，亦未實作方案。若呼叫端連啟動 Python 解譯器或 Git 都不允許，這會是新增限制，需重新評估；目前僅要求呼叫端不能 import Python。記錄與本次結論僅適用於所讀來源。
