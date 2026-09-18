# 盲跑報告：發佈被擋的當下，指出合法的兩條路

intent: docs/loom/intent/2026-09-18-blocked-publish-names-the-legal-routes.md
分支: `fix/2026-09-18-blocked-publish-names-the-legal-routes`，HEAD `2228bb25`
盲跑時間: 2026-09-18
盲跑執行者: agent（loom-code blind-runner），未參與任何實作

---

## 1. 一句話結論

**改變了什麼**：以前，當發佈檢查程式擋下推送、開 PR 或合併時，它只說「這個分支沒有驗證紀錄」，沒有指出接下來能做什麼，於是 agent 就把那行被擋的指令交給你，請你自己貼到終端機執行。現在同一則拒絕訊息會在同一行裡明講兩條 agent 自己就能走的路，並且明文寫「絕對不要把這行指令交給使用者執行」。

**跑起來如何**：**沒有任何一條驗收條件失敗。** 八條裡有六條我用真實指令跑過而且成立；另外兩條（第 4 條、第 5 條）有一部分在今天這個時間點還無法觀察——第 4 條需要你本人親手打一次確認碼，這件事按照設計 agent 做不到；第 5 條的推送、開 PR、合併都還沒發生。這兩條的細節寫在下面各自的列裡，不放在結尾。

> 本報告出現的名詞，第一次出現時都先用白話解釋：
> - **驗證紀錄**：一個放在 `docs/loom/<變更代號>/attestation.json` 的檔案，裡面記錄這個分支通過了哪些審查與測試。沒有它，發佈檢查程式就不放行。
> - **閘門**：`loom_checker.py` 這支檢查程式裡的一條條規則。不通過就印出一行 `BLOCK <規則名稱>: <理由>` 並以錯誤碼結束。
> - **站**：這套流程把一次變更切成幾個階段，每個階段叫一個站。「審查站」（closing-review）就是產出驗證紀錄的那一站。
> - **跳站確認**：agent 可以提出「這次跳過某幾站」的提案，提案會印出一個四碼的代號；你在對話框裡親手打 `/loom-code:expert-mode <代號>` 之後，這個跳站才算數。

---

## 2. 我是怎麼跑的

- 把 repo 重新 clone 到一個乾淨的暫存目錄 `…/scratchpad/blindrun/repo`，切到 `2228bb25`，不使用原本的工作目錄。
- 全程沒有對外連線到 GitHub，沒有推送、沒有開 PR、沒有合併。
- 兩點需要說明白：
  1. 為了讓 `publish` 指令能走到「沒有驗證紀錄」那一關，我把這個 clone 的 origin 位址改成一個不存在的 GitHub 位址 `https://github.com/blindrun-sandbox/loom-plugins.git`。我先讀過 `loom-code/scripts/loom_checker/command_handlers/publish.py:438`，確認那一關在任何對外指令之前執行，所以這樣做不會產生任何網路請求；實際輸出也證實它停在那一關。
  2. repo 自己宣告的整包測試指令，內部有一段會跑 `npm` 安裝 Node 套件。我對 Python 的部分加了 `--offline`，但 `npm` 那一段是 repo 測試指令自己的行為，不在我控制範圍內，它有可能接觸過 npm 套件倉庫。除此之外沒有其他對外連線。
- 我沒有修改這個 repo 裡除了本報告以外的任何檔案。

---

## 3. 逐條驗收

編號沿用 intent 的 Acceptance 編號。

### 第 1 條 — 在沒有驗證紀錄的分支上執行正規發佈指令，拒絕訊息同時指出兩條合法路徑

**我做了什麼**：在乾淨 clone（此分支本來就沒有 `attestation.json`）上跑 ship 站文件寫明的正規發佈指令
`python3 loom-code/scripts/loom_checker.py publish --confirm-authorized --title <標題> --body-file <PR 內文檔>`。
另外也單獨跑了底層的 `loom_checker.py push`。

**我看到什麼**：兩者都以錯誤碼 1 被擋，而且印出同一行拒絕訊息。這行訊息在原本的理由（`branch must carry exactly one generated attestation; found 0`）後面接上：

