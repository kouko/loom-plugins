# Tables in business strategy, consulting and product management documents

Load this when: the user asks for one of these documents: weighted or Pugh matrix, RICE, ICE, MoSCoW or WSJF prioritisation, SWOT or TOWS, competitive analysis, Five Forces, stakeholder analysis, scenario planning, business case or cost-benefit, OKR or KPI tracker, assumption log, go/no-go review, pricing tiers, Kano evaluation, decisional balance sheet, Now-Next-Later roadmap.

A chat reply about a conversation situation (decision, before and after,
progress, checklist, confirmed and unconfirmed, findings, risks, support
matrix) uses `references/plain-language.md` instead of this file.

How to read an entry: "When" is the document situation, "Columns" the
headers, "In chat" whether the table fits a chat reply and, if not, the
reduced columns to use there. The chat notes for B1 to B18 come from the
original business research as practical judgment, not from a separate rule
source. [unverified] marks a source that could not be fully checked. A
"Pointer:" entry is the same usage as a table written elsewhere; use that
table. The example tables and chat notes in B19 to B23 are written for this
file; the pattern names and sources come from the earlier table research.

### B1. Weighted decision matrix

- When: choosing among three or more options on several weighted criteria (vendor, tool, feature bet). Also called a decision matrix; not the same as a decision table (S21 in `references/tables-software.md`). Software variants point here (S4); the Japanese 技術選定比較表 is S3.
- Columns: `Criterion | Weight | Option A score | Option B score | Option C score`, with a total row (or transposed: `Option | Criterion1×w | Criterion2×w | Weighted Total`).
- In chat: fits with at most 3 options and 4 criteria; beyond that the weighted arithmetic is hard to follow in a narrow window, so move it to a document or ask about one option or criterion at a time.

| Criterion (weight) | Vendor A | Vendor B | Vendor C |
|---|---|---|---|
| Cost (×3) | 4 (12) | 3 (9) | 5 (15) |
| Reliability (×2) | 5 (10) | 4 (8) | 3 (6) |
| **Total** | 22 | 17 | 21 |

Sources: https://goleansixsigma.com/weighted-criteria-matrix/, https://airfocus.com/blog/weighted-decision-matrix-prioritization/, https://en.wikipedia.org/wiki/Decision_matrix

### B2. Pugh matrix

- When: comparing several design or product concepts against one baseline ("datum") concept. Also called the decision-matrix method.
- Columns: `Criterion | Datum | Concept B (+/S/−) | Concept C (+/S/−)`; S means same as the datum (some sources write 0).
- In chat: fits; the +/S/− symbols are compact and scan fast even with mixed Chinese or Japanese labels. Good for asking the user "compared with what we do now".

| Criterion | Datum | Concept B | Concept C |
|---|---|---|---|
| Ease of use | S | + | − |
| Cost | S | − | + |
| Time to build | S | + | + |

Sources: https://www.smartsheet.com/content/pugh-matrix-templates-examples, https://sixsigmastudyguide.com/pugh-analysis/, https://en.wikipedia.org/wiki/Decision-matrix_method

### B3. RICE prioritization

- When: ranking product or feature ideas by expected value over effort. RICE originated at Intercom.
- Columns: `Initiative | Reach | Impact | Confidence | Effort | RICE Score`
- In chat: marginal; 6 columns is wide for a narrow window. In chat drop Confidence, or show only `Initiative | Score` with a one-line reason.

| Initiative | Reach | Impact | Confidence | Effort | Score |
|---|---|---|---|---|---|
| Onboarding redesign | 2000 | 2 | 80% | 3 | 1067 |
| Export to CSV | 500 | 1 | 100% | 1 | 500 |
| Dark mode | 3000 | 0.5 | 50% | 2 | 375 |

Sources: https://whatfix.com/blog/rice-scoring-model/, https://kayako.com/blog/rice-prioritization/, https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/

### B4. ICE score or value vs effort

- When: quick, low-rigour ranking when the reach data RICE needs is not available.
- Columns (ICE): `Idea | Impact (1-10) | Confidence (1-10) | Ease (1-10) | Score`
- Columns (value/effort 2×2 as a table): `Idea | Value (H/L) | Effort (H/L) | Quadrant (Quick Win/Big Bet/Fill-in/Money Pit)`. NN/g calls this a prioritization matrix; prefer that name to "impact-effort matrix".
- In chat: fits very well; 3 to 4 short columns suit a quick triage of a short backlog.

