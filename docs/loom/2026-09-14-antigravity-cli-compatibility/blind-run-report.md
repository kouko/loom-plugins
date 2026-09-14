# 讓 loom 外掛能在 Antigravity CLI 上安裝與使用 — 我試了什麼、發生了什麼

2026-09-14 在專案的乾淨副本上試跑，分三輪：先在 3f021a5 試完全部十條；分支前進到 d4a7555 後重試一部分；修正送來後，在 bb875d4 重新照 README 安裝，再重試第 1 到 6 條。每一條標題下方都標了**最後試的版本**。

這個分支還沒推上 GitHub，所以 README 第一行「從 GitHub 複製」我改用本機的乾淨複製代替，其餘步驟完全照 README 打。

## What you asked for, one line at a time

### 1. On a machine with agy and no prior loom install, following the repository's written install steps from a fresh clone installs all three plugins, and agy's plugin validation passes for each.
最後試的版本：bb875d4
- **How I tried it**: 先記下 agy 目前裝了哪些外掛（沒有任何 loom）。接著照 README 的 Antigravity 段落，依序對三個外掛做「檢查」和「安裝」（loom-code 先裝），最後列出外掛清單。三個版本各做一次。
- **What happened**: 三個外掛都檢查通過（loom-code：6 個技能、4 個助手、1 組掛鉤；loom-design：5 個技能；loom-workflow：12 個技能、1 組掛鉤）。三個都裝上，清單裡看得到它們，原本的 9 個外掛都還在。三個版本結果一樣。
- **Evidence**: `evidence/01-install-validate-list.txt`、`evidence/11-reinstall-d4a75550.txt`、`evidence/21-install-bb875d48.txt`
- **Verdict**: works — 照文件就裝得起來，檢查全過。

### 2. After installing, every station and skill of the three plugins appears in agy's skill list, including when another installed plugin ships a skill with the same short name.
最後試的版本：bb875d4
- **How I tried it**: 請 agy 列出它看得到的所有技能。你原本裝的 conductor 外掛也有一個叫 `review` 的技能，所以這是真實的撞名情境。
- **What happened**: 23 個 loom 技能全部出現（6 + 5 + 12），包含審查站的新名字 `closing-review`，而且就列在 conductor 的 `review` 旁邊，沒有被藏起來。三個版本都一樣。
- **Evidence**: `evidence/02-agy-skills.txt`、`evidence/02b-agy-skills-d4a75550.txt`、`evidence/22-agy-skills-bb875d48.txt`
- **Verdict**: works — 撞名時也看得到 loom 的每一站。

### 3. In agy, a small change in a throwaway repository is taken through capture-intent, write-plan, build, review and ship, and the loom checker accepts the intent, plan, attestation and blind-run report it produced.
最後試的版本：bb875d4
- **How I tried it**: 做一個只有加法函式的新練習專案，旁邊放一個本機遠端。照更新後的 README 用「加入工作資料夾」啟動 agy，接著以使用者身分說三句話：「用 loom 幫我加一個減法函式和測試，從 capture-intent 開始」；它覆述需求後回「yes，請一路做完」；它說在等實作助手時，我再說「應該做完了，請繼續」。
- **What happened**:
  - **README 的寫法本身不管用**：照 README 打 `agy --add-dir .`（用「.」代表目前資料夾），agy 仍然沒有接上專案。它回我「請用 `agy --add-dir <專案路徑>` 重新啟動」，沒有動任何檔案。把「.」換成專案的完整路徑，才正常開始。下面的結果都是用完整路徑跑的。
  - 用完整路徑之後，整條流程走完：需求確認（它照規矩問我「對嗎」）→ 計畫 → 先寫測試再實作 → 對抗測試 → 兩位審查者 → 產生審查紀錄 → 盲跑 → 推送前檢查 → 推上遠端。遠端現在確實有這個分支。三句話約 19 分鐘。
  - **上一輪的問題修好了**：實作、對抗、兩位審查者、盲跑，五次派工都用 agy 內建的通用助手。每次派工的第一句都是「先讀 loom 的某某角色說明，嚴格照它做」，讀的是外掛裡原本的說明檔。這一輪 agy 一次都沒有自己臨時定義替身。
  - 每一站呼叫檢查程式，都用已安裝外掛的完整位置，全部找得到。需求、計畫、審查人數、審查紀錄的產生、推送前檢查都通過。我事後在練習專案裡自己跑，需求和推送前檢查也都通過。
  - **不完整的地方一**：盲跑報告有寫出來，也拿給我驗收，但沒有提交，所以推上遠端的分支裡沒有這份報告。
  - **不完整的地方二**：檢查程式裡沒有任何一條規則在檢查盲跑報告，所以「檢查程式接受了盲跑報告」這半句仍然無法證明。
  - 印出模式下，agy 在實作助手還沒做完時就先結束了那一輪，所以需要我多說一句「請繼續」。
