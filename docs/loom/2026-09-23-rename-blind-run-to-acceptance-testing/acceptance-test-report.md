# 把舊名稱的驗收步驟改名為 independent acceptance testing — 我試了什麼、結果如何

2026-09-23 在一份乾淨的專案副本（commit 71e6978）上試過。我沒有參與這次改動的任何實作。

**2026-09-23 重測（commit 7cd16d3）**：修正提交後，由另一位沒有參與實作的測試者在新的乾淨副本上只重測第 3 條。第 1、2、4、5、6 條沿用上一輪的結果，各條下方寫了理由。這兩個修正提交只改了三樣東西：PR 上「跳過了哪些步驟」那一行的產生方式、出貨站的說明文字、給 agent 的白話用語指南（外加對應的兩支測試）。

## 你要的東西，一條一條看

### 1. The step id is `acceptance-test`, the agent is dispatched as `loom-code:acceptance-tester`, and the report is written at `docs/loom/<change-id>/acceptance-test-report.md` from a template of the same name.
- **我怎麼試**：在乾淨副本裡請檢查工具列出這次改動會跑哪些步驟；查看 agent 清單與它的名稱；查看報告的存放位置規則與範本檔。
- **結果**：步驟清單裡出現的是新的 step id，舊 id 不在其中；agent 以新名字存在；報告位置規則與範本都用新名字。我這份報告本身就是照新範本、寫在新位置。
- **證據**：`loom_checker.py selection show 2026-09-23-rename-blind-run-to-acceptance-testing` → `run` 含 `acceptance-test`；`loom-code/agents/acceptance-tester.md`（frontmatter `name: acceptance-tester`）；manifest `artifacts.acceptance-test-report.path = docs/loom/<change-id>/acceptance-test-report.md`；範本 `loom-code/skills/closing-review/references/acceptance-test-report.md`
- **判定**：works — 三個名字都已換成新的。
- **重測**：沿用上一輪 — 修正沒有碰步驟清單、agent 定義、報告位置規則或範本。

### 2. No runtime file, identifier, test fixture or current-version documentation names `blind-run`, `blind-runner`, `blind run` or `blind runner`; only frozen records of merged changes and past CHANGELOG entries keep the old name.
- **我怎麼試**：對整個 repo 搜尋舊名稱的各種寫法（連字號、底線、空格、大小寫、中文舊稱），排除已合併改動的紀錄與 CHANGELOG，逐筆看剩下的結果。
- **結果**：三個 plugin 的程式、測試、流程說明、根目錄的說明文件裡都找不到舊名稱。只剩三處刻意保留：兩句「以前叫做 blind run」的對照說明（見第 4 條），以及原則文件裡記錄「這次改名由你批准」的歷史行。另外，專案的經驗筆記庫裡還有 12 份筆記用舊名稱描述過去的事件；它們不在這條的明確範圍內（見「我不確定你要的」）。
- **證據**：`git grep -n -i -I -E 'blind[-_ ]?run|盲跑' -- . ':!docs/loom/20*' ':!docs/loom/intent' ':!**/CHANGELOG.md'` → 只剩 `PRINCIPLES.md:2`（ratified-by）、`closing-review/SKILL.md:27`、`expert-mode/SKILL.md:31`（兩處皆 `formerly called "blind run"`），以及 `docs/loom/memory/` 12 個檔案
- **判定**：works — 會被執行或被讀來做事的檔案都乾淨了；經驗筆記庫的歸屬請你決定。
- **重測**：沿用上一輪 — 修正新增的文字裡沒有舊名稱；唯一沾邊的是一支測試刻意把舊代號拆成兩段拼起來，用來確認舊紀錄仍照原樣顯示。證據：`git diff c0e67085..HEAD | grep -i '^+.*blind'` → 只有 `retired = "blind" + "-run"`。

