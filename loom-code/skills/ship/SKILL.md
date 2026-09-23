---
name: ship
description: |
  Publish a reviewed branch and verify PR checks. Use after closing-review, normally with a matching attestation.
version: 1.1.0
---

# Ship

Ship validates publication state; it does not repeat functional verification.
It does not execute package tests or adversarial probes.
Write the PR body in the user's conversation language when the host can
establish it from the confirmed intent or active conversation. Repository
conventions still govern committed artifacts. Internal publication reports
remain English.

## 1. Confirm publication authorization

Read the intent and acceptance test report when one was required. A confirmed intent
with `publication: automatic — authorized <YYYY-MM-DD> by <name>` carries that
decision into Ship; do not ask again. Intent prose, status, or contract version
never implies authorization. A legacy intent without that machine-readable field
requires one publication decision before anything leaves the machine.
The user may still explicitly stop publication before the outward action.

At entry, run `loom_checker.py selection show <change-id>` and omit the prose
steps `selection show` lists as skipped (spec, plan, implementer, tdd,
acceptance-test), plus any step the user told you to skip in plain words;
[expert-mode](../expert-mode/SKILL.md) stays an optional route the user may
invoke. When `selection show` reports `bound: false` with a non-empty `skip`
field, the checker judged this change narrow: as you omit those steps, tell the
user its `narrow_change_line` field (`Skipped as a narrow change: <steps>`)
exactly as printed, rather than rebuilding it from conversation recall or the
raw `skip` ids. The default is the full flow:
skip a step only when the user tells you
to in plain words, then tell the user in one line which step is skipped and
continue. When you honour such a skip, write it straight into the PR body's
`Skipped by instruction:` line (§2); Ship only reads the plan's
`skipped-by-instruction:` lines and leaves the plan unchanged, because plan.md
is functional content and an appended line would make the attestation stale.
Never ask the user for a generated code to skip a step.

## 2. Prepare publication text

Ship owns one top-level PR body schema. Reconstruct it from the current intent,
plan, recomputed Git change, generated attestation, and available CI evidence;
do not depend on conversation recall. Use these headings exactly once:

```markdown
## Context
<original problem, relevant history, and why the change is being made now>

## Intended outcome
<the confirmed outcome and success conditions>

## Scope
<included work and explicitly excluded work>

## Decisions
<auditable decision summaries>

## Implementation
<what changed and which components own each responsibility>

## Behaviour change
<observable before-and-after behaviour>

## Verification
<review, tests, attestation, available CI evidence, and known limits>

## Risks and rollback
<remaining risks and a concrete recovery path>

## Follow-ups
<deferred work, or "None">
```
Use a Markdown table for any list‑type or comparison‑type information (options, trade‑offs, decision summaries, etc.). Do not use inline ①②③ lists or plain‑text enumerations.

Under the Verification heading, write the line `Verification status: <status>`,
where `<status>` is the status `publish` computes locally and prints on its
`Verification <status> for <head>` line: `valid`, `valid (skipped: <steps>)`,
`absent`, or `stale (<reason>)`. When the printed status differs from the
body, correct the body in place. Build the line
`Skipped by instruction: <steps>` from the plan's `skipped-by-instruction:`
lines plus any skip decided at Ship (§1), not from conversation recall; with
none recorded or decided, write no such line,
and the recomputed `(missing: …)` clause still discloses the absent records.
Copy the line `Skipped as a narrow change: <steps>` exactly as `selection show`
prints it in its `narrow_change_line` field, not from conversation recall or
the raw `skip` ids; when that field is null, write no such line.

When the attestation carries a selection, open the Verification section with
exactly these lines, filled from the attestation's `selection` field: one
`Skipped steps: <steps> — authority: <source> (<code>, <YYYY-MM-DD>)` line per
confirmation, then one `Prior failure: <step> <rule> <YYYY-MM-DD>` line per
prior failure. On a
mismatch, `publish` prints the expected lines. State that a
reviewer rejection `closing-review` never handed to the checker is unrecorded.

In the `<steps>` of the `Skipped by instruction:` and `Skipped steps:` lines,
write `acceptance-test` as `acceptance-test (independent acceptance testing)`;
every other step reads as recorded. The `Verification status:` and
`Skipped as a narrow change:` lines already arrive in that form from the checker.

Every decision summary states the chosen option, material alternatives,
trade-offs, supporting evidence, and observed or expected outcome. This is an
auditable rationale, never private or hidden chain-of-thought. Omit or label
unsupported claims as limitations instead of inventing an explanation.

Graph-bearing changes require a Mermaid diagram when they contain meaningful
decision branches, component interactions, state transitions, or
before-and-after behaviour flows and the relationship carries information.
Select the matching decision, architecture, sequence, state, or comparison
diagram and introduce it with accessible prose. Simple changes must omit
Mermaid diagrams; exactly one of those outcomes applies. Never add a fixed
diagram count or decorative graph.

Use `loom-workflow:git-memory` to classify the change and contribute durable
Decision, Learning, and Gotcha material inside this schema when earned. It does
not replace or reorder Ship's headings.
Always run its deterministic secrets scan. Known public repository, PR, issue,
task, and vendor identifiers need no semantic privacy judge; ambiguous
private-party text does. A semantic false positive needs an audited
`Privacy-Bypass-Reason`; secret findings cannot be bypassed.

Before publication, reject a body with a missing heading, evidence source that
was silently ignored, unsupported decision claim, hidden-reasoning claim, or a
diagram that is required by the relationships above but absent. Retired review
and probe accounting ledgers and their fields are not valid inputs.

Publication-only edits do not change the functional digest and do not return to
`closing-review`. Functional edits invalidate the attestation and do.

