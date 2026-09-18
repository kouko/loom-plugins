# 盲跑報告：發佈被擋的當下，指出合法的路

intent: docs/loom/intent/2026-09-18-blocked-publish-names-the-legal-routes.md
分支: `fix/2026-09-18-blocked-publish-names-the-legal-routes`
盲跑對象: **HEAD `fc5b8401`**（第二次盲跑；第一次寫於 `2228bb25`）
盲跑時間: 2026-09-18
盲跑執行者: agent（loom-code blind-runner），未參與任何實作

---

## 1. 一句話結論

**改變了什麼**：以前，當發佈檢查程式擋下推送、開 PR 或合併時，它只說「這個分支沒有驗證紀錄」，沒有指出接下來能做什麼，於是 agent 就把那行被擋的指令交給你，請你自己貼到終端機執行。現在同一則拒絕訊息會依照分支當下的狀態，講出對那個狀態而言真的走得通的做法，並且一律以「絕對不要把這行指令交給使用者執行」作結。

**跑起來如何**：**在 `fc5b8401` 上沒有任何一條驗收條件失敗。** 八條裡有六條我用真實指令跑過而且成立；第 4 條與第 5 條各有一部分在今天這個時間點仍無法觀察，原因寫在它們自己的列裡。

**第二次盲跑最重要的一件事，必須先講**：我在團隊要我複跑的那個版本 `057d0c43` 上，**跑出了一個真實的測試失敗**——整包測試結束碼是 1。原因是一個被標成「預期會失敗」的對抗測試已經被修好、卻沒有把標記拿掉，測試框架因此把「意外通過」判為失敗。這個問題在我複跑期間由後續兩個 commit（`3635c03f`、`fc5b8401`）解掉了，我在最新的 `fc5b8401` 上重跑，整包測試結束碼 0。細節在第 4 節第 8 條與附錄 N、O。

> 本報告出現的名詞，第一次出現時都先用白話解釋：
> - **驗證紀錄**：一個放在 `docs/loom/<變更代號>/attestation.json` 的檔案，裡面記錄這個分支通過了哪些審查與測試。沒有它，發佈檢查程式就不放行。
> - **閘門**：`loom_checker.py` 這支檢查程式裡的一條條規則。不通過就印出一行 `BLOCK <規則名稱>: <理由>` 並以錯誤碼結束。
> - **站**：這套流程把一次變更切成幾個階段，每個階段叫一個站。「審查站」（closing-review）就是產出驗證紀錄的那一站。
> - **跳站確認**：agent 可以提出「這次跳過某幾站」的提案，提案會印出一個四碼的代號；你在對話框裡親手打 `/loom-code:expert-mode <代號>`（在 Codex 上是 `$expert-mode <代號>`）之後，這個跳站才算數。
> - **攔截程式（hook）**：agent 每次要執行終端機指令之前，系統會先把指令文字交給一支檢查程式過目。它可以在指令真的跑起來之前擋下來。

---

## 2. 兩次盲跑之間變了什麼

| 項目 | 第一次（`2228bb25`） | 這一次（`fc5b8401`） |
|---|---|---|
| 拒絕訊息的結尾 | 只有一種：講兩條路 | **四種**，依分支狀態擇一（見第 4 節第 1 條） |
| 路徑二的說明 | 只說「在能記錄確認的 session 裡」 | 多加一句：每個變更只能提一次跳站提案 |
| 確認方式的寫法 | 只寫 `/loom-code:expert-mode <code>` | 同時寫出 Codex 的 `$expert-mode` |
| 開 PR 的攔截程式 | — | 整條 PR 內文規則都適用，且只允許名單內的參數；帶 `--label`、`--assignee` 的開 PR 指令現在會被擋 |
| 站的說明文件 | 「遇到拒絕就走它指名的補救」 | 多一句：**拒絕沒有指名任何補救時，就把拒絕回報出來然後停住** |
| 已知限制 | 四項 | **三項，另有一則不計入的提醒**：第一次列的「內容已經進主線的分支會卡在審查站」已經被修掉，其餘三項照舊（見第 7 節） |
| spec 的建置前審查欄位 | `not-required` | **`required — owed and not run`**（見第 6 節） |

### 被修掉的那一項限制

第一次盲跑時我列了一項：內容已經進主線的分支，會卡在審查站原地打轉——拒絕訊息叫 agent 去跑審查站，但那個分支跑幾次都不會脫離。

`41cbcf1b` 補上了第四種拒絕結尾，專門給這個狀態：它**完全不再提審查站那條路**，改成告訴你「這個分支相對基準沒有任何新東西，沒有東西可發佈，你要發的變更應該從一份新的 intent、在自己的分支上重來」。我在一個擺成這個狀態的拋棄式 repo 上實跑確認（第 4 節第 1 條第二列、附錄 C）。對應的對抗測試也被重新校準成檢查「這裡不會指名那條路」，並且通過。

**這已經不是使用者會遇到的限制，而是一個有專屬訊息的已處理狀態。** 整個對抗測試模組現在 98 項全過，沒有任何一項被標記為預期失敗。

---

## 3. 我是怎麼跑的

