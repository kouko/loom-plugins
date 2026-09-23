# 把舊名稱的驗收步驟改名為 independent acceptance testing — 我試了什麼、結果如何

2026-09-23 在一份乾淨的專案副本（commit 71e6978）上試過。我沒有參與這次改動的任何實作。

**2026-09-23 重測（commit 7cd16d3）**：修正提交後，由另一位沒有參與實作的測試者在新的乾淨副本上只重測第 3 條。第 1、2、4、5、6 條沿用上一輪的結果，各條下方寫了理由。這兩個修正提交只改了三樣東西：PR 上「跳過了哪些步驟」那一行的產生方式、出貨站的說明文字、給 agent 的白話用語指南（外加對應的兩支測試）。

**2026-09-23 第二次重測（commit cc2b66b）**：**更正上一輪的說法。** 上一輪重測只試了 PR 上的「Skipped steps:」那一行，就把第 3 條判為 works。可是 PR 與對話裡列出被跳過步驟的不只這一行，還有另外三行，而收尾審查發現那三行當時仍只印出 `acceptance-test` 這個代號。所以上一輪的 works 說得太滿，實際上只做到一部分。之後又有四個修正提交，這一輪由另一位沒有參與實作的測試者，在新的乾淨副本上逐行重測第 3 條提到的四種行。修正內容：讓「查看這次改動會跑哪些步驟」的輸出多一欄現成的「因為改動很小而跳過」那一行；PR 的驗證狀態行改走同一套寫法；出貨站與其他各站的說明文字跟著改；刪掉一支重複的測試，並把改名檢查的搜尋範圍擴大到根目錄的工具資料夾。第 1、2、4、5、6 條沿用前面的結果，各條下方寫了這一輪核對過的理由。

**2026-09-23 第三次重測（commit d6ac4f8）**：又有一個修正提交。它在規劃站、建置站與出貨站的說明各加了一句「要求跳過 acceptance testing 或以前的 blind run，都是指新步驟」；建置站列出可跳過步驟時改寫出完整名稱；改名檢查多掃了兩份根目錄文件，並多一支測試確認四個站都有那句對照；另外改了 CHANGELOG 的措辭、根目錄說明的換行，刪了一支重複的版號測試、改了一支測試的名字。這一輪由另一位沒有參與實作的測試者，在新的乾淨副本上**完整重測第 2、3、4、6 條**（每條提到的每個地方都重試，不只修正碰到的部分），並第一次用這個分支的 plugin 開真實的 agent 對話試白話跳過。第 1、5 條沿用，理由寫在各條下方，都對照過修正的完整差異。

## 你要的東西，一條一條看

### 1. The step id is `acceptance-test`, the agent is dispatched as `loom-code:acceptance-tester`, and the report is written at `docs/loom/<change-id>/acceptance-test-report.md` from a template of the same name.
- **我怎麼試**：在乾淨副本裡請檢查工具列出這次改動會跑哪些步驟；查看 agent 清單與它的名稱；查看報告的存放位置規則與範本檔。
- **結果**：步驟清單裡出現的是新的 step id，舊 id 不在其中；agent 以新名字存在；報告位置規則與範本都用新名字。我這份報告本身就是照新範本、寫在新位置。
- **證據**：`loom_checker.py selection show 2026-09-23-rename-blind-run-to-acceptance-testing` → `run` 含 `acceptance-test`；`loom-code/agents/acceptance-tester.md`（frontmatter `name: acceptance-tester`）；manifest `artifacts.acceptance-test-report.path = docs/loom/<change-id>/acceptance-test-report.md`；範本 `loom-code/skills/closing-review/references/acceptance-test-report.md`
- **判定**：works — 三個名字都已換成新的。
- **重測**：沿用上一輪 — 修正沒有碰步驟清單、agent 定義、報告位置規則或範本。
- **第二次重測**：沿用 — 這四個修正提交沒有碰步驟清單、agent 定義、報告位置規則或範本（`git diff --stat 71a29535..HEAD -- loom-code/contract loom-code/agents loom-code/skills/closing-review/references` → 空）。
- **第三次重測**：沿用 — 這個修正提交只改了三站說明、根目錄說明、CHANGELOG 與測試，沒有碰步驟清單、agent 定義、報告位置規則或範本；在新副本上實際執行「查看會跑哪些步驟」，清單裡仍是 `acceptance-test`。證據：`git diff --stat 0b4b5978..d6ac4f8d` 的 10 個檔案都不在 `loom-code/contract`、`loom-code/agents`、`closing-review/references` 之下；`selection show 2026-09-23-trial-typo` → `run` 含 `acceptance-test`。