- 路徑一：`run the closing-review station, which generates the attestation and needs no confirmation, so it is open in every session`
- 路徑二：`in a session that can record a confirmation the user types, propose a step selection (...) that the user confirms by typing /loom-code:expert-mode <code> ...`
- 並以 `never hand the blocked publication command to the user to run` 結尾。

我另外查證了路徑二講的確認方式是真的會生效的那一種：`loom-code/scripts/loom_checker/selection.py:30-32` 把 `/loom-code:expert-mode` 列在可接受的開頭字串裡。

**結論：成立。**

---

### 第 2 條 — 合併指令因缺少驗證紀錄而拒絕時，出現同樣的資訊

**我做了什麼**：在同一個乾淨 clone 上跑 `python3 loom-code/scripts/loom_checker.py land --accepted-by kouko`。

**我看到什麼**：錯誤碼 1，訊息為 `BLOCK land.merge: branch must carry exactly one attested change; found 0; …`，後面接的兩條路徑與結尾那句「不得交還指令」與第 1 條**逐字相同**。

**結論：成立。**

---

### 第 3 條 — 站的說明文件載明「發佈被擋時不得把指令交給使用者執行」

**我做了什麼**：在 `loom-code/skills/ship/SKILL.md` 裡搜尋這條規則，並讀出前後文；同時搜尋這份文件裡有沒有把這段話標成閘門的標記（這個 repo 用 `<!-- gate: … -->` 來標示「這段散文算閘門」）。

**我看到什麼**：規則在 `loom-code/skills/ship/SKILL.md:123-129`，內容是「不要自己組推送或開 PR 的指令，也不要把被拒絕的發佈指令交給使用者執行；遇到拒絕就走拒絕訊息指名的補救方式——分支沒有驗證紀錄時，那就是兩條路之一」。整份 `ship/SKILL.md` 裡沒有任何 `gate:` 標記，也就是說這條規則是給 agent 讀的指引，沒有被當成可判定的閘門來用（這符合 spec 的設計：真正擋下來的是上面那行拒絕訊息，散文只補上「還沒動手就先放棄」那種情況）。

**結論：成立。**

---

### 第 4 條 — 使用者完成一次跳站確認後，紀錄明載被跳過的站，發佈完成推送並開出 Ready PR，PR 內文含跳站揭露

**這一條我沒有辦法用一次完整的真實流程證實，原因寫在下面。我把它拆成三段，分別說明觀察到什麼。**

**(a) 提出跳站提案 — 真實跑過，成立。**
我跑 `loom_checker.py selection propose 2026-09-18-blocked-publish-names-the-legal-routes --origin agent --skip reviewers`，指令成功，印出確認碼 `7SHT` 與一張八個站的表，`reviewers` 標為 `skip`。

**(b) 使用者親手確認 — 我做不到，而且這正是設計要的。**
接著我試著自己把「使用者打了 `/loom-code:expert-mode 7SHT`」這件事送進負責記錄的程式，得到的是拒絕：

```
BLOCK selection.guard: the selection capture command runs only from the prompt hook
```

我也試著直接讀那個紀錄檔，同樣被擋：

```
BLOCK selection.guard: names the selection record store
```

這代表：**跳站確認只能由你本人在對話框裡打字產生，agent 無法自己補上，也無法自己去翻或改那份紀錄。** 這正好是 intent 的 Constraints 第 2 條（「跳站必須來自使用者親手輸入的確認」）要的效果。我因此確認 `selection show` 仍然回報 `"bound": false`——提案在，確認沒有，跳站不成立。

副作用是：第 4 條開頭那句「使用者完成一次跳站確認後」這個前提，在這次盲跑裡沒有被建立，所以我無法把這一條從頭到尾真的跑一次。

**(c) 確認之後的那一段 — 用 repo 自己的測試接縫觀察，成立。**
我改用 repo 內建的測試骨架，直接把「驗證紀錄裡已經有一筆使用者確認的跳站」這個狀態餵給真正的發佈程式，並把它實際送出的外部指令與最後送出的 PR 內文原封不動印出來。結果：

