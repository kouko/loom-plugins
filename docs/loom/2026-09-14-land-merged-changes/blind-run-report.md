# 讓 Loom 自己收尾：等 CI、合併、同步主幹、清掉分支與工作目錄 — 我試了什麼、發生了什麼

Tried on 2026-09-14, in a clean copy at be0cbb36.

**先說清楚這次怎麼試的**：真的去 GitHub 合併一個 PR 不安全，所以 GitHub 那一側是**模擬的**。我寫了一個假的 GitHub，照劇本回答「檢查過了沒、能不能合併、PR 狀態」；收到合併指令時，它會真的在本機的「遠端倉庫」上做出一個 squash 合併提交。其餘全部是真的：真的 git、真的遠端倉庫、真的主幹目錄、真的多個工作目錄（有的有沒存的檔案、有的放了 `.env`、有的名字很像、有的被別的 session 鎖住）。另外替換掉三件事：①「審查證明是否有效」這一步當作有效，但另跑一次真的檢查，確認假證明會被擋；②每 10 秒的等待只記次數不真等；③本機遠端倉庫被當成 GitHub 上的專案。

**所以這次沒證明的事**：
- 真的 GitHub 怎麼判斷合併狀態（例如什麼時候算「落後」、「被擋」或「草稿」）。
- 真的 GitHub 會不會照我們給的內容寫進合併提交。
- 真的 300 秒逾時和網路狀況。

這是第四次試跑。前幾次在較早版本找到的問題都已修好，下面逐條註明。每個情境都重跑了，包括這一版新增的三種：草稿 PR、標題只出現在內文、沒有任何檢查。

測試結果：
- 本變更自帶的五組測試：89 個全過。
- 已提交的對抗探針：50 個通過；2 個標成「已知不擋」的寫法照預期沒擋。

## What you asked for, one line at a time

### 1. On a change whose blind-run report was accepted and whose merge is authorized, the PR ends up merged without the maintainer typing any git or GitHub command.
- **How I tried it**：在變更的工作目錄裡只下一個指令：land，接受者 kouko。假 GitHub 的劇本是：檢查前兩輪還沒好，第三輪全過（其中一項是「略過」）；合併狀態先是「還在算」，再來是「可以合併」。
- **What happened**：它先印「Waiting for checks on PR #41」，等到全過，再等合併狀態算完。接著它自己合併、確認、同步主幹、清理，最後印出下一步要回到主幹目錄。我全程沒有另外打任何 git 或 GitHub 指令。合併時帶著「只合併這個版本」的保護，別人中途推新東西就不會合；沒有用管理員強制合併、自動合併或順便刪分支的選項。
- **Evidence**：happy path，輸出原文：`Waiting for checks on PR #41` / `All checks passed on PR #41` / `Merged PR #41 as 6499a46` / `Trunk main fast-forwarded to 6499a46` / `Removed worktree …` / `Deleted local branch feat/land-merged-changes` / `Deleted remote branch feat/land-merged-changes` / `next: cd '…'`，exit 0。
- **Verdict**：partly — 整條流程在模擬的 GitHub 上完整成功；真的對 GitHub 發出合併這一步沒有試。

### 2. When a PR check fails or the PR cannot merge cleanly, nothing is merged and the report names the failing check or the blocking reason.
- **How I tried it**：七種情況各開一份新環境：
  - 同時有檢查失敗、被取消、需要人工核准。
  - GitHub 回報 PR「落後主幹」「有衝突」「不穩定」「被擋」「草稿」（五種各一份）。
  - PR 上的版本不是本機這一版。

  另外試了合併指令逾時、而 PR 仍開著的情況。
- **What happened**：每次都沒合併、遠端主幹沒動、exit 1，並逐一點名：
  - `BLOCK land.merge: check lint: FAILURE`、`check docs: CANCELLED`、`check deploy-approval: ACTION_REQUIRED`。
  - `PR #41 is BEHIND`、`is DIRTY`、`is UNSTABLE`、`is BLOCKED`、`is DRAFT`。
  - `PR #41 head … is not HEAD …; publish again`。
  - 逾時那次重讀狀態 6 次後才放棄，印 `merge not performed: TimeoutExpired …`。
