# Tables in software development documents

Load this when: the user asks for one of these documents: incident postmortem, 障害報告書 (incident report summary), test plan or test matrix, traceability matrix, compatibility matrix, migration or deprecation guide, API parameter table, runbook or troubleshooting guide, RACI, ADR or RFC options, feature-flag rollout plan, release notes or deprecation schedule, risk register, RAID log, threat model (STRIDE).

A chat reply about a conversation situation (decision, before and after,
progress, checklist, confirmed and unconfirmed, findings, risks, support
matrix) uses `references/plain-language.md` instead of this file.

How to read an entry: "When" is the document situation, "Columns" the
headers, "In chat" whether the table fits a chat reply and, if not, the
reduced columns to use there. A marker in brackets repeats the research's own
caution: [reconstructed] means the table form was rebuilt from prose, not
copied from a live table; [unverified] means the source could not be fully
checked. A "Pointer:" entry is the same usage as a table written elsewhere;
use that table. The example tables in S21 to S31 are illustrations written
for this file; the pattern names and sources come from the research.

Many canonical software templates are prose or bullet lists by design
(MADR, the Rust RFC template, Keep a Changelog, most pull request
templates). Tables are the norm for look-up content with fixed columns and
many similar rows; for reasoning-heavy sections, prefer prose and headings
even when a team habitually puts them in a table.

### S1. ADR options and trade-offs

- When: the "Considered options" section of an architecture decision record.
- Columns: `Option | Pros | Cons`
- In chat: fits (3 columns). When the user must choose, use the general Decision consequences table instead.
- Marker: [reconstructed convention]. The official MADR template is prose and bullets; the table is a common community adaptation.

| Option | Pros | Cons |
|---|---|---|
| PostgreSQL | Mature, strong consistency | Ops overhead at scale |
| DynamoDB | Fully managed, scales easily | Vendor lock-in, query limits |
| SQLite | Zero-ops, simple | Not built for concurrent writes |

Source: https://github.com/adr/madr/blob/develop/template/adr-template.md

### S2. RFC alternatives considered

- When: the "Rationale and alternatives" section of an RFC, explaining why this design beats the others.
- Columns: `Option | Pros | Cons | Why rejected`
- In chat: fits (4 columns, one-line cells).
- Marker: [reconstructed, unverified as literal table]. The official template is prose only.

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| New syntax | Explicit, discoverable | Breaking change | Too disruptive for stable users |
| Macro-based | No syntax change | Harder to read errors | Fails "easy to understand" goal |
| Do nothing | No cost | Doesn't solve problem | Leaves known pain point |

Source: https://github.com/rust-lang/rfcs/blob/master/0000-template.md

### S3. 技術選定比較表 (technology selection comparison table)

- When: choosing between frameworks, libraries or tools; a weighted scoring comparison common on Japanese engineering blogs.
- Columns: `評価軸 (criterion) | 重み (weight) | 候補A 素点/加重 (candidate A raw/weighted) | 候補B | ... | 加重合計 (weighted total)`
- In chat: does not fit beyond 3 candidates and 4 criteria; in chat use `Criterion | Weight | Candidate A | Candidate B` with the weighted score only, and state the winner in a sentence before the table.
- Marker: verified as a real table with matching columns. The general weighted method is B1 in `references/tables-business.md`.

| 評価軸 | 重み | Laravel (素点/加重) | Rails (素点/加重) | Next.js (素点/加重) |
|---|---|---|---|---|
| 開発初速 | 2.0 | 4 / 8.0 | 5 / 10.0 | 3 / 6.0 |
| 学習コスト | 1.5 | 4 / 6.0 | 3 / 4.5 | 3 / 4.5 |
| **加重合計** | | **32.0** | **29.5** | **27.5** |

Source: https://syusodo.co.jp/tech-blog/articles/tech-selection-decision-process

### S4. Weighted decision matrix

Pointer: `references/tables-business.md` entry B1 "Weighted decision matrix". Software sources for the same method (method confirmed, example cells reconstructed): https://www.projectmanager.com/templates/decision-matrix-template, https://affine.pro/blog/decision-matrix-template

### S5. PR before and after summary

Pointer: `references/plain-language.md` situation "Before and after"; in a pull request description use `Area | Before | After` so reviewers scan behaviour changes without the diff. [reconstructed, unverified as literal table]: GitHub's guidance is prose and checklists. Before/after tables have no authoritative source. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository

### S6. Test plan or test matrix

- When: manual or exploratory QA; each row tracks one test case through execution.
- Columns: `Test Case ID | Test Steps | Expected Result | Actual Result | Status`
- In chat: 5 columns is the limit; in chat drop Test Steps and use `Test Case ID | Expected Result | Actual Result | Status`.
- Marker: verified, standard in QA tooling.

| Test Case ID | Test Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-01 | Log in with valid creds | Redirect to dashboard | Redirect to dashboard | Pass |
| TC-02 | Log in with wrong password | Show error message | Show error message | Pass |
| TC-03 | Submit empty form | Inline validation errors | Form submitted silently | Fail |

Sources: https://artoftesting.com/test-case-template, https://testsigma.com/blog/requirements-traceability-matrix-template/

### S7. Compatibility table

Pointer: `references/plain-language.md` situation "Support matrix"; in a document put features in rows, browsers or platforms in columns (`Feature | Chrome | Firefox | Safari | Edge`) and the first supported version or ✅/⚠️/❌ in each cell, as MDN does. "Compatibility table" is the established name; avoid "support matrix" as the document name. Structure verified from MDN's own guideline. https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Page_structures/Compatibility_tables

### S8. Feature flag rollout plan

- When: tracking staged rollout of feature flags across environments, with an owner.
- Columns: `Flag | Stage | % Rollout | Owner | Status`
- In chat: fits at 5 columns; for a short reply drop Owner.
- Marker: the Stage column is [reconstructed, unverified as literal table]; the other columns are verified from real product vocabulary.

| Flag | Stage | % Rollout | Owner | Status |
|---|---|---|---|---|
| new-checkout-flow | Canary | 5% | @alice | Ramping |
| dark-mode-v2 | GA | 100% | @bob | Released |
| legacy-search | Cleanup | 0% | @carol | Killed |

Sources: https://launchdarkly.com/docs/home/flags/list, https://www.growthbook.io/insights/feature-flags-in-postgres

### S9. Incident postmortem timeline

- When: after an incident is resolved, recording what happened minute by minute.
- Columns: `Time (UTC) | Event | Data Link`
- In chat: fits (3 columns).

| Time (UTC) | Event | Data Link |
|---|---|---|
| 14:02 | Error rate on `checkout-api` exceeds 5% | Grafana |
| 14:09 | On-call paged, incident declared SEV-1 | PagerDuty |
| 14:47 | Rollback deployed, error rate returns to baseline | Deploy log |

Sources: https://sre.google/sre-book/example-postmortem/, https://response.pagerduty.com/after/post_mortem_template/

### S10. Incident postmortem action items

- When: in the same postmortem, tracking fixes that prevent a repeat.
- Columns: `Action Item | Owner | Due | Status`
- In chat: fits (4 columns).
- Marker: the base columns `Action Item | Type | Owner | Bug` are verified from the Google SRE book; Due and Status were added following PagerDuty's accountability practice.

| Action Item | Owner | Due | Status |
|---|---|---|---|
| Add circuit breaker to payment gateway client | @alice | 2026-09-30 | TODO |
| Add alert on p99 latency > 800ms | @bob | 2026-09-25 | IN PROGRESS |
| Document rollback runbook | @carol | 2026-09-20 | DONE |

Sources: https://sre.google/sre-book/example-postmortem/, https://postmortems.pagerduty.com/culture/accountability/

### S11. Risk register

- When: project planning or delivery, tracking identified risks and who owns each mitigation. Also used for business and project risk (B10 in `references/tables-business.md` points here).
- Columns: `Risk | Likelihood | Impact | Mitigation | Owner` (full templates add Category, Score, Status, Comments or Review date)
- In chat: use the general Risks table in `references/plain-language.md` (drop Owner, Status and Review date).

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Third-party payment API deprecated | Medium | High | Migrate to v2 API before EOL date | @dave |
| Key backend engineer leaves mid-sprint | Low | High | Pair-program critical modules now | @erin |
| Load test reveals DB bottleneck | High | Medium | Add read replica ahead of launch | @frank |

Sources: https://www.atlassian.com/software/confluence/templates/risk-register, https://www.rocketlane.com/blogs/risk-register-template, https://catalog.monex.co.jp/article/?p=49009, https://en.wikipedia.org/wiki/Risk_register

### S12. RACI matrix

