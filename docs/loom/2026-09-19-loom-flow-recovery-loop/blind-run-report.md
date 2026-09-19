# Blind-run report — 2026-09-19-loom-flow-recovery-loop

沒有讀取這次變更的實作／adversary 報告，也沒有看 `loom-code/skills/build/SKILL.md`
與 `loom-code/skills/closing-review/SKILL.md` 的 git log/blame；每個場景都是把狀態
實際搭出來，交給一個全新、除了「這是哪個 change、讀哪份 SKILL.md」之外一無所知的
agent 去執行，觀察它真的做了什麼，而不是讀文字判斷「看起來會不會動」。

所有場景都在 `/private/tmp/.../scratchpad/` 下全新建立的 git worktree 裡進行（`run1`
`run2` `run3` `run4a` `run4b` `run5` `run6` `run7`，各自獨立分支），一個極簡的假
change「toy-echo-2026-09-19」（一支三行的 shell script）當作 fixture；本分支
（`fix/2026-09-19-loom-flow-recovery-loop`）本身完全沒有被動到。

## 逐條 Acceptance

1. **部分成立。** 三次獨立、真實執行的 Build/Closing-review 回合（run1、run3、
   run7）都正確地：在「沒有 task 可實作」時繼續往 §3 走而不是停下宣告沒事做、
   讀 `loom-code/contract/manifest.yaml` 判斷缺的東西該誰補、真的 dispatch
   `loom-code:adversary` 產生 adversarial programs、真的 dispatch
   `loom-code:blind-runner` 產生 blind-run report、真的算 reviewer floor 並
   dispatch fresh-context reviewer。但三次都沒有走到一份有效的
   `attestation.json` —— 每次都是被真實的、可重現的 reviewer NEEDS_REVISION
   擋下（fixture 本身的瑕疵：一次是 KICKOFF-DEFAULTS.md 被整份覆寫卻只揭露兩個
   key、一次是缺負向測試案例、`needs-design` 理由沒有逐字寫進 commit
   message）。也就是說：**回頭補件的機制本身每一步都如文字所述運作**，但「跑到
   一份合法 attestation」這件事，在我能負擔的力氣內沒能排除掉 fixture 自身粗糙
   造成的合法卡關去乾淨示範。這是我這次搭 fixture 的限制，不是這次變更文字的
   缺陷 —— 詳見下方「我幫你決定的事」。
2. **成立。** run1 的完整流程中，Build 與 closing-review 各自只被進入一次；run6
   直接構造「closing-review 已經進入兩次」的歷史，第三次進入時它正確地依
   `loom-code/skills/closing-review/SKILL.md` 的「a third entry to any station is
   a recovery that has failed」規則整個停下，不再 dispatch 任何東西、也沒有再
   跳回 Build，並在報告裡列出走過的站序。唯一要注意的落差：run1 的 agent 事後
   坦承自己雖然實際上照規矩只進了一次，卻沒有在過程中「即時」把站序寫成一行
   交接文字（是我事後追問才重建出來的）——這是那次執行的疏漏，不是文字本身
   沒有要求。
3. **成立。** run2（adversarial 缺、屬於 build）：closing-review 冷啟動後直接讀
   `manifest.yaml` 的 `actions[].owner`，判斷 adversarial 歸 build，於是完全不去
   碰它、也不 dispatch reviewer，只回報「交還 Build」並列出站序 ——
   沒有把自己切換成 Build 硬做。run3／run7（blind-run 缺、屬於 closing-review
   自己）：同樣讀 manifest 判斷 owner 是自己，於是自己 dispatch
   `loom-code:blind-runner` 產生報告，完全沒有轉去別的站。兩邊都明確引用
   `actions[].owner` 這個查表結果，而不是文字裡另外寫死一份清單（這份文字裡
   確實也沒有第二份清單）。
4. **成立。** run4a（`second-vendor: ask` 從未被回答）：agent 正確發現「要出
   attestation 得先過 reviewer，reviewer 得先解掉 second-vendor」，確認找不到任何
   已回答的紀錄後，停下來、把要問使用者的問題完整寫出來、並附上站序，沒有自己
   亂猜一個 vendor。run4b（使用者已經說過「你決定」）：agent 直接照 §2「general
   delegation such as 'you decide'」的字句，自己挑了一個可驗證存在的 vendor
   （用 `command -v` 實際探測過），把選擇寫進 plan.md 的 `## Risks` 一行標成
   `user-decided`，全程沒有再問一次。（後面同樣卡在下游 reviewer 的
   NEEDS_REVISION，但那是另一個真實、且這次跑出來還帶點不穩定性的問題，跟
   「決定要不要問」這件事本身無關，見下方限制說明。）