- **Evidence**：failing checks、behind、conflicting、unstable、blocked、draft PR、unpushed local commit、merge timeout；每份前後狀態都沒有變化。
- **Verdict**：works — 在模擬的 GitHub 回答下，每種情況都擋住並說出原因。

### 3. Accepting the blind-run report is the merge authorization (user-decided 2026-09-14). Without that recorded acceptance, nothing is merged and the report says the authorization is missing.
- **How I tried it**：跑了四次：不給接受者名字；給一個不相干的名字「stranger」；給 intent 裡「自動發佈授權人」那一欄的名字；最後用真的審查證明檢查搭配一份假證明。
- **What happened**：前兩次在碰 GitHub 之前就停下，印 `BLOCK land.merge: blind-run acceptance not recorded; pass --accepted-by <name> after the maintainer accepts`，沒有合併。用授權人名字那次正常合併，提交最後一行是 `Accepted-by: Kouko Maintainer 2026-09-14`。假證明那次印 `attestation does not validate at HEAD; return to Review`，沒有合併。
- **Evidence**：no acceptance、stranger name、publication authorizer name、real attestation check。
- **Verdict**：works — 它只能核對名字對不對，無法確認你真的在對話裡點頭（見「I decided for you」）。

### 4. The squash commit on the trunk carries the PR's title and body.
- **How I tried it**：跑了三次：看成功那次遠端主幹最新提交的完整訊息；讓假 GitHub 故意弄丟內文、只留標題；讓假 GitHub 把第一行換成別的字，PR 標題只出現在內文裡。
- **What happened**：
  - 成功那次：第一行是 PR 標題加 `(#41)`，接著是 PR 內文全文，最後是 Accepted-by 行。
  - 弄丟內文：先印 `Merged PR #41 as …`，再印 `BLOCK land.verify: squash commit lacks the PR body`，exit 1。
  - 標題只在內文：先印 `Merged PR #41 as 3c29887`，再印 `BLOCK land.verify: squash commit lacks the PR title`，exit 1。

  後兩次都沒有同步主幹、沒有刪任何東西，也沒有假裝什麼都沒發生。
- **Evidence**：happy path 的主幹提交訊息；body dropped；title only in body。
- **Verdict**：partly — 內容交給合併指令的方式正確，事後讀回核對也確實有效；但真的 GitHub 會不會照這份內容寫進去，沒有試。

### 5. After a successful merge, the local trunk contains the merge commit, or the report states why the trunk was not updated (it is never force-updated or merged into).
- **How I tried it**：試了四種主幹狀態：乾淨；有沒存的修改；有一個只在本機的提交（跟遠端分岔）；沒有任何目錄開著主幹。每次都掃描 land 發出的所有 git 指令，看有沒有任何強制類選項（連「帶保護的強制推送」也算）。
- **What happened**：
  - 乾淨時，本機主幹前進到合併提交。
  - 有修改時印 `trunk not updated: … has local changes`，主幹不動，修改還在。
  - 分岔時只印一行 `trunk not updated: fatal: Not possible to fast-forward, aborting.`，本機主幹停在原本的本機提交，沒被覆蓋、也沒被合併進去。
  - 沒人開著主幹時，本機主幹也照樣前進。

  掃描結果：碰到主幹的只有「只能往前推」的更新，沒有任何強制選項。唯一出現的強制類選項，是刪除遠端「變更分支」時用的帶保護強制推送，詳見第 8 條。
- **Evidence**：happy path、trunk has local edits、trunk has local commit、no trunk checkout；force-option scan。
- **Verdict**：works。

