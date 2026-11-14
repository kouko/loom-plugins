不需要重寫 runner：Python 呼叫端可直接呼叫 `loom_family_commands()` 取得命令清單，沿用現有探索規則，不會執行回傳命令。

- 實測成功：import 真實模組，對暫時空目錄指定 `workflow-mermaid`，回傳 npm、node、bash 三個命令，exit code 0。
- 限制：建構期間仍會執行 Git 查詢；命令回傳不代表工具與檔案可用。只實測指定組別，未執行 suite 或 main。
- 若呼叫端只能使用 CLI，最小變更是增加呼叫同一函式的預覽入口；現有 CLI 會實際執行命令。

已完整讀回研究記錄並確認全部本地連結：
[研究記錄](/private/tmp/loom-research-acceptance-eval/runs/R02/project/docs/loom/research/2026-11-14-package-suite-command-preview.md)

實驗保存於：
[腳本](/private/tmp/loom-research-acceptance-eval/runs/R02/project/scratch/preview_commands.py)、[實際輸出](/private/tmp/loom-research-acceptance-eval/runs/R02/project/scratch/preview_commands.stdout.txt)。

---

重新比較後，仍推薦沿用 `loom_family_commands()`；目前的預覽需求不足以支持重寫。

- 現有函式已把命令建構與執行分開，先前實驗確認能只取得命令。
- 完整替換 runner 不一定造成重複規則，但會擴大需要重新驗證的範圍，包括分組、排除規則、命令順序與失敗處理，尚無必要收益支持。
- 若只能透過 CLI 呼叫，增加共用現有函式的預覽入口即可。

已更新並完整讀回[原研究記錄](/private/tmp/loom-research-acceptance-eval/runs/R02/project/docs/loom/research/2026-11-14-package-suite-command-preview.md)，確認本地連結。此次沒有新增實驗或修改來源；完整 suite 與實際呼叫端整合仍未驗證。

---

推薦改為在現有 runner 增加 JSON 預覽分支，仍共用 `loom_family_commands()`，不必重寫 runner。

- 現有 CLI 會執行命令，不能直接滿足新需求；先前「呼叫端直接 import」已不適用。
- 預覽分支應驗證參數、取得命令陣列、只將 JSON 寫入 stdout，並在任何 suite 執行前返回；錯誤走 stderr 與非零退出碼。
- 此為尚未實作的方案，沒有新增實驗或執行 suite；建構期間仍可能執行 Git 查詢。

已保留舊證據、標記原記錄被新條件取代，並完整讀回兩份記錄、確認連結：

[新條件研究記錄](/private/tmp/loom-research-acceptance-eval/runs/R02/project/docs/loom/research/2026-11-14-package-suite-json-process-preview.md)
[原研究記錄](/private/tmp/loom-research-acceptance-eval/runs/R02/project/docs/loom/research/2026-11-14-package-suite-command-preview.md)
