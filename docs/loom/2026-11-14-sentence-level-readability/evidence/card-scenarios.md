# Card probe scenarios

Eight situations. Each gives the user's message and the working notes an agent
would hold after doing the work. The agent under test writes the chat reply to
the user. Replies to S1-S4 are in English; replies to S5-S8 are in Traditional
Chinese, because the user wrote in that language. The notes are deliberately
terse: the reply must come from these facts only.

## S1
User: "Why did last night's nightly build fail?"
Notes:
- nightly build 02:10 failed, step: integration tests
- 3 tests failed, all in payment module
- cause: sandbox API key expired 2026-11-12
- key rotation job exists; disabled since 2026-10-30 by PR 412 (unrelated cleanup removed its schedule entry)
- fix applied: new key stored, schedule entry restored in PR 431 (open, not merged)
- rerun: 3 payment tests pass; full suite 1,204 passed, 0 failed
- nightly will keep failing until PR 431 merges

## S2
User: "Can we upgrade the PDF library to v5 this sprint?"
Notes:
- current v4.8; v5.0 released 2026-09
- v5 removes sync render API; we call it in 14 places, 9 of them in invoice export
- v5 render 30-40% faster in vendor benchmark; not measured on our docs
- v4 security fixes end 2027-03
- estimate: 6 days migration + 2 days retest of invoice export
- sprint has 4 days of free capacity
- option: migrate invoice export only first (5 days), rest next sprint

## S3
User: "What changed in the search results page since Monday?"
Notes:
- default sort changed: relevance -> newest (commit a3f9, Tuesday)
- result count per page 20 -> 25
- filter panel: "price range" filter added; "brand" filter unchanged
- bug introduced: empty query now returns 0 results instead of all items; ticket 908 opened
- page load p95: 820 ms -> 870 ms after the count change

## S4
User: "Is the data migration safe to run on production tonight?"
Notes:
- migration moves 2.1 million order rows to new partitioned table
- dry run on staging copy: 38 minutes, 0 row mismatches
- writes to orders blocked during migration (read-only window)
- rollback script exists; tested once on staging, took 12 minutes
- production backup last taken 06:00 today; next scheduled 06:00 tomorrow
- no dry run done against production-size indexes (staging has 60% of prod data)
- recommendation in notes: take fresh backup first, run during 01:00-03:00 low-traffic window

## S5
使用者：「為什麼昨天的報表數字和今天對不起來？」
Notes:
- 昨日報表營收 1,284,300；今日重算 1,251,900；差 32,400
- 原因：昨日報表產出時間 09:00，退款批次 11:30 才入帳，共 27 筆
- 退款入帳後報表不會自動重算
- 另有 3 筆訂單時區換算錯誤（UTC 當成台北時間），影響金額 1,150，已含在差額內
- 時區問題已修（PR 388，已合併）；自動重算尚未做
- 今日數字為正確值

## S6
使用者：「登入頁改版現在進度到哪？」
Notes:
- 工作項目 5 項：表單樣式（完成）、錯誤訊息文案（完成）、第三方登入按鈕（進行中）、無障礙檢查（未開始）、行動版排版（卡住）
- 第三方登入：Google 完成，Apple 等對方審核，已送出 4 天
- 行動版排版卡在設計稿缺 320px 寬度版本，已於週二向設計提出
- 無障礙檢查排在行動版之後
- 原訂 11/21 上線；依目前狀況最快 11/26

## S7
使用者：「這個錯誤要怎麼處理比較好？」（指匯入 CSV 時遇到重複訂單編號就整批失敗）
Notes:
- 現況：遇到第一筆重複即中止，整批 rollback
- 上週 12 次匯入失敗中 9 次是此原因
- 作法 A：跳過重複列、其餘照匯，結束後列出被跳過的列；改 1 個函式，約半天
- 作法 B：重複時以新資料覆蓋舊資料；會改到既有訂單，客服曾要求不可自動覆蓋
- 作法 C：維持整批失敗，但錯誤訊息列出所有重複列（目前只列第一筆）；約 2 小時
- 資料表有唯一鍵限制，三種作法都不會產生重複資料

## S8
使用者：「昨天那個記憶體問題查到什麼了？」
Notes:
- 服務：圖片縮圖服務；記憶體每小時約增加 180 MB，約 9 小時後被系統重啟
- 已確認：洩漏發生在處理 GIF 時；處理 JPEG、PNG 不會增加
- 已確認：GIF 每一格解碼後的緩衝區沒有釋放
- 未確認：是我們的程式沒呼叫釋放，還是函式庫 3.2 版本身的問題
- 函式庫 3.3 版更新紀錄提到修正 GIF 記憶體問題，尚未測試
- 暫時措施：已把重啟門檻從 2 GB 調到 1.5 GB，並每 6 小時定時重啟
- 下一步：在測試環境升到 3.3 版，跑 500 張 GIF 觀察
