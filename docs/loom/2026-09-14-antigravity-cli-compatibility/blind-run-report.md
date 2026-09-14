# 讓 loom 外掛能在 Antigravity CLI 上安裝與使用 — 我試了什麼、發生了什麼

2026-09-14 在專案的乾淨副本上試跑，版本 d6e4e9f5。這是需求重新確認後的新一輪；十條全部重試，每一條標題下方都標了試的版本。

這個分支還沒推上 GitHub，所以 README 第一行「從 GitHub 複製」我改用本機的乾淨複製代替。其餘步驟完全照 README 的 Antigravity 段落打，包括新的啟動寫法 `agy --add-dir "$PWD"`。

試跑途中分支前進到 3f3f4af3，只多了兩個提交：一個加測試，一個讓語言提醒在對話紀錄格式異常時不會出錯。那時第 6 條已經在 d6e4e9f5 上試完，所以沒有重跑；其他條目也不受這兩個提交影響。

之後分支又前進到 3d7f718e，改動如下：
- 需求重新確認：辨認 git／gh 指令時繼續不分大小寫。
- 審查站說明改成：先跑完盲跑並提交報告，審查者才讀最後的版本。
- agy 上不提供另一家模型的審查者。
- loom-workflow 的日文和中文 README 補上 agy 安裝段落。
- 幾處程式整理，行為不變。

我沒有在 3d7f718e 上重跑任何一條，只加看了第 1 條的日文 README（見第 1 條）。

## What you asked for, one line at a time

### 1. On a machine with agy and no prior loom install, following the repository's written install steps from a fresh clone installs all three plugins, and agy's plugin validation passes for each.
試的版本：d6e4e9f5
- **How I tried it**: 先記下 agy 目前裝了哪些外掛（9 個，沒有 loom）。接著照 README，在乾淨複製裡對三個外掛依序「檢查」再「安裝」（loom-code 先裝），最後列出外掛清單。
- **What happened**: 三個都檢查通過：loom-code 有 6 個技能、4 個助手、1 組掛鉤；loom-design 有 5 個技能；loom-workflow 有 12 個技能、1 組掛鉤。三個都裝上，清單裡看得到，原本的 9 個外掛都還在。
- **另外在 3d7f718e 只讀檢查**：loom-workflow 的日文 README 新增的 agy 段落，指令和英文版逐字相同：
  - 複製專案；
  - 先裝 loom-code，再裝 loom-workflow；
  - 用 `agy --add-dir "$PWD"` 啟動，並說明「.」不行、只在 agy 命令列有效。
  
  說明文字是對應的日文翻譯。這份 README 只講它自己和 loom-code 兩個外掛；三個一起裝的步驟在專案首頁的 README。
- **Evidence**: `evidence/00-agy-plugin-list-baseline.txt`、`evidence/01-install-validate-list-d6e4e9f5.txt`；日文 README 對照：`evidence/01b-loom-workflow-readme-ja-vs-en-3d7f718e.txt`
- **Verdict**: works — 照文件裝得起來，檢查全過。

### 2. After installing, every station and skill of the three plugins appears in agy's skill list, including when another installed plugin ships a skill with the same short name.
試的版本：d6e4e9f5
- **How I tried it**: 在一個空的練習資料夾啟動 agy（用完整路徑加入工作資料夾），請它列出看得到的所有技能。你原本裝的 conductor 外掛也有一個叫 `review` 的技能，所以這是真實的撞名情境。我再把清單逐一對照三個外掛的技能。
- **What happened**: 23 個 loom 技能一個不少（6 + 5 + 12）。審查站 `closing-review` 和 conductor 的 `review` 同時出現在清單裡，沒有被藏起來。
- **Evidence**: `evidence/02-agy-skills-d6e4e9f5.txt`、`evidence/02b-loom-skill-presence-d6e4e9f5.txt`（23 個都找到，0 個缺）
- **Verdict**: works — 有撞名時也看得到 loom 的每一站。

