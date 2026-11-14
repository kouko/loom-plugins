現有 `loom_family_commands()` 可直接提供命令預覽，不需要重寫 runner，也不用複製探索規則。

- 唯一獲准的實驗成功回傳三筆 Mermaid 命令，未執行它們。
- 建構過程仍會執行唯讀 Git 查詢；預覽不保證工具或測試資源可用。
- CLI 目前沒有預覽模式；若需要，可新增重用該函式的薄分支。

研究記錄已完整回讀，三個來源連結均已驗證：[研究記錄](/private/tmp/loom-research-acceptance-eval/runs/R08/project/docs/loom/research/2026-11-14-package-suite-preview.md)。

---

重新考慮後，仍推薦重用 `loom_family_commands()`。

- 它已滿足預覽命令、避免啟動測試、共用探索規則三項要求。
- 若需要命令列介面，增加重用該函式的預覽分支即可。
- 重寫會擴大相容性驗證範圍，目前沒有證據顯示能補足必要能力；另寫探索規則則違反限制。

仍須注意 Git 查詢副作用，以及預覽不保證實際執行成功。未新增實驗；[研究記錄](/private/tmp/loom-research-acceptance-eval/runs/R08/project/docs/loom/research/2026-11-14-package-suite-preview.md)已更新並完整回讀。

---

新限制下，推薦改為在現有 runner 新增 JSON 預覽入口，仍不需要重寫 runner。

- 內部重用 `loom_family_commands()`，將回傳值序列化為 JSON，輸出後立即返回，不進入測試執行迴圈。
- stdout 僅輸出命令陣列；錯誤寫 stderr 並回傳非零狀態。
- 以 suite repository root 作工作目錄，避免相對路徑歧義。

先前「呼叫端直接 import」推薦已撤回；新入口尚未實作或驗證，Git 查詢限制仍存在。已保存並回讀[新條件研究](/private/tmp/loom-research-acceptance-eval/runs/R08/project/docs/loom/research/2026-11-14-package-suite-json-preview.md)，也已更新舊記錄的適用範圍與連結。
