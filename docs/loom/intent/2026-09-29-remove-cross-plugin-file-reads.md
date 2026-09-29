# 各 plugin 只用自己的檔案
originator: kouko
kind: engineering
needs-design: no — 只改 plugin 內部的 skill 說明、範本複本、檢查腳本與測試，不觸及使用者介面
status: confirmed 2026-09-29
publication: automatic — authorized 2026-09-29 by kouko

## Problem
loom-design 的 5 個 skill，以及 loom-workflow 的 decision-map 與 distill-sessions，在執行時要找到 loom-code 裝在哪裡，才能跑它的檢查程式、讀它的範本或 skill 檔。每支援一種新工具（Claude Code、Codex、Antigravity），就要多寫一條「怎麼找到 loom-code」的規則；在找不到其他 plugin 安裝位置的工具上（例如接下來要支援的 OpenCode），這些 skill 一開始就會停下來。現有的邊界檢查也看不到這些跨 plugin 讀檔，新的依賴隨時可能再加進來。

## Proposed outcome
loom-design 與 loom-workflow 執行時不再讀或執行 loom-code 資料夾裡的任何檔案：需要的範本各自帶一份複本，由測試確保和 loom-code 的原版一致；原本寫完當下做的 intent 格式檢查改由 loom-code 的 write-plan 負責；product 變更缺少原則文件時的處理時機不變。邊界檢查擴大到能擋下新加入的跨 plugin 讀檔。

## Acceptance
1. loom-design 與 loom-workflow 執行時會用到的 skill、reference、腳本與 hook 中，沒有任何一處需要讀或執行 loom-code 資料夾裡的檔案；在沒有 loom-code 檔案可讀的環境中照著它們的步驟做，不會因為找不到 loom-code 而停下。
2. loom-design 與 loom-workflow 帶的範本複本和 loom-code 的原版內容一致；任一邊改了而另一邊沒改時，測試會失敗。
3. 在 loom-design 或 loom-workflow 執行時會用到的檔案中加入一個讀取 loom-code 檔案的寫法（包含腳本與 `<loom-code>` 這類路徑寫法）時，自動的邊界檢查會擋下。
4. 原本 loom-design 寫完 intent 當下做的每一項 intent 格式檢查（結構、product 問題不得含識別字、needs-design 理由與 commit 一致、needs-design 重新計算），在 loom-code 的 write-plan 開始規劃前都會執行；故意寫錯任一項的 intent 會在 write-plan 被擋下。
5. product 變更遇到 repo 沒有已批准的原則文件時，原則訪談仍在第一次確認 intent 的同一段對話中進行，不會延到後面的站。
6. 三個 plugin 的版號各自升級，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。

## Constraints
- skill 之間用名稱互相叫用（例如交給 `loom-code:write-plan`）不算讀檔，保留。
- 不複製 loom-code 的檢查程式到其他 plugin。
- 範本的原版仍在 loom-code；其他 plugin 的是複本。repo 內的測試可以讀兩邊來比對。
- 只裝 loom-design、沒裝 loom-code 時，能產出 intent 與 spec；接著的規劃與實作仍需要 loom-code。
- 沿用 2026-09-27-prose-evidence-class 的證據政策：不新增比對散文措辭的測試；比對檔案內容一致的結構檢查可以。
- 版號必須在 closing review 的 finalize 之前 commit。

## Out of scope
- OpenCode 支援本身（loader、`package.json`、安裝說明）。
- hook 與 agent 在其他工具上的移植。
- 合併 plugin，或把檢查程式獨立成可安裝的套件。
- loom-code 對另外兩個 plugin 的名稱叫用。
- 只在本 repo 開發與發版時用的腳本（例如機制普查、引用檢查）；它們不隨 plugin 在使用者環境執行。

## Open questions
- none
