# Engineering research evidence conditions — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at e85c18651eee5b4d7ba853850ba61bd7462001c5.

## Setup and scope

- Clean detached checkout: `/private/tmp/loom-research-acceptance-clean`; initial `git status --short` was empty; `git rev-parse HEAD` returned the exact SHA above. This is the first acceptance run, not a post-fix carry-over.
- Read root README setup, intent, retained engineering spec and plan. Existing-host updates are explicitly out of scope. No credentials, installs, model calls, external services or source repairs were used.
- Ran `agy plugin validate ./loom-code` from the clean root. Exit 0: skills 8 processed, agents 4 processed, hooks 1 processed; commands/mcpServers absent and skipped. This is actual local package parsing/loading validation, not a new host model session or installed-cache parity claim.
- Ran `UV_CACHE_DIR=/private/tmp/loom-uv-research uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/engineering-research/test_package.py -q`. Exit 0: `5 passed in 0.03s`. Tests cover flat resources/links, portable metadata, direct routing, sole discoverable package and station delegation.
- Full suite deliberately left to finalize-review, not skipped by user instruction: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. It runs before acceptance and blocks attestation on failure; no full-suite result is claimed here.
- Archive prefix below: `docs/skill-dogfood/2026-11-14-research-evidence-acceptance/`. Historical absolute scratch paths are provenance. Actual archived receipts were independently inspected, not recreated or treated as new executions. Six candidate cases, largely one source fixture, cannot establish general efficacy, causal improvement or cross-host reliability. Baseline already satisfies core conditions.

## 1. 研究能指出會影響當前決定的具體未知，以及足以回答各項未知的證據條件，且條件符合使用者已確定的目標與限制。