- 把 repo 重新 clone 到乾淨的暫存目錄，切到 `fc5b8401`，不使用原本的工作目錄。
- 全程沒有對外連線到 GitHub，沒有推送、沒有開 PR、沒有合併。
- 三點需要說明白：
  1. 為了讓 `publish` 指令能走到「沒有驗證紀錄」那一關，我把這個 clone 的 origin 位址改成一個不存在的 GitHub 位址 `https://github.com/blindrun-sandbox/loom-plugins.git`。我先讀過 `loom-code/scripts/loom_checker/command_handlers/publish.py`，確認那一關在任何對外指令之前執行，所以不會產生網路請求；實際輸出也證實它停在那一關。
  2. 為了看到另外三種拒絕結尾，我在暫存目錄另外建了三個**全新的、拋棄式的** git repo，各自擺成一種狀態，然後用受測分支的檢查程式去跑它們。受測的 repo 完全沒有被改動。
  3. repo 自己宣告的整包測試指令，內部有一段會跑 `npm` 安裝 Node 套件。我對 Python 的部分加了 `--offline`，但 `npm` 那一段是 repo 測試指令自己的行為，不在我控制範圍內，它有可能接觸過 npm 套件倉庫。除此之外沒有其他對外連線。
- 我沒有修改這個 repo 裡除了本報告以外的任何檔案。

---

## 4. 逐條驗收

編號沿用 intent 的 Acceptance 編號。

### 第 1 條 — 在沒有驗證紀錄的分支上執行正規發佈指令，拒絕訊息同時指出兩條合法路徑

**變了什麼**：第一次盲跑時，拒絕訊息只有一種結尾。現在它有**四種**，程式會依照分支當下的狀態挑一種。我把四種都跑出來了。

**我做了什麼**：

- 在乾淨 clone（此分支本來就沒有 `attestation.json`）上跑正規發佈指令 `loom_checker.py publish --confirm-authorized …`，以及底層的 `loom_checker.py push`。
- 另外建三個拋棄式 repo，分別做出「有工作但沒驗證紀錄」「分支相對基準沒有任何新東西、而基準已經有驗證紀錄」「一個分支裡有兩份驗證紀錄」三種狀態，各跑一次 `push`。
- 第四種狀態（讀不到數量）不是 CLI 能直接製造的——它只在合併指令解析不出數字時發生——所以我直接呼叫決定結尾的那個函式並印出結果，這一點我如實標記為「非真實指令觀察」。

**我看到什麼**：四種結尾都以錯誤碼 1 被擋，而且都以同一句 `never hand the blocked publication command to the user to run` 作結。

| 分支狀態 | 訊息告訴你什麼 |
|---|---|
| 有工作、沒有驗證紀錄（`found 0`） | **兩條路**：①跑審查站，不需要任何確認，任何 session 都能走；②在能記錄你親手輸入的 session 裡、而且每個變更只能用一次，提出跳站提案，由你打確認碼 |
| 相對基準沒有任何新東西，而基準已經有驗證紀錄（`found 0`） | 這個分支沒有東西可發佈，兩條路都不適用，你要發的變更應該從一份新的 intent、在自己的分支上重來 |
| 一個分支裡有兩份以上驗證紀錄（`found 2`） | 一次發佈只涵蓋一個變更，兩條路都不適用；要先把分支差異收斂到只剩一個已驗證的變更 |
| 數量讀不出來 | 不對數量下任何結論，也不指名任何路；請在 repo 裡用 `loom_checker.py push` 讀出數量，再照那則拒絕做 |

我另外查證了路徑二講的兩種確認寫法都是真的會生效的：`loom-code/scripts/loom_checker/selection.py` 把 `/loom-code:expert-mode` 與 `$expert-mode` 都列在可接受的開頭字串裡。

**結論：成立**（第一次盲跑也成立；這次是訊息內容變多、且每一種都經實跑確認）。

---

### 第 2 條 — 合併指令因缺少驗證紀錄而拒絕時，出現同樣的資訊

**我做了什麼**：在乾淨 clone 上跑 `loom_checker.py land --accepted-by kouko`；在「兩份驗證紀錄」與「沒有東西可發佈」兩個拋棄式 repo 上也各跑一次。

**我看到什麼**：三次都以錯誤碼 1 被擋，規則名稱是 `land.merge`，而結尾那一大段與 `push` 在同樣狀態下印出的**逐字相同**。

**結論：成立**（與第一次盲跑相同，訊息內容隨第 1 條一起更新）。

---

### 第 3 條 — 站的說明文件載明「發佈被擋時不得把指令交給使用者執行」

**變了什麼**：規則本身還在，但多了一句處理「拒絕沒有指名任何補救」的情況。

**我做了什麼**：讀 `loom-code/skills/ship/SKILL.md`，並檢查這份文件有沒有把這段話標成閘門（這個 repo 用 `<!-- gate: … -->` 來標示「這段散文算閘門」）。

**我看到什麼**：規則在 `loom-code/skills/ship/SKILL.md:122-129`。現在寫的是：不要自己組推送或開 PR 的指令，也不要把被拒絕的發佈指令交給使用者執行；**拒絕有指名補救就照做，沒有指名補救就把拒絕回報出來然後停住**——分支沒有驗證紀錄時，補救就是那兩條路。整份文件裡沒有任何 `gate:` 標記，所以這條規則仍然是給 agent 讀的指引，不是可判定的閘門。