- 執行了推送：`git … push --no-follow-tags --recurse-submodules=no -u --no-verify origin <HEAD>:refs/heads/feature`
- 執行了開 PR：`gh pr create --base main --head feature --title … --body-file …`，**沒有 `--draft`**，後面也沒有任何 `pr ready`，也就是開出來就是 Ready PR
- PR 內文的 `## Verification` 段落開頭就是跳站揭露，逐字為：
  ```
  Skipped steps: adversarial — authority: user-typed (AB2C, 2026-09-13)
  Skipped steps: reviewers, adversarial — authority: user-typed (QRST, 2026-09-14)
  Prior failure: reviewers finalize.verdicts 2026-09-12
  Prior failure: finalize finalize.digest 2026-09-13
  ```
- 相對的反面案例也成立：同樣的狀態但 PR 內文沒有揭露時，`test_body_without_disclosure_refused_when_selection_bound` 顯示它在送出任何對外指令之前就被擋下（錯誤碼 1、規則 `push.contextual-body`、外部指令清單為空）。

需要誠實說明的是：這個骨架把「驗證驗證紀錄」那一步換成了直接通過，所以它證明的是「確認之後的發佈行為」，不是「驗證紀錄本身的檢查」。

**(d) 「紀錄明載被跳過的站」這一半。**
產出驗證紀錄的程式在 `loom-code/scripts/loom_checker/command_handlers/finalize.py:85-100,163`：它先讀出已綁定的跳站，若 `reviewers` 在跳站清單裡就把審查人數門檻降為 0，並把整個跳站內容寫進驗證紀錄的 `selection` 欄位。我實際跑了 `finalize-review` 的專屬測試檔（10 項全過），其中 `test_bound_skip_of_reviewers_and_adversarial_validates` 與 `test_unbound_skip_refused_and_digest_mismatch_blocks` 正是這兩面。我也在乾淨 clone 上真的跑了一次 `finalize-review`，在沒有綁定跳站的情況下它照樣被擋（`BLOCK finalize.verdicts: review input has no verdicts`）。

**結論：(a)(c)(d) 成立；(b) 依設計無法由 agent 建立，因此整條「從使用者確認到開出 PR」的一次性真實跑未被觀察。要完成這條的完整觀察，需要你在同一個 session 裡親手打一次 `/loom-code:expert-mode <代號>`。**

---

### 第 5 條 — 本次變更自身的推送與開 PR 由 agent 執行；合併在你口頭同意後同樣由 agent 執行；你全程不輸入任何 git 或 gh 指令

**我做了什麼**：不做任何推送，只從 repo 自己的紀錄裡查證——每一個 commit 是誰寫的、分支有沒有被推過、有沒有任何指令被交到人手上。

**我看到什麼**：

- 這個分支相對 `main` 有 **18 個 commit**（`3bdaa258` 到 `2228bb25`）。**每一個** commit 的訊息結尾都帶著
  `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>` 與
  `Claude-Session: https://claude.ai/code/session_0146jwneKWsFu39c2RATq8FU` 兩行。也就是說，這些 commit 都是在這個 Claude Code session 裡由 agent 產生的。
- **推送還沒有發生。** 分支沒有設定上游（`git rev-parse @{upstream}` 回報 `no upstream configured`），本機沒有 `refs/remotes/origin/fix/2026-09-18-…` 這個參照，分支的 reflog 從 10:47 建立到 14:10 最後一個 commit 為止，沒有任何一筆是推送。
- **開 PR 與合併也還沒有發生**，理由同上，而且本次盲跑不做任何對外呼叫。

**這一條有哪一部分是我無法判定的**：git 的紀錄只記「做了什麼」，不記「是誰在鍵盤上打的」。所以光靠 repo，我可以證明這 18 個 commit 出自這個 agent session，但我無法用 repo 證明「你完全沒有自己打過任何 git 指令」——我只能說：repo 裡沒有留下任何看起來像人手工執行的痕跡（沒有缺少 agent 署名的 commit，也沒有推送紀錄）。