| Idea | Value | Effort | Quadrant |
|---|---|---|---|
| Fix checkout bug | High | Low | Quick Win |
| New analytics platform | High | High | Big Bet |
| Rebrand icons | Low | Low | Fill-in |

Sources: https://www.productplan.com/glossary/ice-scoring-model/, https://www.koji.so/docs/value-vs-effort-prioritization-matrix, https://www.nngroup.com/articles/prioritization-matrices/

### B5. MoSCoW prioritization

- When: scoping a release or requirements under a fixed deadline.
- Columns: `Requirement | Category (Must/Should/Could/Won't) | Rationale`, or four columns with one category each. The canonical MoSCoW form is a list; the table is a convention.
- In chat: fits; 2 to 3 columns read well even with longer Chinese or Japanese requirement text, as long as cells stay on one line.

| Requirement | Category |
|---|---|
| Login via SSO | Must |
| Dark mode | Should |
| Custom themes | Won't (this release) |

Sources: https://www.itmanagement101.co.uk/moscow-prioritisation/, https://vibe.us/blog/moscow-method/, https://en.wikipedia.org/wiki/MoSCoW_method

### B6. SWOT and TOWS (cross-SWOT)

- When: assessing a strategic situation (SWOT), or turning it into action strategies (TOWS: SO, ST, WO, WT).
- Columns (SWOT as a table, not quadrants): `Category (Strength/Weakness/Opportunity/Threat) | Item | Note`
- Columns (TOWS): `Strategy type (SO/ST/WO/WT) | Internal factor | External factor | Resulting strategy`
- In chat: SWOT as a stacked single-column list per category works; the classic 2×2 quadrant does not render as a markdown table and needs a document or diagram (see B23). The TOWS table (4 short columns) fits.

| Type | Internal | External | Strategy |
|---|---|---|---|
| SO | Strong brand | Growing market | Expand aggressively |
| WT | Weak logistics | New competitor | Partner or exit segment |

Sources: https://library.musubu.in/articles/53793, https://asana.com/resources/swot-analysis

### B7. Competitive analysis matrix

- When: comparing your product or company with 3 to 5 competitors on the same dimensions. The design variant with feature groups is D3 in `references/tables-design.md` and points here.
- Columns: `Dimension | Us | Competitor A | Competitor B | Competitor C`
- In chat: fits up to about 4 columns (you plus 2 to 3 competitors); beyond that move it to a document, because layout breaks easily in a narrow window, worse with Chinese or Japanese labels. With 5 to 7 options, NN/g's name is comparison table.

| Dimension | Us | Competitor A | Competitor B |
|---|---|---|---|
| Price | $29/mo | $39/mo | $19/mo |
| Onboarding | Self-serve | Sales-assisted | Self-serve |
| Support SLA | 24h | 4h | None |

Sources: https://blog.hubspot.com/marketing/competitive-matrix, https://wicle.io/blog/knowledge/competitive-analysis-table, https://www.nngroup.com/articles/comparison-tables/

### B8. Porter's Five Forces as a table

- When: an industry-level assessment of competitive intensity.
- Columns: `Force | Current level (Low/Med/High) | Key driver`
- In chat: fits; always five rows and three short columns, one of the most chat-friendly frameworks.

| Force | Level | Driver |
|---|---|---|
| Threat of new entrants | Low | High capital cost |
| Buyer power | High | Many alternatives |
| Supplier power | Medium | Few certified vendors |

Sources: https://www.cascade.app/blog/porters-5-forces, https://www.aha.io/roadmapping/guide/templates/create/porters5forces

### B9. Stakeholder analysis (power and interest)

- When: planning whom to manage closely and whom to keep informed. For assigning responsibility, the RACI matrix is S12 in `references/tables-software.md`.
- Columns: `Stakeholder | Power (H/L) | Interest (H/L) | Strategy (Manage closely/Keep satisfied/Keep informed/Monitor)`
- In chat: fits (4 short columns); a RACI with many roles gets wide, so name at most 4 to 5 roles per message.

| Stakeholder | Power | Interest | Strategy |
|---|---|---|---|
| CFO | High | Low | Keep satisfied |
| End users | Low | High | Keep informed |
| Project sponsor | High | High | Manage closely |

