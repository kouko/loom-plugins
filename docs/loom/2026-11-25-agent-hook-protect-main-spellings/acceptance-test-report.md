# Agent hook 擋下三種繞過 main 的寫法 — 我試了什麼、結果如何

Tried on 2026-11-25, in a clean copy of the project at c13c536c8. How I tried
each line and what came back: `docs/loom/2026-11-25-agent-hook-protect-main-spellings/evidence/acceptance-test-evidence.md`.

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | An agent command `cd <main checkout> && git commit …` (and the same with `git merge`) is refused with the existing "direct git merge, commit, or push on main/master is blocked" message, and nothing is committed. | works | 在 feature branch 上送出「先 cd 到 main 再 commit」、「先 cd 到 main 再 merge」，以及 commit 訊息用多行文字寫的版本，全部被擋下，訊息與 exit code 和原本一樣，main 的 commit 完全沒動；修改前的版本會直接放行並真的寫進 main。對應的自動測試也通過，完整測試套件會在驗收前再跑一次，失敗就擋下。 | re-tested |
| 2 | An agent command `git -C <main checkout> commit …` or `git -C <main checkout> merge …` is refused the same way. | works | 用 `git -C` 指向 main 的 commit 與 merge 都被同一句訊息擋下，main 沒有變；修改前的版本兩者都放行。對應的自動測試也通過，完整測試套件會在驗收前再跑一次，失敗就擋下。 | re-tested |
| 3 | An agent command run on a feature branch that pushes to `main` or `master` on a remote (for example `git push origin HEAD:main`) is refused the same way. | works | 從 feature branch push 到遠端的 main、master、寫成完整 ref 名稱的 main，以及先用另一種方式指定遠端再 push 到 main 的兩種寫法，全部被擋下，遠端 main 沒有變。對應的自動測試也通過，完整測試套件會在驗收前再跑一次，失敗就擋下。 | re-tested |
| 4 | The commands refused today are still refused, and these still pass: commit, merge and push on a feature branch; a push from a feature branch to a feature branch; any command in a repository with `loom.protectMain` set to `false`. | works | 原本就擋的（在 main 上直接 commit、merge、push）仍然擋；feature branch 上的 commit、merge、push、push 到另一個 feature branch，以及「commit 訊息或 PR 說明裡只是『提到』push 到 main 的文字」都放行，那個 commit 也真的寫進了 feature branch；把保護關掉的 repo 裡，所有指令全部放行並真的執行。對應的自動測試也通過，完整測試套件會在驗收前再跑一次，失敗就擋下。 | re-tested |
| 5 | All of the above hold in a repository with no native git hooks installed. | works | 所有試驗用的 repo 都是新建的，裡面一個 git 原生 hook 都沒有（連範例檔都刪掉），也沒有設定其他 hook 路徑，第 1–4 條的結果全是在這種 repo 上得到的。 | re-tested |
| 6 | The three commands from items 1–3, sent through the OpenCode hook loader and through the Antigravity hook adapter, are refused there too. Codex is reported as not verified when its CLI is unavailable in the test environment. | works | 同一組指令（含這次新增的寫法）經過 OpenCode 的載入器和 Antigravity 的轉接器，擋的擋、放的放，和 Claude Code 完全一致、訊息相同。Codex：它的 hook 指令本身我直接執行過，結果一致；但沒有開真的 Codex 對話讓模型下指令，所以「在 Codex 裡實際使用」這部分是 not verified。對應的自動測試也通過，完整測試套件會在驗收前再跑一次，失敗就擋下。 | re-tested |

## 對你既有的資料做了什麼

沒有 — 它只動到這次變更自己建立的檔案。這次改的是 agent 下指令前的檢查規則，不讀寫你 repo 裡任何既有的資料；試驗全部在臨時建立、用完即丟的 repo 裡進行。唯一會「感覺得到」的影響是：以前 agent 用 `cd` 或 `git -C` 指到 main 再 commit／merge、或從 feature branch push 到 main，會悄悄成功，現在會被擋下，這正是你要的。

## 我替你決定的

- **用「允許空 commit」的寫法來試 commit** — 我選這個是為了讓「如果沒擋住，就真的會寫進 main」這件事可以被看到（修改前的版本確實寫進去了）。之後改成別的 commit 寫法，結果不會不同，只是少了這個對照。
- **OpenCode 與 Antigravity 用它們的 hook 入口直接餵指令，而不是開一個真的 OpenCode／Antigravity 對話** — 驗收條文寫的就是「送進載入器與轉接器」，所以這樣算數；若你要的是「在那個工具裡真的讓模型下指令」，那還沒試過。
- **Codex 只驗了它的 hook 指令，沒開真的 Codex 對話** — Codex 的指令列工具其實有裝，但要讓模型實際下這些指令，得先把外掛裝進你的 Codex 設定，我不想動你的環境，所以那部分標為 not verified。
- **建立 PR 的那條指令只看檢查放不放行，沒有真的去開 PR** — 真的執行會對外發出東西，所以只確認了檢查放行。
- **這次修正後六條全部重測，沒有沿用上一輪結果** — 修正改的是所有條目共用的檢查規則，每一條都可能受影響。最後一次變動只是搬動測試檔，沒有改到檢查本身；我仍在最終版本上把六條各跑了一遍，結果與前一輪完全相同。

## 你叫我跳過的步驟

沒有 — 沒有跳過任何步驟。

## 我不確定你要不要的

沒有。
