target: coding-harness

# Reasoning chain

## When to use

A conclusion reached through a chain of causes or inferences: a root-cause
analysis, why a design was chosen. Each edge says why the next state follows.
For a standalone page explaining documented reasoning, use page mode instead.

## Table

| Step | Claim | Why the next step follows |
|---|---|---|
| 1 | p95 latency doubled | the profiler traced it to one endpoint |
| 2 | N+1 queries on /orders | each order row loads its items separately |
| 3 | ORM lazy-loads line items | the fix must remove the per-row load |
| 4 | Eager-load in one query | conclusion |

## ASCII

A reply defaults to the table above; draw this when the shape itself is the
information, or when the destination does not render markdown.

No generator covers labelled edges. Hand-author the chain, then verify it with
`python3 <skill-dir>/scripts/align.py -` (`<skill-dir>` is defined in
`SKILL.md`).

```
┌───────────────────────────┐
│ p95 latency doubled       │
├───────────────────────────┤
│ * 2x increase observed    │
│ * isolated to /orders     │
└─────────────┬─────────────┘
              │ because
              ▼
┌───────────────────────────┐
│ N+1 queries on /orders    │
├───────────────────────────┤
│ * 50+ queries per request │
│ * line items loaded 1-by-1│
└─────────────┬─────────────┘
              │ because
              ▼
┌───────────────────────────┐
│ ORM lazy-loads line items │
├───────────────────────────┤
│ * default relationship    │
│ * missing eager fetch     │
└─────────────┬─────────────┘
              │ so
              ▼
┌───────────────────────────┐
│ eager-load in one query   │
├───────────────────────────┤
│ * use joinedload          │
│ * single round-trip       │
└───────────────────────────┘
```

## Mermaid

Follows the row convention of `references/mermaid-cot-spec.md`: rows are
subgraphs with their own `direction LR`, rows join subgraph to subgraph,
every edge is labelled, and `==>` marks the step into the conclusion.

```mermaid
flowchart TD
    subgraph r1["Symptom"]
        direction LR
        A[<div style='text-align:left'>p95 latency doubled<br/>━━━━━━━━━━━━━━━━━━<br/>• 2x increase observed<br/>• isolated to /orders</div>] -->|"traced to"| B[<div style='text-align:left'>N+1 queries on /orders<br/>━━━━━━━━━━━━━━━━━━━━━━<br/>• 50+ queries per request<br/>• line items loaded 1-by-1</div>]
    end
    subgraph r2["Cause and fix"]
        direction LR
        C[<div style='text-align:left'>ORM lazy-loads line items<br/>━━━━━━━━━━━━━━━━━━━━━━━━━<br/>• default relationship<br/>• missing eager fetch</div>] ==>|"so we"| D[<div style='text-align:left'>Eager-load in one query<br/>━━━━━━━━━━━━━━━━━━━━━━━<br/>• use joinedload<br/>• single round-trip</div>]
    end
    r1 -->|"profiler shows"| r2
    style A fill:#f8f9fa,stroke:#868e96,stroke-width:2px
    style B fill:#fff4e6,stroke:#e67700,stroke-width:2px
    style C fill:#ffe3e3,stroke:#c92a2a,stroke-width:2px
    style D fill:#c5f6fa,stroke:#0c8599,stroke-width:2px
```

## Common mistakes

- Empty edge labels such as "then" or "so" with no reason.
- A node edge that crosses rows; Mermaid then drops the row layout.
- Treating a topic heading as a node; a node carries a claim.
- Leaving out the step that was overturned; a reversal belongs in the chain.