### 6. After a successful merge, the change's local branch, remote branch, and worktree no longer exist.
- **How I tried it**：成功合併後，檢查工作目錄清單、本機分支、遠端分支和資料夾本身。
- **What happened**：變更的工作目錄資料夾不見了，也從 git 的工作目錄清單消失；本機和遠端的變更分支都刪了。執行中的程式會先移到主幹目錄，不會卡在被刪掉的資料夾裡。
- **Evidence**：happy path 的前後狀態比對。
- **Verdict**：works。

### 7. Cleanup removes nothing, and names the reason, when the PR is not merged on GitHub, the worktree has uncommitted or untracked files, or the branch has commits that are not in the merged PR.
- **How I tried it**：準備七個分支，各帶一種狀況，逐一叫它清：有沒追蹤的新檔、有改過沒提交的檔、有被忽略的 `.env`、PR 還沒合併、本機多一個沒推的提交、合併後別人又推到遠端、根本沒有這個分支。另外試了四種 git 狀態看不到的沒存工作：被標成「不追蹤修改」的已改檔案（兩種標法）、藏在 Python 快取資料夾裡的 `.env`、工作目錄設定成不顯示新檔時的新檔。合併流程裡也放了沒追蹤的檔和 `.env`。
- **What happened**：
  - 單獨清理：全部 exit 1、什麼都沒刪，原因分別是 `has untracked files`、`has modified files`、`has ignored files outside the regenerable set: .env`、`no merged PR for feat/e`、`local branch tip … is not PR head …`、`remote branch tip … is not PR head …`、`no merged PR for feat/does-not-exist`。
  - 看不到的沒存工作：兩次 `has files hidden from git status`（後面點名那個被藏起來的檔案）；快取資料夾裡的 `.env` 被點名為範圍外的忽略檔；還有一次 `has untracked files`。掃描清理把這四個都列成 skip。
  - 合併流程中的兩次：PR 照樣被合併，主幹也前進了，然後清理才停下；工作目錄和兩個分支都還在。
- **Evidence**：named cleanup refusals（七份）、hidden edits（四份加一份掃描清單）、change worktree untracked file、change worktree ignored env；除了合併流程那兩份，前後狀態都沒有變化。
- **Verdict**：works — 但請看「Things I am not sure you want」：工作目錄有沒存的東西時，合併仍會先發生。

### 8. Other worktrees and branches — including ones with uncommitted files and names similar to the change's — are untouched after landing or cleanup.
- **How I tried it**：每次執行前後，都拍下全部工作目錄、分支、檔案清單與狀態做比對。鄰居是這樣安排的：
  - 合併流程旁：名字只多「-2」、有沒存修改、沒追蹤檔和 `.env` 的工作目錄；名字少一截、有草稿檔的工作目錄；名字多「-old」的本機與遠端分支。
  - 單獨清理旁：已合併但有髒檔的「feat/a-2」，以及已合併的「feat/a-old」。
  - 掃描清理旁：沒合併、名字很像又有髒檔的「s/clean-2」。

  我也掃描了 land 發出的所有 git 指令，找任何以強制開頭的選項、`-D` 或 `-f`。
- **What happened**：比對下來，改變的只有目標變更自己的工作目錄、它的兩個分支，以及主幹前進。所有鄰居的檔案、沒存的修改、`.env` 和分支都一模一樣。

  掃描結果要照實說：35 份紀錄裡，27 份沒有任何強制類選項。其餘 8 份（有刪到遠端分支的那幾次），每次刪遠端的變更分支都用了一次**帶保護的強制推送**，寫法類似 `--force-with-lease`：先指定「這個分支現在應該在某個版本」，伺服器上如果分支已被移動就會拒絕刪除。這種推送只刪那一個變更分支；主幹和任何工作目錄都沒有被強制選項碰到，工作目錄的刪除也沒有加強制選項。

  「分支被移動就拒絕」這個保護，這次沒有在推送當下實際觸發：別人推新提交的情況，在事前檢查就被擋下了（第 7 條）。
