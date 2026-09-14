# A/B protocol — loom-visualization description on Loom station reporting prompts

The decision rule comes from intent Acceptance 3 at commit `5cf73116`; the
prompts and measures were written before the runs but committed together with
the results (task W1-01, intent Acceptance 2, 3, 4).

## Variants

- **A** — the description at HEAD `6ad80799`, unchanged:
  `Show comparisons, flows, decisions, states or reasoning chains as tables, ASCII or Mermaid in coding chat; not Obsidian notes.`
  Rendered SHA-256 `6c65729a01ccc3b9cc81d7387b163d4b61dd1d0a26386ea69a10cad8d370f64c`.
- **B** — the candidate, exact text:
  `Show comparisons, flows, decisions, states or reasoning chains as tables, ASCII or Mermaid in coding chat, including when a Loom station reports to the user (intent restatement, choices, blind-run results); not Obsidian notes.`
  Rendered SHA-256 `e98a3ed165415900bf405fe07209dde634cd465ff035fbea4ac2c73f57f6fd45`.

Budget check before running, using `_description` from
`scripts/test_loom_skill_description_catalog.py`: with B swapped in, the total
rendered Loom description length is 2,988 characters, within the 4,047 budget
(and within 60% of the 6,746 baseline). A alone renders 126 characters and
B 226.

## Plugin copies

1. `git archive 6ad80799 loom-code loom-design loom-workflow` is extracted into
   `<scratchpad>/ab-desc/A/` and `<scratchpad>/ab-desc/B/`.
2. In B only, the description block of
   `loom-workflow/skills/loom-visualization/SKILL.md` is replaced with B.
3. `run_ab.py build` compares the two trees file by file and fails unless the
   only difference is that one SKILL.md, whose rendered descriptions are A and B
   respectively and whose B hash equals the value above.

## Session shape

Each session runs from a fresh, empty, non-git working directory under the
scratchpad:

```
claude -p "<prompt>" --output-format stream-json --verbose \
  --plugin-dir <variant>/loom-code \
  --plugin-dir <variant>/loom-design \
  --plugin-dir <variant>/loom-workflow \
  --settings '{"enabledPlugins": {<every key of ~/.claude/settings.json enabledPlugins>: false}}'
```

- Only the `enabledPlugins` keys are read from `~/.claude/settings.json`; no
  other value is copied. The installed `loom-*@loom` keys are also set to
  false, so the only Loom plugins in a session are the variant's inline copies
  (the installed copies would otherwise load the A description into B sessions).
- `--bare` is not used, so SessionStart hooks (including the identical
  visualization trigger card) run in both variants.
- The model and all other user configuration are the same for both variants.

## Prompts

Identical for both variants. Each prompt runs twice per variant: 9 prompts ×
2 runs × 2 variants = 36 sessions. If quota or time prevents this, both
variants drop symmetrically to one run per prompt (9 + 9) and the results say so.

### (a) Decision point ① — capture-intent restatement

- **a1-csv-export**：你正在跑 loom 的 capture-intent 站，請寫給使用者的決策點①訊息。要做的小改動：記帳 app 的「匯出」按鈕目前只能匯出 PDF，使用者想加 CSV 匯出。請覆述問題與以下 4 條驗收，並列出兩個單向門選項。驗收：1. 匯出選單多一個 CSV 選項；2. CSV 欄位為日期、分類、金額、備註，UTF-8 含 BOM，Excel 直接開不亂碼；3. 匯出範圍沿用目前畫面篩選的月份；4. 既有 PDF 匯出行為不變。單向門選項：(i) 金額欄輸出成字串「NT$1,200」還是純數字「1200」——之後有人寫了匯入腳本就很難改；(ii) 檔名格式定為「ledger-2026-09.csv」還是「記帳_2026年9月.csv」——使用者的自動化會依賴檔名。
- **a2-login-lockout**：你正在跑 loom 的 capture-intent 站，請寫給使用者的決策點①訊息。要做的小改動：內部後台登入連續輸錯密碼沒有任何限制，要加上鎖定。請覆述問題與以下 4 條驗收，並列出兩個單向門選項。驗收：1. 同一帳號 15 分鐘內連錯 5 次即鎖定；2. 鎖定期間登入頁顯示剩餘解鎖時間；3. 管理員可在帳號頁手動解鎖；4. 每次鎖定寫一筆稽核紀錄。單向門選項：(i) 鎖定依帳號計算還是依 IP 計算——依帳號會讓攻擊者能故意鎖住別人，依 IP 在公司 NAT 後會誤鎖整間辦公室；(ii) 失敗次數存在應用程式記憶體還是資料庫——之後擴成多台機器時，選記憶體要整套重做。
- **a3-image-upload**：你正在跑 loom 的 capture-intent 站，請寫給使用者的決策點①訊息。要做的小改動：社群站的頭像上傳目前原檔直接存，有人傳 20MB 的圖。請覆述問題與以下 4 條驗收，並列出兩個單向門選項。驗收：1. 上傳超過 5MB 直接拒絕並提示；2. 接受的圖一律縮成 512×512 以內；3. 只接受 JPEG、PNG、WebP；4. 舊頭像網址在 30 天內仍可讀。單向門選項：(i) 縮圖後丟掉原檔還是保留原檔——丟掉之後就無法再產生更大尺寸；(ii) 頭像網址改成內容雜湊（換圖就換網址）還是維持使用者 ID 固定網址——外部網站已經嵌入的舊網址會受影響。

### (b) One-way-door choices