### 2. No runtime file, identifier, test fixture or current-version documentation names `blind-run`, `blind-runner`, `blind run` or `blind runner`; only frozen records of merged changes and past CHANGELOG entries keep the old name.
- **我怎麼試**：對整個 repo 搜尋舊名稱的各種寫法（連字號、底線、空格、大小寫、中文舊稱），排除已合併改動的紀錄與 CHANGELOG，逐筆看剩下的結果。
- **結果**：三個 plugin 的程式、測試、流程說明、根目錄的說明文件裡都找不到舊名稱。只剩三處刻意保留：兩句「以前叫做 blind run」的對照說明（見第 4 條），以及原則文件裡記錄「這次改名由你批准」的歷史行。另外，專案的經驗筆記庫裡還有 12 份筆記用舊名稱描述過去的事件；它們不在這條的明確範圍內（見「我不確定你要的」）。
- **證據**：`git grep -n -i -I -E 'blind[-_ ]?run|盲跑' -- . ':!docs/loom/20*' ':!docs/loom/intent' ':!**/CHANGELOG.md'` → 只剩 `PRINCIPLES.md:2`（ratified-by）、`closing-review/SKILL.md:27`、`expert-mode/SKILL.md:31`（兩處皆 `formerly called "blind run"`），以及 `docs/loom/memory/` 12 個檔案
- **判定**：works — 會被執行或被讀來做事的檔案都乾淨了；經驗筆記庫的歸屬請你決定。
- **重測**：沿用上一輪 — 修正新增的文字裡沒有舊名稱；唯一沾邊的是一支測試刻意把舊代號拆成兩段拼起來，用來確認舊紀錄仍照原樣顯示。證據：`git diff c0e67085..HEAD | grep -i '^+.*blind'` → 只有 `retired = "blind" + "-run"`。
- **第二次重測**：沿用 — 這四個修正提交新增的文字裡同樣只有那一處刻意拆開的舊代號；在新副本上重搜，剩下的仍是上一輪列出的三處刻意保留加上經驗筆記庫。證據：`git diff 71a29535..HEAD | grep -i -E '^\+.*(blind|盲)'` → 只有 `retired = "blind" + "-run"`；`git grep -n -i -I -E 'blind[-_ ]?run|盲跑'`（排除同上，另排除 `docs/loom/memory`）→ `PRINCIPLES.md:2`、`closing-review/SKILL.md:27`、`expert-mode/SKILL.md:31`。
- **第三次重測（完整重做）**：這次修正在三個站的說明裡新增了含舊名稱的文字，所以整條重做。我在新副本上用同樣的方式重搜整個 repo。結果：刻意保留的地方從三處變成六處，多出來的三處正是新加的那句「以前叫做 blind run」對照句（規劃站、建置站、出貨站），寫法和原本兩處完全相同，屬於第 4 條要求的對照，不是殘留。修正新增的其他含舊名稱文字只在 CHANGELOG 的改名說明裡，那是這個版本的 release notes，本來就要講舊名稱。新納入掃描的兩份根目錄文件沒有舊名稱。經驗筆記庫仍是 12 份，沒有變化。
- **證據（第三次）**：`git grep -n -i -I -E 'blind[-_ ]?run|盲跑' -- . ':!docs/loom/20*' ':!docs/loom/intent' ':!**/CHANGELOG.md' ':!docs/loom/memory'` → `PRINCIPLES.md:2`（ratified-by）、`build/SKILL.md:24`、`closing-review/SKILL.md:27`、`expert-mode/SKILL.md:31`、`ship/SKILL.md:31`、`write-plan/SKILL.md:49`（後五處都是 `formerly called "blind run"`）；`git diff 0b4b5978..d6ac4f8d | grep -i -E '^\+.*(blind|盲)'` → 三行 `loom-code/CHANGELOG.md` 加三行 `formerly called "blind run"`；`docs/loom/memory` → 12 個檔案。
- **判定（第三次重測）**：works — 會被執行或被讀來做事的檔案裡，舊名稱只出現在刻意保留的對照句與批准紀錄；經驗筆記庫的歸屬仍請你決定（見下方）。

### 3. Text the user reads — the three READMEs, PRINCIPLES.md, station prose and the pull-request lines that list skipped steps — names the step "independent acceptance testing" on first use and never "UAT".
- **我怎麼試（重測）**：在 commit 7cd16d3 的新乾淨副本裡，用產生 PR 揭露行的函式，替一份「跳過了 acceptance test」的證明檔產生那一行；再拿三種 PR 內文去給發布前的檢查比對：寫出完整名稱的、只寫代號的（修正前的寫法）、以及一份已合併、含舊代號的真實證明檔配上它原本的那一行。接著讀出貨站的說明文字與白話用語指南。最後再搜一次獨立的「UAT」字樣。
- **結果**：PR 上那一行現在寫成 `acceptance-test (independent acceptance testing)`，你第一眼就看得到完整名稱。發布檢查接受這個寫法；只寫代號的舊寫法會被擋下，並印出正確的那一行。已合併的舊證明檔照它當初的紀錄顯示舊代號，比對通過、沒有報錯。出貨站的說明文字明寫：這一行裡的 `acceptance-test` 要寫成帶完整名稱的形式，其他步驟照紀錄寫。白話用語指南已不再把「independent acceptance testing」列為要換掉的內部用語。三份說明文件、根目錄說明、原則文件的第一次提及沿用上一輪的確認；除了 intent 本身說明為什麼不用「UAT」之外，沒有任何「UAT」。
- **證據**：`render_selection_disclosure`（`loom-code/scripts/loom_checker/rule_checks/publish.py`）→ `Skipped steps: acceptance-test (independent acceptance testing) — authority: user-typed (AB12, 2026-09-23)`；`validate_selection_disclosure`：完整名稱 → `None`（通過），只寫代號 → `PR body section 'Verification' must start with exactly the attestation's selection disclosure …`，舊證明檔 `docs/loom/2026-09-17-coexist-card-header/attestation.json` 配上 `Skipped steps: spec, plan, implementer, tdd, adversarial, blind-run — authority: user-typed (3NAV, 2026-09-17)` → `None`；`loom-code/skills/ship/SKILL.md:95-96`；`loom-workflow/skills/loom-visualization/references/plain-language.md` 的 Internal terms 清單（第 125-138 行）已無此詞；`git grep -n -w UAT -- '*.md' ':!docs/loom/20*' ':!**/CHANGELOG.md'` → 只有 intent 第 13、14、29 行。上一輪證據：`loom-code/README{,.ja,.zh-TW}.md` 第 23／25 行、`PRINCIPLES.md` 非協商原則第 2 條。
- **判定（上一輪，已更正）**：~~works — PR 上跳過步驟的那一行現在寫出完整名稱，其他使用者會讀到的文字上一輪就已做到。~~ 這個判定說得太滿：上一輪只試了「Skipped steps:」一行，另外三種列出跳過步驟的行沒有試。見下方第二次重測。
- **注意**：出貨站說明第一次提到這一步是在「acceptance test report」（第 19 行），講的是報告而不是步驟本身；完整名稱出現在第 96 行。我判定這樣符合，因為第 19 行並沒有用別的名字稱呼這個步驟。

