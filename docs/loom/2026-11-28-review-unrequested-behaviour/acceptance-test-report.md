# 最後審查要抓出「做了沒人要求的事」 — 我試了什麼、結果如何

Tried on 2026-11-28 in a clean copy at 9526763628c8e19749d79f0e3bc8d42094610082.
每一條怎麼試、回來什麼：`docs/loom/2026-11-28-review-unrequested-behaviour/evidence/acceptance-test-evidence.md`。

## 你要的，一條一條

| # | 你要的 | 結果 | 實際發生什麼 | Re-run |
|---|---|---|---|---|
| 1 | 最後審查的 reviewer 共用指引寫明：交付了 intent 沒要求的行為，或 intent 的 Out of scope 排除的行為，必須當作 finding 提出；沒有 spec 的改動同樣適用。 | works | reviewer 指引開頭、所有審查清單共用的那一段寫著：改動交付了 intent 沒要求、或 Out of scope 排除的行為，reviewer 必須提出，每個改動都適用，包括沒寫 spec 的；緊接著新增一句說這類問題要歸在哪個評分項目，我逐一對過每份審查清單，每份都有對應的項目可歸；spec 審查原本那條檢查沒有被動到。 | carried over — 這次修正只動了測試檔，reviewer 指引一字未改 |
| 2 | 把這條規則刪掉、或改成可以略過時，package suite 會有測試失敗。 | works | 上一輪擋不住的三種豁免寫法——「out-of-scope excludes」（加連字號）、「Out of scope excluded」（過去式）、「Out of scope exclusion」（名詞）——這次修正後各自都讓測試失敗；我另外試了兩種新寫法，全大寫加連字號的複數「OUT-OF-SCOPE EXCLUSIONS」、以及中間隔著冒號的「Out of scope: excluding…」，也都被擋下。每種改壞都先確認真的寫進了檔案，沒改壞時測試全數通過。上一輪已擋下的 26 種改壞（刪改規則本身、用「excess」「unrequested」各種變形寫的豁免）這次沒有重跑，因為這次修正只放寬了「Out of scope」那組字的比對，沒動其他兩組。換句話說、不用規則原字的豁免（例如「跳過第四個方向」、中間多插一個字的「out-of-scope list excludes」）仍然通過，這是你選 A 時接受的已知限制，交給 reviewer 讀出來。接受前執行的自動化測試也包含這些測試，失敗會擋下這個變更。 | re-tested |
| 3 | loom-code 發布新版號，CHANGELOG 寫明這條規則。 | works | loom-code 從 3.92.0 升到 3.93.0，四份設定檔和四份 README 一致；CHANGELOG 最新一則寫出完整規則，包括 Out of scope、沒 spec 也適用、每份審查清單都適用，現在也寫了這類問題要歸在哪個評分項目；版號一致性測試通過，接受前執行的自動化測試也包含它，失敗會擋下這個變更。 | carried over — 這次修正沒動到版號、CHANGELOG 或 README |

## 對你既有的資料做了什麼

沒有 — 這個變更只改了外掛裡給 reviewer 的指引文字、保護它的測試，以及版號與 CHANGELOG，不讀也不寫你既有的任何資料。

## 我替你決定的事

- **安裝方式的檢查用本機驗證代替** — README 的安裝指令會從 GitHub 上已發布的版本安裝，裝不到這個尚未合併的 commit，所以我改用 Claude Code 內建的外掛驗證指令檢查乾淨副本，loom-code 驗證通過。若你要求合併後實際從 marketplace 安裝一次才算數，那一步要等合併後另外做。
- **第 2 條只跑了會讀到這份指引的測試，沒有跑完整 package suite** — 完整 suite 留給接受前的自動化測試。
- **把同一個字的變形算在「用規則原字的豁免」裡** — 你選 A 時說擋得住的是用規則原字寫的豁免。我前幾輪判斷同一個字的變形（複數、過去式、名詞、只差連字號）屬於該擋的那一邊，這次沿用同一個判斷：三組原字的變形現在都擋得住，所以第 2 條記 works。中間多插一個字的寫法（例如「out-of-scope list excludes」）我算成換句話說，歸在已知限制；單獨出現「out of scope」而沒有「排除」字眼的句子，這次修正刻意不擋，因為那常是正常用語（例如「把範圍外的工作留給下一個變更」）。
- 沒有任何嚴重程度 important 以上的審查意見被駁回。

## 你吩咐跳過的步驟

沒有 — 沒有任何步驟被跳過。

## 我不確定你要不要的地方

沒有。