**結論：成立**（第一次盲跑也成立；這次多了「沒有補救就停住」那一句）。

---

### 第 4 條 — 使用者完成一次跳站確認後，紀錄明載被跳過的站，發佈完成推送並開出 Ready PR，PR 內文含跳站揭露

**這一條我仍然沒有辦法用一次完整的真實流程證實**，原因與第一次盲跑相同。我把它拆成四段。

**(a) 提出跳站提案 — 真實跑過，成立。**
`loom_checker.py selection propose … --origin agent --skip reviewers` 成功，印出確認碼 `7SHT` 與八個站的表，`reviewers` 標為 `skip`。

**(b) 使用者親手確認 — agent 做不到，而且這正是設計要的。**
我試著自己把「使用者打了確認碼」這件事送進負責記錄的程式，被擋：`BLOCK selection.guard: the selection capture command runs only from the prompt hook`。我試著直接讀那份紀錄檔，也被擋：`BLOCK selection.guard: names the selection record store`。也就是說，跳站確認只能由你本人在對話框裡打字產生。`selection show` 因此仍然回報 `"bound": false`。這正好是 intent 的 Constraints 第 2 條要的效果，但也代表第 4 條開頭那個前提在我的盲跑裡沒有被建立。

**(c) 「確認之後，審查站產出的紀錄明載被跳過的站」— 這次有真實觀察，成立。**
repo 自己的對抗測試 `test_probe_named_proposal_drops_the_reviewer_floor` 會在一個拋棄式 repo 裡完整走一次：提出提案 → 送進使用者打字的確認 → 用一份**完全沒有審查人意見**的輸入跑 `finalize-review` → 斷言它成功結束而且真的寫出 `attestation.json`。這一項通過。相對的控制組 `test_probe_named_proposal_without_the_skip_does_not_drop_the_floor`（提案裡沒寫要跳過審查人時，門檻不降）也通過。

**(d) 「發佈完成推送並開出 Ready PR、內文含跳站揭露」— 透過 repo 自己的測試接縫觀察，成立。**
我把「驗證紀錄裡已經有一筆使用者確認的跳站」這個狀態餵給真正的發佈程式，並把它實際送出的外部指令與最後送出的 PR 內文原封不動印出來：

- 執行了推送：`git … push --no-follow-tags --recurse-submodules=no -u --no-verify origin <HEAD>:refs/heads/feature`
- 執行了開 PR：`gh pr create --base main --head feature --title … --body-file …`，**沒有 `--draft`**，後面也沒有任何 `pr ready`，也就是開出來就是 Ready PR
- PR 內文的 `## Verification` 段落開頭就是跳站揭露，逐字為：
  ```
  Skipped steps: adversarial — authority: user-typed (AB2C, 2026-09-13)
  Skipped steps: reviewers, adversarial — authority: user-typed (QRST, 2026-09-14)
  Prior failure: reviewers finalize.verdicts 2026-09-12
  Prior failure: finalize finalize.digest 2026-09-13
  ```
- 反面案例也成立：同樣狀態但內文沒有揭露時，在送出任何對外指令之前就被擋（錯誤碼 1、規則 `push.contextual-body`、外部指令清單為空）。

需要誠實說明的是：這個骨架把「驗證驗證紀錄」那一步換成直接通過，所以它證明的是「確認之後的發佈行為」，不是驗證紀錄本身的檢查。

**這次新增的一段觀察**：開 PR 那條攔截程式路線現在也會套用整條 PR 內文規則，而且只接受名單內的參數。我實跑三種情況：

```
allowlisted options only → BLOCK push.attestation: remote branch 'feature' must already equal reviewed HEAD …
plus --label             → BLOCK push.attestation: PR creation must use the canonical trusted-gh command from loom-code:ship
plus --assignee          → BLOCK push.attestation: PR creation must use the canonical trusted-gh command from loom-code:ship
```

第一行走得更遠（在我的拋棄式 repo 裡因為另一個無關的理由被擋），後兩行在「看內文」之前就被擋掉了。這代表：**以後開 PR 的指令帶 `--label` 或 `--assignee` 會被拒絕**，這是每個採用這套流程的 repo 都會感受到的改變。

**結論：(a)(c)(d) 成立；(b) 依設計無法由 agent 建立，因此「從你確認到開出 PR」的一次性真實跑仍未被觀察。要完整走完，需要你在同一個 session 裡親手打一次 `/loom-code:expert-mode <代號>`。**

---

### 第 5 條 — 本次變更自身的推送與開 PR 由 agent 執行；合併在你口頭同意後同樣由 agent 執行；你全程不輸入任何 git 或 gh 指令

**結果與第一次盲跑相同，只有數字更新。**

- 這個分支相對 `main` 現在有 **24 個 commit**（`3bdaa258` 到 `fc5b8401`）。**每一個** commit 都帶著 `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>` 與 `Claude-Session: …session_0146jwneKWsFu39c2RATq8FU`。
- **推送仍然還沒有發生。** 分支沒有上游，本機沒有 `refs/remotes/origin/fix/2026-09-18-…`，分支的 reflog 裡沒有任何一筆推送。
- **開 PR 與合併也還沒有發生。**

