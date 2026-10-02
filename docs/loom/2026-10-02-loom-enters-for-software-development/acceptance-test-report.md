# 不靠個人規則，loom 也會自己接手軟體開發 — 我試了什麼、結果如何

2026-10-02 在專案的乾淨複本（ec97d065）上試的。每一條怎麼試、回來什麼：`docs/loom/2026-10-02-loom-enters-for-software-development/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條核對

| # | 你要的東西 | 判定 | 實際發生什麼 | 重跑 |
|---|---|---|---|---|
| 1 | On Claude Code and on Codex, in a live session with no loom lines in the user's personal rules, a request to add a feature or fix a bug that does not mention loom starts loom's intent capture before any file is edited — both in a repository that already has a loom folder and in one that does not. | 做到 | 在 Claude Code 和 Codex 各開 4 個真的 session（加功能、修 bug，各在有 loom 資料夾和沒有的 repo），8 次都先進入寫需求的步驟、只新增需求文件，程式檔一個字都沒動，最後停下來等你說「對」。 | — |
| 2 | On Claude Code and on Codex, a small edit request (a typo fix or a rename) is made directly without starting loom, and starts loom when the user asks for loom. | 做到 | 改錯字、改變數名稱在兩邊都直接改好、沒進 loom；同樣的改錯字加上「use loom」，兩邊都改成先寫需求、等你確認。 | — |
| 3 | On Claude Code, a request that is not software development (for example research or note-taking in a notes folder) does not start loom. | 做到 | 在筆記資料夾請它研究「刻意練習」並寫成筆記，它直接查資料、寫筆記、更新清單，完全沒進 loom。 | — |
| 4 | Antigravity CLI and OpenCode load the same session-start instruction as Claude Code, shown from the files each host loads. | 做到 | 照四個工具各自的設定檔去執行開場說明，Antigravity CLI 和 OpenCode 拿到的文字和 Claude Code 一字不差；沒有實際開這兩個工具的對話（這條本來就只要求看檔案）。 | — |
| 5 | On Codex, the session-start hook runs without being marked failed. | 做到 | 開場程式的輸出只剩 Codex 接受的那一種格式；8 個真的 Codex session 都收到了開場說明，互動畫面上也沒有任何「失敗」字樣，只有兩則和這次改動無關的啟動提醒。 | — |
| 6 | The three small issues left by PR #74 are fixed: the ship station no longer mentions a narrow-change line nothing produces, the verification status no longer takes a depth argument whose values behave the same, and the trailing blank line in its test file is removed. | 做到 | 三處都確認已清掉：那句提到不存在輸出行的說明不見了、多餘的參數沒了、測試檔結尾的空行也拿掉了。 | — |
| 7 | The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs. | 做到 | 整套測試全部通過（3,045 項通過、6 項略過、0 項失敗）；有改到的兩個 plugin 版本號在各設定檔、更新紀錄、說明文件都一致，沒改到的那個維持原版號。 | — |

## 對你既有的資料做了什麼

沒有——這次只改了 plugin 本身的說明文字和開場程式，不讀也不寫你既有的任何檔案。要注意的是行為上的改變：裝了新版之後，在任何資料夾提出加功能或修 bug 的請求，都會先進入 loom 寫需求；唯一的關閉方式還是原本那個關掉開場說明的開關。

## 我替你決定的事

- **用哪種方式載入這次的新版 plugin 來試** — Claude Code 只在那次執行時關掉你已安裝的 loom，改載入乾淨複本裡的版本；Codex 則開一個暫時的設定資料夾，從乾淨複本安裝。你自己的設定檔都沒動。你的其他 plugin 和個人規則照常生效，因為真實使用時它們也在。
- **Codex 的 hook 信任** — 用「只限這一次執行」的信任方式，而且只在暫時設定資料夾裡，沒有寫進你真正的 Codex 設定。實際安裝後，你還是得在 Codex 裡按一次信任，開場說明才會生效。
- **Claude Code 試驗用的模型** — 你平常用的模型在這種非互動模式下叫不到，所以改用 Opus。換成別的模型，判斷結果可能不同。
- **試驗的請求內容** — 用一個小 Python 檔裡的加功能、修 bug、改錯字、改名稱當代表；更模糊的請求（例如「重構一下」）不在這次試驗範圍內。

被駁回的重要問題：沒有。

## 你叫我跳過的步驟

沒有——沒有跳過任何步驟。

## 我不確定你要不要的事

- 在沒有 loom 資料夾的新 repo 裡，Codex 寫需求時還順手起草了一份產品原則文件（Claude Code 是先問你問題、還沒寫檔）。這是寫需求步驟原本就有的行為，但第一次在別人的 repo 裡出現一個新檔案，你能接受嗎？
