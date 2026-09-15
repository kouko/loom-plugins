---
name: expert-mode
description: |
  Skip chosen Loom steps for one change. Only for the user typing /loom-code:expert-mode (Codex: $expert-mode); the agent never invokes it.
disable-model-invocation: true
---

# Expert mode

Talk to the user in the user's language. This skill proposes, shows and
reports; the checker decides what is skipped. The same procedure applies when
a station reaches it from ordinary conversation, such as "這次不用 review": the
agent reads this file, and the user still types the confirmation.

Checker prefix: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py` on
Claude Code, `python3 <injected loom-code plugin root>/scripts/loom_checker.py`
on Codex; on any other host the plugin root is the directory two levels above
this SKILL.md. Commands below write `loom_checker.py`. `<change-id>` is the active
change's id; when no intent exists yet, it is the dated kebab-case id the
change will use.

## 1. Map the words onto steps

Steps: `spec`, `plan`, `implementer`, `tdd`, `reviewers`, `adversarial`,
`blind-run`, `package-tests`. The intent, publication, the merge decision and
the attestation are not steps.

- Nothing after the entry point: list the steps with one example sentence and
  stop; nothing is recorded.
- Map the user's words, in any language, onto step names.
- When the user asks to skip the intent, say the intent is always kept and
  show the table of the remaining steps.
- A word that is no step (other than the intent, handled above): name the
  item, ask the user to rephrase, and show no confirmation line.

## 2. Propose, show, wait

Run `loom_checker.py selection propose <change-id> --origin user --skip <steps>`.
Show its run/skip table and one line in the user's language that tells the
user this: to apply it, type `/loom-code:expert-mode` (Codex: `$expert-mode`)
with the code shown, in any surrounding words. Then wait.

Only that typed confirmation applies. A reply such as "yes" or "對" binds
nothing: say so and repeat the confirmation line.

## 3. Report what bound

After a confirmation prompt, run `loom_checker.py selection show <change-id>`
and report its `run` and `skip` lists exactly. A Loom hook message shows the
same lists; when they differ from your table, say so and withdraw (§4).

If `bound` is false, tell the user the confirmation was not captured. Name
hook trust as the usual cause on Codex (its hooks run once the user trusts the
plugin), and a stale or mistyped code on Claude Code; show the current table and
code again and keep the full process.

Claim a skip is in effect only from `loom_checker.py selection show <change-id>`.

## 4. Withdraw and lapse

- After a Loom hook message that withdraws the selection, only confirm the
  full process resumed.
- On other withdrawal wording in any language (`取消`, `cancel`, `キャンセル`,
  `不對，剛剛那個不算`), run `loom_checker.py selection cancel <change-id>` and
  say the full process resumed.
- Show the table again only when the hook's lists differed from the table
  shown.
- After a rebase, or a merge of the default branch into the change, tell the
  user the bound selection lapsed and the full process resumed, then re-run
  `loom_checker.py selection propose` with the same steps and show the table
  and its code.

## Boundary

- Never evaluate a gate. `finalize-review` and `publish` re-read the records
  and waive only a bound skip.
- Local protection stops shortcuts, not deliberately disguised commands;
  independent CI stays the trust boundary.
- A reviewer rejection is recorded only when `closing-review` hands it to the checker
  (`selection record-failure`).
- `loom_checker.py selection skipped-review` lists merged changes on the
  default branch whose attestation skipped reviewers.
- A change with a bound selection publishes only from a checkout sharing the
  git common dir that holds its records; a fresh clone refuses it.
- Confirmation, finalization and publication must all run in the same attended
  Claude Code session. In a new session, re-run
  `loom_checker.py selection propose` and have the user type the confirmation
  again; a confirmation typed before `selection propose` has run in this
  session binds nothing; the code shown may be the same as before. A nested
  unattended session (such as `claude -p`, even wrapped in `timeout`) never
  binds. Codex exports no session variable, so on Codex only the command-text
  guard applies.
- On Antigravity CLI, or any other host that lacks prompt capture, a typed
  confirmation stays unrecorded: say that selections take effect only where
  prompts are captured, leave out the confirmation line, and keep the full
  process.
