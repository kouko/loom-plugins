# Adversarial — recipes by artifact type, and how to record what ran

The adversary's job is not to find bugs the reviewers might also find. It
is to make the change fail. It runs at the end of Build, and everything it
runs is committed as a program: Build re-runs those programs on every fix
loop, and `finalize-review` executes them on committed content. If a case
needs the code changed to fail, it is not a case.

## Which recipe to read

Every changed path has an artifact type, from the `artifact_types` list in
`contract/manifest.yaml`. Read this protocol, then the recipe file this table
names for every artifact type among the changed paths: that protocol and those
recipes are the whole procedure, and there is nothing else to find. A type
whose row says `none` has no recipe today — attack it with this protocol
alone, and say in the report that it has none.

| Artifact type | Recipe file |
|---|---|
| `code` | [`adversarial-code.md`](adversarial-code.md) |
| `spec` | [`adversarial-spec.md`](adversarial-spec.md) |
| `skill` | [`adversarial-skill-gate.md`](adversarial-skill-gate.md) |
| `gate` | [`adversarial-skill-gate.md`](adversarial-skill-gate.md) |
| `intent` | none |
| `plan` | none |
| `standing` | none |
| `evidence` | none |
| `map` | none |
| `memory` | none |
| `docs` | none |

Giving a type a recipe is one new file beside this one plus its own row here;
no existing recipe file is edited. Taking one away deletes its file, deletes
the test module named after that kind where it has one, and puts its row back
to `none`.

## Two parts: attack, then pin

The adversarial step runs in two parts. The first part reads the change and
attacks it, and it writes nothing but its report: it names every attack point
it found and what each one did. Only an attack that succeeded opens the second
part, where a program is written to pin what that attack exposed. A change the
first part leaves standing ends there, with its report alone.

A probe program is committed only when it is red against the change as it
stands, because a program that is green the moment it is written restates a
behaviour instead of demonstrating a defect. An attack the change survives is
reported as an attempt, and the second part writes nothing for it.

The report states three numbers: how many attack points the first part found,
how many of them earned a program, and how many programs were committed.

## How many cases

This section is the one place that says how many cases a change may commit. A
recipe, a station, an agent contract or a README may point here; none of them
states a number of its own.

The count is a ceiling and there is no minimum. A change commits **at most
five** probe programs, whatever its artifact types are, and that ceiling has
no written-reason escape: a user who wants more programs, or wants this step
skipped, says so in plain words. The checker rule
`adversarial.proportionate` recomputes the ceiling from the committed tree.

Nothing here asks for a number of cases to be reached. Each program earns its
place by the `concern:` line it carries, which says what kind of defect it
defends against; a program that cannot name one is a program not worth
committing, and an attack that found nothing worth a program is reported as
an attempt rather than padded into one. Reusing a program this change already
committed, or a repository test that already covers a case, commits no new
program and so spends nothing against the ceiling.

## Reuse first, update with evidence

Before writing any probe, the adversary checks what already covers the
target: this change's programs under `docs/loom/<change-id>/evidence/probes/`
and the repository's related tests. It reuses a program that covers a case,
modifies one when a small change covers it, and writes a new probe only when
nothing covers the case. A permanent repository test that already covers a
case counts as reuse: the adversary names it in `reason` and leaves the test as
it is. Its report marks
each probe `reused`, `modified` or `new`, with a one-line reason for every new
one. A stale case that is rewritten or flipped to its positive form counts as
`modified`.

When Build re-dispatches it for a widened scope or for trunk content brought
in by `sync-trunk`, the adversary updates only its own programs and fixes
nothing in the product. When a failing program caught a product defect, the
adversary keeps that program unchanged and returns a finding, and Build then
fixes the product. Every update to a program that was carried into the suite
that runs on every later change carries mutation evidence run against the
committed probe program itself: at least one mutation per kind of change the
update touches, plus one that an over-broad update would wrongly accept, such
as a generic-word substitution that a global replace with a case-insensitive
comparison lets through. A copy of the probe's logic proves nothing about that
program. One mutation restores the original behaviour the stale program
rejected, and the updated probe must turn RED on it. Each mutation must turn
the probe RED and is then reverted, and the report gives each one's command and
observed result. The adversary
commits the updated probe before it makes a copy, because `git worktree add` and
`git archive` hold only committed content, and an uncommitted update takes the
edit-tool route in the working tree. The adversary
applies each mutation in a throwaway copy of the working tree, such as a
temporary `git worktree add` or a `git archive` extract, and runs the committed
probe program there unchanged, or applies and undoes the mutation with the
host's edit tool. Running the unchanged probe inside a copy of the tree still
exercises its own assertion, unlike a copy of its logic. The adversary undoes
each mutation in a worktree copy with the host's edit tool before
`git worktree remove` removes that copy, and prefers a `git archive` extract
when the copy will be left behind in a temp directory. Discard commands
(`git checkout --`, `git restore`, `git reset --hard`, `git clean`,
`git worktree remove --force`) are never used to undo a mutation, because host
guards refuse them and they can destroy uncommitted work. An update never deletes, skips or xfails
a case to make it pass.

## Recording

Build's hand-off names every committed program, and Build re-runs each one on
every fix loop. Closing review supplies them to `finalize-review`, which
executes each one and records the command, artifact, functional-content digest
and observed result in the generated attestation:

```json
{"command": "python3 -m pytest tests/test_abuse_empty_input.py -q",
 "artifact": "docs/loom/<change-id>/evidence/probes/abuse_empty_input.py"}
```

- Record every attempt that failed to break anything, for every artifact
  type — that is what makes the attempts an eval rather than an anecdote.
- `command` must be re-runnable by someone else in a clean tree.
- Every probe program carries a `concern:` line among its first lines, naming
  in free text the kind of defect it defends against. The checker rule
  `adversarial.proportionate` refuses a program without one.
- `artifact` is where the case now lives. Put probes under
  `docs/loom/<change-id>/evidence/probes/` — that path is the `evidence`
  artifact type. Promote a
  probe into the repo's real test suite only through a plan task.
- Anything the adversary found that matters
  becomes a `finding` with an anchor and a fix. Build fixes every fatal or
  important finding before hand-off and lists any left unresolved in its
  hand-off, and closing review passes those into the `findings` input of `finalize-review`.