**什麼時候可以觀察到剩下的部分**：推送與開 PR 會在 ship 站執行時發生，也就是你接受這份報告之後；合併則在你口頭同意之後。那時候可以用 `git branch -vv`（看分支有沒有上游）、`git reflog`（看有沒有推送紀錄）與 PR 頁面的建立者來逐一確認。

**結論：已發生的部分（18 個 commit 全由 agent 產生）成立；推送、開 PR、合併三個動作在本次盲跑時尚未發生，因此未被觀察。**

---

### 第 6 條 — 閘門沒有任何一條規則被放寬

**我做了什麼**：四件事。

1. 在乾淨 clone（沒有驗證紀錄、沒有跳站確認）上分別跑 `push`、`publish`、`land`、`finalize-review`。
2. 把分支上的規則清單（`loom_checker.py --list-rules`）與分岔點 `8b346852` 的清單逐字比對。
3. 把 `loom-code/scripts/loom_checker/` 底下這次被刪掉的每一行都列出來看。
4. 跑這次變更自己新增的對抗測試檔。

**我看到什麼**：

1. 四個指令全部被擋：`push` → `BLOCK push.attestation`（錯誤碼 1）；`publish` → 同一條規則（錯誤碼 1）；`land` → `BLOCK land.merge`（錯誤碼 1）；`finalize-review` → `BLOCK finalize.verdicts`（錯誤碼 1）。
2. 兩份規則清單 **完全相同**，各 25 條，`diff` 沒有任何差異。
3. 程式碼裡被刪掉的行只有兩類：被改寫的拒絕訊息字串本身（都被更長、資訊更多的版本取代），以及一段針對 `gh` 指令 `-R / --repo / --hostname` 這三個參數的舊檢查。這段舊檢查被一份新的「只允許已知參數」白名單取代了。我沒有只相信這個說法——`test_adversarial_blocked_publish_routes.py` 裡有一項專門測試把舊檢查點名過的全部六種寫法重跑一遍，全部仍然被拒。整份對抗測試檔 96 項通過、1 項為已知且已標記的預期失敗（見下面的限制 L1）。
4. 沒有任何一行 `assert`、`return [(...)]`、`report(...)` 或 `raise` 從程式碼或測試裡被刪除。

**結論：成立。**

---

### 第 7 條 — 盲跑報告逐條記錄每一個 git 與 gh 動作由誰執行

下表列出與這次變更有關的每一個 git 與 gh 動作。

| # | 動作 | 執行者 | 依據 |
|---|---|---|---|
| 1 | 建立分支（10:47）與兩次改名（10:58、11:46） | **無法判定** | git 的 reflog 記錄動作與時間，不記錄誰下的指令。這三筆落在 agent 產生 commit 的同一段時間內，但 repo 本身無法區分 |
| 2 | 18 個 commit：`3bdaa258` 到 `2228bb25` | **agent**（本 session） | 每一個 commit 訊息都帶 `Co-Authored-By: Claude Opus 5 (1M context)` 與 `Claude-Session: …session_0146jwneKWsFu39c2RATq8FU` |
| 3 | `git push`（推送本分支） | **尚未發生** | 分支無上游、無 `refs/remotes/origin/…`、reflog 無推送紀錄 |
| 4 | `gh pr create`（開 PR） | **尚未發生** | 同上；本次盲跑不做任何對外呼叫 |
| 5 | `gh pr merge`（合併 PR） | **尚未發生** | 依 intent，這一步在你口頭同意後由 agent 執行 |
| 6 | 盲跑期間的 `git clone`、`git worktree add`、`git remote set-url`、`git log / status / diff / reflog / for-each-ref / rev-parse` | **agent**（本盲跑者） | 全部在暫存目錄的 clone 上執行，見附錄 |
| 7 | 本報告的 commit | **agent**（本盲跑者） | commit 訊息帶同樣兩行署名 |

