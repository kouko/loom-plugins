---
name: an-adversarial-probe-can-go-green-by-excluding-what-would-refute-it
description: A probe that computes its own population (which instances to test) or deselects cases inside its own nested run can choose exactly the member or exclusion that never exercises the defect it exists to catch, producing a pass that proves nothing about the claim; this blind spot is not visible by reading the probe's code or the diff — only by executing the real recipe independently, with a population or instance the probe's own author did not pick (a blind run), does the gap turn red
type: gotcha
sources:
  - resource: 9bf87029 / PR #33 / 2026-09-18-modular-adversary-recipes — corroborated by `docs/loom/2026-09-18-modular-adversary-recipes/evidence/probes/test_modular_recipes_abuse.py`'s own module and `_manifest_types` docstrings, which describe both original defects while explaining their fix, and by a confirming blind-run account
---

`2026-09-18-modular-adversary-recipes` split the adversary's attack
recipes into one file per artifact kind beside a shared protocol. The
adversarial probe written to prove the split held its claimed
properties went through an earlier draft that reported green while it
could not have seen the defects it was written to catch, because the
probe itself chose what its own run would exclude or cover:

- Its nested run went through the repository's own test runner, which
  deselects the cases that copy the repository — and those were
  exactly the cases that required a second file (the routing-table
  row) to exist. With them deselected, the probe could not see the
  defect a missing routing row would cause.
- Its population for "add a kind" was computed as the
  alphabetically-first unrouted artifact type, which happened to be
  the one candidate whose name collided with nothing in the shared
  protocol's prose — the only member that could not trigger the
  name-collision defect that was actually present for other kinds.

Both weaknesses were fixed before the branch merged. But neither was
found by reading the probe's code or the diff — they surfaced only
when a blind-run reader performed the "add a kind" step for real per
the documentation, and separately when the reader redid it choosing a
different, independently-picked kind, which then turned checks red
that the probe's own self-chosen run had left green.

**Why:** a probe that decides its own population, or its own
exclusions, inside the very run meant to prove a claim has no
adversary in the loop for that decision — it can pick, without anyone
intending it, the one member or exclusion that never exercises the
property under test. Reading the probe's source does not surface
this: each assertion does exactly what it says, and the defect is not
in any single assertion but in which case that assertion is ever run
against. A pass produced this way is indistinguishable, on the page,
from a pass produced by a probe that actually covers the claim.

**How to apply:** before trusting a green adversarial probe, ask two
questions that re-reading its code cannot answer: (1) who chose the
population the probe is parametrized over, and could that choice be
narrow enough to dodge the defect it claims to prove absent? (2) does
the probe's own execution deselect, skip, or exclude any case, and
could a real defect live exactly inside what got excluded? Answer
both by executing the real recipe independently — a blind run using a
population or instance the probe's own author did not pick — and
checking whether that run turns red anything the probe's self-chosen
run left green. When a probe must parametrize over a population, draw
it from the same source of truth the feature itself reads (e.g. every
unrouted type a manifest lists), never from a value the probe's own
author selects by hand, and run nested checks with nothing deselected.

Related: [[reading-code-and-running-code-fail-differently]] — the
same "execution finds it, reading does not" split, for a different
mechanism (a stranger typing an untried path, not a probe excluding
its own refuting case). [[a-subset-check-needs-a-refusal-test-because-an-empty-listing-passes-vacuously]]
— also a probe passing vacuously, but there the vacuity comes from a
producer silently returning an empty listing, not from the probe
choosing a narrow non-empty population.
