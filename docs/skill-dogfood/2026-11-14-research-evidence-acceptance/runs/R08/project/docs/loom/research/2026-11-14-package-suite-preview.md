---
title: "Package suite 命令預覽"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# Package suite 命令預覽

## Question and scope

此記錄保留原先允許 Python import 的條件與決策；呼叫端改為獨立程序後，最新適用推薦見 [JSON 預覽重驗](2026-11-14-package-suite-json-preview.md)。原本的直接 import 推薦不適用新呼叫端，不能當成目前交付方案。

呼叫端是否能取得 suite 命令而不啟動 pytest、npm 或 shell tests，且共用既有探索規則？充分條件是追蹤建構與執行邊界及其相依呼叫，並以唯一獲准的空目錄 workflow-mermaid 實驗觀察回傳值。只適用提供的來源快照，未提供 commit 或版本。

## Method and rationale

完整讀取 runner 與兩個相依模組，搭配單次可行性實驗；以不執行測試、共用規則、改動最小為比較標準。不需外部資料或完整 suite。

## Findings

- 來源支持直接沿用 `loom_family_commands(repo, verbosity="-q", only=None)`；它回傳命令參數清單，沒有執行 pytest、npm、node 或 bash。探索與排除規則仍由原實作負責，不需重寫 runner。
- `main()` 才以 `subprocess.call` 執行回傳命令，現有 CLI 沒有預覽模式。一般 import 不會觸發 main。
- 建構函式仍透過 helpers 執行唯讀 Git 查詢；import 也會修改 sys.path。因此它不是完全無子程序或副作用的純函式。
- 實驗成功回傳三筆命令。空目錄也會列出 Mermaid 命令，因此列出不代表工具、測試資源存在或指令可執行。
- 直接呼叫時不驗證 `only`；未知群組會得到空清單，合法性檢查只在 main。

## Evidence

已完整讀取的來源：

- [runner](../../../src/scripts/run_package_tests.py)：47–49 行載入 helpers；68–113 行探索與分組；116–150 行建構命令；153–180 行驗證參數與執行。
- [repo_files](../../../src/loom-code/scripts/repo_files.py)：nested_repositories 經 _git_entries 查詢 rev-parse、ls-files；nested_worktrees 查詢 worktree list。部分 Git 失敗情況回傳空清單，不能解讀為已證明沒有巢狀 repository。
- [git_exec](../../../src/loom-code/scripts/git_exec.py)：run_git 使用 subprocess.run 執行 Git，預設失敗回傳 None，預設沒有 timeout。

單次實驗命令為 `PYTHONDONTWRITEBYTECODE=1 python3 -B -`，stdin scratch 程式如下；避免 src bytecode，暫時空目錄限 research 內並於結束清除：

```python
import importlib.util
import tempfile
from pathlib import Path
root = Path('/private/tmp/loom-research-acceptance-eval/runs/R08/project')
spec = importlib.util.spec_from_file_location('package_preview_probe', root / 'src/scripts/run_package_tests.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with tempfile.TemporaryDirectory(dir=root / 'docs/loom/research') as empty:
    print(module.loom_family_commands(Path(empty), only='workflow-mermaid'))
```

實際 stdout（exit 0）：

```text
[['npm', 'ci', '--prefix', 'loom-workflow/tests/mermaid'], ['node', 'loom-workflow/tests/mermaid/validate_mermaid.mjs'], ['bash', 'loom-workflow/tests/mermaid-validator-negative.sh']]
```

程式未呼叫 main，也未執行回傳命令；這是限定輸入的建構觀察，不是 suite 成功證據。

## Decision impact

最小選擇是 Python 呼叫端 import 現有模組，傳入實際 repository root，直接取得並呈現命令清單，不執行清單。需要群組驗證時重用既有 GROUPS，不新增另一套探索規則。root、verbosity、only 必須與預定執行一致。回傳值未包含工作目錄，且多數命令使用相對路徑，介面應一併顯示 root。

若呼叫端只能使用 CLI，最小新增是重用同一函式與既有驗證的薄預覽分支；目前沒有實作或測試該介面。重寫 runner 沒有必要性證據；另寫 discovery 違反硬性條件並增加規則漂移。若需求升級為禁止所有子程序，現有 Git 查詢路徑不滿足，須另評估邊界，不能直接宣稱可用。

### 同日追問再評估

使用者提出「直接重寫 runner 比較完整」，明確沒有新增需求或證據，原限制不變。重新讀取本記錄及 runner 第 116–180 行後，維持原推薦；沒有新增實驗，也沒有改變充分證據條件。「完整」尚未指出既有命令建構函式欠缺哪個必要行為。

直接重用已滿足 Python 呼叫端預覽及共用探索規則；薄 CLI 分支可處理僅 CLI 的介面需求。全面重寫若保留同一探索函式，仍需額外承擔參數驗證、執行順序與首錯停止行為的相容性驗證，卻未帶來目前需求所需的新能力；若另建探索規則則直接違反限制。這些是由現有邊界推導的改動負擔，不是已測量的重寫缺陷。未提供替代實作，不能宣稱重寫必定失敗或作量化品質比較。唯有確認現有邊界無法滿足的必要行為，才有重新考慮較大改造的理由。

## Limitations and open questions

未執行 suite、pytest、npm、node 或 shell tests；未驗證工具安裝、完整測試探索或實際 suite 成功。僅實測空目錄 workflow-mermaid，其他群組與巢狀 repository 處理只有來源支持。預覽是當時快照，檔案、Git 狀態、Python interpreter 或參數改變時可能不同；實際 runner 首次失敗即停止，不能保證列出的命令全部執行。來源變更需重驗。未修改來源、連網、安裝或發布。
