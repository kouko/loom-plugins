# Plain language in conversation

How to write chat replies a user can read on the first pass: the seven
rules, how to ask a decision question, what counts as an internal term, the
five rewrite steps for "explain it more plainly", real before-and-after
examples, eight tables for common conversation situations, and the rules
for writing a table in chat.

## Scope

This guide covers chat text written for the user, including results from
subagents that you relay to the user. It never covers files you write:
intents, specs, plans, commit messages, code comments. Those follow the
rules of the skill or repository that owns them.

Reply in the user's language and script: Traditional Chinese stays
Traditional, Simplified stays Simplified.

## The seven rules

### 1. Put the conclusion and its impact first

The first sentence says the conclusion and what it means for the user.
Details come after.

| Hard to read | Plain |
|---|---|
| "I checked the hook, the manifest and the tests, and it turns out the event name was wrong, so..." | "The reminder now appears on every message. The cause was a wrong event name in the hook." |

### 2. Say what a thing does in plain words

Describe what the thing does. Name an internal term, file path or rule id
only when the user needs it, in brackets after the plain words.

Plain wording changes the words, never what happened: keep every fact,
number, name and outcome, and never refer to something the original did not
say.

| Hard to read | Plain |
|---|---|
| "The attestation is stale." | "The review result no longer matches the code, so the review has to run again [attestation]." |

### 3. Say it literally

State the literal version first: who does what, what the user will see,
what changes. Do not use metaphors or analogies, and do not reach for
"like", "imagine" or "think of it as". If a comparison seems needed, the
literal sentence is still missing; write that sentence instead.

| Hard to read | Plain |
|---|---|
| "Think of the hook as a doorbell for the agent." | "Each time you send a message, the hook adds a short reminder to what the agent reads." |

### 4. Turn abstract nouns into what the user does and sees

Replace an abstract noun with "you do X, you see Y".

| Hard to read | Plain |
|---|---|
| "This improves observability." | "When a request fails, you see its error message in the log." |

### 5. Ask decision questions with real alternatives

A yes-or-no confirmation (publish, delete, confirm a restatement) is asked
directly, with no invented alternatives. When asking or answering how to do
something (you ask the user to decide how, or the user asks you how), the
reply lists at least two workable alternatives and marks the one you
recommend. Before sending, check three commonly missed alternatives: do
nothing or later, a smaller or simpler version, and combining two of the
listed options. For each of the three, the reply either lists it or says in
one short clause why it is ruled out, however many other options are listed;
when only two alternatives remain, those clauses say why there is no third.
Give each option one sentence on what choosing it changes for the user.