**我無法判定的部分**：git 只記「做了什麼」，不記「是誰在鍵盤上打的」。我可以證明這 24 個 commit 出自這個 agent session，但無法用 repo 證明「你完全沒有自己打過任何 git 指令」——只能說 repo 裡沒有留下任何看起來像人手工執行的痕跡。

**什麼時候可以觀察到剩下的部分**：推送與開 PR 會在 ship 站執行時發生，也就是你接受這份報告之後；合併在你口頭同意之後。那時可以用 `git branch -vv`、`git reflog` 與 PR 頁面的建立者逐一確認。

**結論：已發生的部分（24 個 commit 全由 agent 產生）成立；推送、開 PR、合併三個動作仍未發生，因此未被觀察。**

---

### 第 6 條 — 閘門沒有任何一條規則被放寬

**我做了什麼**：

1. 在乾淨 clone（沒有驗證紀錄、沒有跳站確認）上分別跑 `push`、`publish`、`land`、`finalize-review`。
2. 把分支上的規則清單（`loom_checker.py --list-rules`）與分岔點 `8b346852` 的清單逐字比對。
3. 把 `loom-code/scripts/` 底下這次被刪掉的每一行斷言與拒絕都列出來檢查。
4. 跑這次變更自己的對抗測試檔。
5. 額外檢查這次新增的「只允許名單內參數」是放寬還是收緊。

**我看到什麼**：

1. 四個指令全部被擋，錯誤碼都是 1：`push` → `BLOCK push.attestation`；`publish` → 同一條規則；`land` → `BLOCK land.merge`；`finalize-review` → `BLOCK finalize.verdicts`。
2. 兩份規則清單 **完全相同**，各 25 條，`diff` 沒有任何差異。
3. 程式碼裡沒有任何拒絕被刪掉。測試裡只有一行斷言被改寫：原本寫「錯誤訊息不以某個完整字串開頭」，改成「錯誤訊息裡不出現 `found 0`」——這是**收緊**，因為原本的寫法會放過「開頭是同一個數量、但結尾換了一種」的訊息。
4. 對抗測試 98 項全部通過，沒有任何被標記為預期失敗的項目。
5. 新增的參數名單是**收緊**：以前 `--label`、`--assignee` 會被放行，現在被擋（實跑驗證，見第 4 條）。沒有任何以前會被擋的東西現在被放行。

**結論：成立**（與第一次盲跑相同）。

---

### 第 7 條 — 盲跑報告逐條記錄每一個 git 與 gh 動作由誰執行

| # | 動作 | 執行者 | 依據 |
|---|---|---|---|
| 1 | 建立分支與兩次改名（2026-09-18 上午） | **無法判定** | git 的 reflog 記錄動作與時間，不記錄誰下的指令 |
| 2 | 24 個 commit：`3bdaa258` 到 `fc5b8401` | **agent**（本 session） | 每一個 commit 都帶 `Co-Authored-By: Claude Opus 5 (1M context)` 與 `Claude-Session: …session_0146jwneKWsFu39c2RATq8FU`；我逐一檢查過，沒有一個漏掉 |
| 3 | `git push`（推送本分支） | **尚未發生** | 分支無上游、無 `refs/remotes/origin/…`、reflog 無推送紀錄 |
| 4 | `gh pr create`（開 PR） | **尚未發生** | 同上；本次盲跑不做任何對外呼叫 |
| 5 | `gh pr merge`（合併 PR） | **尚未發生** | 依 intent，這一步在你口頭同意後由 agent 執行 |
| 6 | 兩次盲跑期間的 `git clone`、`git worktree add`、`git remote set-url`、`git log / status / diff / reflog / for-each-ref / rev-parse`，以及三個拋棄式 repo 的 `git init / add / commit / switch` | **agent**（本盲跑者） | 全部在暫存目錄執行，見附錄 |
| 7 | 本報告的兩次 commit | **agent**（本盲跑者） | commit 訊息帶同樣兩行署名 |

**到目前為止，沒有任何 git 或 gh 指令被交給你執行。** 界線：第 1 列我無法從 repo 判定執行者；第 3、4、5 列尚未發生。

**結論：成立。**

---

### 第 8 條 — 既有測試全部通過

**這一條是這次盲跑唯一出現過失敗的地方，必須完整交代。**

**在團隊要我複跑的 `057d0c43` 上：失敗。** 我跑 repo 自己宣告的整包測試指令，**結束碼 1**：

```
1 failed, 2097 passed, 2 skipped, 1 xfailed in 61.17s
FAILED loom-code/scripts/test_adversarial_blocked_publish_routes.py::test_probe_hook_refusal_is_one_block_line_per_failure
[XPASS(strict)] FINDING F12: …
```

白話說明這是什麼：對抗測試裡可以把一項標成「我知道這一項現在會失敗，這是已知缺陷」。這種標記設成了嚴格模式——**一旦那項測試開始通過，框架就會把它判為失敗**，用意是逼人在缺陷修好時把標記拿掉。`41cbcf1b` 把 F12 這個缺陷修好了，但標記沒有跟著拿掉，於是整包測試變紅。而整包測試的執行器在第一個測試群失敗後就停住，後面的測試群那一次完全沒有跑到。