### 3. Text the user reads — the three READMEs, PRINCIPLES.md, station prose and the pull-request lines that list skipped steps — names the step "independent acceptance testing" on first use and never "UAT".
- **我怎麼試（重測）**：在 commit 7cd16d3 的新乾淨副本裡，用產生 PR 揭露行的函式，替一份「跳過了 acceptance test」的證明檔產生那一行；再拿三種 PR 內文去給發布前的檢查比對：寫出完整名稱的、只寫代號的（修正前的寫法）、以及一份已合併、含舊代號的真實證明檔配上它原本的那一行。接著讀出貨站的說明文字與白話用語指南。最後再搜一次獨立的「UAT」字樣。
- **結果**：PR 上那一行現在寫成 `acceptance-test (independent acceptance testing)`，你第一眼就看得到完整名稱。發布檢查接受這個寫法；只寫代號的舊寫法會被擋下，並印出正確的那一行。已合併的舊證明檔照它當初的紀錄顯示舊代號，比對通過、沒有報錯。出貨站的說明文字明寫：這一行裡的 `acceptance-test` 要寫成帶完整名稱的形式，其他步驟照紀錄寫。白話用語指南已不再把「independent acceptance testing」列為要換掉的內部用語。三份說明文件、根目錄說明、原則文件的第一次提及沿用上一輪的確認；除了 intent 本身說明為什麼不用「UAT」之外，沒有任何「UAT」。
- **證據**：`render_selection_disclosure`（`loom-code/scripts/loom_checker/rule_checks/publish.py`）→ `Skipped steps: acceptance-test (independent acceptance testing) — authority: user-typed (AB12, 2026-09-23)`；`validate_selection_disclosure`：完整名稱 → `None`（通過），只寫代號 → `PR body section 'Verification' must start with exactly the attestation's selection disclosure …`，舊證明檔 `docs/loom/2026-09-17-coexist-card-header/attestation.json` 配上 `Skipped steps: spec, plan, implementer, tdd, adversarial, blind-run — authority: user-typed (3NAV, 2026-09-17)` → `None`；`loom-code/skills/ship/SKILL.md:95-96`；`loom-workflow/skills/loom-visualization/references/plain-language.md` 的 Internal terms 清單（第 125-138 行）已無此詞；`git grep -n -w UAT -- '*.md' ':!docs/loom/20*' ':!**/CHANGELOG.md'` → 只有 intent 第 13、14、29 行。上一輪證據：`loom-code/README{,.ja,.zh-TW}.md` 第 23／25 行、`PRINCIPLES.md` 非協商原則第 2 條。
- **判定**：works — PR 上跳過步驟的那一行現在寫出完整名稱，其他使用者會讀到的文字上一輪就已做到。
- **注意**：出貨站說明第一次提到這一步是在「acceptance test report」（第 19 行），講的是報告而不是步驟本身；完整名稱出現在第 96 行。我判定這樣符合，因為第 19 行並沒有用別的名字稱呼這個步驟。

### 4. A plain-words request to skip "acceptance testing", or the old "blind run", maps onto the renamed step.
- **我怎麼試**：查看負責執行這一步的站，以及進階的步驟選擇模式，是否寫明這兩種說法都對應到新步驟；再請檢查工具實際接受「跳過新步驟」與「跳過舊代號」兩種請求。
- **結果**：兩處說明都寫明「acceptance testing」和「以前叫做 blind run」都指新步驟。檢查工具接受新代號；舊代號被拒，並列出正確的步驟清單，所以「舊說法」只能靠 agent 讀說明後翻譯過去。我沒有開一個真實的 agent 對話去說「跳過 blind run」，實際翻譯行為未經測試。另外，規劃站與建置站的說明只寫「使用者用白話說要跳過就跳過」，沒有這條對照句。
- **證據**：`closing-review/SKILL.md:26-28`、`expert-mode/SKILL.md:30-32`；`validate_selection(["acceptance-test"])` → `[]`；`validate_selection(["blind-run"])` → `unknown step 'blind-run' (steps: spec, plan, implementer, tdd, reviewers, adversarial, acceptance-test, package-tests)`
- **判定**：partly — 對照文字在、新代號可用；agent 實際聽到舊說法時的行為我沒有試到。
- **重測**：沿用上一輪 — 修正沒有碰審查站、進階選擇模式的說明，也沒有碰檢查工具接受哪些步驟代號的部分。

### 5. Attestations and reports of merged changes are left as they are, and nothing that runs afterwards fails on them.
- **我怎麼試**：比對這個分支與主線在已合併改動紀錄上的差異；對主線上含舊代號的證明檔，實際跑「列出曾跳過審查的已合併改動」、查看一個舊改動的步驟狀態、以及產生舊證明檔在 PR 上的揭露行。
- **結果**：44 份證明檔、24 份舊名稱報告、經驗筆記庫，都沒有被改動。三個指令都正常結束，舊代號原樣印出，沒有報錯。
- **證據**：`git diff --stat main...HEAD -- 'docs/loom/*/attestation.json' 'docs/loom/*/blind-run-report.md' docs/loom/memory` → 空；`loom_checker.py selection skipped-review` → exit 0，輸出 `2026-09-20-record-the-withdrawn-ordering-lesson 8cff3ec5 skipped: spec, plan, implementer, tdd, reviewers, adversarial, blind-run`；`selection show 2026-09-20-record-the-withdrawn-ordering-lesson` → exit 0；舊證明檔的揭露行 → `Skipped steps: spec, plan, implementer, tdd, reviewers, adversarial, blind-run — authority: user-typed (L352, 2026-09-20)`
- **判定**：works — 舊紀錄沒動，之後會讀它們的指令都照常運作。
- **重測**：沿用上一輪，並補查一處 — 這次修正確實改了產生 PR 揭露行的函式，所以我對舊證明檔重新產生一次：`2026-09-20-record-the-withdrawn-ordering-lesson` 的輸出與上一輪逐字相同，`2026-09-17-coexist-card-header` 也照原樣印出舊代號、沒有報錯。修正只替新代號加上完整名稱，舊代號原樣通過。

