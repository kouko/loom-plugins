# 合併底線移到 GitHub — 我試了什麼、結果如何

2026-09-22 在專案的乾淨副本（f3060a81，尚未推上 GitHub）上試跑。需要 GitHub 的部分，在你同意建立的公開測試 repo 上實地跑：https://github.com/kouko/loom-floor-test （留給你之後刪除）。

## 一條一行的結果

| # | 你要的 | 結果 |
|---|---|---|
| 1 | 內文缺節或空節時 GitHub 擋合併，並指名是哪一節 | 通過 — 合併被 GitHub 擋下；節名寫在檢查的執行紀錄裡，檢查頁面上的摘要只寫「失敗」 |
| 2 | 直接推送到 main 被 GitHub 拒絕 | 通過 |
| 3 | 沒有驗證紀錄、或紀錄不符時仍可合併，PR 上看得到揭露，手改文字無效 | 通過 — 「沒有紀錄」和「不符」都看到了；檢查頁的「工作摘要」這一處我沒看到（沒有瀏覽器可用） |
| 4 | 任何寫法的推送或開 PR 都不被擋，最常見寫法出一行提醒 | 通過（在檢查程式層級驗證；本機裝的是舊版 loom，所以沒能在真實 agent 畫面上看提醒） |
| 5 | ship 站開 PR 前擋下缺節或空節的內文並指名 | 通過（實地） |
| 6 | loom 合併指令擋下缺節的 PR 並指名；齊全但沒紀錄的 PR 會合併並提醒 | 部分通過 — 合併加提醒實地成功；缺節的 PR 有擋，但訊息說的是「GitHub 檢查失敗／被擋」，沒有說是哪一節 |
| 7 | main 沒設規則時說出缺什麼、給設定指令，你沒同意前不改任何設定 | 通過 |
| 8 | 讀不到規則時說「無法確認」並繼續 | 通過 |
| 9 | 把 CI 範本複製進新 repo，結果和第 1、3 條一致 | 部分通過 — 行為一致，但範本得先改兩行才能用，因為它指向的共用檔案還沒發佈上 GitHub |
| 10 | 口語跳過後繼續，不要通行碼；推送、開 PR、合併時都提醒缺哪些紀錄 | 通過 — 提醒三處都看到了；「agent 口頭告知跳過哪一步」只從站點說明文字判斷，沒有實際讓 agent 跑一次 |
| 11 | PRINCIPLES.md 第 2 條改為「跳過必須在 PR 揭露」、不再要打字確認，並有你的簽署 | 通過 — 簽署那一行是 agent 依你在第一個決策點的回答寫上的，不是你親手加的 |
| 12 | 只是文字裡提到合併指令時，沒提醒也不擋 | 通過 |
| 13 | 既有測試全部通過 | 通過 |

## 逐條細節

### 1. 在 main 已設定「必須透過 PR」且啟用內文檢查的 repo：PR 內文缺了九章節中任何一節、或任一節沒有實質內容時，GitHub 上無法合併，檢查結果指名是哪一節。
- **怎麼試的**：在測試 repo 開一個缺「Scope」節的 PR，要 GitHub 合併；再把內文改成「Risks and rollback」節是空的，再合併一次。
- **結果**：兩次 GitHub 都拒絕合併，原因是「必要檢查失敗」。檢查的執行紀錄寫著「heading "Scope" is missing」與「heading "Risks and rollback" is empty」。不過在 PR 的檢查頁上，醒目的錯誤標記只寫「程序以代碼 1 結束」，要點進執行紀錄才看得到節名。
- **證據**：`evidence/blind-run/pr1-missing-scope-joblog.txt:306`、`pr1-empty-risks-joblog.txt`、`pr1-merge-attempt-missing-scope.txt`、`pr1-missing-scope-annotations.json`；PR https://github.com/kouko/loom-floor-test/pull/1
- **判定**：通過 — 擋得住，也有指名；只是節名要多點一層才看得到。