- **Evidence**: `evidence/23-turn01-capture-intent-bb875d48.json`（「.」寫法沒接上專案）、`evidence/23b-turn01-capture-intent-abs-bb875d48.json`、`evidence/23c-turn02-yes-bb875d48.json`、`evidence/23d-turn03-continue-bb875d48.json`、`evidence/23e-dispatches-and-checker-bb875d48.txt`、`evidence/23f-checker-recheck-bb875d48.txt`
- **Verdict**: partly — 流程走完，每個角色都照 loom 自己的說明做事。但 README 的「.」寫法接不上專案；盲跑報告沒進推上去的分支，也沒有檢查規則驗收它。

### 4. In agy, pushing a change branch that has no matching review attestation is blocked by the loom push gate, and the block reason is shown.
最後試的版本：bb875d4
- **How I tried it**: 在另一個練習專案開一個沒有審查紀錄的分支，請 agy 推上遠端（只推一次、被拒不要繞路）。三個版本各試一次。另外，我在 d4a7555 上直接把幾種推送寫法餵給已安裝的推送掛鉤，看它各給什麼理由。
- **What happened**: 每次都被擋，遠端完全沒收到這個分支，agy 也把拒絕原因原文轉給我。但一般人會打的推送指令，看到的理由仍然是「整個推送指令必須用標準的全引號寫法」，講的是指令格式，而不是「這個分支沒有審查紀錄」。只有把指令寫成 loom 自己出貨時用的精確格式，才會看到真正的理由「分支上必須剛好有一份審查紀錄，找到 0 份」。
- **Evidence**: `evidence/04d-agy-push-block-d4a75550.json`、`evidence/24-agy-push-block-bb875d48.json`、`evidence/04b-installed-push-hook-direct.txt`
- **Verdict**: partly — 真的擋得住，也有顯示理由；但一般推送看到的理由是在講格式，使用者看不出真正要補的是審查紀錄。

### 5. In agy, a new session receives loom's station order and the repository's kickoff defaults without the user asking.
最後試的版本：bb875d4
- **How I tried it**: 做一個練習專案，放一份開案預設檔（其中刻意寫「預設流程：精簡」）。開新對話，禁止 agy 讀任何檔案，只問它：站序是什麼、有哪個開案預設、有沒有收到「沒接上專案」的提醒。分三種啟動方式：不加工作資料夾、照 README 加「.」、加完整路徑。
- **What happened**:
  - 不加工作資料夾：站序答對，說沒收到開案預設，並原文引用新的提醒「沒有接上工作資料夾，所以沒載入開案預設；請使用者用 `agy --add-dir <專案>` 重新啟動」。這個修正有效。
  - 照 README 加「.」：結果和不加完全一樣，也收到「沒有接上工作資料夾」的提醒。
  - 加完整路徑：站序答對（capture-intent → write-spec → write-plan → build → closing-review → ship），說出「預設流程：精簡」，沒有收到提醒。
- **Evidence**: `evidence/25b-session-context-without-add-dir-bb875d48.json`、`evidence/25a-session-context-with-add-dir-bb875d48.json`（「.」寫法）、`evidence/25c-session-context-absolute-add-dir-bb875d48.json`
- **Verdict**: partly — 用完整路徑時站序和開案預設都送到了，沒接上時也會提醒；但照 README 寫的「.」其實接不上，照文件做的使用者拿不到開案預設。

