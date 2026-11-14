兩案原樣都不滿足條件：

- 直接 runner：L139–145 建構 npm/node/bash 命令，L163–164 實際執行，沒有 JSON-only 模式。
- 只 import：回傳 Python list，尚未提供外部程序所需的 JSON 命令介面。
- 最小替代：新增 JSON-only CLI 分支，呼叫既有 `loom_family_commands` 一次，序列化後立即返回；不複製 discovery。

已保存並完整讀回：[研究記錄](/private/tmp/loom-research-acceptance-eval/runs/R06/project/docs/loom/research/2026-11-14-suite-json-command-interface.md)。三個相對來源連結均已解析確認。

實際證據：只讀 runner、repo_files、git_exec 的相關控制流程；未執行 runner、main、suite、import 或安裝。結論為靜態來源判讀；替代介面尚未實作或測試，未聲稱取得實際 JSON。
