# Recap Alignment Schema — Reference Bundle

> **SSOT for `loom-workflow:recap-state` v0.1**
> This file owns the L3 orientation contract and retains the historical
> seven-block lineage for the possible L2 HANDOFF sister skill.
> Source research: `AI Agent Recap 框架研究` (2026-05-25),
> `對話接續綜論` (2026-05-25), and `2026-05-26-recap-v0.1-brief.md`.

The renderer keeps planning private. Never output `<thinking>` or `<recap>`
tags, their closing forms, or numbered `Block N` labels.

## L3 user-visible template

Use an orientation-first, variable-length recap in the conversation language.
For a long conversation, lead with the conversation-grounded original purpose
when available and the current position. Show a proposed next step only when
the purpose is grounded. Explain how key decisions and completed work led here,
then name the remaining gap. Mark assumptions and unknown facts as such; never
infer a purpose or completed work from silence.
Before reporting a historical decision, identify the user turn or prior action
that establishes it. A formatting choice made for this recap is not a
historical decision; omit unsupported decision claims.
If the original purpose is unknown, ask only for the purpose. Do not invent a
proposed work step when the purpose is unknown. When the original purpose is
grounded, ask about the proposed next step. If asking for purpose, wait for the
user to state or clarify it. In a short session, omit sections with no useful
content; never pad a history or invent a pending question to fill a template.

Use clear section headings for content that warrants sections. Frame each
heading in an ASCII box with `■ ` before the heading text. Use
`loom-visualization` to generate or verify CJK alignment rather than eyeballing
cell widths. Put one fullwidth-space-only line between sections, and inspect
the rendered chat spacing; do not use visible HTML break tags. Keep the first
section focused on purpose and position, and the final section focused on a
directed question about purpose when unknown, or the grounded next step.
Stop until the user responds.

Use bullets for a short path through decisions and work. Put a short
situation sentence before each table. A table earns its place by comparing
information or compressing meaningful metadata. Draw a relationship diagram
when it clarifies a real dependency, branch, merge, rationale, evidence, or
sequence relationship; a flat status list needs no diagram. Route the form and
any ASCII alignment through
`loom-visualization`; follow its client-specific renderer guidance. Preserve
the user's exact wording when a phrase changes subsequent behavior, including
paths, errors, constraints, tools, and commands. Keep confirmed facts,
assumptions, and unknowns distinct. Answer in the current chat only; do not
write a recap file or replace HANDOFF or the built-in `/recap`.

## 1 — The Seven Blocks (historical lineage)

The V1 model used seven blocks. The map records why each mattered and how a
future L2 HANDOFF might use it. It is not the L3 display format.

| # | Block | Original purpose | L3 treatment | Future L2 |
|---|---|---|---|---|
| 1 | Situation | Open at the present moment | Lead with purpose and position | Render |
| 2 | Background | Preserve the reasoning trail | Include key decisions when relevant | Render |
| 3 | Assessment | Expose assumption, confidence, and unknowns | Distinguish facts from assumptions | Render |
| 4 | User messages | Preserve all user intent for a cold reader | Skip the full message dump | Render verbatim |
| 5 | Why-this-question | Explain a pending agent question | Include its stakes only when one exists | Skip |
| 6 | Pending | Show remaining work | Name the gap and useful next work | Render |
| 7 | Synthesis-check | Catch a direction mismatch | Ask a directed final question and wait | Render with L2-specific strength |

The original Block 2 guidance used 3–5 bullets and the original L3 renderer
used six natural sections. Those limits are history, not current requirements.
The full message dump was dropped at L3 because an in-session reader already
has their turns; consequential phrases still require exact quotation. L2 has
a different reader and may need every turn. HANDOFF-specific additions belong
to HANDOFF, not this recap.

## 2 — Visual aids

Use a table to compare alternatives or compress meaningful metadata, and put
a short situation sentence before it. A single row or unrelated items rarely
earn a table. Use a relationship diagram for meaningful rationale, evidence,
sequence, dependency, branch, or merge relationships when spatial layout helps.
Follow `loom-visualization` for client rendering choice, ASCII frames, and
alignment verification. An ordinary status snapshot works as prose or bullets.
An explicit user format request wins where the client can render it.

## 3 — The Five Shared Core Principles

### structured-schema

Lead with grounded purpose when available and current position, adapt the
middle to the conversation, and end with the conditional question above.
Predictable endpoints help orientation; mandatory empty sections hide useful
work behind filler.

### quote-not-paraphrase

Reproduce behavior-changing user wording exactly, including paths, error
messages, named constraints, and tool or command names. For example,
"kill `config/base.py` and split into `config/db.py` + `config/app.py`"
cannot be reduced to "restructure the config file" without losing the action.