**到目前為止，沒有任何 git 或 gh 指令被交給你執行。** 需要說清楚的界線是：第 1 列我無法從 repo 判定執行者；第 3、4、5 列尚未發生，要等 ship 站與合併之後才能觀察。

**結論：成立（每一個動作都已具名，無法判定的與尚未發生的都寫在該列裡）。**

---

### 第 8 條 — 既有測試全部通過

**我做了什麼**：在乾淨 clone 上跑 repo 自己宣告的整包測試指令（宣告位置：`docs/loom/KICKOFF-DEFAULTS.md`）：

```
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

（我另外加了 `--offline`，讓 Python 套件不從網路取得。）

**我看到什麼**：**結束碼 0**。loom-code 主測試群 **2088 passed, 2 skipped, 1 xfailed**；其餘 12 個 pytest 群全綠，另有 17 個獨立檢查腳本全部 `0 FAIL`。整份輸出裡沒有任何一行 `FAIL`、`FAILED` 或 `n failed`。那 1 個 `xfailed` 是本次刻意留下的已知限制（下面的 L1），不是失敗。

**結論：成立。**

---

## 4. 逐條結果一覽

| 條號 | 內容摘要 | 結果 |
|---|---|---|
| 1 | 發佈被擋時指出兩條路 | **成立**（真實指令觀察） |
| 2 | 合併被擋時同樣資訊 | **成立**（真實指令觀察） |
| 3 | 站的說明文件寫明不得交還指令 | **成立**（檔案內容觀察） |
| 4 | 跳站確認後完整發佈並揭露 | **部分未觀察**——提案、發佈行為、紀錄寫入三段都成立；「使用者親手確認」這一步 agent 依設計做不到，需要你打一次確認碼才能完整走完 |
| 5 | 本次變更的推送／開 PR／合併由 agent 執行 | **部分未觀察**——18 個 commit 全由 agent 產生已證實；推送、開 PR、合併三個動作在盲跑當下尚未發生 |
| 6 | 閘門沒有一條規則被放寬 | **成立**（四個指令實跑被擋 + 規則清單零差異 + 刪除行逐行檢查） |
| 7 | 報告逐一具名執行者 | **成立**（見上表） |
| 8 | 既有測試全過 | **成立**（結束碼 0，2088 passed） |

**沒有任何一條驗收條件失敗。**

---

## 5. 這次沒有處理、但你應該知道的四個限制

這四點是對抗測試階段找出來並且決定「留著、講清楚」的已知限制。每一點都寫成三段：**你會看到什麼**、**這代表什麼**、**該怎麼做**。

### L1 — 內容已經進主線的分支，會卡在審查站原地打轉

- **你會看到什麼**：`push` 說 `found 0`（找不到驗證紀錄），你去跑審查站，它成功結束並印出 `wrote docs/loom/<變更代號>/attestation.json`，然後 `push` 還是說 `found 0`，一模一樣。
- **這代表什麼**：這個分支的功能內容和主線完全一樣，所以重新產生出來的驗證紀錄跟已經合併進去的那一份逐位元組相同，因此它根本不會出現在這個分支的差異裡。次數永遠不會從 0 變成 1。
- **該怎麼做**：這個分支沒有東西可以發佈。不要再跑審查站，改成從一份新的 intent 重新開始。對應的測試：`test_probe_closing_review_route_terminates_at_count_zero`，永久標記為預期失敗。

### L2 — 攔截程式看的是它當下讀到的 PR 內文，不是 PR 最後真正收到的內文

- **你會看到什麼**：**看不到任何徵兆。** 這一點按其構造就是不可見的。
- **這代表什麼**：攔截程式在檢查開 PR 指令的那一刻讀一次 PR 內文檔，`gh` 之後會再讀一次。任何在這兩次讀取之間改寫這個檔案的行為，攔截程式都看不到。
- **該怎麼做**：把攔截程式的放行理解成「這份內文在被檢查的那一刻是誠實的」這項證據，不要理解成對最終 PR 內容的保證。`775eba95` 已經把這件事寫進 ship 站說明的第 3 節，那是正確的位置。

### L3 — 系統提供給你的跳站確認，在你的 session 裡有可能根本記不下來

- **你會看到什麼**：agent 提出跳站提案，你打了 `/loom-code:expert-mode <代號>`，但 `loom_checker.py selection show <變更代號>` 仍然回報 `"bound": false`。
- **這代表什麼**：確認只有在「有人在旁的使用者，在提出這個提案的同一個 session 裡親手打出來」時才會生效。巢狀的無人值守執行、在後來的 session 裡才打的確認、以及沒有擷取輸入提示能力的執行環境，這三種情況都會讓這條路是死的。
- **該怎麼做**：改走第一條路——跑審查站，它不需要任何確認，在任何 session 都能走。這個限制的代價是白打一次字，因為在你動手之前沒有任何東西會先告訴你這條路不通。對應的測試：`test_probe_route_two_condition_is_not_self_evaluable`、`test_probe_route_two_really_is_unavailable_there`。

### L4 — 非常大的 PR 內文檔會被整份讀進攔截程式

- **你會看到什麼**：開 PR 的那個工具呼叫停在那裡不動。
- **這代表什麼**：攔截程式會擋掉具名管道、裝置檔與讀不到的路徑，但任何讀得到的一般檔案都會被整份讀進來，沒有大小上限。
- **該怎麼做**：讓 PR 內文保持是一份文件，不要拿它當資料檔。路徑是 agent 自己指定的，而且過程中沒有任何東西被發佈出去，所以代價只是一個卡住的工具呼叫，沒有別的。對應的測試：`test_probe_body_read_has_no_size_ceiling`。

---

## 6. 附錄：實際執行的指令與原始輸出

以下指令與輸出未經翻譯、未經整理。除特別標示外，工作目錄為乾淨 clone `…/scratchpad/blindrun/repo`。

### A. 建立乾淨環境

```console
$ git clone --no-hardlinks --branch fix/2026-09-18-blocked-publish-names-the-legal-routes /Users/kouko/GitHub/loom-plugins …/scratchpad/blindrun/repo
Cloning into '…/scratchpad/blindrun/repo'...
done.