## 3. Publish once

Before publishing, run `python3 <loom-code>/scripts/loom_checker.py github-rules`
and relay its lines to the user. When it reports a missing rule, ask the user
in consequence form — from then on <trunk> accepts changes only through a PR
whose body check passes, for you too — then show the user the setup command
that `loom_checker.py github-rules --print-setup` prints, and run that setup
command only after the user explicitly agrees in conversation. Never run the
setup command unasked. When it reports `template not on <trunk>`, relay the
printed step to the user; add the template only after the user explicitly
agrees, as its own change and never inside the current change's PR, then run
`github-rules` again for the rules. When it reports that the rules could not be
confirmed, tell the user and continue publishing.

For an intent carrying automatic-publication authorization, pass its absolute
path to the installed plugin's one publication command:

```text
python3 <loom-code>/scripts/loom_checker.py publish --intent <absolute-intent-path> --title <title> --body-file <absolute-path>
```

For a legacy intent, obtain one publication decision and acknowledge it with:

```text
python3 <loom-code>/scripts/loom_checker.py publish --confirm-authorized --title <title> --body-file <absolute-path>
```

The `<title>` is a Conventional Commits subject whose type equals the current
branch's `<type>/` prefix, because it becomes the squash-merge commit.

The command validates the body, identifies the change from the branch
`<type>/<change-id>` or its one committed intent, and computes the
verification status locally and prints it. It then derives the origin repository, default
base, current branch, and exact refspec (destination/refspec safety); performs
a non-forced push; and opens or reuses one PR. Publishing proceeds without an
attestation: an absent or stale one is disclosed, not refused. Before pushing,
beyond authorization and repository safety, it refuses only a malformed body
(naming the heading), a `Skipped steps:` mismatch against a bound selection,
and an unidentified change. Do not run a
separate attestation preflight, construct Git push or PR-create commands, or
hand a refused publication command to the user to run; where a refusal names a
remedy, take it, and where it names none, report the refusal and stop.

The installed plugin's `PreToolUse` hook only reminds: a direct push or PR
create prints one line naming the branch's verification status. No
repository-local checker scaffold or hook-firing ledger is required.

## 4. Observe CI

The publication command reports the PR URL, inspects required CI immediately,
and checks again every 10 seconds while any required check remains pending.
It stops when all required checks pass, a required check fails or is cancelled,
or GitHub reports that user action is required. Optional checks do not keep the
command alive. Unchanged pending snapshots produce no repeated user-facing
output.

If checks remain pending after 360 polling intervals (60 minutes), stop and
report that a reliable terminal result could not be obtained. Treat an empty
required-check snapshot, including GitHub CLI's explicit no-checks response,
as registration delay. Check every 10 seconds for up to 60 seconds; if checks
are still absent on the final observation, report that no required checks are
registered and finish successfully. Other observation errors stop immediately.

Observation belongs only to the active publication process. Do not create a
scheduler, daemon, persistent polling record, or restart recovery mechanism.
Stopping the task or Desktop app stops observation.

CI is the external trust boundary. When required CI fails, the same active task
identifies the failed required checks and each available failure log; the
publication command's failure does not end the task. Missing required
diagnostics or permission, a safely unattributed failure, a persistent external
failure established from available evidence, or a required change to
requirements, visible behaviour, or guarantees is reported as a concrete
blocker. An unattributed failure must not be rerun automatically.

Keep a functional or test repair in the original change. When an existing test
already exposes the root cause, use it; otherwise add the smallest permanent
regression case. Run it to observe RED, apply the minimum fix under Build's
test-first discipline, and rerun it to observe GREEN. Every committed-file
change, including code, tests, and version files, invalidates the attestation
and resumes the same bounded Review episode at its next functional digest
without resetting the episode or adding another retry budget, then returns to
Ship. A PR title, body, or other publication data not committed to the
repository may be fixed in place and reuse the matching attestation.

## 5. Land after acceptance

After all checks pass, present the result and the acceptance test report when one
exists (decision point ③). Publication never authorizes or invokes merge; only
the maintainer's explicit acceptance does. Never type `gh pr merge` yourself:
merge through land, which checks the live PR body and discloses verification.
Publication authorization, including `publication: automatic`, is not
acceptance; always present the result and ask at decision point ③ before
running land. Before running land, invoke `loom-workflow:git-memory` for the
merge checkpoint.

On that acceptance, take the root of the change branch's worktree —
`git rev-parse --show-toplevel` run from that worktree, never the
task or main checkout — and land the change as one Bash command:

```text
cd '<absolute worktree root>' && python3 <loom-code>/scripts/loom_checker.py land --accepted-by <name>
```

`<name>` is the maintainer who accepted; it must match the intent originator or
the publication authorizer. Always render that absolute `cd`;
never rely on the Bash tool's workdir, because Codex may report the task root
rather than the executor worktree, and `land` acts on the worktree it runs in.
`land` removes that worktree, so the agent's next Bash command starts with the
`cd` printed on land's `next:` line. When no `next:` line is printed, keep the
current directory.

If land prints `Merged PR` and then a BLOCK, do not rerun `--accepted-by`;
resolve the named state and run `land --cleanup <branch>`. If it names a
failing non-required check, repair it as in §4.

For one merged change left from earlier work, run `land --cleanup <branch>`
through the same command. `land --sweep` lists merged changes, removes nothing,
and prints a token; pass `--sweep --confirm <token>` only after the maintainer
answers yes to the printed list.

## Handoff

Report the attestation digest when one exists, else the verification status
publish printed, publication checks, PR URL, CI state, and land's output.
