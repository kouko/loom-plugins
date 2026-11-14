---
title: "獨立程序的 package suite JSON 預覽"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# 獨立程序的 package suite JSON 預覽

## Question and scope

呼叫端現改為不能 import Python，只能執行命令並讀取 stdout 的 JSON 命令陣列。預覽仍不能啟動 suite，不能新增另一套 discovery，且本次不得實作或新增實驗。這是使先前推薦不適用的實質條件變更；[原研究](2026-11-14-package-suite-preview.md)保留原條件、來源與唯一實驗，不覆寫其歷史結論。

充分條件：確認現有 CLI 是否可輸出 JSON 而不執行命令，及最小新增是否能共用原建構邊界。只有來源層次評估，新增 CLI 的實際輸出與不執行保證尚未經實作驗證。

## Method and rationale

沿用並重新檢視已讀取的來源快照，特別是 runner 第 116–180 行。比較同樣的 JSON 介面、不執行 suite、共用 discovery 三項硬條件，選擇最小改動；無外部資料與新實驗。版本或 commit 未提供。

## Findings

- 現有 CLI 不符合新條件：main 的 loom-family 分支逐筆 subprocess.call 建構結果，沒有 JSON 輸出或預覽分支；直接執行現有 suite 命令會啟動測試。
- 現有 loom_family_commands 仍是可重用的內部邊界，回傳 list[list[str]]，能直接序列化為 JSON 命令陣列；它本身不執行回傳的 pytest、npm、node、bash 命令。
- 因呼叫端限制變更，撤回「呼叫端直接 import」作為當前方案；來源能力判斷不變。原空目錄實驗只證明函式建構，不能證明尚未存在的 JSON CLI。

## Evidence

- [runner](../../../src/scripts/run_package_tests.py)：116–150 行建立並回傳命令；153–167 行處理群組、立即執行及首錯停止；179–180 行腳本入口。這些是來源觀察，非新 CLI 執行結果。
- [repo_files](../../../src/loom-code/scripts/repo_files.py) 與 [git_exec](../../../src/loom-code/scripts/git_exec.py)：建構期間仍有唯讀 Git 子程序，不能描述為完全不建立子程序。
- [原研究的實驗與限制](2026-11-14-package-suite-preview.md)：唯一已執行的小實驗回傳三筆 workflow-mermaid 命令；沒有執行它們，沒有 JSON CLI 驗證。

## Decision impact

推薦在現有 runner 新增薄的 JSON 預覽分支，例如設計為 `--loom-family --preview-json [--only GROUP]`；名稱只是提案，現在並不存在。重用原群組驗證與 loom_family_commands，僅以標準 JSON 編碼輸出回傳清單，隨即成功返回，絕不進入 subprocess.call 迴圈。stdout 僅有一個 JSON 陣列，不混入進度文字；無效參數或建構錯誤使用非零退出碼及 stderr，不能用空成功陣列掩蓋錯誤。不要從既有執行輸出反推命令。

為保持頂層就是 JSON 命令陣列，不另包工作目錄欄位；呼叫端以約定的 suite repository root 作為程序工作目錄，與現有 main 的 Path.cwd() 一致。命令陣列中的相對路徑依此解讀。verbosity 及 only 沿用相同語意。

可信替代是獨立小型 Python wrapper，由程序內部 import 原函式並輸出 JSON；呼叫端本身仍無須 import，也能共用 discovery。但目前沒有禁止修改 runner 的需求，新增 wrapper 會多出入口與相依載入維護面，所以優先既有 runner 的薄分支。若另有不能改 runner 的部署限制，可轉選 wrapper，無須全面重寫。完整重寫若保留建構函式沒有額外必要收益；若重做 discovery 則違反硬條件。

## Limitations and open questions

本次沒有實作、suite 執行或新實驗；JSON 格式、stdout 純淨度、預覽分支不進入執行迴圈及錯誤路徑仍須未來實作後驗證，不能宣稱已可用。唯讀 Git 查詢仍存在且其失敗可能被 helper 轉成空排除清單；薄預覽不新增整體可執行性保證。預覽仍受當下檔案與 Git 狀態影響，不能保證後續全部命令實際執行或成功。