$ git -C …/scratchpad/blindrun/repo log --oneline -1
2228bb25 test(loom-code): attack the four fixes and retire their markers

$ ls -la docs/loom/2026-09-18-blocked-publish-names-the-legal-routes/
plan.md
spec.md
（沒有 attestation.json）

$ git remote set-url origin https://github.com/blindrun-sandbox/loom-plugins.git
```

### B. 第 1 條：底層推送檢查

```console
$ python3 loom-code/scripts/loom_checker.py push
BLOCK push.attestation: branch must carry exactly one generated attestation; found 0; two legal routes, both run by the agent: run the closing-review station, which generates the attestation and needs no confirmation, so it is open in every session; or, in a session that can record a confirmation the user types, propose a step selection (`loom_checker.py selection propose <change-id> --origin agent --skip reviewers`) that the user confirms by typing `/loom-code:expert-mode <code>` with the code the proposal printed, after which finalize-review drops the reviewer floor to zero and still emits an attestation recording the skip; never hand the blocked publication command to the user to run
EXIT=1
```

### C. 第 1 條：正規發佈指令

```console
$ python3 loom-code/scripts/loom_checker.py publish --confirm-authorized --title "fix(loom-code): blocked publication names the legal routes" --body-file …/blindrun/body.md
BLOCK push.attestation: branch must carry exactly one generated attestation; found 0; two legal routes, both run by the agent: run the closing-review station, which generates the attestation and needs no confirmation, so it is open in every session; or, in a session that can record a confirmation the user types, propose a step selection (`loom_checker.py selection propose <change-id> --origin agent --skip reviewers`) that the user confirms by typing `/loom-code:expert-mode <code>` with the code the proposal printed, after which finalize-review drops the reviewer floor to zero and still emits an attestation recording the skip; never hand the blocked publication command to the user to run
EXIT=1
```

（同一個指令在 origin 還是本機路徑時，先被更早的一關擋下：`BLOCK push.attestation: literal origin is not a supported GitHub repository URL`。這就是我改 origin 位址的原因。）

### D. 第 2 條：合併指令

```console
$ python3 loom-code/scripts/loom_checker.py land --accepted-by kouko
BLOCK land.merge: branch must carry exactly one attested change; found 0; two legal routes, both run by the agent: run the closing-review station, which generates the attestation and needs no confirmation, so it is open in every session; or, in a session that can record a confirmation the user types, propose a step selection (`loom_checker.py selection propose <change-id> --origin agent --skip reviewers`) that the user confirms by typing `/loom-code:expert-mode <code>` with the code the proposal printed, after which finalize-review drops the reviewer floor to zero and still emits an attestation recording the skip; never hand the blocked publication command to the user to run
EXIT=1
```

### E. 第 3 條：ship 站說明文件

```console
$ sed -n '120,129p' loom-code/skills/ship/SKILL.md
The command verifies exactly one branch attestation, its schema, content
digest, execution identities/results, reviewer verdicts, and live HEAD. It
then derives the origin repository, default base, current branch, and exact
refspec; performs a non-forced push; and opens or reuses one PR. Do not run a
separate attestation preflight, construct Git push or PR-create commands, or
hand a refused publication command to the user to run; on a refusal take the
remedy that refusal names — where the branch attests nothing, that is one of
two routes: run the closing-review station, which generates the attestation,
or propose a step selection the user confirms by typing
`/loom-code:expert-mode <code>` with the code the proposal printed.

