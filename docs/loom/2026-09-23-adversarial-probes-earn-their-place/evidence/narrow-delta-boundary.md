# The narrow-delta boundary, re-examined against 134 recorded changes

Acceptance 2 of
`docs/loom/intent/2026-09-23-adversarial-probes-earn-their-place.md`: the
boundary that decides which deltas skip the adversarial step now decides more
than it used to, so it is re-examined here against the recorded history and
either kept with the evidence stated or adjusted.

**Verdict: kept in place, and tightened three times while this change was
built.** No delta that was narrow before is narrow now — every tightening
only ever removes deltas from the exempt set — so the survey below still
bounds what the boundary exempts. What changed is written out in "How the
boundary moved" before the survey, because one of the three also changes the
reviewer floor, which is consumer-visible behaviour and is listed in the
CHANGELOG as such.

Across the 128 changes whose delta could be read back out of git, the
boundary would have exempted two, both documentation-only, both of which
committed no probe program at all and neither of which had a probe catch
anything. The step it now skips was already buying nothing on exactly those
deltas. One observation that argues for a *wider* boundary later is recorded
at the end; it is not made here, because the same predicate also sets the
reviewer floor and moving it moves the reviewer count, which this change's
intent puts out of scope.

## How the boundary moved

| Tightening | Was | Is | Also moves the reviewer floor |
|---|---|---|---|
| a delta that **deletes a test** | narrow, floor 1 | wide, floor **2** | yes — 1 → 2 |
| a delta carrying an **executed file**, wherever it sits | narrow when the file was under the change's own store | wide | no — floor was already decided by the allowlist |
| a **program with no suffix** (`#!` first line, or git mode 100755) | read as a document | read as a program, so wide | no — narrowness only |

The first is the one a consumer feels: a change whose whole delta is the
intent, its store and a deleted test used to need one reviewer and now needs
two. The reasoning is in `reviewer_floor_for_paths` — adding a test is low
risk, removing one deletes the evidence a later reviewer would read — and it
is stated here because the reviewer floor is a published number, not an
internal detail of the adversarial step.

## What the boundary is today

`is_narrow_delta` in `loom-code/scripts/loom_checker/reviewers.py` asks two
things, and a delta has to pass both.

**One — no executed file, wherever it sits.** If any committed path's suffix
is one `is_program_path` in `loom_checker/helpers.py` knows — `.py`, `.sh`,
`.js`, `.rb` and the rest — the delta is wide, whatever else the allowlist
below would say about it. A suffix list is a list of the names a program may
be given, so `helpers.tree_programs` asks the selected commit the two
questions the name cannot answer: git's recorded mode (100755) and a `#!`
first line. `evidence/probes/run` is a program by either. This is the test
that makes skipping the
adversarial step safe: the justification for skipping it is that the delta
carries no executed behaviour a probe program could make fail, and a test
file, a script, or a probe program committed under the change's own store
(which `finalize-review` runs as a subprocess) is executed behaviour.

**Two — the reviewer-floor allowlist.** *Every* committed path must be one of:

| Allowed | Example |
|---|---|
| this change's intent | `docs/loom/intent/<change-id>.md` |
| this change's own store | `docs/loom/<change-id>/…` |
| the repo-level evidence store | `docs/loom/evidence/…` |
| a test file, or any path with a `tests` component | `loom-code/scripts/test_x.py` |
| a `.md`, `.mdx`, `.rst` or `.txt` file **outside** `docs/loom/` | `README.md` |

and *no* path is protected, and *no* removed path is a test. Protected means
a path component named `agents`, `api`, `cli`, `commands`, `contract`,
`hooks`, `skills` or `templates`, or a file named `AGENTS.md`, `CLAUDE.md`,
`DESIGN.md`, `kickoff-defaults.md`, `PRINCIPLES.md` or `SKILL.md`. Anything
unrecognised — a `.json`, a `.yaml`, a binary — makes the delta wide. The
list is an allowlist: one unrecognised path is enough to lose narrowness.
Deleting a test is treated as wide even though adding one is not, because
what a deletion changes is what the repository can still catch.