### 2. 同一個 repo：直接推送到 main 被 GitHub 拒絕。
- **怎麼試的**：以 repo 擁有者（管理員）身分試兩種直接寫入：一般的 git 推送，以及透過 GitHub 網頁 API 直接改 main 上的檔案。
- **結果**：兩次都被拒，GitHub 回「Changes must be made through a pull request」。main 前後沒有變。
- **證據**：`evidence/blind-run/direct-git-main.txt`、`direct-contents-put-main.txt`
- **判定**：通過 — 連管理員都不能繞過。

### 3. 同一個 repo：九章節齊全、但分支沒有驗證紀錄的 PR 可以合併，且 PR 上看得到「沒有驗證紀錄」的揭露；驗證紀錄存在但與目前內容不符時，PR 上看得到「不符」的揭露；兩種揭露都由 loom 重新計算，手動改寫 PR 上的狀態文字不會讓檢查結果改變。
- **怎麼試的**：開了三個內文齊全的 PR，而且每個內文都手寫了一行「驗證狀態：有效」：
  - PR 1：分支沒有驗證紀錄
  - PR 2：驗證紀錄是壞的
  - PR 4：從本專案另一個舊變更搬來一份真的驗證紀錄，但內容已經對不上
- **結果**：三個都能合併。檢查附上的提示分別是：
  - PR 1：「absent」（沒有紀錄）
  - PR 2：「stale（格式不完整）」
  - PR 4：「stale（內容摘要與目前內容不符）」

  手寫的「有效」完全沒被採用。這些提示在 PR 的檢查結果裡看得到。檢查另外會把狀態寫進「工作摘要」頁面，但那一頁要靠瀏覽器才顯示，我這次沒有瀏覽器，所以沒看到。
- **證據**：`evidence/blind-run/pr1-good-annotations.txt`、`pr2-stale-notice.txt`、`pr4-stale-notice.txt`、`pr1-merge-good.txt`、`pr2-merge-stale.txt`、`pr4-merge.txt`；PR https://github.com/kouko/loom-floor-test/pull/1 、/pull/2 、/pull/4
- **判定**：通過 — 工作摘要那一處沒有親眼看到。

### 4. 在沒有驗證紀錄的分支上，agent 用任何 shell 寫法推送或開 PR，都不會被 loom 擋下；最常見的直接寫法會在終端出現一行提醒。
- **怎麼試的**：在一個拋棄式 repo 裡，把 16 種指令寫法照 agent 工具送出的格式交給這個分支的 loom 檢查：
  - 直接推送、直接開 PR
  - 前面加環境變數
  - 用 `true;`、`if`、括號、`xargs`、heredoc、`bash -c`、`&&` 包起來的寫法
- **結果**：全部放行。直接推送、直接開 PR、前面加變數這三種出現一行「loom: verification absent (missing: plan, attestation); publishing anyway.」，其他包裝寫法沒有提醒（符合「認不出就不提醒」）。拿不在 repo 裡的位置去跑、讓它出錯時，也是放行並說明出錯。
- **證據**：`evidence/blind-run/hook-cases.txt`（由 `hookdrive.py` 產生）
- **判定**：通過 — 限於檢查程式本身；這台機器裝的是舊版 loom，無法在真實 agent 畫面上看提醒。

### 5. 用 ship 站開 PR 時，內文缺章節或有空章節會在 PR 送出前被擋下，並指名是哪一節。
- **怎麼試的**：在測試 repo 用 ship 站那一支發佈指令，依序送缺「Scope」、「Risks and rollback」空白、以及完整的內文。
- **結果**：前兩次分別回「heading "Scope" is missing」「heading "Risks and rollback" is empty」，分支完全沒被推上去。完整內文那次推送成功、開了 PR 5、CI 通過，終端出現「verification absent (missing: plan, attestation); publishing anyway.」。
- **證據**：`evidence/blind-run/ship-publish-missing-scope.txt`、`ship-publish-empty-risks.txt`、`ship-publish-good.stdout.txt`、`ship-publish-good.stderr.txt`
- **判定**：通過。