- **Evidence**：happy path、named cleanup success、sweep confirm 的前後狀態比對；force-option scan（27 份無，8 份只有刪遠端變更分支的帶保護推送）。
- **Verdict**：works。

### 9. Cleanup alone, run for one already-merged change, removes that change's branches and worktree under the same refusals as 6–8.
- **How I tried it**：在主幹目錄下執行 land，只清理 feat/a；它的工作目錄裡只有 Python 的快取檔。第 7 條的拒絕情境也都是用這個單獨清理的形式跑的。
- **What happened**：它先印出要刪的工作目錄完整位置，再刪工作目錄、本機分支和遠端分支，最後印出下一步要回到主幹目錄，exit 0。過程中沒有合併任何東西，也沒碰主幹。
- **Evidence**：named cleanup success。
- **Verdict**：works。

### 10. A sweep selects only changes whose PR is merged on GitHub; before removing anything it lists what it would remove and what it skips with each reason, and removes only after the maintainer confirms that list. Each selected change gets the same refusals as 7–8, and one refusal does not stop the others.
- **How I tried it**：準備八個分支：已合併且乾淨、已合併但只剩遠端、已合併但有沒追蹤檔、已合併但有 `.env`、沒合併、沒合併且名字很像又髒、已合併但工作目錄被別的 session 鎖住、一開始沒合併。依序做了六步：
  1. 只列清單。
  2. 用錯的確認碼。
  3. 列完之後，讓「一開始沒合併」那個變成已合併，再用舊確認碼。
  4. 重新列清單。
  5. 用新確認碼確認。
  6. 再列一次，看剩什麼。
- **What happened**：
  1. 列出 3 條 remove 和 2 條附原因的 skip，沒合併的兩個完全沒出現；印出確認碼，什麼都沒刪。
  2. 和 3. 都印 `BLOCK land.cleanup: the sweep list differs from the one confirmed; run land --sweep again`，什麼都沒刪。
  4. 新清單多了剛合併的那個，確認碼也換了。
  5. 刪掉乾淨的、只剩遠端的、剛合併的三個。被鎖住的那個被拒，訊息是 `git refused to remove worktree …: fatal: cannot remove a locked working tree, lock reason: in use by another session`，沒有任何「強制覆蓋」的提示，也沒擋住其他三個；exit 1。
  6. 只剩兩條 skip 和被鎖住的那一個。
- **Evidence**：sweep list、wrong token、list changed after listing、relist、sweep confirm、sweep after。
- **Verdict**：works。

### 11. A hand-typed `gh pr merge` is still refused by Loom's publication hook; only the landing path merges.
- **How I tried it**：把 49 種 Bash 指令寫法當成 agent 要執行的指令，餵給發佈攔截器，看它放不放行。
- **What happened**：
  - 所有真的會合併的寫法都擋下，印 `BLOCK push.merge: merge through … land --accepted-by <name>`。包括：直接打；先切換到絕對路徑再打；包在 `bash -c`、`sh -c`、`zsh -c`、`eval` 裡；完整路徑；前面加 `env`、`command`、`sudo`、`nohup`、`timeout 60` 或環境變數；括號、大括號、`if … then … fi`；多打空格；分號或換行接在別的指令後；`-R` 參數放前面；管線；背景執行；`$( )` 和反引號；反斜線換行拆開；加引號；跳脫字元。
  - 這一版新擋下的：`gh pr $'merge' 5`、`gh pr $"merge" 5`，以及把三個字都用 `$'…'` 包起來的寫法。
  - 正確放行的有：`gh pr view`、`gh pr checks`、`git status`、執行 land 的那一行。
  - 仍然放行的有：GitHub 網頁 API 的合併方式（刻意不擋，已揭露）；以及在執行時才用 `printf` 拼出這幾個字的寫法（已知限制，對抗探針裡也標為「已知不擋」）。
  - 副作用：只要指令文字依序出現這三個字就會被擋，即使只是提到。例如提交訊息裡寫到、`grep` 搜這幾個字、註解或 `echo` 裡出現。
  - land 自己的合併走程式內部呼叫，不經過這個攔截器，第 1 條的成功流程可以看到。
