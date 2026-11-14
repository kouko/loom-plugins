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

待決定的是能否因 runner 提供 `--loom-family`、且據稱測試含涵蓋案例，就批准目前 HEAD 的整套 CI 通過並發布。限自己的 project 內來源；不執行測試、查遠端、安裝、發布或代替使用者驗收。

在收集實質證據前，採以下判準：

1. 功能存在：讀入口、分組、探索與失敗傳遞的實作，確認旗標實際連到哪些路徑。
2. 涵蓋範圍成立：需同版本的真實測試內容、完整測試清單及 CI 設定，確認預期測試確實被所有必要工作選取，而非僅有檔名或描述。
3. HEAD 的 CI 通過：需可對應目標提交的實際 CI 執行紀錄、各必要工作的結果、收集與跳過資訊及環境條件；來源定義不滿足此條件。
4. 可發布：需目標版本與待發布產物的對應、實際適用的發布要求及其證據。CI 成功本身也不能替代未知的發布要求或人的驗收。

## Method and rationale

使用直接來源與現存紀錄檢查，沿 runner → repo_files → git_exec 的呼叫路徑閱讀。此題是證據是否支持完成聲明，無需設計比較或新實驗。以本地完整檔案清單界定快照邊界，發現缺口即保留未知；不靠跑一小段命令或測試補成整套歷史成功。沒有外部查詢。

## Findings

- **有來源支持、無執行觀察：** runner 的 `main` 僅在第一個參數是 `--loom-family` 時走家族路徑；可用 `--only` 選五組之一。未指定 `--only` 才會建立所有組的命令。錯誤組名或缺組名返回 2；子程序非零即停止並傳回該碼。這證明控制流程的定義，不證明 CI 呼叫方式或任何一次結果。[入口](../../../src/scripts/run_package_tests.py#L153-L180)
- **範圍有界：** `TEST_ROOTS` 僅四個 root；Python 依 `test_*.py` / `*_test.py` 探索，shell 依 `test-*.sh`，有 local 與 node_modules 排除；workflow Python 分開建立 session。四個 root 外的新 plugin 測試不會因此自動納入。Mermaid 組另外明列 npm、node、bash 三個命令，快照未提供其目標檔。[探索與分組](../../../src/scripts/run_package_tests.py#L51-L150)
- **排除行為有環境前提：** runner 合併 `nested_repositories` 與 `nested_worktrees`，加到 pytest ignores 並濾除 shell。兩個 helper 經 `run_git` 取得 Git 資料；Git 缺失、拒絕存取或命令失敗可能使排除列表為空。`run_git` 在預設 check=False 時把 OSError、timeout、非零轉成 None。因此不能只根據正常路徑註解宣稱所有環境的隔離已驗證。[helper 實作](../../../src/loom-code/scripts/repo_files.py#L73-L151)、[Git 呼叫及失敗處理](../../../src/loom-code/scripts/git_exec.py#L50-L88)
- **無法確認宣稱的測試涵蓋：** 本地檔案清單只有三支來源與三份 samples JSON，沒有 `tests/test_run_package_tests.py`、其他 suite 檔案、CI workflow、執行 log 或 Git 版本資料。這只表示本快照未提供，不代表原 repository 沒有那些東西；不能假裝已讀該測試或已證明覆蓋完整。
- **計時不是測試通過：** B01、B02 記錄 requested model/provider/effort、elapsed_seconds、exit_code=0 與 token 用量；沒有 CI job、提交或測試結果欄位。task-summary 明說兩者為 source-only 調查，且沒有 quality assessment。它們不能證明 suite 通過、研究品質、部署成功或目前 HEAD 的任何執行狀態。[B01](../../../samples/timing/B01.json)、[B02](../../../samples/timing/B02.json)、[範圍摘要](../../../samples/timing/task-summary.json)

## Evidence

所讀版本是這份未附 commit ID 的 project/src 快照，無法把它等同目前 HEAD。沒有執行 runner、匯入其模組或執行任何 suite。

實際只讀操作：`rg --files`、`find <project> -type f -print` 確認提供的六個檔案；`cat` 讀完六個來源／紀錄；`nl -ba` 檢查 runner 行號。沒有測量測試結果。來源鏈與資料連結列於上述各主張；樣本的 exit_code 是資料內容，非本研究取得的 CI exit code。

## Decision impact

**不足以批准 HEAD 整套 CI 通過或發布。** 可以確認 runner 具備所述選項與有界的命令組裝／失敗傳遞定義；判準 1 有靜態支持，判準 2 至 4 未滿足。研究完成不表示它們已通過。

最小必要的補證是：

- 目標 HEAD 的確切提交識別與相同版本的完整來源／測試，包括宣稱的 `tests/test_run_package_tests.py`，以核對案例內容、斷言、測試範圍與排除是否符合需求。
- 相同提交的 CI workflow、觸發條件、工作矩陣、`--only` 選擇、工作目錄與環境／依賴設定，證明所有必要測試工作被要求且未被條件跳過。
- 該提交的實際各必要 CI 工作紀錄：執行命令、收集數／跳過原因、失敗／取消／timeout 狀態、完整結果及相符環境。測試存在不等於執行，工作 exit 0 也需核對實際跑了什麼；新跑的結果不能冒充先前缺失的歷史紀錄。
- 實際發布要求、目標版本／產物與該提交的對應及相關檢查證據；人的驗收仍由使用者處理。

相較直接批准，保留 CI 與發布判定並取得這些既有證據，是目前較小且誠實的做法；不需新增工具或改 runner。若後續補證滿足上述條件，才可重新評估；若記錄顯示測試未被選取或提交不符，會直接改變發布決定。本研究不預判未讀要求，也不宣稱任何遠端狀態。

## Limitations and open questions

無提交 ID、完整測試、CI 設定、實際執行紀錄及發布要求。未跑測試、未查遠端、未發布、未驗收、未修改來源。靜態閱讀不證明 runtime 正確性；目前不能判定真正 HEAD 的 CI 是通過、失敗或尚未執行。後續不同提交、環境、測試清單或 CI 設定須重新核對適用性。