- When: at project start, making clear who does the work, who signs off, who is consulted and who is informed. Also called a responsibility assignment matrix. Use "RACI", not "swimlane table": a swimlane is defined only as a diagram.
- Columns: `Task | Responsible | Accountable | Consulted | Informed`
- In chat: fits at 5 columns; with many roles, name at most 4 to 5 roles per message.

| Task | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Write test plan | QA Lead | Eng Manager | Product Manager | Dev Team |
| Approve API design | Backend Dev | Tech Lead | Security Team | Frontend Dev |
| Deploy to production | DevOps | Eng Manager | None | All Stakeholders |

Sources: https://www.projectmanager.com/templates/raci-matrix-template, https://www.vertex42.com/ExcelTemplates/raci-matrix.html, https://sinnaps.com/en/project-management-blog/raci-matrix-template, https://en.wikipedia.org/wiki/Responsibility_assignment_matrix

### S13. Weekly status report

Pointer: `references/plain-language.md` situation "Progress report"; a weekly engineering status document uses the same shape (`Item | Status | Blocker | Next`). [reconstructed, unverified as literal table]: the sources describe narrative paragraphs, not a rendered table. https://recapline.com/blog/weekly-status-report-template-engineering, https://asana.com/templates/status-report

### S14. Known and unknown issues

Pointer: `references/plain-language.md` situation "Confirmed, unconfirmed, to decide"; in a README or release notes, a Known Issues table often uses `Issue | Description | Workaround | Status`. [reconstructed, unverified: no single standard template found]; closest real precedents are an enterprise known-issues page and the ITIL known-error database. https://taasupportportal.wolterskluwer.com/uk/known-issue/CCH-Central---K-3127295, https://en.wikipedia.org/wiki/Known_error

### S15. Migration or deprecation mapping, old to new

- When: a library ships a breaking API change and readers look up the replacement for an old parameter or method.
- Columns: `Legacy version | Current version | Integration tips`
- In chat: fits (3 columns); keep each tip to one line.
- Marker: verified as a real table (Stripe, "Parameter conversion").

| Legacy version | Current version | Integration tips |
|---|---|---|
| `amount` | Sum of `line_items` | Total = sum of line items passed to Checkout |
| `email` | `Session.customer_email` | Prefill at Session creation |
| `token` or `source` | `success_url` | No JS callback; redirect via `success_url` |

Source: https://docs.stripe.com/payments/checkout/migration

### S16. API reference parameter table

- When: documenting a REST or API endpoint's inputs so developers scan name, type and constraints without prose.
- Columns: `Name | Type | Description`; OpenAPI practice adds explicit `Required` and `Located in` (query, path, header) columns.
- In chat: does not fit a long endpoint; keep it in the document. For one or two parameters in chat, use `Name | Type | Required | Meaning` with one-line meanings.
- Marker: verified as a real table (GitHub). The OpenAPI specification is confirmed; its rendered table is generated by the UI, not static markdown.

| Name | Type | Description |
|---|---|---|
| `owner` | string | Account owner of the repository. Not case sensitive. |
| `repo` | string | Repository name without `.git`. Not case sensitive. |
| `ref` | string | Commit, branch or tag. Default: the default branch. |

Sources: https://docs.github.com/en/rest/repos/contents, https://swagger.io/docs/specification/v3_0/describing-parameters/

### S17. Deprecation schedule or release-notes table

- When: tracking when features are deprecated and shut down, as a table alternative to a changelog.
- Columns: `Feature | Deprecated | Shutdown date | For more information`
- In chat: fits (4 columns).
- Marker: verified as a real table (Google Cloud). Keep a Changelog and most real changelogs group bullets under Added, Changed, Deprecated, Removed, Fixed, Security; a table is the exception and suits deprecation schedules best.

| Feature | Deprecated | Shutdown date | For more information |
|---|---|---|---|
| NVIDIA P4 | Aug 1, 2026 | Aug 1, 2027 | NVIDIA P4 end of support |
| Customer-supplied encryption keys (CSEKs) | Jun 15, 2026 | Jun 16, 2027 | Deprecation of CSEKs |
| NVIDIA P100 | Sep 15, 2025 | Sep 15, 2026 | NVIDIA P100 end of support |

Sources: https://docs.cloud.google.com/compute/docs/deprecations, https://keepachangelog.com/en/1.1.0/

### S18. Runbook or troubleshooting table

