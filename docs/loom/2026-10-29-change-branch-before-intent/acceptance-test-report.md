# 變更紀錄從一開始就放在變更分支上，主幹分歧時不擅自丟掉 — 我試了什麼、結果如何

2026-10-29 在乾淨的專案副本（`52bf2842`）上逐條試過。每條都在拋棄式的 git 沙盒裡做（本機假的 origin 加一份 clone，沒有碰 GitHub）：我照著這次改過的站點說明一步一步執行 git 操作，看 commit 實際落在哪裡；「主幹能不能跟上合併」這部分直接跑了真正的主幹同步程式。每一條怎麼試、回來什麼：`docs/loom/2026-10-29-change-branch-before-intent/evidence/acceptance-test-evidence.md`。

## 你要求的每一項

| # | 你要求的結果 | 判定 | 實際發生的事 | 重測 |
|---|---|---|---|---|
| 1 | Running a change from a clean, synchronized trunk through `capture-intent` (and `write-spec` when it runs) adds no commit to the local trunk; the intent commit is on the change branch. | works | 照說明先開變更分支再 commit：intent 和 spec 都在變更分支上，本機主幹一個 commit 都沒多，仍和 origin 一致；之後從主幹重新進來寫 spec，也是切回既有分支，不會重開。 | — |
| 2 | Starting from a trunk synchronized with `origin` and receiving no independent local commits, after that change is merged through `land` the local trunk fast-forwards to the merge with no manual reconciliation. | works | 在 origin 模擬 squash merge 後跑真正的主幹同步：主幹沒被 checkout、或乾淨地 checkout 在主副本上，兩種情況都直接 fast-forward 到合併結果。對照組照舊做法把 intent commit 在主幹上，就重現了 dogfood 看到的「trunk not updated」。 | — |
| 3 | Given a local-only sentinel commit on the trunk and `land` reporting `trunk not updated`, an agent following the station instructions reports it to the maintainer and leaves the trunk's commit identifier unchanged; merge acceptance does not count as permission to discard it. | works | 主幹上放一個只在本機的 commit，真正的同步程式回報「trunk not updated」且沒動主幹；發布站的說明接著要求把這行告訴你、主幹原樣不動，並寫明你接受合併不等於同意丟棄，照做後那個 commit 的識別碼完全沒變。「告訴你」這半是讀說明確認的，沒有實際開一個新的 agent 來觀察。 | — |
| 4 | A change entered at `write-plan` (loom-design absent) branches before its first change-owned commit, including the intent-confirmation commit. | works | 只裝 loom-code 的入口：開分支的規則寫在所有 commit 點之前，照做後 intent 確認、跳過紀錄、plan 三個 commit 都在變更分支上，第一個 commit 直接接在主幹最新點後面；已確認的 intent 從新 session 進來修正，也是切到既有分支才 commit。 | — |
| 5 | When HEAD is already on the branch belonging to this change, the station reuses it; on an unrelated branch or a detached HEAD it does not commit there before that is resolved, and existing work is preserved. | works | 五種情況都試了：已經在本變更分支就直接用；在無關分支（還有未 commit 的修改）或 detached HEAD 時不在那裡 commit，另開乾淨的工作目錄處理，原本的修改、檔案和 commit 一個都沒動；分支已存在就切過去，舊 commit 保留；分支開在別的工作目錄就到那裡做。 | — |
| 套件 | 完整自動測試 | works | 整套跑一次全部通過、沒有失敗；這套測試在變更被接受前還會由收尾檢查再跑一次，失敗就會擋下。 | — |

## 對你既有的資料做了什麼

沒有 — 這次只改了站點說明文字、版本號和對應的測試，沒有讀寫你任何既有的專案資料。以後的影響是：agent 會在第一次 commit 前就開變更分支，而不是等到寫 plan 時；已經 commit 在主幹上的舊 intent 不受影響。

## 我替你決定的事

- **無關分支或 detached HEAD 時怎麼「先處理好」** — 說明只說不要在那裡 commit、要保留既有工作、不准 reset 或丟棄，沒說用什麼方法。我選了另開一個工作目錄從主幹建變更分支，原本的位置完全不碰。另一個很自然的做法（在原位置直接開新分支）也不會弄丟東西，但會把那些無關的未 commit 修改一起帶進變更分支的工作目錄，之後容易被誤 commit 進這個變更。如果你希望 agent 固定用某一種做法，需要再補一句說明。
- **行為怎麼驗** — 第 1、3、4、5 條是我扮演 agent、只照說明文字操作，git 結果是真的，但不是另開一個全新的 agent 來觀察它會不會照做。第 2、3 條的主幹同步跑的是真正的程式；合併本身是在本機模擬 GitHub 的 squash merge，沒有走真的 PR。
- **沒有被駁回的重要問題** — 這次沒有任何嚴重度「重要」以上的問題被駁回。

## 你要求略過的步驟

沒有 — 沒有跳過任何步驟。

## 我不確定你是否想要的

- 在無關分支或 detached HEAD 上時，要不要讓說明直接指定處理方式（例如「另開工作目錄」或「先問你」），而不是交給 agent 自己判斷？