**第二次重測（commit cc2b66b，逐行）**

PR 與對話裡列出被跳過步驟的共有四種行。我在新的乾淨副本上逐行試：每一行都看新代號是否寫成 `acceptance-test (independent acceptance testing)`、一份已合併且含舊代號的證明檔是否照它當初的紀錄顯示，以及有沒有出現 intent 明令不用的那個縮寫。

- **「Skipped steps:」行（PR 驗證區開頭，依證明檔產生）**
  - **我怎麼試**：用產生這一行的函式，分別替兩份已合併的舊證明檔，以及一份把舊代號換成新代號的複本產生這一行；再拿「寫完整名稱」與「只寫代號」兩種 PR 內文給發布前的檢查比對。
  - **結果**：新代號寫成完整名稱；兩份舊證明檔照原樣印出舊代號、沒有報錯。發布檢查接受完整名稱，只寫代號會被擋下並印出正確的那一行。
  - **證據**：`render_selection_disclosure` → 新代號複本 `Skipped steps: spec, plan, implementer, tdd, adversarial, acceptance-test (independent acceptance testing) — authority: user-typed (3NAV, 2026-09-17)`；舊證明檔 `2026-09-17-coexist-card-header`（commit 4d6337a2）→ `… adversarial, blind-run — authority: user-typed (3NAV, 2026-09-17)`；`2026-09-20-record-the-withdrawn-ordering-lesson`（commit 8cff3ec5）→ `… reviewers, adversarial, blind-run — authority: user-typed (L352, 2026-09-20)`；`validate_selection_disclosure`：完整名稱 → `None`，只寫代號 → `PR body section 'Verification' must start with exactly the attestation's selection disclosure …`
  - **判定**：works

- **「Verification status: valid (skipped: …)」行（PR 驗證狀態）**
  - **我怎麼試**：在新副本裡把兩個已合併改動當初的提交各開一份，用這次改動的檢查工具計算它們的驗證狀態；再對其中一份做一個把舊代號換成新代號的提交，同樣計算。
  - **結果**：新代號寫成完整名稱；舊代號照原樣印出、沒有報錯。
  - **證據**：`verification_status(..., depth="ci")` → 新代號 `valid (skipped: spec, plan, implementer, tdd, adversarial, acceptance-test (independent acceptance testing))`；commit 4d6337a2 → `valid (skipped: spec, plan, implementer, tdd, adversarial, blind-run)`；commit 8cff3ec5 → `valid (skipped: spec, plan, implementer, tdd, reviewers, adversarial, blind-run)`。同樣兩份用本機模式計算得到 `stale (attestation selection does not match the local selection records)`，原因是我的副本不在當初的分支上，跳過紀錄對不上分支；這和名稱無關，舊代號也沒有造成錯誤。
  - **判定**：works

- **「Skipped as a narrow change:」行（改動很小、自動跳過時，各站在對話裡說、出貨站寫進 PR）**
  - **我怎麼試**：在一份拷貝的專案裡，把主線設在這次改動的最新版，另開一個只加了一份 intent 和一行說明文字的小分支，實際執行「查看這次改動會跑哪些步驟」；再對這次改動本身（不算小改動）執行同一個指令。
  - **結果**：小改動的輸出多了一欄現成的那一行，新代號寫成完整名稱；不算小改動時那一欄是空的，出貨站的說明寫明這時不寫這一行。這一行的步驟永遠來自目前的步驟清單，不會出現舊代號；我另外直接把含舊代號的清單交給同一套寫法，舊代號照原樣保留。四站說明文字都改成「照這一欄原樣告訴使用者」。
  - **證據**：`loom_checker.py selection show 2026-09-23-narrow-probe` → exit 0，`"narrow_change_line": "Skipped as a narrow change: spec, plan, adversarial, acceptance-test (independent acceptance testing)"`；`selection show 2026-09-23-rename-blind-run-to-acceptance-testing` → `"bound": false`、`"narrow_change_line": null`；`plain_step_names(["spec", "blind-run"])` → `spec, blind-run`；發布檢查對含這一行的 PR 內文 → `None`；`loom-code/skills/ship/SKILL.md:88-90`，`build`／`closing-review`／`write-plan` 的 SKILL.md 同段
  - **判定**：works