### 3. In agy, a small change in a throwaway repository is taken through capture-intent, write-plan, build, closing-review and ship; the loom checker accepts the intent, plan and attestation it produced, and its blind-run report is produced and committed on the change branch.
試的版本：d6e4e9f5
- **How I tried it**: 做一個只有加法函式的新練習專案，旁邊放一個本機遠端。照 README 用完整路徑啟動 agy，以使用者身分說兩句話：
  - 第一句：「用 loom 幫我加一個減法函式和測試，從 capture-intent 一路做到 ship」。
  - 它覆述需求、問「對嗎」之後，第二句回「yes，請一路做完」。
  
  完成後，我從遠端重新複製那個分支，自己再跑一次檢查程式。
- **What happened**:
  - **流程走完**：第一句約 2 分鐘，寫出需求，照規矩問「對嗎」。第二句約 12 分鐘，依序完成：需求確認 → 計畫 → 先寫測試再實作 → 對抗測試 → 盲跑 → 兩位審查者 → 產生審查紀錄 → 推上遠端。這次不需要我多說「請繼續」。
  - **角色派工符合預期**：實作、對抗、盲跑、兩位審查者，共五次派工。每一次都用 agy 內建的通用助手，第一句都是「先讀 loom 的某某角色說明，嚴格照它做」，讀的是外掛裡的角色說明檔。
  - **檢查程式接受了三份產出**：
    - 需求：第一次在主分支上跑，被拒，理由是「要在變更分支上做」。它開了分支後再跑就通過。
    - 計畫：通過。
    - 審查紀錄：第一次產生時被拒，理由是「對抗測試的指令必須直接執行測試檔」。它修正後重跑，成功寫出審查紀錄。
    - 推送前檢查：通過。
    - 我自己在遠端的乾淨複製上重跑需求、計畫、推送前檢查，全部通過；測試 10 個全過。
  - **盲跑報告有提交，也在推上去的分支裡**：遠端分支上看得到它，而且報告的提交排在審查紀錄之前。上一輪「報告沒提交」的問題修好了。
  - **推送的過程值得你知道**：
    - loom 正式的「推送並開 PR」指令拒絕了，理由是遠端不是 GitHub 網址。這是練習環境本來就會發生的，所以沒有開 PR。
    - 它接著打一般的 `git push`，被推送閘門擋下，理由是指令格式。這個分支已經有審查紀錄，所以只剩格式問題，這是正確的行為。
    - 它隨後去讀檢查程式的原始碼，照裡面的規則自己拼出標準格式的推送指令，推送成功。
- **Evidence**: `evidence/03-turn01-summary.txt`、`evidence/03-turn02-response.txt`、`evidence/03-dispatches-and-checker-d6e4e9f5.txt`（五次派工與每次檢查的結果）、`evidence/03-remote-and-checker-recheck-d6e4e9f5.txt`（遠端分支的檔案清單與我自己的重跑）
- **Verdict**: works — 整條流程走完，三份產出都被檢查程式接受，盲跑報告也提交在推上去的分支裡。沒有開 PR，因為練習用的遠端不是 GitHub。

### 4. In agy, pushing a change branch that has no matching review attestation is blocked by the loom push gate, and the first reason shown says the review attestation is missing.
試的版本：d6e4e9f5
- **How I tried it**: 在另一個練習專案開一個沒有審查紀錄的分支，請 agy 只執行一次最普通的 `git push origin <分支>`，被拒就不要繞路，並原文告訴我第一個理由。
- **What happened**: 被擋下，遠端只有原本的主分支，沒收到這個分支。agy 原文轉述的第一句是「分支上必須剛好有一份審查紀錄，找到 0 份」，第二句才是指令格式的說明。上一輪「第一句在講格式」的問題修好了。
- **Evidence**: `evidence/04-agy-push-block-d6e4e9f5.json`、`evidence/04-remote-branches-after.txt`
- **Verdict**: works — 擋得住，而且第一句就說出缺審查紀錄。