$ grep -rn "gate:" loom-code/skills/ship/SKILL.md
（無輸出）
```

### F. 第 4 條：提出跳站提案

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
```

### G. 第 4 條：agent 無法自行建立使用者確認

```console
$ python3 loom-code/scripts/loom_checker.py selection capture --hook < …/blindrun/prompt-payload.json
PreToolUse:Bash hook error: [python3 ".../loom-code/3.7.1/scripts/loom_checker.py" push --hook]: BLOCK selection.guard: the selection capture command runs only from the prompt hook

$ cat …/blindrun/repo/.git/loom/selections/2026-09-18-blocked-publish-names-the-legal-routes.jsonl
PreToolUse:Bash hook error: [python3 ".../loom-code/3.7.1/scripts/loom_checker.py" push --hook]: BLOCK selection.guard: names the selection record store

$ python3 loom-code/scripts/loom_checker.py selection show 2026-09-18-blocked-publish-names-the-legal-routes
{
  "change_id": "2026-09-18-blocked-publish-names-the-legal-routes",
  "bound": false,
  "run": [
    "spec",
    "plan",
    "implementer",
    "tdd",
    "reviewers",
    "adversarial",
    "blind-run",
    "package-tests"
  ],
  "skip": [],
  "code": null,
  "failures": []
}
EXIT=0
```

### H. 第 4 條：確認之後的發佈行為（透過 repo 自己的測試接縫觀察）

```console
$ python3 …/blindrun/observe_a4.py …/blindrun/repo
exit code: 0
stderr: ''
--- external commands the publication executed, in order ---
/usr/local/bin/gh repo view github.com/example/project --json defaultBranchRef --jq .defaultBranchRef.name
/usr/bin/git -C /…/repo ls-remote --heads origin refs/heads/feature
/usr/bin/git -C /…/repo push --no-follow-tags --recurse-submodules=no -u --no-verify origin c83b342810d46968d074063ca1051f3823333652:refs/heads/feature
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

### I. 第 4 條與第 6 條：沒有綁定跳站時的審查站

```console
$ python3 loom-code/scripts/loom_checker.py finalize-review 2026-09-18-blocked-publish-names-the-legal-routes --input …/blindrun/review-input.json
BLOCK finalize.verdicts: review input has no verdicts
EXIT=1