- **「Skipped by instruction:」行（使用者用白話說要跳過時，出貨站寫進 PR）**
  - **我怎麼試**：讀出貨站說明；再把一份只寫代號的這一行放進 PR 內文，交給發布前的檢查。
  - **結果**：說明寫明這一行裡的 `acceptance-test` 要寫成帶完整名稱的形式、其他步驟照紀錄寫（照紀錄寫，也就代表舊代號會原樣保留）。但這一行只靠 agent 讀說明後自己寫：沒有任何程式產生它，發布檢查也刻意不檢查它，所以只寫代號的寫法會照樣通過。我沒有開一次真實的出貨對話去看 agent 實際怎麼寫。
  - **證據**：`loom-code/skills/ship/SKILL.md:84-87`、`:100-103`；`validate_selection_disclosure` 對含 `Skipped by instruction: acceptance-test` 的內文 → `None`（通過）；`STATUS_PREFIXES = ("Verification status:", "Skipped by instruction:")` 註明「always accepted, never validated」
  - **判定**：partly — 說明寫對了，但沒有東西保證這一行真的寫出完整名稱；上一輪被抓到的正是這類「只靠說明」的行。

- **不用的縮寫**：四種行的輸出、四個修正提交的差異、以及三份說明文件、原則文件與各站說明，都沒有出現 intent 明令不用的那個縮寫；唯一出現的是 intent 本身解釋為什麼不用它。證據：`git grep -n -w UAT -- . ':!docs/loom/20*' ':!**/CHANGELOG.md'` → 只有 intent 第 13、14、29 行；`git diff 71a29535..HEAD | grep -w UAT` → 無輸出。

- **判定（第二次重測）**：partly — 由程式產生的三種行（Skipped steps、Verification status、Skipped as a narrow change）都寫出完整名稱，舊紀錄照原樣顯示；只靠說明文字的「Skipped by instruction:」行沒有機制保證，也沒有在真實對話中試過。

**第三次重測（commit d6ac4f8，完整重做）**

這次修正改了三個站的說明文字與根目錄說明，這兩者都在第 3 條的範圍內，所以我把第 3 條點名的四類文字全部重試一次。

- **四份說明文件與原則文件**
  - **我怎麼試**：在新副本裡，對根目錄說明、loom-code 的英文／日文／中文說明、原則文件，逐一找出第一次提到這個步驟的那一行，看那一行是否就寫出完整名稱。
  - **結果**：五份文件第一次提到這個步驟時都寫出「independent acceptance testing」。根目錄說明這次只重新換行，「acceptance tester」「acceptance test report」這兩個詞出現在完整名稱之後。
  - **證據**：第一次提到＝完整名稱所在行：`README.md:6`、`loom-code/README.md:25`、`loom-code/README.ja.md:25`、`loom-code/README.zh-TW.md:23`、`PRINCIPLES.md:2`（批准紀錄）與 `:9`（非協商原則第 2 條）；`git diff 0b4b5978..d6ac4f8d -- README.md` 只有換行。
  - **判定**：works

- **各站說明**
  - **我怎麼試**：同樣逐站找出第一次提到這個步驟的那一行，和完整名稱第一次出現的那一行比較。
  - **結果**：建置站改好了，第一次提到時就寫成 `acceptance-test`（independent acceptance testing）。其他四處在第一次提到時仍只寫代號 `acceptance-test`，完整名稱在同一段、兩到七行之後才出現：規劃站和出貨站列出「可跳過的步驟」時只寫代號，而建置站同一句話已經改成帶完整名稱，三站寫法不一致。出貨站第一次提到的是「acceptance test report」（見上方「注意」）。進階選擇模式的步驟清單只寫代號，完整名稱在後面的對照句。沒有任何一站用別的名字稱呼這個步驟，也沒有出現那個縮寫。
  - **證據**：第一次提到行／完整名稱行：`build/SKILL.md` 20／20；`write-plan/SKILL.md` 46／48；`ship/SKILL.md` 19（報告）、28（代號）／30；`closing-review/SKILL.md` 24／26；`expert-mode/SKILL.md` 25／32。
  - **判定**：partly — 完整名稱都在同一段內出現，但嚴格照「第一次提到就寫完整名稱」來看，規劃站、出貨站、審查站、進階選擇模式還差一點；我在「我不確定你要的」列了這一題。

- **PR 上列出被跳過步驟的四種行**
  - **我怎麼試**：這次修正沒有改任何產生或檢查這些行的程式（`git diff --stat 0b4b5978..d6ac4f8d -- loom-code/scripts/loom_checker` → 空），但我仍重試：用產生「Skipped steps:」行的函式替兩份已合併的舊證明檔、以及把舊代號換成新代號的複本產生那一行，再拿完整名稱、只寫代號、以及加一行只寫代號的「Skipped by instruction:」的 PR 內文給發布前檢查比對；「Verification status」與「Skipped as a narrow change」兩行跑它們的針對性測試。
  - **結果**：新代號寫成完整名稱，舊證明檔照原樣印出舊代號、沒有報錯；只寫代號會被擋下。「Skipped by instruction:」行只寫代號仍會通過，和上一輪一樣。
  - **證據**：`render_selection_disclosure` → 新代號複本 `Skipped steps: spec, plan, implementer, tdd, adversarial, acceptance-test (independent acceptance testing) — authority: user-typed (3NAV, 2026-09-17)`；舊證明檔 `2026-09-17-coexist-card-header` → `… adversarial, blind-run — authority: user-typed (3NAV, 2026-09-17)`，`2026-09-20-record-the-withdrawn-ordering-lesson` → `… reviewers, adversarial, blind-run — authority: user-typed (L352, 2026-09-20)`；`validate_selection_disclosure`：完整名稱 → `None`，只寫代號 → `PR body section 'Verification' must start with exactly the attestation's selection disclosure …`，含 `Skipped by instruction: acceptance-test` → `None`；`pytest test_loom_publish.py test_verification_status.py test_simplified_station_text.py test_build_mechanical_checks.py -k "plain or narrow or skipped or acceptance or disclosure or selection"` → `33 passed`。我沒有重做上一輪「自己做一個小改動分支」的實測，因為這要強制移動分支指標，被安全防護擋下；那部分程式這次沒有改動。
  - **判定**：partly — 程式產生的三種行沒變、仍正確；「Skipped by instruction:」行仍沒有機制保證。