### 6. A check fails the repository if one of the old names reappears in a runtime file.
- **我怎麼試**：在乾淨副本裡故意把舊名稱放回兩個地方（一句出貨站說明文字用空格寫法、一處程式的步驟集合用底線寫法），跑那支檢查，然後改回原樣再跑一次。
- **結果**：放回後檢查失敗，並精確指出兩個位置；改回後恢復通過。這支檢查屬於 CI 每次都會跑的套件。
- **證據**：`pytest loom-code/scripts/test_legacy_contract_removed.py::test_no_runtime_file_names_the_retired_step_name` → `1 failed`，hits `['loom-code/scripts/loom_checker/reviewers.py:30', 'loom-code/skills/ship/SKILL.md:19']`；還原後 `test_legacy_contract_removed.py` → `8 passed`；CI `loom-code-ci.yml` 以 `run_package_tests.py --loom-family --only code` 執行整個套件
- **判定**：works — 舊名稱一回來就會擋下。
- **重測**：沿用上一輪 — 修正沒有碰這支檢查；我在新副本上只重跑了它，確認修正新增的文字沒有觸發它：`test_legacy_contract_removed.py` → `8 passed`。

### 附帶確認（對應你設下的限制）
- 檢查工具的規則清單在主線與這個分支上完全相同（26 行，逐字比對無差異）。證據：`loom_checker.py --list-rules` 兩邊 `diff` → 無輸出。
- 版號是 minor 升級（3.9.0 → 3.10.0），release notes 有寫進行中改動的影響。

## Review summary

這份報告只涵蓋 acceptance testing。兩位 fresh-context reviewer 的審查還沒交到我手上，所以這裡沒有審查結論可以摘要；結論會在審查完成後另外呈現給你。

## Questions I asked you

沒有——這次試驗過程中我沒有問你任何問題。

## 對你既有的資料做了什麼 (what this did to data you already had)

這次改動沒有改寫任何你已有的紀錄：已合併改動的證明檔、舊報告、經驗筆記都原封不動，舊代號仍然讀得到，指令照常處理它們，所以不需要備份。唯一會碰到的是**另一個 repo 裡還沒合併、而且已經用舊代號記錄過「跳過哪些步驟」的改動**：升級後，檢查工具不再認得舊代號，重新提出跳過請求時會被要求改用新代號。這件事 release notes 有寫，但我沒有在真實的進行中改動上試過。

## I decided for you

- **經驗筆記庫算不算「會被讀來做事的檔案」** — 我把它當作「過去改動的紀錄」看待，所以第 2 條判 works。這 12 份筆記會被 agent 回想時讀到，其中幾份的建議仍用舊名稱描述現行做法。如果你認為它們屬於現行文件，第 2 條應改判 partly，要補一次筆記改寫。
- **沒有開真實 agent 對話測試白話跳過** — 我判斷這需要一整套載入分支版本 plugin 的對話環境，所以第 4 條只驗證了說明文字與檢查工具，並判 partly，沒有宣稱可行。
- **只跑了針對性測試** — 依照指示，整個套件已在這個版本通過，我只跑了改名檢查那支測試。
- **審查者駁回的重要發現** — 沒有收到任何一筆，所以這裡無可列。
- **（重測）出貨站說明的「第一次提及」怎麼算** — 第一次出現的是「acceptance test report」這份報告，完整步驟名稱在稍後才出現。我把它算作符合第 3 條，因為那裡沒有用其他名字稱呼這個步驟；如果你要求連報告的第一次出現也帶上完整名稱，第 3 條要改判 partly。
- **（重測）只重測第 3 條** — 其他各條沿用上一輪，理由寫在各條下方；我核對過修正的完整差異，才寫下那些理由。

## Things I am not sure you want

- ~~PR 上列出被跳過步驟時只寫 `acceptance-test` 這個代號，你是否希望旁邊也寫出「independent acceptance testing」？~~ 已解決（重測）：現在寫成 `acceptance-test (independent acceptance testing)`，見第 3 條。
- 經驗筆記庫裡用舊名稱的 12 份筆記，要保留原樣當歷史，還是改寫成新名稱？
- 規劃站與建置站也要加上「blind run 就是 acceptance testing」這句對照嗎？目前只有審查站與進階選擇模式有。
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
| 測試說明文字 | 守住 | 不適用 | `test_adversarial_rename_guard_near_miss.py` 等模組與函式 docstring 為英文 |
| 測試名稱 | 守住 | 部分守住：多數符合 `test_<unit>_<state>_<expected>`，少數不符 | 符合：`test_rename_guard_underscore_form_is_flagged`；不符：`test_retired_step_name_helper_synthetic`、`test_no_runtime_file_names_the_retired_step_name` |
| Commit 訊息 | 守住 | 守住（Conventional Commits） | `git log --format=%s main..HEAD` 13 筆皆為 `type(scope): …` 英文 |
