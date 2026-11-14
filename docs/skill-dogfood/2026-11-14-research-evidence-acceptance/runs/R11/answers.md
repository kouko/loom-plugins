最小方案是直接呼叫既有 `loom_family_commands(repo, only="workflow-mermaid")`，取得命令陣列供預覽；目前需求不需要 HTTP 服務、常駐索引或另一份發現設定。

已保存並完整讀回[研究記錄](/private/tmp/loom-research-acceptance-eval/runs/R11/project/docs/loom/research/2026-11-14-workflow-mermaid-preview.md)，確認三個來源連結正確。

限制：函式仍會進行唯讀 Git 查詢，載入模組會修改 `sys.path`；本次只有來源檢查，未執行函式、suite、安裝或服務。