### 5. In agy, a new session receives loom's station order and the repository's kickoff defaults without the user asking.
試的版本：d6e4e9f5
- **How I tried it**: 做一個練習專案並放一份開案預設檔，裡面刻意寫「預設流程：精簡」。在專案資料夾裡照 README 打 `agy --add-dir "$PWD"` 開新對話，不准它讀檔或執行任何指令，只問三件事：站序、開案預設、有沒有收到「沒接上專案」的提醒。
- **What happened**:
  - 第一次我自己寫的預設檔格式不對：不是 loom 規定的「一行一個設定」寫法。結果它答得出站序，但回答「沒收到開案預設」，也沒有收到任何提醒。這是我準備的檔案有錯，不是這次變更的問題。
  - 把預設檔改成 loom 的格式再試一次：站序答對（capture-intent → write-spec → write-plan → build → closing-review → ship，出事時 maintain），三個開案預設都原文說出，包括「預設流程：精簡」，也沒有收到「沒接上專案」的提醒。上一輪「照 README 寫法接不上專案」的問題修好了。
- **Evidence**: `evidence/05b-session-context-pwd-d6e4e9f5.json`；格式不對那次：`evidence/05a-session-context-pwd-badfixture-d6e4e9f5.json`
- **Verdict**: works — 照 README 的寫法開新對話，站序和開案預設都自動送到。

### 6. In agy, after a loom skill is used in a Japanese or Chinese conversation, the language reminder that Claude Code gives also reaches the agent.
試的版本：d6e4e9f5
- **How I tried it**: 用完整路徑開新對話，用日文請 agy 使用 loom 的「回顧現況」技能，再請它原文引用載入技能後收到的語言提醒。我也翻了這次的對話紀錄，看提醒是不是真的被插進去，而不是模型自己編的。
- **What happened**:
  - 第一次 agy 需要執行指令，但印出模式沒辦法問我要不要允許，所以直接停下，什麼都沒回。這和這次變更無關。
  - 第二次限定在那個練習專案裡自動允許，就正常跑完。它先用日文回顧了專案現況，再原文引用提醒：「ユーザー向けの説明は常に会話言語（日本語）を使用してください。brief/verdict/commit などの機械向けアーティファクトは元の言語のままにします。」
  - 對話紀錄證實了這一點：它讀完技能檔之後，下一步就是系統插入的這段日文提醒。上一輪「提醒一次都沒送到」的問題修好了。
- **Evidence**: `evidence/06b-language-reminder-ja-d6e4e9f5.json`、`evidence/06c-transcript-steps-d6e4e9f5.txt`（第 4 步就是插入的提醒）；停下那次：`evidence/06a-language-reminder-ja-permission-denied-d6e4e9f5.json`
- **Verdict**: works — 在實際的日文對話裡，語言提醒送到了 agy。

### 7. In agy, writing a nested subfolder inside a skill folder is rejected by the loom-workflow folder-structure rule.
試的版本：d6e4e9f5
- **How I tried it**: 在練習專案裡放一份 loom-workflow 的副本，請 agy 用它的寫檔工具在某個技能的參考資料夾下「再開一層子資料夾」寫檔。接著請它在同一層直接寫檔。兩次都用完整路徑加入工作資料夾。
- **What happened**: 開子資料夾那次被擋下，agy 原文轉述了規則說明（技能資料夾裡只能有一層子資料夾，並建議怎麼改），子資料夾沒有產生。直接寫在同一層則成功。副本裡只多了那一個同層檔案。
- **Evidence**: `evidence/07a-agy-nested-write-d6e4e9f5.json`、`evidence/07b-agy-flat-write-d6e4e9f5.json`、`evidence/07c-references-listing-after.txt`
- **Verdict**: works — 開子資料夾會被拒，同層寫檔可以。

