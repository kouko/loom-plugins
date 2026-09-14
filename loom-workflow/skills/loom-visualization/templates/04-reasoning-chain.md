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

No generator covers labelled edges. Hand-author the chain, then verify it with
`python3 scripts/align.py -`.

```
┌───────────────────────────┐
│ p95 latency doubled       │
└─────────────┬─────────────┘
              │ because
              ▼
┌───────────────────────────┐
│ N+1 queries on /orders    │
└─────────────┬─────────────┘
              │ because
              ▼
┌───────────────────────────┐
│ ORM lazy-loads line items │
└─────────────┬─────────────┘
              │ so
              ▼
┌───────────────────────────┐
│ eager-load in one query   │
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
        A["p95 latency doubled"] -->|"traced to"| B["N+1 queries on /orders"]
    end
    subgraph r2["Cause and fix"]
        direction LR
        C["ORM lazy-loads line items"] ==>|"so we"| D["Eager-load in one query"]
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
