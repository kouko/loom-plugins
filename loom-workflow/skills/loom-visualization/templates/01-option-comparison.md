target: coding-harness

# Option comparison

## When to use

Two or more options judged on the same criteria: libraries, designs,
approaches, fixes. The reader has to pick, so every option gets the same
columns and the recommendation is stated after the table, not buried in a cell.

## Table

The default form. One row per option, one column per criterion, short cells.

| 方案 | 延遲 | 維護成本 | 適合 |
|---|---|---|---|
| Redis 快取 | 低 | 中 | 讀多寫少 |
| CDN | 最低 | 低 | 靜態資源 |
| DB index | 中 | 低 | 查詢慢 |

## ASCII

A GFM markdown table is the form in every client. Use this ASCII table only
when the answer goes into a code block or a plain-text destination that does
not render markdown. Run `python3 <skill-dir>/scripts/generate.py table`
(`<skill-dir>` is defined in `SKILL.md`) with this input on stdin:

```json
{"headers": ["方案", "延遲", "維護成本", "適合"], "rows": [
  ["Redis 快取", "低", "中", "讀多寫少"],
  ["CDN", "最低", "低", "靜態資源"],
  ["DB index", "中", "低", "查詢慢"]
]}
```

Output:

```
┌────────────┬──────┬──────────┬──────────┐
│ 方案       │ 延遲 │ 維護成本 │ 適合     │
├────────────┼──────┼──────────┼──────────┤
│ Redis 快取 │ 低   │ 中       │ 讀多寫少 │
│ CDN        │ 最低 │ 低       │ 靜態資源 │
│ DB index   │ 中   │ 低       │ 查詢慢   │
└────────────┴──────┴──────────┴──────────┘
```

## Mermaid

Only where the client check allows Mermaid, and only when two numeric axes
really separate the options; otherwise keep the table.

```mermaid
quadrantChart
    title Caching options: effort vs impact
    x-axis Low effort --> High effort
    y-axis Low impact --> High impact
    quadrant-1 Plan carefully
    quadrant-2 Do first
    quadrant-3 Skip
    quadrant-4 Avoid
    Redis cache: [0.6, 0.8]
    CDN: [0.3, 0.7]
    DB index: [0.2, 0.5]
```

## Common mistakes

- Different criteria per option, so the rows cannot be compared.
- Long sentences in cells; move the reasoning below the table.
- A quadrant chart with invented coordinates when the criteria are not numeric.
- Emoji or check-mark symbols as cell values in the ASCII form; they break alignment.
