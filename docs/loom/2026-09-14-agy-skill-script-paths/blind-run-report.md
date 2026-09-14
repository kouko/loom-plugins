# loom-workflow 在每個宿主都找得到自己的腳本，視覺化提醒卡也送到 agy 與 Codex — 我試了什麼、發生了什麼

試跑日期 2026-09-14，用的是專案的乾淨複本，版本 6603aca8（從本機這份工作目錄重新 clone 出來，代替從 GitHub 取得；clone 後確認沒有任何未提交的改動）。試跑後分支前進到 41796371，多了三個 commit：新增對抗測試（b51d0f14）、檢查與同步腳本的健壯性修正和測試說明補充（e4a615ed）、說明書加上 agy 同名匯入的警告（41796371）。這三個 commit 沒有改到我試跑時用到的技能說明；視覺化技能資料夾裡只有兩支推理頁腳本各改了幾行，不是這次用到的腳本。第 1 條中 agy 做表那一格，我在 41796371 用乾淨複本重跑過；其餘各條的結果仍是 6603aca8 上的。

使用的宿主版本：Claude Code 2.1.270、Antigravity CLI（agy）1.2.2、Codex 0.154.0。

## 你要的東西，一條一條試

### 1. On Claude Code and on agy, from a working directory outside the skill folder, loom-visualization runs its bundled scripts successfully when producing a diagram, and goal-create runs its bundled lint script.

- **我怎麼試**：開一個跟外掛完全無關的空專案資料夾，裡面只有一個說明檔和一份故意寫得不完整的目標檔。在這個資料夾裡分別對 Claude Code（只在這次啟動時載入複本裡的 loom-workflow）和 agy（先把複本的 loom-code、loom-workflow 裝進去）各下兩個請求：「用視覺化技能、透過它自帶的產生器，做一張兩個方案比速度與成本的小表」，以及「用 goal-create 對現有目標檔跑它自帶的檢查，不要改檔」。事後讀 agy 的對話紀錄，確認指令真的有執行、以及執行時所在的資料夾。
- **發生了什麼**：
  - Claude Code 做表：先跑了判斷顯示環境的腳本，得到 `target: coding-harness`，再用產生器做出表格，對齊檢查回報 `✓ no drift`、`exit=0`。三支腳本都是用技能資料夾的完整位置呼叫，執行所在地是那個無關的專案資料夾。
  - Claude Code 跑目標檢查：腳本正常執行，照實指出目標檔缺三個欄位（`ERROR [missing-field]: Missing or empty field: Outcome` 等），`exit=1`。這個 1 是檢查結果「目標檔不合格」，是預期中的，不是腳本找不到。
  - agy 做表（第一次，6603aca8）：同樣用完整位置呼叫產生器，輸出一張 29 字寬的方框表，對齊檢查 `✓ no drift`。但對話紀錄顯示，agy 自己把這三個指令的執行所在地設成了技能資料夾本身，不是專案資料夾。
  - agy 做表（重跑，41796371）：把複本更新到新版本並重新安裝，在新的空專案資料夾再問一次，並在請求裡明講「每個指令都要在這個專案資料夾裡執行，不要切到技能資料夾」。對話紀錄顯示三個指令（判斷顯示環境、產生器、對齊檢查）的執行所在地都是那個專案資料夾，產生器用完整位置找到並輸出同一張方框表。
  - agy 跑目標檢查：在專案資料夾內用完整位置呼叫檢查腳本，輸出和 Claude Code 完全相同的三行缺欄位錯誤。
