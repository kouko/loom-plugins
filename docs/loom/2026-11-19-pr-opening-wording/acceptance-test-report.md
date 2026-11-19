# 開 PR 這一步不再叫 publish — 我試了什麼、結果如何

Tried on 2026-11-19, in a clean copy of the project at 518bcca7a. How I tried
each line and what came back: `docs/loom/2026-11-19-pr-opening-wording/evidence/acceptance-test-evidence.md`.

## 你要求的，逐條

| # | 你要求的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | `open-pr` 以原本 `publish` 的相同參數完成推送、開啟或沿用 PR、等待 CI。 | works | 兩種參數寫法都被接受，在測試用的本機 repo 走到開 PR 前的檢查並正確擋下、沒有推送；涵蓋這一條的測試全部通過，另有自動化測試套件會在變更被接受前執行、失敗即擋下。真的對 GitHub 開 PR 沒有實地試。 | — |
| 2 | 執行舊命令 `publish` 時，與任何不存在的命令一樣回報 unknown sub-command，不推送、不開 PR，以非零結束。 | works | `publish`、`publish --help` 和透過啟動器呼叫都只回 unknown sub-command、結束碼 2，跟亂打一個命令完全一樣，沒有改名提示。 | — |
| 3 | 開 PR 這一步（含等待 CI 與交付狀態回報）中，CLI 印給使用者的訊息、命令說明與錯誤建議，都把這一步描述為開啟或沿用 PR、等待合併，不再使用 publish／published／publication 字眼。 | partly | 說明的開頭與錯誤建議都改成「開啟或沿用 PR、等待合併」，但 `open-pr --help` 結尾的共用說明仍印出 "No validation or publication occurred" 和 "never authorizes … publication"。 | — |
| 4 | 推送提醒 hook 印給使用者的說明（目前的 `publishing anyway`）改用相同的說法。 | works | 推送時提醒改為 "proceeding"，在 main 上被擋時建議改為 "open its PR"。 | — |
| 5 | Ship 站對使用者的回報（PR 結果與合併前的驗收提問）、Ship 指示 agent 執行的命令，以及確認 intent 時告知「答 yes 之後會推送並開 PR」的那句話，都用相同的說法與新命令名，並保留「合併是另外的決定」。 | works | Ship 叫 agent 執行的是 `open-pr`，確認 intent 時說的是「推送並開一個等待合併的 PR」，「合併另外決定」仍在；只剩一處給 agent 看的說明用了 "Publication-only edits" 一詞。 | — |
| 6 | repo 的 README 中描述這一步的文字使用相同的說法與新命令名。 | partly | 英文 README 都改好了，但 loom-code 的繁中與日文 README 仍寫「送到已發布的 pull request」「③ 發布 PR」「PR を公開」等，正是這次要消除的誤讀。 | — |
| 7 | 已經安裝原生 git hook 的 repo 在更新後，仍能正常安裝與移除該 hook。 | works | 先用舊版裝上 hook，再用新版重裝（內容逐位元相同）並移除，都成功。 | — |
| 8 | 照 Ship 指示操作的 agent 仍能完成開 PR、等待 CI 與合併，完整 package suite 通過。 | works | Ship 指示的命令與新的命令一致，相關測試 146 個全過；完整測試套件由自動化測試套件在變更被接受前執行，失敗即擋下。真的在 GitHub 上合併沒有實地試。 | — |
| UI-1 | 新命令：執行 `open-pr` | works | 同第 1 條。 | — |
| UI-2 | 舊命令：執行 `publish` | works | 同第 2 條。 | — |
| UI-3 | 說明：執行 `open-pr --help` | partly | 同第 3 條，結尾仍有 publication 字眼。 | — |
| UI-4 | 推送提醒 | works | 同第 4 條。 | — |

## 對你既有的資料做了什麼

已經裝在你 repo 裡的 git hook 內容完全沒變，舊 intent 裡的 `publication:` 欄位與交付狀態名稱照舊可讀；唯一受影響的是習慣打 `publish` 的人或腳本，現在會得到 unknown sub-command 而不會推送。

## 我替你決定的

- **沒有實地對 GitHub 開 PR 或合併** — 我只在本機的假 remote 上試到開 PR 前的檢查，真正的推送與 CI 等待靠既有測試佐證，因為依指示不能開真的 PR。若要實證，需要一個可拋棄的 GitHub repo。

## 你要我跳過的步驟

沒有 — 沒有步驟被跳過。

## 我不確定你要不要的

- `open-pr --help` 結尾那段所有命令共用的說明裡的 "publication" 字樣，要不要也改掉？
- 繁中與日文 README 裡的「發布」「公開」要不要在這次一起改？
