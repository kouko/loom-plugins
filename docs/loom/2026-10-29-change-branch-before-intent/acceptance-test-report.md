# 變更紀錄從一開始就放在變更分支上，主幹分歧時不擅自丟掉 — 我試了什麼、結果如何

2026-10-29 先在乾淨的專案副本（`52bf2842`）上逐條試過；同日幾次修正後，先後在新的乾淨副本（`ea554bea`、`66f30dd2`、`910034de`）上重測受影響的項目。intent 重新確認後多了第 6 條，下表是 `910034de` 的結果。每條都在拋棄式的 git 沙盒裡做（本機假的 origin 加一份 clone，沒有碰 GitHub）：我照著站點說明一步一步執行 git 操作，看 commit 實際落在哪裡、原本的工作目錄有沒有被動到（逐位元組比對）；「主幹能不能跟上合併」這部分直接跑了真正的主幹同步程式。每一條怎麼試、回來什麼：`docs/loom/2026-10-29-change-branch-before-intent/evidence/acceptance-test-evidence.md`。

## 你要求的每一項

| # | 你要求的結果 | 判定 | 實際發生的事 | 重測 |
|---|---|---|---|---|
| 1 | Running a change from a clean, synchronized trunk through `capture-intent` (and `write-spec` when it runs) adds no commit to the local trunk; the intent commit is on the change branch. | works | 照說明先開變更分支再 commit：intent 和 spec 都在變更分支上，本機主幹一個 commit 都沒多，仍和 origin 一致；之後從主幹重新進來寫 spec，現在是先切回既有分支再動筆，spec 也 commit 在變更分支上。 | 重測過 |
| 2 | Starting from a trunk synchronized with `origin` and receiving no independent local commits, after that change is merged through `land` the local trunk fast-forwards to the merge with no manual reconciliation. | works | 在 origin 模擬 squash merge 後跑真正的主幹同步：主幹沒被 checkout、或乾淨地 checkout 在主副本上，兩種情況都直接 fast-forward 到合併結果。對照組照舊做法把 intent commit 在主幹上，就重現了 dogfood 看到的「trunk not updated」。 | 沿用 — 這幾次修正都沒有碰主幹同步程式和發布站說明 |
| 3 | Given a local-only sentinel commit on the trunk and `land` reporting `trunk not updated`, an agent following the station instructions reports it to the maintainer and leaves the trunk's commit identifier unchanged; merge acceptance does not count as permission to discard it. | works | 主幹上放一個只在本機的 commit，真正的同步程式回報「trunk not updated」且沒動主幹；發布站的說明接著要求把這行告訴你、主幹原樣不動，並寫明你接受合併不等於同意丟棄，照做後那個 commit 的識別碼完全沒變。「告訴你」這半是讀說明確認的，沒有實際開一個新的 agent 來觀察。 | 沿用 — 這幾次修正都沒有碰主幹同步程式和發布站說明 |
| 4 | A change entered at `write-plan` (loom-design absent) branches before its first change-owned commit, including the intent-confirmation commit. | works | 只裝 loom-code 的入口，照最新說明重做：intent 確認、跳過紀錄、plan 三個 commit 都在變更分支上，第一個 commit 直接接在主幹最新點後面；已確認的 intent 從新 session 進來修正，也是切到既有分支才 commit。說明裡刪掉的幾句沒有影響開分支的順序。 | 重測過 |
| 5 | When HEAD is already on the branch belonging to this change, the station reuses it; on an unrelated branch or a detached HEAD it does not commit there before that is resolved, and existing work is preserved. | works | 兩個入口（寫 intent、寫 plan）各試五種情況：已在本變更分支就直接用；在無關分支（有自己未 commit 的修改和新檔）或 detached HEAD 時另開一個從主幹出發的工作目錄，所有 commit 都在變更分支上，原位置的分支、修改、新檔和那個沒有分支的 commit 逐位元組不變；分支已存在就切過去，舊 commit 保留；分支開在別的工作目錄就到那裡做。有一個說明沒涵蓋的組合，見下方「我不確定你是否想要的」第一項。 | 重測過 |
| 6 | When the change moves to another worktree — a new one, or the one where its branch is already checked out — every uncommitted file the change produced so far (the intent draft, a spec, a `PRINCIPLES.md` edit) ends up committed on the change branch there, and the original checkout keeps exactly its own earlier work. A spec is never left in a checkout the change has left. | works | 三種情況都照說明做：分支已開在別的工作目錄時，intent 草稿和原則檔上的批准紀錄一起搬過去 commit；在無關分支上另開工作目錄時也一樣（寫 intent 和寫 plan 兩個入口都試了）；寫 spec 時從無關分支出發，先到變更分支所在的工作目錄才動筆，spec commit 在變更分支上，原位置沒有留下任何 spec。每一種情況，原位置都和開始前逐位元組相同。 | 重測過 |
| 套件 | 完整自動測試 | works | 和第 1、4、5、6 條有關的測試在新版本上重跑全部通過；完整的自動測試會在變更被接受前由收尾檢查執行，失敗就會擋下。 | 重測過 |

## 對你既有的資料做了什麼

沒有 — 這次只改了站點說明文字、版本號和對應的測試，沒有讀寫你任何既有的專案資料。以後的影響是：agent 會在第一次 commit 前就開變更分支，而不是等到寫 plan 時；已經 commit 在主幹上的舊 intent 不受影響。變更要換到別的工作目錄時，agent 會把這個變更自己產生、還沒 commit 的檔案（intent 草稿、原則檔上的批准紀錄、spec）一起搬過去，原位置的其他東西不動。

## 我替你決定的事

- **原則檔上的批准紀錄怎麼「搬」** — 這個檔案原本就在專案裡，變更只是在裡面加一行。我只搬那一行的修改，不是整個檔案搬過去。整個檔案搬也行得通，除非你所在的那個無關分支自己也改過這個檔案，這時會把那個分支的內容一起帶進這次變更（見下方第二項）。
- **行為怎麼驗** — 第 1、3、4、5、6 條是我扮演 agent、只照說明文字操作，git 結果是真的，但不是另開一個全新的 agent 來觀察它會不會照做。第 2、3 條的主幹同步跑的是真正的程式；合併本身是在本機模擬 GitHub 的 squash merge，沒有走真的 PR。
- **沒有被駁回的重要問題** — 這次沒有任何嚴重度「重要」以上的問題被駁回。

## 你要求略過的步驟

沒有 — 沒有跳過任何步驟。

## 我不確定你是否想要的

- 你在無關分支上、而這個變更的分支已經存在但沒在任何地方打開時（例如之前在主幹上確認過 intent，後來你切去做別的事），說明給的「另開工作目錄」指令會被 git 拒絕（分支已存在）；說明裡另一句「切過去」則會把你現在的工作目錄整個切到變更分支，連同你自己未 commit 的修改一起帶過去，之後容易被一起 commit 進這個變更。安全的做法是「在既有分支上另開一個工作目錄」，但說明沒寫。要不要補一句？
- 你所在的無關分支自己也改過原則檔時，批准紀錄搬過去會撞到：只搬那一行會衝突，整個檔案搬則會把那個分支的改動帶進這次變更。這種情況很少見，要不要說明遇到時先問你？