- **Evidence**：hook payloads（18 種基本寫法、16 種包裝寫法、10 種拆字與只提到的寫法、5 種 `$'…'` 引號寫法）。
- **Verdict**：works — 手打的合併都被擋；代價是單純提到這幾個字的指令也會被擋。

## 對你既有的資料做了什麼

這次試跑沒有碰你任何既有的資料：所有操作都在暫存的乾淨複製和臨時建立的倉庫上，唯一寫進你專案的是這份報告（未提交）。

這個變更本身只有在被叫用時才會動你的東西，而且動了就不可還原：
- 合併 PR。
- 刪掉那個變更的工作目錄（連同裡面的快取）。
- 刪本機變更分支。
- 用帶保護的強制推送刪遠端變更分支。
- 把本機主幹往前推（只推進，不覆蓋）。

它不改寫任何舊檔案格式，也不做備份。安全靠的是「條件不符就整個不動」：遇到沒存的檔、被 git 狀態藏起來的修改、`.env` 這類非快取的忽略檔、不在 PR 裡的提交，或 PR 沒合併，都會拒絕。

## I decided for you

以下是這個變更做的、沒有問過你的決定（review 站沒有交給我任何被駁回的重要發現）：

- **刪遠端變更分支的方式** — I picked 帶保護的強制推送（指定分支應在的版本，分支被移動時伺服器拒絕）because 一般的刪除不比對版本，檢查之後有人推了新東西也會被刪掉；changing it later means 換回一般刪除會失去這層保護，或改用 GitHub API 刪分支就要另外處理比對。
- **單獨清理和掃描清理怎麼找工作目錄** — I picked 在 git 的工作目錄清單裡，找「分支欄位完全等於變更分支名」的那一筆，並先印出完整位置再刪 because 單獨清理和掃描清理沒有「目前所在的工作目錄」可用，一定得查清單；所以我把 intent 的「絕不從清單篩選」解讀成「絕不用部分比對或模糊比對來篩」。changing it later means 若你堅持字面意思，掃描清理這個功能就做不出來。
- **掃描清理只看最近 1000 個已合併 PR** — I picked 一次查 1000 個，查滿時輸出會明說「更舊的沒檢查」 because GitHub 一次查詢有上限；changing it later means 要改成分頁查詢，掃描會變慢。
- **60 秒內都沒有任何檢查出現時照樣合併** — I picked 印 `No checks registered on PR #41` 後繼續合併（實測確實合併了） because 沒有設定 CI 的專案也要能用；changing it later means 改成拒絕的話，沒有 CI 的專案就永遠合併不了，除非另加一個選項。
- **變更分支開在主幹目錄時** — I picked 把主幹目錄切回主幹分支，再刪變更分支（前提是主幹目錄乾淨、且沒有別處開著主幹） because 分支還開著時刪不掉；changing it later means 改成拒絕的話，你得自己先切換。
- **草稿 PR 一律拒絕合併** — I picked 印 `PR #<n> is DRAFT` 並停下 because 草稿代表還沒準備好；changing it later means 你要先在 GitHub 把 PR 標成可審查，才能用 land。
- **「可以一起刪」的忽略檔只有一小份清單** — I picked `.DS_Store`、`.pyc` 檔，以及 pytest／mypy／ruff 快取、`.venv`、`node_modules` 資料夾裡的東西；其他被忽略的檔（包括放在 Python 快取資料夾裡的非 `.pyc` 檔）都會讓清理拒絕 because git 不加強制選項刪工作目錄時，會默默把被忽略的 `.env` 一起刪掉；changing it later means 清單以外的快取（例如 `dist`、`.tox`、`target`）會讓清理一直被拒，要改清單才行。
- **被 git 狀態藏起來的修改一律拒絕清理** — I picked 檢查 skip-worktree 和 assume-unchanged 標記，看到就拒絕 because 刪工作目錄會連這些看不到的修改一起刪掉；changing it later means 若你刻意用這兩種標記放本機設定，得先取消標記才能用 land 清理。
- **接受者名字必須等於 intent 的發起人或自動發佈授權人** — I picked 只核對名字 because 這是程式唯一能核對的東西；changing it later means 換人代為接受時要先改 intent，而且它仍靠 agent 如實轉述你的點頭。
- **所有檢查都要過，不只必要檢查** — I picked 失敗、取消或需要人工核准都擋 because 這個專案四項檢查裡只有一項是必要的；changing it later means 一個不重要的檢查壞了，也要修好或重跑才能合併。
- **掃描清理用一組確認碼** — I picked 清單有任何變動就整批不刪 because 要證明刪的就是你看過的那份清單；changing it later means 多一步，而且帶確認碼這一步同樣靠 agent 如實轉述。
- **攔截器改成寧可錯擋** — I picked 只要 Bash 指令文字依序出現 gh、pr、merge 就擋，即使只是提到 because 各種包裝和引號寫法猜不完；changing it later means agent 要寫提到這個指令的提交訊息或搜尋時得改寫法，你自己想手動合併也只能走 land 或 GitHub 網頁。
- **herdr 的工作區紀錄可能過期** — I picked 直接用 git 刪工作目錄 because Loom 也要在沒有 herdr 的地方用；changing it later means herdr 側邊欄可能留著已刪掉的項目，要手動清。
- **沒有擋 GitHub 網頁 API 的合併方式** — I picked 只擋 intent 寫到的那個指令 because 範圍是這樣定的；changing it later means 要另外擋 API 寫法。
- **Accepted-by 行的日期用執行那台電腦的時區** — I picked 本機日期 because 最簡單；changing it later means 改成 UTC 的話，在台北深夜跑會跟你的日曆差一天。

