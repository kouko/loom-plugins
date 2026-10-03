# 預設檔裡有控制字元時，session start 不再失效：我試了什麼、結果如何

2026-10-03 第一次在專案的乾淨副本（d01d6ddb）上試；修正後在新的乾淨副本（4dea7292）上重試了全部四條，並拿修改前的版本（c14e176c）做對照。每一條怎麼試、回來什麼：`docs/loom/2026-10-03-session-start-control-characters/evidence/acceptance-test-evidence.md`。

## 你要求的，一條一條看

| # | 你要求的 | 結果 | 實際發生的事 | Re-run |
|---|---|---|---|---|
| 1 | With a form feed or a terminal escape character in a defaults line, the session-start output is valid JSON and still carries the station order and the repository's other defaults lines. | works | 我在預設檔放進 form feed、垂直 tab、終端機顏色碼、其他看不見的字元、非 UTF-8 的位元組，以及混了 form feed 的中文；修改前大多讓開場訊息壞掉或整個消失，現在每一種都是合法 JSON，站序和其他預設行都在，form feed 和垂直 tab 變成一個空格；把電腦上的編碼轉換工具拿掉或弄壞再試，form feed 和顏色碼的結果完全一樣。 | re-tested |
| 2 | With an ordinary defaults file, the session-start output is unchanged. | works | 用這個 repo 自己的預設檔、一份自製的普通檔、純中文的檔、以及沒有預設檔的情況，輸出和修改前逐位元組完全一樣，沒有編碼轉換工具時也一樣；唯一不同的仍是 Windows 換行（CRLF）存的檔，見下面「我替你決定的」。 | re-tested |
| 3 | The loom-code 3.29.0 CHANGELOG no longer claims that pytest options which run no tests are always refused; it states that such an option passed through a configuration override still gets through. | works | 3.29.0 那一條這次修正沒有動，仍寫明直接傳的「不跑測試」選項會被擋、經由設定覆寫塞進來的仍會通過並標成已知限制；我再拿檢查器試一次，行為和描述一致；3.29.1 那條改寫後的說明也和我實際看到的行為對得上。 | re-tested |
| 4 | The existing package test suite passes, and loom-code carries a new version consistent across manifests, CHANGELOG and READMEs. | works | 涵蓋這次修改的 17 個測試全部通過（多了一個「編碼轉換工具壞掉」的測試），四份 manifest、CHANGELOG 和各語言 README 都還是 3.29.1；完整的 package test suite 由驗收前自動執行的測試把關，失敗就會擋下這次修改。 | re-tested |

## 對你既有的資料做了什麼

沒有改動任何東西。這次修改只會「讀」你 repo 裡既有的預設檔，在 session 開場時把讀到的內容裡的控制字元和壞掉的位元組濾掉再送出；檔案本身不會被改寫，磁碟上的內容和原來一模一樣。

## 我替你決定的

- **用 Windows 換行（CRLF）存的預設檔，每行結尾那個看不見的 carriage return 現在會被拿掉** — 實作時決定把 tab 和換行以外的控制字元一律濾掉，carriage return 也包含在內。結果是這種檔的開場訊息和以前差了這幾個看不見的字元，可讀的文字完全一樣，兩邊都是合法 JSON。之後要改回「保留」只需動那一行過濾規則。
- **form feed 和垂直 tab 變成空格，而不是直接刪掉** — 這樣 `繁體` 和 `中文` 中間夾了 form feed 時會變成「繁體 中文」，而不是黏在一起；寫在開頭破折號後面的 form feed 也不會讓那一行消失（修正前的版本會）。
- **非 UTF-8 的位元組直接丟掉，不嘗試轉碼** — 例如用 Latin-1 打的 `café` 會變成 `caf`。好處是開場不再整個沉默；代價是那個字會少一個字母。之後若要改成轉碼，需要額外判斷原始編碼。
- **電腦上沒有編碼轉換工具（iconv）時，壞掉的位元組會原樣送出** — 開場訊息仍然會出現、不會沉默，但那段內容不是合法的 UTF-8；Claude Code 收到這種內容會怎麼處理，我沒有試。macOS 和一般 Linux 都內建這個工具，所以只有很少見的環境會碰到。CHANGELOG 已寫明這個限制。
- 沒有任何 important 以上的意見被駁回；對抗測試找到的那一個（非 UTF-8 位元組讓開場整個沉默）已經修好，並收進固定測試。

## 你要我跳過的步驟

沒有，這次沒有跳過任何步驟。

## 我不確定你要不要的

- 終端機顏色碼只有開頭那個看不見的 ESC 字元被拿掉，像 `[31m` 這樣的殘留文字仍會出現在開場訊息裡。要不要連這些殘留也清掉？（目前不清；清理預設檔本身不在這次範圍內。）