The two questions are not the same predicate. Narrowness is strictly
stronger than reviewer floor 1: a delta that only adds a test file gets
floor 1 and is **not** narrow, so it skips no step. Every narrow delta still
gets floor 1.

A delta that cannot be computed at all — a single-branch CI clone with no
trunk to diff against — is a third answer, neither narrow nor wide.
`auto_skipped_steps` returns the whole auto-skip set there, so a checkout
that cannot read the delta does not refuse an attestation finalize wrote
where it could; `required_reviewer_count` still fails closed at two, which
costs an honest change nothing because the verdicts are in the attestation.
Sitting on the trunk is not that case: there the delta is computable and
empty, and every recomputed rule keeps failing closed on it.

## What it would have exempted

Source: the five survey CSVs behind this change (134 changes; columns
`change_kind`, `probe_files`, `test_functions`, `probe_lines`,
`did_a_probe_catch_a_real_defect`). Every number below was recomputed from
those files, and the path-level classification was recomputed by importing
`is_narrow_delta` itself — in the form described above, after the program and
deletion tests were added, which only ever narrows the answer — and running it
over each change's committed delta —
the commit that added `docs/loom/intent/<change-id>.md` on the repository's
first-parent `main` history, in local clones of all five repositories.

| Repository | Changes | Delta readable | Narrow |
|---|---:|---:|---:|
| monkey-skills | 64 | 64 | 0 |
| loom-plugins | 45 | 42 | 2 |
| dotfiles | 20 | 18 | 0 |
| redshift-comment-mcp | 4 | 3 | 0 |
| kumiko-zaiku-app-icons | 1 | 1 | 0 |
| **total** | **134** | **128** | **2** |

Six changes have no intent file added on their repository's first-parent
`main` history under that change id (three in loom-plugins, two in dotfiles,
one in redshift-comment-mcp) and could not be classified; none of the six is
documentation-only.

The two the boundary exempts:

| Change | Kind | Probe programs | Did a probe catch a defect |
|---|---|---:|---|
| `loom-plugins 2026-09-14-plugin-readme-rewrite` | docs-only | 0 | no (a pre-existing checker caught one) |
| `loom-plugins 2026-09-14-root-readme-overview` | docs-only | 0 | no |

So the mechanism that this change extends would, over the whole recorded
history, have skipped a step that in both cases produced no program and found
nothing. It would have skipped no change on which a probe ever caught a
defect.

## Is that acceptable given what probes catch

Recomputed from the same CSVs, by the first word of `change_kind`:

| Kind | Changes | Probe files | Test functions | A probe caught a defect |
|---|---:|---:|---:|---|
| code | 54 | 95 | 536 | 20 yes, 17 no, 12 unknown, 5 step skipped |
| mixed | 39 | 108 | 866 | 18 yes, 9 no, 1 partial, 11 unknown |
| skill-or-gate | 27 | 36 | 174 | 6 yes, 15 no, 1 partial, 5 unknown |
| docs-only | 13 | 14 | 67 | 2 qualified yes, 11 no |
| unknown | 1 | 2 | 1 | 1 yes |
| **total** | **134** | **255** | **1,644** | 47 yes, 52 no, 28 unknown, 5 skipped, 2 partial |

For code changes that is 20 of 54, **37.0 %**; 20 of 49 (**40.8 %**) leaving
out the five where the adversarial step was skipped; 20 of 37 (**54.1 %**)
leaving out the twelve whose outcome the record does not state. The intent's
"37 to 46 per cent" is the low end of that range; 37.0 % reproduces exactly,
46 % does not reproduce from these columns under any denominator tried, and
nothing here depends on which end is right.

Both documentation-only "yes" rows are qualified in the record itself:

- `2026-09-17-loom-readme-small-fixes` — "defect in implementer's test, not
  README"; `how_found` is `unknown`. Not a product defect.
- `2026-09-23-intent-records-match-current-behaviour` — `how_found` is
  "reading (per baseline); PR says adversarial test proved it — possibly
  program-red, not verifiable".

Neither is an executed program catching, on a documentation-only delta, a
product defect that reading did not. That is the claim the intent makes, and
it survives recomputation. Both changes are also **wide** by the predicate
above, so the boundary exempts neither of them either way.

## The observation the boundary leaves on the table

Eleven of the thirteen documentation-only changes are *not* narrow, and the
paths that make them wide are mostly documentation:

| Change | What makes it wide |
|---|---|
| `2026-09-16-clean-stale-references` | `docs/loom/README.md`, a `references/` file under a `skills/` tree |
| `2026-09-17-fix-artifact-types-pointer` | `docs/loom/README.md`, `loom-code/contract/manifest.yaml` |
| `2026-09-17-loom-readme-small-fixes` | `docs/loom/README.md` |
| `2026-09-20-adversarial-probe-self-referential-blind-spot` | `docs/loom/memory/…` |
| `2026-09-20-record-the-withdrawn-ordering-lesson` | another change's intent file, `docs/loom/memory/…` |
| `2026-09-23-intent-records-match-current-behaviour` | other changes' intent files |
| `2026-09-14-manifest-repo-urls` | five `plugin.json` files |

A `.md` file under `docs/loom/` is deliberately excluded from the low-risk
documentation rule unless it is this change's own store or the shared
evidence store, which makes the loom's own README, its memory store and any
other change's intent a wide delta. On the evidence above those deltas are
exactly the ones where an adversarial program has never caught anything.
Widening the allowlist to cover `docs/loom/memory/`, `docs/loom/README.md`
and other changes' intent files would make exactly four more of the 128
narrow — `2026-09-17-loom-readme-small-fixes`,
`2026-09-20-adversarial-probe-self-referential-blind-spot`,
`2026-09-20-record-the-withdrawn-ordering-lesson` and monkey-skills'
`2026-09-09-fog-history-skips-non-ascii-ticket-names`, all documentation-only.
On one of the four the adversarial step was already skipped by hand; on none
of them did a probe catch a product defect (the first is the
implementer's-test row above).

It is not done here. The predicate is deliberately one predicate: widening it
for the adversarial step also drops those changes from two reviewers to one,
and this change's intent puts the reviewer-count policy out of scope. A later
change that wants it should decide both effects together, with this table as
its starting evidence.

## Reproducing these numbers

The CSVs live outside the repository (the survey's scratch directory). The
path classification is reproduced by importing the predicate and running it
over each change's delta:

```python
import sys, subprocess
sys.path.insert(0, "loom-code/scripts")
from loom_checker.reviewers import is_narrow_delta

sha = subprocess.run(
    ["git", "-C", repo, "log", "--first-parent", "main", "--diff-filter=A",
     "--format=%H", "--", f"docs/loom/intent/{change_id}.md"],
    capture_output=True, text=True).stdout.split()[-1]
status = subprocess.run(
    ["git", "-C", repo, "show", "--name-status", "--format=", "--no-renames", sha],
    capture_output=True, text=True).stdout
paths, removed = set(), set()
for line in status.splitlines():
    code, _, name = line.partition("\t")
    if not name.strip():
        continue
    paths.add(name.strip())
    if code.strip().upper().startswith("D"):
        removed.add(name.strip())
is_narrow_delta(paths, change_id, removed)
```

Re-run after all three tightenings, both exempted changes are still narrow:
neither delta contains an executed file, a deletion, or a suffix-less
executable. The snippet passes no `executable` argument, which is the
name-only half of the predicate; `auto_skipped_steps` passes the other half in
from the commit, and adding it can only remove changes from the narrow set.
The other four repositories had no narrow change to lose, and the predicate
only ever got stricter, so the table above stands unchanged.