### 8. The existing package test suite and the Codex manifest drift check still pass, so Claude Code and Codex installs are unchanged.
試的版本：d6e4e9f5
- **How I tried it**: 在乾淨複製上照 README「Development」段落跑完整測試，再跑同一段列出的四個設定檔檢查（包含 Codex 設定檔一致性檢查）。
- **What happened**: Python 測試共 2090 個通過、6 個略過；17 組 shell 檢查共 145 項全過，整體結束狀態為成功。四個設定檔檢查都通過。第一次跑這四個檢查時，是我自己把指令打錯（shell 沒有把指令拆開），不是它們失敗；重跑後都通過，兩次紀錄都留在同一個檔案裡。跑完之後，複製裡沒有多出任何變更。
- **Evidence**: `evidence/08-package-tests-d6e4e9f5.txt`
- **Verdict**: works — 測試全綠，Codex 設定沒有漂移。

### 9. The repository's product principles name Antigravity CLI alongside Claude Code and Codex as a supported host.
試的版本：d6e4e9f5（閱讀）
- **How I tried it**: 打開這個版本的產品原則文件，找支援平台的地方。
- **What happened**:
  - 「給誰用」那句寫的是 Claude Code、Codex CLI 或 Antigravity CLI。
  - 「掛鉤由誰安裝」那條也列了這三個平台。
  - 簽核行補了一句「2026-09-14 由 kouko 加入 Antigravity CLI」。
- **Evidence**: `evidence/09-principles-d6e4e9f5.md`（第 2、5、24 行）
- **Verdict**: works

### 10. On Claude Code, Codex and agy the review station is invoked as `closing-review`, and loom's own station order and guidance use that name.
試的版本：agy 與 Claude Code 在 d6e4e9f5 實測；Codex 引用協調者先前的實測紀錄（見下）
- **How I tried it**:
  - **agy**：看第 2 條的技能清單，並看第 3、5 條實際的站序與派工。
  - **Claude Code**：只讓它暫時載入這次副本裡的 loom-code，不動全域設定，請它列出 loom-code 的技能。
  - **Codex**：我沒有權限在 Codex 裡安裝外掛，所以讀了協調者先前的實測紀錄：他把這個分支的 loom-code 暫時裝進 Codex，請它列出技能，測完就移除。那份紀錄沒有標版本，是在 bb875d48 那一輪做的。之後到 d6e4e9f5 的提交只修改了審查站說明的內容，沒有改任何技能的名字。
- **What happened**:
  - **agy**：清單裡是 `closing-review`。第 5 條它說出的站序寫 closing-review；第 3 條實際跑的也是這一站。
  - **Claude Code**：列出 `loom-code:build`、`closing-review`、`maintain`、`ship`、`using-loom-code`、`write-plan`，沒有 `review`。
  - **Codex**：列出來自這個分支副本的 `loom-code:closing-review`。同一份清單裡另一個 `loom-code:review`，來自你電腦上原本就裝著的舊版 loom，不是這個分支。
- **Evidence**: `evidence/02-agy-skills-d6e4e9f5.txt`、`evidence/05b-session-context-pwd-d6e4e9f5.json`、`evidence/10-claude-plugin-dir-skills-d6e4e9f5.txt`；Codex：上一輪暫存區的 `blindrun/evidence/10b-codex-live-closing-review.txt`（協調者執行）
- **Verdict**: works — 三個平台都叫得出 closing-review。Codex 那次不是我親手跑的，而且不是在 d6e4e9f5 上跑的。

## Review summary

- 我沒有收到這一輪的審查結論。
- 分支上現有的審查紀錄，是需求重新確認之前那一輪留下的：兩位審查者都判定通過。
- 紀錄裡還有兩個不擋出貨的小意見，都還開著。一個是「每個角色派一次」的說法可能讓人誤讀；另一個是 README 說互動模式也接不上專案，但實際只在印出模式觀察到。
- 這次盲跑的結果和那兩個小意見不衝突。