## Things I am not sure you want

- 寧可錯擋的攔截器，會擋下只是提到那三個字的提交訊息、搜尋、註解和 `echo`。這個代價你能接受嗎？
- 變更的工作目錄還有沒存的檔或 `.env` 時，land 仍會**先合併**，到清理那步才停下（第 7 條實測）。要不要改成合併前就先檢查，髒的話連合併都不做？
- 60 秒內沒有任何檢查出現時，land 會直接合併。如果你的專案有 CI、只是那次剛好還沒排上，這會跳過 CI。這樣可以嗎？
- 需要時，land 最多會等 60 分鐘的檢查，這段時間 agent 的那次指令會一直卡住。你能接受嗎？

## 各份文件是否遵守英文規則與模板規則

| 文件 | 英文規則 | 模板規則 | 證據 |
| --- | --- | --- | --- |
| 計畫 | 成立；「問過的問題」一段是引用你的中文原話 | 不適用 | plan「Questions asked」段 |
| 規格 | 成立 | 成立：需求都是 EARS 句型，並對回驗收條目 | spec `REQ-1`…`REQ-11` |
| 審查紀錄的發現 | 這個版本還沒有審查紀錄，無法判斷 | 無法判斷 | 變更資料夾內無審查紀錄 |
| 證據 | 成立：對抗探針的說明和我的試跑紀錄都是英文 | 不適用 | adversarial probes；blind-run evidence |
| 測試說明文字 | 成立 | 不適用 | land merge／cleanup／sweep 測試的模組說明 |
| 測試名稱 | 成立 | 大致成立：多數是「對象＿狀態＿結果」，少數缺結果段；探針用駝峰式三段 | `test_sweep_no_candidates`、`test_remote_already_deleted`、`test_hookClassifier_obfuscatedForms_blocked` |
| 提交訊息 | 成立：沒有中日文 | 不適用 | branch commits since trunk |