- **不用的縮寫**：四類文字與這次修正的差異裡都沒有；只剩 intent 本身解釋為什麼不用它。證據：`git grep -n -w -E 'U[A]T' -- . ':!docs/loom/20*' ':!**/CHANGELOG.md'` → 只有 intent 第 13、14、29 行；`git diff 0b4b5978..d6ac4f8d | grep -w -E 'U[A]T'` → 無輸出（搜尋式刻意用方括號寫，這份報告就不必寫出那個縮寫）。

- **判定（第三次重測）**：partly — 說明文件、原則文件、程式產生的 PR 行都做到了；「Skipped by instruction:」行仍只靠說明，另外四處站內說明第一次提到時只寫代號，完整名稱在同段稍後才出現。

### 4. A plain-words request to skip "acceptance testing", or the old "blind run", maps onto the renamed step.
- **我怎麼試**：查看負責執行這一步的站，以及進階的步驟選擇模式，是否寫明這兩種說法都對應到新步驟；再請檢查工具實際接受「跳過新步驟」與「跳過舊代號」兩種請求。
- **結果**：兩處說明都寫明「acceptance testing」和「以前叫做 blind run」都指新步驟。檢查工具接受新代號；舊代號被拒，並列出正確的步驟清單，所以「舊說法」只能靠 agent 讀說明後翻譯過去。我沒有開一個真實的 agent 對話去說「跳過 blind run」，實際翻譯行為未經測試。另外，規劃站與建置站的說明只寫「使用者用白話說要跳過就跳過」，沒有這條對照句。
- **證據**：`closing-review/SKILL.md:26-28`、`expert-mode/SKILL.md:30-32`；`validate_selection(["acceptance-test"])` → `[]`；`validate_selection(["blind-run"])` → `unknown step 'blind-run' (steps: spec, plan, implementer, tdd, reviewers, adversarial, acceptance-test, package-tests)`
- **判定**：partly — 對照文字在、新代號可用；agent 實際聽到舊說法時的行為我沒有試到。
- **重測**：沿用上一輪 — 修正沒有碰審查站、進階選擇模式的說明，也沒有碰檢查工具接受哪些步驟代號的部分。
- **第二次重測**：沿用 — 審查站說明這次只改了「改動很小時怎麼告訴你」那一段，第 26-28 行的對照句沒動；進階選擇模式與步驟代號清單都不在修正差異裡。
- **補充說明（第三次重測）**：前兩輪的「沿用」只證明對照句沒被改壞，判定一直是 partly：規劃站與建置站缺這句對照，也從沒開過真實對話。這一輪的修正補上了缺的那兩站（外加出貨站），所以我整條重做。

**第三次重測（commit d6ac4f8，完整重做，含真實對話）**
- **我怎麼試**：先在新副本裡逐站確認對照句：規劃站、建置站、審查站、出貨站、進階選擇模式。再從這個分支的版本載入 loom-code plugin（沒有載入我平常安裝的版本），在一份拷貝的專案裡為一個只修一個錯字的小改動寫一份 intent，然後開真實的 agent 對話：對規劃站、建置站、出貨站、進階選擇模式說「這次跳過 blind run，diff 我自己看」，對審查站說「這次跳過 acceptance testing」，要它照該站的進場步驟做完，用一行告訴我跳過哪一步、代號是什麼，然後停下，不派任何 agent、不改檔。最後做一個對照組：用修正前（commit 0b4b597，建置站還沒有對照句）的版本重跑建置站那一場。
- **結果**：五個地方都有同一句對照（進階選擇模式用自己的寫法，意思相同）。五場對話都把使用者的話對到 `acceptance-test`，並用完整名稱回報。規劃站、建置站、審查站、出貨站那四場都確實載入了該站，並先跑了「查看會跑哪些步驟」；進階選擇模式只能由使用者打指令叫出，第一場 agent 是自己打開那個站的說明檔來讀，第二場我用指令直接叫它，也對到同一個代號，但從輸出看不出站的說明有沒有被載入。對照組：修正前的建置站也對對了，所以這次在真實對話裡看到的正確行為，不能全算在新加的那句上，模型本身就猜得出來；新句子讓它不必靠猜。另外，路由入口（使用者沒指定站時的分派說明）也寫著「使用者用白話要求就跳過」，卻沒有這句對照；它會把人交給各站，各站現在都有，所以我判定不影響結果。檢查工具本身仍不接受舊代號，對照只靠 agent 讀說明。
- **證據**：對照句：`write-plan/SKILL.md:48-50`、`build/SKILL.md:23-25`、`closing-review/SKILL.md:26-28`、`ship/SKILL.md:30-32`、`expert-mode/SKILL.md:30-32`；`test_legacy_contract_removed.py::test_every_station_honouring_plain_words_skips_maps_the_old_name` 通過。真實對話（`claude -p --plugin-dir <分支副本>/loom-code`，初始化訊息顯示 `loom-code@inline 3.10.0` 指向分支副本）：
  - 規劃站：`Skill loom-code:write-plan` → `selection show` → 「I'm skipping independent acceptance testing (the step formerly called "blind run"); its exact step id is `acceptance-test`.」
  - 建置站：`Skill loom-code:build` → `selection show` → 「Skipping independent acceptance testing (the old "blind run"), step id `acceptance-test`.」
  - 審查站（新說法）：`Skill loom-code:closing-review` → `selection show` → 「I'm skipping independent acceptance testing because you asked to: step id `acceptance-test`.」
  - 出貨站：`Skill loom-code:ship` → `selection show` → 「I'm skipping independent acceptance testing (the step that used to be called "blind run"), as you asked; its step id is `acceptance-test`.」
  - 進階選擇模式：agent 讀 `loom-code/skills/expert-mode/SKILL.md` → 「Skipping the step formerly called "blind run", which is now independent acceptance testing. Its step id is `acceptance-test`.」；以 `/loom-code:expert-mode` 指令叫出 → 「I'd skip step `acceptance-test`. "Blind run" is the old name for independent acceptance testing.」
  - 對照組（修正前的建置站）：「I'm skipping the acceptance test (it used to be called the "blind run"); its step id is `acceptance-test`.」