**在目前的 `fc5b8401` 上：通過。** `3635c03f` 與 `fc5b8401` 兩個 commit 把標記清掉了。我重跑同一個指令：

```
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

**結束碼 0**。loom-code 主測試群 **2100 passed, 2 skipped**（沒有任何預期失敗項），其餘 12 個 pytest 群全綠，另有 17 個獨立檢查腳本全部 `0 FAIL`。整份輸出裡沒有任何一行 `FAIL`、`FAILED`、`failed` 或 `XPASS`。

**結論：在 `fc5b8401` 上成立；在 `057d0c43` 上不成立。** 如果你接受的是 `fc5b8401`，這一條通過。

---

## 5. 逐條結果一覽

| 條號 | 內容摘要 | 結果（`fc5b8401`） | 與第一次盲跑相比 |
|---|---|---|---|
| 1 | 發佈被擋時指出合法的路 | **成立** | 相同；訊息從一種結尾變成四種，四種都經實跑 |
| 2 | 合併被擋時同樣資訊 | **成立** | 相同 |
| 3 | 站的說明文件寫明不得交還指令 | **成立** | 相同；多了「沒有補救就停住」 |
| 4 | 跳站確認後完整發佈並揭露 | **部分未觀察** | 大致相同，但 (c) 這次有真實觀察，比第一次更完整 |
| 5 | 本次變更的推送／開 PR／合併由 agent 執行 | **部分未觀察** | 相同；commit 數 18 → 24 |
| 6 | 閘門沒有一條規則被放寬 | **成立** | 相同；新增的參數名單是收緊 |
| 7 | 報告逐一具名執行者 | **成立** | 相同 |
| 8 | 既有測試全過 | **成立** | **不同**：`057d0c43` 上失敗，`fc5b8401` 上通過 |

---

## 6. 關於「建置前審查」

spec 的開頭欄位現在寫的是 **`required — owed and not run`**——意思是：這個變更**應該**在動手寫程式之前先做一次審查，但**那次審查沒有做**。

當初寫 spec 時判定不需要，理由是「整個變更只是一串拒絕訊息加上鎖住它的測試，沒有任何對外契約改變形狀」。實際做出來的東西超出了這兩句：它在攔截程式的開 PR 路線裡加了新的拒絕點、加了會讀檔的 PR 內文讀取器、還加了一份只允許名單內參數的規則——而「攔截程式接受哪些開 PR 指令」是每個採用這套流程的 repo 都依賴的對外契約。

**這對你的意義**：這個變更缺一道原本該有的事前檢查。補上它位置的是分支結束時的那次 closing review，而那次審查正是自己從差異重新算出這個結論的。我這份報告沒有任何地方宣稱這個變更在動手前被審查過。

---

## 7. 目前的已知限制：三項，另有一則不計入的提醒

我對照目前的對抗測試模組逐項重新清點，不是沿用第一次盲跑那張清單。結果是**三項**。

第一次盲跑列的四項裡，「內容已經進主線的分支會卡在審查站」那一項**已經不存在了**，理由寫在第 2 節。剩下三項都還在，我逐一實跑確認過。

每一項都寫成三段：**你會看到什麼**、**這代表什麼**、**該怎麼做**。

### L1 — 攔截程式看的是它當下讀到的 PR 內文，不是 PR 最後真正收到的內文

- **你會看到什麼**：**看不到任何徵兆。** 這一點按其構造就是不可見的。
- **這代表什麼**：攔截程式在檢查開 PR 指令的那一刻讀一次 PR 內文檔，`gh` 之後會再讀一次。任何在這兩次讀取之間改寫這個檔案的行為，攔截程式都看不到。
- **該怎麼做**：把攔截程式的放行理解成「這份內文在被檢查的那一刻是誠實的」這項證據，不要理解成對最終 PR 內容的保證。`loom-code/skills/ship/SKILL.md` 第 3 節已經寫明這件事。對應的測試：`test_probe_body_can_change_between_the_check_and_the_request`。

### L2 — 系統提供給你的跳站確認，在你的 session 裡有可能根本記不下來

- **你會看到什麼**：agent 提出跳站提案，你打了 `/loom-code:expert-mode <代號>`（Codex 上是 `$expert-mode <代號>`），但 `loom_checker.py selection show <變更代號>` 仍然回報 `"bound": false`。
- **這代表什麼**：確認只有在「有人在旁的使用者，在提出這個提案的同一個 session 裡親手打出來」時才會生效。巢狀的無人值守執行、在後來的 session 裡才打的確認、以及沒有擷取輸入提示能力的執行環境，這三種情況都會讓這條路是死的。而且沒有任何東西會事先告訴你這條路通不通。
- **該怎麼做**：改走第一條路——跑審查站，它不需要任何確認，在任何 session 都能走。這個限制的代價是白打一次字。對應的測試：`test_probe_route_two_condition_is_not_self_evaluable`、`test_probe_route_two_really_is_unavailable_there`。

### L3 — 非常大的 PR 內文檔會被整份讀進攔截程式

- **你會看到什麼**：開 PR 的那個工具呼叫停在那裡不動。
- **這代表什麼**：攔截程式會擋掉具名管道、裝置檔與讀不到的路徑，但任何讀得到的一般檔案都會被整份讀進來，沒有大小上限。
- **該怎麼做**：讓 PR 內文保持是一份文件，不要拿它當資料檔。路徑是 agent 自己指定的，過程中沒有任何東西被發佈出去，所以代價只是一個卡住的工具呼叫。對應的測試：`test_probe_body_read_has_no_size_ceiling`。

### 另外一則：不是限制，是給日後改這份文件的人的提醒

對抗測試模組裡還有第四則被記下來的東西，但它**不是你使用這套流程時會遇到的限制**，所以我沒有把它算進上面三項。

有一項測試負責確保 ship 站那句規則不會承諾「檢查程式不一定會指名的路」。這項測試只讀破折號（`—`）前面那半句，所以一句寫在破折號後面的無條件承諾，它看不見。實際使用時看不到任何徵兆，也不影響任何發佈行為。它的意義只有一個：日後有人改動 ship 站那句規則時，不要以為那項測試會攔下錯誤的承諾，破折號後面的字要人自己讀過。對應的測試：`test_probe_scoping_dash_hides_a_promise_placed_after_it`。

---

## 8. 附錄：實際執行的指令與原始輸出

以下指令與輸出未經翻譯、未經整理。除特別標示外，工作目錄為乾淨 clone（`fc5b8401`）。

### A. 建立乾淨環境

```console
$ git clone --no-hardlinks --branch fix/2026-09-18-blocked-publish-names-the-legal-routes /Users/kouko/GitHub/loom-plugins …/scratchpad/blindrun3
Cloning into '…/scratchpad/blindrun3'...
done.