### 6. 用 loom 自己的合併指令合併一個內文缺章節的 PR 會被擋下並指名是哪一節；內文齊全、沒有驗證紀錄的 PR 會合併，終端出現提醒。
- **怎麼試的**：把 PR 5 的內文在 GitHub 上改成缺「Scope」，執行 loom 的合併指令。之後把 GitHub 規則暫時關掉約一分鐘再試一次，測完立刻打開。最後把內文改回完整，再合併。
- **結果**：
  - 規則開著時：回「PR #5 is BLOCKED」，同時印出「All checks passed」。改內文後新的檢查還沒登記上去，所以這行是錯的。
  - 規則關著時：回「check loom-pr-floor / PR floor: FAILURE」。

  兩次都沒合併，但都沒說是哪一節。原因是合併指令先看 GitHub 的檢查和合併狀態，只要 repo 裝了 CI 範本，缺節的 PR 永遠先卡在這裡，輪不到它自己的節名檢查。它自己「指名哪一節」的那段只有套件測試證明過。內文改回完整後成功合併，終端出現「verification absent (missing: plan, attestation); merged anyway.」。
- **證據**：`evidence/blind-run/land-missing-scope.txt`、`land-missing-scope-no-rules.txt`、`land-good-absent.txt`、`ruleset-reenabled.txt`；套件測試 `test_land_merge.py::test_missing_heading_refuses_names_it`
- **判定**：部分通過 — 擋得住，也會合併加提醒；但實際使用時不會指名哪一節。

### 7. 在 main 沒有設定規則的 repo 執行 ship 站：ship 站說出缺了哪一項，並顯示一個設定指令；使用者沒同意前，GitHub 上的設定沒有任何改變。
- **怎麼試的**：CI 範本放上測試 repo 的 main 之後、還沒設規則之前，跑 ship 站會呼叫的那支規則檢查。前後各讀一次 GitHub 上的規則清單。另外讀 ship 站說明，確認它要求 agent 先徵得同意。
- **結果**：輸出「main does not require a pull request (administrators included)」與「does not require the check "loom-pr-floor / PR floor"」，接著是一段完整的設定指令。前後規則清單都是空的。ship 站說明寫著「只在使用者明確同意後才執行設定指令，絕不自行執行」。我照你的同意把那段設定套用到測試 repo 後，再跑一次，得到「main requires a pull request (administrators included) and the check…」，也就是「已設定」。
- **證據**：`evidence/blind-run/github-rules-no-rules.txt`、`rulesets-before.json`、`rulesets-after-probe.json`、`github-rules-configured.txt`、`ruleset-created.json`
- **判定**：通過 — 「agent 會先問你」這點是從說明文字判斷的。

### 8. 在讀不到 GitHub 規則的 repo（權限不足或不是 GitHub）執行 ship 站：ship 站說「無法確認」並繼續，不擋下。
- **怎麼試的**：五種情況：
  - 沒有遠端
  - 遠端是 GitLab
  - 沒裝 GitHub 指令工具
  - GitHub 回伺服器錯誤
  - 以沒有權限的訪客身分讀已設好規則的測試 repo
- **結果**：五種都回「could not confirm GitHub rules …」加原因，程式正常結束、沒有擋。訪客身分那次特別值得注意：GitHub 不讓非管理員看到「誰可以繞過規則」，所以即使規則設得完全正確，沒有管理權限的人永遠只會看到「無法確認」。GitLab 那次的原因寫成「HTTP 410」，而不是「不是 GitHub」，因為它把 GitLab 當成 GitHub 去問了。
- **證據**：`evidence/blind-run/github-rules-unreadable.txt`、`github-rules-anonymous-viewer.txt`、`ruleset-anonymous.json`
- **判定**：通過。