### 6. In agy, after a loom skill is used in a Japanese or Chinese conversation, the language reminder that Claude Code gives also reaches the agent.
最後試的版本：bb875d4
- **How I tried it**: 用日文請 agy 使用 loom 的「回顧現況」技能，再請它原文引用載入技能後收到的語言提醒。bb875d4 上試兩次（「.」和完整路徑各一次），之前的版本也試過四次。每次都翻對話紀錄，看有沒有額外插進去的訊息。我也把這次的對話紀錄直接交給已安裝的掛鉤。
- **What happened**: agy 每次都確實載入了 loom 技能，但每次都回答「沒有收到」，對話紀錄裡也沒有語言提醒。直接測掛鉤時：只給到「模型剛下指令讀技能檔」這一步，兩種紀錄格式現在都會產生正確的日文提醒，上一輪的格式問題確實修好了。但只要紀錄裡多了下一步「讀檔的結果」，掛鉤就什麼都不產生。agy 在讀檔結果回來之後才會再呼叫模型，那時紀錄的最後一步已經是讀檔結果，所以實際使用時提醒永遠不會觸發。
- **Evidence**: `evidence/26-language-reminder-ja-bb875d48.json`、`evidence/26c-language-reminder-ja-abs-bb875d48.json`、`evidence/26b-installed-hook-anchor-direct-bb875d48.txt`；較早的版本：`evidence/06f-agy-language-reminder-ja-d4a75550.json`
- **Verdict**: not yet — 在實際的日文對話裡，語言提醒仍然一次都沒送到 agy。

### 7. In agy, writing a nested subfolder inside a skill folder is rejected by the loom-workflow folder-structure rule.
最後試的版本：d4a7555
- **How I tried it**: 在練習專案裡放一份 loom-workflow 的副本，請 agy 在某個技能的參考資料夾下「再開一層子資料夾」寫檔，接著請它在同一層直接寫檔。
- **What happened**: 開子資料夾那次被擋下，agy 原文轉述了規則說明（技能資料夾裡只能有一層子資料夾），檔案沒有產生。直接寫在同一層則成功。3f021a5 和 d4a7555 結果一樣。（3f021a5 那次同層寫檔沒指定專案，agy 把檔案寫進你電腦上另一份 loom-plugins 副本；我已刪掉，那份副本已恢復乾淨。）
- **Evidence**: `evidence/07c-agy-nested-write-d4a75550.json`、`evidence/07d-agy-flat-write-d4a75550.json`
- **Verdict**: works — 開子資料夾會被拒，同層寫檔可以。

### 8. The existing package test suite and the Codex manifest drift check still pass, so Claude Code and Codex installs are unchanged.
最後試的版本：d4a7555
- **How I tried it**: 在乾淨複製上照 README「Development」段落跑完整測試，再跑 Codex 設定檔一致性檢查。
- **What happened**: d4a7555：Python 測試 2030 個通過、6 個略過，17 組 shell 檢查共 145 項全過，一致性檢查通過。3f021a5 也全過（1974 個通過）。bb875d4 上沒有重跑。
- **Evidence**: `evidence/08b-package-tests-d4a75550.txt`、`evidence/08-package-tests-and-manifest-check.txt`
- **Verdict**: works — 試過的版本測試全綠，Codex 設定沒有漂移。

### 9. The repository's product principles name Antigravity CLI alongside Claude Code and Codex as a supported host.
最後試的版本：3f021a5
- **How I tried it**: 打開產品原則文件，找支援平台的地方。
- **What happened**: 「給誰用」那句寫的是 Claude Code、Codex CLI 或 Antigravity CLI。「掛鉤由誰安裝」那條也列了這三個平台。簽核行補了一句「2026-09-14 由 kouko 加入 Antigravity CLI」。
- **Evidence**: 產品原則文件（`PRINCIPLES.md`）第 2、5、24 行
- **Verdict**: works