$ git log --oneline -1
fc5b8401 docs(loom-code): record that the adversarial module carries no marker

$ ls docs/loom/2026-09-18-blocked-publish-names-the-legal-routes/
blind-run-report.md
plan.md
spec.md
（沒有 attestation.json）

$ git remote set-url origin https://github.com/blindrun-sandbox/loom-plugins.git
```

### B. 第 1 條，狀態一：有工作、沒有驗證紀錄

```console
$ python3 loom-code/scripts/loom_checker.py push
BLOCK push.attestation: branch must carry exactly one generated attestation; found 0; two legal routes, both run by the agent: run the closing-review station, which generates the attestation and needs no confirmation, so it is open in every session; or, in a session that can record a confirmation the user types and only once per change, because expert-mode allows the agent one skip proposal per change, propose a step selection (`loom_checker.py selection propose <change-id> --origin agent --skip reviewers`) that the user confirms by typing `/loom-code:expert-mode <code>` (Codex: `$expert-mode`) with the code the proposal printed, after which finalize-review drops the reviewer floor to zero and still emits an attestation recording the skip; never hand the blocked publication command to the user to run
EXIT=1

$ python3 loom-code/scripts/loom_checker.py publish --confirm-authorized --title "fix(loom-code): blocked publication names the legal routes" --body-file …/body.md
（與上面 push 的那一行逐字相同）
EXIT=1
```

### C. 第 1 條，狀態二：分支相對基準沒有任何新東西，而基準已有驗證紀錄

```console
$ cd …/scratchpad/cases/nothing-to-publish
$ python3 …/blindrun3/loom-code/scripts/loom_checker.py push
BLOCK push.attestation: branch must carry exactly one generated attestation; found 0; this branch adds nothing to its base and the base already attests a change, so there is no unattested work here to review and nothing to publish: neither route out of a missing attestation applies, and the change you mean to publish starts from a new intent on its own branch; never hand the blocked publication command to the user to run
EXIT=1
```

### D. 第 1 條，狀態三：一個分支裡有兩份驗證紀錄

```console
$ cd …/scratchpad/cases/two-attestations
$ python3 …/blindrun3/loom-code/scripts/loom_checker.py push
BLOCK push.attestation: branch must carry exactly one generated attestation; found 2; a publication covers exactly one change, so neither route out of a missing attestation applies here: the branch delta has to end at one attested change first, by landing the other changes from their own branches or by taking their attestations out of this delta; never hand the blocked publication command to the user to run
EXIT=1
```

### E. 第 1 條，狀態四：數量讀不出來（非真實指令觀察，直接呼叫決定結尾的函式）

```console
$ python3 -c "import sys; sys.path.insert(0,'loom-code/scripts'); from loom_checker.command_handlers.push import publication_advice; print('found=None ->' + publication_advice(None))"
found=None ->; the attestation count could not be read here, so nothing is claimed about it and no route out is named: read it with `loom_checker.py push` in the repository, which always reports a count, and take what that refusal names; never hand the blocked publication command to the user to run
```

### F. 第 2 條：合併指令

```console
$ python3 loom-code/scripts/loom_checker.py land --accepted-by kouko
BLOCK land.merge: branch must carry exactly one attested change; found 0; two legal routes, both run by the agent: … (Codex: `$expert-mode`) … never hand the blocked publication command to the user to run
EXIT=1