### all-user-messages

This is an L2-only principle for a cold reader. At L3, do not dump all user
turns. If a user asks for message history, provide that listing separately.

### synthesis-check

Finish with one directed question: ask for the original purpose if it is
unknown; otherwise ask about the grounded next step. Wait for the user's
answer. When asking about a next step, a clear confirmation opens this soft
pause; a correction replaces the proposed direction. When purpose is unknown,
wait for the user to state or clarify it. Do not resume a tool call, edit, or
analysis on your own.

### plain-language

Explain the situation to the user in the conversation language, as a person
speaking to them. Define an unfamiliar term when first used. Prefer "We chose
Y because X would have delayed the migration" to shorthand such as
"Decision: Y; rationale: migration constraint." Keep sentences short and
separate facts, assumptions, and unknowns.

## 4 — Good Example

This fictional long-session recap shows how the user gets back to the original
purpose and the path to the next decision. The CJK heading frames were checked
with `loom-visualization`'s alignment tool.

```text
┌──────────────────────────┐
│ ■ 目的與目前位置         │
└──────────────────────────┘
```

你最初要「每週一早上看得到上週的淨銷售額」。目前資料已匯入，報表仍缺
退款的計算方式；下一步是先確認退款應歸到哪一週，才能完成淨銷售欄位。

　

```text
┌──────────────────────────┐
│ ■ 關鍵決定與進度         │
└──────────────────────────┘
```

- 我們決定先用訂單付款日期統計銷售，因為這和現有匯入資料一致。
- 已完成訂單與退款資料的匯入，也核對了上週的訂單總額。
- 原先想只列訂單總額，但那會忽略退款；因此改為要計算淨銷售額。

這些已做的選擇有取捨關係，用決策脈絡圖可看出為何放棄舊方案。

```text
┌──────────────────────────┐
│ 目的: 每週看淨銷售額     │
└────────────┬─────────────┘
             │ 評估
             ▼
┌──────────────────────────┐
│ 舊方案: 只列訂單總額     │
└────────────┬─────────────┘
             │ 漏掉退款，故捨棄
             ▼
┌──────────────────────────┐
│ 決定: 計入退款           │
└──────────────────────────┘
```

　

```text
┌──────────────────────────┐
│ ■ 已知與待辦             │
└──────────────────────────┘
```

目前可確認的進度與仍需釐清的地方如下。

| 項目 | 狀況 |
|---|---|
| 已確認 | 匯入完成；訂單總額已核對。 |
| 未知 | 退款應歸在原付款週，還是實際退款週。 |
| 待辦 | 確認規則後計算淨銷售額，再檢查報表。 |

　

```text
┌──────────────────────────┐
│ ■ 下一步                 │
└──────────────────────────┘
```

我的理解是先確認退款歸屬週，再完成淨銷售欄位。這符合你的方向嗎？

## 5 — Bad Example

"Current state: implementation pending. Confidence: high. Next: proceed."
This hides the user's purpose, treats a guess as a fact, and continues without
a directed question. Six padded headings or a decorative graph would make the
same short exchange harder to scan.

The historical implementation example mentioned
`loom-workflow/skills/recap-state/scripts/`; it is retained here only as a
lineage pointer, not as a current test-location instruction.

## 6 — Other diagram examples

These are alternatives for different questions, not four diagrams in one recap.
Each uses the same fictional sales and refunds situation. Draw one only when
the relationship adds understanding; flat progress is clearer in prose or a
table. The maps summarize stated facts and decisions, without claiming access
to hidden deliberation.

### Argument map

An argument map（論證圖）shows what supports a claim. Suppose the fictional
imported data contains a cross-week refund. That confirmed example and the
still unknown attribution rule support asking the user to settle the rule
before finalizing net sales; neither branch is a decision already made.

```text
已確認: 有跨週退款 ──支持────┐
                             ├──► 主張: 先確認退款歸屬週
未知: 退款歸屬規則 ──待解────┘
```

### Decision tree

A decision tree（決策樹）shows future branches, not the chosen policy. Each
answer leads to a distinct calculation action after the user decides.

```text
退款應歸哪一週？
│
├─ 原付款週 ─► 重算原付款週
└─ 實際退款週 ─► 計入實際退款週
```

### Flowchart

A flowchart（流程圖）shows an ordered procedure once the rule is confirmed.
These steps do not branch; the rule must be settled before calculation.

```text
┌──────────┐
│ 確認規則 │
└──────────┘
      │
      ▼
┌──────────┐
│ 計算淨額 │
└──────────┘
      │
      ▼
┌──────────┐
│ 核對報表 │
└──────────┘
```
