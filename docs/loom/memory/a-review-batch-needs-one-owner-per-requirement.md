---
name: a-review-batch-needs-one-owner-per-requirement
description: Historical (2026-08-31; Review Batches since retired) — a Review Batch was refused at `packet` time when two members cite the same `Brief item covered` value ("ownership proof contains duplicate requirement authority") — one requirement, one owner — and same-module dependency chains, exactly the tasks the module rule batches, usually share one brief item; cite the item's clauses verbatim per task (plan-format referent kind (a)) so each member owns a distinct requirement, and expect `ready` and `check_review_batches.py` to say yes before `packet` says no
type: gotcha
sources:
  - resource: batch-review-measurement-and-nudge arc (2026-08-31) — batch `proposer` (Tasks 7/8/9, all `BI-3`) passed `ready` and the schema oracle, then `batch_review_cli.py packet` refused; resolved by quoting BI-3's `--check` clause on Task 8 and its gate/plan-format clause on Task 9
---

The ownership proof in `review_batch.py` requires every owned requirement
in a batch to have exactly one owner. That invariant was written for
per-task packets and is right there; a brief item that names one script,
its `--check` mode and the prose that wires them is one item across three
tasks, and the module rule clusters exactly those. The refusal surfaces
late — after `ready` and `check_review_batches.py` both accepted the plan —
and its message names the proof, not the field.

**Why:** the batch mechanism attributes every finding to the task that
owns the requirement it violates; two owners of one requirement make that
attribution ambiguous, so the packet refuses rather than guess.

**How to apply:** when a proposed batch's members share a `Brief item
covered` value, give each member a verbatim clause of that item (kind (a)
in plan-format §Brief item covered) before sealing — or leave the id on
the task that delivers the item's core and quote clauses on the rest. Do
it at plan time; the seal will not do it for you.

Note 2026-11-21: Review Batches, `review_batch.py`, `check_review_batches.py`,
`batch_review_cli.py`, plan-format and the `Brief item covered` field were
removed, so the procedure above is historical; no successor batches review
per task. Closing review now reads the whole branch once
(`loom-code/skills/closing-review/`). The surviving lesson: when a mechanism
attributes each finding to one owner, give every requirement exactly one owner
at plan time. No current Loom check enforces one owner; the lesson applies
wherever such an attribution mechanism exists.