$ cd …/scratchpad/cases/two-attestations
$ python3 …/blindrun3/loom-code/scripts/loom_checker.py land --accepted-by kouko
BLOCK land.merge: branch must carry exactly one attested change; found 2; a publication covers exactly one change, … never hand the blocked publication command to the user to run
EXIT=1

$ cd …/scratchpad/cases/nothing-to-publish
$ python3 …/blindrun3/loom-code/scripts/loom_checker.py land --accepted-by kouko
BLOCK land.merge: branch must carry exactly one attested change; found 0; this branch adds nothing to its base … never hand the blocked publication command to the user to run
EXIT=1
```

### G. 第 3 條：ship 站說明文件

```console
$ sed -n '119,129p' loom-code/skills/ship/SKILL.md
The command verifies exactly one branch attestation, its schema, content
digest, execution identities/results, reviewer verdicts, and live HEAD. It
then derives the origin repository, default base, current branch, and exact
refspec; performs a non-forced push; and opens or reuses one PR. Do not run a
separate attestation preflight, construct Git push or PR-create commands, or
hand a refused publication command to the user to run; where a refusal names a
remedy, take it, and where it names none, report the refusal and stop — where
the branch attests nothing, the remedy is one of two routes: run the
closing-review station, which generates the attestation, or propose a step
selection the user confirms by typing `/loom-code:expert-mode <code>`
(Codex: `$expert-mode`) with the code the proposal printed.

$ grep -rn "gate:" loom-code/skills/ship/SKILL.md
（無輸出，結束碼 1）
```

### H. 第 4 條：提出跳站提案，以及 agent 無法自行建立確認

```console
$ python3 loom-code/scripts/loom_checker.py selection propose 2026-09-18-blocked-publish-names-the-legal-routes --origin agent --skip reviewers
change: 2026-09-18-blocked-publish-names-the-legal-routes  code: 7SHT
spec           run
plan           run
implementer    run
tdd            run
reviewers      skip
adversarial    run
blind-run      run
package-tests  run
EXIT=0

$ python3 loom-code/scripts/loom_checker.py selection capture --hook < …/prompt-payload.json
PreToolUse:Bash hook error: BLOCK selection.guard: the selection capture command runs only from the prompt hook

$ cat …/.git/loom/selections/2026-09-18-blocked-publish-names-the-legal-routes.jsonl
PreToolUse:Bash hook error: BLOCK selection.guard: names the selection record store

$ python3 loom-code/scripts/loom_checker.py selection show 2026-09-18-blocked-publish-names-the-legal-routes
{
  "change_id": "2026-09-18-blocked-publish-names-the-legal-routes",
  "bound": false,
  "run": ["spec","plan","implementer","tdd","reviewers","adversarial","blind-run","package-tests"],
  "skip": [],
  "code": null,
  "failures": []
}
EXIT=0
```

### I. 第 4 條：確認之後的整條路（repo 自己的對抗測試，在拋棄式 repo 裡真的走一次）

```console
$ python3 -m pytest loom-code/scripts/test_adversarial_blocked_publish_routes.py -v -k "named_proposal or route_two"
test_probe_named_proposal_drops_the_reviewer_floor PASSED
test_probe_named_proposal_without_the_skip_does_not_drop_the_floor PASSED
test_probe_route_two_really_is_unavailable_there[a nested unattended session-S1-S1-0] PASSED
test_probe_route_two_really_is_unavailable_there[a confirmation typed in a later session-S1-S2-1] PASSED
test_probe_refusal_names_route_two_only_where_it_can_be_taken PASSED
test_probe_route_two_condition_is_not_self_evaluable PASSED
test_probe_route_one_survives_where_route_two_does_not PASSED
```

### J. 第 4 條：發佈行為與送出的 PR 內文

```console
$ python3 …/observe_a4.py …/blindrun3
exit code: 0
stderr: ''
--- external commands the publication executed, in order ---
/usr/local/bin/gh repo view github.com/example/project --json defaultBranchRef --jq .defaultBranchRef.name
/usr/bin/git -C /…/repo ls-remote --heads origin refs/heads/feature
/usr/bin/git -C /…/repo push --no-follow-tags --recurse-submodules=no -u --no-verify origin 55a6ef243845e837d024fcac692349ccd8152af9:refs/heads/feature
/usr/bin/git -C /…/repo ls-remote --heads origin refs/heads/feature
/usr/local/bin/gh api --hostname github.com repos/example/project/pulls?state=open&head=example%3Afeature
/usr/bin/git -C /…/repo ls-remote --heads origin refs/heads/feature
/usr/local/bin/gh pr create --base main --head feature --title feat(loom): safe --body-file /…/pr-body.md
/usr/bin/git -C /…/repo ls-remote --heads origin refs/heads/feature
/usr/local/bin/gh pr checks https://github.com/example/project/pull/1 --required --json name,state,bucket
--- the PR body that was published ---
…
## Verification
Skipped steps: adversarial — authority: user-typed (AB2C, 2026-09-13)
Skipped steps: reviewers, adversarial — authority: user-typed (QRST, 2026-09-14)
Prior failure: reviewers finalize.verdicts 2026-09-12
Prior failure: finalize finalize.digest 2026-09-13
Focused race and contract regressions pass.
…
```

（`observe_a4.py` 位於暫存目錄，不在 repo 內。它匯入 repo 自己的測試模組 `test_loom_publish`，呼叫其中既有的 `selected_publication` 骨架，只是把結果印出來。）

### K. 第 4、6 條：開 PR 的參數名單

```console
$ python3 …/observe_hook.py …/blindrun3/loom-code/scripts
### allowlisted options only
exit: 2
BLOCK push.attestation: remote branch 'feature' must already equal reviewed HEAD a08428f058443222ecdd803594b13446edc4f781

