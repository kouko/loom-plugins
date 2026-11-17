---
name: document-ownership-does-not-require-a-runtime
description: A single owner for durable planning documents needs clear reading and update responsibilities, not a specialized store, schema or execution loop.
type: project
sources:
  - resource: docs/loom/2026-11-16-roadmap-simplification/spec.md
---

## Trigger

Several skills need the same durable project planning context.

## Correct path

Give one skill ownership of document selection and maintenance; other entry
points link to that owner and retain their own responsibilities. Use ordinary
documents with evidence links unless an observed requirement needs enforcement.

## Why

Concentrated ownership prevents competing summaries. A specialized runtime
adds separate formats, lifecycle rules and maintenance cost; ownership alone
does not justify those mechanisms or authorize execution of the plan.