### 9. 把 plugin 附的 CI 範本複製進一個新的 GitHub repo 並開 PR，內文檢查會執行，結果與第 1、3 條一致。
- **怎麼試的**：把範本和它呼叫的共用檔案複製進測試 repo。範本改一行（呼叫的位置改成測試 repo），共用檔案改一行（下載 loom 的來源改成測試 repo）。loom 的檢查程式夾和它必讀的規格檔夾也一起放進去，因為真正的共用檔案會把整個 loom-code 夾抓下來。先把範本放上 main，再加規則。另外開了 PR 3：這個 PR 把範本改成「永遠通過」、內文缺節。
- **結果**：第 1、3 條的結果都在這個 repo 上跑出來。檢查在 GitHub 上顯示的名稱正是預期的「loom-pr-floor / PR floor」。改內文會重跑檢查。PR 3 出現兩個同名檢查：main 版本失敗、PR 自己改的版本通過。GitHub 仍然拒絕合併（「is failing」），也就是 PR 改不了自己的必要檢查。PR 3 保持開著當證據。
- **證據**：`evidence/blind-run/test-repo-workflow-diff.txt`（改動的兩行）、`pr3-checkrun-origins.txt`、`pr3-merge-attempt.txt`、`always-pass.yml`；PR https://github.com/kouko/loom-floor-test/pull/3
- **判定**：部分通過 — 行為一致；「不改就能用」要等本專案把共用檔案發佈到 GitHub 的 main 後才能證明。

### 10. 使用者口語指示跳過步驟後，agent 繼續完成推送與開 PR，過程中沒有要求使用者輸入任何通行碼；推送、開 PR、合併時終端都出現提醒，列出哪些驗證紀錄不存在。
- **怎麼試的**：在沒有計畫、也沒有驗證紀錄的分支上推送、開 PR、合併，每一步都看有沒有提醒、有沒有要求輸入代碼。另外讀了各站點的說明文字。
- **結果**：
  - 推送、開 PR：出現「(missing: plan, attestation)」
  - 在 loom 以外合併：出現「this merges outside … (missing: plan, attestation); merging anyway.」
  - ship 發佈、loom 合併：同樣列出缺的紀錄
  - 全程沒有要求輸入代碼

  用法說明、ship、closing-review、build 四處都寫著：只在使用者口語要求時跳過，並用一句話告訴使用者跳過了哪一步，然後繼續，絕不要求輸入產生的代碼。寫計畫的站點（write-plan）沒有這段話，只寫了「照跳站紀錄省略步驟」；如果 agent 是直接從這一站開始，就沒有文字提醒它要說出跳過了什麼。
- **證據**：`evidence/blind-run/hook-cases.txt`、`ship-publish-good.stderr.txt`、`land-good-absent.txt`；`loom-code/skills/using-loom-code/SKILL.md:22-24`、`ship/SKILL.md:29-32`、`closing-review/SKILL.md:25-28`、`build/SKILL.md:21-24`、`write-plan/SKILL.md:44-47`
- **判定**：通過 — agent 口頭告知這部分只看了說明文字，沒有實際讓 agent 跑一次；寫計畫的站點少了這段話。

### 11. PRINCIPLES.md 第 2 條寫明「跳過驗證必須在 PR 揭露」且不再要求打字確認，並帶有使用者的簽署（ratified-by）。
- **怎麼試的**：對照修改前後的第 2 條與簽署行。
- **結果**：原文「透過打字確認明確跳過的步驟…」改成「使用者以口語指示跳過的步驟…每一次跳過都必須在 PR 揭露，PR 上的驗證狀態是重新計算的，不是宣稱的」。簽署行多了「non-negotiable 2 plain-words-skip amendment by kouko 2026-09-22」。
- **證據**：`PRINCIPLES.md:2`、`PRINCIPLES.md:9`；commit e4208b1f
- **判定**：通過 — 那行簽署是 agent 依你在第一個決策點選的 A 寫上的，最後的措辭你還沒親自看過。

### 12. 只是在文字裡提到合併指令的操作（搜尋那串字、印出那串字、當作 commit 訊息），指令正常執行，沒有提醒也沒有阻擋。
- **怎麼試的**：送出搜尋、echo、printf，以及把合併指令寫進 commit 訊息，四種寫法。
- **結果**：四種都放行，沒有任何輸出。
- **證據**：`evidence/blind-run/hook-cases.txt`（#12 四筆）
- **判定**：通過。

