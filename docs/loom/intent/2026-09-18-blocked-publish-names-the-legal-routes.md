# 發佈被擋的當下，指出合法的兩條路，不把指令交還給使用者

originator: kouko
kind: engineering
needs-design: no — checker stderr text and station prose under loom-code/scripts/ and loom-code/skills/, which the manifest classifies as the `gate` and `skill` artifact types, not interface surfaces (`**/cli/**`, `**/api/**`, `**/commands/**`, `**/*.tsx`, `**/templates/**`)
evidence: [loom-code/scripts/loom_checker/command_handlers/push.py, loom-code/scripts/loom_checker/command_handlers/finalize.py, loom-code/skills/ship/SKILL.md, loom-code/skills/expert-mode/SKILL.md]
status: confirmed 2026-09-18
publication: automatic — authorized 2026-09-18 by kouko

## Problem

發佈閘門擋下 agent 的推送、開 PR 與合併時，訊息沒有指出任何可以走的路。agent 因此把被擋的指令原封不動交給使用者，請他自己貼進終端機執行。

使用者反覆承擔本來屬於 agent 的機械工作。已知證據：

| 時間 | 專案 | 發生什麼 |
|---|---|---|
| 2026-09-18 上午 | dotfiles | 發佈四個 PR 期間閘門觸發五次，每一次都由使用者把同一行指令貼進自己的 shell 執行 |
| 2026-09-07 23:09–23:10 | iCHEF-dbt-pipeline | 連續三次交還指令：推送 → 開 PR → 合併 PR |
| 掃過八個專案的對話紀錄 | 四個專案 | 共 33 處「請你自己跑」 |

合法的路其實存在，而且已經蓋好：使用者親手打一次跳站確認碼之後，審查站的門檻降為零、照樣產出驗證紀錄，紀錄裡明載哪些站被跳過，PR 的揭露段落就是從它算出來的。但被擋的當下沒有任何訊息提到這條路，agent 也沒有任何規則禁止它把指令交還，於是五次全部走向交還。

## Proposed outcome

發佈被擋的當下，agent 手上就有可以自己接續的資訊：補跑審查站，或當場提出跳站提案讓使用者用一次親手確認完成。把指令交還給使用者不再是被允許的作法。這是機制上的常態，不是某一次變更的例外。

## Acceptance

1. 在沒有驗證紀錄的分支上執行正規發佈指令，拒絕訊息同時指出兩條合法路徑：補跑審查站，以及提出跳站提案由使用者親手確認。
2. 同樣的資訊出現在合併指令因缺少驗證紀錄而拒絕時。
3. 站的說明文件載明一條規則：發佈被擋時不得把被擋的指令交給使用者執行，必須走上述兩條路之一。
4. 使用者完成一次跳站確認後，審查站產出的紀錄明載被跳過的站，正規發佈指令完成推送並開出 Ready PR，且該 PR 內文包含跳站揭露。
5. 本次變更自身的推送與開 PR 由 agent 執行；合併在使用者口頭同意後同樣由 agent 執行。使用者全程不輸入任何 git 或 gh 指令。
6. 閘門沒有任何一條規則被放寬：沒有驗證紀錄且沒有跳站確認時，發佈仍然被擋。
7. 盲跑報告逐條記錄每一個 git 與 gh 動作由誰執行，顯示沒有任何指令交給使用者執行。
8. 既有測試全部通過。

## Constraints

- 不放寬閘門的任何一條規則，也不改變共用回報函式的語意。
- 不產生任何不實的驗證紀錄；跳站必須來自使用者親手輸入的確認，符合原則第 2 條。
- 每一次跳站都必須在 PR 內文揭露。
- 機器面輸出（訊息文字、測試、commit）維持英文。

## Out of scope

- 把「沒有驗證紀錄」從擋下降級為警告（先前考慮過的方案；審查證明它會連帶破壞交付追蹤、跳站稽核與 PR 誠實揭露，並牴觸原則第 2、3 條。證據保留在 dotfiles 的 backlog 紀錄）。
- 使用者個人設定造成的攔截：bash-guard 的 PR 合併與 main 分支保護、settings.json 裡的破壞性指令拒絕規則。
- Bash 指令文字只要出現 PR 合併那三個字就被擋的誤攔。
- `!` 前綴指令是否經過同一個 hook 的查證。

## Open questions

- none