- **判定（第三次重測）**：works — 五個會處理白話跳過的地方都寫明兩種說法對到新步驟，真實對話裡四個站與進階選擇模式都照做。保留兩點：進階選擇模式的說明是否真的被載入，我從輸出確認不了；對照組顯示模型不靠這句也猜得對。

### 5. Attestations and reports of merged changes are left as they are, and nothing that runs afterwards fails on them.
- **我怎麼試**：比對這個分支與主線在已合併改動紀錄上的差異；對主線上含舊代號的證明檔，實際跑「列出曾跳過審查的已合併改動」、查看一個舊改動的步驟狀態、以及產生舊證明檔在 PR 上的揭露行。
- **結果**：44 份證明檔、24 份舊名稱報告、經驗筆記庫，都沒有被改動。三個指令都正常結束，舊代號原樣印出，沒有報錯。
- **證據**：`git diff --stat main...HEAD -- 'docs/loom/*/attestation.json' 'docs/loom/*/blind-run-report.md' docs/loom/memory` → 空；`loom_checker.py selection skipped-review` → exit 0，輸出 `2026-09-20-record-the-withdrawn-ordering-lesson 8cff3ec5 skipped: spec, plan, implementer, tdd, reviewers, adversarial, blind-run`；`selection show 2026-09-20-record-the-withdrawn-ordering-lesson` → exit 0；舊證明檔的揭露行 → `Skipped steps: spec, plan, implementer, tdd, reviewers, adversarial, blind-run — authority: user-typed (L352, 2026-09-20)`
- **判定**：works — 舊紀錄沒動，之後會讀它們的指令都照常運作。
- **重測**：沿用上一輪，並補查一處 — 這次修正確實改了產生 PR 揭露行的函式，所以我對舊證明檔重新產生一次：`2026-09-20-record-the-withdrawn-ordering-lesson` 的輸出與上一輪逐字相同，`2026-09-17-coexist-card-header` 也照原樣印出舊代號、沒有報錯。修正只替新代號加上完整名稱，舊代號原樣通過。
- **第二次重測**：沿用，並補查一處 — 修正沒有動任何已合併紀錄，但這次改了會讀舊證明檔的驗證狀態計算，所以我對兩份含舊代號的已合併證明檔重新計算：都正常得出 `valid (skipped: … blind-run)`、沒有報錯（詳見第 3 條第二次重測）。
- **第三次重測**：沿用 — 這個修正提交沒有動任何已合併紀錄，也沒有改會讀它們的程式（`git diff --stat 0b4b5978..d6ac4f8d -- 'docs/loom/*/attestation.json' docs/loom/memory loom-code/scripts/loom_checker` → 空）；CHANGELOG 只是把「之後的指令照常處理舊紀錄」說得更清楚。我在新副本上順手重新產生兩份舊證明檔的 PR 揭露行，仍照原樣印出舊代號、沒有報錯（見第 3 條第三次重測）。