### 13. 既有測試全部通過。
- **怎麼試的**：在乾淨副本跑完整套件測試。
- **結果**：全部通過，程式結束代碼 0。主套件 2124 通過、2 略過，其餘各組也全數通過、沒有失敗。
- **證據**：`evidence/blind-run/package-suite.log`
- **判定**：通過。

### 使用流程（規格裡的畫面流程）

| 流程 | 我做了什麼 | 看到什麼 | 證據 |
|---|---|---|---|
| 推送、沒有紀錄 | 直接推送 | 放行，出現一行「absent」提醒 | `hook-cases.txt` |
| 包起來的推送 | 7 種包裝寫法 | 放行，沒有提醒 | `hook-cases.txt` |
| 檢查本身出錯 | 在 repo 外執行 | 放行，並說明出錯 | `hook-cases.txt` |
| 跳站紀錄目錄 | 寫入那個目錄 | 仍然擋下（照原本要求保留） | `hook-cases.txt` |
| 在 loom 以外合併 | 直接合併指令 | 放行，出現提醒 | `hook-cases.txt` |
| 只提到合併字樣 | 搜尋、印出、commit 訊息 | 沒有任何輸出 | `hook-cases.txt` |
| ship 發佈、內文不對 | 缺節、空節 | 送出前擋下並指名 | `ship-publish-*.txt` |
| ship 發佈、內文正確 | 完整內文 | 推送、開 PR、提醒 | `ship-publish-good.*` |
| ship、規則沒設 | 沒規則的 repo | 列出缺的兩項加設定指令，沒改設定 | `github-rules-no-rules.txt` |
| ship、範本不在 main | 模擬範本不存在 | 叫你先放範本 | `github-rules-template-missing.txt` |
| ship、讀不到規則 | 五種情況 | 「無法確認」，繼續 | `github-rules-unreadable.txt` |
| 你同意設定 | 套用印出的設定 | 再跑一次變成「已設定」 | `github-rules-configured.txt` |
| loom 合併、內文不對 | 缺節 | 擋下，但沒指名節（見第 6 條） | `land-missing-scope*.txt` |
| loom 合併、沒紀錄 | 完整內文 | 合併並提醒 | `land-good-absent.txt` |
| CI、內文不對 | 缺節、空節 | 檢查失敗，執行紀錄裡有節名；改內文會重跑 | `pr1-*-joblog.txt` |
| CI、內文正確 | 三種紀錄狀態 | 通過，提示「absent／stale」 | `pr*-notice.txt` |
| CI、PR 改自己的檢查 | 改成永遠通過 | 無效，仍擋合併 | `pr3-*.txt` |
| 口語跳過 | 只看說明文字 | 說明要求 agent 說一句跳過了哪一步 | 站點說明文字 |

一處跟規格不一樣：規格說「既沒有範本也沒有規則的 repo，表現跟『規則沒設』相同」，實際上只會說「範本不在 main，請先放上去」，不會同時列出缺的兩項規則。

## 審查摘要

交給我的資料裡沒有審查意見，也沒有被駁回的重要以上意見，所以這裡沒有東西可以摘要。這份報告本身不是審查。

## 我問過你的問題

盲跑過程中我沒有問你任何問題。以下是先前在第一個決策點已經問過你、這次照著執行的：
- PR 內文維持九個章節，還是放寬？——你說維持九個。
- PRINCIPLES.md 第 2 條要改成「只需在 PR 揭露」（A）還是保留打字確認（B）？——你選 A，並確認「口語就能跳過任何步驟」。
- 跳過時要怎麼做？——你說要提醒，但不擋流程。
- 是否授權自動推送與開 PR？——你說是；合併另外決定。

## 對你既有的資料做了什麼