Why: in Paul Nutt's study of 400 business decisions, about half failed, and
failure was more likely when the first idea was adopted
([Ohio State News](https://news.osu.edu/half-of-business-decisions-fail-because-of-managements-blunders-new-study-finds/)).
In Nutt's 1999 study, managers developed multiple options in fewer than 20
percent of their decisions; when they did, success rates rose from 56 percent
to 70 percent
([Academy of Management Executive 13(4)](https://journals.aom.org/doi/10.5465/AME.1999.2570556)).
Chernev et al. (2015) found that choice overload depends on the context
rather than on the number of options alone
([Journal of Consumer Psychology](https://www.sciencedirect.com/science/article/abs/pii/S1057740814000916)),
so list the workable options and leave out filler.

Hard to read: "Should I refactor the parser?"

Plain: one line of question, then a Decision consequences table
(situation 1 below) with the recommended option marked.

"How should the parser change?"

| Option | What you gain | What you give up | Best if |
|---|---|---|---|
| Fix only the failing case (recommended) | One file changes today | Other cases stay as they are | The bug blocks a release |
| Rewrite the parser | Every input format gets retested | Two days of work | More formats are coming |
| Leave it for now | No work now | The error stays until next week | Nobody hits it yet |

Combining the fix and the rewrite is ruled out: the rewrite already covers the
failing case.

| Hard to read | Plain |
|---|---|
| "Do you want option A, B or C for publishing?" (for a publish confirmation) | "Publish the page now?" |

### 6. Show shaped content as tables or diagrams

Option comparisons, flows of three or more steps, branches and state
changes go into a table or diagram, following loom-visualization's
`SKILL.md`.

| Hard to read | Plain |
|---|---|
| Three paragraphs, each describing one option's cost, speed and risk | One table with a row per option and columns for cost, speed and risk |

### 7. Give only what the user needs

Leave out process detail unless the user asks for it.

| Hard to read | Plain |
|---|---|
| "First I grepped the repo, then I read four files, then I ran the tests twice..." | "The tests pass. Ask if you want the steps I took." |

## Internal terms

Replace these with what they do before sending, or add them in brackets
after the plain words when the user needs the name:

- loom station names (capture-intent, write-spec, write-plan, build,
  review, ship, maintain)
- gate ids and rule ids
- requirement ids and finding ids (REQ-3, F-4)
- lane
- attestation
- probe
- blind run
- temporary names the agent coined during the work
- file names and function names

## Rewrite steps

When the user asks for a plainer explanation, rewrite the last reply in
this order:

1. Make the first sentence the conclusion: the most important news or the answer. Put no announcement before it ("let me explain again", 「我重新說明一次」), no heading, and no background.
2. Replace every internal term with what it does, and turn each abstraction into who does what and what the user sees.
3. Keep the facts: rewriting changes wording, never what happened; keep every fact, number, name and outcome from the original, and keep its lead news. Translate a term by saying what it does instead of substituting a different thing: a review stays a review, and an agent is not a person; never refer to something the original did not say.
4. Cut process detail the user's decision does not need; never cut the lead news or an outcome.
5. Check for metaphor words ("like", "imagine", "think of it as", analogies) before sending, and replace each with the literal statement.

## Before and after examples

Real hard-to-read phrases from past replies, each with a literal rewrite.
Where the original context is not recorded here, the rewrite is written
generically; keep the pattern, not the details.

| Hard to read | Plain |
|---|---|
| 「small lane／full lane」 | 「小改動只跑較短的檢查；大改動跑完整的檢查。」 |
| 「REQ-1 設計不夠嚴」 | 「第一條需求還沒寫清楚『要發生什麼』，所以沒有測試能證明它做到了〔REQ-1〕。」 |
| 「殺極性突變體」 | 「我們把程式裡的一個判斷條件改成相反（例如 `>` 改成 `<`），確認有測試因此失敗；現在這種錯誤會被測試抓到。」 |
| 「薄殼開火，寫進本 repo 自己的 ledger」 | 「那支很短的包裝腳本執行了，並把結果寫進這個 repo 的紀錄檔。」 |
| 「建立可替換邊界」 | 「把跟外部服務溝通的程式集中到一個函式；之後要換服務時，只改這個函式。」 |
| 「F-4 的裁定方向…〔derived〕〔proposed〕」 | 「第 4 個審查發現：審查者傾向某個做法。這是推論出來的，不是你說過的，而且還只是建議，等你決定。」 |

Metaphors that slipped into rewrites, and what to write instead:

| Hard to read | Plain |
|---|---|
| 「就像插座」 | 「只要照這個輸入格式，任何工具都能接上，不用改程式。」 |
| 「家裡三個門禁」 | 「發布前依序跑三項檢查；三項都通過才會發布。」 |

## Conversation situation tables

Eight situations that come up in chat replies. Each table below is an
example: keep the headers, replace the rows, keep cells short.

### 1. Decision consequences

When to use: the user must choose how to do something, and each choice
changes what they get. This differs from `templates/01-option-comparison.md`:
that template scores options on measured criteria (latency, cost); this
table shows what each choice gains and gives up for the user.

| Option | What you gain | What you give up | Best if |
|---|---|---|---|
| Fix the one case (recommended) | Done today | Other cases stay | The bug blocks a release |
| Rewrite the parser | All formats handled | Two days of work | More formats are coming |
| Wait | No work now | Error stays a week | Nobody hits it yet |

### 2. Before and after

When to use: something changed, such as behaviour, wording or a setting,
and the user needs to see what differs.

| Item | Before | After | Impact on you |
|---|---|---|---|
| Reminder timing | Once per session | Every message | Rules stay in effect |
| Error text | "E42" | "File not found" | You see the cause |
| Default depth | Full check | Short check | Faster small changes |

### 3. Progress report

When to use: several pieces of work are under way and the user wants to know
where each one stands.

| Item | Status | Blocked on | Next step |
|---|---|---|---|
| Login page | Done | None | None |
| Export | In progress | None | Add CSV test |
| Billing | Blocked | API key | You send the key |

### 4. Acceptance checklist

When to use: checking whether a change meets its criteria, or is ready to
ship.

| Criterion | Met? | Note |
|---|---|---|
| Tests pass | Yes | 42 passed |
| Works offline | No | Cache missing |
| Docs updated | Not applicable | No user-facing change |

### 5. Confirmed, unconfirmed, to decide

When to use: some facts are verified, some are assumed, and some need the
user's decision.

| Item | Status | Basis or next step |
|---|---|---|
| Crash cause | Confirmed | Reproduced in a test |
| Affects Windows | Unconfirmed | Run on Windows CI |
| Support old format | To decide | You choose yes or no |

### 6. Findings and recommendations

When to use: a review, audit or investigation found problems and each needs
a recommended fix.

| Problem | Severity | Recommendation |
|---|---|---|
| Password in log | High | Remove the log line |
| Slow search | Medium | Add an index |
| Typo in button | Low | Fix the text |

### 7. Risks

When to use: a plan could go wrong in known ways and the user needs to weigh
them.

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Upgrade needs re-approval | High | Feature stays off | Say so in release notes |
| Migration loses data | Low | Records gone | Back up first |
| Slower first load | Medium | Users wait longer | Load in background |

### 8. Support matrix

When to use: a feature works in some environments and not others.

| Feature | Environment A | Environment B | Environment C |
|---|---|---|---|
| Reminder | Yes | Yes | No |
| Mermaid display | No | Yes | Not applicable |
| Diagram check | Yes | Yes | Yes |

In a real reply, replace "Environment A / B / C" with the environment names.

## Table-writing rules and common mistakes

### Rules

1. Use a table only when each item has three or more attributes; otherwise use a list (Google, Microsoft). Exception: a key-value summary table, one label plus one value per row (such as the incident report summary S19 or the component state matrix D7), may have two columns.
2. Put the value that identifies the row in the leftmost column (Microsoft).
3. Keep columns few and cells to one line; in chat, use at most 4 to 5 columns. The one-line cell is Microsoft's rule; the column cap is derived from fitting chat width, not a published rule.
4. Write specific headers, and do not let a header and its cell form a sentence (Microsoft).
5. Order rows logically; order columns by importance, with related columns next to each other (Google, NN/g).
6. Never leave a cell blank; write None or Not applicable (Microsoft).
7. Split a large table into smaller tables (Google).
8. State the conclusion in a sentence before the table, not inside a cell.
9. Keep cells short; put explanations outside the table.
10. Use a fixed small vocabulary in status columns, such as Done, In progress, Blocked.

Rules 8 to 10 come from analysing real user complaints about hard-to-read
agent replies, not from a published source.

### Status symbols

- Distinguish status by shape, not colour alone: ✓ and ✗ read without
  colour (Microsoft adds a check mark to green and a capital X to red).
- Coloured dots (🟢🟡🔴) need a text legend, because colour must not be the
  only way information is shown (WCAG 1.4.1).
- For graded comparisons, the Japanese four-level scale ◎ ○ △ × carries more
  than a yes/no pair and does not depend on colour.

### In-cell visuals

What can go inside a table cell, and what cannot:

- Block bars (`████░░░░`): usable only with the number in the same cell. Google
  Cloud SDK's accessibility mode replaces Unicode bars with plain percentages,
  so the vendor treats a bar alone as inaccessible.
- Text sparklines (`▁▂▃▄▅▆▇█`): usable. Tufte says a sparkline can go wherever
  a word or number can, tables included. The ceiling is 8 levels.
- Check and cross marks: shape over hue; see Status symbols above.
- Coloured dots: only with a text legend (WCAG 1.4.1); see Status symbols
  above. The ◎ ○ △ × scale is there too.
- A blank cell for "no": not allowed; see table rule 6.
- Cell background colour or a heatmap: not possible in plain Markdown. GFM
  cells hold only inline content, and GitHub strips inline style and class.
- shields.io badges: usable but risky. Badges are cached by design, and a dead
  third-party badge host breaks every badge that uses it.
- `<progress>` and `<meter>`: depend on the renderer (Obsidian shows them,
  GitHub strips them). They are not interchangeable: the WHATWG specification
  says a meter should not be used to show progress.
- Inline `<svg>`: do not use; GitHub's Markdown renderer skips `<svg>`
  elements.

Layout: when cells hold text, compare items across a row; when cells hold
numbers, compare down a column so the digits line up (a Japanese table
convention).

### Table or chart

- Per item: one data point → a list; two related data points → term and
  value lines; three or more → a table (Google).
- When the user looks up or compares individual values, or the values must be
  precise, use a table. When the message is in the shape of the data (a
  trend, a pattern, an exception), use a chart. When both matter, show both
  (Stephen Few).
- A 2×2 with categorical axes (important or not × urgent or not) can be a
  table. A 2×2 with continuous axes (market share × growth rate) cannot: the
  meaning is in each item's position, so use a chart.
- When the reader compares the data in two directions, across rows and down
  columns, a table beats a chart (Datawrapper).
- A table is the formal text alternative for a complex diagram such as a
  flowchart or an org chart: W3C's own long-description example is a table
  (W3C WAI, complex images).

### Time in tables

Time goes into a table in two opposite ways:

- Time as the column axis (Q1 to Q4, measurement dates, lifecycle stages):
  replaces a drawn Gantt chart or roadmap.
- Time as a cell value (What | Who | When): replaces a checklist.

A Now-Next-Later roadmap orders its columns by confidence, not by dates
(ProdPad, a vendor source); see entry B22 in `references/tables-business.md`.
For events placed on dates, use `templates/10-timeline.md`.

### When not to use a table

- For layout: placing content side by side is not a table (GOV.UK).
- For a single column: use a list (Google, Microsoft).
- With merged cells or multi-level headers: split into several simple tables
  (Red Hat, W3C).
- With a table inside a cell: screen readers read the inner table before the
  next outer cell (WCAG F49).
- For an incomplete comparison: if an attribute is unknown for some items,
  leave that attribute out of the table (NN/g).
- In the middle of numbered steps (Google).

### Options as columns or rows

NN/g puts options in columns and attributes in rows for comparison tables.
In a narrow chat window, use columns only for three or fewer options, and
rows for more. This is a judgment for chat width, not a published rule, and
it departs from NN/g when there are more than three options.

## Sources

- Google Developer Documentation Style Guide, tables: https://developers.google.com/style/tables
- Google Technical Writing, lists and tables: https://developers.google.com/tech-writing/one/lists-and-tables
- Microsoft Writing Style Guide, tables: https://learn.microsoft.com/en-us/style-guide/scannable-content/tables
- Microsoft, accessible Word documents: https://support.microsoft.com/en-us/accessibility/word/make-your-word-documents-accessible-to-people-with-disabilities
- NN/g, data tables: https://www.nngroup.com/articles/data-tables/
- NN/g, comparison tables: https://www.nngroup.com/articles/comparison-tables/
- GOV.UK Design System, table: https://design-system.service.gov.uk/components/table/
- Red Hat supplementary style guide, accessibility of tables: https://redhat-documentation.github.io/supplementary-style-guide/#accessibility-tables
- W3C WAI, multi-level tables: https://www.w3.org/WAI/tutorials/tables/multi-level/
- W3C WAI, complex images: https://www.w3.org/WAI/tutorials/images/complex/
- Datawrapper, what to consider when creating tables: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables
- WCAG F49: https://www.w3.org/WAI/WCAG22/Techniques/failures/F49
- WCAG 1.4.1 Use of Color: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- Stephen Few, Effectively Communicating Numbers: https://www.perceptualedge.com/articles/Whitepapers/Communicating_Numbers.pdf
- Japanese four-level scale ◎○△×: https://itoyusuke.net/1020/
- Japanese table layout, text across and numbers down: https://maki-ichikawa.com/2019/08/01/table2019/
- Google Cloud SDK accessibility mode (replaces Unicode bars): https://docs.cloud.google.com/sdk/gcloud/reference/alpha/topic/accessibility
- Tufte, sparkline theory and practice: https://www.edwardtufte.com/notebook/sparkline-theory-and-practice-edward-tufte/
- GFM specification: https://github.github.com/gfm/
- github/markup (strips style and class): https://github.com/github/markup
- README badge host risk: https://movermeyer.com/2018-06-22-readme-badges-are-vulns/
- WHATWG, form elements (meter is not for progress): https://html.spec.whatwg.org/dev/form-elements.html
- GitHub skips inline SVG: https://alexwlchan.net/notes/2024/how-to-render-svgs-on-github/
- ProdPad, Now-Next-Later roadmap: https://www.prodpad.com/blog/invented-now-next-later-roadmap/
- Paul Nutt, 400 decisions: https://news.osu.edu/half-of-business-decisions-fail-because-of-managements-blunders-new-study-finds/
- Nutt, P. C. (1999), "Surprising but true: Half the decisions in organizations fail", Academy of Management Executive 13(4): https://journals.aom.org/doi/10.5465/AME.1999.2570556
- Chernev et al. (2015), choice overload: https://www.sciencedirect.com/science/article/abs/pii/S1057740814000916