## Questions I asked you

這一輪盲跑沒有另外問你問題。

需求確認時你回答過的問題在計畫裡，最後兩個是這次重新確認新增的：
- 第 3 條原本寫「檢查程式接受盲跑報告」，但沒有規則在檢查它。你決定改成「盲跑報告要提交在變更分支上」。
- 推送被擋時，第一句要不要先說缺審查紀錄。你決定改，三個平台都先說。

## 對你既有的資料做了什麼 (what this did to data you already had)

三個 loom 外掛只是暫時裝進你的 agy，試完就解除安裝了。之後的外掛清單和開始前記下的一字不差，你原本的 9 個外掛都沒被動到。

安裝時 agy 自動建了一個空的 loom-design 外掛資料夾，我已經刪掉。loom-code 和 loom-workflow 的空資料夾在我開始前就存在（上一輪留下的），所以沒動。

所有 agy 對話都用練習專案的完整路徑啟動，只在練習專案裡寫檔、提交、推送。這一輪沒有碰到你電腦上其他專案，也沒有動 Claude Code 或 Codex 的設定：Claude Code 只在單次指令裡暫時載入副本。

agy 會照常把這幾次對話紀錄存在它自己的對話紀錄資料夾裡，我沒有刪。

## I decided for you

以下是計畫中由 agent 自行決定、沒有問你的事，用白話列出：

- **審查站連同內部代號一起改名** — 站名和技能資料夾一起改成 closing-review，讓兩邊保持一致；檢查程式裡「產生審查紀錄」的指令名和規則代號沒改。以後如果想連內部名稱也統一，要改的是檢查程式和所有引用它的地方。
- **外掛位置用「兩段式」說法描述** — 技能說明寫「在 Claude Code 用它提供的變數，在其他平台就往上找兩層資料夾」。這次 agy 上每一站都找得到檢查程式（第 3 條）。另外加了一條自動檢查，擋掉只寫 Claude 變數的寫法。
- **Antigravity 設定檔沿用現有的 Codex 同步工具產生** — 沒有另寫一個工具。電腦上沒裝 agy 時，相關檢查會自動略過，所以雲端測試不需要 agy。
- **agy 的三種提醒全靠一支轉接程式** — 推送檢查、開場說明、語言提醒都經由同一支轉接程式處理。agy 沒有「對話開始」事件，所以開場說明和語言提醒改在「模型每次開始思考前」插入。推送檢查遇到無法判斷的情況一律擋下。
- **技能資料夾規則改成「寫檔前檢查」** — agy 在寫完之後才觸發的掛鉤不能阻擋，所以改成寫之前先看目標路徑。Claude Code 那邊的規則不變。
- **agy 上用內建通用助手扮演 loom 的每個角色** — 規定一律派 agy 內建的通用助手，並要它先讀 loom 的角色說明。代價是：角色的限制只靠說明文字約束，不是 agy 本身強制，例如審查者「不准改檔」只是說明裡的一句話。
- **語言提醒改成在「這一輪使用者發言之內」找技能讀取** — agy 在讀檔結果回來之後才呼叫模型，所以不能只看最後一步。這次實測送到了（第 6 條）。
- **README 改用完整路徑啟動，並把「沒接上專案」的說法限定在實際觀察到的印出模式** — 這次照新寫法，開案預設送到了（第 5 條）。
- **審查站明寫「先提交盲跑報告，再產生審查紀錄」** — 產生審查紀錄本來就要求沒有未提交的檔案，這次在說明裡寫清楚。實測報告確實提交了（第 3 條）。
- **安裝方式訂為「複製專案後，逐一安裝三個外掛」** — loom-code 要先裝；日文和繁中 README 都補上同一段。
- **loom-design 的第二家審查說明補上 Antigravity** — 施工中發現那份說明只列了 Codex 和 Claude，所以追加一個任務補上，措辭照 loom-code 的版本。

