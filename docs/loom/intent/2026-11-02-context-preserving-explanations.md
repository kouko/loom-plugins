# 保留必要背景的使用者說明
originator: kouko
kind: engineering
needs-design: no — 僅調整既有需求確認的技能指引與參考說明，未新增介面或工作流程。
status: confirmed 2026-11-06 — 使用者確認可選說明格式並授權本次合併
publication: automatic — authorized 2026-11-06 by kouko
intent_confirmed_sha: 44276606332c340a1d5fed8c8c4ab2b2900dac2a

## Problem
Loom 請使用者確認工作範圍時，說明可能只剩抽象的修復項目，缺少理解所需的背景。使用者必須追問名詞指的是什麼，並自行補回誰在做什麼、發生什麼問題及其影響，才能判斷是否符合自己的需求。原對話已出現要求詳細說明後，仍須追問「設定是什麼」的情況。

## Proposed outcome
Loom 在需求確認點使用適合需求的清楚說明，可用五段組織背景與目前方向、目前問題與影響、這次要改變什麼、範圍與驗收及確認內容。將已知且必要的專案或功能背景與此次需求接起來，再交代改變與必要授權；句子自然撰寫，份量隨需求調整，圖表用於有助理解時。

## Acceptance
1. 使用者能理解相關專案或功能的用途、目前方向及此次需求的關聯，並辨識討論對象、目前問題與影響、預期結果，以及此次確認的範圍與後果。背景與方向須有現有文件或對話依據；未知時不補造專案介紹或路線圖。
2. 五段可作說明結構，不要求每次固定五段；標題使用對話語言，句子與篇幅自由撰寫。必要事實不足時維持訪談，不得假稱需求已確認。
3. 簡單需求各段簡短且不跨段重複，複雜需求保留理解必需的背景。流程差異與條件判斷適合時使用 ASCII 圖，對比圖在圖內標示修改前與修改後，未驗證結果標示為預期；比較條件可用表格，沒有流程的文字修正不強塞圖表。圖文不增加使用者未提出的事實、範圍或保證。
4. 需求確認仍只要求使用者確認需求與必要授權，不要求使用者評斷實作方案、規格品質或審查結論。

## Constraints
- user-decided — 2026-11-06：使用者確認可選說明格式並以「合併吧」授權本次發布與合併，取代先前發布及合併暫停；其他範圍及既有檢查不變。
- user-decided — 2026-11-05: Continue up to ten further Codex-only iterations with relaxed criteria: neither 100% correctness nor five fixed sections in every response is required. Do not invent or change material requirements, authorization or facts, or present missing information as confirmed. Compare against the released baseline, disclose observed material regressions, and use diagrams when they improve understanding. Preserve previous failures, the template-only scope, per-round call limit, and publication/merge holds. This supersedes the earlier fixed-five-sections requirement, not its historical record.
- user-decided — 2026-11-05: Continue up to ten further iterations using Codex only. The change is limited to the explanation template and necessary examples; do not add a workflow, mechanism, model call, or substantial ongoing cost to this stage. Compare behavior and costs with the released baseline, accept a demonstrated relative improvement rather than requiring perfect accuracy, and preserve earlier attempts, failures and publication/merge holds.
- user-decided — 2026-11-05：「如果修改前的實作也會有相同的問題產生的話 只要比修改前要好 也許就可以 release，有可能做到 100% 正確的成本太高了」；以與已發布原版的實際比較評估是否值得釋出，不再要求 100% 正確作為最低門檻。保留已確認的說明內容與授權要求，揭露剩餘錯誤和退步；此決定不授權發布或合併。
- user-decided — 2026-11-05：「繼續迭代吧 最多迭代10次」授權在已保留的所有輪次與失敗紀錄之後，再進行最多十輪；已達相對改善且適合驗收時可提早停止。原廠普通模型的既有測試指定、發布與合併暫停均維持。
- user-decided — 2026-11-04：「繼續迭代吧 先做最多5輪」授權接續最多五輪，含選項指引的隔離比較與依證據修正適用條件；相關 loom-visualization 指引可限縮修正，不新增確認點或全面研究階段。保留 W3-04 及先前所有次數／失敗，不把此次授權當作重設。主對話模型由使用者切換，實際 Claude Code 行為測試仍固定原廠 claude-sonnet-5-5、medium requested；不隨主對話升級。達標可提早停，發布與合併仍暫停。
- user-decided — 2026-11-04：「試試看吧」同意保留五段組織方式，但每段只承載有依據且必要的內容；沒有資料時保留必要的未知，不要求填滿背景、方向、影響與效益。既有閱讀、必要事實訪談、授權及圖表條件不變，不以縮短說明取代查證。此項是降低段落填滿要求的新交付義務；保留 W3-03 的初次實作、兩次續修與所有失敗證據。
- 使用繁體中文與使用者溝通；既有專案慣例仍適用於其他工程產出。
- 簡潔仍須保留理解所需的連接資訊，不能只列修復項目名稱。
- 遵守既有確認點及其適用條件。
- 本輪先改善需求確認①；2026-11-04 使用者以「好 開始吧」及「現在就基於『五段式說明，開頭補背景與目前方』的模板 繼續迭代吧」確認改用固定五段結構，取代先前不固定章節的要求；仍不規定逐字填空句型。
- user-decided — 2026-11-03：另將已展示的「圖內具修改前／修改後標題、外框包住各自流程」樣式存入 loom-visualization 既有線性流程樣板，供共用；僅保存圖表範例與入口提示，不代表已確認或實作討論中的五段式需求確認改版。既有驗收條件、失敗紀錄與發布暫停限制保留。
- user-decided — 2026-11-04：上條記錄的圖表樣板已透過 PR #130 獨立合併；本輪沿用它，不重複釋出或更改其工具。發布與合併本需求確認改版仍暫停，完成實作與驗證不代表授權發布。
- agent-decided — 新的固定五段、具來源的開頭背景與適用圖解，構成先前自由分段要求所沒有的交付義務；以新任務實作，同時保留先前五輪的計數與失敗證據，不將舊證據當作新模板通過的證明。

## Out of scope
- 行為確認②與完成驗收③的說明改版。
- 原對話中的派工設定與重試問題修復。
- 新增確認站點或改變既有發布與合併授權。
- 無關站點、一般回覆風格與其他技能的全面改寫。

## Open questions
- none