- How I tried it: Inspected R07's exact-root question/conditions and runner constant; inspected R08/R11/R12 caller constraints and the actual source boundary. AST extraction independently returned ('tests', 'loom-code/tests', 'loom-design/tests', 'loom-workflow/tests'). Each retained record names sufficient evidence rather than generic completion.
- What came back: 六個實際案例均提出與當前限制相符的具體問題及足夠證據。 Result: works.
- Evidence: runs/R07/project/docs/loom/research/2026-11-14-package-runner-test-roots.md; runs/R08/project/docs/loom/research/*.md; runs/R11 and R12 records.

## 2. 研究方法與深度依問題及證據缺口選擇；簡單查證、已有充分證據及混合情境皆可適度處理，不因分類而增加不必要活動或使用者確認。

- How I tried it: Read R07 actions (9 records), concise saved record and answer: source-only, no experiment. R08 actions (29 records) include the one permitted builder import/call and actual returned three argument arrays. Source and measurement are combined only for this gap. R11/R12 remain source-only. No category selection or extra user confirmation appears. Existing support is reused on R08 turn 2 without a second experiment.
- What came back: 簡單查檔直接作答，需查呼叫路徑的問題才深入，僅有一項獲准的小實驗。 Result: works.
- Evidence: runs/R07/actions.jsonl; runs/R08/actions.jsonl:9–10,18–28; runs/R11/actions.jsonl; runs/R12/actions.jsonl.

## 3. 研究結論能對應需要釐清的事項，區分已支持、未支持與仍無法確認，並保留適用版本、環境及其他會影響判斷的限制。

- How I tried it: Read all seven candidate saved records and six answer files in full. R08 differentiates source-supported builder behavior, its one empty-directory observation and unimplemented JSON interface. R09 distinguishes recorded timing, missing quality/billing and confounding scope. R10 explicitly identifies missing commit, test files, CI and actual results. Independently read runner lines 110–180 and historical JSON. Recomputed 60.551 seconds and 58.680272899949614%; no monetary or quality inference follows.
- What came back: 各案例區分來源、實測與提案，並保留快照缺少版本識別等限制。 Result: works.
- Evidence: runs/R08/project/src/scripts/run_package_tests.py:116–180; runs/R09/project/samples/timing/{B01.json,B02.json,task-summary.json}; runs/R09 and R10 saved records.

## 4. 未知仍無法解決時，研究能交代缺少的證據與受影響的決定，不把未滿足條件算成已滿足，也不為宣稱完成而降低證據要求。

- How I tried it: R09 record Findings/Decision impact/Limitations and R10 equivalent sections leave the process-change and release decisions unsupported. Actual task-summary.json says scopes differ and quality assessment is absent. The snapshot really contains no full CI/test result. Their concluded status describes completed research, not satisfied decision conditions. No lowering of criteria is needed to reach the negative findings.
- What came back: 兩個證據不足案例明確拒絕推論品質改善或批准發布，列出所缺證據。 Result: works.
- Evidence: runs/R09/project/docs/loom/research/2026-11-14-timing-process-claim.md; runs/R10/project/docs/loom/research/2026-11-14-ci-release-evidence.md.

## 5. 重要方案推薦能公平比較滿足相同目標與必要限制的較小替代方案，說明重要新增部分的具體用途及相關負擔；較小方案不符合必要條件時，也不因追求簡單而推薦它。

- How I tried it: R11 record compares direct builder reuse with HTTP/index/duplicate discovery under the same trusted local Python constraint, explaining lifecycle, staleness and synchronization burdens as inference. R12 rejects both executable main and caller-import-only under mandatory process/JSON/no-suite constraints, and explains the minimal shared-builder JSON interface's output/maintenance obligations. Independently checked actual main calls subprocess.call and has no preview/JSON branch. Necessary complexity is proposed, not claimed implemented.
- What came back: 同程序情境排除不必要服務；跨程序情境則保留必要的新介面與維護負擔。 Result: works.
- Evidence: runs/R11/project/docs/loom/research/2026-11-14-workflow-mermaid-preview.md; runs/R12/project/docs/loom/research/2026-11-14-suite-command-json.md; actual runner:139–167.

## 6. 研究條件或推薦改變時，能說明改變的依據，並讓交付結論與保存的研究紀錄保持一致；無新證據的追問不構成改推薦的充分理由。

- How I tried it: Compared R08 answers across all three turns with snapshots/turn1 and snapshots/turn2, final original record and new JSON record; inspected actions for reading the challenge, retaining recommendation, updating and reading back records. Turn 2 supplies no new evidence and does not reverse. Turn 3 changes caller constraints; final old record explicitly says direct import is inapplicable and links new revalidation; new record links back and retracts direct import as current recommendation. Changed conditions explain the change; final delivery agrees.
- What came back: 三輪實際問答先維持有支持的推薦，再因真正的限制變更更新結論與相互連結的紀錄。 Result: works.
- Evidence: runs/R08/answers.md; runs/R08/actions.jsonl:18–28; runs/R08/snapshots/turn{1,2}/project/docs/loom/research/; final preview and JSON-preview records.

## 7. 正式技能的上述行為有可追查的實際案例結果與獨立判斷，區分已證實與未驗證部分，並保留既有來源品質、授權界線及一般研究能力。

- How I tried it: Ran README-described agy validation and the five focused package tests. Verified all eight delivered skill files match candidate-skill-hashes.json, and 26 relative links in candidate saved records resolve. Read both independent assessor artifacts, preserved write failure/recovery and stdin-script protocol deviation, raw actions and provenance. Actual local source/boundary behavior is supported. External-source handling, external-service privacy, no-write draft behavior and broad general-research preservation are not behaviorally tested; unchanged policy text and package checks cannot establish them. Thus partly, without a demonstrated regression.
- What came back: 實際案例及獨立評估可追查，載入檢查與五項套件測試通過；外部來源、隱私及一般研究能力僅部分觀察。 Result: partly.
- Evidence: candidate-skill-hashes.json; behavior-assessor.md; evidence-assessor.md; runs/R07–R12/provenance.json; focused test output above.

## Retained qualifications and independent checks

- Candidate raw action counts: R07 9, R08 29, R09 11, R10 17, R11 13, R12 11. Provenance reports native gpt-6.1-sol/low; immutable provider identity was not verified. R08 retains three profiles for one continuing actor.
- R08 actions 11–12 retain the blocked first shell write; 13–16 retain recovery using apply_patch and substantive readback. This is not a successful initial write, nor a failed builder observation. Stdin scratch packaging differs from the requested retained script; actual experiment code/stdout are present.
- SHA-256 comparison over all eight candidate skill files returned True. Independent AST check of the actual frozen runner confirmed four TEST_ROOTS, builder-only construction and main's subprocess.call. Link walk over candidate records found 26 relative targets and zero broken targets; it does not validate prose claims by itself.
- A7 partial is a validation limit. No important-or-worse dismissed findings were supplied; no demonstrated source contradiction or authorization breach was found in examined candidate cases. Broader general research, external privacy and no-write behavior require additional actual observations if full behavioral coverage is demanded. Automatic activation and cross-host parity are outside the intent's guarantees.

