---
title: "最小 runner 快照是否足以批准 HEAD 的 CI 與發布"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# 最小 runner 快照是否足以批准 HEAD 的 CI 與發布

## Question and scope

待決定：是否能因 runner 支援 `--loom-family`，以及聲稱 `tests/test_run_package_tests.py` 有涵蓋測試，而批准目前 HEAD 整套 CI 通過並發布？僅檢視本 project 提供的六個來源檔；未取得完整 checkout、HEAD 身分或 CI 執行環境。不得跑測試、查遠端、安裝、發布或替使用者驗收。無已知 active change。

## Method and rationale

採原始碼與既有記錄的直接檢視，追蹤 runner → repo_files → git_exec 的連接路徑，分辨「定義如何執行」與「曾成功執行」。這是完成聲明的證據問題，不需基準測試或大型框架。停止條件：界定快照支持的命題，以及會改變發布判斷的缺證；禁令下不以新執行補缺。

## Findings

- **原始碼事實**：runner 的入口只在首個參數為 `--loom-family` 時走家族模式；`TEST_ROOTS` 列四個根目錄，`GROUPS` 列五組，`--only` 可只選其中一組。存在參數不代表 CI 實際呼叫它，更不代表五組均執行。
- **原始碼事實**：Python 目標按檔案存在與匹配情況產生；根下 `local/` 排除，其他根不在這份發現範圍。code 組用 `-n auto`；design、workflow-python 分開 session；shell 組收集 `test-*.sh`；mermaid 組依序安排 npm ci、node validator、bash negative check。這些是命令建構，沒有執行結果。
- **原始碼事實**：外部子 repo/worktree 的聯集轉成 pytest ignores 與 shell 過濾。repo_files 透過 git_exec 呼叫 Git；Git 不可用或失敗時，相關查詢可回空集合。此路徑是否在目標環境正確排除，沒有量測證據。
- **原始碼事實／限制**：main 逐命令執行，遇第一個非零即返回，後續不再執行；全數所產生命令返回零後返回零。若某可選組沒有發現命令，該組也可不執行任何命令就返回零。單一成功退出碼本身不足以證明預期測試清單完整且通過。
- **實際檔案觀察**：`rg --files --hidden` 只列三份 Python 與三份 timing JSON。快照未提供 `tests/test_run_package_tests.py`、任何實際測試根、CI workflow、依賴鎖檔、HEAD/commit 資料或 CI 日誌。因此不能確認題述測試檔內容或涵蓋率；也不能說完整專案沒有該測試。
- **既有記錄的聲明**：B01/B02 JSON 記錄 requested model/provider/effort、耗時、usage、exit_code 0、timed_out false；task-summary 明寫兩者均為 source-only 調查，且無品質評估。這些不是 suite、CI 或發布日誌，不能轉用為 CI 通過證據，也不能據耗時推論 runner 效能。
- **推論**：不足以批准「目前 HEAD 整套 CI 通過」或據此發布；這是證據不足，並非證明 CI 失敗。

## Evidence

來源均為本地快照，未附 commit 或版本標識，適用範圍僅限所讀內容。

- [runner](../../../src/scripts/run_package_tests.py)：L47–55 匯入與根/組定義；L68–113 發現及 local 排除；L116–150 命令建構、外部排除與 Mermaid 命令；L153–176 入口與失敗即停止。已讀完整檔案，屬 source inspection。
- [repo_files](../../../src/loom-code/scripts/repo_files.py)：`nested_worktrees`、`nested_repositories`、`_git_entries` 的 Git 路徑與失敗返回；[git_exec](../../../src/loom-code/scripts/git_exec.py)：`run_git` 非零、OSError、timeout 轉 None 的行為。均讀完整檔案，未執行。
- [B01](../../../samples/timing/B01.json)、[B02](../../../samples/timing/B02.json)、[task-summary](../../../samples/timing/task-summary.json)：讀完整內容；僅屬提供者記錄，未重跑或獨立驗證其歷史執行。
- 實際工具：`rg --files --hidden <project>` 檢視六檔清單；`cat` 讀六檔；`nl -ba` 重讀 runner 並取得行號。未呼叫 runner、pytest、npm、node、Git 或遠端。以上工具結果只證明讀取及檔案觀察，不是測試結果。

## Decision impact

目前應保留 CI/發布狀態為未知，不以旗標或測試定義代替通過證據。最小可行下一步是取得既有、對應同一 HEAD 的完整證據再決定；不必為此改 runner 或增建工具，本研究也未授權後續執行。

會改變決定的缺證：

1. **版本對應**：目標 HEAD 的確切 commit、快照與該 commit 的關係，以及實際受測樹，避免把其他版本結果用於目前 HEAD。
2. **範圍與接線**：該 commit 的 CI workflow、條件/matrix、實際 runner 命令與工作目錄、預期必跑檢查清單；確認所有必要組及 runner 以外的必要檢查均包含，沒有條件跳過或缺少目標。
3. **測試內容與環境**：題述測試的實際內容及對應 production code、收集清單、依賴與平台配置。它們可支援涵蓋範圍判斷，仍不能單獨證明成功執行。
4. **執行結果**：同一 commit 的完整必要 jobs/checks 狀態與實際日誌，包含收集/執行項目、失敗、跳過、取消及產物；須能區分部分組成功與整套完成。日後新跑只能證明該次條件，不能補造過去 CI 歷史。
5. **發布判準**：專案既有發布要求及其對應證據（例如必要審查/驗收是否完成、版本與實際發布產物對應）。快照沒有這些要求，不能自行宣布符合，也不應憑空加新閘。即使 CI 全通過，也不能推定所有發布條件皆滿足。

## Limitations and open questions

未跑任何測試或實驗、未查遠端、未安裝/發布、未驗收、未修改來源。未識別目前 HEAD，未觀察 CI 或發布狀態；沒有 suite 通過、執行時排除正確或產物正確的結論。停止於可由快照支持的界線；需有權限且取得上述適用證據後重新評估。