Sources: https://www.rock.so/blog/power-interest-grid, https://sinnaps.com/en/project-management-blog/raci-matrix-template, https://www.nomura-system.co.jp/contents/stakeholder-analysis/

### B10. Risk register

Pointer: `references/tables-software.md` entry S11 "Risk register"; business and project registers use the same columns (`Risk | Likelihood | Impact | Mitigation | Owner`, sometimes plus Status). In chat, drop Status and Review date and use the general Risks table in `references/plain-language.md`.

### B11. Scenario planning

- When: stress-testing a strategy against several possible futures.
- Columns: `Scenario | Key assumption | Implication for us | Early-warning signal`
- In chat: fits with 3 to 4 scenarios and short cells; full financial output columns (revenue or profit per year) push it into a document.

| Scenario | Assumption | Implication | Signal |
|---|---|---|---|
| Rapid growth | Demand +50% | Need more capacity | Order backlog rising |
| Recession | Demand -30% | Cut discretionary spend | Churn rate rising |
| Status quo | Demand flat | Stay the course | Metrics stable |

Sources: https://www.abacum.ai/blog/scenario-planning-templates-build-your-strategic-finance-toolkit, https://www.synario.com/resources/blog/the-scenario-planning-template/

### B12. Business case or cost-benefit

- When: justifying an investment by comparing costs and benefits over several years.
- Columns: `Item | Type (Cost/Benefit) | Year 1 | Year 2 | Year 3`, or simplified `Item | One-time cost | Ongoing cost | Expected benefit`.
- In chat: a full multi-year NPV/IRR table needs a document or spreadsheet; the simplified 3-column cost/benefit table fits a quick go/no-go discussion.

| Item | Cost | Benefit |
|---|---|---|
| New CRM license | $12k/yr | Faster sales cycle |
| Migration effort | $8k one-time | Cleaner data |
| Training | $2k | Higher adoption |

Sources: https://www.projectmanager.com/templates/cost-benefit-analysis-template, https://asana.com/templates/cost-benefit-analysis

### B13. RAG status report

Pointer: `references/plain-language.md` situation "Progress report"; a red/amber/green project report uses `Workstream | Status (R/A/G) | Issue | Next step`. If the status is a coloured dot (🟢🟡🔴), add the word or a legend, because colour must not be the only signal. https://www.mastt.com/resources/rag-status-template, https://excelguru.io/templates/project-management/project-status-reporting/

### B14. OKR or KPI table

- When: tracking objectives and measurable key results, or reporting KPI progress.
- Columns: `Objective/KPI | Key result / Target | Current | Status`
- In chat: fits (4 columns, short cells); drop Owner and Timeframe in chat and keep them in the tracking document.

| Objective | Key result | Current | Status |
|---|---|---|---|
| Improve reliability | 99.9% uptime | 99.7% | At risk |
| Grow revenue | +20% ARR | +12% | On track |
| Cut support load | -30% tickets | -35% | Done |

Sources: https://asana.com/templates/okr-objectives-key-results, https://www.atlassian.com/team-playbook/plays/okrs

### B15. Assumption log

- When: exposing the unverified assumptions behind a plan and how to test each.
- Columns: `Assumption | Confidence (H/M/L) | How to test | Impact if wrong`
- In chat: fits (4 columns); well suited to an agent laying out its own assumptions before acting.

| Assumption | Confidence | How to test | Impact if wrong |
|---|---|---|---|
| Users want dark mode | Medium | Survey top 100 users | Wasted sprint |
| API can handle 10x load | Low | Load test | Outage risk |
| Partner will renew | High | Contract review | Revenue gap |

Sources: https://www.projectmanagementdocs.com/template/project-documents/assumption-log/, https://thoughtbot.com/blog/product-management-templates-assumptions-tracker

### B16. Trade-off consequence table

Pointer: `references/plain-language.md` situation "Decision consequences"; the business form is `Option | What we gain | What we give up | Best if`, qualitative consequences rather than a scoring matrix. [unverified as a single canonical named framework]: a commonly taught pattern, so "consequence table" is a descriptive name, not a branded template. https://www.clearmissionconsulting.com/lens-on-leadership/beyond-pros-cons-better-way-to-choose, https://blog.thumbtack.com/framing-tradeoffs-how-to-use-decision-matrices-to-make-the-hard-calls-e851421b8af9

### B17. Go/No-Go decision checklist