5. **成立，但這個情境是我用敘述構造出來的，不是真的讓 dispatch 失敗。** 我直接
   告訴 run5 的 agent「你剛剛 dispatch blind-runner 失敗了，錯誤是
   XXX」，再讓它純粹依文字判斷下一步。它正確地：沒有再試第二次、沒有轉交給
   Build 或 Ship、把「哪個東西缺、試過什麼、在哪裡失敗」三件事都寫進它給使用者
   的訊息裡，並且逐字引用了「Do not attempt that item a second time and do not
   hand the change on to another station」。我沒能在合理力氣內真的讓一次
   dispatch 在這個環境裡自然失敗（`loom-code:blind-runner` 這個 agent 型別在這
   個環境裡確實可用），所以這條的驗證方式是「餵一個已經發生的失敗事實，看
   agent 怎麼接下去」，而不是「真的弄壞工具鏈觀察它自己撞上失敗」——如果之後
   想要更硬的證據，需要一個能真的讓 dispatch 失敗的環境。

## Review summary
這次變更要修的東西——「碰到缺件時，回頭補、按 owner 查表路由、不要卡死循環」
——在七次獨立構造的場景裡，每一次的路由判斷（誰該補、要不要問、要不要停）都
跟文字描述的完全一致，而且都是真的讀 manifest.yaml、真的 dispatch 對應 agent，
不是紙上談兵。唯一沒能乾淨示範到底的是 Acceptance 1 的「最後一哩」——跑到一份
合法 attestation——三次嘗試都被真實 reviewer 對這個極簡 fixture 本身瑕疵的合理
挑錯擋下，而不是被 recovery 規則本身擋下。另外發現一個跟這次變更無關的旁生
問題：`loom_checker.py` 的 selection 相關指令要求 change-id 是
`YYYY-MM-DD-<name>` 的格式，`toy-echo-2026-09-19`（`<name>-YYYY-MM-DD`）在
`selection record-failure` 上會直接報錯退出 2，而 `selection show` /
`reviewer-count` 則是靜默地退回預設值而不是報錯——這是既有 checker 對不規則
change-id 的容錯行為，不是這次改動introduce的，順手記下來給之後參考。

## Questions I asked you
沒有 —— 這次是工程性的黑箱驗證，過程中沒有出現需要你做決定的分岔點。

## What this did to existing data
沒有動到任何既有資料。所有動作都發生在 `/private/tmp/.../scratchpad/` 底下全新
建立、跑完即可丟棄的 git worktree／分支裡；這個分支
（`fix/2026-09-19-loom-flow-recovery-loop`）本身、以及本 repo 其他任何真實的
change 目錄，都沒有被讀寫或提交任何內容（只有本檔案本身這次新增）。

## I decided for you
- 用一支三行的 shell script 當唯一的功能內容，把每個場景縮到最小，而不是用一個
  更真實、看起來更有代表性的假 change——為了讓每次 dispatch adversary／
  blind-runner／reviewer 的成本可控。
- 為了在同一個 fixture 上重覆測不同的缺件組合，我用 `git worktree` 疊出多個分支
  （fixture-base / fixture-adv / fixture-a4 / fixture-a1-clean），而不是每個
  Acceptance 都從零建一次；這代表 run3/run5 共用同一個「adversarial 已存在、
  blind-run 缺」的起點，run4a/run4b 共用同一個「兩者都在、只缺 attestation、
  second-vendor: ask」的起點。
- Acceptance 4 的「需要決定」場景，我選了 `second-vendor: ask` 且從未被回答
  當構造：這不是文字裡列出的三個具名項目（adversarial／blind-run／
  attestation）本身需要決定，而是「補 attestation 這件事，順著文字往下走會撞到
  一個尚未回答的既有決定點」。四個 run4a agent 自己也判斷這是合理、非牽強的
  讀法，理由列在上面第 4 條；我認同這個判斷，但這仍是一個詮釋，不是文字逐字
  點名的情境，如實揭露。
- Acceptance 5 的「補件失敗」，我沒有真的弄壞任何工具鏈去讓它自然失敗（在這個
  環境裡，`loom-code:blind-runner` 這個 agent 型別本身是可用的，我沒有辦法在
  不做出人工阻斷的情況下讓它真的啟動失敗），而是把「已經失敗」當成餵給 agent
  的既定事實，只驗證它在文字上「接下來怎麼做」的判斷是否正確。如果要更硬的
  證據，需要一個能讓 agent dispatch 真正失敗的環境，這次沒有做到。
- 沒有為了讓 Acceptance 1 乾淨跑到 attestation 而去反覆修 fixture 直到通過
  review——嘗試了一次修正（把 KICKOFF-DEFAULTS.md 的改動寫進 plan 的
  Files/Risk）後，遇到的是另一組同樣真實、只是換了種類的 reviewer 挑錯（缺負向
  測試、needs-design 理由沒逐字進 commit message），判斷再繼續修下去是在花力氣
  把 fixture 做得更像一個真的 production-quality change，而不是在驗證
  recovery-loop 本身，所以在此停下並如實回報這個限制，而不是繼續砸資源直到
  「湊」出一次通過。
