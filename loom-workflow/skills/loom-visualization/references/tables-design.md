# Tables in design and UX documents

Load this when: the user asks for one of these documents: heuristic evaluation, usability test report, content audit, design critique or review feedback log, design tokens table, component state matrix, accessibility (WCAG) audit, journey map or service blueprint, personas or JTBD comparison, design decision log, microcopy change log.

A chat reply about a conversation situation (decision, before and after,
progress, checklist, confirmed and unconfirmed, findings, risks, support
matrix) uses `references/plain-language.md` instead of this file.

How to read an entry: "When" is the document situation, "Columns" the
headers, "In chat" whether the table fits a chat reply and, if not, the
reduced columns to use there. [synthesized] marks a column set the research
rebuilt from several articles' prose; no single source gave that table, so
treat it as an inference, not a quotation. [unverified] marks a source that
could not be fully checked. A "Pointer:" entry is the same usage as a table
written elsewhere; use that table.

### D1. Heuristic evaluation

- When: an expert rates a UI against usability principles (such as Nielsen's ten heuristics) to find and rank problems without real users.
- Columns: `Heuristic | Problem Description | Severity (0-4) | Suggested Fix | Notes`. Severity: 0 not a problem, 1 cosmetic, 2 minor, 3 major, 4 catastrophic.
- In chat: drop Notes (4 columns); for a short review reply, use the general Findings and recommendations table.

| Heuristic | Problem Description | Severity | Suggested Fix |
|---|---|---|---|
| Visibility of system status | No loading indicator when saving | 3 | Add spinner/progress bar |
| Error prevention | No confirmation before deleting account | 4 | Add confirm dialog |
| Consistency and standards | Button colors vary by page | 2 | Standardize on token |

Sources: https://www.philipburgess.net/post/heuristic-evaluation-template, https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/

### D2. Usability test findings

- When: reporting moderated or unmoderated usability test results to stakeholders.
- Columns: `Task | Observation | Severity | Participant | Recommendation` [synthesized from Maze + Contentsquare]. Severity (Maze): 4-Critical, 3-Serious, 2-Medium, 1-Low, 0-No issue.
- In chat: 5 columns is the limit; in chat drop Participant.

| Task | Observation | Severity | Participant | Recommendation |
|---|---|---|---|---|
| Checkout | Clicked "Cancel" instead of "Submit" | 3-Serious | P4 | Increase contrast/size of primary CTA |
| Search | Could not find filter panel | 2-Medium | P2, P5 | Move filters above the fold |
| Sign-up | Password rules unclear until error shown | 1-Low | P3 | Show rules inline before submit |

Sources: https://maze.co/guides/usability-testing/analysis/, https://contentsquare.com/guides/usability-testing/report/

Japanese variant, a per-participant pass/fail grid [synthesized]: `Task | P1 | P2 | P3 | Issue found`. In chat it fits with up to three participants.

| Task | P1 | P2 | P3 | Issue found |
|---|---|---|---|---|
| ログイン (Login) | 成功 | 失敗 | 成功 | パスワード表示ボタンに気づかない |
| 検索 (Search) | 成功 | 成功 | 失敗 | フィルタの意味が不明 |
| 購入完了 (Purchase done) | 失敗 | 成功 | 成功 | 完了画面が出るまで不安 |

Sources: https://uxdaystokyo.com/articles/how-you-summarize-usability-test-result/, https://note.com/betsychen/n/n5d7090dfd4a3, https://blog.nijibox.jp/article/usability_test2/

### D3. Competitive or feature comparison matrix

Pointer: `references/tables-business.md` entry B7 "Competitive analysis matrix"; for sales positioning, Crayon adds a Feature Group column (`Feature Group | Feature Name | Your Company | Competitor A | Competitor B`) and colours cells green (strong), yellow (weak), red (absent). Colour needs a text value or legend (WCAG 1.4.1). The artifact is standard; the name "matrix" has no authoritative source. https://www.crayon.co/blog/competitive-matrix-examples

### D4. Content audit spreadsheet

- When: inventorying existing pages before a redesign, SEO clean-up or migration.
- Columns: `URL | Title | Word count | Unique visits | Keyword | Position` (Buffer's list, trimmed to the core)
- In chat: does not fit (6 columns, many rows); keep it in the document. In chat, report only the pages that need action: `URL | Problem | Action`.

| URL | Title | Word count | Unique visits | Keyword | Position |
|---|---|---|---|---|---|
| /blog/seo-basics | SEO Basics for Beginners | 1,450 | 3,200 | seo basics | 4 |
| /blog/old-post | (untitled, missing) | 320 | 40 | None | None |
| /pricing | Pricing – Acme | 600 | 8,900 | acme pricing | 1 |

Source: https://buffer.com/resources/content-audit/

### D5. Design critique or review feedback

- When: making peer and stakeholder feedback trackable and actionable.
- Columns: `Reviewer | Comment | Type | Status` [synthesized from Ziflow status field + Jotform critique zones]. Status values (Ziflow): Approved, Approved with Minor Changes, Needs Major Revisions, Rejected.
- In chat: fits (4 columns); when the reply reports problems to fix, use the general Findings and recommendations table.

| Reviewer | Comment | Type | Status |
|---|---|---|---|
| Alex | Great use of whitespace on hero | Positive | Not applicable |
| Jamie | Why is nav collapsed on tablet? | Clarifying Question | Needs Major Revisions |
| Sam | CTA button contrast fails AA | Critical Concern | Approved with Minor Changes |

Sources: https://www.ziflow.com/blog/design-feedback-template, https://www.jotform.com/board-templates/design-critique-template

### D6. Design tokens table

- When: documenting a design system's token names, values and where they apply.
- Columns: `Token | Function | Mixin | Utility class` (U.S. Web Design System, verbatim headers)
- In chat: the full token table stays in the document; for one or two tokens in chat, use `Token | Value | Used for`.

| Token | Function | Mixin | Utility class |
|---|---|---|---|
| 'red' | color('red') | u-border('red') | .border-red |
| 'blue-50v' | color('blue-50v') | u-bg('blue-50v') | .bg-blue-50v |
| 'gray-cool-10' | color('gray-cool-10') | u-bg('gray-cool-10') | .bg-gray-cool-10 |

Source: https://designsystem.digital.gov/design-tokens/

### D7. Component state matrix

- When: specifying how each interaction state (hover, focus, pressed, disabled) changes a component's properties, state × variant.
- Columns: `State | Layer opacity` (Material Design 3 state layers)
- In chat: fits (2 columns).
- Marker: [unverified: page not fully fetchable]. The percentages come from search snippets, not a direct page fetch; check them again before reuse.

| State | Layer opacity |
|---|---|
| Hover | 8% |
| Focus | 12% |
| Pressed | 12% |
| Dragged | 16% |

Source: https://m3.material.io/foundations/interaction/states/state-layers

### D8. Accessibility audit (WCAG)

- When: auditing a site or app against WCAG success criteria and tracking fixes.
- Columns: `Issue Id | WCAG SC | Level | Impact | Recommendation` (DigitalA11Y, trimmed)
- In chat: 5 columns is the limit; in chat drop Issue Id.

| Issue Id | WCAG SC | Level | Impact | Recommendation |
|---|---|---|---|---|
| A11Y-001 | 1.1.1 Non-text Content | A | Serious | Add descriptive alt text to hero image |
| A11Y-002 | 2.4.7 Focus Visible | AA | Moderate | Restore visible focus ring on nav links |
| A11Y-003 | 1.4.3 Contrast (Minimum) | AA | Serious | Increase button text contrast to 4.5:1 |

Source: https://www.digitala11y.com/creating-an-accessibility-audit-template/

### D9. User journey map or service blueprint as a table

- When: laying out a persona's experience across phases to find pain points and opportunities.
- Columns: `Phase | Action | Touchpoint | Emotion | Pain point | Opportunity` [synthesized: no single source showed a full worked table]
- In chat: does not fit at 6 columns; in chat use `Phase | Pain point | Opportunity`.

| Phase | Action | Touchpoint | Emotion | Pain point |
|---|---|---|---|---|
| 認知 Awareness | SNS広告を見る | Instagram | 少し興味 | 広告が多すぎる |
| 比較検討 Consideration | 口コミを検索 | レビューサイト | 不安 | 情報が分散 |
| 購入 Purchase | カート投入 | 自社EC | 期待 | 会員登録が面倒 |

Sources: https://bow-now.jp/media/column/customerjourneymap/, https://popinsight.jp/blog/?p=2327, https://u-site.jp/alertbox/journey-mapping-101

### D10. Personas or JTBD comparison table

- When: comparing several personas side by side, or comparing the jobs customers hire a product to do (Jobs to be Done).
- Columns (persona, notepm.jp): `Name | Age/Job | Family/Housing | SNS used | Key info source | Decision priority | Purchase trigger`
- Columns (JTBD) [synthesized, low confidence: no canonical source table found]: `Job Statement | Trigger/Context | Desired Outcome | Current Solution (hired/fired) | Satisfaction Gap`
- In chat: neither full set fits; in chat use `Name | Age/Job | Key concern | Info source` for personas, or `Job | Desired outcome | Gap` for JTBD.

| Name | Age/Job | Key concern | Info source |
|---|---|---|---|
| 田中さん | 34/会社員 | コスパ重視 | Instagram |
| 佐藤さん | 45/自営業 | 時短重視 | Google検索 |

Sources: https://notepm.jp/template/persona, https://www.theydo.com/templates/jobs-to-be-done-template, https://userpilot.com/blog/jobs-to-be-done-template/

### D11. Design decision log (ADR style)

- When: recording why a design or architecture choice was made, for later reference.
- Columns: `ID | Decision | Status (Proposed/Accepted/Superseded) | Date | Decision drivers` [synthesized from the MADR / adr.github.io ecosystem: no verbatim table retrieved, the template link returned 404]
- In chat: fits without Decision drivers (4 columns).

| ID | Decision | Status | Date |
|---|---|---|---|
| ADR-001 | Use REST over GraphQL | Accepted | 2026-01-10 |
| ADR-002 | Adopt design tokens | Proposed | 2026-02-03 |

Sources: https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/decision-log/ (template link dead), https://adr.github.io/, https://ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html

### D12. Microcopy before and after

Pointer: `references/plain-language.md` situation "Before and after"; for a copy review or post-mortem use `Location | Before | After | Result`, with the measured effect (such as a conversion change) in Result. [synthesized: sources show before/after as prose pairs, not tables]. Before/after tables have no authoritative source. https://microcopy.org/case_studies/longcopyshortcopy/, https://www.a8.net/ec/column/?book_id=column_135