- When: sending the reader quickly from an observed symptom to the likely cause and fix.
- Columns: `Symptom | Possible Cause | Fix` (normalised from Microsoft's verified `Category | Typical symptom | Where to start`)
- In chat: fits (3 columns). When reporting problems found in a review, use the general Findings and recommendations table instead.
- Marker: verified as a real table.

| Symptom | Possible Cause | Fix |
|---|---|---|
| Client can't reach server/instance | Network or instance reachability | See network-related error article |
| Sign-in fails, SSPI context error | Authentication/Kerberos misconfiguration | See "Cannot generate SSPI context" article |
| TLS handshake fails, certificate untrusted | Certificate chain not trusted | See certificate-chain article |

Source: https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/connect/resolve-connectivity-errors-overview

### S19. 障害報告書サマリ表 (incident report summary table)

- When: after an outage, so managers or customers grasp scope and severity without reading the full report.
- Columns: `項目 (item) | 内容 (content)`, key-value rows such as 障害発生日時 (start time), 影響範囲 (impact scope), 復旧日時 (recovery time), 原因 (cause), 再発防止策 (prevention).
- In chat: fits (2 columns, short values).
- Marker: the 10-item field list and section headings are verified; the table rendering itself is [reconstructed, unverified as literal table]: both sources use prose sections.

| 項目 | 内容 |
|---|---|
| 障害発生日時 | 2026-09-10 14:32 |
| 影響範囲 | 決済API利用ユーザー約1,200名、注文確定不可 |
| 復旧日時 | 2026-09-10 15:10（38分後） |

Sources: https://www.qbook.jp/column/1793.html, https://notepm.jp/template/failure-report

### S20. Migration plan, team-level before and after

Pointer: `references/plain-language.md` situation "Before and after"; for a team-level migration use `Area | Before (現状) | After (移行後) | Impact on team`, covering process and operations rather than code mapping (code mapping is S15). [reconstructed, unverified: no live table found]; the As-Is/To-Be concept is confirmed, but in practice it appears as slides or diagrams. Before/after tables have no authoritative source. https://www.signavio.com/wiki/process-discovery/as-is-to-be-process-mapping/, https://novajournal.net/mini-series/structuring/vol-6/

### S21. Decision table

- When: a rule set of conditions and actions that replaces a decision tree or flowchart; a formal technique in testing, backed by the OMG DMN specification and the ISTQB glossary.
- Columns: conditions and actions as rows, one rule per column (`Condition | R1 | R2 | R3`).
- In chat: use the table form in `templates/03-branching-decision.md`; do not repeat it here. A decision table is not a decision matrix: the table maps conditions to actions, the matrix scores options against criteria (B1).

Sources: https://en.wikipedia.org/wiki/Decision_table, https://www.omg.org/spec/DMN/, https://istqb-glossary.page/decision-table-testing/

### S22. State-transition table

- When: specifying a finite-state machine; a state-transition table is one of the standard alternatives to a state diagram.
- Columns: current state × input → next state.
- In chat: use the table form in `templates/05-state-lifecycle.md`; do not repeat it here.

Source: https://en.wikipedia.org/wiki/State-transition_table

### S23. Truth table

- When: listing every input combination of a logical expression and its result, in place of a logic-gate diagram.
- Columns: one column per input variable, then the result.
- In chat: fits for up to three inputs (eight rows); beyond that, keep it in the document.

| A | B | A AND B |
|---|---|---|
| true | true | true |
| true | false | false |
| false | false | false |

Source: https://en.wikipedia.org/wiki/Truth_table

### S24. Traceability matrix (RTM)

- When: mapping requirements to tests, in place of a bipartite diagram; row and column totals expose requirements no test covers. "Coverage matrix" is an informal synonym with no authoritative source (not in the ISTQB glossary).
- Columns: `Requirement | T-01 | T-02 | ... | Covered`, with `x` where a test covers the requirement.
- In chat: fits up to about three tests; for more, report only the uncovered requirements as a list.

| Requirement | T-01 | T-02 | Covered |
|---|---|---|---|
| R-01 | x | None | 1 |
| R-02 | None | None | 0 |

Sources: https://en.wikipedia.org/wiki/Traceability_matrix, https://testsigma.com/blog/requirements-traceability-matrix-template/

### S25. Morphological box (Zwicky)

- When: laying out a combinational design space; each row is a parameter, each cell a value, and one solution picks one cell per row. Mermaid has no matching diagram type.
- Columns: `Parameter | Value 1 | Value 2 | Value 3`
- In chat: fits with up to three values per parameter.

| Parameter | Value 1 | Value 2 | Value 3 |
|---|---|---|---|
| Storage | SQLite | PostgreSQL | Object store |
| Sync | None | Polling | Push |

Source: https://en.wikipedia.org/wiki/Morphological_analysis_(problem-solving)

### S26. Risk matrix

- When: rating risk level from likelihood × severity, as distinct from the risk register (S11), which lists individual risks.
- Columns: likelihood levels as rows, severity levels as columns, risk level in each cell.
- In chat: fits as a 3 × 3 grid with text levels (never colour alone).

| Likelihood \ Severity | Low | Medium | High |
|---|---|---|---|
| High | Medium | High | High |
| Medium | Low | Medium | High |
| Low | Low | Low | Medium |

Source: https://en.wikipedia.org/wiki/Risk_matrix

### S27. RAID log

- When: tracking Risks, Assumptions, Issues and Dependencies in one table, folded by a Category column.
- Columns: `Category | Item | Owner | Status`
- In chat: fits (4 columns).
- Marker: named in the earlier table research's pattern list; no dedicated source URL was recorded for it.

| Category | Item | Owner | Status |
|---|---|---|---|
| Risk | Vendor API changes | @dave | Open |
| Assumption | Traffic stays under 1k rps | @erin | Unchecked |
| Dependency | Auth service v2 release | @frank | Waiting |

Source: https://en.wikipedia.org/wiki/Risk_register (the register pattern it extends)

### S28. STRIDE-per-element

- When: threat modelling; each data-flow-diagram element type is checked against the six STRIDE threat categories.
- Columns: `Element type | S | T | R | I | D | E`
- In chat: does not fit (7 columns); in chat list per element only the categories that apply: `Element | Applicable threats | Mitigation`.

| Element type | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| External entity | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Data store | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |

Source: https://learn.microsoft.com/en-us/archive/blogs/larryosterman/threat-modeling-again-stride-per-element

### S29. Feature table

- When: showing which features each plan tier or edition includes (✓/✗). GitLab's documentation adds hidden screen-reader text beside the symbols. "Feature matrix" is not an established name; call it a feature table.
- Columns: `Feature | Tier 1 | Tier 2 | Tier 3`
- In chat: fits with up to three tiers; use ✓ and ✗ (shape, not colour).

| Feature | Free | Premium | Ultimate |
|---|---|---|---|
| Merge requests | ✓ | ✓ | ✓ |
| Code owners | ✗ | ✓ | ✓ |

Source: https://docs.gitlab.com/development/documentation/styleguide/

### S30. Confusion matrix

- When: evaluating a classifier; actual classes as rows, predicted classes as columns.
- Columns: `Actual \ Predicted | Class A | Class B`
- In chat: fits for two or three classes.

| Actual \ Predicted | Spam | Not spam |
|---|---|---|
| Spam | 90 | 10 |
| Not spam | 5 | 895 |

Source: https://en.wikipedia.org/wiki/Confusion_matrix

### S31. Correlation matrix

- When: showing pairwise correlation between variables; symmetric n × n.
- Columns: one column per variable, one row per variable.
- In chat: fits for up to four variables; beyond that, name only the strongest pairs in a sentence.
- Marker: named in the earlier table research's pattern list; no dedicated source URL was recorded for it.

| Variable | Latency | CPU | Errors |
|---|---|---|---|
| Latency | 1.00 | 0.82 | 0.40 |
| CPU | 0.82 | 1.00 | 0.35 |
| Errors | 0.40 | 0.35 | 1.00 |

Source: [unverified] the research recorded no URL for this pattern; general definition at https://en.wikipedia.org/wiki/Correlation, added here and not checked by the research.

## Names without an authoritative source

Common in practice, but no authoritative source was found; say so when you
use them:

- before/after tables (S5, S20, and the general Before and after situation)
- coverage matrix (an informal synonym for a traceability matrix, S24)
- feature matrix or competitive matrix: the artifact is standard, the name "matrix" is not
- a 5-Whys analysis as a table (Asana's own template is a list)
- a generic "roadmap table" (use Now-Next-Later roadmap, B22 in `references/tables-business.md`)
- text sparklines specifically inside Markdown table cells

ADRs are not table-oriented: MADR uses bullets, and the Rust RFC template has
no tables. An options × criteria table in an ADR is a community adaptation.
