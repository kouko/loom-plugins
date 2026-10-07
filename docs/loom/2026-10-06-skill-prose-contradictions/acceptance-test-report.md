# 修正 write-plan 與 closing-review 文件裡互相矛盾的四處規則 — 我試了什麼、結果如何

2026-10-07 在專案的乾淨副本（0c36aa69）上試過；這是修正後的重跑，第一次試的是 cdde0ea2。每一條怎麼試、回來什麼：`docs/loom/2026-10-06-skill-prose-contradictions/evidence/acceptance-test-evidence.md`。

開始前先確認這份副本能照 README 載入：三個 plugin 的設定檔驗證都通過（只有兩個警告，改動前就已存在），開場提示也能正常產生。沒有實際覆蓋安裝到你電腦上的 plugin。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 實際情況 | 重跑 |
|---|---|---|---|---|
| 1 | ① 的訊息說明與 one-way door 規則一致：product 改動的無法回頭選擇在 ② 問，engineering 的在 ① 問；loom-code 與 loom-design 兩邊說法相同。 | works | 規則本身、① 的訊息說明、開場提示、各語言 README 都寫成同一種分法（不寫 spec 的 product 改動則留在 ① 問），兩個 plugin 用字幾乎一字不差；上次提到的缺口已補上：write-plan 自己寫 spec 時，② 的詳細步驟現在也列出要問這些選擇。 | re-tested |
| 2 | 所有提到 Codex 授權停頓的地方，都說它在 plugin 新裝或更新時出現，不再說是每個 repo 第一次使用時。 | works | 全 repo 搜尋後，提到這個停頓的只有兩處，兩處都說是 plugin 新裝或更新時；找不到任何「每個 repo 第一次」的說法。 | carried over — 這次修正沒有改到任何提到 Codex 或授權停頓的句子 |
| 3 | adversary 的規則清楚區分攻擊時試跑的案例與最後提交的程式，兩份文件不再互相衝突。 | works | 兩份文件與 adversary 自己的說明都寫成：攻擊時可以寫來試跑但不提交，只有真的攻破的那個才提交成程式。 | carried over — 這次修正沒有改到 adversary 的三份規則，只改了一個測試檔的說明文字 |
| 4 | reviewer 的規則對已轉正進測試資料夾的 probe 只給一種指示：當作改過的測試檔照跑。 | works | reviewer 規則兩處都是「還留在證據資料夾的不跑，已轉正進測試資料夾的當一般測試檔照跑」；這次調整了句子順序後，「沒跑不算扣分」只指不跑的那兩類，意思更清楚，沒找到相反的指示。 | re-tested |
| 5 | 對這幾個 skill 重跑一致性檢查時，上述四點不再被列為矛盾；完整 package suite 通過，loom-code 與 loom-design 的版號字串與 CHANGELOG 新區段一致。 | works | 在修正後的版本重跑一致性檢查，兩份報告都是通過，原本四點都不在其中（capture-intent 不在檢查範圍，我改用逐字閱讀確認）；完整測試 3084 個通過、0 失敗，這個 suite 在正式接受前還會再自動跑一次、失敗就擋下；版號各處都是 3.37.0 / 2.13.0，CHANGELOG 新區段也對得上，重複的一條已刪除。 | re-tested |

## 對你既有的資料做了什麼

沒有 — 這次只改了說明文字、版號與測試檔，不讀也不寫任何你已經有的資料。

## 我替你決定的

- **不寫 spec 的 product 改動，其無法回頭的選擇在 ① 問** — 這是修正過程中由 agent 決定的：你原本要求「product 在 ②、engineering 在 ①」，但 product 改動若不寫 spec 就根本沒有 ②，照字面會變成這類選擇沒有任何地方問。所以補上「不寫 spec 時改在 ① 問」，並註明之後若還是寫了 spec，② 不再重問。之後若想改，只要改這幾段文字，成本很低。

沒有任何嚴重度 important 以上的 finding 被駁回。

## 你要求跳過的步驟

沒有 — 沒有跳過任何步驟。

## 我不確定你要不要的

沒有。