這次重新確認時，由你決定的兩件事：

- **第 3 條驗收的說法改了** — 不再要求「檢查程式接受盲跑報告」（本來就沒有規則在檢查它），改成「盲跑報告要產生並提交在變更分支上」。這次實測符合新說法。
- **推送被擋時先說缺審查紀錄** — 三個平台共用同一段訊息；哪些推送會被擋不變，只改第一句先講什麼。這次實測第一句就是缺審查紀錄（第 4 條）。

我在這次盲跑中替你決定的：

- 分支還沒上 GitHub，所以用本機乾淨複製代替 README 的網址。
- 第 3 條需要你回答的地方，我以使用者身分回了「yes」。
- 第 5 條我第一次準備的開案預設檔格式不對，改成 loom 的格式後重試。
- 第 6 條第一次因為沒辦法問允許而停下，第二次限定在練習專案裡自動允許。
- Codex 只引用協調者先前的實測，沒有在 d6e4e9f5 上重跑。

審查者駁回的重大意見：沒有收到任何被駁回的重大意見可列。

## Things I am not sure you want

- 在 agy 裡，loom 正式的「推送並開 PR」指令被拒之後，agent 去讀檢查程式的原始碼，自己拼出標準格式的推送指令推上去了。這次分支已經有審查紀錄，閘門本來就會放行。但你希望 agent 遇到這種情況時自己想辦法推，還是停下來問你？
- 開案預設檔的格式寫錯時，loom 不會提醒，只會當作沒設定（第 5 條我自己踩到）。要不要在格式不對時提醒一句？
- agy 上每個 loom 角色都靠「先讀說明再照做」約束，審查者不改檔這類限制沒有強制力。這樣可以接受嗎？
- 你電腦上的 Codex 同時裝著舊版 loom，會同時看到舊的 `review` 和新的 `closing-review`。要提醒你之後更新或移除舊版嗎？

## 英文規則與範本規則逐項檢查

| 產出物 | 英文規則是否守住 | 範本規則 | 證據 |
|---|---|---|---|
| 計畫 | 守住：工程內容全文英文；只有「問過你的問題」一節照規定逐字保留你的中文問答 | 不適用 | `plan.md`：Questions asked 之前 0 個中日文字，Risks 0 個 |
| 規格 | 不適用：這個變更標為不需設計，沒有規格 | 需求編號格式：不適用（沒有規格） | 需求檔 `needs-design: no` |
| 審查紀錄的意見 | 守住：意見文字全英文 | 守住：兩個待處理的小意見都以規定的標籤開頭，並標註不擋出貨 | `evidence/12-review-record-findings-d6e4e9f5.txt`（`attestation.json` findings，0 個中日文字） |
| 證據檔 | 守住：都是英文的指令輸出；第 6 條的日文是測試輸入和被引用的提醒 | 不適用 | `evidence/*.txt`、`evidence/*.json` |
| 測試說明文字 | 守住：新增測試裡出現的中日文只是測試用的輸入資料，不是說明文字 | 不適用 | `evidence/11-english-rule-d6e4e9f5.txt`（`2e4da589..d6e4e9f5` 測試檔新增行） |
| 測試名稱 | 守住，英文 | 守住：新增 118 個測試，全部符合「單元_狀態_預期」三段以上的格式（只驗段數，沒評名字取得好不好） | `evidence/11-english-rule-d6e4e9f5.txt`（`def test_*`） |
| 提交訊息 | 守住：32 則，沒有任何中日文字 | 不適用 | `git log 2e4da589..d6e4e9f5` |

證據檔都放在這一輪盲跑暫存區的 `blindrun2/evidence/` 下，沒有提交進專案。