Pointer: `references/plain-language.md` situation "Acceptance checklist"; a go/no-go gate signs off explicit criteria with `Criterion | Met? (Yes/No/Partial) | Note`, useful before an irreversible action. https://gonogo.team/go-no-go-decision/template, https://guides.visual-paradigm.com/making-informed-decisions-with-a-go-no-go-checklist-for-agile-projects-a-scoring-approach/

### B18. Pricing or packaging tiers

- When: presenting product tiers (Good/Better/Best) for a pricing or packaging decision. For feature availability only, use a feature table (S29 in `references/tables-software.md`).
- Columns: `Feature | Tier 1 | Tier 2 | Tier 3`
- In chat: fits with up to 3 tiers and 4 to 5 feature rows; more tiers or features belong in a document, since pricing pages usually need more rows than a chat table can carry.

| Feature | Basic | Pro | Enterprise |
|---|---|---|---|
| Users | 1 | 10 | Unlimited |
| Support | Email | Priority | Dedicated |
| Price | $9/mo | $29/mo | Custom |

Sources: https://en.wikipedia.org/wiki/Good%E2%80%93better%E2%80%93best, https://bogos.io/tiered-pricing/

### B19. WSJF (weighted shortest job first)

- When: sequencing work in SAFe by cost of delay divided by job size.
- Columns: `Job | User-business value | Time criticality | Risk reduction | Job size | WSJF`
- In chat: does not fit (6 columns); in chat use `Job | Cost of delay | Job size | WSJF`.

| Job | Cost of delay | Job size | WSJF |
|---|---|---|---|
| Fix billing bug | 20 | 2 | 10 |
| New report | 12 | 6 | 2 |

Source: https://framework.scaledagile.com/wsjf

### B20. Decisional balance sheet

- When: weighing the gains and losses of one choice; this is the proper name for a "pros and cons table", traced to Benjamin Franklin's 1772 "moral algebra".
- Columns: `Consideration | Gains | Losses`
- In chat: fits (3 columns). When the user chooses between several options, use the general Decision consequences table instead.

| Consideration | Gains | Losses |
|---|---|---|
| For me | More focus time | Less visibility |
| For the team | Fewer meetings | Slower hand-offs |

Source: https://en.wikipedia.org/wiki/Decisional_balance_sheet

### B21. Kano evaluation table

- When: classifying a feature from survey answers; the answer to the functional (positive) question × the answer to the dysfunctional (negative) question gives the category.
- Columns: functional answer as rows, dysfunctional answer as columns, category in each cell.
- In chat: the full 5 × 5 grid does not fit; in chat report results as `Feature | Category | Share of answers`.

| Feature | Category | Share of answers |
|---|---|---|
| Offline mode | Attractive | 48% |
| Password reset | Must-be | 71% |

Source: https://en.wikipedia.org/wiki/Kano_model

### B22. Now-Next-Later roadmap

- When: presenting a product roadmap without committing to dates; the three columns rank confidence, not time. The only roadmap table pattern with a traceable origin (its inventor's own account, a vendor source); prefer this name to a generic "roadmap table".
- Columns: `Now | Next | Later`
- In chat: fits (3 columns, one item per cell); for many items, use one row per item with `Item | Horizon`.

| Now | Next | Later |
|---|---|---|
| SSO login | Audit log | Custom roles |
| CSV export | Scheduled reports | Public API |

Source: https://www.prodpad.com/blog/invented-now-next-later-roadmap/

### B23. 2×2 quadrants as tables

- When: placing items on two axes. A 2×2 whose axes are categorical (Eisenhower: important or not × urgent or not; SWOT: internal or external × helpful or harmful) can be a table. A 2×2 whose axes are continuous (BCG growth-share: market share × growth rate) cannot: the meaning is in each item's position, so a table misleads; use a quadrant chart.
- Columns: `Item | Axis 1 | Axis 2 | Quadrant`
- In chat: fits (4 columns). In Markdown, templates that put a list in each quadrant use four headings, because a table cell cannot hold a list.

| Item | Important | Urgent | Quadrant |
|---|---|---|---|
| Production outage | Yes | Yes | Do now |
| Refactor tests | Yes | No | Schedule |
| Meeting invite | No | Yes | Delegate |

Source: https://www.nngroup.com/articles/prioritization-matrices/ ([unverified] the research recorded no dedicated URL for the categorical versus continuous distinction)
