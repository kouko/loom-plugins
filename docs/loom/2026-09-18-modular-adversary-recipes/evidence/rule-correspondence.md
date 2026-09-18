# Rule correspondence — where each adversary rule lives after the split

Acceptance 8 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`:
every rule present before the split is still present after it, and none was
added.

The pre-split document is
`loom-code/skills/closing-review/references/adversarial.md`, read
at commit `5b8dfdce727792a338f4c7778d1d0c1b55295b23`. Anyone can reproduce
the left-hand column with:

```
git show 5b8dfdce727792a338f4c7778d1d0c1b55295b23:loom-code/skills/closing-review/references/adversarial.md
```

and diff it against the four files named in the right-hand column. The
split moved whole `##` sections; no sentence was reworded, reordered,
dropped or written. `loom-code/scripts/test_adversary_layout.py` recomputes
this correspondence from that commit on every run, so the table below is a
reader's index, not the check itself.

Every destination path is relative to
`loom-code/skills/closing-review/references/`.

| # | Rule | Original heading | Now lives in |
|---|---|---|---|
| 1 | The adversary's job is to make the change fail, not to find bugs reviewers would also find | (preamble) | `adversarial.md` |
| 2 | It runs at the end of Build; everything it runs is committed as a program, re-run by Build on every fix loop and executed by `finalize-review` | (preamble) | `adversarial.md` |
| 3 | If a case needs the code changed to fail, it is not a case | (preamble) | `adversarial.md` |
| 4 | Before writing any probe, check this change's committed programs and the repository's related tests | `Reuse first, update with evidence` | `adversarial.md` |
| 5 | Reuse a covering program, modify one a small change covers, write a new probe only when nothing covers the case | `Reuse first, update with evidence` | `adversarial.md` |
| 6 | A permanent repository test that already covers a case counts as reuse; name it in `reason` and leave it as it is | `Reuse first, update with evidence` | `adversarial.md` |
| 7 | Mark each probe `reused`, `modified` or `new`, with a one-line reason for every new one | `Reuse first, update with evidence` | `adversarial.md` |
| 8 | A stale case rewritten or flipped to its positive form counts as `modified` | `Reuse first, update with evidence` | `adversarial.md` |
| 9 | On a re-dispatch the adversary updates only its own programs and fixes nothing in the product | `Reuse first, update with evidence` | `adversarial.md` |
| 10 | A failing program that caught a product defect is kept unchanged and returned as a finding; Build fixes the product | `Reuse first, update with evidence` | `adversarial.md` |
| 11 | Every update carries mutation evidence against the committed probe program itself, including one an over-broad update would wrongly accept | `Reuse first, update with evidence` | `adversarial.md` |
| 12 | A copy of the probe's logic proves nothing about that program | `Reuse first, update with evidence` | `adversarial.md` |
| 13 | One mutation restores the behaviour the stale program rejected, and the updated probe must turn RED on it | `Reuse first, update with evidence` | `adversarial.md` |
| 14 | Each mutation must turn the probe RED and is then reverted; the report gives each one's command and observed result | `Reuse first, update with evidence` | `adversarial.md` |
| 15 | Commit the updated probe before making a copy, because `git worktree add` and `git archive` hold only committed content | `Reuse first, update with evidence` | `adversarial.md` |
| 16 | Apply each mutation in a throwaway copy and run the committed probe there unchanged, or apply and undo it with the host's edit tool | `Reuse first, update with evidence` | `adversarial.md` |
| 17 | Running the unchanged probe inside a copy of the tree still exercises its own assertion | `Reuse first, update with evidence` | `adversarial.md` |
| 18 | Undo a mutation in a worktree copy with the host's edit tool before `git worktree remove`; prefer a `git archive` extract for a copy left behind | `Reuse first, update with evidence` | `adversarial.md` |
| 19 | Discard commands are never used to undo a mutation | `Reuse first, update with evidence` | `adversarial.md` |
| 20 | An update never deletes, skips or xfails a case to make it pass | `Reuse first, update with evidence` | `adversarial.md` |
| 21 | With declared mutation or fuzz tooling, run it over the changed modules and report survivors | `Code` | `adversarial-code.md` |
| 22 | With none declared, write at least three executable abuse or boundary cases, run them and record each one | `Code` | `adversarial-code.md` |
| 23 | Three is the floor, not the target; reused and modified cases count toward it | `Code` | `adversarial-code.md` |
| 24 | Reuse toward the floor counts only this change's committed programs and tests unchanged outside the branch | `Code` | `adversarial-code.md` |
| 25 | Any other test added or changed on the branch is named as related coverage only | `Code` | `adversarial-code.md` |
| 26 | The five classes to draw cases from: empty and absent, boundary, hostile input, wrong order, failure of a dependency | `Code` | `adversarial-code.md` |
| 27 | Prefer cases that live as real tests afterwards; a case that only ran in the adversary's head is not evidence | `Code` | `adversarial-code.md` |
| 28 | For each `REQ-<n>`, name a behaviour the requirement permits that the author clearly did not want | `Spec` | `adversarial-spec.md` |
| 29 | Look for the states the spec never mentions, and anchor each finding to its requirement | `Spec` | `adversarial-spec.md` |
| 30 | Make each attempt against the file and write down what the file made you do | `Skill and gate` | `adversarial-skill-gate.md` |
| 31 | Read the instruction as an agent under time pressure, hunting a compliant-looking reading that skips the expensive step | `Skill and gate` | `adversarial-skill-gate.md` |
| 32 | Attempt the prose temptations verbatim and record whether the text refuses them | `Skill and gate` | `adversarial-skill-gate.md` |
| 33 | For a gate script, feed it the input it was written to catch, then the same input one character different | `Skill and gate` | `adversarial-skill-gate.md` |
| 34 | Build's hand-off names every committed program; closing review supplies them to `finalize-review`, which records command, artifact, digest and result | `Recording` | `adversarial.md` |
| 35 | Record every attempt that failed to break anything, for every artifact type | `Recording` | `adversarial.md` |
| 36 | `command` must be re-runnable by someone else in a clean tree | `Recording` | `adversarial.md` |
| 37 | `artifact` is where the case now lives; probes go under the change's evidence path, and promotion into the real suite happens only through a plan task | `Recording` | `adversarial.md` |
| 38 | Anything found that matters becomes a `finding` with an anchor and a fix, reaching the `findings` input of `finalize-review` | `Recording` | `adversarial.md` |

Count: 38 rules before the split, 38 after. Nothing added: the only text
that did not come from the pre-split document is each new file's title, its
one-line pointer back to the shared protocol, and the routing marker in
`adversarial.md`, none of which states a rule.