### 6. A check fails the repository if one of the old names reappears in a runtime file.
- **我怎麼試**：在乾淨副本裡故意把舊名稱放回兩個地方（一句出貨站說明文字用空格寫法、一處程式的步驟集合用底線寫法），跑那支檢查，然後改回原樣再跑一次。
- **結果**：放回後檢查失敗，並精確指出兩個位置；改回後恢復通過。這支檢查屬於 CI 每次都會跑的套件。
- **證據**：`pytest loom-code/scripts/test_legacy_contract_removed.py::test_no_runtime_file_names_the_retired_step_name` → `1 failed`，hits `['loom-code/scripts/loom_checker/reviewers.py:30', 'loom-code/skills/ship/SKILL.md:19']`；還原後 `test_legacy_contract_removed.py` → `8 passed`；CI `loom-code-ci.yml` 以 `run_package_tests.py --loom-family --only code` 執行整個套件
- **判定**：works — 舊名稱一回來就會擋下。
- **重測**：沿用上一輪 — 修正沒有碰這支檢查；我在新副本上只重跑了它，確認修正新增的文字沒有觸發它：`test_legacy_contract_removed.py` → `8 passed`。
- **第二次重測**：沿用，證據更新 — 修正刪掉了一支和這支檢查重複的測試，並把搜尋範圍從三個 plugin 擴大到根目錄的工具資料夾（`scripts/`、`.claude/`、`.claude-plugin/`、`.github/`），另加一項測試確認範圍包含它們。我在新副本上重跑整支檢查，再在新納入的 `.github/` 裡暫時放一個寫著舊名稱的檔案，檢查當場失敗並指出位置；移除後恢復通過。證據：`pytest loom-code/scripts/test_legacy_contract_removed.py` → `9 passed`；暫放 `.github/probe_retired.md` 後 `::test_no_runtime_file_names_the_retired_step_name` → `AssertionError: assert ['.github/probe_retired.md:1'] == []`，`1 failed`；移除後 → `9 passed`。
- **第三次重測（完整重做）**：這次修正把兩份根目錄文件（新手預設說明、給 agent 的專案說明）加進檢查範圍，並加了一支測試確認四個站都有對照句，所以整條重做。我在新副本上先跑整支檢查；再同時在三個地方放回舊名稱：新納入的兩份文件各加一行（一個用「blind runner」、一個用底線寫法），以及把規劃站的對照句改成直接寫舊代號；跑檢查後用程式還原原文，再跑一次。
- **結果**：放回後兩項檢查同時失敗：改名檢查指出三個位置（第一個是專案說明第 3 行，最後一個是規劃站說明第 49 行），對照句檢查指出規劃站缺了那句。還原後恢復通過，副本沒有留下任何改動。
- **證據（第三次）**：`pytest loom-code/scripts/test_legacy_contract_removed.py` → `10 passed`；放回後 → `2 failed, 8 passed`：`test_no_runtime_file_names_the_retired_step_name` → `AssertionError: assert ['CLAUDE.md:3.../SKILL.md:49'] == []`（`Left contains 3 more items, first extra item: 'CLAUDE.md:3'`），`test_every_station_honouring_plain_words_skips_maps_the_old_name` → `AssertionError: write-plan`；還原後 → `10 passed`，`git status --short` 無輸出。
- **判定（第三次重測）**：works — 舊名稱在新納入的文件裡一出現就擋下，拿掉某站的對照句也會擋下。

### 附帶確認（對應你設下的限制）
- 檢查工具的規則清單在主線與這個分支上完全相同（26 行，逐字比對無差異）。證據：`loom_checker.py --list-rules` 兩邊 `diff` → 無輸出。
- 版號是 minor 升級（3.9.0 → 3.10.0），release notes 有寫進行中改動的影響。

## Review summary

這份報告只涵蓋 acceptance testing。兩位 fresh-context reviewer 的審查還沒交到我手上，所以這裡沒有審查結論可以摘要；結論會在審查完成後另外呈現給你。

## Questions I asked you

沒有——這次試驗過程中我沒有問你任何問題。

## 對你既有的資料做了什麼 (what this did to data you already had)

這次改動沒有改寫任何你已有的紀錄：已合併改動的證明檔、舊報告、經驗筆記都原封不動，舊代號仍然讀得到，指令照常處理它們，所以不需要備份。唯一會碰到的是**另一個 repo 裡還沒合併、而且已經用舊代號記錄過「跳過哪些步驟」的改動**：升級後，檢查工具不再認得舊代號，重新提出跳過請求時會被要求改用新代號。這件事 release notes 有寫，但我沒有在真實的進行中改動上試過。（第三次重測補充：release notes 現在多寫了一種情況，進行中的改動如果已經提交了舊檔名的驗收報告，升級後會被要求重做一次 acceptance testing，除非先把檔案改成新檔名。這一點我同樣沒有實際試過。）

## I decided for you