- **證據**：
  - Claude 做表時實際下的指令：`printf '%s' '{"headers": ["Option", "Speed", "Cost"], ...}' | python3 $D/scripts/generate.py table`（`$D` 為技能資料夾完整位置），輸出 `│ Option A │ Fast  │ High │` 與 `✓ no drift`。
  - agy 目標檢查的紀錄：`cwd: .../userrepo-agy-goal | script: [.../loom-workflow/skills/goal-create/scripts/goal_lint.py]`。
  - agy 做表第一次的紀錄：`cwd: .../loom-workflow/skills/loom-visualization | script: [.../scripts/generate.py]`。
  - agy 做表重跑的紀錄（三個指令都一樣）：`run_command | cwd: .../userrepo-agy-viz2 | cmd: ... | python3 .../loom-workflow/skills/loom-visualization/scripts/generate.py table`，輸出 `│ Option A │ Fast  │ Costly │`，`exit=0`。
  - 暫存證據（次要）：`blindrun3/a1-claude-viz.jsonl`、`blindrun3/a1-claude-goal.jsonl`、`blindrun3/a1-agy-viz.txt`、`blindrun3/a1-agy-goal.txt`、`blindrun3/agy-transcripts-summary.txt`、`blindrun3/a1-agy-viz-cwds.txt`、`blindrun3/a1-agy-viz2.txt`、`blindrun3/a1-agy-viz2-cwds.txt`。
- **判定**：works — 兩個宿主、兩個技能都在專案資料夾執行時找到並跑成了自帶腳本，沒有任何一次找不到腳本。第一次試跑缺的那一格（agy 從技能資料夾以外做表）已在重跑中直接看到。（Claude Code 兩次與 agy 目標檢查為 6603aca8，agy 做表重跑為 41796371）

### 2. A skill instruction that contains a bare `python3 scripts/...` style command is rejected by the repository's contract lint, and the current loom-workflow skills pass it.

- **我怎麼試**：在複本裡，找一份目前沒有任何腳本指令的 loom-workflow 技能說明（recap-state），在最後加一段縮排程式碼 `python3 scripts/foo.py`，跑專案的契約檢查；接著把檔案還原成原樣（確認複本沒有殘留改動），再跑一次。
- **發生了什麼**：加了那行之後檢查擋下來，指出檔案與行號並要求改成從技能資料夾出發的寫法，結束碼 1。還原之後檢查通過，結束碼 0，只列出規則上線前就已登記、仍待清理的 4 個舊檔。
- **證據**：
  - 加入後：`BARE BUNDLED-SCRIPT PATH: loom-workflow/skills/recap-state/SKILL.md:146 runs scripts/ relative to the working directory; anchor it as <skill-dir>/scripts/` → `exit=1`
  - 還原後：`OK: 4 known-violating files unchanged, no new contract citations of this repo's records.` → `exit=0`
  - 暫存證據（次要）：`blindrun3/a2-lint-with-bare.txt`、`blindrun3/a2-lint-clean.txt`、`blindrun3/a2-git-status-after-revert.txt`（空白＝無殘留改動）。
- **判定**：works — 會擋、指得出位置，現有技能通過。（版本 6603aca8）

### 3. A new agy session and a new Codex session with loom-workflow installed each receive the loom-visualization trigger card text without the user asking for it.

- **我怎麼試**：
  - agy：延續第 1 條的安裝，在另一個空資料夾開全新對話，問「不要讀檔、不要執行指令，逐字引用你收到的任何視覺化提醒卡或規則的第一行；沒有就說 NONE」，接著用「延續上一個對話」再問同一題。事後查對話紀錄，確認兩輪都沒有讀檔或執行指令。
  - Codex：在暫存區做一個臨時外掛市集（名為 blindrun3），裡面放複本 loom-workflow 的乾淨匯出版本，加入市集並安裝，在空資料夾開一次性會話問同一題，並加問收到幾張。
- **發生了什麼**：
  - agy 第一輪與第二輪都回答了卡片內容，兩輪都沒有任何工具呼叫。但它先引用的「第一行」是一行產生檔註解，第二行才是卡片標題。
  - Codex 回答收到 1 張，標題逐字相符。你自己原本就在 Codex 裝了一份 loom-workflow（來自你的 loom 市集），但我查過那份沒有給 Codex 用的開場鉤子，所以這張卡只可能來自這次試跑的那份。
  - **重要**：Codex 預設不會執行外掛自帶的開場鉤子，要等使用者看過並「信任」一次之後才會跑。這次為了在不改你設定的情況下試跑，我加了「這一次略過信任檢查」的旗標，Codex 也照實警告 `--dangerously-bypass-hook-trust is enabled`。實際使用時，你需要在 Codex 裡對 loom-workflow 的鉤子按一次信任，卡片才會出現；在那之前 Codex 收不到卡。