- **你原本的 repo**：這次試跑沒有動到 kouko/loom-plugins 或任何其他 repo 的設定、分支、規則或 PR。
- **新建的測試 repo**：建了一個公開 repo kouko/loom-floor-test，在裡面建了分支、PR、一組規則，合併了 PR 1、2、4、5。這組規則還曾經暫停約一分鐘，之後已恢復。這個 repo 留著給你刪。
- **這個變更本身的影響**：它不改寫你任何檔案內容，但會拿掉 loom 在本機擋推送的那一道關卡。一旦安裝新版，你其他 repo 裡「沒有 PR 就合進 main」的防線，就只剩 GitHub 規則；而這些規則要你自己同意才會設定。目前 kouko/loom-plugins 還沒有這組規則，這個專案自己的 main 在新版上線後會暫時沒有這道保護。
- **PRINCIPLES.md**：第 2 條最後一句被改寫。舊文字在版本紀錄裡還讀得到。

## 我替你決定的事

- **測試 repo 裡多放了檔案**：除了 loom 的檢查程式夾，我也放了它必讀的規格檔夾和範本夾。只放程式夾它根本跑不起來；真正的共用檔案會抓整個 loom-code 夾，所以這樣最接近真實情況。之後要改，只需要重新放一次檔案。
- **暫停測試 repo 的規則約一分鐘**：為了看 loom 合併指令自己的節名檢查會不會出現。結果它仍然先被 CI 擋下。規則已恢復。這只影響測試 repo。
- **「不符」用了真的舊紀錄**：從本專案另一個已完成的變更搬一份真實的驗證紀錄來，比自己捏造一份壞檔更像真實情況。那份壞檔的例子我也保留了。
- **用替身模擬讀不到規則的情況**：沒有權限、伺服器錯誤、範本不在 main 這三種，我用一個假的 GitHub 指令工具模擬，沒有真的去找一個你沒權限的 repo。
- **PR 3 留著不關**：它證明「PR 改自己的檢查沒用」，留著方便你看。

以下是之前由 agent 決定、你可能想知道的事（取自規格）：
- **沒有替 kouko/loom-plugins 套用規則**：這要改 GitHub 設定，屬於要先問你的事。以後要套，就是執行一段設定指令。
- **範本跟著本專案的 main 走，沒有固定版本**：本專案之後改了，所有用這個範本的 repo 都會立刻跟著變。範本裡有註解教你改成固定版本。
- **CI 看到「宣稱跳過」時一律顯示「有效（跳過了…）」**：GitHub 上沒有本機的跳過紀錄可以核對，所以它不會把宣稱跳過的顯示成完全有效。

## 我不確定你要不要的事

- 要不要現在就在 kouko/loom-plugins 套用這組 GitHub 規則？沒套的話，新版上線後這個專案的 main 只剩本機提醒。
- loom 合併指令擋缺節的 PR 時只說「GitHub 檢查失敗」，沒說是哪一節。這樣可以接受，還是要它先看內文、直接說出節名？
- 沒有管理權限的協作者跑 ship 站時，永遠會看到「無法確認規則」。這樣可以嗎？
- CI 失敗時，節名要多點一層才看得到。要不要讓它直接顯示在 PR 的檢查頁上？
- 測試 repo 什麼時候刪？PR 3 還開著。

## 英文規則與格式規則

| 產出 | 英文規則成立？ | 另外的格式規則 | 證據 |
|---|---|---|---|
| 計畫 | 成立 — 只有「我問過你的問題」照你的原話保留中文 | — | `plan.md:72-75` |
| 規格 | 成立 — 中文只出現在引用你原話的「Carried detail」 | 每條需求都用 WHEN／WHERE／IF／shall 的句型寫成：成立 | `spec.md:35,38,46,47`；`spec.md:6-31` |
| 審查意見 | 無法判斷 — 沒有交給我 | 標籤格式：無法判斷 | — |
| 證據 | 成立 — 這次的證據檔與試探程式都是英文 | — | `evidence/blind-run/`、`evidence/probes/` |
| 測試說明文字 | 成立 — 新增或修改的說明文字裡沒有中文 | — | 35 個測試檔的差異 |
| 測試名稱 | 成立 | 命名至少分成三段：130 個全部符合；每段是否真的是「對象／狀態／預期」，我沒有逐一判斷 | 35 個測試檔的差異 |
| commit 訊息 | 成立 — 31 筆都是英文 | — | `git log eb35e8b9..f3060a81` |