- **經驗筆記庫算不算「會被讀來做事的檔案」** — 我把它當作「過去改動的紀錄」看待，所以第 2 條判 works。這 12 份筆記會被 agent 回想時讀到，其中幾份的建議仍用舊名稱描述現行做法。如果你認為它們屬於現行文件，第 2 條應改判 partly，要補一次筆記改寫。
- **沒有開真實 agent 對話測試白話跳過** — 我判斷這需要一整套載入分支版本 plugin 的對話環境，所以第 4 條只驗證了說明文字與檢查工具，並判 partly，沒有宣稱可行。
- **只跑了針對性測試** — 依照指示，整個套件已在這個版本通過，我只跑了改名檢查那支測試。
- **審查者駁回的重要發現** — 沒有收到任何一筆，所以這裡無可列。
- **（重測）出貨站說明的「第一次提及」怎麼算** — 第一次出現的是「acceptance test report」這份報告，完整步驟名稱在稍後才出現。我把它算作符合第 3 條，因為那裡沒有用其他名字稱呼這個步驟；如果你要求連報告的第一次出現也帶上完整名稱，第 3 條要改判 partly。
- **（重測）只重測第 3 條** — 其他各條沿用上一輪，理由寫在各條下方；我核對過修正的完整差異，才寫下那些理由。
- **（第二次重測）用自己做的小改動來試「改動很小」那一行** — 這個 repo 裡沒有現成的小改動分支，所以我在一份拷貝的專案裡自己做了一個（只加一份 intent 和一行說明文字），試完就刪掉。
- **（第二次重測）用改過代號的舊證明檔複本來試新代號** — 手邊沒有一份記錄了新代號的真實證明檔，所以我把一份已合併的證明檔複本裡的舊代號換成新代號來產生那兩行。真正的舊證明檔沒有被改動。
- **（第二次重測）「Skipped by instruction:」行判 partly** — 說明文字寫對了，但沒有東西產生或檢查這一行，我也沒有開真實的出貨對話。我沒有把「說明寫對了」當成「做到了」。
- **（第三次重測）更正上面「沒有開真實 agent 對話」那一條** — 這一輪開了：用分支版本的 plugin 在拷貝的專案裡跑了六場很短的對話（五場各試一個地方，一場修正前版本的對照組），每場都叫它照進場步驟做完就停，不派 agent、不改檔。所以第 4 條改判 works。對話只做到「對出哪個步驟」，沒有讓它真的把跳過紀錄寫進計畫檔、也沒有走完整個站。
- **（第三次重測）站內說明「第一次提到只寫代號」算不算違反第 3 條** — 我判它 partly，而不是像上一輪對出貨站「報告」那一處那樣放過，因為這次看到的是步驟本身的代號，而且建置站同一句話已經改成帶完整名稱，另外兩站沒跟上。如果你認為代號出現在步驟清單裡不算「稱呼這個步驟」，這一項就是 works。
- **（第三次重測）沒有重做「改動很小」那一行的實測** — 要重現它得強制移動副本的分支指標，被安全防護擋下。產生那一行的程式這次沒有改，我改跑它的針對性測試。
- **（第三次重測）只重測第 2、3、4、6 條** — 修正改了站內說明與根目錄說明（第 3 條）、新增含舊名稱的對照句（第 2、4 條）、擴大改名檢查的範圍（第 6 條）；第 1、5 條涉及的檔案與程式都不在差異裡。

## Things I am not sure you want

- ~~PR 上列出被跳過步驟時只寫 `acceptance-test` 這個代號，你是否希望旁邊也寫出「independent acceptance testing」？~~ 已解決（重測）：現在寫成 `acceptance-test (independent acceptance testing)`，見第 3 條。
- （第二次重測）「Skipped by instruction:」這一行要不要也像另外三行一樣，由檢查工具產生或檢查，而不是只靠 agent 讀說明？目前只寫代號的寫法會照樣通過發布檢查。
- 經驗筆記庫裡用舊名稱的 12 份筆記，要保留原樣當歷史，還是改寫成新名稱？
- ~~規劃站與建置站也要加上「blind run 就是 acceptance testing」這句對照嗎？目前只有審查站與進階選擇模式有。~~ 已解決（第三次重測）：規劃站、建置站、出貨站都加上了，見第 4 條。
- （第三次重測）規劃站、出貨站列出可跳過步驟時，要不要像建置站一樣寫成 `acceptance-test`（independent acceptance testing）？審查站與進階選擇模式第一次提到時也只寫代號。見第 3 條。
- （第三次重測）使用者沒指定站時負責分派的路由說明，也寫著「使用者用白話要求就跳過」，但沒有這句對照。它會把人交給各站，各站都有，所以我判定不影響結果；要不要也加上，請你決定。
- 原則文件寫著這次改名「由你於 2026-09-23 批准」。依你的規矩，這要你親自批准；我無法從檔案確認你真的批准過，請你確認一次。
- ~~內部用語清單把「independent acceptance testing」列為對你說話時要換成白話的詞，但第 3 條又要求它作為對你顯示的正式名稱。兩者要怎麼並存？~~ 已解決（重測）：這個詞已從內部用語清單移除，不再衝突。
- 這次改動的資料夾裡沒有規劃文件（其他類似改動有的有、有的沒有），這是你預期的嗎？

## 英文規則與範本規則是否守住

| 項目 | 英文規則 | 範本規則 | 證據 |
|---|---|---|---|
| 規劃文件 | 無法判定——分支上找不到 | 不適用 | `docs/loom/2026-09-23-rename-blind-run-to-acceptance-testing/` 內無 `plan.md` |
| 設計規格 | 不適用——這次不需要設計 | 不適用（EARS `REQ-<n>`） | intent `needs-design: no` |
| 審查發現 | 尚未產生 | 尚未產生（Conventional Comments label） | 審查尚未交付 |
| 證據檔 | 守住 | 不適用 | `ab/protocol.md`、`ab/results.md`、`evidence/ab-*/*.stderr.txt` 為英文 |
| 測試說明文字 | 守住 | 不適用 | `test_legacy_contract_removed.py`、`test_loom_publish.py`、`test_verification_status.py` 的模組與函式 docstring 為英文（第二次重測：原先列的 `test_adversarial_rename_guard_near_miss.py` 已刪除） |
| 測試名稱 | 守住 | 部分守住：多數符合 `test_<unit>_<state>_<expected>`，少數不符 | 符合：`test_skipped_status_names_the_acceptance_step_in_plain_words`、`test_show_renders_the_narrow_change_line`；不符：`test_retired_step_name_helper_synthetic`、`test_no_runtime_file_names_the_retired_step_name`；第三次重測新增的 `test_every_station_honouring_plain_words_skips_maps_the_old_name` 與改名後的 `test_plain_step_names_renders_every_pr_step_list` 也不符 |
| Commit 訊息 | 守住 | 守住（Conventional Commits） | `git log --format=%s main..HEAD` 23 筆（第三次重測時）皆為 `type(scope): …` 英文 |