### 10. On Claude Code, Codex and agy the review station is invoked as `closing-review`, and loom's own station order and guidance use that name.
最後試的版本：3f021a5（agy 清單另在 bb875d4 看過；Codex 實測由協調者執行，版本見下）
- **How I tried it**: agy：看技能清單。Claude Code：只用這次的副本、不動全域設定，請它列出 loom-code 的技能。Codex：我沒有權限在 Codex 裡安裝外掛。協調者另外做了一次實測：把這個分支的 loom-code 暫時裝進 Codex，請它列出技能，測完就移除；我讀了那份紀錄。我也搜尋了整個外掛，確認沒有留下舊的 `review` 名稱。
- **What happened**: agy 和 Claude Code 列出的都是 `loom-code:closing-review`。Codex 實測列出 `loom-code:closing-review`，而且來源是這個分支的副本。清單裡另一個 `loom-code:review` 來自你電腦上原本就裝著的舊版 loom，不是這個分支的。紀錄最後有移除的記錄。舊名只剩在更新紀錄的歷史條目，和一個專門抓舊名殘留的測試裡。站序設定和新對話的開場說明都寫 closing-review（第 5 條 agy 實際說出來的就是這個）。
- **Evidence**: `evidence/02-agy-skills.txt`、`evidence/22-agy-skills-bb875d48.txt`、`evidence/10-claude-loom-code-skills.txt`、`evidence/10b-codex-live-closing-review.txt`（協調者執行）、`evidence/10-closing-review-name-scan.txt`
- **Verdict**: works — 三個平台都叫得出 closing-review。Codex 那次不是我親手跑的；另外，你電腦上的 Codex 目前同時裝著舊版，會同時看到舊的 `review`。

## 對你既有的資料做了什麼 (what this did to data you already had)

三個 loom 外掛只是暫時裝進你的 agy，前後裝過三輪。每一輪結束我都解除安裝，外掛清單和開始前記下的一字不差，你原本的 9 個外掛都沒被動到。安裝時 agy 自動建的兩個空外掛資料夾也刪了；loom-code 那個空資料夾在我開始前就存在，所以沒動。第一輪有一件意外：agy 把一行測試文字寫進你電腦上另一份 loom-plugins 副本。我已刪掉那個檔案，那份副本目前沒有未提交變更。同一輪，agy 為了找分支讀過你家目錄底下的一些專案和 shell 歷史紀錄，只讀、沒有修改。Codex 的暫時安裝由協調者執行，紀錄裡有移除記錄。其餘都發生在這次新建的練習專案裡，沒有碰到你既有的專案，也沒有動到 Claude Code 或 Codex 的設定。

## I decided for you

以下是計畫中由 agent 自行決定、沒有問你的事，用白話列出：

- **審查站連同內部代號一起改名** — 站名和技能資料夾一起改成 closing-review，讓兩邊保持一致；檢查程式裡「產生審查紀錄」的指令名和規則代號不改。以後如果想連內部名稱也統一，要改的是檢查程式和所有引用它的地方。
- **外掛位置用「兩段式」說法描述** — 技能說明寫的是「在 Claude Code 用它提供的變數，在其他平台就往上找兩層資料夾」。這次 agy 上每一站的檢查程式都找得到（第 3 條）。另外加了一條自動檢查，擋掉只寫 Claude 變數的舊寫法。
- **Antigravity 設定檔沿用現有的 Codex 同步工具產生** — 沒有另寫一個工具。電腦上沒裝 agy 時，相關檢查會自動略過，所以雲端測試不需要 agy。
- **agy 的三種提醒全靠一支轉接程式** — 推送檢查、開場說明、語言提醒都經由同一支轉接程式處理。agy 沒有「對話開始」事件，所以開場說明和語言提醒改在「模型每次開始思考前」插入。推送檢查遇到無法判斷的情況一律擋下。第 6 條的語言提醒就是在這個時間點上觸發不到。
- **技能資料夾規則改成「寫檔前檢查」** — agy 在寫完之後才觸發的掛鉤不能阻擋，所以改成寫之前先看目標路徑。Claude Code 那邊的規則不變。
- **agy 上改用內建通用助手扮演 loom 的每個角色** — 外掛附帶的助手在 agy 上沒有工具可用，所以規定一律派 agy 內建的通用助手，並要它先讀 loom 的角色說明。這次實測有效（第 3 條）。代價是：角色的限制只靠說明文字約束，不是 agy 本身強制，例如審查者「不准改檔」只是說明裡的一句話。
- **README 教使用者用 `agy --add-dir .` 啟動** — 用「.」代表目前資料夾。這次實測發現「.」接不上專案，要完整路徑才行（第 3、5 條）。
- **沒接上專案時，只提醒、不阻擋** — 新對話如果沒接上專案，會提醒 agent 請使用者重新啟動，但不會禁止它繼續工作。
- **安裝方式訂為「複製專案後，逐一安裝三個外掛」** — loom-code 要先裝；日文和繁中 README 都補上同一段。
- **loom-design 的第二家審查說明補上 Antigravity** — 施工中發現那份說明只列了 Codex 和 Claude，所以追加一個任務補上，措辭照 loom-code 的版本。
- **我在盲跑中替你決定的** — 分支還沒上 GitHub，所以用本機乾淨複製代替 README 的網址。「.」寫法失敗後，第 3、5、6 條改用專案的完整路徑繼續試，這樣才量得到後面的行為。第 3 條需要你回答的地方，我以使用者身分回了「yes」和「請繼續」。第 7、8、9 條沒有在 bb875d4 重試，因為這一輪的修正沒有動到它們相關的部分。