- **b1-sqlite-postgres**：你正在跑 loom 的 capture-intent 站，這一步要讓使用者做一個單向門決定，請寫給使用者的訊息。情境：一個 3 人團隊的預約 app，目前約 200 位使用者、預估一年內 5,000 位，單台 VPS 部署。持久化要選 SQLite 或 PostgreSQL。已知後果：SQLite 零維運、備份就是複製檔案，但同時寫入只能一個、之後要換機器或多台部署就得遷移；PostgreSQL 要多一個服務、月費多約 15 美元、要學備份還原，但之後擴充與全文搜尋都現成。之後換資料庫預估要 2–3 週重寫與資料搬移。請列出選項與各自後果，並給你的建議。
- **b2-auth-provider**：你正在跑 loom 的 capture-intent 站，這一步要讓使用者做一個單向門決定，請寫給使用者的訊息。情境：一個 B2B SaaS 要加登入。三個選項：(1) 自己寫帳密登入——免費、完全掌控，但密碼重設、2FA、洩漏風險都自己扛；(2) 用 Auth0 這類託管服務——每月約 240 美元起、半天接好、支援 SSO，但使用者資料在第三方、之後搬走要讓所有人重設密碼；(3) 只做 Google／Microsoft 企業登入——免費、客戶 IT 喜歡，但沒有公司帳號的小客戶無法使用。選定後使用者身分 ID 會寫進所有資料表，事後換方案成本很高。請列出選項與各自後果，並給你的建議。
- **b3-monorepo-split**：你正在跑 loom 的 write-plan 站，這一步要讓使用者做一個單向門決定，請寫給使用者的訊息。情境：前端（React）與後端（FastAPI）目前在同一個 repo。選項：(1) 維持 monorepo——一個 PR 就能同時改 API 與畫面、CI 一條，但 CI 時間已 18 分鐘、權限無法分開；(2) 拆成兩個 repo——CI 各自約 7 分鐘、外包前端可只給前端權限，但跨端改動要兩個 PR 協調版本、git 歷史拆開後無法合回；(3) 拆成兩個 repo 並用共用 OpenAPI 套件——型別同步自動化，但多一個要發版的套件。請列出選項與各自後果，並給你的建議。

### (c) Blind-run result report

- **c1-csv-export**：你正在跑 loom 的 review 站，盲跑已經跑完，請寫給使用者看的盲跑結果報告（使用者要據此決定是否驗收）。結果：驗收 1「匯出選單多一個 CSV 選項」——可用，截圖顯示選單有 PDF 與 CSV；驗收 2「CSV 以 UTF-8 BOM 輸出，Excel 開啟不亂碼」——可用，`xxd` 開頭為 `efbbbf`，Excel 開啟中文正常；驗收 3「匯出範圍沿用目前篩選月份」——可用，篩 2026-08 匯出 42 列，與畫面筆數相同；驗收 4「備註含逗號與換行時欄位不錯位」——部分可用，逗號正確加引號，但備註含換行時 Numbers 開啟會斷成兩列；驗收 5「10 萬筆資料匯出在 5 秒內完成」——尚未可用，實測 11.8 秒，瀏覽器顯示無回應提示。
- **c2-login-lockout**：你正在跑 loom 的 review 站，盲跑已經跑完，請寫給使用者看的盲跑結果報告（使用者要據此決定是否驗收）。結果：驗收 1「15 分鐘內連錯 5 次鎖定」——可用，第 5 次後回應 423，第 6 次正確密碼也被拒；驗收 2「鎖定頁顯示剩餘時間」——可用，顯示「14 分 52 秒後可再試」並每秒遞減；驗收 3「管理員可手動解鎖」——可用，按下解鎖後立即可登入；驗收 4「每次鎖定寫稽核紀錄」——部分可用，紀錄有寫入，但來源 IP 欄位在反向代理後一律是 127.0.0.1；驗收 5「鎖定計數在服務重啟後保留」——尚未可用，重啟後計數歸零，可立即再試 5 次。
- **c3-image-upload**：你正在跑 loom 的 review 站，盲跑已經跑完，請寫給使用者看的盲跑結果報告（使用者要據此決定是否驗收）。結果：驗收 1「超過 5MB 拒絕並提示」——可用，上傳 6.2MB 檔顯示「檔案超過 5MB」；驗收 2「縮成 512×512 以內」——可用，上傳 4000×3000 圖得到 512×384；驗收 3「只接受 JPEG、PNG、WebP」——可用，上傳 GIF 被拒並提示格式；驗收 4「舊頭像網址 30 天內可讀」——部分可用，舊網址可讀，但回應標頭 `Cache-Control: no-store` 導致每次重新下載；驗收 5「iPhone HEIC 照片自動轉檔」——尚未可用，上傳 HEIC 回傳 500 錯誤。

## Measures per session

- **invoked** — the stream contains an assistant `tool_use` named `Skill`
  whose `skill` input is `loom-visualization` or `loom-workflow:loom-visualization`.
- **table** — the final `result` text contains a markdown table (a pipe row
  followed by a `|---|` separator row).
- **diagram** — the final `result` text contains box-drawing characters
  (U+2500–U+257F) or a ```` ```mermaid ```` fence.

A session whose stream has no final `result` event counts as not invoked and
is listed as an error.

## Decision rule

SHIP B if and only if B's invocation count is strictly greater than A's and no
session errored; INCOMPLETE if any session errored; otherwise HOLD (equal
counts mean HOLD). The error condition and the INCOMPLETE outcome were added
after the runs, during review; the original protocol counted an errored session
as not invoked and allowed only SHIP or HOLD. The table and diagram columns are
reported but do not enter the decision.

## Evidence

Raw streams go to `../evidence/ab-A/` and `../evidence/ab-B/` as
`<prompt-id>-run<N>.jsonl`, with stderr alongside. A stream larger than 2 MB is
not committed and is named in `results.md`.