### plus --label
exit: 2
BLOCK push.attestation: PR creation must use the canonical trusted-gh command from loom-code:ship

### plus --assignee
exit: 2
BLOCK push.attestation: PR creation must use the canonical trusted-gh command from loom-code:ship
```

（`observe_hook.py` 位於暫存目錄。它在一個拋棄式 git repo 上呼叫受測分支的攔截程式，餵給它與正式運作時一樣形狀的 JSON。）

### L. 第 6 條：沒有綁定跳站時的審查站，與規則清單比對

```console
$ python3 loom-code/scripts/loom_checker.py finalize-review 2026-09-18-blocked-publish-names-the-legal-routes --input …/review-input.json
BLOCK finalize.verdicts: review input has no verdicts
EXIT=1

$ diff rules-base.txt rules-branch.txt        # 分岔點 8b346852 vs fc5b8401
DIFF_EXIT=0                                   # 完全相同，各 25 條

$ git diff 8b346852..fc5b8401 -- loom-code/scripts/ | grep -E "^-" | grep -vE "^---" | grep -E "assert|return \[|report\(|raise "
-    assert not err.getvalue().startswith(FOUND_ZERO)
（唯一一行，替換成更嚴格的 `assert "found 0" not in err.getvalue()`）
```

### M. 第 6 條：對抗測試

```console
$ python3 -m pytest loom-code/scripts/test_adversarial_blocked_publish_routes.py -q -rxX
98 passed in 41.29s
（沒有任何 xfail／xpass）
```

### N. 第 8 條：整包測試，在 `057d0c43` 上（失敗）

```console
$ uv run --isolated --offline --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
EXIT=1

=================================== FAILURES ===================================
____________ test_probe_hook_refusal_is_one_block_line_per_failure _____________
[XPASS(strict)] FINDING F12: the hook route emits a refusal whose reason contains a newline, so stderr carries a line with no `BLOCK ` prefix …
=========================== short test summary info ============================
FAILED loom-code/scripts/test_adversarial_blocked_publish_routes.py::test_probe_hook_refusal_is_one_block_line_per_failure
1 failed, 2097 passed, 2 skipped, 1 xfailed in 61.17s (0:01:01)
（執行器在這一群失敗後停住，後面的測試群那一次沒有跑到）
```

### O. 第 8 條：整包測試，在 `fc5b8401` 上（通過）

```console
$ uv run --isolated --offline --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
EXIT=0

（節錄各測試群的結尾摘要行）
2100 passed, 2 skipped in 52.91s
245 passed, 1 skipped in 1.87s
52 passed in 7.08s
195 passed in 2.15s
261 passed in 9.37s
121 passed in 0.29s
64 passed in 11.94s
43 passed in 0.11s
13 passed in 0.03s
1 passed in 0.01s
80 passed, 3 skipped in 1.87s
204 passed, 5 skipped in 0.49s
12 passed in 0.03s
Summary: 9 PASS / 0 FAIL
Summary: 13 PASS / 0 FAIL
Summary: 5 PASS / 0 FAIL
Summary: 2 PASS / 0 FAIL
Summary: 5 PASS / 0 FAIL
Summary: 2 PASS / 0 FAIL
Summary: 15 PASS / 0 FAIL
Summary: 21 PASS / 0 FAIL
Summary: 12 PASS / 0 FAIL
Summary: 12 PASS / 0 FAIL
Summary: 11 PASS / 0 FAIL
Summary: 6 PASS / 0 FAIL
Summary: 5 PASS / 0 FAIL
Summary: 5 PASS / 0 FAIL
Summary: 5 PASS / 0 FAIL
Summary: 6 PASS / 0 FAIL
Summary: 11 PASS / 0 FAIL

$ grep -cE "^FAIL|FAILED|[1-9][0-9]* failed|XPASS" package-tests-3.log
0
```

### P. 第 5、7 條：commit 署名與推送狀態

```console
$ git rev-list --count main..HEAD
24

$ git log --format='%h %(trailers:key=Co-Authored-By,valueonly)' main..HEAD | grep -v "Claude Opus 5"
（無輸出：24 個 commit 沒有一個缺少 agent 署名）

$ git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
fatal: no upstream configured for branch 'fix/2026-09-18-blocked-publish-names-the-legal-routes'

$ git for-each-ref --format='%(refname)' 'refs/remotes/origin/*2026-09-18*'
（無輸出）

$ git reflog -n 40 'fix/2026-09-18-blocked-publish-names-the-legal-routes' | grep -ci "update by push"
0

$ git branch -vv | grep 2026-09-18
* fix/2026-09-18-blocked-publish-names-the-legal-routes fc5b8401 docs(loom-code): record that the adversarial module carries no marker
（沒有上游標記，代表從未推送）
```