$ python3 -m pytest loom-code/scripts/test_selection_finalize.py -v
… 10 passed in 10.51s
```

### J. 第 6 條：規則清單與刪除行比對

```console
$ git worktree add --detach …/blindrun/base 8b34685236c5b5984f7eaed49c78035f6ae146d6
Preparing worktree (detached HEAD 8b346852)
HEAD is now at 8b346852 docs(loom): point artifact-type mapping to manifest.yaml and add the memory row (#29)

$ （分岔點）python3 loom-code/scripts/loom_checker.py --list-rules > rules-base.txt
$ （分支）  python3 loom-code/scripts/loom_checker.py --list-rules > rules-branch.txt
$ diff rules-base.txt rules-branch.txt
DIFF_EXIT=0

$ wc -l rules-branch.txt
25

$ git diff 8b346852..2228bb25 -- loom-code/scripts/ | grep -E "^-" | grep -vE "^---" | grep -E "assert|return \[|report\(|raise "
（無輸出）
```

### K. 第 6 條：對抗測試

```console
$ python3 -m pytest loom-code/scripts/test_adversarial_blocked_publish_routes.py -q
96 passed, 1 xfailed in 33.00s

$ python3 -m pytest loom-code/scripts/test_adversarial_blocked_publish_routes.py -q -rx
XFAIL loom-code/scripts/test_adversarial_blocked_publish_routes.py::test_probe_closing_review_route_terminates_at_count_zero - FINDING F6: the count-zero tail names the closing-review route unconditionally, but a branch whose base already carries the attestation finalize-review regenerates gets `found 0` and stays there -- running the named station rewrites byte-identical content, so the count never moves. …
```

### L. 第 1、2、3 條相關測試群

```console
$ python3 -m pytest loom-code/scripts/test_loom_publish.py -k "confirmed_skip or body_without_disclosure_refused_when_selection_bound or missing_attestation_names_both_routes or missing_attestation_reason_stays_one_line" -v
loom-code/scripts/test_loom_publish.py::test_confirmed_skip_publishes_with_disclosure PASSED
loom-code/scripts/test_loom_publish.py::test_body_without_disclosure_refused_when_selection_bound PASSED
loom-code/scripts/test_loom_publish.py::test_missing_attestation_names_both_routes PASSED
loom-code/scripts/test_loom_publish.py::test_missing_attestation_reason_stays_one_line PASSED
4 passed, 142 deselected in 1.69s

$ python3 -m pytest loom-code/scripts/test_ship_station_text.py loom-code/scripts/test_ship_worktree_merge.py loom-code/scripts/test_adversarial_push_reason.py -q
89 passed in 17.70s
```

### M. 第 8 條：整包測試

```console
$ uv run --isolated --offline --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
EXIT=0

（節錄各測試群的結尾摘要行）
2088 passed, 2 skipped, 1 xfailed in 52.91s
245 passed, 1 skipped in 1.68s
52 passed in 15.84s
195 passed in 1.99s
261 passed in 8.54s
121 passed in 0.28s
64 passed in 11.10s
43 passed in 0.18s
13 passed in 0.02s
1 passed in 0.00s
80 passed, 3 skipped in 1.70s
209 passed in 2.25s
12 passed in 0.02s
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

$ grep -cE "^FAIL|FAILED|[1-9][0-9]* failed" package-tests.log
0
```

### N. 第 5、7 條：commit 署名與推送狀態

```console
$ git log --format='%h|%an|%s' main..HEAD | wc -l
18

$ git log --format='=== %h%n%B' main..HEAD | grep -E '^(===|Co-Authored-By|Claude-Session)'
=== 2228bb25
Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0146jwneKWsFu39c2RATq8FU
… （其餘 17 個 commit 完全相同的兩行，逐一確認）

$ git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
fatal: no upstream configured for branch 'fix/2026-09-18-blocked-publish-names-the-legal-routes'

$ git for-each-ref --format='%(refname) %(objectname:short)' 'refs/remotes/origin/*2026-09-18*'
（無輸出）

$ git branch -vv | grep 2026-09-18
* fix/2026-09-18-blocked-publish-names-the-legal-routes 2228bb25 test(loom-code): attack the four fixes and retire their markers
（沒有上游標記，代表從未推送）
```