審查者駁回的重大意見：沒有收到任何被駁回的重大意見可列。

## Things I am not sure you want

- README 寫的 `agy --add-dir .` 在 agy 1.2.2 上接不上專案，要換成完整路徑（例如 `agy --add-dir "$PWD"`）嗎？
- 在 agy 裡，日文或中文對話的語言提醒仍然完全沒送到。這條要算這次必須做到的嗎？
- 一般人打的推送指令被擋時，看到的理由是在講「指令格式」，不是「還沒審查」。這樣可以接受嗎？還是希望第一句就說出缺審查紀錄？
- 盲跑報告寫出來了卻沒有提交，推上去的分支裡沒有它；而且檢查程式也沒有規則在檢查它。要補一條規則，還是把這條驗收的說法改掉？
- agy 上每個 loom 角色都靠「先讀說明再照做」約束，審查者不改檔這類限制沒有強制力。這樣可以接受嗎？
- 你電腦上的 Codex 同時裝著舊版 loom，會同時看到舊的 `review` 和新的 `closing-review`。要我提醒你之後更新或移除舊版嗎？

## 英文規則與範本規則逐項檢查

| 產出物 | 英文規則是否守住 | 範本規則 | 證據 |
|---|---|---|---|
| 計畫 | 守住，全文英文 | 不適用 | `docs/loom/2026-09-14-antigravity-cli-compatibility/plan.md` |
| 規格 | 不適用：這個變更標為不需設計，沒有規格 | 需求編號格式：不適用（沒有規格） | 需求檔 `needs-design: no` |
| 審查紀錄的意見 | 盲跑時沒有收到可檢查的審查意見 | 意見標籤格式：同左，無法檢查 | 我這一份只從變更資料夾讀了 `plan.md` |
| 證據檔 | 守住，都是英文的指令輸出 | 不適用 | `evidence/*.txt`、`evidence/*.json`；第 6 條的日文是測試輸入 |
| 測試說明文字 | 守住；出現的日文、中文只是測試用的輸入資料 | 不適用 | `test_agy_adapter.py`、`test_adversarial_agy_adapter.py`、`test-adversarial-agy-skill-folder.sh` |
| 測試名稱 | 守住，英文 | 守住：到 bb875d4 為止新增 109 個測試，全部符合「單元_狀態_預期」三段以上的格式（只驗段數，沒評名字取得好不好） | 對合併基準 `2e4da589..bb875d48` 的差異裡新增的 `def test_*` |
| 提交訊息 | 守住：24 則都是英文，沒有任何中日文字 | 不適用 | `git log 2e4da589..bb875d48` |

證據檔都放在盲跑暫存區的 `blindrun/evidence/` 下，沒有提交進專案。