- **證據**：
  - agy 第一輪：`<!-- Generated from skills/loom-visualization/assets/trigger-card.md by scripts/sync_codex_manifests.py; ... -->`，附註 `First markdown heading / content line: # Visualization trigger card (loom-workflow)`；第二輪同樣內容。
  - Codex：`"# Visualization trigger card (loom-workflow)" Separate visualization trigger cards received: 1.`
  - 暫存證據（次要）：`blindrun3/a3-agy-card.txt`、`blindrun3/agy-transcripts-summary.txt`（card 對話只有兩則使用者訊息、零工具呼叫）、`blindrun3/a3-codex-card.jsonl`、`blindrun3/codex-install.txt`。
- **判定**：works — 兩個宿主都在沒被要求時收到卡片。Codex 的前提是你信任過一次鉤子；agy 看到的卡片前面多了一行內部產生註解。（版本 6603aca8）

### 4. Claude Code sessions still receive the trigger card exactly once, and the existing package test suite passes.

- **我怎麼試**：在空資料夾用 Claude Code 只載入複本的 loom-workflow，問「不要讀檔、不要執行指令，開場收到幾張視覺化提醒卡，逐一引用第一行」；並直接數開場注入內容裡以 loom 卡片標題開頭的段數。接著在複本裡跑完整的套件測試與外掛清單同步檢查。
- **發生了什麼**：
  - 開場注入內容裡，loom 的視覺化卡片正好 1 段。模型回答「兩張」，但第二張是你另外裝的 ascii-graph-toolkit 自己的圖表卡，不是 loom 的。你在 Claude Code 使用者層級裝的舊版 loom-workflow（4.3.4）這次被複本那份取代，沒有另外再送一次。
  - 套件測試全數通過：pytest 共 2445 通過、11 略過、0 失敗；另有腳本式測試 145 項通過、0 失敗；整體結束碼 0。
  - 外掛清單同步檢查結束碼 0。
- **證據**：
  - 計數：`session-start contexts whose first line is loom's visualization card: 1` → `# Visualization trigger card (loom-workflow, ascii-graph-toolkit active)`
  - 模型回答：`Two cards: 1. # Visualization trigger card (loom-workflow, ascii-graph-toolkit active) 2. # Diagram trigger card (ascii-graph-toolkit)`
  - 測試：各段結尾如 `1336 passed, 2 skipped in 26.04s`、`Summary: 21 PASS / 0 FAIL`，最後 `exit=0`；同步檢查 `exit=0`。
  - 暫存證據（次要）：`blindrun3/a4-claude-card.jsonl`、`blindrun3/a4-claude-card-count.txt`、`blindrun3/a4-package-tests.txt`、`blindrun3/a4-sync-check.txt`。
- **判定**：works — Claude Code 仍只收到一張 loom 卡，測試全過。（版本 6603aca8）

## Review summary

審查站尚未把審查紀錄交給我，這份報告只根據我自己試跑的結果：四條都成立；第 1 條原本缺的「agy 從專案資料夾做表」已在 41796371 重跑補上。沒有看到任何失敗。

## Questions I asked you

- 這次要不要順便讓 Codex 也收到這張提醒卡？你的回答：agy 和 Codex 都做。
- 「你要的是」四點和不包含的範圍是否都對？你的回答：對（同時授權審查通過後自動 push 並開 PR；merge 另外決定）。

## 對你既有的資料做了什麼 (what this did to data you already had)

