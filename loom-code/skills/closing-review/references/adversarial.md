# Adversarial — recipes by artifact type, and how to record what ran

The adversary's job is not to find bugs the reviewers might also find. It
is to make the change fail. It runs at the end of Build, and everything it
runs is committed as a program: Build re-runs those programs on every fix
loop, and `finalize-review` executes them on committed content.

## Reuse first, update with evidence

Before writing any probe, the adversary checks what already covers the
target: this change's programs under `docs/loom/<change-id>/evidence/probes/`
and the repository's related tests. It reuses a program that covers a case,
modifies one when a small change covers it, and writes a new probe only when
nothing covers the case. A permanent repository test that covers a case
counts as reuse, and the adversary leaves that test as it is. Its report marks
each probe `reused`, `modified` or `new`, with a one-line reason for every new
one. A stale case that is rewritten or flipped to its positive form counts as
`modified`.

When Build re-dispatches it for a widened scope or for trunk content brought
in by `sync-trunk`, the adversary updates only its own programs and fixes
nothing in the product. When a failing program caught a product defect, the
adversary keeps that program unchanged and returns a finding, and Build then
fixes the product. Every update carries mutation evidence run against the
committed probe program itself: at least one mutation per kind of change the
update touches, plus one that an over-broad update would wrongly accept. One
mutation restores the original behaviour the stale program rejected, and the
updated probe must turn RED on it. Each mutation turns the probe RED and is
reverted, and the report gives its command and observed result. The adversary
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

## Code

**If the repo declares mutation or fuzz tooling** — a `mutmut`,
`cosmic-ray`, `stryker` or fuzz target in its config — run it over the
changed modules and report survivors: a surviving mutant is a test that
asserts nothing.

**If it declares none** (the common case), write **at least three**
executable abuse or boundary cases against the changed behaviour, run them,
and record each one. Three is the floor, not the target. Reused and modified
cases count toward the floor. Reuse toward the floor counts only (a) the
programs the adversary committed for this change and (b) tests that exist
unchanged outside this change's branch. Any other test added or changed on the
branch, such as an implementer's pin, is named as related coverage only. Draw
them from:

| Class | The question |
|---|---|
| Empty and absent | zero items, empty string, missing file, unset variable — does it behave, or explode? |
| Boundary | one less, one more, exactly at the limit, the limit plus one |
| Hostile input | wrong type, enormous value, path traversal, injection payload, mixed encodings and non-ASCII |
| Wrong order | the second step called first; the operation run twice; two callers at once |
| Failure of a dependency | the network call fails, the disk is full, the subprocess exits non-zero — is the failure loud, or swallowed? |

Prefer cases that live as real tests afterwards. A case that only ran in
the adversary's head is not evidence.

## Spec

Red-team it: for each `REQ-<n>`, name a behaviour the requirement permits
that the author clearly did not want. Then look for the states the spec
never mentions — the second user, the interrupted run, the empty account,
the migration from what exists today. Each one is a finding with the
requirement as its anchor.

## Skill and gate

Make each attempt below against the file, and write down what the file made
you do:

- Read the instruction as an agent under time pressure — is there a reading
  that skips the expensive step and still looks compliant?
- Attempt the prose temptations verbatim ("the diff is one line, proceed?")
  and record whether the text refuses them.
- For a gate script, feed it the input it was written to catch, then the
  same input one character different.

An attempt that the file survives is recorded too — that is what makes the
attempts an eval rather than an anecdote.

## Recording

Build's hand-off names every committed program, and Build re-runs each one on
every fix loop. Closing review supplies them to `finalize-review`, which
executes each one and records the command, artifact, functional-content digest
and observed result in the generated attestation:

```json
{"command": "python3 -m pytest tests/test_abuse_empty_input.py -q",
 "artifact": "docs/loom/<change-id>/evidence/probes/abuse_empty_input.py"}
```

- `command` must be re-runnable by someone else in a clean tree.
- `artifact` is where the case now lives. Put probes under
  `docs/loom/<change-id>/evidence/probes/` — that path is the `evidence`
  artifact type. Promote a
  probe into the repo's real test suite only through a plan task.
- Anything the adversary found that matters
  becomes a `finding` with an anchor and a fix. Build fixes every fatal or
  important finding before hand-off and lists any left unresolved in its
  hand-off, and closing review passes those into the `findings` input of `finalize-review`.
