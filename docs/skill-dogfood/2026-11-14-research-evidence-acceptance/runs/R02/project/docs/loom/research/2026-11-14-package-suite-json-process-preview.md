---
title: "獨立程序如何取得 package suite JSON 命令預覽"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# 獨立程序如何取得 package suite JSON 命令預覽

## Question and scope

呼叫端已確定不能 import Python，只能執行命令並讀取 stdout 的 JSON 命令陣列。預覽絕對不能執行 suite，也不能另寫 discovery（找出要跑哪些測試的規則）。僅研究提供的 src 快照；沒有提供 commit 或 release。只更新研究，不實作、不再執行實驗。這是[原研究](2026-11-14-package-suite-command-preview.md)的條件變更再驗證；保留先前結論所依賴的舊條件與證據。

## Method and rationale

本輪重新閱讀真實 runner 116–180 行，確認命令建構與 CLI 執行路徑。沿用先前已讀取的 helper 與唯一允許實驗，僅用於仍適用的命令建構能力；不把該實驗視為新增 CLI 已可用。比較能否供獨立程序呼叫、stdout JSON、零 suite 執行、共用探索規則與變更範圍。來源足以辨認缺少的介面，無需再跑 main 或 suite。

## Findings

- **來源支持：現有 CLI 不直接滿足。** [runner](../../../src/scripts/run_package_tests.py) 153–167 行的 `--loom-family` 分支驗證 group 後，逐一用 `subprocess.call` 執行命令；168–175 行一般分支也執行 pytest。沒有 JSON 預覽分支。不能把未支援的預覽參數傳入後假設安全；尤其第一個參數不是 `--loom-family` 時會走一般 pytest 分支。
- **來源支持：命令建構能力仍可沿用。** 同一來源 116–150 行的 `loom_family_commands` 回傳 `list[list[str]]`，沒有執行回傳的測試命令；GROUPS 驗證位於 main，函式不自行驗證。新程序入口可以內部呼叫此函式；「呼叫端不能 import」不等於入口程序內部不能使用 Python。
- **先前實際觀察，適用範圍有限：** [先前 scratch 腳本](../../../scratch/preview_commands.py) import 真實模組，對暫時空目錄指定 workflow-mermaid，成功印出 npm、node、bash 三組參數列 JSON，exit code 0。[原始輸出](../../../scratch/preview_commands.stdout.txt)已讀過。本輪未重跑；這證明該組的建構與序列化可行，不證明新 CLI 已存在或完整探索正確。
- **來源支持的限制：** 函式 123 行仍查 Git，沿用 [repo_files.py](../../../src/loom-code/scripts/repo_files.py) 與 [git_exec.py](../../../src/loom-code/scripts/git_exec.py) 的子程序；它不會因為輸出 JSON 就成為無任何子程序的操作。這不違反不執行 suite 的既有條件。

## Evidence

本輪工具實際讀取 runner 116–180 行及原研究全文。沒有修改來源，沒有新增執行結果；唯一實驗命令、輸出與條件均保留於原研究。下列方案是依已檢查來源提出的設計推論，尚未實作或執行驗證。

## Decision impact

**目前推薦改為：在現有 runner 的 `--loom-family` 路徑增加小型 JSON 預覽分支，保留同一個命令建構函式；不重寫 runner。** 先前「呼叫端直接 import」推薦因真實條件改變而不再適用，並非建構能力的證據失效。

建議介面形狀例如 `python3 scripts/run_package_tests.py --loom-family --preview-json [--only <group>]`；此命令僅為提案，現有程式不支援，現在不能執行以取得安全預覽。

最小流程為：明確解析預覽旗標及沿用 GROUPS 驗證 → 呼叫一次 `loom_family_commands(Path.cwd(), verbosity, only)` → 將完整 `list[list[str]]` 序列化為單一 JSON 值寫入 stdout → 成功退出。預覽分支必須在任何 `subprocess.call` 前返回，且沒有 fall-through；驗證失敗走 stderr 及非零 exit，不執行 suite，stdout 不混入人類說明或測試輸出。參數列保留為字串陣列，無需自行拼接 shell 指令。

相較之下，獨立 Python 包裝命令也可以在內部 import 同一函式、輸出 JSON 而不複製探索；它可保持 runner 原檔不變，但增加入口檔與跨檔 import/部署定位。提供來源已將建構與執行放在同一 runner，沒有要求 runner 不得修改，因此優先在原入口加分支，避免額外封裝。若日後確定 runner 不能改，包裝命令才是合理替代。

完整重寫也能設計成單一探索規則，但對此新增介面沒有必要收益，反而擴大分組、排除、順序與失敗傳播的相容性重驗範圍。現有執行路徑維持不變又不補介面，則不符合獨立程序的純 JSON 預覽需求。

## Limitations and open questions

- 沒有實作任何旗標或入口，尚未驗證 JSON stdout 純淨度、錯誤輸入退出、預覽分支無落入執行，以及既有執行模式相容性；以上是未來實作需驗證的具體行為，不是已通過的檢查。
- 沒有執行 suite 或 runner main，亦沒有追加實驗。既有實驗只涵蓋空目錄 Mermaid 組別。
- 呼叫端應以目標 repo 為工作目錄；JSON 依要求只含命令陣列，工作目錄須由呼叫約定保留，不能從陣列推知。回傳仍不保證工具可用、檔案存在或之後探索結果相同。
- Python 程序仍需可啟動；使用者限制是呼叫端不能 import，沒有宣告環境不可執行 Python。若連 Python runtime 也不可用，這項方案須重新評估，不能自行假設。