這個改動本身只改外掛自己的檔案，不讀寫你專案裡的任何東西。但有兩點會碰到你電腦上已有的設定，試跑中都遇到了：第一，在 agy 裡，你之前已經從 Claude Code 匯入了同名的 loom-code 與 loom-workflow；照說明書從複本「安裝」會直接蓋掉那兩份，之後「解除安裝」會連同那兩份匯入紀錄一起刪掉，不會回到原狀。這次我事先備份，結束後放回，外掛清單與檔案雜湊都和試跑前一模一樣。第二，Codex 在一次性會話後會自動把那個資料夾記為「信任」並寫進你的 Codex 設定；我已刪掉那筆，設定檔與試跑前逐位元組相同。另外，agy 的外掛資料資料夾清單在試跑前有一個名為 ruleprobe 的項目，試跑結束時已不在；我沒有動過它，也沒有備份它，可能是同時間其他工作階段清掉的，請你留意。

## I decided for you

- **腳本位置的寫法** — 沿用之前外掛根目錄已採用的跨宿主寫法：Claude Code 用它提供的技能資料夾變數，其他宿主用「放這份說明的資料夾」。其他參考文件一律指回那個定義，不自己算層數。以後要換寫法，需要改所有技能說明與檢查規則。
- **用現有的契約檢查來擋舊寫法** — 沒有另做一支工具，而是擴充原本的檢查，並涵蓋 python3、bash、sh 與 `./scripts/` 等形式，程式碼區塊裡的也算（因為代理會直接複製區塊裡的指令）。缺點是規則越擴越廣，將來可能誤擋合理寫法。
- **agy 用「外掛規則檔」送卡** — agy 沒有開場事件，所以把卡片做成 agy 每次對話都會載入、而 Claude Code 會忽略的外掛規則檔，並由既有的同步腳本從唯一的卡片來源自動產生。副作用是那份規則檔開頭多一行「由某腳本產生」的註解，agy 的模型也讀得到。
- **Codex 用開場鉤子送卡，並在說明書寫明要先信任** — 沿用 Claude Code 那支產生卡片的腳本；因為 Codex 要使用者信任過鉤子才會執行，說明書加了這個步驟。代價是你不信任就完全收不到卡。
- **Codex 也一起做**（你的決定，不是我替你決定的）— 已如實做在這次改動裡。

沒有收到任何「嚴重度 important 以上但被審查者駁回」的項目。

## Things I am not sure you want

- 在 agy 裡，照說明書「從複本安裝／解除安裝」會蓋掉並刪除你先前從 Claude Code 匯入的同名外掛。要不要在說明書提醒這件事，或建議先確認沒有同名匯入？（更新：41796371 已在說明書加上這個警告，請你確認寫法是否足夠。）
- agy 收到的卡片開頭多一行內部產生註解（寫著來源檔名與腳本名）。你能接受模型每次都讀到這行嗎？
- Codex 需要你手動信任一次鉤子才會出現卡片。這個一次性步驟你可以接受嗎，還是希望找其他不需信任的送法？

## 英文規則與格式規則是否守住

| 文件 | 英文規則 | 同時適用的格式規則 | 證據 |
|---|---|---|---|
| 計畫 | 守住 | 不適用 | `plan.md` 標題與任務內容皆為英文；「Questions asked」依規定保留使用者原問句 |
| 設計規格 | 不存在（這次不需要設計） | 需求條目格式不適用 | intent `needs-design: no` |
| 審查紀錄的發現 | 尚未取得，無法判斷 | 發現的標籤格式無法判斷 | 審查資料夾只有 `plan.md` |
| 試跑證據 | 守住 | 不適用 | `blindrun3/*.txt`、`*.jsonl` 皆為英文工具輸出 |
| 測試說明文字 | 守住 | 不適用 | 例：`"""A3 negative: an edited rule, an edited card, or no rule fails --check."""` |
| 測試名稱 | 守住 | 部分守住：多數是「對象＋預期」兩段式，缺少明確的「狀態」段 | 例：`test_bare_python3_scripts_command_flagged`、`test_claude_ignores_plugin_rules_dir` |
| 提交訊息 | 守住 | 不適用 | 例：`feat(loom-workflow): deliver the visualization card to agy as a plugin rule` |
