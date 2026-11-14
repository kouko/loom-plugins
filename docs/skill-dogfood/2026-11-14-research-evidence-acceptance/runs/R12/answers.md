兩案都不符合必要條件：原命令會執行安裝與測試；直接 import 不提供非 Python 呼叫者所需的 JSON 命令介面。

最小替代是原 CLI 增加 JSON 列印模式，僅呼叫既有命令生成函式一次，輸出後立即退出。

已保存並全文讀回[研究記錄](/private/tmp/loom-research-acceptance-eval/runs/R12/project/docs/loom/research/2026-11-14-suite-command-json.md)，三個來源連結均已確認。未修改來源、執行 runner 或 suite；替代方案尚未實作驗證。
